from __future__ import annotations

from pathlib import Path

import cv2
import pytesseract
from PIL import Image


class OCRAnalyzer:
    def analyze(self, file_path: str) -> dict:
        image_path = Path(file_path)
        pil_image = Image.open(image_path)
        text = pytesseract.image_to_string(pil_image)
        image = cv2.imread(str(image_path))
        height, width, _ = image.shape if image is not None else (0, 0, 0)

        return {
            "source_type": "image_ocr",
            "file_name": image_path.name,
            "title": image_path.stem,
            "text": text.strip(),
            "dimensions": {"width": width, "height": height},
            "ocr_confidence": "approximate",
        }
