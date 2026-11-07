from eth_account import Account
acct=Account.create()
print('Address:',acct.address)
print('Private key (store securely; never share or commit):',acct.key.hex())
