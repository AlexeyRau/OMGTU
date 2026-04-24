import re
from docx import Document
import json
import pathlib

def load_constitution(path: str) -> str:
    """Загружаем текст из docx"""
    doc = Document(path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    return full_text


def parse_articles(text: str) -> list[dict]:
    chunks = []
    
    # Обновленный паттерн: ищем цифры, за которыми может следовать точка и еще цифры
    # \d+(?:\.\d+)? — найдет "67" или "67.1"
    pattern = r'Статья\s+(\d+(?:\.\d+)?)'
    matches = list(re.finditer(pattern, text))
    
    for i, match in enumerate(matches):
        article_id = match.group(1) # Теперь это строка, например "67.1"
        start = match.start()
        
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)
        
        article_text = text[start:end].strip()
        
        if len(article_text) < 20:
            continue
        
        chunks.append({
            "article_num": article_id, # Оставляем строкой
            "text": article_text,
        })
    
    seen = set()
    unique_chunks = []
    for chunk in chunks:
        if chunk["article_num"] not in seen:
            seen.add(chunk["article_num"])
            unique_chunks.append(chunk)

    return unique_chunks


def find_chapter(text: str, article_num: str) -> str:
    """Определяем главу, переводя номер в float для сравнения"""
    chapter_pattern = r'ГЛАВА\s+(\d+)[.\s]*\n([^\n]+)'
    article_pattern = r'Статья\s+(\d+(?:\.\d+)?)'
    
    chapters = list(re.finditer(chapter_pattern, text))
    
    # Преобразуем "67.1" в 67.1 для математического сравнения
    try:
        current_art_val = float(article_num)
    except ValueError:
        return "Неизвестно"

    for j, ch_match in enumerate(chapters):
        ch_start = ch_match.start()
        ch_end = chapters[j+1].start() if j+1 < len(chapters) else len(text)
        chapter_text = text[ch_start:ch_end]
        
        articles_in_chapter = re.findall(article_pattern, chapter_text)
        if articles_in_chapter:
            # Сравниваем как числа
            first_article = float(articles_in_chapter[0])
            last_article = float(articles_in_chapter[-1])
            
            if first_article <= current_art_val <= last_article:
                chapter_num = ch_match.group(1)
                chapter_name = ch_match.group(2).strip()
                return f"Глава {chapter_num}. {chapter_name}"
    
    return "Неизвестно"


if __name__ == "__main__":
    # Загружаем
    
    script_dir = pathlib.Path(__file__).parent.resolve()
    file_path = script_dir / "data" / "constitutionrf.docx"

    print(f"Ищем файл по пути: {file_path}")

    if not file_path.exists():
        print(f"❌ Ошибка: Файл не найден по пути {file_path}")
    else:
        print("Загружаем документ...")
        text = load_constitution(str(file_path))
        
        # Парсим статьи
        print("Нарезаем на чанки...")
        chunks = parse_articles(text)
    
    # Добавляем информацию о главе
    for chunk in chunks:
        chunk["chapter"] = find_chapter(text, chunk["article_num"])
    
    # Смотрим что получилось
    print(f"\nВсего статей найдено: {len(chunks)}")
    print("\n--- Первые 3 чанка ---")
    for chunk in chunks[:3]:
        print(f"\n[{chunk['chapter']}]")
        print(f"Номер статьи: {chunk['article_num']}")
        print(f"Текст: {chunk['text'][:200]}...")
    
    # Сохраняем в json чтобы переиспользовать на следующем шаге
    output_json = script_dir / "data" / "chunks.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
        
    print(f"\n✓ Чанки сохранены в {output_json}")