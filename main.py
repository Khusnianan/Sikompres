import streamlit as st
from docx import Document
import io

# Fungsi untuk kompresi (Run Length Encoding)
def compress(data):
    compressed_data = []
    i = 0
    while i < len(data):
        char = data[i]
        count = 1
        while i + 1 < len(data) and data[i + 1] == char:
            i += 1
            count += 1
        # Simpan posisi dan jumlah pengulangan
        compressed_data.append((i, char, count))
        i += 1
    return compressed_data

# Fungsi untuk dekompresi (Run Length Decoding)
def decompress(compressed_data):
    decompressed_data = []
    for pos, char, count in compressed_data:
        decompressed_data.append(char * count)  # Rekonstruksi data
    return ''.join(decompressed_data)

# Fungsi untuk membaca file .txt
def read_txt(file):
    return file.getvalue().decode("utf-8")

# Fungsi untuk membaca file .docx
def read_docx(file):
    doc = Document(io.BytesIO(file.read()))
    return "\n".join([para.text for para in doc.paragraphs])

# UI Streamlit
st.title('Run Length Encoding (RLE) Compression & Decompression')

# Upload file
uploaded_file = st.file_uploader("Pilih file untuk di-upload", type=["txt", "docx"])

if uploaded_file is not None:
    # Membaca konten file
    if uploaded_file.type == "text/plain":
        input_data = read_txt(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        input_data = read_docx(uploaded_file)
    
    st.write(f"### Konten file yang di-upload:")
    st.text_area("Isi file:", input_data, height=200)

    # Kompresi
    st.write("### Kompresi")
    if st.button('Kompresi'):
        if input_data:
            compressed_result = compress(input_data)
            st.write('Data yang dikompresi:', compressed_result)
        else:
            st.warning('File kosong, tidak dapat diproses.')

    # Dekompresi
    st.write("### Dekompresi")
    compressed_input = st.text_area('Masukkan data terkompresi untuk dekompresi:', "")

    if st.button('Dekompresi'):
        if compressed_input:
            try:
                compressed_data = eval(compressed_input)  # Mengonversi string ke list of tuples
                decompressed_result = decompress(compressed_data)
                st.write('Data setelah didekompresi:', decompressed_result)
            except:
                st.error('Data terkompresi tidak valid, pastikan formatnya benar.')
        else:
            st.warning('Harap masukkan data terkompresi untuk didekompresi.')
