import pymupdf4llm
import pymupdf
import pathlib
from pathlib import Path

def ingest_text(file):
    data = pymupdf4llm.to_markdown(
        file, 
        write_images=True, 
        image_path="output_images", 
        page_chunks=True, 
        use_layout=False, 
        show_progress=True
        )


    for page in data:
        chunk = dict(
            text = data["text"], 
            page = data["page"], 
            file = Path(data["file"]).name
            )
        return chunk
""" 
pathlib.Path("output.md").write_bytes(md_text.encode())
"""


def ingest_images(file):
    doc = pymupdf.open(file)

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images()