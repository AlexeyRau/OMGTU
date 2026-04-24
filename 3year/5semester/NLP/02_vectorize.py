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

    # Загружаем чанки
    chunks_path = script_dir / "data" / "chunks.json"
    print("Загружаем чанки...")
    chunks = load_chunks(str(chunks_path))
    print(f"Загружено чанков: {len(chunks)}")

    # Загружаем модель для эмбеддингов
    print("\nЗагружаем модель для эмбеддингов...")
    model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    print("✓ Модель загружена")

    # Векторизуем тексты
    print("\nВекторизуем чанки...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    print(f"✓ Размерность эмбеддингов: {embeddings.shape[1]}")

    # Подключаемся к Qdrant Cloud
    print("\nПодключаемся к Qdrant Cloud...")
    client = QdrantClient(
        url=os.environ["QDRANT_URL"],
        api_key=os.environ["QDRANT_API_KEY"],
    )
    print("✓ Подключение установлено")

    # Создаём коллекцию (удаляем старую если есть)
    collection_name = "constitution"
    existing = [c.name for c in client.get_collections().collections]
    if collection_name in existing:
        print(f"Коллекция '{collection_name}' уже существует, пересоздаём...")
        client.delete_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=embeddings.shape[1],  # 768 для mpnet
            distance=Distance.COSINE
        )
    )
    print(f"✓ Коллекция '{collection_name}' создана")

    # Формируем точки для загрузки
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

    # Загружаем в Qdrant
    print(f"\nЗагружаем {len(points)} векторов в Qdrant...")
    client.upsert(
        collection_name=collection_name,
        points=points
    )

    # Проверяем
    count = client.get_collection(collection_name).points_count
    print(f"✓ Сохранено документов: {count}")