from app.intelligence import get_entity_info
def normalize_transfer(transfer, direction):
    return {
        "transaction_hash": transfer.get("hash"),
        "from_address": transfer.get("from"),
        "to_address": transfer.get("to"),
        "asset": transfer.get("asset"),
        "value": transfer.get("value"),
        "block_number": transfer.get("blockNum"),
        "timestamp": transfer.get("metadata", {}).get("blockTimestamp"),
        "direction": direction
    }

def normalize_wallet_transfers(transfers):
    normalized = []

    for transfer in transfers.get("outgoing", []):
        normalized.append(
            normalize_transfer(transfer, "outgoing")
        )

    for transfer in transfers.get("incoming", []):
        normalized.append(
            normalize_transfer(transfer, "incoming")
        )

    return normalized


def build_wallet_relationships(transactions, wallet_address):
    relationships = []

    wallet_address = wallet_address.lower()

    for tx in transactions:
        from_address = tx.get("from_address")
        to_address = tx.get("to_address")

        if not from_address or not to_address:
            continue

        from_address = from_address.lower()
        to_address = to_address.lower()

        if from_address == wallet_address:
            relationships.append({
                "wallet": wallet_address,
                "connected_wallet": to_address,
                "direction": "outgoing",
                "transaction_hash": tx.get("transaction_hash"),
                "asset": tx.get("asset"),
                "value": tx.get("value"),
                "timestamp": tx.get("timestamp")
            })

        elif to_address == wallet_address:
            relationships.append({
                "wallet": wallet_address,
                "connected_wallet": from_address,
                "direction": "incoming",
                "transaction_hash": tx.get("transaction_hash"),
                "asset": tx.get("asset"),
                "value": tx.get("value"),
                "timestamp": tx.get("timestamp")
            })

    return relationships

def build_transaction_graph(transactions):
    nodes = set()
    edges = []

    for tx in transactions:
        from_address = tx.get("from_address")
        to_address = tx.get("to_address")

        if not from_address or not to_address:
            continue

        from_address = from_address.lower()
        to_address = to_address.lower()

        nodes.add(from_address)
        nodes.add(to_address)

        edges.append({
            "from": from_address,
            "to": to_address,
            "transaction_hash": tx.get("transaction_hash"),
            "asset": tx.get("asset"),
            "value": tx.get("value"),
            "timestamp": tx.get("timestamp")
        })

    return {
        "nodes": list(nodes),
        "edges": edges
    }
def trace_wallet_paths(transactions, start_wallet, max_hops=3):

    start_wallet = start_wallet.lower()

    graph = {}

    for tx in transactions:
        from_address = tx.get("from_address")
        to_address = tx.get("to_address")

        if not from_address or not to_address:
            continue

        from_address = from_address.lower()
        to_address = to_address.lower()

        if from_address not in graph:
            graph[from_address] = []

        graph[from_address].append(to_address)

    paths = []

    def explore(current_wallet, path, hops):

        if hops >= max_hops:
            return

        for next_wallet in graph.get(current_wallet, []):

            if next_wallet in path:
                continue

            new_path = path + [next_wallet]

            paths.append({
                "path": new_path,
                "hops": hops + 1
            })

            explore(
                next_wallet,
                new_path,
                hops + 1
            )

    explore(start_wallet, [start_wallet], 0)

    return paths
def analyze_fund_flow(transactions):

    incoming_value = 0
    outgoing_value = 0

    incoming_count = 0
    outgoing_count = 0

    for tx in transactions:

        value = tx.get("value")

        if value is None:
            continue

        try:
            value = float(value)
        except (TypeError, ValueError):
            continue

        direction = tx.get("direction")

        if direction == "incoming":
            incoming_value += value
            incoming_count += 1

        elif direction == "outgoing":
            outgoing_value += value
            outgoing_count += 1

    return {
        "incoming_value": incoming_value,
        "outgoing_value": outgoing_value,
        "total_value": incoming_value + outgoing_value,
        "incoming_transactions": incoming_count,
        "outgoing_transactions": outgoing_count
    }
def calculate_risk_indicators(transactions, wallet_address):

    wallet_address = wallet_address.lower()

    incoming_count = 0
    outgoing_count = 0
    unique_counterparties = set()

    for tx in transactions:

        from_address = tx.get("from_address")
        to_address = tx.get("to_address")

        if not from_address or not to_address:
            continue

        from_address = from_address.lower()
        to_address = to_address.lower()

        if to_address == wallet_address:
            incoming_count += 1
            unique_counterparties.add(from_address)

        elif from_address == wallet_address:
            outgoing_count += 1
            unique_counterparties.add(to_address)

    indicators = []

    if incoming_count > 10:
        indicators.append({
            "indicator": "High incoming transaction activity",
            "severity": "medium",
            "reason": f"{incoming_count} incoming transactions detected"
        })

    if outgoing_count > 10:
        indicators.append({
            "indicator": "High outgoing transaction activity",
            "severity": "medium",
            "reason": f"{outgoing_count} outgoing transactions detected"
        })

    if len(unique_counterparties) > 10:
        indicators.append({
            "indicator": "Large number of connected wallets",
            "severity": "medium",
            "reason": f"{len(unique_counterparties)} unique counterparties detected"
        })

    return {
        "wallet": wallet_address,
        "incoming_transactions": incoming_count,
        "outgoing_transactions": outgoing_count,
        "unique_counterparties": len(unique_counterparties),
        "indicators": indicators
    }
def trace_wallet_paths_recursive(
    ethereum_client,
    start_wallet,
    from_block,
    to_block,
    max_hops=3,
    max_paths=100
):

    start_wallet = start_wallet.lower()

    paths = []
    visited = {start_wallet}

    def explore(current_wallet, path, hops, hop_details):

        if hops >= max_hops:
            return

        if len(paths) >= max_paths:
            return

        connected_wallets = ethereum_client.get_connected_wallets(
            current_wallet,
            from_block,
            to_block
        )

        for next_wallet in connected_wallets:

            if len(paths) >= max_paths:
                return

            next_wallet = next_wallet.lower()

            if next_wallet in visited:
                continue

            transaction = find_wallet_connection(
                ethereum_client,
                current_wallet,
                next_wallet,
                from_block,
                to_block
            )

            current_entity = get_entity_info(
                current_wallet
            )

            next_entity = get_entity_info(
                next_wallet
            )

            # Analyze transaction
            indicators = analyze_transaction_indicators(
                transaction
            )

            new_path = path + [next_wallet]

            new_hop = {
                "hop": hops + 1,

                "from_wallet": current_wallet,
                "from_entity": current_entity,

                "to_wallet": next_wallet,
                "to_entity": next_entity,

                "transaction": transaction,

                "indicators": indicators
            }

            new_hop_details = hop_details + [
                new_hop
            ]

            path_data = {
                "path": new_path,
                "hops": hops + 1,
                "path_length": len(new_path),
                "hop_details": new_hop_details
            }

            paths.append(path_data)

            visited.add(next_wallet)

            explore(
                next_wallet,
                new_path,
                hops + 1,
                new_hop_details
            )

            visited.remove(next_wallet)

    explore(
        start_wallet,
        [start_wallet],
        0,
        []
    )

    return paths[:max_paths]

def find_wallet_connection(
    ethereum_client,
    from_wallet,
    to_wallet,
    from_block,
    to_block
):

    from_wallet = from_wallet.lower()
    to_wallet = to_wallet.lower()

    transfers = ethereum_client.get_wallet_transfers(
        from_wallet,
        from_block=from_block,
        to_block=to_block
    )

    # Check outgoing transfers:
    # current wallet -> connected wallet
    for transfer in transfers.get("outgoing", []):

        transfer_to = transfer.get("to")

        if not transfer_to:
            continue

        if transfer_to.lower() == to_wallet:

            return {
                "transaction_hash": transfer.get("hash"),
                "from_address": transfer.get("from"),
                "to_address": transfer.get("to"),
                "asset": transfer.get("asset"),
                "value": transfer.get("value"),
                "block_number": transfer.get("blockNum"),
                "timestamp": transfer.get(
                    "metadata", {}
                ).get("blockTimestamp"),
                "direction": "outgoing"
            }

    # Check incoming transfers:
    # connected wallet -> current wallet
    for transfer in transfers.get("incoming", []):

        transfer_from = transfer.get("from")

        if not transfer_from:
            continue

        if transfer_from.lower() == to_wallet:

            return {
                "transaction_hash": transfer.get("hash"),
                "from_address": transfer.get("from"),
                "to_address": transfer.get("to"),
                "asset": transfer.get("asset"),
                "value": transfer.get("value"),
                "block_number": transfer.get("blockNum"),
                "timestamp": transfer.get(
                    "metadata", {}
                ).get("blockTimestamp"),
                "direction": "incoming"
            }

    return None
def analyze_transaction_indicators(transaction):

    if not transaction:
        return []

    indicators = []

    value = transaction.get("value")
    asset = transaction.get("asset")

    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0

    # Simple investigation threshold.
    # This is an indicator, not proof of suspicious activity.
    if asset == "ETH" and value >= 10:
        indicators.append({
            "indicator": "High-value ETH transfer",
            "severity": "medium",
            "reason": f"{value} ETH transferred"
        })

    elif asset != "ETH" and value >= 10000:
        indicators.append({
            "indicator": "Large token transfer",
            "severity": "medium",
            "reason": f"{value} {asset} transferred"
        })

    return indicators