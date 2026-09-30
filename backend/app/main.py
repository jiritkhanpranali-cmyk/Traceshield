from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import json

from app.blockchain_service import blockchain_service
from app.transaction_service import transaction_service
from app.graph_service import graph_service
from app.risk_service import risk_service


app = FastAPI(
    title="TraceShield AI Backend",
    description="Blockchain Investigation & Analytics Platform — Smart India Hackathon 2026 (MHA)",
    version="1.0.0"
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class WalletValidateRequest(BaseModel):
    wallet_address: str
    network: Optional[str] = "Ethereum"
    trace_depth: Optional[int] = 2


# ---------------------------------------------------------
# Basic APIs
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "project": "TraceShield AI",
        "status": "running",
        "message": "Blockchain Investigation Platform",
        "version": "1.0.0",
        "hackathon": "Smart India Hackathon 2026 (SIH 2026)",
        "theme": "Ministry of Home Affairs (MHA) - Cybersecurity & Blockchain"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "TraceShield AI Backend"
    }


# ---------------------------------------------------------
# Blockchain Status
# ---------------------------------------------------------

@app.get("/blockchain/status")
def blockchain_status():
    return blockchain_service.get_status()


# ---------------------------------------------------------
# Existing Investigation API
# ---------------------------------------------------------

@app.post("/api/v1/investigation/validate")
def validate_wallet(payload: WalletValidateRequest):

    addr = payload.wallet_address.strip()

    if not addr.startswith("0x") or len(addr) != 42:
        raise HTTPException(
            status_code=400,
            detail="Invalid EVM wallet address format"
        )

    return {
        "valid": True,
        "wallet_address": addr,
        "network": payload.network,
        "trace_depth": payload.trace_depth,
        "status": "ready_for_ingestion"
    }


@app.get("/api/v1/investigation/graph/{wallet_address}")
def get_investigation_graph(wallet_address: str, depth: int = 2):

    return {
        "wallet": wallet_address,
        "depth": depth,
        "graph": graph_service.get_wallet_connections(wallet_address)
    }


# ---------------------------------------------------------
# Transaction APIs
# ---------------------------------------------------------

@app.get("/transactions")
def get_transactions():

    transactions = transaction_service.get_database_transactions()

    return {
        "mode": "mysql",
        "count": len(transactions),
        "transactions": transactions
    }


@app.get("/transactions/{tx_hash}")
def get_transaction(tx_hash: str):

    transaction = transaction_service.get_transaction(tx_hash)

    if transaction is None:
        return {
            "found": False,
            "transaction": None
        }

    return {
        "found": True,
        "transaction": transaction
    }


@app.get("/wallet/{wallet_address}/transactions")
def get_wallet_transactions(wallet_address: str):

    transactions = transaction_service.get_wallet_transactions(
        wallet_address
    )

    return {
        "wallet": wallet_address,
        "count": len(transactions),
        "transactions": transactions
    }


# ---------------------------------------------------------
# Graph APIs
# ---------------------------------------------------------

@app.get("/graph")
def get_graph():

    return graph_service.build_transaction_graph()


@app.get("/graph/wallet/{wallet_address}")
def get_wallet_graph(wallet_address: str):

    return graph_service.get_wallet_connections(wallet_address)


# ---------------------------------------------------------
# Risk Analysis API
# ---------------------------------------------------------

@app.get("/risk/{wallet_address}")
def get_wallet_risk(wallet_address: str):

    return risk_service.analyze_wallet(wallet_address)


# ---------------------------------------------------------
# WebSocket Live Events
# ---------------------------------------------------------

@app.websocket("/ws/live-events")
async def websocket_live_events(websocket: WebSocket):

    await websocket.accept()

    try:

        while True:

            await asyncio.sleep(12)

            event_payload = {
                "type": "block_mined",
                "block_number": 19602402,
                "timestamp": "2026-09-28T14:35:00Z"
            }

            await websocket.send_text(
                json.dumps(event_payload)
            )

    except WebSocketDisconnect:
        pass
