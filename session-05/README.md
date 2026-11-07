# Session 05 — IPFS file storage

Name: Sathwik PK
Enrollment ID: Au24ug035

This session adds a small FastAPI service that uploads a file to Pinata and returns its CID and `ipfs://` URI. The Pinata JWT stays on the backend; do not expose it to a browser or commit it.

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
# Add your Pinata JWT to .env
uvicorn main:app --reload
```

Open `/docs` and call `POST /upload` with a small test file. This is an independent implementation because the reference repository did not include working Session 05 source. Do not upload private documents unless you understand IPFS's public/distributed retrieval model; encryption must happen before upload for confidential data.
