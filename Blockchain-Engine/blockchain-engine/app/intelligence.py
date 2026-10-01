KNOWN_ENTITIES = {
    # Add verified public labels here later.
    # Example:
    # "0x...": {
    #     "name": "Example Exchange",
    #     "type": "exchange",
    #     "source": "verified intelligence source"
    # }
}


def get_entity_info(wallet_address):

    wallet_address = wallet_address.lower()

    entity = KNOWN_ENTITIES.get(wallet_address)

    if entity:
        return {
            "wallet": wallet_address,
            "identified": True,
            "name": entity["name"],
            "type": entity["type"],
            "source": entity["source"]
        }

    return {
        "wallet": wallet_address,
        "identified": False,
        "name": None,
        "type": "unknown",
        "source": None
    }