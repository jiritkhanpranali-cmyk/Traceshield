
"""
TraceShield API package.

This package contains the API routes used by the
TraceShield backend application.
"""

from app.api.investigation import router as investigation_router


__version__ = "1.0.0"

__all__ = [
    "investigation_router",
]


