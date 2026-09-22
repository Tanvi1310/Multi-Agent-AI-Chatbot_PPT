from pathlib import Path

from app.generation.document_generator import DocumentGenerator
from app.generation.ppt_generator import PPTGenerator


def test_document_generator_creates_docx_file(tmp_path):
    output_path = tmp_path / 'generated_proposal.docx'
    generator = DocumentGenerator(output_dir=str(tmp_path))
    result = generator.generate(
        title='AI Strategy Proposal',
        sections=['Executive Summary', 'Market Opportunity', 'Implementation Plan'],
        body='This document captures a practical enterprise AI roadmap.',
    )

    assert result['status'] == 'completed'
    assert Path(result['file_path']).exists()
    assert output_path.name in result['file_path']


def test_ppt_generator_creates_pptx_file(tmp_path):
    output_path = tmp_path / 'generated_deck.pptx'
    generator = PPTGenerator(output_dir=str(tmp_path))
    result = generator.generate(
        title='AI Transformation Deck',
        slides=[
            {'title': 'Agenda', 'bullets': ['Overview', 'Plan', 'Outcomes']},
            {'title': 'Outcome', 'bullets': ['Scalable rollout', 'ROI focus']},
        ],
    )

    assert result['status'] == 'completed'
    assert Path(result['file_path']).exists()
    assert output_path.name in result['file_path']
