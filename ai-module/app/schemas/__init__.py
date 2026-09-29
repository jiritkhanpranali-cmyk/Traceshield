
"""
TraceShield schema package.

This package contains Pydantic models used for
investigation input and investigation reports.
"""

from app.schemas.investigation_input import InvestigationInput
from app.schemas.investigation_report import InvestigationReport

__all__ = [
    "InvestigationInput",
    "InvestigationReport",
]
