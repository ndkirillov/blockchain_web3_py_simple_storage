from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()


with open ("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read();

#Compile solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources":{"SimpleStorage.sol":{"content": simple_storage_file}},
        "settings":{
            "outputSelection":{
                "*":{"*":["abi","metadata","evm.bytecode","evm.sourcemap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol, file)

#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["StorageContract"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["StorageContract"]["abi"]

#for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = os.getenv("PRIVATE_KEY")

#create contract in python 
SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)
#get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build Transaction 
# 2. Sign Transaction
# 3. Send Transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce}
)
signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

#working with the contract, always need: 1. Contract address 2. Contract ABI 
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

#Call -> Simulate making the call and getting a return value
#Transact -> Actually make a state change in blockchain

#initital value of var
print("Waiting for state of var...")
print(simple_storage.functions.viewStateVar().call())
print("Done!")

print("Storing new var in blockchain...")
store_transaction = simple_storage.functions.store(15).buildTransaction({
    "gasPrice": w3.eth.gas_price, "chainId": chain_id, "from": my_address, "nonce": nonce+1
})
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key = private_key)

hash_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
receipt_store_txn = w3.eth.waitForTransactionReceipt(hash_store_txn)
print("Done!")