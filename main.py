import streamlit as st
from io import BytesIO

# Fungsi untuk kompresi teks dengan RLE dimodifikasi
def modified_run_length_encode(data, Sc="#"):
    encoding = ''
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        if count > 1:
            encoding += f"{Sc}{count}{data[i]}"  # Format: #CcX
        else:
            encoding += data[i]
        i += 1
    return encoding

# Fungsi untuk dekompresi teks dengan RLE dimodifikasi
def modified_run_length_decode(encoded_data, Sc="#"):
    decoded = ''
    i = 0
    while i < len(encoded_data):
        if encoded_data[i] == Sc:  # Apakah karakter adalah penanda kompresi?
            count = int(encoded_data[i+1])  # Mengambil jumlah pengulangan
            decoded += encoded_data[i+2] * count  # Mengulang karakter sesuai count
            i += 3  # Lewati #CcX
        else:
            decoded += encoded_data[i]
            i += 1
    return decoded

# Fungsi untuk kompresi file biner dengan RLE dimodifikasi
def run_length_encode_bytes(data, Sc=b'\xFF'):  # Memakai byte sebagai penanda
    encoding = bytearray()
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        if count > 1:
            encoding.extend([Sc, count, data[i]])  # Format: penanda #CcX
        else:
            encoding.append(data[i])
        i += 1
    return bytes(encoding)

# Fungsi untuk dekompresi file biner dengan RLE dimodifikasi
def run_length_decode_bytes(encoded_data, Sc=b'\xFF'):
    decoded = bytearray()
    i = 0
    while i < len(encoded_data):
        if encoded_data[i] == Sc:
            count = encoded_data[i+1]
            decoded.extend([encoded_data[i+2]] * count)
            i += 3
        else:
            decoded.append(encoded_data[i])
            i += 1
    return bytes(decoded)

# Streamlit UI
st.title("File Compression and Decompression with Run Length Encoding")
st.write("This tool allows you to compress and decompress text and binary files using modified Run Length Encoding (RLE).")

# Pilih jenis file yang akan diupload
file_type = st.radio("Choose file type", ('Text', 'Binary (Audio, Video, PDF, etc.)'))

if file_type == 'Text':
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode("utf-8")
        
        st.subheader("Original Text:")
        st.text(file_content)
        
        # Kompresi file teks
        compressed_data = modified_run_length_encode(file_content)
        st.subheader("Compressed Text:")
        st.text(compressed_data)

        # Menyediakan tombol untuk mendownload file terkompresi
        st.download_button("Download Compressed Text File", compressed_data, "compressed.txt", "text/plain")

        # Dekompresi untuk verifikasi
        decompressed_data = modified_run_length_decode(compressed_data)
        st.subheader("Decompressed Text (Verification):")
        st.text(decompressed_data)

elif file_type == 'Binary (Audio, Video, PDF, etc.)':
    uploaded_file = st.file_uploader("Upload a binary file", type=["pdf", "mp3", "mp4", "jpg", "png"])

    if uploaded_file is not None:
        file_content = uploaded_file.read()

        st.subheader("Original Binary File (in byte format):")
        st.text(file_content[:200])  # Tampilkan sebagian awal file biner untuk tampilan

        # Kompresi file biner
        compressed_binary = run_length_encode_bytes(file_content)
        st.subheader("Compressed Binary File:")
        st.text(compressed_binary[:200])  # Tampilkan sebagian awal file biner yang terkompresi

        # Menyediakan tombol untuk mendownload file terkompresi
        st.download_button("Download Compressed Binary File", compressed_binary, "compressed_file.bin", "application/octet-stream")

        # Dekompresi file biner untuk verifikasi
        decompressed_binary = run_length_decode_bytes(compressed_binary)
        st.subheader("Decompressed Binary File (Verification):")
        st.text(decompressed_binary[:200])  # Tampilkan sebagian awal file biner yang didekompresi
