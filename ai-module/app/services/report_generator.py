from typing import List

from app.schemas.investigation_input import InvestigationInput
from app.schemas.investigation_report import (
    CaseInformation,
    EntityIntelligenceReport,
    FundFlowReport,
    InvestigationReport,
    RiskIndicatorReport,
    TimelineReport,
    TransactionReport,
    WalletRelationshipReport,
)
from app.services.ai_service import ai_service


class ReportGenerator:
    """
    Generates the final TraceShield investigation report.

    This service only transforms information already supplied
    by the investigation/analysis layer.

    It does not:
    - fetch blockchain data
    - invent evidence
    - determine wallet ownership
    - establish criminal activity
    - create unsupported conclusions
    """

    def generate_report(
        self,
        investigation: InvestigationInput
    ) -> InvestigationReport:
        """
        Convert InvestigationInput into a structured
        InvestigationReport.
        """

        # --------------------------------------------------
        # 1. Case information
        # --------------------------------------------------

        case_information = CaseInformation(
            case_id=investigation.case_id,
            network=investigation.network,
            investigated_wallet=investigation.wallet_address,
        )

        # --------------------------------------------------
        # 2. Investigation summary
        # --------------------------------------------------

        investigation_summary = (
            ai_service.generate_investigation_summary(
                investigation
            )
        )

        # --------------------------------------------------
        # 3. Transaction summary
        # --------------------------------------------------

        transaction_summary = TransactionReport()

        if investigation.transaction_summary:
            source = investigation.transaction_summary

            transaction_summary = TransactionReport(
                total_transactions=source.total_transactions,
                incoming_transactions=source.incoming_transactions,
                outgoing_transactions=source.outgoing_transactions,
                total_value_received=source.total_value_received,
                total_value_sent=source.total_value_sent,
                summary=source.summary,
            )

        # --------------------------------------------------
        # 4. Major fund flows
        # --------------------------------------------------

        major_fund_flows: List[FundFlowReport] = []

        for flow in investigation.fund_flows:

            explanation = getattr(
                flow,
                "explanation",
                None
            )

            if not explanation:
                explanation = ai_service.explain_fund_flow(
                    flow
                )

            major_fund_flows.append(
                FundFlowReport(
                    source_address=flow.source_address,
                    destination_address=flow.destination_address,
                    transaction_hash=flow.transaction_hash,
                    value=flow.value,
                    timestamp=flow.timestamp,
                    hop_number=flow.hop_number,
                    explanation=explanation,
                )
            )

        # --------------------------------------------------
        # 5. Wallet relationships
        # --------------------------------------------------

        wallet_relationships: List[
            WalletRelationshipReport
        ] = []

        for relationship in investigation.wallet_relationships:

            wallet_relationships.append(
                WalletRelationshipReport(
                    wallet_address=relationship.wallet_address,
                    relationship_type=(
                        relationship.relationship_type
                    ),
                    transaction_count=(
                        relationship.transaction_count
                    ),
                    total_value=relationship.total_value,
                    first_seen=relationship.first_seen,
                    last_seen=relationship.last_seen,
                    explanation=getattr(
                        relationship,
                        "explanation",
                        None,
                    ),
                )
            )

        # --------------------------------------------------
        # 6. Risk indicators
        # --------------------------------------------------

        risk_indicators: List[RiskIndicatorReport] = []

        for indicator in investigation.risk_indicators:

            explanation = getattr(
                indicator,
                "explanation",
                None
            )

            if not explanation:
                explanation = (
                    ai_service.explain_risk_indicator(
                        indicator
                    )
                )

            risk_indicators.append(
                RiskIndicatorReport(
                    indicator=indicator.indicator,
                    severity=indicator.severity,
                    description=indicator.description,
                    explanation=explanation,
                    evidence=indicator.evidence,
                )
            )

        # --------------------------------------------------
        # 7. Entity intelligence
        # --------------------------------------------------

        entity_intelligence: List[
            EntityIntelligenceReport
        ] = []

        for entity in investigation.entity_intelligence:

            entity_intelligence.append(
                EntityIntelligenceReport(
                    address=entity.address,
                    entity_name=entity.entity_name,
                    entity_type=entity.entity_type,
                    attribution=entity.attribution,
                    source=entity.source,
                    confidence=entity.confidence,
                    explanation=getattr(
                        entity,
                        "explanation",
                        None,
                    ),
                )
            )

        # --------------------------------------------------
        # 8. Investigation timeline
        # --------------------------------------------------

        timeline_data = ai_service.generate_timeline(
            investigation
        )

        investigation_timeline: List[TimelineReport] = []

        for event in timeline_data:

            investigation_timeline.append(
                TimelineReport(
                    timestamp=event.get("timestamp"),
                    block_number=event.get("block_number"),
                    transaction_hash=event.get(
                        "transaction_hash"
                    ),
                    event_type=event.get("event_type"),
                    description=event.get("description"),
                    evidence_reference=event.get(
                        "evidence_reference"
                    ),
                )
            )

        # --------------------------------------------------
        # 9. Evidence references
        # --------------------------------------------------

        evidence_references = (
            ai_service.generate_evidence_references(
                investigation
            )
        )

        # --------------------------------------------------
        # 10. Analytical interpretation
        # --------------------------------------------------

        analytical_interpretation = (
            "The analytical interpretation is based on the "
            "transaction, fund-flow, wallet relationship, "
            "risk-indicator, entity-intelligence, and timeline "
            "information supplied to TraceShield. The underlying "
            "evidence should be reviewed by the investigator "
            "before drawing further conclusions."
        )

        # --------------------------------------------------
        # 11. Report limitations
        # --------------------------------------------------

        limitations = [
            (
                "The report is based only on the analytical "
                "information supplied to TraceShield."
            ),
            (
                "A blockchain address does not by itself "
                "establish a real-world identity."
            ),
            (
                "Risk indicators are analytical observations "
                "and require investigator review."
            ),
            (
                "Entity attribution depends on the reliability "
                "of the referenced intelligence source."
            ),
            (
                "The report does not independently establish "
                "criminal activity, ownership, or intent."
            ),
        ]

        # --------------------------------------------------
        # 12. Final investigation report
        # --------------------------------------------------

        report = InvestigationReport(
            case_information=case_information,
            investigation_summary=investigation_summary,
            transaction_summary=transaction_summary,
            major_fund_flows=major_fund_flows,
            wallet_relationships=wallet_relationships,
            risk_indicators=risk_indicators,
            entity_intelligence=entity_intelligence,
            investigation_timeline=investigation_timeline,
            analytical_interpretation=(
                analytical_interpretation
            ),
            evidence_references=evidence_references,
            investigator_review_notes=None,
            limitations=limitations,
        )

        return report


# Shared ReportGenerator instance
report_generator = ReportGenerator()
