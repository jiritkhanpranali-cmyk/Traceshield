from app.config import BLOCKCHAIN_MODE


class BlockchainService:
    def __init__(self):
        self.mode = BLOCKCHAIN_MODE

    def get_chain_id(self):
        if self.mode == "dummy":
            return 1

        raise NotImplementedError("Real blockchain connection is not configured yet.")

    def get_latest_block(self):
        if self.mode == "dummy":
            return 1000000

        raise NotImplementedError("Real blockchain connection is not configured yet.")

    def get_status(self):
        return {
            "mode": self.mode,
            "network": "Ethereum Mainnet",
            "connected": self.mode == "dummy",
            "chain_id": self.get_chain_id(),
            "latest_block": self.get_latest_block()
        }


blockchain_service = BlockchainService()