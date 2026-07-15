import pymupdf4llm
import pymupdf
import pathlib

def ingest_text(file):
    md_text = pymupdf4llm.to_markdown(
        file, 
        write_images=True, 
        image_path="output_images", 
        page_chunks=True, 
        use_layout=False, 
        show_progress=True
        )
    
    for page in md_text:

""" 
    pathlib.Path("output.md").write_bytes(md_text.encode())
 """


def ingest_images(file):
    doc = pymupdf.open(file)

    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images()