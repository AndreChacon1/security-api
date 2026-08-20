# Security API – x-api-key Anti-Pattern Demo

A minimal FastAPI backend that demonstrates the `x-api-key` authentication anti-pattern. The client must send a static API key in the `x-api-key` header for every protected request.

## Endpoints

| Method | Endpoint   | API Key Required | Description              |
| ------ | ---------- | ---------------- | ------------------------ |
| GET    | `/health`  | No               | Health/status response   |
| GET    | `/api/data`| Yes              | Returns static JSON data |
| POST   | `/api/data`| Yes              | Returns confirmation     |

## Setup

```bash
pip install fastapi "uvicorn[standard]"
uvicorn app:app --reload
```

The API runs at `http://127.0.0.1:8000`.

## API Key

The hardcoded API key is:

```
my-super-secret-api-key-12345
```

Pass it as the `x-api-key` HTTP header on protected endpoints.

## Testing with curl

```bash
# Health (no key required)
curl http://127.0.0.1:8000/health

# GET /api/data without key → 401
curl http://127.0.0.1:8000/api/data

# GET /api/data with wrong key → 401
curl -H "x-api-key: wrong-key" http://127.0.0.1:8000/api/data

# GET /api/data with correct key → 200
curl -H "x-api-key: my-super-secret-api-key-12345" http://127.0.0.1:8000/api/data

# POST /api/data without key → 401
curl -X POST http://127.0.0.1:8000/api/data

# POST /api/data with correct key → 200
curl -X POST -H "x-api-key: my-super-secret-api-key-12345" http://127.0.0.1:8000/api/data
```
