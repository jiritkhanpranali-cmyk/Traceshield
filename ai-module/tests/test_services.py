
"""
TraceShield Service Tests.

Tests the core service-layer functionality:
- AI service
- Report generator
- LLM service
"""

from app.schemas.investigation_input import (
    InvestigationInput,
    RiskIndicator,
    TransactionSummary,
)
from app.services.ai_service import ai_service
from app.services.llm_service import llm_service
from app.services.report_generator import report_generator


def create_test_investigation() -> InvestigationInput:
    """
    Create a small synthetic investigation for service testing.
    """

    return InvestigationInput(
        case_id="TS-SERVICE-001",
        wallet_address="0xSERVICEWALLET",
        network="Ethereum",
        transaction_summary=TransactionSummary(
            total_transactions=5,
            incoming_transactions=3,
            outgoing_transactions=2,
            total_value_received=2500.0,
            total_value_sent=1200.0,
            summary="Synthetic service test data.",
        ),
        risk_indicators=[
            RiskIndicator(
                indicator="Test indicator",
                severity="low",
                description="Synthetic test indicator.",
                evidence=["0xSERVICE_TX"],
            )
        ],
    )


def test_ai_service_summary():
    """
    Test AI service investigation summary generation.
    """

    investigation = create_test_investigation()

    summary = ai_service.generate_investigation_summary(
        investigation
    )

    assert isinstance(summary, str)
    assert "0xSERVICEWALLET" in summary
    assert "Ethereum" in summary
    assert "5 transaction(s)" in summary
    assert "Test indicator" in summary


def test_ai_service_context():
    """
    Test construction of structured AI context.
    """

    investigation = create_test_investigation()

    context = ai_service.build_ai_context(
        investigation
    )

    assert context["case_id"] == "TS-SERVICE-001"
    assert context["wallet_address"] == "0xSERVICEWALLET"
    assert context["network"] == "Ethereum"

    assert context["transaction_summary"]["total_transactions"] == 5

    assert len(context["risk_indicators"]) == 1
    assert context["risk_indicators"][0]["indicator"] == "Test indicator"


def test_report_generator():
    """
    Test structured investigation report generation.
    """

    investigation = create_test_investigation()

    report = report_generator.generate_report(
        investigation
    )

    assert report.case_information.case_id == "TS-SERVICE-001"
    assert report.case_information.network == "Ethereum"

    assert (
        report.transaction_summary.total_transactions
        == 5
    )

    assert len(report.risk_indicators) == 1

    assert (
        report.risk_indicators[0].indicator
        == "Test indicator"
    )

    assert len(report.limitations) > 0


def test_llm_service_configuration():
    """
    Test LLM configuration status.
    """

    status = llm_service.get_configuration_status()

    assert "configured" in status
    assert "model" in status
    assert "provider" in status

    assert isinstance(status["configured"], bool)
    assert isinstance(status["model"], str)
    assert isinstance(status["provider"], str)

