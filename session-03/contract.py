import os
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()
RPC_URL=os.getenv('SEPOLIA_RPC_URL','')
CONTRACT_ADDRESS=os.getenv('CONTRACT_ADDRESS','')
ABI=[{'type':'function','name':'getMessage','stateMutability':'view','inputs':[],'outputs':[{'type':'string','name':''}]}]

def get_web3():
    if not RPC_URL: raise RuntimeError('SEPOLIA_RPC_URL is not configured')
    w3=Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'timeout':15}))
    if not w3.is_connected(): raise RuntimeError('Could not connect to RPC provider')
    if w3.eth.chain_id != 11155111: raise RuntimeError('RPC is not connected to Sepolia')
    return w3

def get_contract(w3):
    if not Web3.is_address(CONTRACT_ADDRESS): raise RuntimeError('CONTRACT_ADDRESS is missing or invalid')
    return w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS),abi=ABI)
