from app.transaction_service import transaction_service


class GraphService:

    def build_transaction_graph(self):
        transactions = transaction_service.get_database_transactions()

        nodes = set()
        edges = []

        for tx in transactions:
            sender = tx["from"]
            receiver = tx["to"]

            nodes.add(sender)
            nodes.add(receiver)

            edges.append({
                "from": sender,
                "to": receiver,
                "tx_hash": tx["tx_hash"],
                "value_eth": tx["value_eth"],
                "timestamp": tx["timestamp"],
                "block_number": tx["block_number"]
            })

        return {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": list(nodes),
            "edges": edges
        }

    def get_wallet_connections(self, wallet_address: str):
        graph = self.build_transaction_graph()

        connections = []

        for edge in graph["edges"]:
            if (
                edge["from"].lower() == wallet_address.lower()
                or edge["to"].lower() == wallet_address.lower()
            ):
                connections.append(edge)

        return {
            "wallet": wallet_address,
            "connection_count": len(connections),
            "connections": connections
        }


graph_service = GraphService()
