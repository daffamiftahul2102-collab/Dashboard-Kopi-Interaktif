import streamlit as st
import streamlit.components.v1 as components

# 1. Konfigurasi Halaman Streamlit (Bikin Full Screen)
st.set_page_config(layout="wide", page_title="Dashboard Produksi Kopi", page_icon="☕")

# 2. Injeksi CSS untuk menghilangkan batas (padding) bawaan Streamlit
st.markdown("""
    <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        /* Sembunyikan header dan footer bawaan Streamlit */
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Membaca file HTML, CSS, dan JS bawaan lu
# (Asumsi filenya ada di dalam folder 'frontend' seperti di screenshot VS Code lu)
try:
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        html_data = f.read()
    
    with open("frontend/style.css", "r", encoding="utf-8") as f:
        css_data = f.read()
        
    with open("frontend/script.js", "r", encoding="utf-8") as f:
        js_data = f.read()

    # 4. Menggabungkan (Inject) CSS dan JS ke dalam HTML
    # Mengganti tag pemanggil file dengan isi kodenya langsung agar terbaca oleh Streamlit
    html_data = html_data.replace('<link rel="stylesheet" href="style.css">', f"<style>{css_data}</style>")
    html_data = html_data.replace('<script src="script.js"></script>', f"<script>{js_data}</script>")

    # 5. Menampilkan Web HTML lu di dalam bingkai Streamlit!
    # Tinggi (height) diset 900px agar pas satu layar desktop
    components.html(html_data, height=900, scrolling=True)

except Exception as e:
    st.error(f"Gagal memuat file: {e}. Pastikan path foldernya benar!")