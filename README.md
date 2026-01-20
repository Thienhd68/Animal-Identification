# 🐄 Hệ thống phân loại & đếm động vật

Hệ thống nhận diện và đếm động vật trong chăn nuôi sử dụng AI YOLOv8.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green)

## 📸 Demo

<!-- Thêm screenshot ứng dụng ở đây -->

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/Thienhd68/Animal-Identification.git
cd Animal-Identification
```

### 2. Tạo virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng

```bash
streamlit run app.py
```

Hoặc double-click file `run_app.bat` (Windows)

## 📋 Tính năng

- ✅ Upload ảnh hoặc video động vật
- ✅ Nhận diện tự động với YOLOv8
- ✅ Đếm số lượng chính xác
- ✅ Tracking video với ByteTrack
- ✅ Lưu trữ lịch sử vào SQLite
- ✅ Xuất báo cáo CSV

## 🛠️ Công nghệ

- **YOLOv8** - Object Detection
- **Streamlit** - Web Interface
- **OpenCV** - Image Processing
- **SQLite** - Database
- **Plotly** - Data Visualization

## 👥 Thực hiện

**Nhóm 9** - Đồ án Machine Learning

## 📄 License

MIT License
