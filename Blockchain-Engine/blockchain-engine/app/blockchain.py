from web3 import Web3
from app.config import settings


class EthereumClient:

    def __init__(self):
        self.w3 = Web3(
            Web3.HTTPProvider(settings.ETH_RPC_URL)
        )

    def is_connected(self):
        return self.w3.is_connected()

    def get_chain_id(self):
        return self.w3.eth.chain_id

    def get_latest_block(self):
        return self.w3.eth.block_number

    def get_transaction(self, tx_hash):
        return self.w3.eth.get_transaction(tx_hash)

    def get_wallet_transfers(
        self,
        wallet_address,
        from_block=None,
        to_block=None
    ):

        if from_block is None:
            from_block = 0

        if to_block is None:
            to_block = self.get_latest_block()

        categories = [
            "external",
            "internal",
            "erc20",
            "erc721",
            "erc1155"
        ]

        def fetch_transfers(direction):

            all_transfers = []
            page_key = None

            while True:

                params = {
                    "fromBlock": hex(from_block),
                    "toBlock": hex(to_block),
                    "category": categories,
                    "withMetadata": True,
                    "maxCount": "0x3e8"
                }

                if direction == "outgoing":
                    params["fromAddress"] = wallet_address
                else:
                    params["toAddress"] = wallet_address

                if page_key:
                    params["pageKey"] = page_key

                response = self.w3.provider.make_request(
                    "alchemy_getAssetTransfers",
                    [params]
                )

                if not response:
                    break

                result = response.get("result") or {}

                transfers = result.get("transfers", [])

                all_transfers.extend(transfers)

                page_key = result.get("pageKey")

                if not page_key:
                    break

            return all_transfers

        outgoing = fetch_transfers("outgoing")
        incoming = fetch_transfers("incoming")

        return {
            "outgoing": outgoing,
            "incoming": incoming
        }
    def get_connected_wallets(
        self,
        wallet_address,
        from_block,
        to_block
    ):
        transfers = self.get_wallet_transfers(
        wallet_address,
        from_block=from_block,
        to_block=to_block
        )

        connected_wallets = set()

        for transfer in transfers.get("outgoing", []):

           address = transfer.get("to")

           if address:
                connected_wallets.add(
                address.lower()
             )

        for transfer in transfers.get("incoming", []):

            address = transfer.get("from")

            if address:
              connected_wallets.add(
                address.lower()
            )

        connected_wallets.discard(
            wallet_address.lower()
        )

        return list(connected_wallets)