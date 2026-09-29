
"""
TraceShield Blockchain Service.

Provides processing and normalization of blockchain transaction
data supplied to the TraceShield investigation pipeline.

This service does not:
- fetch or invent blockchain data
- determine wallet ownership
- identify real-world persons
- establish criminal activity
- store information in a database
"""

from typing import Any, Dict, List, Optional


class BlockchainService:
    """Process blockchain transaction data supplied to TraceShield."""

    REQUIRED_FIELDS = (
        "transaction_hash",
        "source_address",
        "destination_address",
    )

    def validate_transaction(
        self,
        transaction: Dict[str, Any],
    ) -> bool:
        """Validate the minimum required transaction structure."""

        if not isinstance(transaction, dict):
            return False

        for field in self.REQUIRED_FIELDS:
            value = transaction.get(field)

            if not isinstance(value, str) or not value.strip():
                return False

        return True

    def normalize_transaction(
        self,
        transaction: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Normalize a single supplied blockchain transaction."""

        if not self.validate_transaction(transaction):
            raise ValueError(
                "Invalid transaction. Required fields: "
                "transaction_hash, source_address, "
                "destination_address."
            )

        value = transaction.get("value")

        if value is not None:
            try:
                value = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "Transaction value must be numeric."
                ) from exc

        block_number = transaction.get("block_number")

        if block_number is not None:
            try:
                block_number = int(block_number)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    "Block number must be an integer."
                ) from exc

        return {
            "transaction_hash": transaction["transaction_hash"],
            "source_address": transaction["source_address"],
            "destination_address": transaction["destination_address"],
            "value": value,
            "timestamp": transaction.get("timestamp"),
            "block_number": block_number,
            "network": transaction.get("network"),
        }

    def normalize_transactions(
        self,
        transactions: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Normalize a collection of supplied transactions."""

        if not isinstance(transactions, list):
            raise ValueError(
                "Transactions must be provided as a list."
            )

        return [
            self.normalize_transaction(transaction)
            for transaction in transactions
        ]

    def filter_wallet_transactions(
        self,
        transactions: List[Dict[str, Any]],
        wallet_address: str,
    ) -> List[Dict[str, Any]]:
        """
        Return transactions where the supplied wallet appears
        as either the source or destination address.
        """

        if not isinstance(wallet_address, str):
            return []

        target_wallet = wallet_address.strip().lower()

        if not target_wallet:
            return []

        matching_transactions = []

        for transaction in transactions:
            source = transaction.get("source_address")
            destination = transaction.get("destination_address")

            source_matches = (
                isinstance(source, str)
                and source.strip().lower() == target_wallet
            )

            destination_matches = (
                isinstance(destination, str)
                and destination.strip().lower() == target_wallet
            )

            if source_matches or destination_matches:
                matching_transactions.append(transaction)

        return matching_transactions

    def calculate_transaction_summary(
        self,
        transactions: List[Dict[str, Any]],
        wallet_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Calculate descriptive transaction statistics.

        The calculation is based only on supplied transaction data.
        """

        if not isinstance(transactions, list):
            raise ValueError(
                "Transactions must be provided as a list."
            )

        relevant_transactions = transactions

        if wallet_address:
            relevant_transactions = self.filter_wallet_transactions(
                transactions,
                wallet_address,
            )

        total_transactions = len(relevant_transactions)

        incoming_transactions = 0
        outgoing_transactions = 0

        total_value_received = 0.0
        total_value_sent = 0.0

        target_wallet = (
            wallet_address.strip().lower()
            if wallet_address
            else None
        )

        for transaction in relevant_transactions:
            source = transaction.get("source_address")
            destination = transaction.get("destination_address")
            value = transaction.get("value")

            try:
                numeric_value = (
                    float(value)
                    if value is not None
                    else 0.0
                )
            except (TypeError, ValueError):
                numeric_value = 0.0

            if target_wallet:

                if (
                    isinstance(destination, str)
                    and destination.strip().lower() == target_wallet
                ):
                    incoming_transactions += 1
                    total_value_received += numeric_value

                if (
                    isinstance(source, str)
                    and source.strip().lower() == target_wallet
                ):
                    outgoing_transactions += 1
                    total_value_sent += numeric_value

        return {
            "total_transactions": total_transactions,
            "incoming_transactions": incoming_transactions,
            "outgoing_transactions": outgoing_transactions,
            "total_value_received": total_value_received,
            "total_value_sent": total_value_sent,
        }

    def get_transaction_hashes(
        self,
        transactions: List[Dict[str, Any]],
    ) -> List[str]:
        """Return unique transaction hashes in their original order."""

        hashes: List[str] = []

        for transaction in transactions:
            transaction_hash = transaction.get("transaction_hash")

            if (
                isinstance(transaction_hash, str)
                and transaction_hash.strip()
                and transaction_hash not in hashes
            ):
                hashes.append(transaction_hash)

        return hashes


blockchain_service = BlockchainService()

