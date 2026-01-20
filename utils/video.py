import cv2
import tempfile
from predict import predict_animals

def process_video(
    uploaded_file,
    frame_skip: int = 5
):
    """
    Xử lý toàn bộ video:
    - Lấy frame theo frame_skip
    - Detect từng frame
    - Gom toàn bộ detection
    """
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(uploaded_file.read())

    cap = cv2.VideoCapture(temp.name)

    frame_id = 0
    all_detections = []
    last_frame_rgb = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        if frame_id % frame_skip != 0:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        detections = predict_animals(frame_rgb)
        all_detections.extend(detections)

        last_frame_rgb = frame_rgb

    cap.release()

    return last_frame_rgb, all_detections
