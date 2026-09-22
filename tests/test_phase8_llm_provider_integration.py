from app.services.llm_service import LLMService, LLMServiceFactory


def test_llm_service_falls_back_to_mock_when_demo_key_is_used():
    service = LLMService(provider='openai_compatible', api_key='demo-key', base_url='http://localhost:11434/v1')
    result = service.generate_text('Draft a proposal summary for enterprise AI strategy.')

    assert result
    assert 'proposal' in result.lower() or 'ai' in result.lower()


def test_llm_factory_returns_provider_service():
    service = LLMServiceFactory.create(provider='mock')
    assert isinstance(service, LLMService)
    assert service.provider == 'mock'
