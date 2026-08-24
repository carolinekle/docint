import sqlite3
import sqlite_vec
from pipeline import embed_image
from PIL import Image

db = sqlite3.connect("docint.db")
db.enable_load_extension(True)
sqlite_vec.load(db)
db.enable_load_extension(False)

query_image = Image.open("test_data/test.png")  
query_embedding = embed_image(query_image)

results = db.execute(
    """
    SELECT images.page_number, matches.distance
    FROM (
        SELECT rowid, distance
        FROM image_vectors
        WHERE embedding MATCH ? AND k = 5
        ORDER BY distance
    ) AS matches
    JOIN images ON images.id = matches.rowid
    ORDER BY matches.distance
    """,
    (sqlite_vec.serialize_float32(query_embedding),)
).fetchall()

for page, dist in results:
    print(f"page {page} (dist {dist:.4f})")