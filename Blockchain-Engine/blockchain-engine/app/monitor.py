import time

from app.blockchain import EthereumClient
from app.database import ( save_transactions,get_last_processed_block,
save_last_processed_block)
from app.analytics import normalize_transfer


class WalletMonitor:

    def __init__(self, wallet_address, interval=10):

        self.wallet_address = wallet_address.lower()
        self.interval = interval
        self.ethereum = EthereumClient()
        self.last_block = None

    def check_block(self, block_number):

        block = self.ethereum.w3.eth.get_block(
            block_number,
            full_transactions=True
        )

        detected_transactions = []

        for tx in block.transactions:

            from_address = tx["from"].lower()

            to_address = (
                tx["to"].lower()
                if tx["to"]
                else None
            )

            if (
                from_address == self.wallet_address
                or to_address == self.wallet_address
            ):

                direction = (
                    "outgoing"
                    if from_address == self.wallet_address
                    else "incoming"
                )

                transaction = {
                    "transaction_hash": tx["hash"].hex(),
                    "from_address": from_address,
                    "to_address": to_address,
                    "asset": "ETH",
                    "value": float(
                        self.ethereum.w3.from_wei(
                            tx["value"],
                            "ether"
                        )
                    ),
                    "block_number": str(block_number),
                    "timestamp": None,
                    "direction": direction
                }

                detected_transactions.append(transaction)

        return detected_transactions

    def check_wallet_transfers(self, from_block, to_block):

        categories = [
            "external",
            "internal",
            "erc20",
            "erc721",
            "erc1155"
        ]

        outgoing_params = {
            "fromBlock": hex(from_block),
            "toBlock": hex(to_block),
            "fromAddress": self.wallet_address,
            "category": categories,
            "withMetadata": True,
            "maxCount": "0x3e8"
        }

        outgoing_response = self.ethereum.w3.provider.make_request(
            "alchemy_getAssetTransfers",
            [outgoing_params]
        )

        outgoing_result = outgoing_response.get("result", {})

        outgoing = outgoing_result.get("transfers", [])

        incoming_params = {
            "fromBlock": hex(from_block),
            "toBlock": hex(to_block),
            "toAddress": self.wallet_address,
            "category": categories,
            "withMetadata": True,
            "maxCount": "0x3e8"
        }

        incoming_response = self.ethereum.w3.provider.make_request(
            "alchemy_getAssetTransfers",
            [incoming_params]
        )

        incoming_result = incoming_response.get("result", {})

        incoming = incoming_result.get("transfers", [])

        return {
            "outgoing": outgoing,
            "incoming": incoming
        }

    def start(self):

        print("🔴 Live wallet monitoring started")
        print("Wallet:", self.wallet_address)

        while True:

            try:

                latest_block = self.ethereum.get_latest_block()
                
                saved_block = get_last_processed_block(
                self.wallet_address
                )
                if saved_block is not None:

                    self.last_block = saved_block

                    print("Resuming from block:",self.last_block)
       
                else:

                    self.last_block = latest_block

                    save_last_processed_block(
                       self.wallet_address,
                       self.last_block
                 )

                    print("Starting from block:",self.last_block )

                if latest_block > self.last_block:

                    for block_number in range(
                        self.last_block + 1,
                        latest_block + 1
                    ):

                        # Check normal ETH transactions
                        eth_transactions = self.check_block(
                            block_number
                        )

                        if eth_transactions:

                            save_transactions(
                                eth_transactions
                            )

                            print(
                                f"🚨 ETH activity detected "
                                f"in block {block_number}"
                            )

                            for tx in eth_transactions:

                                print(
                                    "Transaction:",
                                    tx["transaction_hash"]
                                )

                                print(
                                    "Direction:",
                                    tx["direction"]
                                )

                                print(
                                    "Value:",
                                    tx["value"],
                                    "ETH"
                                )

                        # Check token and asset transfers
                        asset_transfers = self.check_wallet_transfers(
                            block_number,
                            block_number
                        )

                        outgoing = asset_transfers["outgoing"]
                        incoming = asset_transfers["incoming"]

                        normalized_assets = []

                        for transfer in outgoing:

                            normalized_assets.append(
                                normalize_transfer(
                                    transfer,
                                    "outgoing"
                                )
                            )

                        for transfer in incoming:

                            normalized_assets.append(
                                normalize_transfer(
                                    transfer,
                                    "incoming"
                                )
                            )

                        if normalized_assets:

                            save_transactions(
                                normalized_assets
                            )

                            print(
                                f"🚨 Asset activity detected "
                                f"in block {block_number}"
                            )

                            print(
                                "Outgoing assets:",
                                len(outgoing)
                            )

                            print(
                                "Incoming assets:",
                                len(incoming)
                            )

                            print(
                                "Saved to database:",
                                len(normalized_assets)
                            )

                        self.last_block = block_number
                        
                        save_last_processed_block(
                           self.wallet_address,
                           block_number
                        )
                    time.sleep(self.interval)

            except KeyboardInterrupt:

                print("\n🛑 Monitoring stopped")
                break

            except Exception as error:

                print(
                    "⚠️ Monitoring error:",
                    error
                )

                time.sleep(self.interval)