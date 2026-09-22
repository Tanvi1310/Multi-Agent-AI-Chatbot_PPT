from __future__ import annotations

from typing import Any

from app.config import get_settings


class LLMService:
    def __init__(self, provider: str = 'mock', model: str | None = None, api_key: str | None = None, base_url: str | None = None) -> None:
        settings = get_settings()
        self.provider = (provider or settings.llm_provider or 'mock').lower()
        self.model = model or settings.llm_model or 'gpt-4o-mini'
        self.api_key = api_key or settings.llm_api_key or ''
        self.base_url = base_url or settings.llm_base_url or 'http://localhost:11434/v1'
        self._client = None

        if self.provider in {'openai', 'openai_compatible'} and self.api_key and self.api_key != 'demo-key':
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            except Exception:
                self._client = None

    def _mock_response(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if 'proposal' in prompt_lower:
            return 'AI Strategy Proposal: This proposal emphasizes phased modernization, executive storytelling, and measurable ROI across the enterprise.'
        if 'deck' in prompt_lower or 'presentation' in prompt_lower or 'slides' in prompt_lower:
            return 'Leadership Deck: This presentation summarizes enterprise AI priorities, operating model changes, and near-term value creation.'
        if 'research' in prompt_lower or 'trend' in prompt_lower:
            return 'Research Summary: Generative AI adoption is accelerating across enterprise workflows, with strongest value in automation, insight generation, and decision support.'
        return 'AI response: The system synthesized a practical enterprise AI recommendation with measurable business value and phased implementation guidance.'

    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        if self.provider == 'mock' or self.api_key == 'demo-key' or self._client is None:
            return self._mock_response(prompt)

        try:
            completion = self._client.chat.completions.create(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                temperature=kwargs.get('temperature', 0.3),
            )
            return completion.choices[0].message.content or self._mock_response(prompt)
        except Exception:
            return self._mock_response(prompt)


class LLMServiceFactory:
    @staticmethod
    def create(provider: str | None = None, **kwargs: Any) -> LLMService:
        settings = get_settings()
        chosen = (provider or settings.llm_provider or 'mock').lower()
        return LLMService(
            provider=chosen,
            model=kwargs.get('model') or settings.llm_model,
            api_key=kwargs.get('api_key') or settings.llm_api_key,
            base_url=kwargs.get('base_url') or settings.llm_base_url,
        )
