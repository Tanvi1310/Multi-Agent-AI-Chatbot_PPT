from __future__ import annotations

from pathlib import Path
from typing import Any

from app.document_processing.document_analyzer import DocumentAnalyzer
from app.document_processing.ocr_analyzer import OCRAnalyzer
from app.document_processing.pdf_analyzer import PDFAnalyzer
from app.document_processing.style_extractor import StyleExtractor
from app.ppt_processing.ppt_analyzer import PPTAnalyzer


class AnalysisService:
    def __init__(self) -> None:
        self.doc_analyzer = DocumentAnalyzer()
        self.ppt_analyzer = PPTAnalyzer()
        self.pdf_analyzer = PDFAnalyzer()
        self.ocr_analyzer = OCRAnalyzer()
        self.style_extractor = StyleExtractor()

    def analyze_file(self, file_path: str) -> dict[str, Any]:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".docx":
            analysis = self.doc_analyzer.analyze(str(path))
        elif suffix == ".pptx":
            analysis = self.ppt_analyzer.analyze(str(path))
        elif suffix == ".pdf":
            analysis = self.pdf_analyzer.analyze(str(path))
        elif suffix in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
            analysis = self.ocr_analyzer.analyze(str(path))
        else:
            raise ValueError(f"Unsupported file type for analysis: {suffix}")

        analysis["style"] = self.style_extractor.extract(analysis)
        return analysis
