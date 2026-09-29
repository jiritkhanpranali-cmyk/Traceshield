
"""
TraceShield Investigation API.

This module provides the investigation endpoint.

The endpoint:
1. Receives investigation data.
2. Validates the input using Pydantic.
3. Generates a structured investigation report.
4. Returns the report as JSON.

No blockchain data is fetched directly by this API.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.investigation_input import InvestigationInput
from app.schemas.investigation_report import InvestigationReport
from app.services.report_generator import report_generator


router = APIRouter(
    prefix="/investigation",
    tags=["Investigation"],
)


@router.post(
    "/generate",
    response_model=InvestigationReport,
)
def generate_investigation_report(
    investigation: InvestigationInput,
) -> InvestigationReport:
    """
    Generate a TraceShield investigation report.

    Request:
        InvestigationInput

    Response:
        InvestigationReport
    """

    try:
        report = report_generator.generate_report(
            investigation
        )

        return report

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate investigation report: {exc}",
        ) from exc

