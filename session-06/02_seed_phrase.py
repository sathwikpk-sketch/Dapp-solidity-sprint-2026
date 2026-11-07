from eth_account import Account
Account.enable_unaudited_hdwallet_features()
acct,mnemonic=Account.create_with_mnemonic()
print('Address:',acct.address)
print('Mnemonic (write it offline; never share):',mnemonic)
