import json
import pathlib
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
from dotenv import load_dotenv
load_dotenv()

def load_chunks(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent.resolve()

    chunks_path = script_dir / "data" / "chunks.json"
    print("Загрузка чанков...")
    chunks = load_chunks(str(chunks_path))
    print(f"Загружено чанков: {len(chunks)}")

    print("\nЗагрузка модели для эмбеддингов...")
    model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    print("Модель загружена")

    print("\nВекторизация чанков...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    print(f"Размерность эмбеддингов: {embeddings.shape[1]}")

    client = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
    )

    collection_name = "constitution"
    existing = [c.name for c in client.get_collections().collections]
    if collection_name in existing:
        print(f"Коллекция '{collection_name}' уже существует, пересоздаём...")
        client.delete_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=embeddings.shape[1],
            distance=Distance.COSINE
        )
    )
    print(f"Коллекция '{collection_name}' создана")

    points = [
        PointStruct(
            id=i,
            vector=embeddings[i].tolist(),
            payload={
                "article_num": chunk["article_num"],
                "chapter": chunk["chapter"],
                "text": chunk["text"]
            }
        )
        for i, chunk in enumerate(chunks)
    ]

    print(f"\nЗагрузка {len(points)} векторов в Qdrant...")
    client.upsert(
        collection_name=collection_name,
        points=points
    )