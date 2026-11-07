import solc from 'solc';
import { ContractFactory, Contract, type InterfaceAbi } from 'ethers';
import { source, signer } from './common.js';

type SolcError = {
  severity: string;
  formattedMessage: string;
};

type StorageArtifact = {
  abi: InterfaceAbi;
  evm: {
    bytecode: {
      object: string;
    };
  };
};

type SolcOutput = {
  errors?: SolcError[];
  contracts?: {
    'Storage.sol'?: {
      Storage?: StorageArtifact;
    };
  };
};

const input = {
  language: 'Solidity',
  sources: {
    'Storage.sol': {
      content: source
    }
  },
  settings: {
    optimizer: {
      enabled: true,
      runs: 200
    },
    outputSelection: {
      '*': {
        '*': ['abi', 'evm.bytecode.object']
      }
    }
  }
};

const output = JSON.parse(
  solc.compile(JSON.stringify(input))
) as SolcOutput;

const errors = (output.errors ?? []).filter(
  (error) => error.severity === 'error'
);

if (errors.length > 0) {
  throw new Error(
    errors.map((error) => error.formattedMessage).join('\n')
  );
}

const artifact = output.contracts?.['Storage.sol']?.Storage;

if (!artifact || !artifact.evm.bytecode.object) {
  throw new Error('Storage contract compilation failed.');
}

const wallet = await signer();

const factory = new ContractFactory(
  artifact.abi,
  `0x${artifact.evm.bytecode.object}`,
  wallet
);

const deployment = await factory.deploy();

console.log(
  'Deployment transaction:',
  deployment.deploymentTransaction()?.hash
);

await deployment.waitForDeployment();

const address = await deployment.getAddress();

console.log('Deployed Storage:', address);

const contract = new Contract(address, artifact.abi, wallet);

const retrieve = contract.getFunction('retrieve');
const store = contract.getFunction('store');

console.log(
  'Initial value:',
  (await retrieve()).toString()
);

const tx = await store(25);

console.log('Store transaction:', tx.hash);

await tx.wait();

console.log(
  'Updated value:',
  (await retrieve()).toString()
);

console.log(
  `Save this address in .env as CONTRACT_ADDRESS=${address}`
);