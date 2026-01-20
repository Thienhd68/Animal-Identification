import streamlit as st
import numpy as np
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

from utils.draw import draw_boxes

def render_result(image: np.ndarray, detections: list):
    if image is None or len(detections) == 0:
        st.warning("Không phát hiện đối tượng nào")
        return

    # ----------- DRAW IMAGE -----------
    result_img = draw_boxes(image, detections)

    st.markdown(
        "<div class='section-title'>📸 Kết quả nhận dạng</div>",
        unsafe_allow_html=True
    )

    st.image(result_img, use_container_width=True)

    # ----------- STATISTICS -----------
    labels = [d[4] for d in detections]
    counter = Counter(labels)

    st.markdown(
        "<div class='section-title'>📊 Thống kê</div>",
        unsafe_allow_html=True
    )

    # KPI CARDS
    cols = st.columns(len(counter) + 1)

    with cols[0]:
        st.markdown(
            f"""
            <div class="card metric">
                <div class="metric-label">Tổng phát hiện</div>
                <div class="metric-value">{sum(counter.values())}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    for i, (k, v) in enumerate(counter.items()):
        with cols[i + 1]:
            st.markdown(
                f"""
                <div class="card metric">
                    <div class="metric-label">{k}</div>
                    <div class="metric-value">{v}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # TABLE + CHART
    df = pd.DataFrame(counter.items(), columns=["Loài", "Số lượng"])

    left, right = st.columns(2)

    with left:
        st.subheader("📋 Bảng chi tiết")
        st.dataframe(df, use_container_width=True)

    with right:
        st.subheader("📈 Biểu đồ tổng hợp")
        fig, ax = plt.subplots()
        ax.bar(df["Loài"], df["Số lượng"])
        ax.set_ylabel("Số lượng")
        st.pyplot(fig)

    return counter
