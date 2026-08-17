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
    CREATE VIRTUAL TABLE IF NOT EXISTS text_vectors USING vec0(
        embedding float[384]
    )
""")

db.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS image_vectors USING vec0(
        embedding float[384]
    )
""")
# Image -> images table, then image_vectors
cur = db.execute(
    "INSERT INTO notes (title, body) VALUES (?, ?)",
    ("Grocery list", "eggs, oat milk, coffee")
)

chunk_id = cur.lastrowid

fake_embedding = [0.1] * 384  # stand-in for model.encode(body)
db.execute(
    "INSERT INTO text_vectors (rowid, embedding) VALUES (?, ?, ?, ?)",
    (chunk_id, sqlite_vec.serialize_float32(fake_embedding))
)
db.commit()

# Text chunk -> chunks table, then chunk_vectors
cur = db.execute(
    "INSERT INTO notes (title, body) VALUES (?, ?)",
    ("Grocery list", "eggs, oat milk, coffee")
)

doc_id = cur.lastrowid

db.execute(
    "INSERT INTO image_vectors (rowid, embedding) VALUES (?, ?)",
    (doc_id, sqlite_vec.serialize_float32(fake_embedding))
)
db.commit()

query_embedding = [0.1] * 384
results = db.execute("""
    SELECT docs.title, docs.body, note_vectors.distance
    FROM note_vectors
    JOIN notes ON notes.id = note_vectors.rowid
    WHERE note_vectors.embedding MATCH ?
    ORDER BY distance
    LIMIT 3
""", (sqlite_vec.serialize_float32(query_embedding),)).fetchall()