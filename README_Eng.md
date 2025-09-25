Конечно! Вот аккуратный английский перевод твоего `README.md`, готовый для GitHub:

````markdown
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
````

---

## 🔹 Usage

1. Clone the repository:

```bash
git clone https://github.com/username/habr-python-parser.git
cd habr-python-parser
```

2. Run the script:

```bash
python Paper_pars.py
```

3. After execution:

   * The database `Habr_paper_pars.db` will be created in the specified directory.
   * The `articles` table will be populated with data.
   * The first 5 records will be printed to the console for verification.

---

## 🔹 Database Structure

| Field            | Type    | Description                           |
| ---------------- | ------- | ------------------------------------- |
| `id`             | TEXT    | Unique article identifier (md5)       |
| `title`          | TEXT    | Article title                         |
| `description`    | TEXT    | Short description                     |
| `link`           | TEXT    | Link to the article                   |
| `article_number` | INTEGER | Sequential article number on the page |
| `page_number`    | INTEGER | Page number on Habr hub               |

---

## 🔹 Notes

* The script uses `requests` to download pages and `BeautifulSoup` for HTML parsing.
* If Habr’s structure changes, you may need to adjust the CSS selectors for titles and descriptions.
* For large amounts of data, it is recommended to add pauses between requests or use Selenium to avoid being blocked by Habr.

---

## 🔹 License

MIT License
