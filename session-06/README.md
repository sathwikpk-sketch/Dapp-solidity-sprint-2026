# Session 06 — Wallet basics and signatures

Scripts cover account generation, mnemonic generation, message signing/recovery, and a raw EIP-1559 Sepolia transfer.

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
python 01_make_address.py
python 02_seed_phrase.py
python 03_sign_verify.py
# Only after setting a disposable funded Sepolia wallet and recipient:
python 04_raw_transaction.py
```

The account and mnemonic scripts print sensitive secrets. Run them privately, never capture/share the terminal output, and never use a wallet holding real funds. The raw transaction sends 0.001 test ETH and waits for its receipt.
