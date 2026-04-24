import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, CrossEncoder
from qdrant_client import QdrantClient
from ollama import Client as OllamaClient

load_dotenv()

embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
reranker = CrossEncoder("DiTy/cross-encoder-russian-msmarco")
qdrant = QdrantClient(
    url=os.environ["QDRANT_URL"],
    api_key=os.environ["QDRANT_API_KEY"],
)
ollama = OllamaClient()

def retrieve(query: str, top_k: int = 10) -> list[dict]:
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

def rerank(query: str, candidates: list[dict], top_n: int = 3) -> list[dict]:
    pairs = [[query, c["text"]] for c in candidates]
    scores = reranker.predict(pairs)

    for i, doc in enumerate(candidates):
        doc["rerank_score"] = float(scores[i])

    reranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    return reranked[:top_n]


def build_prompt(query: str, docs: list[dict]) -> str:
    context = ""
    for doc in docs:
        context += f"[Статья {doc['article_num']} | {doc['chapter']}]\n"
        context += f"{doc['text']}\n\n"

    prompt = f"""Ты — юридический ассистент, который помогает пользователям находить информацию в Конституции Российской Федерации.

Тебе предоставлены релевантные статьи из Конституции РФ. Твоя задача — дать точный и полезный ответ на вопрос пользователя, опираясь исключительно на предоставленный контекст.

ОБЯЗАТЕЛЬНЫЕ ПРАВИЛА:
- Отвечай ТОЛЬКО на русском языке, независимо ни от каких обстоятельств
- Отвечай только на основе предоставленных статей, не придумывай информацию
- Если в контексте нет ответа на вопрос — честно скажи об этом
- Указывай номера статей, на которые опираешься
- Думай пошагово перед тем как дать финальный ответ

Контекст из Конституции РФ:
{context}
Вопрос пользователя: {query}

Ответ на русском языке:"""
    return prompt


def ask(query: str) -> dict:
    candidates = retrieve(query, top_k=10)

    top_docs = rerank(query, candidates, top_n=3)

    prompt = build_prompt(query, top_docs)
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.message.content,
        "sources": [
            {
                "article_num": d["article_num"],
                "chapter": d["chapter"],
                "rerank_score": round(d["rerank_score"], 4)
            }
            for d in top_docs
        ]
    }


if __name__ == "__main__":
    test_queries = [
        "Какие права имеет человек на свободу слова?",
        "Кто является верховным главнокомандующим?",
        "Сколько лет должно быть президенту?"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Вопрос: {query}")
        print('='*60)
        result = ask(query)
        print(f"Ответ:\n{result['answer']}")
        print(f"\nИсточники:")
        for s in result["sources"]:
            print(f"  - Статья {s['article_num']} ({s['chapter']}) | rerank: {s['rerank_score']}")