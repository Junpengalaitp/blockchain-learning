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
    my_address = "0xE25725Ab99FDBD69BCa7Af40C420b76ACcd9C78B"
    private_key = "0x495d7eb2ba46b1dd9a3ee52a5ec8929d475433043f0dd34fb442f40fdac62b0a"

    simple_storage = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.getTransactionCount(my_address)
    # print(nonce)

    transaction = simple_storage.constructor().buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce}
    )

    print(transaction)


