"""
security-api/app.py
===================

A minimal FastAPI backend that demonstrates the x-api-key authentication
anti-pattern.  The client must send a static API key in the x-api-key
header for every protected request.

Run:
    pip install fastapi "uvicorn[standard]"
    uvicorn app:app --reload

Endpoints:
    GET  /health      – public, no key required
    GET  /api/data    – protected, requires x-api-key
    POST /api/data    – protected, requires x-api-key
"""

from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------------------------
# The "secret" API key — in a real system this would live in a secret
# manager, but here it is hardcoded for demonstration purposes.
# ---------------------------------------------------------------------------
API_KEY = "my-super-secret-api-key-12345"

app = FastAPI(
    title="Security API – x-api-key Anti-Pattern Demo",
    description="Demonstrates relying on a static API key sent via HTTP header.",
    version="1.0.0",
)

# Allow the frontend (any origin for local dev) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _verify_api_key(x_api_key: str | None) -> None:
    """Raise 401 if the provided key does not match."""
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing x-api-key header.",
        )


# ---------------------------------------------------------------------------
# Health – public
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Protected GET
# ---------------------------------------------------------------------------
@app.get("/api/data")
def get_data(x_api_key: str | None = Header(default=None)):
    _verify_api_key(x_api_key)
    return {
        "message": "Protected data",
        "course": "Security Exercise",
        "status": "success",
    }


# ---------------------------------------------------------------------------
# Protected POST
# ---------------------------------------------------------------------------
@app.post("/api/data")
def post_data(x_api_key: str | None = Header(default=None)):
    _verify_api_key(x_api_key)
    return {"message": "POST received"}
