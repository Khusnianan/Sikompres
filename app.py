import streamlit as st
from docx import Document
from PyPDF2 import PdfReader, PdfWriter
import os
import io

# Fungsi menghitung ukuran file
def get_size_in_kb(size_bytes):
    return round(size_bytes / 1024, 2)

# -------------------- RLE ENCODE / DECODE --------------------

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

def run_length_decode(text):
    import re
    pattern = re.compile(r'(\d+)(\D)')
    decompressed = ''.join([int(count) * char for count, char in pattern.findall(text)])
    return decompressed

# -------------------- FILE HANDLING FUNCTIONS --------------------

# Kompres file DOCX menggunakan RLE
def compress_docx(uploaded_file):
    doc = Document(uploaded_file)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    encoded_text = run_length_encode(full_text)

    compressed_io = io.BytesIO()
    compressed_io.write(encoded_text.encode('utf-8'))
    compressed_io.seek(0)
    return compressed_io, '.rle'

# Dekompres file RLE menjadi file TXT
def decompress_rle(uploaded_file):
    encoded_data = uploaded_file.read().decode('utf-8', errors='ignore')
    decoded_text = run_length_decode(encoded_data)

    decompressed_io = io.BytesIO()
    decompressed_io.write(decoded_text.encode('utf-8'))
    decompressed_io.seek(0)
    return decompressed_io, '.txt'

# Kompres file PDF (copy ulang)
def compress_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    compressed_io = io.BytesIO()
    writer.write(compressed_io)
    compressed_io.seek(0)
    return compressed_io, '.pdf'

# -------------------- UI LAYOUT --------------------

st.set_page_config(page_title="Kompres & Dekompres File", page_icon="🗜️")
st.title("🗜️ Kompres & Dekompres File Word / PDF")
st.markdown("Pilih apakah kamu ingin mengompres file atau mendekompres hasil RLE.")

mode = st.radio("Mode Operasi", ["Kompresi", "Dekomresi (khusus file .rle)"])

uploaded_file = st.file_uploader("📁 Unggah file:")

if uploaded_file is not None:
    file_size_kb = get_size_in_kb(len(uploaded_file.getvalue()))
    filename, ext = os.path.splitext(uploaded_file.name)
    result_io = None
    result_ext = ""
    download_filename = ""

    with st.spinner("⏳ Memproses file..."):

        if mode == "Kompresi":
            if ext == ".docx":
                result_io, result_ext = compress_docx(uploaded_file)
            elif ext == ".pdf":
                result_io, result_ext = compress_pdf(uploaded_file)
            else:
                st.error("❌ Format file tidak didukung untuk kompresi. Hanya .docx dan .pdf yang didukung.")
        else:  # DEKOMPRESI
            if ext == ".rle":
                result_io, result_ext = decompress_rle(uploaded_file)
            else:
                st.error("❌ Untuk dekompresi, hanya file .rle yang didukung.")

    if result_io:
        result_size_kb = get_size_in_kb(len(result_io.getvalue()))
        download_filename = filename + ("_compressed" if mode == "Kompresi" else "_decompressed") + result_ext

        col1, col2 = st.columns(2)
        col1.metric("📦 Ukuran Asli", f"{file_size_kb} KB")
        col2.metric("📤 Ukuran Hasil", f"{result_size_kb} KB")

        st.success("✅ Berhasil diproses!")
        st.download_button(
            label="⬇️ Unduh Hasil",
            data=result_io,
            file_name=download_filename,
            mime="application/octet-stream"
        )
