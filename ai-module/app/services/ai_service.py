from typing import Any, Dict, List

from app.schemas.investigation_input import InvestigationInput


class AIService:
    """
    TraceShield AI Intelligence Service.

    This service converts verified analytical outputs into
    investigator-friendly explanations.

    Important:
    - It does not fetch blockchain data.
    - It does not invent blockchain facts.
    - It does not determine wallet ownership.
    - It does not establish criminality.
    - It does not create unsupported evidence.
    """

    def generate_investigation_summary(
        self,
        investigation: InvestigationInput
    ) -> str:
        """
        Generate a factual investigation summary from
        verified analytical outputs.
        """

        wallet = investigation.wallet_address
        network = investigation.network

        transaction_summary = investigation.transaction_summary
        fund_flows = investigation.fund_flows
        relationships = investigation.wallet_relationships
        risk_indicators = investigation.risk_indicators
        entities = investigation.entity_intelligence

        parts: List[str] = []

        parts.append(
            f"The investigation concerns public wallet {wallet} "
            f"on the {network} network."
        )

        # Transaction information
        if transaction_summary:
            total = transaction_summary.total_transactions

            if total is not None:
                parts.append(
                    f"The supplied analytical data contains "
                    f"{total} transaction(s)."
                )

            if transaction_summary.incoming_transactions is not None:
                parts.append(
                    f"{transaction_summary.incoming_transactions} "
                    f"incoming transaction(s) were recorded in the "
                    f"provided analysis."
                )

            if transaction_summary.outgoing_transactions is not None:
                parts.append(
                    f"{transaction_summary.outgoing_transactions} "
                    f"outgoing transaction(s) were recorded in the "
                    f"provided analysis."
                )

        # Fund-flow information
        if fund_flows:
            parts.append(
                f"The analysis contains {len(fund_flows)} "
                f"fund-flow record(s)."
            )

            max_hop = max(
                (
                    flow.hop_number
                    for flow in fund_flows
                    if flow.hop_number is not None
                ),
                default=None
            )

            if max_hop is not None:
                parts.append(
                    f"The supplied fund-flow analysis reaches "
                    f"up to hop {max_hop}."
                )

        # Wallet relationships
        if relationships:
            parts.append(
                f"The graph analysis contains "
                f"{len(relationships)} wallet relationship(s)."
            )

        # Risk indicators
        if risk_indicators:
            parts.append(
                f"The risk-analysis layer identified "
                f"{len(risk_indicators)} investigation indicator(s)."
            )

            indicator_names = [
                indicator.indicator
                for indicator in risk_indicators
                if indicator.indicator
            ]

            if indicator_names:
                parts.append(
                    "The supplied indicators include: "
                    + ", ".join(indicator_names)
                    + "."
                )

        # Entity intelligence
        if entities:
            parts.append(
                f"The entity-intelligence layer contains "
                f"{len(entities)} record(s)."
            )

            entity_names = [
                entity.entity_name
                for entity in entities
                if entity.entity_name
            ]

            if entity_names:
                parts.append(
                    "Named entities in the supplied intelligence include: "
                    + ", ".join(entity_names)
                    + "."
                )

        # No analytical data
        if not any(
            [
                transaction_summary,
                fund_flows,
                relationships,
                risk_indicators,
                entities,
                investigation.timeline_events,
            ]
        ):
            parts.append(
                "No additional analytical results were supplied "
                "to the intelligence layer."
            )

        parts.append(
            "The observations in this summary are based only on "
            "the analytical data supplied to TraceShield AI. "
            "They do not independently establish wallet ownership, "
            "identity, criminal intent, or criminal attribution."
        )

        return " ".join(parts)

    def explain_risk_indicator(
        self,
        indicator: Any
    ) -> str:
        """
        Explain a risk indicator using only the information
        supplied by the risk-analysis layer.
        """

        explanation_parts: List[str] = []

        if indicator.indicator:
            explanation_parts.append(
                f"Investigation indicator: {indicator.indicator}."
            )

        if indicator.severity:
            explanation_parts.append(
                f"Severity supplied by the risk engine: "
                f"{indicator.severity}."
            )

        if indicator.description:
            explanation_parts.append(
                f"Description: {indicator.description}"
            )

        if indicator.evidence:
            explanation_parts.append(
                "Supporting evidence references: "
                + ", ".join(indicator.evidence)
                + "."
            )
        else:
            explanation_parts.append(
                "No evidence references were supplied "
                "for this indicator."
            )

        explanation_parts.append(
            "This indicator represents an analytical observation "
            "and does not by itself establish criminal activity."
        )

        return " ".join(explanation_parts)

    def explain_fund_flow(
        self,
        fund_flow: Any
    ) -> str:
        """
        Explain one verified fund-flow record.
        """

        parts: List[str] = []

        if fund_flow.source_address:
            parts.append(
                f"Source address: {fund_flow.source_address}."
            )

        if fund_flow.destination_address:
            parts.append(
                f"Destination address: {fund_flow.destination_address}."
            )

        if fund_flow.transaction_hash:
            parts.append(
                f"Transaction reference: {fund_flow.transaction_hash}."
            )

        if fund_flow.value is not None:
            parts.append(
                f"Reported value: {fund_flow.value}."
            )

        if fund_flow.timestamp:
            parts.append(
                f"Timestamp: {fund_flow.timestamp}."
            )

        if fund_flow.hop_number is not None:
            parts.append(
                f"Fund-flow hop: {fund_flow.hop_number}."
            )

        if not parts:
            return (
                "No sufficient fund-flow information was supplied "
                "for an explanation."
            )

        return " ".join(parts)

    def generate_timeline(
        self,
        investigation: InvestigationInput
    ) -> List[Dict[str, Any]]:
        """
        Convert verified timeline events into a structured
        investigator-friendly timeline.

        No new blockchain events are created here.
        """

        timeline: List[Dict[str, Any]] = []

        for event in investigation.timeline_events:
            timeline.append(
                {
                    "timestamp": event.timestamp,
                    "block_number": event.block_number,
                    "transaction_hash": event.transaction_hash,
                    "event_type": event.event_type,
                    "description": event.description,
                    "evidence_reference": event.evidence_reference,
                }
            )

        # Sort only when timestamps are available.
        timeline.sort(
            key=lambda event: (
                event["timestamp"] is None,
                event["timestamp"] or "",
            )
        )

        return timeline

    def generate_evidence_references(
        self,
        investigation: InvestigationInput
    ) -> List[str]:
        """
        Collect evidence references supplied by upstream
        analytical modules.
        """

        references: List[str] = []

        # Transaction hashes from fund flows
        for flow in investigation.fund_flows:
            if flow.transaction_hash:
                references.append(flow.transaction_hash)

        # Evidence references from risk indicators
        for indicator in investigation.risk_indicators:
            references.extend(indicator.evidence)

        # Evidence references from timeline
        for event in investigation.timeline_events:
            if event.evidence_reference:
                references.append(event.evidence_reference)

            if event.transaction_hash:
                references.append(event.transaction_hash)

        # Remove duplicates while preserving order
        unique_references = list(dict.fromkeys(references))

        return unique_references

    def build_ai_context(
        self,
        investigation: InvestigationInput
    ) -> Dict[str, Any]:
        """
        Prepare a structured context that can later be supplied
        to an external LLM.

        The context is derived only from verified input data.
        """

        return {
            "case_id": investigation.case_id,
            "wallet_address": investigation.wallet_address,
            "network": investigation.network,
            "transaction_summary": (
                investigation.transaction_summary.model_dump()
                if investigation.transaction_summary
                else None
            ),
            "fund_flows": [
                flow.model_dump()
                for flow in investigation.fund_flows
            ],
            "wallet_relationships": [
                relationship.model_dump()
                for relationship in investigation.wallet_relationships
            ],
            "risk_indicators": [
                indicator.model_dump()
                for indicator in investigation.risk_indicators
            ],
            "entity_intelligence": [
                entity.model_dump()
                for entity in investigation.entity_intelligence
            ],
            "timeline_events": [
                event.model_dump()
                for event in investigation.timeline_events
            ],
        }


# Shared service instance
ai_service = AIService()