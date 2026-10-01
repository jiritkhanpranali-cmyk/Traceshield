
"""
TraceShield FastAPI Application.

This is the main entry point for the TraceShield backend.

It:
- Creates the FastAPI application.
- Registers the investigation API router.
- Registers the LLM API router.
- Provides basic health-check endpoints.
"""

from fastapi import FastAPI

from app.api.investigation import router as investigation_router
from app.api.llm import router as llm_router


app = FastAPI(
    title="TraceShield API",
    description=(
        "Investigation-support backend for blockchain "
        "transaction analysis and evidence-grounded reporting."
    ),
    version="1.0.0",
)


app.include_router(investigation_router)
app.include_router(llm_router)


@app.get("/")
def root():
    """
    Basic API information endpoint.
    """
    return {
        "application": "TraceShield",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    """
    Health-check endpoint used to verify that
    the backend is running correctly.
    """
    return {
        "status": "healthy",
        "service": "TraceShield Backend",
    }

