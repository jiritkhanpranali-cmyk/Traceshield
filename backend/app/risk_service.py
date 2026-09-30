from app.transaction_service import transaction_service


class RiskService:

    def analyze_wallet(self, wallet_address: str):
        transactions = transaction_service.get_wallet_transactions(
            wallet_address
        )

        if not transactions:
            return {
                "wallet": wallet_address,
                "risk_score": 0,
                "risk_level": "LOW",
                "indicators": [],
                "transaction_count": 0
            }

        indicators = []
        risk_score = 0

        # Indicator 1: multiple transactions
        if len(transactions) >= 2:
            indicators.append("Multiple transaction connections")
            risk_score += 20

        # Indicator 2: high-value transaction
        total_value = sum(
            tx["value_eth"] for tx in transactions
        )

        if total_value >= 2:
            indicators.append("High transaction value")
            risk_score += 30

        # Indicator 3: wallet acts as sender and receiver
        sent = any(
            tx["from"].lower() == wallet_address.lower()
            for tx in transactions
        )

        received = any(
            tx["to"].lower() == wallet_address.lower()
            for tx in transactions
        )

        if sent and received:
            indicators.append("Wallet acts as both sender and receiver")
            risk_score += 20

        if risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 25:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "wallet": wallet_address,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "indicators": indicators,
            "transaction_count": len(transactions),
            "total_value_eth": total_value
        }


risk_service = RiskService()