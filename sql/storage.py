import sqlite3

DB_PATH = "search.engine.db"


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pages (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            url        TEXT    NOT NULL UNIQUE,
            title      TEXT,
            content    TEXT,
            crawled_at TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS links (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            from_page_id INTEGER NOT NULL,
            to_url       TEXT    NOT NULL,
            FOREIGN KEY (from_page_id) REFERENCES pages(id) ON DELETE CASCADE,
            UNIQUE (from_page_id, to_url)
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_links_from ON links(from_page_id)"
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_links_to ON links(to_url)")
    conn.commit()


def save_page(conn: sqlite3.Connection, page: dict) -> int:
    if not page.get("url"):
        raise ValueError("page must contain a url")

    unique_links = list(dict.fromkeys(page.get("links", [])))

    with conn:
        conn.execute(
            """
            INSERT INTO pages (url, title, content)
            VALUES (?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                title      = excluded.title,
                content    = excluded.content,
                crawled_at = CURRENT_TIMESTAMP
            """,
            (page["url"], page.get("title"), page.get("content")),
        )
        page_id = conn.execute(
            "SELECT id FROM pages WHERE url = ?", (page["url"],)
        ).fetchone()["id"]

        conn.execute("DELETE FROM links WHERE from_page_id = ?", (page_id,))
        conn.executemany(
            "INSERT OR IGNORE INTO links (from_page_id, to_url) VALUES (?, ?)",
            [(page_id, link) for link in unique_links],
        )

    return page_id


def get_page(conn: sqlite3.Connection, page_id: int) -> dict | None:
    row = conn.execute(
        "SELECT id, url, title, content, crawled_at FROM pages WHERE id = ?",
        (page_id,),
    ).fetchone()
    if row is None:
        return None

    page = dict(row)
    page["links"] = [
        r["to_url"]
        for r in conn.execute(
            "SELECT to_url FROM links WHERE from_page_id = ? ORDER BY id",
            (page_id,),
        )
    ]
    return page