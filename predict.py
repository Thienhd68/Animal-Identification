import cv2

import numpy as np

from ultralytics import YOLO

import os



# =========================

# KHỞI TẠO MODEL

# =========================

try:

    # Ưu tiên lấy file model bạn đã train từ Roboflow

    model_path = os.path.join(os.path.dirname(__file__), 'best.pt')

    model = YOLO(model_path)

except Exception as e:

    print(f"Lưu ý: Đang dùng model mặc định do lỗi: {e}")

    model = YOLO('yolov8n.pt')



# =========================

# XỬ LÝ ẢNH (Dùng cho Phân tích Ảnh)

# =========================

def predict_image(image, conf=0.25):

    # Streamlit dùng RGB, OpenCV dùng BGR nên phải chuyển đổi

    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

   

    # iou=0.45 giúp loại bỏ các khung hình chồng lấn lên nhau

    results = model.predict(source=image_bgr, conf=conf, iou=0.45)

    res = results[0]

   

    output_img = image_bgr.copy()

    counter = {"Bò": 0}



    if len(res.boxes) > 0:

        for box in res.boxes:

            # Lấy tọa độ pixel chuẩn từ AI

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

            score = float(box.conf[0])

           

            # Vẽ khung màu xanh lá (Green)

            cv2.rectangle(output_img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # Ghi nhãn và độ tự tin

            cv2.putText(output_img, f"Bo {score:.2f}", (x1, y1 - 10),

                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

           

            counter["Bò"] += 1



    # Chuyển về RGB để Streamlit hiển thị đúng màu sắc

    final_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)

    return {"image": final_img, "counter": counter}



# =========================

# XỬ LÝ VIDEO (Dùng Tracking để đếm chuẩn)

# =========================

def predict_video(video_path, conf=0.4, progress_callback=None):

    cap = cv2.VideoCapture(video_path)

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps    = cap.get(cv2.CAP_PROP_FPS)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))



    # Đổi sang codec 'avc1' để có thể phát trực tiếp trên trình duyệt web

    out_path = video_path.replace(".mp4", "_out.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'avc1')

    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))



    # Sử dụng Set để lưu trữ các ID duy nhất đã từng xuất hiện

    unique_ids = set()

    timeline = []

    frame_idx = 0



    # Chạy Tracking với thuật toán ByteTrack

    # persist=True giúp AI "nhớ mặt" con bò qua từng frame

    results = model.track(source=video_path, conf=conf, iou=0.5, persist=True, stream=True, tracker="bytetrack.yaml")



    for r in results:

        frame = r.orig_img.copy()

        current_frame_count = 0

       

        # Kiểm tra xem có phát hiện được con nào và AI có gán ID không

        if r.boxes is not None and r.boxes.id is not None:

            ids = r.boxes.id.int().cpu().tolist()

           

            for i, box in enumerate(r.boxes):

                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

                obj_id = ids[i]

               

                # Lưu ID vào danh sách tổng (Set tự động loại bỏ trùng lặp)

                unique_ids.add(obj_id)

                current_frame_count += 1

               

                # Vẽ khung + ID để demo chuyên nghiệp

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

                cv2.putText(frame, f"Bo ID:{obj_id}", (x1, y1 - 10),

                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)

       

        # Ghi lại diễn biến cho biểu đồ (mỗi 1 giây video)

        if frame_idx % int(fps) == 0:

            timeline.append({'frame': frame_idx, 'counter': {'Bò': current_frame_count}})

           

        out.write(frame)

        

        # Cập nhật tiến trình

        if progress_callback and total_frames > 0:

            progress = min(frame_idx / total_frames, 1.0)

            progress_callback(progress)

            

        frame_idx += 1



    cap.release()

    out.release()

   

    # Tổng số bò = Số lượng ID duy nhất đã xuất hiện trong toàn bộ video

    total_cows = len(unique_ids)

   

    return {

        "counter": {"Bò": total_cows},

        "video_out": out_path,

        "timeline": timeline

    }