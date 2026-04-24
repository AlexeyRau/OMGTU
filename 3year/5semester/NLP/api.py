import os
import pathlib
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, CrossEncoder
from qdrant_client import QdrantClient
from ollama import Client as OllamaClient
import re

load_dotenv()

# Глобальные переменные для моделей
embedder = None
reranker = None
qdrant = None
ollama = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Загружаем модели один раз при старте сервера"""
    global embedder, reranker, qdrant, ollama
    print("Загружаем модели...")
    embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    reranker = CrossEncoder("DiTy/cross-encoder-russian-msmarco")
    qdrant = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
    )
    ollama = OllamaClient()
    print("✓ Модели загружены, сервер готов")
    yield
    print("Сервер останавливается...")


app = FastAPI(
    title="Constitution RAG API",
    description="API для поиска информации в Конституции РФ",
    version="1.0.0",
    lifespan=lifespan
)


# --- Схемы запроса и ответа ---

class QueryRequest(BaseModel):
    query: str

class Source(BaseModel):
    article_num: str
    chapter: str
    rerank_score: float

class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]


# --- Вспомогательные функции (те же что в 03_rag_pipeline.py) ---

def retrieve(query: str, top_k: int = 15) -> list[dict]:
    query_vector = embedder.encode(query).tolist()
    results = qdrant.query_points(
        collection_name="constitution",
        query=query_vector,
        limit=top_k
    ).points
    return [
        {
            "text": r.payload["text"],
            "article_num": r.payload["article_num"],
            "chapter": r.payload["chapter"],
            "score": r.score
        }
        for r in results
    ]


def rerank(query: str, candidates: list[dict], top_n: int = 5) -> list[dict]:
    pairs = [[query, c["text"]] for c in candidates]
    scores = reranker.predict(pairs)
    for i, doc in enumerate(candidates):
        doc["rerank_score"] = float(scores[i])
    reranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    return reranked[:top_n]

def is_relevant(top_docs: list[dict], threshold: float = 0.05) -> bool:
    """Если лучший rerank-score ниже порога — вопрос не по Конституции"""
    if not top_docs:
        return False
    return top_docs[0]["rerank_score"] >= threshold


def build_prompt(query: str, docs: list[dict]) -> str:
    context = ""
    for doc in docs:
        context += f"[Статья {doc['article_num']} | {doc['chapter']}]\n"
        context += f"{doc['text']}\n\n"

    return f"""Тебе предоставлены релевантные статьи из Конституции РФ. Твоя задача — дать точный и полезный ответ на вопрос пользователя, опираясь исключительно на предоставленный контекст.

ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА:
- Отвечай ТОЛЬКО на русском языке
- Отвечай только на основе предоставленных статей, не придумывай информацию
- Если в контексте нет ответа — честно скажи об этом
- Указывай номера статей, на которые опираешься
- Думай пошагово перед финальным ответом

Контекст из Конституции РФ:
{context}
Вопрос пользователя: {query}

Ответ на русском языке:"""

OFF_TOPIC_PHRASES = [
    "что ты написал", "прошлое сообщение", "системный промпт", 
    "твой промпт", "предыдущее сообщение"
]

def clean_response(text: str) -> str:
    """Убираем только китайские символы"""
    text = re.sub(r'[\u4e00-\u9fff\u3400-\u4dbf\uff00-\uffef]+', '', text)
    return text.strip()

@app.get("/")
def root():
    return {"message": "Constitution RAG API работает"}

@app.post("/ask", response_model=QueryResponse)
def ask(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Запрос не может быть пустым")

    query_lower = request.query.lower()
    if any(phrase in query_lower for phrase in OFF_TOPIC_PHRASES):
        return QueryResponse(
            answer="Я могу отвечать только на вопросы по тексту Конституции Российской Федерации.",
            sources=[]
        )

    candidates = retrieve(request.query)
    top_docs = rerank(request.query, candidates)

    # Проверяем релевантность по score реранкера
    if not is_relevant(top_docs, threshold=0.01):
        return QueryResponse(
            answer="Ваш вопрос не относится к Конституции Российской Федерации. Пожалуйста, задайте вопрос по тексту Конституции.",
            sources=[]
        )
    prompt = build_prompt(request.query, top_docs)


    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "system",
                "content": "Ты — юридический ассистент по Конституции РФ. Отвечай ТОЛЬКО на русском языке. Если вопрос не связан с Конституцией РФ — вежливо откажись отвечать."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    raw_answer = response.message.content
    print("="*60)
    print("RAW ОТВЕТ МОДЕЛИ:")
    print(raw_answer)
    print("="*60)

    cleaned_answer = clean_response(raw_answer)
    print("ПОСЛЕ ОЧИСТКИ:")
    print(cleaned_answer)
    print("="*60)
    
    return QueryResponse(
        answer=clean_response(response.message.content),
        sources=[
            Source(
                article_num=d["article_num"],
                chapter=d["chapter"],
                rerank_score=round(d["rerank_score"], 4)
            )
            for d in top_docs
        ]
    )