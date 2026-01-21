import streamlit as st

def render_alert(counter):
    """
    Hiển thị cảnh báo dựa trên số lượng động vật phát hiện được. 
    
    Args:
        counter: Dictionary chứa số lượng từng loại động vật
                 Ví dụ: {"Bò": 55, "Heo": 10, "Gà": 100}
    """
    # Kiểm tra input hợp lệ
    if not counter or not isinstance(counter, dict):
        return False  # Không có gì để cảnh báo
    
    # Lấy số lượng từng loại (mặc định = 0 nếu không có)
    cow_count = counter.get("Bò", 0)
    pig_count = counter.get("Heo", 0)
    chicken_count = counter.get("Gà", 0)
    total = sum(counter.values())
    
    # Biến theo dõi có cảnh báo nào được hiển thị không
    has_alert = False
    
    # ========== CẢNH BÁO BÒ ==========
    if cow_count > 10:
        st.error(f"🚨 **CẢNH BÁO NGHIÊM TRỌNG:** Phát hiện {cow_count} con bò - Nguy cơ QUÁ TẢI chuồng trại!")
        has_alert = True
    elif cow_count > 3:
        st.warning(f"⚠️ **CHÚ Ý:** Phát hiện {cow_count} con bò - Số lượng đang ở mức CAO!")
        has_alert = True
    
    # ========== CẢNH BÁO HEO ==========
    if pig_count > 5:
        st.warning(f"⚠️ **CHÚ Ý:** Phát hiện {pig_count} con heo - Cần theo dõi DỊCH BỆNH!")
        has_alert = True
    
    # ========== CẢNH BÁO GÀ ==========
    if chicken_count > 10:
        st.info(f"🐔 **THÔNG BÁO:** Phát hiện {chicken_count} con gà - Kiểm tra THÔNG GIÓ chuồng trại!")
        has_alert = True
    
    # ========== CẢNH BÁO TỔNG ==========
    if total > 10:
        st.warning(f"📊 **TỔNG HỢP:** Tổng cộng {total} cá thể được phát hiện - Cần KIỂM TRA mật độ!")
        has_alert = True
    
    return has_alert