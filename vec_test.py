import sqlite3
import sqlite_vec


db = sqlite3.connect(":memory:")

db.enable_load_extension(True)

sqlite_vec.load(db)

db.enable_load_extension(False)

db.execute("""
    CREATE VIRTUAL TABLE vec_docs USING vec0 (
    embedding float[4])
""")

print(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())

db.execute(
    "INSERT INTO vec_docs (rowid, embedding) VALUES (?, ?)",
    (1, sqlite_vec.serialize_float32([0.1, 0.2, 0.3, 0.4]))
)

result = db.execute("SELECT rowid, embedding FROM vec_docs").fetchall()
print(result)
print("sqlite-vec is working")