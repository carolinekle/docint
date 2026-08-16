import pymupdf4llm
import pymupdf
import pathlib
from pathlib import Path
from PIL import Image
import io

#langchain splitter later
def ingest_text(file):
    data = pymupdf4llm.to_markdown(
        
        file, 
        write_images=False,  
        page_chunks=True, 
        use_layout=False, 
        show_progress=True, 
        header=False, 
        footer=False
        )
    print(data[0].get("metadata"))
    chunk_list=[]
    for page in data:
        chunk = dict(
            text = page["text"], 
            page = page["page"], 
            file = Path(file).name
            )
        chunk_list.append(chunk)
    return chunk_list
""" 
pathlib.Path("output.md").write_bytes(md_text.encode())
"""

def ingest_images_from_pdf(file):
    doc = pymupdf.open(file)
    image_list = []
    for page_index in range(len(doc)):
        page = doc[page_index]

        for image in page.get_images():
            xref = image[0]
        image_list.append({"xref": xref, "page": page_index})
    return image_list

#provide mechanism to avoid multiple extracts because there may be repeats
def extract_images_from_xrefs(file, image_info):
    doc = pymupdf.open(file)
    seen = set()
    extracted =[]
    for entry in image_info:
        xref = entry["xref"]
        if xref in seen:
            continue
        seen.add(xref)

        image_dict= doc.extract_image(xref)
        image = Image.open(io.BytesIO(image_dict["image"]))
        extracted.append({
            "image": image,
            "page": entry["page"],
            "xref": xref,
            "source": Path(file).name
        })
    return extracted


if __name__ == "__main__":
    test_file = "test_data/test.pdf"
    image_info = ingest_images_from_pdf(test_file)
    
    extract = extract_images_from_xrefs(test_file, image_info)
    print(len(image_info))
    print(extract[0])
    print(extract[1])
    
    extract[0]["image"].save("test_output.png")
    extract[1]["image"].save("test2_output.png")
    chunks = ingest_text(test_file)
    print(chunks[0]["text"])
    print(chunks[1]["text"])