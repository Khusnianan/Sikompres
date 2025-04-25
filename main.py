import streamlit as st

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

# UI Streamlit
st.title('Run Length Encoding (RLE) Compression & Decompression')

# Kompresi
st.write("### Kompresi")
input_data = st.text_area('Masukkan teks untuk dikompresi:', 'AAAAABBBBCCCCDDDD')

if st.button('Kompresi'):
    if input_data:
        compressed_result = compress(input_data)
        st.write('Data yang dikompresi:', compressed_result)
    else:
        st.warning('Harap masukkan data untuk dikompresi.')

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
