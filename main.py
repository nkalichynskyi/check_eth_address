import argparse

import httpx
from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider("https://rpc.sepolia.org/"))
etherscan_url = "https://api-sepolia.etherscan.io/api"


parser = argparse.ArgumentParser(description='Test assignment')
parser.add_argument('address', type=str, help='Eth address to check')
parser.add_argument('--api-key', type=str, help='Etherscan api key', required=False)


def _get_balance(address: str) -> int:
    return Web3.from_wei(w3.eth.get_balance(address), 'ether')


def _get_transactions_for_address(api_key: str, address: str, tx_type: str = "txlist"):
    params = {
        "module": "account",
        "action": tx_type,
        "startblock": 0,
        "address": address,
        "apikey": api_key
    }
    txs = []
    limit = 10000  # default limit
    page = 0

    while True:
        page += 1
        params["page"] = page
        res = httpx.get(etherscan_url, params=params)

        if res.status_code != 200:
            raise RuntimeError("Failed to get Tx list")

        if (res := res.json())["status"] == "0":
            raise RuntimeError("Failed to get Tx list")

        txs.extend(res["result"])
        if len(res["result"]) < limit:
            break

    return txs

def get_internal_tx(api_key: str, address: str) -> list[dict]:
    return _get_transactions_for_address(api_key, address, "txlistinternal")


if __name__ == '__main__':
    args = parser.parse_args()
    address = args.address

    if not Web3.is_address(address):
        raise ValueError("provided value is not a valid eth address")

    address = Web3.to_checksum_address(address)
    txs = None
    internal_txs = None

    if args.api_key:
        txs = _get_transactions_for_address(args.api_key, address)
        internal_txs = get_internal_tx(args.api_key, address)

    with open("output.csv", "w") as output:
        output.write("address, balance, # of txs, # of internal txs \n")
        txs_number = len(txs) if txs else "N/A"
        internal_txs_number = len(internal_txs) if internal_txs else "N/A"
        output.write(f"{address}, {_get_balance(address)}, {txs_number}, {internal_txs_number}")

    print("Done, check CSV file")
