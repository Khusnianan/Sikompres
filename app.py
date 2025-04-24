import streamlit as st
from PIL import Image
import os
import zipfile
import io
from PyPDF2 import PdfReader, PdfWriter

def get_size_in_kb(size_bytes):
    return round(size_bytes / 1024, 2)

def compress_image(uploaded_file):
    image = Image.open(uploaded_file)
    compressed_io = io.BytesIO()
    image.save(compressed_io, format='JPEG', quality=30)
    compressed_io.seek(0)
    return compressed_io

def compress_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    compressed_io = io.BytesIO()
    writer.write(compressed_io)
    compressed_io.seek(0)
    return compressed_io

def compress_text(uploaded_file):
    compressed_io = io.BytesIO()
    with zipfile.ZipFile(compressed_io, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(uploaded_file.name, uploaded_file.getvalue())
    compressed_io.seek(0)
    return compressed_io

st.title("🔻 Kompres File Online")

uploaded_file = st.file_uploader("Unggah file (gambar, PDF, atau teks):")

if uploaded_file is not None:
    file_size_kb = get_size_in_kb(len(uploaded_file.getvalue()))
    st.write("📦 Ukuran file asli:", file_size_kb, "KB")

    filename, ext = os.path.splitext(uploaded_file.name)
    compressed_data = None
    download_filename = filename + "_compressed" + ext

    if uploaded_file.type.startswith("image"):
        compressed_data = compress_image(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        compressed_data = compress_pdf(uploaded_file)
    elif uploaded_file.type.startswith("text") or ext == ".txt":
        compressed_data = compress_text(uploaded_file)
        download_filename = filename + "_compressed.zip"

    if compressed_data:
        compressed_size_kb = get_size_in_kb(len(compressed_data.getvalue()))
        st.write("🗜️ Ukuran file setelah kompres:", compressed_size_kb, "KB")
        st.download_button(
            label="⬇️ Unduh File Terkompresi",
            data=compressed_data,
            file_name=download_filename,
            mime="application/octet-stream"
        )
