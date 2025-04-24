import streamlit as st
import os
from PIL import Image
import io
import PyPDF2
import zipfile

st.set_page_config(page_title="File Kompresor", layout="centered")

st.title("📦 File Kompresor")
st.write("Upload file dan dapatkan versi terkompresinya.")

uploaded_file = st.file_uploader("Upload file (Gambar, PDF, atau .txt)", type=["jpg", "jpeg", "png", "pdf", "txt"])

def compress_image(image_file):
    image = Image.open(image_file)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=40)  # 40% kualitas
    buffer.seek(0)
    return buffer

def compress_text(file):
    text = file.read().decode("utf-8")
    compressed = text.encode("utf-8")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("compressed.txt", compressed)
    buffer.seek(0)
    return buffer

def compress_pdf(file):
    reader = PyPDF2.PdfReader(file)
    writer = PyPDF2.PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer

if uploaded_file:
    file_type = uploaded_file.type

    if "image" in file_type:
        result = compress_image(uploaded_file)
        st.success("Gambar berhasil dikompres!")
        st.download_button("Download Gambar Terkompresi", result, file_name="compressed.jpg")
    
    elif "pdf" in file_type:
        result = compress_pdf(uploaded_file)
        st.success("PDF berhasil dikompres (struktur minimal)!")
        st.download_button("Download PDF Terkompresi", result, file_name="compressed.pdf")
    
    elif "text" in file_type or uploaded_file.name.endswith(".txt"):
        result = compress_text(uploaded_file)
        st.success("File teks berhasil dikompres!")
        st.download_button("Download Teks Terkompresi (.zip)", result, file_name="compressed_text.zip")
    else:
        st.error("Jenis file belum didukung.")
