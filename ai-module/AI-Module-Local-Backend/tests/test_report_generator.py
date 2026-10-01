
"""
TraceShield Report Generator Tests.

Tests the conversion of investigation input into
the final structured investigation report.
"""

from app.schemas.investigation_input import (
    EntityIntelligence,
    FundFlow,
    InvestigationInput,
    RiskIndicator,
    TimelineEvent,
    TransactionSummary,
    WalletRelationship,
)
from app.services.report_generator import report_generator


def create_complete_investigation() -> InvestigationInput:
    """
    Create synthetic investigation data for testing.
    """

    return InvestigationInput(
        case_id="TS-REPORT-001",
        wallet_address="0xREPORTWALLET",
        network="Ethereum",

        transaction_summary=TransactionSummary(
            total_transactions=8,
            incoming_transactions=5,
            outgoing_transactions=3,
            total_value_received=4000.0,
            total_value_sent=2500.0,
            summary="Synthetic transaction summary.",
        ),

        fund_flows=[
            FundFlow(
                source_address="0xSOURCE",
                destination_address="0xREPORTWALLET",
                transaction_hash="0xREPORTTX001",
                value=1000.0,
                timestamp="2026-09-29T09:00:00Z",
                hop_number=1,
            )
        ],

        wallet_relationships=[
            WalletRelationship(
                wallet_address="0xRELATED",
                relationship_type="counterparty",
                transaction_count=2,
                total_value=800.0,
                first_seen="2026-09-01T10:00:00Z",
                last_seen="2026-09-29T09:00:00Z",
            )
        ],

        risk_indicators=[
            RiskIndicator(
                indicator="Test risk indicator",
                severity="medium",
                description="Synthetic risk observation.",
                evidence=["0xREPORTTX001"],
            )
        ],

        entity_intelligence=[
            EntityIntelligence(
                address="0xRELATED",
                entity_name="Synthetic Entity",
                entity_type="exchange",
                attribution="Test attribution",
                source="Test source",
                confidence="medium",
            )
        ],

        timeline_events=[
            TimelineEvent(
                timestamp="2026-09-29T09:00:00Z",
                block_number=123456,
                transaction_hash="0xREPORTTX001",
                event_type="transfer",
                description="Synthetic transfer.",
                evidence_reference="0xREPORTTX001",
            )
        ],
    )


def test_generate_complete_report():
    """
    Test generation of a complete investigation report.
    """

    investigation = create_complete_investigation()

    report = report_generator.generate_report(
        investigation
    )

    assert report.case_information.case_id == "TS-REPORT-001"
    assert report.case_information.network == "Ethereum"
    assert (
        report.case_information.investigated_wallet
        == "0xREPORTWALLET"
    )

    assert (
        report.transaction_summary.total_transactions
        == 8
    )

    assert len(report.major_fund_flows) == 1
    assert (
        report.major_fund_flows[0].transaction_hash
        == "0xREPORTTX001"
    )

    assert len(report.wallet_relationships) == 1
    assert (
        report.wallet_relationships[0].wallet_address
        == "0xRELATED"
    )

    assert len(report.risk_indicators) == 1
    assert (
        report.risk_indicators[0].indicator
        == "Test risk indicator"
    )

    assert len(report.entity_intelligence) == 1
    assert (
        report.entity_intelligence[0].entity_name
        == "Synthetic Entity"
    )

    assert len(report.investigation_timeline) == 1

    assert "0xREPORTTX001" in report.evidence_references

    assert len(report.investigation_summary) > 0
    assert len(report.analytical_interpretation) > 0
    assert len(report.limitations) > 0


def test_report_preserves_supplied_explanation():
    """
    Test that a supplied fund-flow explanation is preserved.
    """

    investigation = InvestigationInput(
        case_id="TS-REPORT-002",
        wallet_address="0xWALLET",
        network="Ethereum",
        fund_flows=[
            FundFlow(
                source_address="0xSOURCE",
                destination_address="0xWALLET",
                transaction_hash="0xTX",
                value=500.0,
                explanation="Custom investigator explanation.",
            )
        ],
    )

    report = report_generator.generate_report(
        investigation
    )

    assert (
        report.major_fund_flows[0].explanation
        == "Custom investigator explanation."
    )


def test_report_preserves_supplied_risk_explanation():
    """
    Test that a supplied risk explanation is preserved.
    """

    investigation = InvestigationInput(
        case_id="TS-REPORT-003",
        wallet_address="0xWALLET",
        network="Ethereum",
        risk_indicators=[
            RiskIndicator(
                indicator="Custom indicator",
                severity="low",
                explanation="Custom investigator explanation.",
            )
        ],
    )

    report = report_generator.generate_report(
        investigation
    )

    assert (
        report.risk_indicators[0].explanation
        == "Custom investigator explanation."
    )


def test_report_has_required_limitations():
    """
    Test that important analytical limitations are included.
    """

    investigation = InvestigationInput(
        case_id="TS-REPORT-004",
        wallet_address="0xWALLET",
        network="Ethereum",
    )

    report = report_generator.generate_report(
        investigation
    )

    assert len(report.limitations) >= 5

    limitations_text = " ".join(
        report.limitations
    ).lower()

    assert "ownership" in limitations_text
    assert "criminal" in limitations_text

