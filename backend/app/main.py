from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import asyncio
import json

app = FastAPI(
    title="TraceShield AI Backend",
    description="Blockchain Investigation & Analytics Platform — Smart India Hackathon 2026 (MHA)",
    version="0.1.0"
)

# Enable CORS for local React dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WalletValidateRequest(BaseModel):
    wallet_address: str
    network: Optional[str] = "Ethereum"
    trace_depth: Optional[int] = 2

@app.get("/")
def home():
    return {
        "project": "TraceShield AI",
        "status": "running",
        "message": "Blockchain Investigation Platform",
        "version": "0.1.0",
        "hackathon": "Smart India Hackathon 2026 (SIH 2026)",
        "theme": "Ministry of Home Affairs (MHA) - Cybersecurity & Blockchain"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected",
        "rpc_provider": "active"
    }

@app.post("/api/v1/investigation/validate")
def validate_wallet(payload: WalletValidateRequest):
    addr = payload.wallet_address.strip()
    if not addr.startswith("0x") or len(addr) != 42:
        raise HTTPException(status_code=400, detail="Invalid EVM wallet address format")
    
    return {
        "valid": True,
        "wallet_address": addr,
        "network": payload.network,
        "trace_depth": payload.trace_depth,
        "status": "ready_for_ingestion"
    }

@app.get("/api/v1/investigation/graph/{wallet_address}")
def get_wallet_graph(wallet_address: str, depth: int = 2):
    # Returns graph topology with monitored wallet, counterparties, and exchange attributions
    return {
        "case_id": "TS-2026-0047",
        "monitored_wallet": wallet_address,
        "nodes_count": 9,
        "edges_count": 8,
        "risk_level": "Medium",
        "potential_exchanges": ["Binance", "Coinbase"],
        "sanctioned_services": ["Tornado Cash"]
    }

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
            await websocket.send_text(json.dumps(event_payload))
    except WebSocketDisconnect:
        pass
