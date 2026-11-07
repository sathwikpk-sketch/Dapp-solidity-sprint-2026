import os
from eth_account import Account
from eth_account.messages import encode_defunct
from dotenv import load_dotenv
load_dotenv()
key=os.getenv('PRIVATE_KEY')
if not key: raise SystemExit('Set PRIVATE_KEY in .env (use a disposable test wallet)')
message='I am learning how Ethereum message signatures work.'
signed=Account.sign_message(encode_defunct(text=message),private_key=key)
recovered=Account.recover_message(encode_defunct(text=message),signature=signed.signature)
print('Message:',message); print('Signature:',signed.signature.hex()); print('Recovered signer:',recovered)
print('Matches key address:',recovered.lower()==Account.from_key(key).address.lower())
