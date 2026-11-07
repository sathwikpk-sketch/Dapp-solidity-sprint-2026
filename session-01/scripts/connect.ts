import { signer } from './common.js';
const wallet = await signer();
console.log('Wallet:', wallet.address);
console.log('Balance (ETH):', (await wallet.provider!.getBalance(wallet.address)).toString());
