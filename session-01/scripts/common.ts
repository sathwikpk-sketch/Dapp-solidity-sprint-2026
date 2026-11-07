import 'dotenv/config';
import { JsonRpcProvider, Wallet, Contract } from 'ethers';
import fs from 'node:fs';
import path from 'node:path';

export const source = fs.readFileSync(path.resolve('contracts/Storage.sol'), 'utf8');
export function config() {
  const rpc = process.env.SEPOLIA_RPC_URL;
  if (!rpc) throw new Error('Missing SEPOLIA_RPC_URL in .env');
  return new JsonRpcProvider(rpc);
}
export async function signer() {
  const key = process.env.DEPLOYER_PRIVATE_KEY;
  if (!key) throw new Error('Missing DEPLOYER_PRIVATE_KEY in .env');
  const provider = config();
  const network = await provider.getNetwork();
  if (network.chainId !== 11155111n) throw new Error(`Wrong network: expected Sepolia (11155111), got ${network.chainId}`);
  return new Wallet(key, provider);
}
export const abi = [
  'function store(uint256 number)',
  'function retrieve() view returns (uint256)',
  'event NumberStored(address indexed caller, uint256 value)'
];
export function deployedContract(address: string, runner: any) { return new Contract(address, abi, runner); }
