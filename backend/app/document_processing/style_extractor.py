from __future__ import annotations

from typing import Any


class StyleExtractor:
    def extract(self, analysis: dict[str, Any]) -> dict[str, Any]:
        style = analysis.get("style", {})
        source_type = analysis.get("source_type", "unknown")

        return {
            "source_type": source_type,
            "tone": "professional",
            "layout": "standard",
            "heading_style": "default",
            "font_preferences": style.get("fonts", {}),
            "color_palette": style.get("colors", {}),
            "structure_summary": {
                "slide_count": analysis.get("slide_count"),
                "page_count": analysis.get("page_count"),
                "heading_count": len(analysis.get("headings", [])),
            },
        }
