
"""
TraceShield Investigation Service.

This module coordinates the complete investigation workflow.

Flow:

Supplied blockchain transactions
        ↓
Blockchain normalization
        ↓
Transaction analysis
        ↓
Fund-flow analysis
        ↓
Wallet relationship analysis
        ↓
Risk indicator analysis
        ↓
Investigation report

Important:
- The service uses only supplied transaction data.
- It does not fetch or invent blockchain information.
- It does not determine wallet ownership.
- It does not identify real-world persons.
- It does not establish criminal activity.
- It does not use a database.
"""

from typing import Any, Dict, List

from app.schemas.investigation_input import (
    EntityIntelligence,
    FundFlow,
    InvestigationInput,
    RiskIndicator,
    TransactionSummary,
    WalletRelationship,
)

from app.services.analysis_service import analysis_service
from app.services.blockchain_service import blockchain_service
from app.services.report_generator import report_generator


class InvestigationService:
    """Coordinate the complete TraceShield investigation workflow."""

    def prepare_investigation(
        self,
        case_id: str,
        wallet_address: str,
        network: str,
        transactions: List[Dict[str, Any]],
        entity_intelligence: List[Dict[str, Any]] | None = None,
    ) -> InvestigationInput:
        """
        Convert supplied blockchain transaction data into the
        InvestigationInput structure used by TraceShield.
        """

        if not case_id or not case_id.strip():
            raise ValueError("Case ID is required.")

        if not wallet_address or not wallet_address.strip():
            raise ValueError("Wallet address is required.")

        if not network or not network.strip():
            raise ValueError("Network is required.")

        normalized_transactions = (
            blockchain_service.normalize_transactions(
                transactions
            )
        )

        summary_data = (
            blockchain_service.calculate_transaction_summary(
                normalized_transactions,
                wallet_address,
            )
        )

        transaction_summary = TransactionSummary(
            total_transactions=summary_data[
                "total_transactions"
            ],
            incoming_transactions=summary_data[
                "incoming_transactions"
            ],
            outgoing_transactions=summary_data[
                "outgoing_transactions"
            ],
            total_value_received=summary_data[
                "total_value_received"
            ],
            total_value_sent=summary_data[
                "total_value_sent"
            ],
            summary=(
                "Transaction statistics calculated from "
                "the supplied blockchain transaction data."
            ),
        )

        fund_flow_data = analysis_service.analyze_fund_flows(
            normalized_transactions,
            wallet_address,
        )

        fund_flows = [
            FundFlow(**flow)
            for flow in fund_flow_data
        ]

        relationship_data = (
            analysis_service.analyze_wallet_relationships(
                normalized_transactions,
                wallet_address,
            )
        )

        wallet_relationships = [
            WalletRelationship(**relationship)
            for relationship in relationship_data
        ]

        risk_data = analysis_service.generate_risk_indicators(
            normalized_transactions,
            wallet_address,
        )

        risk_indicators = [
            RiskIndicator(**indicator)
            for indicator in risk_data
        ]

        entity_data = entity_intelligence or []

        entities = [
            EntityIntelligence(**entity)
            for entity in entity_data
        ]

        return InvestigationInput(
            case_id=case_id,
            wallet_address=wallet_address,
            network=network,
            transaction_summary=transaction_summary,
            fund_flows=fund_flows,
            wallet_relationships=wallet_relationships,
            risk_indicators=risk_indicators,
            entity_intelligence=entities,
        )

    def generate_investigation(
        self,
        case_id: str,
        wallet_address: str,
        network: str,
        transactions: List[Dict[str, Any]],
        entity_intelligence: List[Dict[str, Any]] | None = None,
    ) -> Dict[str, Any]:
        """
        Execute the complete TraceShield investigation workflow.

        Returns a structured investigation report as a dictionary.
        """

        investigation = self.prepare_investigation(
            case_id=case_id,
            wallet_address=wallet_address,
            network=network,
            transactions=transactions,
            entity_intelligence=entity_intelligence,
        )

        report = report_generator.generate_report(
            investigation
        )

        return report.model_dump()

    def analyze_supplied_transactions(
        self,
        transactions: List[Dict[str, Any]],
        wallet_address: str,
    ) -> Dict[str, Any]:
        """
        Return the analytical components without generating
        the final investigation report.
        """

        normalized_transactions = (
            blockchain_service.normalize_transactions(
                transactions
            )
        )

        transaction_analysis = (
            analysis_service.analyze_transactions(
                normalized_transactions,
                wallet_address,
            )
        )

        fund_flows = analysis_service.analyze_fund_flows(
            normalized_transactions,
            wallet_address,
        )

        relationships = (
            analysis_service.analyze_wallet_relationships(
                normalized_transactions,
                wallet_address,
            )
        )

        risk_indicators = (
            analysis_service.generate_risk_indicators(
                normalized_transactions,
                wallet_address,
            )
        )

        return {
            "transaction_analysis": transaction_analysis,
            "fund_flows": fund_flows,
            "wallet_relationships": relationships,
            "risk_indicators": risk_indicators,
        }


investigation_service = InvestigationService()

