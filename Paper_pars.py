import requests
from bs4 import BeautifulSoup
import sqlite3
import logging
import hashlib
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_PATH = r"D:\Programm and code\Python\Project in progress\Habr_paper_pars\Habr_paper_pars2.db"
BASE_URL = "https://habr.com/ru/hubs/python/articles/"

def create_database():
    # Создаём папку, если её нет
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    db_exists = os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            link TEXT,
            article_number INTEGER,
            page_number INTEGER
        )
    """)
    conn.commit()
    conn.close()
    if db_exists:
        logging.info(f"✅ База данных '{DB_PATH}' существует, таблица 'articles' проверена")
    else:
        logging.info(f"✅ База данных '{DB_PATH}' создана и таблица 'articles' готова")

def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении HTML: {e}")
        return None

def extract_articles(html, page_number):
    soup = BeautifulSoup(html, "html.parser")
    articles_data = []

    articles = soup.find_all("article")
    if not articles:
        logging.warning("⚠️ Статьи не найдены")
        return articles_data

    for idx, article in enumerate(articles, start=1):
        # Название и ссылка
        title_tag = article.find("h2")
        if title_tag:
            a_tag = title_tag.find("a", href=True)
            title = a_tag.get_text(strip=True)
            link = "https://habr.com" + a_tag['href']
        else:
            title = "Название не найдено"
            link = "#"

        # Краткое описание
        desc_tag = article.find("div", class_="tm-article-body tm-article-snippet__lead")
        if not desc_tag:
            desc_tag = article.find("div", class_="article-formatted-body")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # Уникальный ID
        uid = hashlib.md5(link.encode("utf-8")).hexdigest()

        articles_data.append((uid, title, description, link, idx, page_number))

    logging.info(f"✅ Извлечено {len(articles_data)} статей на странице {page_number}")
    return articles_data

def insert_articles(data):
    if not data:
        logging.warning("⚠️ Нет данных для вставки")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.executemany(
            """
            INSERT OR IGNORE INTO articles 
            (id, title, description, link, article_number, page_number) 
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            data
        )
        conn.commit()
        logging.info(f"✅ Вставлено {cursor.rowcount} новых записей в БД")
    except Exception as e:
        logging.error(f"Ошибка при вставке данных: {e}")
    finally:
        conn.close()

def show_sample(n=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM articles LIMIT ?", (n,))
        rows = cursor.fetchall()
        logging.info(f"📊 Первые {n} записей в базе:")
        for row in rows:
            print(row)
    except Exception as e:
        logging.error(f"Ошибка при чтении данных из базы: {e}")
    finally:
        conn.close()

def main():
    create_database()
    all_data = []

    for page in range(1, 6):  # первые 5 страниц
        url = BASE_URL if page == 1 else f"{BASE_URL}page{page}/"
        logging.info(f"📄 Скачиваем страницу {page}: {url}")
        html = get_html(url)
        if not html:
            logging.error(f"❌ Не удалось скачать страницу {page}")
            continue

        page_data = extract_articles(html, page_number=page)
        all_data.extend(page_data)

    insert_articles(all_data)
    show_sample()
    logging.info("🎉 Парсинг Habr Python-хаба завершён успешно")

if __name__ == "__main__":
    main()
