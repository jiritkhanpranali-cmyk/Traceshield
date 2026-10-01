from fastapi import FastAPI

from app.api import router


app = FastAPI(
    title="TraceShield AI Blockchain Engine",
    description="Real-time blockchain analytics engine for TraceShield AI",
    version="1.0.0"
)


app.include_router(router)