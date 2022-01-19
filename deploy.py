import json
import solcx
from solcx import compile_standard
from web3 import Web3

with open('./SimpleStorage.sol') as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

# solcx.install_solc('0.6.0')

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        }
    },
    solc_version="0.6.0"
)

if __name__ == "__main__":
    # print(compiled_sol)
    with open("compiled_code.json", "w") as f:
        json.dump(compiled_sol, f)

    bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
    # print(bytecode)
    abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
    # print(abi)
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
    chain_id = 1337
    my_address = "0x3bcaDCB9068461aa6Cd941Cc8f4cCCF2f7CBc2b2"
    private_key = "0xdc96642c44187bc3afa72c7ade6d9b7619ee1a3ce7c615bbfac15c239dd3fd3f"

    # eth = w3.eth

    simple_storage = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(my_address)
    # print(nonce)

    # 1. Build an transaction
    # 2. Sign an transaction
    # 3. Send an transaction
    transaction = simple_storage.constructor().buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce}
    )
    
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # print(signed_txn)


    simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    print(simple_storage.functions.retrieve().call())
    store_transaction = simple_storage.functions.store(15).buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
    )
    sign_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key)
    sign_store_txn_hash = w3.eth.sendRawTransaction(sign_store_txn.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(sign_store_txn_hash)
    print(simple_storage.functions.retrieve().call())