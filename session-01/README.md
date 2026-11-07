# Session 01 — Deploy and interact with Storage

Name: Sathwik PK
Enrollment ID: Au24ug035

The contract stores one unsigned integer. The TypeScript script compiles the Solidity source, checks that the RPC is connected to Sepolia, deploys, reads the initial value, writes `25`, and reads again.

```powershell
Copy-Item .env.example .env
npm install
npm run check
npm run deploy
```

After deployment, copy the printed address into `CONTRACT_ADDRESS` in `.env`. Run `npm run interact` to write `42`. Fund only a test wallet. Never paste a private key into chat or commit `.env`.
