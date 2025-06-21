import streamlit as st
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from models.SupportedTypes import SupportedTypes
from modules.funcs import *
from docx import Document
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


supported_types = [extension.value for extension in SupportedTypes]

st.set_page_config(layout="wide", page_title="ZipxT3xt😎")

st.title("ZipxT3xt😎")
st.write("Faça um upload de um arquivo zip e obtenha o texto de cada arquivo formatado em um arquivo .docx")
uploaded_zip = st.file_uploader(
    "📁 Faça o upload de um arquivo zip", key="upload", type=["zip"])

if uploaded_zip is not None:
    zip_path = Path("temp.zip")
    zip_path.write_bytes(uploaded_zip.read())

    extracted_path = Path("temp_extracted")
    extracted_path.mkdir(exist_ok=True)

    with ZipFile(zip_path, "r") as file:
        file.extractall(extracted_path)

    file_paths = sorted(p for p in extracted_path.iterdir(
    ) if p.suffix.lower() in ['.pdf', '.jpg', 'jpeg', '.png'])

    doc = Document()

    content = ""

    for path in file_paths:
        try:
            if not path.suffix.lower() in supported_types:
                raise RuntimeError(
                    "Um dos arquivos não é um arquivo permitido (.pdf, .jpg, .jpeg, .png)")
        except ValueError as err:
            st.error(f'🚨 Erro:{err}')
        except Exception as err:
            st.error(f'🚨 Erro:{err}')
        else:
            if path.suffix.lower() == supported_types[0]:
                content = read_pdf_from_path(path)
            else:
                content = read_pic_from_path(path)
                
            st.info(f"🔼 Arquivo {path.name} adicionado com sucesso")
            add_section(doc=doc, title=path.stem, content=content)

    st.success(f"✅ Documento docx gerado com sucesso.")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        "⬇️ Baixar documento",
        buffer,
        "resultado.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        key="download",

    )
