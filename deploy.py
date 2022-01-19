import json
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
    my_address = "0xFCA99518cD183A9753494b8148fA5e82CFB600db"
    private_key = "0x39e5393edff2ac8fda5528f23b073c6cb7a63f10a0d44ecfb659bf9d24aa9da8"

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
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(signed_txn)


    simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    print(simple_storage.functions.retrieve().call())
    store_transaction = simple_storage.functions.store(15).buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
    )
    sign_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key)
    sign_store_txn_hash = w3.eth.send_raw_transaction(sign_store_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(sign_store_txn_hash)
    print(simple_storage.functions.retrieve().call())