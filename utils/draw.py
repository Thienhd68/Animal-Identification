import cv2
import numpy as np
from typing import List, Tuple

# result format:
# (x1, y1, x2, y2, label)

COLOR_MAP = {
    "Bò": (0, 200, 0),
    "Heo": (200, 0, 200),
    "Gà": (0, 165, 255),
}

def draw_boxes(
    image: np.ndarray,
    results: List[Tuple[int, int, int, int, str]]
) -> np.ndarray:
    """
    Vẽ bounding box + label lên ảnh

    Args:
        image: ảnh gốc (numpy array)
        results: list bounding box (x1, y1, x2, y2, label)

    Returns:
        image đã vẽ
    """

    if image is None or len(results) == 0:
        return image

    img = image.copy()

    for (x1, y1, x2, y2, label) in results:
        color = COLOR_MAP.get(label, (255, 255, 255))

        # Bounding box
        cv2.rectangle(
            img,
            (x1, y1),
            (x2, y2),
            color,
            thickness=2
        )

        # Label background
        label_text = f"{label}"
        (tw, th), _ = cv2.getTextSize(
            label_text,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            2
        )

        cv2.rectangle(
            img,
            (x1, y1 - th - 10),
            (x1 + tw + 6, y1),
            color,
            -1
        )

        # Label text
        cv2.putText(
            img,
            label_text,
            (x1 + 3, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
            cv2.LINE_AA
        )

    return img
