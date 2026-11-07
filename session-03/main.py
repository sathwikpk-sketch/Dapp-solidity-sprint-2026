from fastapi import FastAPI, HTTPException
from web3 import Web3
from contract import get_web3, get_contract
app=FastAPI(title='Sepolia Read API',version='1.0.0')
@app.get('/status')
def status():
    try:
        w3=get_web3()
        return {'connected':True,'chain_id':w3.eth.chain_id,'latest_block':w3.eth.block_number}
    except Exception as exc: raise HTTPException(status_code=503,detail=str(exc))
@app.get('/message')
def message():
    try:
        w3=get_web3(); value=get_contract(w3).functions.getMessage().call()
        return {'message':value}
    except Exception as exc: raise HTTPException(status_code=503,detail=str(exc))
@app.get('/balance/{address}')
def balance(address:str):
    if not Web3.is_address(address): raise HTTPException(status_code=400,detail='Invalid Ethereum address')
    try:
        w3=get_web3(); wei=w3.eth.get_balance(Web3.to_checksum_address(address))
        return {'address':Web3.to_checksum_address(address),'balance_wei':str(wei),'balance_eth':str(Web3.from_wei(wei,'ether'))}
    except Exception as exc: raise HTTPException(status_code=503,detail=str(exc))
