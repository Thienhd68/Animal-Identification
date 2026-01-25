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

## 🛠️ Công nghệ

<table>
  <tr>
    <td align="center" width="96">
      <img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Reverse.svg" width="48" height="48" alt="YOLOv8" />
      <br><strong>YOLOv8</strong>
      <br><sub>Object Detection</sub>
    </td>
    <td align="center" width="96">
      <img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="48" height="48" alt="Streamlit" />
      <br><strong>Streamlit</strong>
      <br><sub>Web Interface</sub>
    </td>
    <td align="center" width="96">
      <img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/NumPy_logo.svg" width="48" height="48" alt="NumPy" />
      <br><strong>NumPy</strong>
      <br><sub>Data Processing</sub>
    </td>
    <td align="center" width="96">
      <img src="https://opencv.org/wp-content/uploads/2022/05/logo.png" width="48" height="48" alt="OpenCV" />
      <br><strong>OpenCV</strong>
      <br><sub>Image Processing</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="96">
      <img src="https://pytorch.org/assets/images/pytorch-logo.png" width="48" height="48" alt="PyTorch" />
      <br><strong>PyTorch</strong>
      <br><sub>Deep Learning</sub>
    </td>
    <td align="center" width="96">
      <img src="https://pandas.pydata.org/static/img/pandas_mark.svg" width="48" height="48" alt="Pandas" />
      <br><strong>Pandas</strong>
      <br><sub>Data Analysis</sub>
    </td>
    <td align="center" width="96">
      <img src="https://matplotlib.org/stable/_images/sphx_glr_logos2_003.png" width="48" height="48" alt="Matplotlib" />
      <br><strong>Matplotlib</strong>
      <br><sub>Visualization</sub>
    </td>
    <td align="center" width="96">
      <img src="https://www.sqlite.org/images/sqlite370_banner.gif" width="48" height="48" alt="SQLite" />
      <br><strong>SQLite</strong>
      <br><sub>Database</sub>
    </td>
  </tr>
</table>

## 👥 Thực hiện

**Nhóm 9** - Đồ án Machine Learning

## 📄 License

MIT License
