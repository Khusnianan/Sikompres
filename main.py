import streamlit as st
from io import StringIO

# Fungsi kompresi
def run_length_encode(data):
    encoding = ''
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            i += 1
            count += 1
        encoding += str(count) + data[i]
        i += 1
    return encoding

# Fungsi untuk mendekode
def run_length_decode(encoded_data):
    decoded = ''
    i = 0
    while i < len(encoded_data):
        count = int(encoded_data[i])
        decoded += encoded_data[i+1] * count
        i += 2
    return decoded

# UI Streamlit
st.title("File Compression with Run Length Encoding")
st.write("Upload a text file to compress it using the RLE algorithm.")

uploaded_file = st.file_uploader("Choose a file", type=["txt"])

if uploaded_file is not None:
    # Baca konten file
    file_content = uploaded_file.getvalue().decode("utf-8")
    
    st.subheader("Original File Content:")
    st.text(file_content)
    
    # Kompresi menggunakan RLE
    compressed_data = run_length_encode(file_content)
    st.subheader("Compressed File Content:")
    st.text(compressed_data)

    # Menyediakan opsi untuk mendownload hasil kompresi
    st.download_button("Download Compressed File", compressed_data, "compressed.txt", "text/plain")

    # Dekode untuk memverifikasi hasil
    decoded_data = run_length_decode(compressed_data)
    st.subheader("Decoded File Content (For Verification):")
    st.text(decoded_data)
