import sqlite3
import sqlite_vec

def init_db(db_path="docint.db"):
    db = sqlite3.connect(db_path)
    db.execute("PRAGMA foreign_keys = ON")

    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)

    db.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            ingested_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY,
            chunk_id TEXT NOT NULL,
            doc_id INTEGER NOT NULL REFERENCES documents(id),
            page_number INTEGER NOT NULL,
            text TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            doc_id INTEGER NOT NULL REFERENCES documents(id),
            page_number INTEGER NOT NULL,
            chunk_id INTEGER REFERENCES chunks(id)
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS chunk_vectors USING vec0(
            embedding float[384]
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS image_vectors USING vec0(
            embedding float[768]
        );
    """)

    db.commit()
    return db


if __name__ == "__main__":
    init_db()
    print("Schema created.")