import streamlit as st

def render_alert(counter):
    if not counter or not isinstance(counter, dict):
        return

    cow_count = counter.get("Bò", 0)
    pig_count = counter.get("Heo", 0)
    chicken_count = counter.get("Gà", 0)

    if cow_count > 10:
        st.error("🚨 Quá nhiều bò – nguy cơ quá tải chuồng!")
    elif pig_count > 20:
        st.warning("⚠️ Heo đông – cần theo dõi dịch bệnh!")
    elif chicken_count > 50:
        st.info("🐔 Gà nhiều – chú ý thông gió!")
