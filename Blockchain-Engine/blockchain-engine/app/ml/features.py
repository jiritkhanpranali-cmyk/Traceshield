def extract_wallet_features(transactions, wallet_address):

    wallet_address = wallet_address.lower()

    incoming_count = 0
    outgoing_count = 0

    unique_counterparties = set()
    assets = set()

    incoming_values = []
    outgoing_values = []

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

        if to_address == wallet_address:

            incoming_count += 1

            unique_counterparties.add(
                from_address
            )

            incoming_values.append(value)

        elif from_address == wallet_address:

            outgoing_count += 1

            unique_counterparties.add(
                to_address
            )

            outgoing_values.append(value)

    transaction_count = (
        incoming_count + outgoing_count
    )

    total_value_transfers = (
        len(incoming_values) +
        len(outgoing_values)
    )

    average_incoming_value = 0

    if incoming_values:
        average_incoming_value = (
            sum(incoming_values)
            / len(incoming_values)
        )

    average_outgoing_value = 0

    if outgoing_values:
        average_outgoing_value = (
            sum(outgoing_values)
            / len(outgoing_values)
        )

    incoming_outgoing_ratio = 0

    if outgoing_count > 0:
        incoming_outgoing_ratio = (
            incoming_count / outgoing_count
        )

    return {

        "transaction_count":
            transaction_count,

        "incoming_transactions":
            incoming_count,

        "outgoing_transactions":
            outgoing_count,

        "unique_counterparties":
            len(unique_counterparties),

        "unique_assets":
            len(assets),

        "average_incoming_value":
            average_incoming_value,

        "average_outgoing_value":
            average_outgoing_value,

        "incoming_outgoing_ratio":
            incoming_outgoing_ratio,

        "transfer_count":
            total_value_transfers
    }