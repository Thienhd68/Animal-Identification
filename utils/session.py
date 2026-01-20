import streamlit as st
from datetime import datetime

# ==============================
# INIT SESSION
# ==============================
def init_history():
    """
    Khởi tạo session state cho toàn bộ app
    """
    if "history" not in st.session_state:
        st.session_state["history"] = []

    if "current_result" not in st.session_state:
        st.session_state["current_result"] = None


# ==============================
# SAVE RESULT
# ==============================
def save_result(result: dict):
    """
    Lưu kết quả detect hiện tại vào history

    result: {"Bò": 55, "Heo": 10, ...}
    """
    record = {
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "result": result
    }

    st.session_state["history"].append(record)
    st.session_state["current_result"] = record


# ==============================
# GET LATEST
# ==============================
def get_latest_result():
    """
    Lấy kết quả detect gần nhất
    """
    if "current_result" not in st.session_state:
        return None
    return st.session_state["current_result"]["result"]


# ==============================
# GET HISTORY
# ==============================
def get_history():
    """
    Trả về toàn bộ lịch sử
    """
    return st.session_state.get("history", [])
