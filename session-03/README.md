# Session 03 — Read-only blockchain API

Name: Sathwik PK
Enrollment ID: Au24ug035

FastAPI exposes `/status`, `/message`, and `/balance/{address}`. It validates the Sepolia chain and checks Ethereum address format. It does not sign or send transactions.

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit the RPC URL and deployed MessageBoard address
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the endpoints.
