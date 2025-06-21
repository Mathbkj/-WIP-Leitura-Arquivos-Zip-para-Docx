
import pytesseract as image_reader
import re
from PIL import Image
from pypdf import PdfReader
from pathlib import Path
from docx.shared import Pt
from docx.document import Document as DocFunc
from docx.enum.text import WD_ALIGN_PARAGRAPH

def read_pdf_from_path(path:Path):
    reader = PdfReader(path)
    all_text = ""
    for i,page in enumerate(reader.pages):
        page_text = page.extract_text().strip()
        if not page_text:
            continue
        all_text+=f"\n--- Page {i+1} ---\n{page_text}\n"

    print(f"PDF Content:\n{all_text}")
    return all_text    


def read_pic_from_path(path: Path):
    image = Image.open(path)
    text:str = image_reader.image_to_string(image, lang='por')
    
    cleaned_text = re.sub(r'[ \t]+', ' ', text)  # collapse multiple spaces/tabs
    cleaned_text = re.sub(r' *\n *', '\n', cleaned_text)  # clean newlines
    cleaned_text = cleaned_text.strip()

    # Optional: pretty title for display
    header = "\n" + "=" * 40 + "\n🖼️  Conteúdo da Imagem\n" + "=" * 40

    print(f"{header}\n{cleaned_text}\n{'=' * 40}")
    return cleaned_text

def add_section(doc: DocFunc, title: str, content: str):
    # Add title
    heading = doc.add_heading(title, level=1)
    heading.alignment = WD_ALIGN_PARAGRAPH.LEFT
    # Add paragraph(s)
    for p in content.strip().split('\n'):
        if p.strip():
            p = doc.add_paragraph(p)
            if not p.style:break
            p.style.font.size=Pt(11)
