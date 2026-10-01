from sklearn.ensemble import RandomForestClassifier


FEATURE_NAMES = [
    "transaction_count",
    "incoming_transactions",
    "outgoing_transactions",
    "unique_counterparties",
    "unique_assets",
    "average_incoming_value",
    "average_outgoing_value",
    "incoming_outgoing_ratio",
    "transfer_count"
]


def create_model():

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    return model