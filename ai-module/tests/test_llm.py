
"""
TraceShield LLM API Tests.

Tests:
- LLM configuration status endpoint.
- LLM request preparation endpoint.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_llm_status():
    """
    Test the LLM configuration status endpoint.
    """

    response = client.get("/llm/status")

    assert response.status_code == 200

    data = response.json()

    assert "configured" in data
    assert "model" in data
    assert "provider" in data


def test_llm_prepare():
    """
    Test preparation of an investigation for LLM processing.
    """

    payload = {
        "case_id": "TS-LLM-TEST-001",
        "wallet_address": "0xTESTLLMWALLET",
        "network": "Ethereum",
        "transaction_summary": {
            "total_transactions": 2,
            "incoming_transactions": 1,
            "outgoing_transactions": 1,
            "total_value_received": 1000.0,
            "total_value_sent": 500.0,
            "summary": "Synthetic test transaction summary."
        }
    }

    response = client.post(
        "/llm/prepare",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "prepared"
    assert "configured" in data
    assert "model" in data
    assert "system_prompt" in data
    assert "user_prompt" in data

    assert "0xTESTLLMWALLET" in data["user_prompt"]
    assert "Ethereum" in data["user_prompt"]
    assert "TS-LLM-TEST-001" in data["user_prompt"]

