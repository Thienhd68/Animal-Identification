import streamlit as st
import os
import cv2
import tempfile
import numpy as np
import datetime
import pandas as pd
import sqlite3
import plotly.express as px
from layout.alert import render_alert
# =========================
# 1. CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Hệ thống Quản trị Chăn Nuôi 4.0",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 2. XỬ LÝ DATABASE (SQLITE)
# =========================
def init_db():
    conn = sqlite3.connect('farm_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            type TEXT,
            cow_count INTEGER,
            pig_count INTEGER,
            chicken_count INTEGER,
            total INTEGER,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(data_type, counter):
    conn = sqlite3.connect('farm_data.db')
    c = conn.cursor()
    cows = counter.get("Bò", 0)
    pigs = counter.get("Heo", 0)
    chickens = counter.get("Gà", 0)
    total = sum(counter.values())
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('''
        INSERT INTO history (timestamp, type, cow_count, pig_count, chicken_count, total, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, data_type, cows, pigs, chickens, total, "AI Detection"))
    conn.commit()
    conn.close()

def load_data():
    try:
        conn = sqlite3.connect('farm_data.db')
        df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

init_db()

# =========================
# 3. CSS GIAO DIỆN CAO CẤP
# =========================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    .header-container {
        background: linear-gradient(90deg, #059669 0%, #10B981 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 4. IMPORT LOGIC AI
# =========================
try:
    from predict import predict_image, predict_video
except ImportError:
    st.error("⚠️ Thiếu file 'predict.py'.")
    st.stop()

# =========================
# 5. SIDEBAR (CẬP NHẬT THÔNG TIN NHÓM)
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2395/2395796.png", width=70)
    st.markdown("### 🛠 CONTROL PANEL")
    
    # --- PHẦN SỬA ĐỔI ---
    st.info("""
    **Thực hiện: Nhóm 9**
    \n*Hệ thống phân loại và đếm số lượng động vật trong chăn nuôi sử dụng Machine Learning*
    """)
    # --------------------
    
    st.markdown("---")
    # Đặt value=0.6 để mặc định nó nằm ở mức cao, giúp lọc chó/mèo tốt hơn
    confidence = st.slider("🎚️ Độ nhạy AI (Confidence)", min_value=0.1, max_value=0.9, value=0.6)
    
    st.markdown("---")
    try:
        df_quick = load_data()
        st.metric("📦 Tổng bản ghi Database", len(df_quick))
    except:
        pass

# =========================
# 6. MAIN HEADER
# =========================
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size:2rem;">HỆ THỐNG QUẢN TRỊ TRANG TRẠI THÔNG MINH</h1>
    <p style="margin:0; opacity:0.9;">AI Powered Livestock Management System</p>
</div>
""", unsafe_allow_html=True)

# =========================
# 7. TAB LAYOUT
# =========================
tab1, tab2, tab3 = st.tabs(["📸 GIÁM SÁT (MONITOR)", "📊 PHÂN TÍCH (ANALYTICS)", "🗄️ DỮ LIỆU (DATABASE)"])

# === TAB 1: GIÁM SÁT ===
with tab1:
    col_up, col_guide = st.columns([3, 1])
    with col_up:
        uploaded_file = st.file_uploader("Tải lên Video/Hình ảnh", type=['jpg','png','mp4'])
    with col_guide:
        st.success("🟢 Hệ thống: Online")
        # Hiển thị độ nhạy hiện tại để kiểm tra
        st.warning(f"🎯 Độ nhạy đang set: {confidence}")

    if uploaded_file:
        st.divider()
        filename = uploaded_file.name.lower()
        
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            with st.spinner("🤖 AI đang quét chuồng trại..."):
                res = predict_image(img, conf=confidence)
            
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.image(res["image"], use_container_width=True, caption="Kết quả xử lý Visual")
            
            with c2:
                counter = res["counter"]
                if not counter:
                    st.error("⚠️ Không phát hiện vật nuôi mục tiêu!")
                    st.caption("AI đã lọc bỏ các đối tượng không chắc chắn (như chó, mèo...).")
                else:
                    df_res = pd.DataFrame(list(counter.items()), columns=['Loại', 'Số lượng'])
                    fig = px.pie(df_res, values='Số lượng', names='Loại', hole=0.4, 
                                 title="Cơ cấu vật nuôi hiện tại", 
                                 color_discrete_sequence=px.colors.sequential.Greens_r)
                    fig.update_layout(height=300, margin=dict(t=30,b=0,l=0,r=0))
                    st.plotly_chart(fig, use_container_width=True)

                    # ========== GỌI HÀM CẢNH BÁO ==========
                    st.markdown("---")
                    render_alert(counter)
                    # ==========================================

                    save_to_db("Image", counter)
                    st.toast("✅ Đã lưu dữ liệu!", icon="💾")

        elif filename.endswith('.mp4'):
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            
            prog = st.progress(0, "Đang khởi động Engine...")
            def update_p(p): prog.progress(int(p*100), f"Processing: {int(p*100)}%")
            
            try:
                res = predict_video(tfile.name, conf=confidence, progress_callback=update_p)
                prog.empty()
                v1, v2 = st.columns([2, 1])
                with v1: st.video(res["video_out"])
                with v2:
                    st.subheader("Kết quả tổng hợp")
                    counter = res["counter"]
                    if counter:
                        for k,v in counter.items(): st.metric(k, v)
                        save_to_db("Video", counter)
                        st.success("Đã ghi nhận vào CSDL")
                    else:
                        st.warning("Không có dữ liệu")
            except Exception as e:
                st.error(f"Lỗi: {e}")

# === TAB 2: PHÂN TÍCH ===
with tab2:
    st.subheader("📈 Báo cáo thông minh (BI)")
    df = load_data()
    
    if not df.empty:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Tổng lượt quét", len(df))
        k2.metric("Tổng số Bò", df['cow_count'].sum())
        k3.metric("Tổng số Heo", df['pig_count'].sum())
        k4.metric("Cập nhật cuối", df.iloc[0]['timestamp'].split(" ")[1])
        
        st.divider()
        df_chart = df.head(20).sort_values(by="id")
        st.markdown("##### 📉 Xu hướng số lượng vật nuôi")
        fig_line = px.line(df_chart, x='timestamp', y=['cow_count', 'pig_count', 'chicken_count'],
                           markers=True, title="Biến động đàn gia súc theo thời gian")
        st.plotly_chart(fig_line, use_container_width=True)
            
    else:
        st.info("Chưa có dữ liệu phân tích.")

# === TAB 3: DỮ LIỆU ===
with tab3:
    st.subheader("🗄️ Quản lý Cơ sở dữ liệu")
    df = load_data()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Xuất báo cáo CSV", csv, "baocao.csv", "text/csv")
        
        if st.button("🗑️ Xóa dữ liệu (Reset)"):
            conn = sqlite3.connect('farm_data.db')
            c = conn.cursor()
            c.execute("DELETE FROM history")
            conn.commit()
            conn.close()
            st.rerun()
    else:
        st.write("Database trống.")