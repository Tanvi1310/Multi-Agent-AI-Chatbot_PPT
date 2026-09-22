from __future__ import annotations

from pathlib import Path

import fitz


class PDFAnalyzer:
    def analyze(self, file_path: str) -> dict:
        doc = fitz.open(file_path)
        text_pages = []
        for page in doc:
            text_pages.append(page.get_text("text"))

        return {
            "source_type": "pdf",
            "file_name": Path(file_path).name,
            "title": Path(file_path).stem,
            "text": "\n".join(text_pages),
            "page_count": len(doc),
            "pages": [{"page_number": i + 1, "text": page_text} for i, page_text in enumerate(text_pages)],
        }
