import streamlit as st
from utils.session import get_history

def render_history():
    st.markdown(
        "<div class='section-title'>🕒 Lịch sử xử lý</div>",
        unsafe_allow_html=True
    )

    history = get_history()

    if not history:
        st.info("Chưa có lịch sử xử lý")
        return

    for idx, item in enumerate(reversed(history), 1):
        st.markdown(
            f"""
            <div class="card">
                <b>Lần {idx}</b><br>
                Thời gian: {item["time"]}<br>
                Kết quả: {item["result"]}
            </div>
            """,
            unsafe_allow_html=True
        )
