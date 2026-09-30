
from typing import List, Dict

from app.database import get_database_connection


class TransactionService:

    def __init__(self):
        self.mode = "dummy"

        # Temporary development data.
        # These records are used only to seed the MySQL database.
        self.transactions = [
            {
                "tx_hash": "0xTX001",
                "from": "0xVICTIM001",
                "to": "0xSUSPECT001",
                "value_eth": 2.5,
                "timestamp": "2026-09-28T10:00:00Z",
                "block_number": 100001,
                "status": "confirmed"
            },
            {
                "tx_hash": "0xTX002",
                "from": "0xSUSPECT001",
                "to": "0xWALLET002",
                "value_eth": 1.8,
                "timestamp": "2026-09-28T10:05:00Z",
                "block_number": 100002,
                "status": "confirmed"
            },
            {
                "tx_hash": "0xTX003",
                "from": "0xWALLET002",
                "to": "0xWALLET003",
                "value_eth": 1.2,
                "timestamp": "2026-09-28T10:10:00Z",
                "block_number": 100003,
                "status": "confirmed"
            }
        ]

    def get_all_transactions(self) -> List[Dict]:
        return self.transactions

    def get_wallet_transactions(self, wallet_address: str) -> List[Dict]:
        wallet_address = wallet_address.lower()

        return [
            tx
            for tx in self.transactions
            if tx["from"].lower() == wallet_address
            or tx["to"].lower() == wallet_address
        ]

    def get_transaction(self, tx_hash: str):
        for tx in self.transactions:
            if tx["tx_hash"].lower() == tx_hash.lower():
                return tx

        return None

    def get_database_transactions(self) -> List[Dict]:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT
                    tx_hash,
                    sender,
                    receiver,
                    value_eth,
                    transaction_timestamp,
                    block_number
                FROM transactions
                ORDER BY block_number ASC
            """)

            rows = cursor.fetchall()

            transactions = []

            for row in rows:
                transactions.append({
                    "tx_hash": row["tx_hash"],
                    "from": row["sender"],
                    "to": row["receiver"],
                    "value_eth": float(row["value_eth"]),
                    "timestamp": row["transaction_timestamp"].isoformat() + "Z",
                    "block_number": row["block_number"],
                    "status": "confirmed"
                })

            return transactions

        finally:
            cursor.close()
            connection.close()

    def save_transactions_to_database(self):
        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            query = """
                INSERT INTO transactions
                (
                    tx_hash,
                    sender,
                    receiver,
                    value_eth,
                    transaction_timestamp,
                    block_number
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    sender = VALUES(sender),
                    receiver = VALUES(receiver),
                    value_eth = VALUES(value_eth),
                    transaction_timestamp = VALUES(transaction_timestamp),
                    block_number = VALUES(block_number)
            """

            for tx in self.transactions:
                timestamp = tx["timestamp"].replace("Z", "")

                cursor.execute(
                    query,
                    (
                        tx["tx_hash"],
                        tx["from"],
                        tx["to"],
                        tx["value_eth"],
                        timestamp,
                        tx["block_number"]
                    )
                )

            connection.commit()

            return {
                "status": "success",
                "saved_count": len(self.transactions)
            }

        finally:
            cursor.close()
            connection.close()


transaction_service = TransactionService()

