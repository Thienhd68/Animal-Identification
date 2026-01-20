# 🐄 Hệ thống phân loại & đếm động vật

Hệ thống nhận diện và đếm động vật trong chăn nuôi sử dụng AI YOLOv8.

## 🚀 Cách chạy

### Cách 1: Sử dụng file batch (Đơn giản nhất)
1. Double-click vào file `run_app.bat`
2. Ứng dụng sẽ tự động mở trình duyệt

### Cách 2: Manual qua Command Prompt
```bash
cd C:\Users\Ryan24\Downloads\MODELS\MODELS
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

### Bước 3: Mở trình duyệt
Mở trình duyệt web và truy cập: `http://localhost:8501`

## 📋 Tính năng
- ✅ Upload ảnh hoặc video động vật
- ✅ Nhận diện tự động với YOLOv8
- ✅ Đếm số lượng chính xác
- ✅ Tracking video với ByteTrack
- ✅ Cảnh báo mật độ chăn nuôi
- ✅ Lịch sử phân tích

## 🛠️ Công nghệ sử dụng
- **YOLOv8** (Ultralytics) - Object Detection
- **Streamlit** - Web UI
- **OpenCV** - Xử lý ảnh/video
- **PyTorch** - Deep Learning Framework

## 📁 Cấu trúc thư mục
```
MODELS/
├── app.py              # Ứng dụng chính
├── predict.py          # Logic xử lý AI
├── config.py           # Cấu hình
├── model/
│   └── best.pt         # Model YOLOv8 đã train
├── layout/             # Components UI
├── styles/             # CSS styling
└── requirements.txt    # Dependencies
```