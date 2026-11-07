export const messageBoardAbi = [
  'function getMessage() view returns (string)',
  'function setMessage(string newMessage)',
  'event MessageUpdated(address indexed editor, string newMessage)'
];
export const contractAddress = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS ?? '';
export const targetChainId = Number(process.env.NEXT_PUBLIC_CHAIN_ID ?? '11155111');
