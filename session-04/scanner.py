import os, time
from dotenv import load_dotenv
from web3 import Web3
load_dotenv()
RPC=os.getenv('SEPOLIA_RPC_URL',''); ADDRESS=os.getenv('CONTRACT_ADDRESS',''); START=int(os.getenv('START_BLOCK','0'))
EVENT_ABI=[{'anonymous':False,'type':'event','name':'MessageUpdated','inputs':[{'indexed':True,'name':'editor','type':'address'},{'indexed':False,'name':'newMessage','type':'string'}]}]
def main():
    if not RPC or not Web3.is_address(ADDRESS): raise SystemExit('Set SEPOLIA_RPC_URL and valid CONTRACT_ADDRESS')
    w3=Web3(Web3.HTTPProvider(RPC,request_kwargs={'timeout':20}))
    if not w3.is_connected() or w3.eth.chain_id!=11155111: raise SystemExit('RPC must connect to Sepolia')
    contract=w3.eth.contract(address=Web3.to_checksum_address(ADDRESS),abi=EVENT_ABI)
    latest=w3.eth.block_number; step=100
    for start in range(START,latest+1,step):
        end=min(start+step-1,latest)
        try:
            logs=contract.events.MessageUpdated().get_logs(from_block=start,to_block=end)
            for log in logs: print({'block':log['blockNumber'],'tx':log['transactionHash'].hex(),'editor':log['args']['editor'],'message':log['args']['newMessage']})
        except Exception as exc:
            print(f'Could not scan blocks {start}-{end}: {exc}')
            time.sleep(2)
if __name__=='__main__': main()
