# Session 04 — Smart contract events

Deploy `contracts/MessageBoard.sol` with an initial string. The contract emits `MessageUpdated` whenever a user changes the message. `scanner.py` scans historical logs in block ranges; `subscribe.py` listens through a WebSocket RPC endpoint.

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
# Fill HTTP RPC, WebSocket RPC, contract address and deployment block
python scanner.py
python subscribe.py
```

The WebSocket provider must support `eth_subscribe`. Historical scanning can be limited by provider log-range limits; reduce the range if your provider rejects requests.
