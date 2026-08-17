import sqlite3
import sqlite_vec

db = sqlite3.connect("vector_store.db")

db.enable_load_extension(True)

sqlite_vec.load(db)

db.enable_load_extension(False)

db.execute("""
    CREATE TABLE IF NOT EXISTS docs(
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL, 
    body TEXT NOT NULL, 
    ingested_at TIME datetime(now)
    )
    
"""
)

db.execute(""" 
    CREATE VIRTUAL TABLE IF NOT EXISTS chunk_vectors USING vec0(
        embedding float[384]
    )
""")

db.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS image_vectors USING vec0(
        embedding float[384]
    )
""")

