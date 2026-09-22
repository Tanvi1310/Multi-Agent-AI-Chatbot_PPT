from app.agents.rag_agent import EnterpriseRAGAgent
from app.agents.web_research_agent import WebResearchAgent
from app.rag.vector_store import MockVectorStore, VectorStoreFactory
from app.services.research_service import ResearchService, ResearchServiceFactory


def test_research_service_returns_citations_and_results():
    service = ResearchServiceFactory.create(provider='mock')
    result = service.search('generative AI trends in enterprise workflows')

    assert result['query'] == 'generative AI trends in enterprise workflows'
    assert result['results']
    assert result['citations']


def test_vector_store_returns_match_results():
    store = VectorStoreFactory.create(provider='mock')
    matches = store.similarity_search('enterprise AI strategy plan', k=2)

    assert matches
    assert any('enterprise' in str(match.get('content', '')).lower() for match in matches)


def test_agents_use_live_style_search_and_rag_output():
    research = WebResearchAgent().run({'request': 'Research generative AI trends for enterprise proposals'})
    rag = EnterpriseRAGAgent().run({'request': 'Find enterprise AI strategy guidance'})

    assert research['status'] == 'completed'
    assert research['citations']
    assert rag['status'] == 'completed'
    assert rag['retrieved_context']
    assert rag['citations']
