
"""
TraceShield AI Service Tests.

Tests the explanation and evidence-processing logic
implemented by the TraceShield AI service.
"""

from app.schemas.investigation_input import (
    FundFlow,
    InvestigationInput,
    RiskIndicator,
    TimelineEvent,
)
from app.services.ai_service import ai_service


def test_explain_fund_flow():
    """
    Test fund-flow explanation generation.
    """

    fund_flow = FundFlow(
        source_address="0xSOURCE",
        destination_address="0xDESTINATION",
        transaction_hash="0xTX001",
        value=1500.0,
        timestamp="2026-09-29T10:00:00Z",
        hop_number=2,
    )

    explanation = ai_service.explain_fund_flow(
        fund_flow
    )

    assert isinstance(explanation, str)
    assert "0xSOURCE" in explanation
    assert "0xDESTINATION" in explanation
    assert "0xTX001" in explanation
    assert "1500.0" in explanation
    assert "Fund-flow hop: 2" in explanation


def test_explain_risk_indicator():
    """
    Test risk-indicator explanation generation.
    """

    indicator = RiskIndicator(
        indicator="Unusual transaction pattern",
        severity="medium",
        description="Synthetic test observation.",
        evidence=["0xTX001", "0xTX002"],
    )

    explanation = ai_service.explain_risk_indicator(
        indicator
    )

    assert isinstance(explanation, str)
    assert "Unusual transaction pattern" in explanation
    assert "medium" in explanation
    assert "0xTX001" in explanation
    assert "0xTX002" in explanation
    assert "does not by itself establish criminal activity" in explanation


def test_generate_timeline():
    """
    Test timeline generation and chronological sorting.
    """

    investigation = InvestigationInput(
        case_id="TS-AI-001",
        wallet_address="0xWALLET",
        network="Ethereum",
        timeline_events=[
            TimelineEvent(
                timestamp="2026-09-29T12:00:00Z",
                block_number=200,
                transaction_hash="0xTX002",
                event_type="transfer",
                description="Second event",
                evidence_reference="REF002",
            ),
            TimelineEvent(
                timestamp="2026-09-29T10:00:00Z",
                block_number=100,
                transaction_hash="0xTX001",
                event_type="transfer",
                description="First event",
                evidence_reference="REF001",
            ),
        ],
    )

    timeline = ai_service.generate_timeline(
        investigation
    )

    assert len(timeline) == 2
    assert timeline[0]["transaction_hash"] == "0xTX001"
    assert timeline[1]["transaction_hash"] == "0xTX002"


def test_generate_evidence_references():
    """
    Test collection and de-duplication of evidence references.
    """

    investigation = InvestigationInput(
        case_id="TS-AI-002",
        wallet_address="0xWALLET",
        network="Ethereum",
        fund_flows=[
            FundFlow(
                transaction_hash="0xTX001"
            )
        ],
        risk_indicators=[
            RiskIndicator(
                indicator="Test indicator",
                evidence=[
                    "0xTX001",
                    "0xTX002",
                ],
            )
        ],
        timeline_events=[
            TimelineEvent(
                transaction_hash="0xTX002",
                evidence_reference="REF001",
            )
        ],
    )

    references = ai_service.generate_evidence_references(
        investigation
    )

    assert references == [
        "0xTX001",
        "0xTX002",
        "REF001",
    ]

