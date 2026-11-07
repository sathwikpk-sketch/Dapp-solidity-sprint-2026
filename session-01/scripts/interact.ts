import { signer, deployedContract } from './common.js';
const address = process.env.CONTRACT_ADDRESS;
if (!address) throw new Error('Set CONTRACT_ADDRESS in .env');
const wallet = await signer();
const contract = deployedContract(address, wallet);
console.log('Current value:', (await contract.retrieve()).toString());
const tx = await contract.store(42);
await tx.wait();
console.log('New value:', (await contract.retrieve()).toString());
