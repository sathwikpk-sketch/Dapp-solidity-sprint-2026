# Session 07 — Backend-controlled transaction

Name: Sathwik PK
Enrollment ID: Au24ug035

The FastAPI service signs `setMessage` transactions using a dedicated backend test wallet. `POST /send` requires an `X-API-Key` header, validates the Sepolia RPC, estimates gas with a 20% margin, signs, broadcasts, and waits for confirmation.

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
# Set all values, including a long random API_KEY
uvicorn main:app --reload
```

Example request: `POST /send` with JSON `{"message":"Hello from the API"}` and header `X-API-Key: <your API_KEY>`.

**Security limitation:** this is a local learning demo. A production service needs proper user authentication/authorization, request rate limits, nonce coordination for concurrent sends, key vault/HSM custody, audit logs, monitoring, and abuse controls. Never use a personal wallet or real funds.
