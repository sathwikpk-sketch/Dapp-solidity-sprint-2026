'use client';
import { useEffect, useState } from 'react';
import { BrowserProvider, Contract } from 'ethers';
import { contractAddress, messageBoardAbi, targetChainId } from '../lib/contract';

declare global { interface Window { ethereum?: any } }
export default function Home() {
  const [account,setAccount]=useState(''); const [chain,setChain]=useState('');
  const [message,setMessage]=useState(''); const [draft,setDraft]=useState('');
  const [status,setStatus]=useState('Not connected'); const [error,setError]=useState('');
  async function connect() {
    setError('');
    try {
      if(!window.ethereum) throw new Error('MetaMask was not found. Install or unlock MetaMask.');
      const provider=new BrowserProvider(window.ethereum);
      await provider.send('eth_requestAccounts',[]);
      const signer=await provider.getSigner(); const network=await provider.getNetwork();
      setAccount(await signer.getAddress()); setChain(network.chainId.toString());
      if(Number(network.chainId)!==targetChainId) { setStatus('Switch MetaMask to Sepolia.'); return; }
      if(!contractAddress) { setStatus('Wallet connected. Add the contract address to .env.local.'); return; }
      const contract=new Contract(contractAddress,messageBoardAbi,provider);
      const current=await contract.getMessage(); setMessage(current); setDraft(current); setStatus('Connected to Sepolia');
    } catch(e:any) { setError(e?.shortMessage||e?.message||'Connection failed'); }
  }
  async function save() {
    setError('');
    try {
      if(!window.ethereum) throw new Error('MetaMask not found');
      const provider=new BrowserProvider(window.ethereum); const signer=await provider.getSigner();
      const network=await provider.getNetwork();
      if(Number(network.chainId)!==targetChainId) throw new Error('Switch MetaMask to Sepolia first');
      if(!contractAddress) throw new Error('Set NEXT_PUBLIC_CONTRACT_ADDRESS in .env.local');
      const contract=new Contract(contractAddress,messageBoardAbi,signer);
      setStatus('Transaction pending…'); const tx=await contract.setMessage(draft); await tx.wait();
      setMessage(draft); setStatus('Transaction confirmed');
    } catch(e:any) { setStatus('Transaction failed'); setError(e?.shortMessage||e?.message||'Transaction failed'); }
  }
  useEffect(()=>{
    if(!window.ethereum) return;
    const onAccounts=(accounts:string[])=>setAccount(accounts[0]||'');
    const onChain=(id:string)=>{setChain(BigInt(id).toString());setStatus('Network changed — reconnect to refresh data');};
    window.ethereum.on?.('accountsChanged',onAccounts); window.ethereum.on?.('chainChanged',onChain);
    return ()=>{window.ethereum.removeListener?.('accountsChanged',onAccounts);window.ethereum.removeListener?.('chainChanged',onChain);};
  },[]);
  return <main><h1>MessageBoard</h1><p>Connect MetaMask on Sepolia to read and update the on-chain message.</p>
    <button onClick={connect}>Connect wallet</button><p className="muted">Account: {account||'—'}<br/>Chain ID: {chain||'—'}</p>
    <h3>Current on-chain message</h3><p>{message||'Connect your wallet to load the message.'}</p>
    <label htmlFor="draft">New message</label><textarea id="draft" value={draft} onChange={e=>setDraft(e.target.value)} />
    <button onClick={save} disabled={!account||!draft.trim()}>Update message</button><p>{status}</p>{error&&<p className="error">{error}</p>}
  </main>;
}
