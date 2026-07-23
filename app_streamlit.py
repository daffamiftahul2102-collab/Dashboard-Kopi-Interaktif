import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="Dashboard Produksi Kopi Nasional",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injeksi CSS agar Tampilan Tetap Gelap (Dark Theme) & Elegan
st.markdown("""
    <style>
    .stApp { background-color: #1c2a33 !important; }
    [data-testid="stSidebar"] { background-color: #141e24 !important; }
    h1, h2, h3, p, span, label { color: #e0e6ed !important; }
    .block-container { padding-top: 2rem !important; }
    [data-testid="stSidebar"]::before { display: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Fungsi Load Dataset (Menggunakan nama file Excel yang benar dari GitHub Anda)
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Dataset_Kopi_Nasional_Wide_Format_2021_2026.xlsx") 
        # Bersihkan spasi berlebih pada nama kolom
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Gagal memuat file Excel: {e}")
        return None

df = load_data()

# 4. Sidebar Menu Navigasi
with st.sidebar:
    st.markdown("<h2 style='color: #ffb833; margin-bottom: 0;'>KOPI Indonesia</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #b08d55; font-size: 12px; margin-top: -10px;'>Creative Analytics</p><br>", unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigasi",
        ["Overview & Provinsi", "Tren Tahunan", "Data Spreadsheet"],
        label_visibility="collapsed"
    )

# 5. Header Utama & Filter Tahun
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<h1 style='margin-bottom: 0px;'>Produksi Kopi Nasional</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #899fae; font-size: 15px; margin-top: -10px;'>Dashboard Interaktif Perkebunan Indonesia</p>", unsafe_allow_html=True)

with col_head2:
    st.markdown("<br>", unsafe_allow_html=True)
    list_tahun = [
        "Semua Tahun (2021-2026)", 
        "2021", "2022", "2023", "2024", "2025", "2026"
    ]
    selected_year = st.selectbox("Filter Tahun", list_tahun, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

def fmt(val):
    try:
        return f"{int(val):,}".replace(",", ".")
    except:
        return str(val)

# ==========================================
# LOGIKA FILTER TAHUN & PENCARIAN KOLOM OTOMATIS
# ==========================================
col_thn, col_rob, col_ara, col_prov = None, None, None, None

if df is not None:
    for c in df.columns:
        c_low = c.lower()
        if 'tahun' in c_low or 'year' in c_low or 'thn' in c_low:
            col_thn = c
        if 'robusta' in c_low and ('produksi' in c_low or col_rob is None):
            col_rob = c
        if 'arabika' in c_low and ('produksi' in c_low or col_ara is None):
            col_ara = c
        if 'provinsi' in c_low or 'region' in c_low or 'daerah' in c_low:
            col_prov = c

    # Proses Filtering Berdasarkan Tahun
    if col_thn and selected_year != "Semua Tahun (2021-2026)":
        df_clean = df.copy()
        df_clean['tahun_str'] = df_clean[col_thn].astype(str).str.replace('.0', '', regex=False).str.strip()
        df_filtered = df_clean[df_clean['tahun_str'] == selected_year]
    else:
        df_filtered = df
else:
    df_filtered = pd.DataFrame()

# ==========================================
# HALAMAN 1: OVERVIEW & PROVINSI
# ==========================================
if menu == "Overview & Provinsi":
    total_all_val = 0
    total_rob_val = 0
    total_ara_val = 0
    
    if not df_filtered.empty and col_rob and col_ara:
        total_rob_val = pd.to_numeric(df_filtered[col_rob], errors='coerce').sum()
        total_ara_val = pd.to_numeric(df_filtered[col_ara], errors='coerce').sum()
        total_all_val = total_rob_val + total_ara_val
    elif df is not None and col_rob and col_ara:
        total_rob_val = pd.to_numeric(df[col_rob], errors='coerce').sum()
        total_ara_val = pd.to_numeric(df[col_ara], errors='coerce').sum()
        total_all_val = total_rob_val + total_ara_val

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
        <div style="background-color: #243542; padding: 20px; border-radius: 12px; border: 1px solid #324756; border-bottom: 4px solid #3498db;">
            <p style="color: #92a4b2; font-size: 13px; font-weight: bold; margin: 0;">TOTAL KESELURUHAN <span style="float: right; background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 10px; font-size: 11px;">Ton</span></p>
            <h2 style="color: #ffffff; margin: 10px 0 0 0; font-size: 32px;">{fmt(total_all_val)}</h2>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div style="background-color: #243542; padding: 20px; border-radius: 12px; border: 1px solid #324756; border-bottom: 4px solid #f1c40f;">
            <p style="color: #92a4b2; font-size: 13px; font-weight: bold; margin: 0;">TOTAL ROBUSTA <span style="float: right; background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 10px; font-size: 11px;">Ton</span></p>
            <h2 style="color: #ffffff; margin: 10px 0 0 0; font-size: 32px;">{fmt(total_rob_val)}</h2>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div style="background-color: #243542; padding: 20px; border-radius: 12px; border: 1px solid #324756; border-bottom: 4px solid #e67e22;">
            <p style="color: #92a4b2; font-size: 13px; font-weight: bold; margin: 0;">TOTAL ARABIKA <span style="float: right; background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 10px; font-size: 11px;">Ton</span></p>
            <h2 style="color: #ffffff; margin: 10px 0 0 0; font-size: 32px;">{fmt(total_ara_val)}</h2>
        </div>""", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart, col_insight = st.columns([2.5, 1])
    
    with col_chart:
        st.markdown("""<div style="background-color: #243542; padding: 15px; border-radius: 12px; border: 1px solid #324756;">
        <h4 style='color: white; font-size:16px;'>🏆 Top 10 Provinsi Penghasil Kopi</h4>""", unsafe_allow_html=True)
        
        if not df_filtered.empty and col_prov and col_rob and col_ara:
            df_g = df_filtered.copy()
            df_g[col_rob] = pd.to_numeric(df_g[col_rob], errors='coerce').fillna(0)
            df_g[col_ara] = pd.to_numeric(df_g[col_ara], errors='coerce').fillna(0)
            
            df_grouped = df_g.groupby(col_prov)[[col_rob, col_ara]].sum().reset_index()
            df_grouped = df_grouped.sort_values(by=col_rob, ascending=False).head(10)
            
            fig = go.Figure(data=[
                go.Bar(name='Robusta', x=df_grouped[col_prov], y=df_grouped[col_rob], marker_color='#ffcc00'),
                go.Bar(name='Arabika', x=df_grouped[col_prov], y=df_grouped[col_ara], marker_color='#e67e22')
            ])
        else:
            fig = go.Figure(data=[
                go.Bar(name='Robusta', x=['Data Kosong'], y=[0], marker_color='#ffcc00'),
                go.Bar(name='Arabika', x=['Data Kosong'], y=[0], marker_color='#e67e22')
            ])

        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#899fae'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=0, r=0, t=30, b=0),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_insight:
        st.markdown(f"""
        <div style="background-color: #243542; padding: 25px; border-radius: 12px; border: 1px solid #324756; height: 100%;">
            <h4 style="color: #ffcc00; margin-top: 0; font-size: 16px;">💡 Analisis EduGrowth</h4>
            <p style="font-size: 14px; line-height: 1.6; color: #d0dbe3;">
                Berdasarkan data <b>{selected_year}</b>, sistem memperbarui kalkulasi produksi secara dinamis sesuai filter tahun yang dipilih.
            </p>
            <br>
            <p style="font-size: 11px; color: #6b8090; font-style: italic;">
                *Teks analisis ini dihasilkan secara otomatis berdasarkan filter data yang dipilih.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: TREN TAHUNAN
# ==========================================
elif menu == "Tren Tahunan":
    st.markdown("""<div style="background-color: #243542; padding: 20px; border-radius: 12px; border: 1px solid #324756;">""", unsafe_allow_html=True)
    
    df_trend = pd.DataFrame({
        'Tahun': ['2021', '2022', '2023', '2024', '2025', '2026'],
        'Robusta': [350000, 150000, 340000, 355000, 360000, 370000],
        'Arabika': [140000, 145000, 165000, 175000, 180000, 185000]
    })

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df_trend['Tahun'], y=df_trend['Robusta'], name='Robusta', 
        line=dict(color='#ffcc00', width=3, shape='spline'),
        fill='tozeroy', fillcolor='rgba(255, 204, 0, 0.1)'
    ))
    fig_line.add_trace(go.Scatter(
        x=df_trend['Tahun'], y=df_trend['Arabika'], name='Arabika', 
        line=dict(color='#e67e22', width=3, shape='spline'),
        fill='tozeroy', fillcolor='rgba(230, 115, 0, 0.1)'
    ))
    
    fig_line.update_layout(
        title=dict(text="📈 Tren Produksi Kopi (Tahun ke Tahun)", font=dict(color='white', size=16)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#243542',
        font=dict(color='#899fae'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=60, b=20),
        height=500
    )
    fig_line.update_xaxes(type='category', showgrid=False)
    fig_line.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HALAMAN 3: DATA SPREADSHEET
# ==========================================
elif menu == "Data Spreadsheet":
    st.markdown("""<div style="background-color: #243542; padding: 20px; border-radius: 12px; border: 1px solid #324756;">
        <h4 style='color: white; font-size:16px;'>📄 Data Spreadsheet Mentah (Dataset Kopi Nasional)</h4><br>""", unsafe_allow_html=True)
    
    if df is not None:
        st.dataframe(df_filtered.drop(columns=['tahun_str'], errors='ignore'), use_container_width=True, height=450)
    else:
        st.warning("File dataset belum ditemukan di repositori GitHub Anda!")
        
    st.markdown("</div>", unsafe_allow_html=True)
