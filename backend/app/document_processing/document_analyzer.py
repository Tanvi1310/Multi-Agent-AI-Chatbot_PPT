from __future__ import annotations

from collections import Counter
from pathlib import Path

from docx import Document


class DocumentAnalyzer:
    def analyze(self, file_path: str) -> dict:
        doc = Document(file_path)
        headings = []
        paragraphs = []
        fonts = Counter()
        colors = Counter()

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text.strip())
                if paragraph.style.name and paragraph.style.name.lower().startswith("heading"):
                    headings.append(paragraph.text.strip())
                for run in paragraph.runs:
                    if run.font.name:
                        fonts[run.font.name] += 1
                    if run.font.color and getattr(run.font.color, "rgb", None):
                        colors[f"#{run.font.color.rgb}"] += 1

        text = "\n".join(paragraphs)
        return {
            "source_type": "docx",
            "file_name": Path(file_path).name,
            "title": headings[0] if headings else (paragraphs[0] if paragraphs else "Untitled document"),
            "text": text,
            "headings": headings,
            "metadata": {
                "paragraph_count": len(paragraphs),
                "heading_count": len(headings),
            },
            "style": {
                "fonts": dict(fonts.most_common(5)),
                "colors": dict(colors.most_common(5)),
            },
        }
