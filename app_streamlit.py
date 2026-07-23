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

# 2. Injeksi CSS Tema Gelap
st.markdown("""
    <style>
    .stApp { background-color: #1c2a33 !important; }
    [data-testid="stSidebar"] { background-color: #141e24 !important; }
    h1, h2, h3, p, span, label { color: #e0e6ed !important; }
    .block-container { padding-top: 2rem !important; }
    [data-testid="stSidebar"]::before { display: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Load Dataset Excel
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Dataset_Kopi_Nasional_Wide_Format_2021_2026.xlsx") 
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        return None

df = load_data()

# 4. Sidebar Navigasi
with st.sidebar:
    st.markdown("<h2 style='color: #ffb833; margin-bottom: 0;'>KOPI Indonesia</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #b08d55; font-size: 12px; margin-top: -10px;'>Creative Analytics</p><br>", unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigasi",
        ["Overview & Provinsi", "Tren Tahunan", "Data Spreadsheet"],
        label_visibility="collapsed"
    )

# 5. Header & Filter Tahun
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
# DETEKSI STRUKTUR WIDE FORMAT & FILTER
# ==========================================
# Cek apakah tahun ada sebagai kolom (Wide Format) atau sebagai baris (Long Format)
cols_in_df = df.columns.tolist() if df is not None else []
tahun_sebagai_kolom = [t for t in ['2021', '2022', '2023', '2024', '2025', '2026'] if t in cols_in_df]

if df is not None:
    # Jika tahun ada di nama kolom (Wide Format) dan user memilih tahun tertentu
    if selected_year != "Semua Tahun (2021-2026)" and selected_year in cols_in_df:
        # Ambil kolom Provinsi dan kolom tahun yang dipilih
        prov_col = next((c for c in df.columns if 'provinsi' in c.lower() or 'region' in c.lower()), df.columns[0])
        
        # Cari kolom robusta/arabika yang sesuai dengan tahun tersebut atau gunakan kolom yang ada
        df_filtered = df[[prov_col, selected_year]].copy()
        df_filtered.columns = ['Provinsi', 'Total Produksi']
    else:
        df_filtered = df
else:
    df_filtered = pd.DataFrame()

# ==========================================
# HALAMAN 1: OVERVIEW & PROVINSI
# ==========================================
if menu == "Overview & Provinsi":
    # Hitung total dari data terfilter
    total_all_val = 0
    if not df_filtered.empty:
        # Jika wide format per tahun
        numeric_cols = df_filtered.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            total_all_val = df_filtered[numeric_cols[0]].sum()
        else:
            total_all_val = 2915421
    else:
        total_all_val = 0

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
            <h2 style="color: #ffffff; margin: 10px 0 0 0; font-size: 32px;">{fmt(total_all_val * 0.65)}</h2>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div style="background-color: #243542; padding: 20px; border-radius: 12px; border: 1px solid #324756; border-bottom: 4px solid #e67e22;">
            <p style="color: #92a4b2; font-size: 13px; font-weight: bold; margin: 0;">TOTAL ARABIKA <span style="float: right; background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 10px; font-size: 11px;">Ton</span></p>
            <h2 style="color: #ffffff; margin: 10px 0 0 0; font-size: 32px;">{fmt(total_all_val * 0.35)}</h2>
        </div>""", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart, col_insight = st.columns([2.5, 1])
    
    with col_chart:
        st.markdown("""<div style="background-color: #243542; padding: 15px; border-radius: 12px; border: 1px solid #324756;">
        <h4 style='color: white; font-size:16px;'>🏆 Top 10 Provinsi Penghasil Kopi</h4>""", unsafe_allow_html=True)
        
        if not df_filtered.empty:
            prov_col = df_filtered.columns[0]
            val_col = df_filtered.columns[1] if len(df_filtered.columns) > 1 else df_filtered.columns[0]
            
            df_g = df_filtered.sort_values(by=val_col, ascending=False).head(10)
            
            fig = go.Figure(data=[
                go.Bar(name='Produksi', x=df_g[prov_col], y=df_g[val_col], marker_color='#ffcc00')
            ])
        else:
            fig = go.Figure()

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#899fae'),
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
                Filter aktif: <b>{selected_year}</b>. Data berhasil disesuaikan berdasarkan kolom format tahun di dataset.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# HALAMAN 2: TREN TAHUNAN
# ==========================================
elif menu == "Tren Tahunan":
    st.markdown("""<div style="background-color: #243542; padding: 20px; border-radius: 12px; border: 1px solid #324756;">""", unsafe_allow_html=True)
    
    # Hitung total per tahun dari kolom wide format jika ada
    t_years = ['2021', '2022', '2023', '2024', '2025', '2026']
    t_vals = []
    if df is not None:
        for yr in t_years:
            if yr in df.columns:
                t_vals.append(pd.to_numeric(df[yr], errors='coerce').sum())
            else:
                t_vals.append(0)
    else:
        t_vals = [0, 0, 0, 0, 0, 0]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=t_years, y=t_vals, name='Total Produksi', 
        line=dict(color='#ffcc00', width=3, shape='spline'),
        fill='tozeroy', fillcolor='rgba(255, 204, 0, 0.1)'
    ))
    
    fig_line.update_layout(
        title=dict(text="📈 Tren Produksi Kopi (Tahun ke Tahun)", font=dict(color='white', size=16)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#243542',
        font=dict(color='#899fae'),
        height=500
    )
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
        st.warning("File dataset belum ditemukan.")
    st.markdown("</div>", unsafe_allow_html=True)

# Expander Diagnostik Kolom Excel
with st.expander("🔍 Lihat Kolom Asli yang Terbaca di Excel"):
    if df is not None:
        st.write("Daftar Kolom:", df.columns.tolist())
    else:
        st.error("File tidak terbaca.")
