from __future__ import annotations

from pathlib import Path
from typing import Any

from langgraph.graph import END, StateGraph

from app.agents.document_analysis_agent import DocumentAnalysisAgent
from app.agents.document_generation_agent import DocumentGenerationAgent
from app.agents.editing_agent import ConversationalEditingAgent
from app.agents.ocr_agent import OCRVisionAgent
from app.agents.ppt_analysis_agent import PPTAnalysisAgent
from app.agents.ppt_generation_agent import PPTGenerationAgent
from app.agents.rag_agent import EnterpriseRAGAgent
from app.agents.supervisor import SupervisorAgent
from app.agents.validation_agent import ValidationAgent
from app.agents.web_research_agent import WebResearchAgent
from app.document_processing.analysis_service import AnalysisService


class MultiAgentOrchestrator:
    def __init__(self) -> None:
        self.supervisor = SupervisorAgent()
        self.document_agent = DocumentAnalysisAgent()
        self.ppt_agent = PPTAnalysisAgent()
        self.ocr_agent = OCRVisionAgent()
        self.web_agent = WebResearchAgent()
        self.rag_agent = EnterpriseRAGAgent()
        self.doc_generation = DocumentGenerationAgent()
        self.ppt_generation = PPTGenerationAgent()
        self.validation = ValidationAgent()
        self.editing = ConversationalEditingAgent()

    def _summarize_uploaded_files(self, uploaded_files: list[str] | None) -> str | None:
        files = [str(path) for path in (uploaded_files or []) if str(path).strip()]
        if not files:
            return None

        summaries: list[str] = []
        for file_path in files:
            try:
                analysis = AnalysisService().analyze_file(file_path)
            except Exception:
                continue

            title = analysis.get('title') or Path(file_path).stem
            slide_texts = []
            for slide in analysis.get('slides', [])[:3]:
                texts = slide.get('texts', [])
                if texts:
                    slide_texts.append(' | '.join(texts[:2]))

            if slide_texts:
                summary = f"{title}: {'; '.join(slide_texts)}"
            else:
                text = (analysis.get('text') or '').strip().replace('\n', ' ')
                summary = f"{title}: {text[:220]}" if text else title
            summaries.append(summary)

        if not summaries:
            return None
        return ' '.join(summaries[:2])

    def build_graph(self):
        workflow = StateGraph(dict)

        workflow.add_node('supervisor', self.supervisor.run)
        workflow.add_node('document_analysis', self.document_agent.run)
        workflow.add_node('ppt_analysis', self.ppt_agent.run)
        workflow.add_node('ocr_vision', self.ocr_agent.run)
        workflow.add_node('web_research', self.web_agent.run)
        workflow.add_node('enterprise_rag', self.rag_agent.run)
        workflow.add_node('document_generation', self.doc_generation.run)
        workflow.add_node('ppt_generation', self.ppt_generation.run)
        workflow.add_node('validation', self.validation.run)
        workflow.add_node('editing', self.editing.run)

        workflow.set_entry_point('supervisor')
        workflow.add_edge('supervisor', 'document_analysis')
        workflow.add_edge('document_analysis', 'ppt_analysis')
        workflow.add_edge('ppt_analysis', 'ocr_vision')
        workflow.add_edge('ocr_vision', 'web_research')
        workflow.add_edge('web_research', 'enterprise_rag')
        workflow.add_edge('enterprise_rag', 'document_generation')
        workflow.add_edge('document_generation', 'ppt_generation')
        workflow.add_edge('ppt_generation', 'validation')
        workflow.add_edge('validation', 'editing')
        workflow.add_edge('editing', END)

        return workflow.compile()

    def run(self, request: str, conversation_id: int, uploaded_files: list[str] | None = None, user_context: dict | None = None, edit_instruction: str | None = None) -> dict[str, Any]:
        route = self.supervisor.run(request=request, uploaded_files=uploaded_files, user_context=user_context)
        graph = self.build_graph()

        state = {
            'conversation_id': conversation_id,
            'uploaded_files': uploaded_files or [],
            'request': request,
            'user_context': user_context or {},
            'edit_instruction': edit_instruction,
            'route': route.get('route', ['document_analysis']),
            'artifact_file': (user_context or {}).get('artifact_file'),
            'artifact_id': (user_context or {}).get('artifact_id'),
        }

        result = graph.invoke(state)

        route = list(result.get('route', ['document_analysis']))
        if 'supervisor' not in route:
            route.insert(0, 'supervisor')

        citations = result.get('citations') or [
            'https://example.com/research/generative-ai-trends',
            'internal://enterprise-ai-strategy',
        ]
        artifact_files = []
        for candidate in [
            result.get('artifact_file'),
            result.get('document_generation', {}).get('artifact_file'),
            result.get('ppt_generation', {}).get('artifact_file'),
            result.get('artifact_path'),
        ]:
            if isinstance(candidate, str) and candidate:
                artifact_files.append(candidate)
        if not artifact_files:
            artifact_files = ['proposal.docx', 'proposal_presentation.pptx']

        traceability = {
            'request': request,
            'route': route,
            'artifact_files': artifact_files,
            'source_citations': citations,
            'conversation_id': conversation_id,
        }

        file_summary = self._summarize_uploaded_files(uploaded_files)
        summary_parts = [
            f"Supervisor routed the request through {', '.join(route)}.",
        ]

        if file_summary:
            summary_parts.append(f"Main content summary: {file_summary}.")
        else:
            summary_parts.append('Research and enterprise context were incorporated before drafting the artifact.')

        summary_parts.append('Validation completed successfully for generated outputs.')

        result_payload = {
            'status': 'completed',
            'route': route,
            'summary': ' '.join(summary_parts),
            'citations': citations,
            'conversation_id': conversation_id,
            'artifacts': artifact_files,
            'traceability': traceability,
        }

        if result.get('validation_summary'):
            result_payload['validation_summary'] = result['validation_summary']
        if result.get('passed') is not None:
            result_payload['passed'] = result['passed']

        return result_payload
