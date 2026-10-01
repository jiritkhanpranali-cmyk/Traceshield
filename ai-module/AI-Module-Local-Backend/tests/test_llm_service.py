
"""
TraceShield LLM Service Tests.

Tests:
- System prompt generation
- Investigation prompt generation
- LLM explanation preparation
- Configuration status
"""

from app.schemas.investigation_input import (
    InvestigationInput,
    TransactionSummary,
)
from app.services.llm_service import llm_service


def create_test_investigation() -> InvestigationInput:
    """
    Create synthetic investigation data for LLM testing.
    """

    return InvestigationInput(
        case_id="TS-LLM-SERVICE-001",
        wallet_address="0xLLMWALLET",
        network="Ethereum",
        transaction_summary=TransactionSummary(
            total_transactions=3,
            incoming_transactions=2,
            outgoing_transactions=1,
            total_value_received=1500.0,
            total_value_sent=500.0,
            summary="Synthetic LLM service test.",
        ),
    )



def test_system_prompt():
    """
    Test that the LLM system prompt contains
    the required safety and evidence rules.
    """

    prompt = llm_service.build_system_prompt()

    assert isinstance(prompt, str)

    assert "TraceShield AI" in prompt
    assert "Never invent transactions" in prompt
    assert "wallet belongs to a person or organization" in prompt
    assert "criminal activity" in prompt
    assert "uncertainty" in prompt



def test_build_prompt():
    """
    Test construction of the investigation prompt.
    """

    investigation = create_test_investigation()

    prompt = llm_service.build_prompt(
        investigation
    )

    assert isinstance(prompt, str)

    assert "TS-LLM-SERVICE-001" in prompt
    assert "0xLLMWALLET" in prompt
    assert "Ethereum" in prompt
    assert "3" in prompt

    assert "Verified investigation data" in prompt


def test_generate_explanation():
    """
    Test preparation of the LLM explanation request.
    """

    investigation = create_test_investigation()

    result = llm_service.generate_explanation(
        investigation
    )

    assert isinstance(result, dict)

    assert "configured" in result
    assert "model" in result
    assert "system_prompt" in result
    assert "user_prompt" in result

    assert isinstance(result["configured"], bool)
    assert isinstance(result["model"], str)
    assert isinstance(result["system_prompt"], str)
    assert isinstance(result["user_prompt"], str)


def test_configuration_status():
    """
    Test LLM configuration status.
    """

    status = llm_service.get_configuration_status()

    assert isinstance(status, dict)

    assert "configured" in status
    assert "model" in status
    assert "provider" in status

    assert isinstance(status["configured"], bool)
    assert isinstance(status["model"], str)
    assert isinstance(status["provider"], str)

