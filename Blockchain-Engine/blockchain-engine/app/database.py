import sqlite3


DATABASE_NAME = "traceshield.db"


def get_connection():

    return sqlite3.connect(DATABASE_NAME)


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_hash TEXT,
            from_address TEXT,
            to_address TEXT,
            asset TEXT,
            value REAL,
            block_number TEXT,
            timestamp TEXT,
            direction TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_checkpoints (
            wallet_address TEXT PRIMARY KEY,
            last_block INTEGER
        )
    """)

    connection.commit()
    connection.close()


def save_transactions(transactions):

    connection = get_connection()
    cursor = connection.cursor()

    for tx in transactions:

        cursor.execute("""
            INSERT INTO transactions (
                transaction_hash,
                from_address,
                to_address,
                asset,
                value,
                block_number,
                timestamp,
                direction
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tx.get("transaction_hash"),
            tx.get("from_address"),
            tx.get("to_address"),
            tx.get("asset"),
            tx.get("value"),
            tx.get("block_number"),
            tx.get("timestamp"),
            tx.get("direction")
        ))

    connection.commit()
    connection.close()


def get_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            transaction_hash,
            from_address,
            to_address,
            asset,
            value,
            block_number,
            timestamp,
            direction
        FROM transactions
    """)

    rows = cursor.fetchall()

    connection.close()

    transactions = []

    for row in rows:

        transactions.append({
            "transaction_hash": row[0],
            "from_address": row[1],
            "to_address": row[2],
            "asset": row[3],
            "value": row[4],
            "block_number": row[5],
            "timestamp": row[6],
            "direction": row[7]
        })

    return transactions


def get_last_processed_block(wallet_address):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT last_block
        FROM monitoring_checkpoints
        WHERE wallet_address = ?
    """, (wallet_address.lower(),))

    row = cursor.fetchone()

    connection.close()

    if row:

        return row[0]

    return None


def save_last_processed_block(wallet_address, block_number):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO monitoring_checkpoints (
            wallet_address,
            last_block
        )
        VALUES (?, ?)
    """, (
        wallet_address.lower(),
        block_number
    ))

    connection.commit()
    connection.close()