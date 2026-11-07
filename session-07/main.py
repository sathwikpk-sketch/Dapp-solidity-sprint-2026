import os, secrets
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from web3 import Web3
load_dotenv()
app=FastAPI(title='MessageBoard Transaction API')
ABI=[{'type':'function','name':'setMessage','stateMutability':'nonpayable','inputs':[{'name':'newMessage','type':'string'}],'outputs':[]}]
class MessageInput(BaseModel): message: str=Field(min_length=1,max_length=280)
def settings():
    rpc=os.getenv('SEPOLIA_RPC_URL',''); key=os.getenv('PRIVATE_KEY',''); address=os.getenv('CONTRACT_ADDRESS','')
    if not rpc or not key or not Web3.is_address(address): raise RuntimeError('Server configuration is incomplete')
    w3=Web3(Web3.HTTPProvider(rpc,request_kwargs={'timeout':20}))
    if not w3.is_connected() or w3.eth.chain_id!=11155111: raise RuntimeError('Server RPC must connect to Sepolia')
    account=w3.eth.account.from_key(key)
    return w3,account,Web3.to_checksum_address(address)
def auth(x_api_key):
    expected=os.getenv('API_KEY','')
    if not expected or not x_api_key or not secrets.compare_digest(expected,x_api_key): raise HTTPException(status_code=401,detail='Invalid API key')
@app.get('/status')
def status():
    try:
        w3,account,address=settings()
        return {'chain_id':w3.eth.chain_id,'block':w3.eth.block_number,'signer':account.address,'contract':address}
    except Exception as exc: raise HTTPException(status_code=503,detail=str(exc))
@app.post('/send')
def send_message(payload:MessageInput,x_api_key:str|None=Header(default=None)):
    auth(x_api_key)
    try:
        w3,account,address=settings(); contract=w3.eth.contract(address=address,abi=ABI)
        function=contract.functions.setMessage(payload.message)
        nonce=w3.eth.get_transaction_count(account.address,'pending')
        latest=w3.eth.get_block('latest'); base=latest.get('baseFeePerGas') or w3.eth.gas_price
        priority=w3.to_wei(1,'gwei'); max_fee=base*2+priority
        tx={'from':account.address,'nonce':nonce,'chainId':11155111,'type':2,'maxFeePerGas':max_fee,'maxPriorityFeePerGas':priority,'value':0}
        tx['gas']=function.estimate_gas({'from':account.address})*120//100
        tx=function.build_transaction(tx)
        signed=account.sign_transaction(tx); tx_hash=w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt=w3.eth.wait_for_transaction_receipt(tx_hash,timeout=120)
        if receipt.status!=1: raise RuntimeError('Transaction was mined but reverted')
        return {'transaction_hash':tx_hash.hex(),'block_number':receipt.blockNumber,'status':'confirmed'}
    except Exception as exc: raise HTTPException(status_code=502,detail=str(exc))
