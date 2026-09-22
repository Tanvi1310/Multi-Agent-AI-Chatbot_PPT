from app.agents.orchestrator import MultiAgentOrchestrator
from app.agents.validation_agent import ValidationAgent


def test_validation_agent_builds_traceability_metadata():
    result = ValidationAgent().run({
        'request': 'Research generative AI trends and draft a proposal.',
        'artifact_file': 'storage/artifacts/generated_proposal_v2.docx',
        'retrieved_context': 'Enterprise AI strategy and modernization guidance.',
        'citations': ['https://example.com/ai-trends', 'internal://enterprise-rag'],
        'artifact_type': 'docx',
        'version': 'v2',
    })

    assert result['passed'] is True
    assert result['traceability']['artifact_file'] == 'storage/artifacts/generated_proposal_v2.docx'
    assert result['traceability']['source_citations']
    assert 'validation' in result['validation_summary'].lower()


def test_orchestrator_returns_citations_and_traceability():
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.run(
        request='Research generative AI trends and create a deck for leadership.',
        conversation_id=7,
        uploaded_files=['sample.pptx'],
        user_context={'theme': 'leadership deck'},
    )

    assert result['status'] == 'completed'
    assert result['citations']
    assert 'traceability' in result
    assert result['traceability']['request']
    assert result['traceability']['artifact_files']
