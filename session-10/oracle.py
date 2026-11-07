import asyncio, os, statistics, time
import httpx
from dotenv import load_dotenv
from web3 import Web3
load_dotenv()
RPC=os.getenv('SEPOLIA_RPC_URL',''); KEY=os.getenv('PRIVATE_KEY',''); ADDRESS=os.getenv('CONTRACT_ADDRESS','')
ABI=[{'type':'function','name':'updatePrice','stateMutability':'nonpayable','inputs':[{'name':'nextPrice','type':'int256'}],'outputs':[]},{'type':'function','name':'latestPrice','stateMutability':'view','inputs':[],'outputs':[{'type':'uint80','name':'roundId'},{'type':'int256','name':'price'},{'type':'uint256','name':'updatedAt'}]}]
async def fetch_prices(client):
    urls=[('coingecko','https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'),('coinbase','https://api.coinbase.com/v2/prices/ETH-USD/spot')]
    values=[]
    for name,url in urls:
        try:
            r=await client.get(url); r.raise_for_status(); data=r.json()
            value=float(data['ethereum']['usd'] if name=='coingecko' else data['data']['amount'])
            if 100<=value<=10000: values.append(value)
        except Exception as exc: print(f'{name} source unavailable: {exc}')
    if not values: raise RuntimeError('No valid ETH/USD source returned a price')
    # Median reduces the effect of one outlier when two providers disagree.
    return statistics.median(values)
def send_price(w3,account,contract,price):
    scaled=int(round(price*1e8)); nonce=w3.eth.get_transaction_count(account.address,'pending')
    latest=w3.eth.get_block('latest'); base=latest.get('baseFeePerGas') or w3.eth.gas_price
    priority=w3.to_wei(1,'gwei'); fn=contract.functions.updatePrice(scaled)
    tx={'from':account.address,'nonce':nonce,'chainId':11155111,'type':2,'maxFeePerGas':base*2+priority,'maxPriorityFeePerGas':priority}
    tx['gas']=fn.estimate_gas({'from':account.address})*120//100
    signed=account.sign_transaction(fn.build_transaction(tx)); tx_hash=w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt=w3.eth.wait_for_transaction_receipt(tx_hash,timeout=120)
    if receipt.status!=1: raise RuntimeError('Price update transaction reverted')
    print(f'Updated ${price:.2f}; tx={tx_hash.hex()}')
async def main():
    if not RPC or not KEY or not Web3.is_address(ADDRESS): raise SystemExit('Configure RPC, PRIVATE_KEY and PriceFeed CONTRACT_ADDRESS')
    w3=Web3(Web3.HTTPProvider(RPC,request_kwargs={'timeout':20}))
    if not w3.is_connected() or w3.eth.chain_id!=11155111: raise SystemExit('RPC must connect to Sepolia')
    account=w3.eth.account.from_key(KEY); contract=w3.eth.contract(address=Web3.to_checksum_address(ADDRESS),abi=ABI)
    async with httpx.AsyncClient(timeout=15) as client:
        last_value=None; last_update=0
        while True:
            try:
                value=await fetch_prices(client)
                changed=last_value is None or abs(value-last_value)/last_value>=0.001
                heartbeat=time.time()-last_update>=60
                if changed or heartbeat:
                    await asyncio.to_thread(send_price,w3,account,contract,value)
                    last_value=value; last_update=time.time()
                else: print(f'No material change: ${value:.2f}')
            except Exception as exc: print('Oracle loop error:',exc)
            await asyncio.sleep(20)
if __name__=='__main__': asyncio.run(main())
