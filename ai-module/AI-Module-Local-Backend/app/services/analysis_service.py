
"""
TraceShield Analysis Service.

This service performs descriptive analysis on blockchain
transaction data supplied to TraceShield.

Responsibilities:
- Analyze transaction activity.
- Build basic fund-flow records.
- Identify wallet counterparties.
- Generate analytical risk indicators from observable patterns.
- Preserve evidence references.

Important:
- No blockchain data is invented.
- No wallet ownership is inferred.
- No real-world identity is inferred.
- No criminal activity is concluded.
- Risk indicators are observations that require investigator review.
"""

from collections import Counter
from typing import Any, Dict, List


class AnalysisService:
    """Perform evidence-grounded analysis on supplied transactions."""

    def analyze_transactions(
        self,
        transactions: List[Dict[str, Any]],
        wallet_address: str,
    ) -> Dict[str, Any]:
        """
        Analyze transaction activity for a supplied wallet.
        """

        if not isinstance(transactions, list):
            raise ValueError(
                "Transactions must be provided as a list."
            )

        if not isinstance(wallet_address, str) or not wallet_address.strip():
            raise ValueError(
                "A wallet address is required."
            )

        wallet = wallet_address.strip().lower()

        incoming = []
        outgoing = []

        for transaction in transactions:
            source = transaction.get("source_address")
            destination = transaction.get("destination_address")

            if (
                isinstance(destination, str)
                and destination.strip().lower() == wallet
            ):
                incoming.append(transaction)

            if (
                isinstance(source, str)
                and source.strip().lower() == wallet
            ):
                outgoing.append(transaction)

        return {
            "wallet_address": wallet_address,
            "total_transactions": len(
                set(
                    transaction.get("transaction_hash")
                    for transaction in incoming + outgoing
                    if transaction.get("transaction_hash")
                )
            ),
            "incoming_transactions": incoming,
            "outgoing_transactions": outgoing,
        }

    def analyze_fund_flows(
        self,
        transactions: List[Dict[str, Any]],
        wallet_address: str,
    ) -> List[Dict[str, Any]]:
        """
        Convert supplied transactions into fund-flow records.
        """

        wallet = wallet_address.strip().lower()
        fund_flows: List[Dict[str, Any]] = []

        for transaction in transactions:
            source = transaction.get("source_address")
            destination = transaction.get("destination_address")

            if not isinstance(source, str):
                continue

            if not isinstance(destination, str):
                continue

            source_matches = source.strip().lower() == wallet
            destination_matches = destination.strip().lower() == wallet

            if not (source_matches or destination_matches):
                continue

            fund_flows.append(
                {
                    "source_address": source,
                    "destination_address": destination,
                    "transaction_hash": transaction.get(
                        "transaction_hash"
                    ),
                    "value": transaction.get("value"),
                    "timestamp": transaction.get("timestamp"),
                    "hop_number": 1,
                    "explanation": (
                        "Fund flow observed directly between the "
                        "investigated wallet and the supplied "
                        "counterparty."
                    ),
                }
            )

        return fund_flows

    def analyze_wallet_relationships(
        self,
        transactions: List[Dict[str, Any]],
        wallet_address: str,
    ) -> List[Dict[str, Any]]:
        """
        Build wallet-to-wallet relationship summaries.

        Relationships are based only on observed transaction
        counterparties in the supplied data.
        """

        wallet = wallet_address.strip().lower()

        relationship_data: Dict[str, Dict[str, Any]] = {}

        for transaction in transactions:
            source = transaction.get("source_address")
            destination = transaction.get("destination_address")

            if not isinstance(source, str):
                continue

            if not isinstance(destination, str):
                continue

            source_normalized = source.strip().lower()
            destination_normalized = destination.strip().lower()

            counterparty = None

            if source_normalized == wallet:
                counterparty = destination

            elif destination_normalized == wallet:
                counterparty = source

            if not counterparty:
                continue

            key = counterparty.strip().lower()

            if key not in relationship_data:
                relationship_data[key] = {
                    "wallet_address": counterparty,
                    "relationship_type": "transaction_counterparty",
                    "transaction_count": 0,
                    "total_value": 0.0,
                    "first_seen": transaction.get("timestamp"),
                    "last_seen": transaction.get("timestamp"),
                    "explanation": (
                        "Relationship derived from supplied "
                        "transaction activity."
                    ),
                }

            relationship = relationship_data[key]

            relationship["transaction_count"] += 1

            value = transaction.get("value")

            try:
                relationship["total_value"] += (
                    float(value)
                    if value is not None
                    else 0.0
                )
            except (TypeError, ValueError):
                pass

            timestamp = transaction.get("timestamp")

            if timestamp:
                first_seen = relationship.get("first_seen")
                last_seen = relationship.get("last_seen")

                if not first_seen or timestamp < first_seen:
                    relationship["first_seen"] = timestamp

                if not last_seen or timestamp > last_seen:
                    relationship["last_seen"] = timestamp

        return list(relationship_data.values())

    def generate_risk_indicators(
        self,
        transactions: List[Dict[str, Any]],
        wallet_address: str,
    ) -> List[Dict[str, Any]]:
        """
        Generate descriptive indicators from observable patterns.

        These indicators are not conclusions of criminal activity.
        """

        wallet = wallet_address.strip().lower()
        indicators: List[Dict[str, Any]] = []

        wallet_transactions = []

        for transaction in transactions:
            source = transaction.get("source_address")
            destination = transaction.get("destination_address")

            source_matches = (
                isinstance(source, str)
                and source.strip().lower() == wallet
            )

            destination_matches = (
                isinstance(destination, str)
                and destination.strip().lower() == wallet
            )

            if source_matches or destination_matches:
                wallet_transactions.append(transaction)

        if len(wallet_transactions) >= 100:
            hashes = [
                transaction.get("transaction_hash")
                for transaction in wallet_transactions
                if transaction.get("transaction_hash")
            ]

            indicators.append(
                {
                    "indicator": "High transaction volume",
                    "severity": "medium",
                    "description": (
                        "The supplied data contains a high number "
                        "of transactions involving the investigated wallet."
                    ),
                    "explanation": (
                        "This is a descriptive activity indicator. "
                        "Transaction volume alone does not establish "
                        "suspicious or criminal activity."
                    ),
                    "evidence": hashes[:20],
                }
            )

        counterparties = []

        for transaction in wallet_transactions:
            source = transaction.get("source_address")
            destination = transaction.get("destination_address")

            if (
                isinstance(source, str)
                and source.strip().lower() == wallet
                and isinstance(destination, str)
            ):
                counterparties.append(destination.strip().lower())

            elif (
                isinstance(destination, str)
                and destination.strip().lower() == wallet
                and isinstance(source, str)
            ):
                counterparties.append(source.strip().lower())

        counterparty_counts = Counter(counterparties)

        repeated_counterparties = [
            address
            for address, count in counterparty_counts.items()
            if count >= 10
        ]

        if repeated_counterparties:
            indicators.append(
                {
                    "indicator": "Repeated counterparty activity",
                    "severity": "low",
                    "description": (
                        "The supplied data shows repeated transactions "
                        "with one or more wallet counterparties."
                    ),
                    "explanation": (
                        "Repeated interaction is an observable "
                        "transaction pattern and requires contextual "
                        "investigator review."
                    ),
                    "evidence": [
                        transaction.get("transaction_hash")
                        for transaction in wallet_transactions
                        if transaction.get("transaction_hash")
                    ][:20],
                }
            )

        return indicators


analysis_service = AnalysisService()

