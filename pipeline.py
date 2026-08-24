from pathlib import Path
import sqlite_vec
from ingest import ingest_text, ingest_images_from_pdf, extract_images_from_xrefs
from db import init_db
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from PIL import Image
from transformers import AutoProcessor, AutoModel
import torch

text_model= SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

image_model = AutoModel.from_pretrained("google/siglip-base-patch16-224")
image_processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")

def embed_text(text):

    embeddings = text_model.encode(text).tolist()
    return embeddings


def embed_image(image):
    inputs = image_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = image_model.get_image_features(**inputs)
    return outputs.pooler_output[0].tolist()


def ingest_and_store(file, db):
    db= init_db()
    cur = db.execute("INSERT INTO documents (filename) VALUES (?)", (Path(file).name,))
    doc_id = cur.lastrowid

    page_to_chunk_row_id = {}

    for i, chunk in enumerate(ingest_text(file)):
        chunk_id_str = f"{Path(file).stem}_p{chunk['page']}_{i}"
        text_embedding = embed_text(chunk["text"])

        cur = db.execute(
            "INSERT INTO chunks (chunk_id, doc_id, page_number, text) VALUES (?, ?, ?, ?)",
            (chunk_id_str, doc_id, chunk["page"], chunk["text"])
        )
        chunk_row_id = cur.lastrowid
        page_to_chunk_row_id[chunk["page"]] = chunk_row_id

        db.execute(
            "INSERT INTO chunk_vectors (rowid, embedding) VALUES (?, ?)",
            (chunk_row_id, sqlite_vec.serialize_float32(text_embedding))
        )

    image_info = ingest_images_from_pdf(file)
    for image_entry in extract_images_from_xrefs(file, image_info):
        matching_chunk_row_id = page_to_chunk_row_id.get(image_entry["page"])
        image_embedding = embed_image(image_entry["image"])

        cur = db.execute(
            "INSERT INTO images (doc_id, page_number, chunk_id) VALUES (?, ?, ?)",
            (doc_id, image_entry["page"], matching_chunk_row_id)
        )
        image_row_id = cur.lastrowid
        db.execute(
            "INSERT INTO image_vectors (rowid, embedding) VALUES (?, ?)",
            (image_row_id, sqlite_vec.serialize_float32(image_embedding))
        )

    db.commit()

if __name__ == "__main__":
    test_file = "test_data/mueller_report.pdf"
    
    ingest_and_store(test_file, init_db())
