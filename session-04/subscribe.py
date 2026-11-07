import asyncio, os
from dotenv import load_dotenv
from web3 import AsyncWeb3, Web3, WebSocketProvider
load_dotenv()
WSS=os.getenv('SEPOLIA_WSS_URL',''); ADDRESS=os.getenv('CONTRACT_ADDRESS','')
ABI=[{'anonymous':False,'type':'event','name':'MessageUpdated','inputs':[{'indexed':True,'name':'editor','type':'address'},{'indexed':False,'name':'newMessage','type':'string'}]}]
async def main():
    if not WSS or not Web3.is_address(ADDRESS): raise SystemExit('Set SEPOLIA_WSS_URL and valid CONTRACT_ADDRESS')
    async with AsyncWeb3(WebSocketProvider(WSS)) as w3:
        if await w3.eth.chain_id != 11155111: raise SystemExit('WebSocket RPC must connect to Sepolia')
        address=Web3.to_checksum_address(ADDRESS)
        contract=w3.eth.contract(address=address,abi=ABI)
        topic=Web3.keccak(text='MessageUpdated(address,string)').hex()
        subscription_id=await w3.eth.subscribe('logs',{'address':address,'topics':[topic]})
        print('Listening for MessageUpdated events. Stop with Ctrl+C.')
        async for response in w3.socket.process_subscriptions():
            if response.get('subscription') != subscription_id: continue
            try:
                event=contract.events.MessageUpdated().process_log(response['result'])
                print({'editor':event['args']['editor'],'message':event['args']['newMessage'],'block':event['blockNumber']})
            except Exception as exc:
                print('Could not decode event:',exc)
if __name__=='__main__': asyncio.run(main())
