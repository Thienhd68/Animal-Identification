import streamlit as st
from config import FRAME_SKIP_DEFAULT

def render_sidebar():
    st.sidebar.title("⚙️ Điều khiển hệ thống")

    theme = st.sidebar.radio(
        "🌓 Giao diện",
        ["Sáng", "Tối"]
    )

    data_type = st.sidebar.radio(
        "📂 Dữ liệu đầu vào",
        ["Ảnh", "Video"]
    )

    frame_skip = st.sidebar.slider(
        "⏩ Bỏ qua frame (video)",
        1, 10, FRAME_SKIP_DEFAULT
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "Hệ thống hỗ trợ nhận dạng và đếm động vật "
        "trong môi trường chăn nuôi thực tế."
    )

    return theme, data_type, frame_skip
