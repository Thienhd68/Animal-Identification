import os

import cv2
import numpy as np
from ultralytics import YOLO

# =========================
# KHỞI TẠO MODEL
# =========================

try:
    # Ưu tiên load model đã train
    model_path = os.path.join(os.path.dirname(__file__), "best.pt")
    model = YOLO(model_path)

except Exception as e:
    print(f"Lưu ý: Đang dùng model mặc định do lỗi: {e}")
    model = YOLO("yolov8n.pt")

# =========================
# XỬ LÝ ẢNH (Dùng cho phân tích ảnh)
# =========================


def predict_image(image, conf: float = 0.25):
    """
    Detect object trong ảnh.

    Args:
        image (np.ndarray): Ảnh RGB từ Streamlit.
        conf (float): Ngưỡng confidence.

    Returns:
        dict: {
            "image": ảnh output RGB,
            "counter": {"Bò": int}
        }
    """

    # Streamlit dùng RGB, OpenCV dùng BGR
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # iou giúp loại bỏ box chồng lấn
    results = model.predict(source=image_bgr, conf=conf, iou=0.45)

    res = results[0]
    output_img = image_bgr.copy()

    counter = {"Bò": 0}

    if len(res.boxes) > 0:
        for box in res.boxes:
            # Tọa độ bounding box
            x1, y1, x2, y2 = (
                box.xyxy[0].cpu().numpy().astype(int)
            )

            score = float(box.conf[0])

            # Vẽ bounding box
            cv2.rectangle(
                output_img,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3,
            )

            # Ghi label
            cv2.putText(
                output_img,
                f"Bo {score:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            counter["Bò"] += 1

    # Chuyển về RGB để Streamlit hiển thị
    final_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)

    return {
        "image": final_img,
        "counter": counter,
    }


# =========================
# XỬ LÝ VIDEO (Tracking + Đếm)
# =========================


def predict_video(video_path, conf: float = 0.4, progress_callback=None):
    """
    Detect + Track bò trong video bằng ByteTrack.

    Args:
        video_path (str): Đường dẫn video input.
        conf (float): Ngưỡng confidence.
        progress_callback (callable): Hàm update progress.

    Returns:
        dict:
        {
            "counter": {"Bò": total},
            "video_out": path,
            "timeline": [...]
        }
    """

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Output video
    out_path = video_path.replace(".mp4", "_out.mp4")

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    # Lưu ID duy nhất
    unique_ids = set()

    timeline = []
    frame_idx = 0

    # Tracking bằng ByteTrack
    results = model.track(
        source=video_path,
        conf=conf,
        iou=0.5,
        persist=True,
        stream=True,
        tracker="bytetrack.yaml",
    )

    for r in results:
        frame = r.orig_img.copy()
        current_frame_count = 0

        # Kiểm tra có detection + ID không
        if r.boxes is not None and r.boxes.id is not None:
            ids = r.boxes.id.int().cpu().tolist()

            for i, box in enumerate(r.boxes):
                x1, y1, x2, y2 = (
                    box.xyxy[0].cpu().numpy().astype(int)
                )

                obj_id = ids[i]

                # Thêm vào set (auto unique)
                unique_ids.add(obj_id)
                current_frame_count += 1

                # Vẽ bounding box + ID
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3,
                )

                cv2.putText(
                    frame,
                    f"Bo ID:{obj_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    3,
                )

        # Lưu timeline mỗi 1 giây
        if fps > 0 and frame_idx % int(fps) == 0:
            timeline.append(
                {
                    "frame": frame_idx,
                    "counter": {"Bò": current_frame_count},
                }
            )

        out.write(frame)

        # Update progress
        if progress_callback and total_frames > 0:
            progress = min(frame_idx / total_frames, 1.0)
            progress_callback(progress)

        frame_idx += 1

    cap.release()
    out.release()

    # Tổng bò = số ID unique
    total_cows = len(unique_ids)

    return {
        "counter": {"Bò": total_cows},
        "video_out": out_path,
        "timeline": timeline,
    }
