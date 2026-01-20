import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.session import get_latest_result

def render_statistics():
    """
    Hiển thị thống kê + biểu đồ tổng hợp
    """

    st.markdown(
        "<div class='section-title'>📊 Thống kê tổng hợp</div>",
        unsafe_allow_html=True
    )

    result = get_latest_result()

    if not result:
        st.info("Chưa có dữ liệu để thống kê")
        return

    # result dạng: {"Bò": 55, "Heo": 10, ...}
    df = pd.DataFrame(
        list(result.items()),
        columns=["Loài", "Số lượng"]
    )

    # ===== BẢNG =====
    st.subheader("📋 Bảng số liệu")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ===== BIỂU ĐỒ =====
    st.subheader("📈 Biểu đồ phân bố")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(
        df["Loài"],
        df["Số lượng"]
    )
    ax.set_ylabel("Số lượng")
    ax.set_xlabel("Loài")
    ax.set_title("Thống kê số lượng động vật")

    st.pyplot(fig)

    # ===== TỔNG =====
    total = df["Số lượng"].sum()
    st.success(f"🔢 Tổng số cá thể phát hiện: **{total}**")
