
"""
TraceShield LLM API.

This module exposes the LLM service through API endpoints.

The current implementation:
- Reports LLM configuration status.
- Builds an investigation prompt from supplied data.
- Does not call an external LLM unless a provider is
  connected later.
"""

from fastapi import APIRouter

from app.schemas.investigation_input import InvestigationInput
from app.services.llm_service import llm_service


router = APIRouter(
    prefix="/llm",
    tags=["LLM"],
)


@router.get("/status")
def get_llm_status():
    """
    Return the current LLM configuration status.
    """
    return llm_service.get_configuration_status()


@router.post("/prepare")
def prepare_llm_request(
    investigation: InvestigationInput,
):
    """
    Prepare an investigation for LLM processing.

    This endpoint only creates the system prompt and
    user prompt. It does not send data to an external
    LLM provider.
    """
    result = llm_service.generate_explanation(
        investigation
    )

    return {
        "status": "prepared",
        "configured": result["configured"],
        "model": result["model"],
        "system_prompt": result["system_prompt"],
        "user_prompt": result["user_prompt"],
    }
