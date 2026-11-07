import os
from dotenv import load_dotenv
from web3 import Web3
load_dotenv()
rpc=os.getenv('SEPOLIA_RPC_URL',''); key=os.getenv('PRIVATE_KEY',''); recipient=os.getenv('RECIPIENT_ADDRESS','')
if not rpc or not key or not Web3.is_address(recipient): raise SystemExit('Set SEPOLIA_RPC_URL, PRIVATE_KEY and valid RECIPIENT_ADDRESS')
w3=Web3(Web3.HTTPProvider(rpc,request_kwargs={'timeout':20}))
if not w3.is_connected() or w3.eth.chain_id!=11155111: raise SystemExit('RPC must connect to Sepolia')
account=w3.eth.account.from_key(key); recipient=Web3.to_checksum_address(recipient)
nonce=w3.eth.get_transaction_count(account.address,'pending'); latest=w3.eth.get_block('latest')
base_fee=latest.get('baseFeePerGas') or w3.eth.gas_price
priority=w3.to_wei(1,'gwei'); max_fee=base_fee*2+priority
transaction={'type':2,'chainId':11155111,'nonce':nonce,'to':recipient,'value':w3.to_wei('0.001','ether'),'data':b'','gas':21000,'maxFeePerGas':max_fee,'maxPriorityFeePerGas':priority}
signed=account.sign_transaction(transaction)
tx_hash=w3.eth.send_raw_transaction(signed.raw_transaction)
print('Broadcast transaction:',tx_hash.hex())
receipt=w3.eth.wait_for_transaction_receipt(tx_hash,timeout=180)
print('Receipt status:',receipt.status,'(1 means success)')
