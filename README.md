# Solidity Sprint 2026

This repository contains the code used across the Solidity Sprint sessions. Each session has its own folder, README, and `.env.example` file. The examples are meant for learning and local testing, not as production-ready applications.

## Sessions

| Session | What it covers |
| --- | --- |
| 01 | A simple storage contract with TypeScript deployment scripts |
| 02 | A MessageBoard contract and Next.js frontend using MetaMask |
| 03 | A read-only blockchain API built with FastAPI |
| 04 | Smart contract events, a historical event scanner, and a WebSocket listener |
| 05 | IPFS uploads and reads through the Pinata API |
| 06 | Wallet creation, mnemonic derivation, signing, verification, and raw transactions |
| 07 | A FastAPI service that prepares and sends transactions |
| 10 | Price feed contracts and a Python oracle that reads multiple sources |

Start with the README in the session you are working on. It includes the commands and configuration needed for that part of the project.

## Before you run anything

- Copy `.env.example` to `.env` and add only test credentials.
- Use Sepolia for network examples and fund a separate test wallet.
- Never commit `.env`, private keys, seed phrases, API keys, or personal data.
- Session 07 handles transaction signing through a backend service. It should not be used for real funds or exposed publicly without authentication, key handling, and other security controls.
- Session 05 requires your own Pinata JWT. Keep it in `.env`, not in frontend code.

## Checks

The Python files can be checked with `py_compile`. Running Solidity or TypeScript code requires installing the dependencies in the relevant session and setting up the RPC connection described in its README. No contracts are deployed as part of this repository itself, and live blockchain transactions should only be made with credentials you control.
