import { config } from './common.js';
const provider = config();
const network = await provider.getNetwork();
console.log(`Connected. chainId=${network.chainId}`);
if (network.chainId !== 11155111n) throw new Error('This exercise expects Sepolia.');
console.log(`Latest block: ${await provider.getBlockNumber()}`);
