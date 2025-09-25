# Habr Python Articles Parser

This parser collects articles from the [Python hub on Habr](https://habr.com/ru/hubs/python/articles/), extracting titles, links, short descriptions, as well as adding a unique ID, article number on the page, and page number. All data is stored in a local SQLite database.

---

## 🔹 Features

- Parsing the **first 5 pages** of the Habr Python hub.
- Extracts:
  - `title` — article title.
  - `link` — link to the article.
  - `description` — short description.
  - `id` — unique article identifier (md5 of the link).
  - `article_number` — article's sequential number on the page.
  - `page_number` — page number on Habr.
- Saves data into a **SQLite** database.
- Automatically creates the database and table if they do not exist.
- Logs all actions, including the number of records processed.

---

## 🔹 Requirements

- Python 3.10+  
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `sqlite3` (standard library)
  - `hashlib` (standard library)
  - `logging` (standard library)
  - `os` (standard library)

Install external libraries with:

```bash
pip install requests beautifulsoup4
