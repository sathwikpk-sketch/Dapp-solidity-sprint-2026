# Session 10 — ETH/USD oracle

`PriceFeed.sol` stores an 8-decimal ETH/USD price and allows only the configured oracle address to update it. `PriceConsumer.sol` reads the feed and rejects stale values. `oracle.py` fetches CoinGecko and Coinbase spot prices, validates a broad sanity range, uses the median of available sources, and updates the feed when price changes by at least 0.1% or after a 60-second heartbeat.

Deploy `PriceFeed` with the oracle wallet address as constructor argument. Set that same wallet's private key in the backend `.env`, then run:

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
# Set RPC, oracle wallet key and deployed PriceFeed address
python oracle.py
```

The oracle wallet must be the address passed to `PriceFeed` or the contract will reject updates. `PriceConsumer` constructor needs the feed address and max age in seconds (for example `300`). The code is a learning demo, not a production-grade oracle: source APIs, price manipulation, key security, transaction retries and independent verification require more work.
