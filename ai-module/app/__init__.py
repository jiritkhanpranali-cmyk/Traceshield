
"""
TraceShield Services Package.

This package contains the service layer responsible for:

- Blockchain transaction processing
- Transaction and risk analysis
- AI-assisted investigation explanations
- Investigation report generation
- LLM prompt preparation
- External LLM provider integration
- Complete investigation orchestration
"""

from app.services.ai_service import AIService, ai_service
from app.services.analysis_service import (
    AnalysisService,
    analysis_service,
)
from app.services.blockchain_service import (
    BlockchainService,
    blockchain_service,
)
from app.services.investigation_service import (
    InvestigationService,
    investigation_service,
)
from app.services.llm_provider import (
    LLMProvider,
    llm_provider,
)
from app.services.llm_service import (
    LLMService,
    llm_service,
)
from app.services.report_generator import (
    ReportGenerator,
    report_generator,
)


__all__ = [
    "AIService",
    "ai_service",
    "AnalysisService",
    "analysis_service",
    "BlockchainService",
    "blockchain_service",
    "InvestigationService",
    "investigation_service",
    "LLMProvider",
    "llm_provider",
    "LLMService",
    "llm_service",
    "ReportGenerator",
    "report_generator",
]


