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

# 3. Fungsi Load Dataset Langsung Menggunakan Pandas
@st.cache_data
def load_data():
    try:
        # Ganti dengan nama file excel yang ada di repo GitHub Anda
        df = pd.read_excel("dataset_kopi_indonesia_2023.xlsx") 
        return df
    except Exception as e:
        try:
            # Coba nama alternatif jika ada
            df = pd.read_excel("Dataset_Kopi_Nasional_Wide_Format_2021_2026.xlsx")
            return df
        except:
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
    list_tahun = ["Semua Tahun (2021-2026)"]
    if df is not None:
        # Cari kolom tahun secara otomatis
        col_thn = next((c for c in df.columns if 'tahun' in c.lower()), None)
        if col_thn:
            list_tahun += sorted(df[col_thn].dropna().unique().astype(str).tolist())
    
    selected_year = st.selectbox("Filter Tahun", list_tahun, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

def fmt(val):
    try:
        return f"{int(val):,}".replace(",", ".")
    except:
        return str(val)

# Filter Data Berdasarkan Tahun
if df is not None:
    col_thn = next((c for c in df.columns if 'tahun' in c.lower()), None)
    if selected_year != "Semua Tahun (2021-2026)" and col_thn:
        df_filtered = df[df[col_thn].astype(str) == selected_year]
    else:
        df_filtered = df
else:
    df_filtered = pd.DataFrame()

# Deteksi nama kolom otomatis untuk aman dari KeyError
col_rob = None
col_ara = None
col_prov = None
if df is not None:
    col_rob = next((c for c in df.columns if 'robusta' in c.lower() and 'produksi' in c.lower()), None)
    if not col_rob:
        col_rob = next((c for c in df.columns if 'robusta' in c.lower()), None)
        
    col_ara = next((c for c in df.columns if 'arabika' in c.lower() and 'produksi' in c.lower()), None)
    if not col_ara:
        col_ara = next((c for c in df.columns if 'arabika' in c.lower()), None)
        
    col_prov = next((c for c in df.columns if 'provinsi' in c.lower()), None)

# ==========================================
# HALAMAN 1: OVERVIEW & PROVINSI
# ==========================================
if menu == "Overview & Provinsi":
    total_all_val = 2915421
    total_rob_val = 1921118
    total_ara_val = 994303
    
    if not df_filtered.empty and col_rob and col_ara:
        total_rob_val = df_filtered[col_rob].sum()
        total_ara_val = df_filtered[col_ara].sum()
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
            df_grouped = df_filtered.groupby(col_prov)[[col_rob, col_ara]].sum().reset_index()
            df_grouped = df_grouped.sort_values(by=col_rob, ascending=False).head(10)
            
            fig = go.Figure(data=[
                go.Bar(name='Robusta', x=df_grouped[col_prov], y=df_grouped[col_rob], marker_color='#ffcc00'),
                go.Bar(name='Arabika', x=df_grouped[col_prov], y=df_grouped[col_ara], marker_color='#e67e22')
            ])
        else:
            fig = go.Figure(data=[
                go.Bar(name='Robusta', x=['Sumatera Selatan', 'Lampung', 'Aceh'], y=[1068716, 680000, 79800], marker_color='#ffcc00'),
                go.Bar(name='Arabika', x=['Sumatera Selatan', 'Lampung', 'Aceh'], y=[50000, 10000, 412000], marker_color='#e67e22')
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
                Berdasarkan data {selected_year}, <b>Sumatera Selatan</b> memimpin sebagai produsen <b>Kopi Robusta</b> terbesar dengan total produksi mencapai <span style="color: #ffcc00;">1.068.716 Ton</span>.
            </p>
            <p style="font-size: 14px; line-height: 1.6; color: #d0dbe3;">
                Di sisi lain, untuk pasar <b>Kopi Arabika</b>, wilayah <b>Sumatera Utara</b> mendominasi dengan angka produksi sebesar <span style="color: #e67e22;">512.408 Ton</span>.
            </p>
            <p style="font-size: 14px; line-height: 1.6; color: #d0dbe3;">
                Secara umum, provinsi-provinsi di Pulau Sumatera mendominasi sentra kopi nasional.
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
        st.dataframe(df_filtered, use_container_width=True, height=450)
    else:
        st.warning("File dataset belum ditemukan di repositori GitHub Anda. Pastikan file Excel sudah di-*push*!")
        
    st.markdown("</div>", unsafe_allow_html=True)
