from fastapi import APIRouter, HTTPException

from app.blockchain import EthereumClient

from app.analytics import (
    normalize_wallet_transfers,
    build_wallet_relationships,
    build_transaction_graph,
    trace_wallet_paths,
    trace_wallet_paths_recursive,
    analyze_fund_flow,
    calculate_risk_indicators
)

from app.intelligence import get_entity_info


router = APIRouter()

ethereum = EthereumClient()


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@router.get("/health")
def health_check():

    return {
        "status": "ok",
        "ethereum_connected": ethereum.is_connected(),
        "chain_id": ethereum.get_chain_id()
    }


# ---------------------------------------------------------
# COMPLETE WALLET ANALYSIS
# ---------------------------------------------------------

@router.get("/wallet/{wallet_address}")
def analyze_wallet(wallet_address: str):

    if not ethereum.w3.is_address(wallet_address):

        raise HTTPException(
            status_code=400,
            detail="Invalid Ethereum wallet address"
        )

    wallet_address = ethereum.w3.to_checksum_address(
        wallet_address
    )

    try:

        latest_block = ethereum.get_latest_block()

        from_block = max(
            0,
            latest_block - 1000
        )

        transfers = ethereum.get_wallet_transfers(
            wallet_address,
            from_block=from_block,
            to_block=latest_block
        )

        transactions = normalize_wallet_transfers(
            transfers
        )

        relationships = build_wallet_relationships(
            transactions,
            wallet_address
        )

        graph = build_transaction_graph(
            transactions
        )

        paths = trace_wallet_paths(
            transactions,
            wallet_address,
            max_hops=3
        )

        fund_flow = analyze_fund_flow(
            transactions
        )

        risk = calculate_risk_indicators(
            transactions,
            wallet_address
        )

        entity = get_entity_info(
            wallet_address
        )

        summary = {
            "transaction_count": len(transactions),
            "relationship_count": len(relationships),
            "graph_nodes": len(graph["nodes"]),
            "graph_edges": len(graph["edges"]),
            "multi_hop_path_count": len(paths),
            "incoming_value": fund_flow["incoming_value"],
            "outgoing_value": fund_flow["outgoing_value"],
            "unique_counterparties": risk["unique_counterparties"],
            "risk_indicator_count": len(risk["indicators"])
        }

        return {
            "summary": summary,
            "wallet": wallet_address,
            "transactions": transactions,
            "relationships": relationships,
            "graph": graph,
            "multi_hop_paths": paths,
            "fund_flow": fund_flow,
            "risk": risk,
            "entity": entity
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------------------------
# WALLET TRANSACTIONS
# ---------------------------------------------------------

@router.get("/wallet/{wallet_address}/transactions")
def wallet_transactions(wallet_address: str):

    if not ethereum.w3.is_address(wallet_address):

        raise HTTPException(
            status_code=400,
            detail="Invalid Ethereum wallet address"
        )

    wallet_address = ethereum.w3.to_checksum_address(
        wallet_address
    )

    try:

        latest_block = ethereum.get_latest_block()

        from_block = max(
            0,
            latest_block - 1000
        )

        transfers = ethereum.get_wallet_transfers(
            wallet_address,
            from_block=from_block,
            to_block=latest_block
        )

        transactions = normalize_wallet_transfers(
            transfers
        )

        return {
            "wallet": wallet_address,
            "transaction_count": len(transactions),
            "transactions": transactions
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------------------------
# WALLET GRAPH
# ---------------------------------------------------------

@router.get("/wallet/{wallet_address}/graph")
def wallet_graph(wallet_address: str):

    if not ethereum.w3.is_address(wallet_address):

        raise HTTPException(
            status_code=400,
            detail="Invalid Ethereum wallet address"
        )

    wallet_address = ethereum.w3.to_checksum_address(
        wallet_address
    )

    try:

        latest_block = ethereum.get_latest_block()

        from_block = max(
            0,
            latest_block - 1000
        )

        transfers = ethereum.get_wallet_transfers(
            wallet_address,
            from_block=from_block,
            to_block=latest_block
        )

        transactions = normalize_wallet_transfers(
            transfers
        )

        graph = build_transaction_graph(
            transactions
        )

        return {
            "wallet": wallet_address,
            "node_count": len(graph["nodes"]),
            "edge_count": len(graph["edges"]),
            "graph": graph
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------------------------
# WALLET RISK ANALYSIS
# ---------------------------------------------------------

@router.get("/wallet/{wallet_address}/risk")
def wallet_risk(wallet_address: str):

    if not ethereum.w3.is_address(wallet_address):

        raise HTTPException(
            status_code=400,
            detail="Invalid Ethereum wallet address"
        )

    wallet_address = ethereum.w3.to_checksum_address(
        wallet_address
    )

    try:

        latest_block = ethereum.get_latest_block()

        from_block = max(
            0,
            latest_block - 1000
        )

        transfers = ethereum.get_wallet_transfers(
            wallet_address,
            from_block=from_block,
            to_block=latest_block
        )

        transactions = normalize_wallet_transfers(
            transfers
        )

        risk = calculate_risk_indicators(
            transactions,
            wallet_address
        )

        return {
            "wallet": wallet_address,
            "risk": risk
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ---------------------------------------------------------
# WALLET FUND FLOW
# ---------------------------------------------------------

@router.get("/wallet/{wallet_address}/fund-flow")
def wallet_fund_flow(wallet_address: str):

    if not ethereum.w3.is_address(wallet_address):

        raise HTTPException(
            status_code=400,
            detail="Invalid Ethereum wallet address"
        )

    wallet_address = ethereum.w3.to_checksum_address(
        wallet_address
    )

    try:

        latest_block = ethereum.get_latest_block()

        from_block = max(
            0,
            latest_block - 1000
        )

        transfers = ethereum.get_wallet_transfers(
            wallet_address,
            from_block=from_block,
            to_block=latest_block
        )

        transactions = normalize_wallet_transfers(
            transfers
        )

        fund_flow = analyze_fund_flow(
            transactions
        )

        return {
            "wallet": wallet_address,
            "fund_flow": fund_flow
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
#   ---------------------------------------------------------
# MULTIPLE HOP WALLET PATHS
#   ---------------------------------------------------------

@router.get("/wallet/{wallet_address}/multi-hop")
def wallet_multi_hop(
    wallet_address: str,
    max_hops: int = 3,
    max_paths: int = 100
):

    if not ethereum.w3.is_address(wallet_address):
        raise HTTPException(
            status_code=400,
            detail="Invalid Ethereum wallet address"
        )

    if max_hops < 1 or max_hops > 5:
        raise HTTPException(
            status_code=400,
            detail="max_hops must be between 1 and 5"
        )

    if max_paths < 1 or max_paths > 500:
        raise HTTPException(
            status_code=400,
            detail="max_paths must be between 1 and 500"
        )

    wallet_address = ethereum.w3.to_checksum_address(
        wallet_address
    )

    try:

        latest_block = ethereum.get_latest_block()

        from_block = max(
            0,
            latest_block - 1000
        )

        paths = trace_wallet_paths_recursive(
            ethereum,
            wallet_address,
            from_block,
            latest_block,
            max_hops=max_hops,
            max_paths=max_paths
        )

        return {
            "wallet": wallet_address,
            "from_block": from_block,
            "to_block": latest_block,
            "max_hops": max_hops,
            "max_paths": max_paths,
            "path_count": len(paths),
            "paths": paths
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )