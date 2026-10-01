def extract_wallet_features(transactions, wallet_address):

    wallet_address = wallet_address.lower()

    incoming_count = 0
    outgoing_count = 0

    unique_counterparties = set()
    assets = set()
    values = []

    for tx in transactions:

        from_address = tx.get("from_address")
        to_address = tx.get("to_address")

        if not from_address or not to_address:
            continue

        from_address = from_address.lower()
        to_address = to_address.lower()

        asset = tx.get("asset")

        if asset:
            assets.add(asset)

        try:
            value = float(tx.get("value") or 0)
        except (TypeError, ValueError):
            value = 0

        values.append(value)

        if to_address == wallet_address:
            incoming_count += 1
            unique_counterparties.add(from_address)

        elif from_address == wallet_address:
            outgoing_count += 1
            unique_counterparties.add(to_address)

    transaction_count = incoming_count + outgoing_count

    total_value = sum(values)

    average_transfer_value = 0

    if values:
        average_transfer_value = total_value / len(values)

    maximum_transfer_value = 0

    if values:
        maximum_transfer_value = max(values)

    return {
        "transaction_count": transaction_count,
        "incoming_transactions": incoming_count,
        "outgoing_transactions": outgoing_count,
        "unique_counterparties": len(unique_counterparties),
        "unique_assets": len(assets),
        "average_transfer_value": average_transfer_value,
        "maximum_transfer_value": maximum_transfer_value
    }
