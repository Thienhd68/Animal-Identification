import streamlit as st

def render_uploader(data_type="image"):
    """
    Trả về:
        uploaded_file (file | None)
        data_type (image | video)
    """

    st.markdown(
        "<div class='section-title'>📤 Tải dữ liệu</div>",
        unsafe_allow_html=True
    )

    if data_type == "image":
        uploaded_file = st.file_uploader(
            "Chọn ảnh (jpg, png)",
            type=["jpg", "jpeg", "png"]
        )
    else:
        uploaded_file = st.file_uploader(
            "Chọn video (mp4)",
            type=["mp4"]
        )

    # ⚠️ BẮT BUỘC – DÒNG NÀY KHÔNG ĐƯỢC THIẾU
    return uploaded_file, data_type
