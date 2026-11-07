import os
import httpx
from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
load_dotenv()
app=FastAPI(title='IPFS Upload API')
@app.post('/upload')
async def upload(file: UploadFile=File(...)):
    token=os.getenv('PINATA_JWT')
    if not token: raise HTTPException(status_code=503,detail='PINATA_JWT is not configured')
    data=await file.read()
    if not data: raise HTTPException(status_code=400,detail='Uploaded file is empty')
    if len(data)>10*1024*1024: raise HTTPException(status_code=413,detail='Maximum file size is 10 MB')
    headers={'Authorization':f'Bearer {token}'}
    files={'file':(file.filename or 'upload.bin',data,file.content_type or 'application/octet-stream')}
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response=await client.post('https://api.pinata.cloud/pinning/pinFileToIPFS',headers=headers,files=files)
        response.raise_for_status(); payload=response.json()
        cid=payload.get('IpfsHash')
        if not cid: raise ValueError('Pinata response did not include IpfsHash')
        return {'cid':cid,'uri':f'ipfs://{cid}','gateway_url':f'https://gateway.pinata.cloud/ipfs/{cid}'}
    except (httpx.HTTPError,ValueError) as exc: raise HTTPException(status_code=502,detail=f'IPFS upload failed: {exc}')
