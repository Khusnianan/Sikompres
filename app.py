import streamlit as st
from PIL import Image
import os
import io
from PyPDF2 import PdfReader, PdfWriter

# Fungsi menghitung ukuran file
def get_size_in_kb(size_bytes):
    return round(size_bytes / 1024, 2)

# Fungsi kompresi gambar jadi WebP dengan kualitas rendah
def compress_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    compressed_io = io.BytesIO()
    image.save(compressed_io, format='WEBP', quality=10)
    compressed_io.seek(0)
    return compressed_io, '.webp'

# Fungsi kompresi PDF (sederhana, hanya copy ulang halaman)
def compress_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    compressed_io = io.BytesIO()
    writer.write(compressed_io)
    compressed_io.seek(0)
    return compressed_io, '.pdf'

# Fungsi RLE untuk kompresi teks
def run_length_encode(text):
    if not text:
        return ""
    compressed = []
    prev_char = text[0]
    count = 1
    for char in text[1:]:
        if char == prev_char:
            count += 1
        else:
            compressed.append(f"{count}{prev_char}")
            prev_char = char
            count = 1
    compressed.append(f"{count}{prev_char}")
    return ''.join(compressed)

# Fungsi kompresi teks dengan RLE
def compress_text(uploaded_file):
    text_data = uploaded_file.read().decode('utf-8', errors='ignore')  # baca teks dari file
    encoded_text = run_length_encode(text_data)
    
    compressed_io = io.BytesIO()
    compressed_io.write(encoded_text.encode('utf-8'))
    compressed_io.seek(0)
    return compressed_io, '.rle'

# ---------------------- UI Layout ----------------------

st.set_page_config(page_title="Kompres File", page_icon="🗜️")
st.title("🗜️ Kompres File Online")
st.markdown("📁 *Unggah file dan kami akan memperkecil ukurannya untukmu!*")

uploaded_file = st.file_uploader("Pilih file gambar, PDF, atau teks yang ingin dikompres:")

if uploaded_file is not None:
    with st.spinner("🔄 Mengompres file..."):
        file_size_kb = get_size_in_kb(len(uploaded_file.getvalue()))
        filename, ext = os.path.splitext(uploaded_file.name)
        compressed_data = None
        new_ext = ext  # default ekstensi

        # Tentukan metode kompresi berdasarkan jenis file
        if uploaded_file.type.startswith("image"):
            compressed_data, new_ext = compress_image(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            compressed_data, new_ext = compress_pdf(uploaded_file)
        elif uploaded_file.type.startswith("text") or ext == ".txt":
            compressed_data, new_ext = compress_text(uploaded_file)

        if compressed_data:
            compressed_size_kb = get_size_in_kb(len(compressed_data.getvalue()))
            download_filename = filename + "_compressed" + new_ext

            col1, col2 = st.columns(2)
            col1.metric("📦 Ukuran Asli", f"{file_size_kb} KB")
            col2.metric("🗜️ Ukuran Terkompresi", f"{compressed_size_kb} KB")

            st.success("✅ Kompresi selesai!")
            st.download_button(
                label="⬇️ Unduh File Terkompresi",
                data=compressed_data,
                file_name=download_filename,
                mime="application/octet-stream"
            )
