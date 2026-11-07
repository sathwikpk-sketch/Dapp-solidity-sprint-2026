# Session 02 — MetaMask + MessageBoard

The UI connects MetaMask, checks the configured chain ID, reads `getMessage()`, and calls `setMessage()` with a wallet signature. The ABI and function names match `contracts/MessageBoard.sol`.

Deploy the contract separately (Remix or Hardhat) with an initial message, then set its address:

```powershell
Copy-Item .env.example .env.local
# Edit .env.local and set NEXT_PUBLIC_CONTRACT_ADDRESS
npm install
npm run dev
```

Open `http://localhost:3000`, switch MetaMask to Sepolia, connect, and test a short message. The browser uses a public contract address only; never put a private key in a `NEXT_PUBLIC_` variable.
