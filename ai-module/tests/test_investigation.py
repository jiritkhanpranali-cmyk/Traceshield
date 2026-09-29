
"""
TraceShield Investigation API Tests.

Tests the complete investigation-report generation flow.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_generate_investigation_report():
    """
    Test generation of a complete investigation report
    from valid investigation input.
    """

    payload = {
        "case_id": "TS-TEST-001",
        "wallet_address": "0xTESTWALLET123",
        "network": "Ethereum",

        "transaction_summary": {
            "total_transactions": 10,
            "incoming_transactions": 6,
            "outgoing_transactions": 4,
            "total_value_received": 5000.0,
            "total_value_sent": 3200.0,
            "summary": "Test transaction summary."
        },

        "fund_flows": [
            {
                "source_address": "0xSOURCE123",
                "destination_address": "0xTESTWALLET123",
                "transaction_hash": "0xTXHASH001",
                "value": 1000.0,
                "timestamp": "2026-09-28T10:00:00Z",
                "hop_number": 1
            }
        ],

        "wallet_relationships": [
            {
                "wallet_address": "0xRELATED123",
                "relationship_type": "transaction_counterparty",
                "transaction_count": 3,
                "total_value": 1500.0,
                "first_seen": "2026-09-01T10:00:00Z",
                "last_seen": "2026-09-28T10:00:00Z"
            }
        ],

        "risk_indicators": [
            {
                "indicator": "High transaction frequency",
                "severity": "medium",
                "description": "Test risk indicator.",
                "evidence": [
                    "0xTXHASH001"
                ]
            }
        ],

        "entity_intelligence": [
            {
                "address": "0xRELATED123",
                "entity_name": "Test Entity",
                "entity_type": "exchange",
                "attribution": "Test attribution",
                "source": "Test source",
                "confidence": "medium"
            }
        ],

        "timeline_events": [
            {
                "timestamp": "2026-09-28T10:00:00Z",
                "block_number": 123456,
                "transaction_hash": "0xTXHASH001",
                "event_type": "transfer",
                "description": "Test transfer event.",
                "evidence_reference": "0xTXHASH001"
            }
        ]
    }

    response = client.post(
        "/investigation/generate",
        json=payload
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    assert response.status_code == 200

    data = response.json()

    assert data["case_information"]["case_id"] == "TS-TEST-001"
    assert (
        data["case_information"]["network"]
        == "Ethereum"
    )
    assert (
        data["case_information"]["investigated_wallet"]
        == "0xTESTWALLET123"
    )

    assert data["transaction_summary"]["total_transactions"] == 10

    assert len(data["major_fund_flows"]) == 1
    assert (
        data["major_fund_flows"][0]["transaction_hash"]
        == "0xTXHASH001"
    )

    assert len(data["wallet_relationships"]) == 1

    assert len(data["risk_indicators"]) == 1
    assert (
        data["risk_indicators"][0]["indicator"]
        == "High transaction frequency"
    )

    assert len(data["entity_intelligence"]) == 1

    assert len(data["investigation_timeline"]) == 1

    assert "limitations" in data
    assert len(data["limitations"]) > 0

    assert "investigation_summary" in data
    assert len(data["investigation_summary"]) > 0

