import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
import os
import io

# -------------------- CONSTANTS --------------------
MARKER = b'\x00'  # Penanda byte khusus untuk kompresi biner


# -------------------- RLE ALGORITHM (Binary) --------------------

def rle_compress_binary(data: bytes) -> bytes:
    """Kompresi data biner dengan RLE menggunakan penanda khusus"""
    output = bytearray()
    i = 0
    while i < len(data):
        count = 1
        while i + count < len(data) and data[i] == data[i + count] and count < 255:
            count += 1

        if count >= 4 or data[i] == MARKER[0]:
            output.append(MARKER[0])
            if data[i] == MARKER[0]:
                output.append(0)  # Escape untuk marker asli
            else:
                output.append(count)
                output.append(data[i])
        else:
            output.extend(data[i:i + count])
        i += count
    return bytes(output)


def rle_decompress_binary(data: bytes) -> bytes:
    """Dekompresi data biner hasil RLE dengan penanda khusus"""
    output = bytearray()
    i = 0
    while i < len(data):
        if data[i] == MARKER[0]:
            i += 1
            if data[i] == 0:
                output.append(MARKER[0])
                i += 1
            else:
                count = data[i]
                byte = data[i + 1]
                output.extend([byte] * count)
                i += 2
        else:
            output.append(data[i])
            i += 1
    return bytes(output)


# -------------------- FILE HANDLING --------------------

def extract_text_from_docx(file) -> bytes:
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.encode('utf-8')


def create_docx_from_text(text_bytes: bytes) -> io.BytesIO:
    text = text_bytes.decode('utf-8', errors='ignore')
    doc = Document()
    doc.add_paragraph(text)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def extract_text_from_pdf(file) -> bytes:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.encode('utf-8')


def create_txt_buffer(content: bytes) -> io.BytesIO:
    buffer = io.BytesIO()
    buffer.write(content)
    buffer.seek(0)
    return buffer


# -------------------- UI STREAMLIT --------------------

st.set_page_config(page_title="SiKompres", page_icon="🗜️")
st.title("🗜️ SiKompres")
st.markdown("🔧 Kompresi & Dekompresi File `.docx`, `.txt`, dan `.pdf` menggunakan **Modified RLE**.")

mode = st.radio("Pilih Mode:", ["Kompresi", "Dekompresi"])
uploaded_file = st.file_uploader("Unggah file (.docx, .txt, .pdf)", type=["docx", "txt", "pdf"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    filename, ext = os.path.splitext(uploaded_file.name)
    result_io = io.BytesIO()
    result_ext = ext

    with st.spinner("⏳ Memproses file..."):
        original_size_kb = round(len(file_bytes) / 1024, 2)

        # ------- KOMpresi -------
        if mode == "Kompresi":
            if ext == ".docx":
                content = extract_text_from_docx(io.BytesIO(file_bytes))
                compressed = rle_compress_binary(content)
                result_io = create_docx_from_text(compressed)
            elif ext == ".txt":
                content = file_bytes
                compressed = rle_compress_binary(content)
                result_io = create_txt_buffer(compressed)
            elif ext == ".pdf":
                content = extract_text_from_pdf(io.BytesIO(file_bytes))
                compressed = rle_compress_binary(content)
                result_io = create_txt_buffer(compressed)
                result_ext = ".txt"  # hasil dari PDF dikompresi ke .txt

        # ------- DEkompresi -------
        else:
            if ext == ".docx":
                content = extract_text_from_docx(io.BytesIO(file_bytes))
                decompressed = rle_decompress_binary(content)
                result_io = create_docx_from_text(decompressed)
            elif ext == ".txt":
                content = file_bytes
                decompressed = rle_decompress_binary(content)
                result_io = create_txt_buffer(decompressed)
            elif ext == ".pdf":
                st.warning("PDF tidak dapat didekompresi langsung. Harap gunakan file hasil kompresi (.txt/.docx).")
                result_io = None

        if result_io:
            result_size_kb = round(len(result_io.getvalue()) / 1024, 2)
            download_name = filename + ("_compressed" if mode == "Kompresi" else "_decompressed") + result_ext

            col1, col2 = st.columns(2)
            col1.metric("Ukuran Asli", f"{original_size_kb} KB")
            col2.metric("Ukuran Hasil", f"{result_size_kb} KB")

            st.success("✅ File berhasil diproses.")
            st.download_button("⬇️ Unduh File", data=result_io, file_name=download_name)

