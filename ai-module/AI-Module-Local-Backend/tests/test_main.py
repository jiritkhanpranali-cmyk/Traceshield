
"""
TraceShield Main Application Tests.

Tests:
- Root endpoint
- Health endpoint
- Investigation route availability
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "TraceShield"
    assert data["status"] == "running"
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    """Test the health-check endpoint."""

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "TraceShield Backend"


def test_investigation_endpoint_validation():
    """
    Verify that the investigation endpoint validates
    incoming request data.
    """

    response = client.post(
        "/investigation/generate",
        json={}
    )

    assert response.status_code == 422

