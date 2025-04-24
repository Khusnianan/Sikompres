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

def compress_image(image_file, output_name):
    image = Image.open(image_file)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=30)  # Lebih kecil kualitas = lebih kompres
    buffer.seek(0)
    return buffer, output_name + "_compressed.jpg"

def compress_text(file, output_name):
    text = file.read().decode("utf-8")
    compressed = text.encode("utf-8")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(output_name + "_compressed.txt", compressed)
    buffer.seek(0)
    return buffer, output_name + "_compressed.zip"

def compress_pdf(file, output_name):
    reader = PyPDF2.PdfReader(file)
    writer = PyPDF2.PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer, output_name + "_compressed.pdf"

if uploaded_file:
    file_type = uploaded_file.type
    file_name = os.path.splitext(uploaded_file.name)[0]

    if "image" in file_type:
        result, download_name = compress_image(uploaded_file, file_name)
        st.success("Gambar berhasil dikompres!")
        st.download_button("Download", result, file_name=download_name)
    
    elif "pdf" in file_type:
        result, download_name = compress_pdf(uploaded_file, file_name)
        st.success("PDF berhasil dikompres (struktur minimal)!")
        st.download_button("Download", result, file_name=download_name)
    
    elif "text" in file_type or uploaded_file.name.endswith(".txt"):
        result, download_name = compress_text(uploaded_file, file_name)
        st.success("File teks berhasil dikompres!")
        st.download_button("Download", result, file_name=download_name)
    else:
        st.error("Jenis file belum didukung.")
