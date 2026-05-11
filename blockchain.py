from web3 import Web3
from pathlib import Path
import json, time
from datetime import datetime

# Connect to the local Ethereum node
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

CONTRACT_ADDRESS = '0xb67AbaeC373722828930Da4FAfA1579672b821f4'

current_dir = Path.cwd()
file_loc = 'blockchain/build/contracts/FruitTrace.json'
abi = ''
with open(current_dir.joinpath(file_loc), 'r') as file:
    data = json.load(file)
    abi = data["abi"]
CONTRACT_ABI = abi
# Load the contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def add_fruit(name, location, supply_date, expiry_date, vendor, trace_info, fruit_id):
    try:
        # Convert dates to Unix timestamp (uint256)
        supply_date_timestamp = int(time.mktime(time.strptime(supply_date, '%Y-%m-%d')))
        expiry_date_timestamp = int(time.mktime(time.strptime(expiry_date, '%Y-%m-%d')))

        tx_hash = contract.functions.addFruit(
            name,                  # string
            location,              # string
            supply_date_timestamp, # uint256
            expiry_date_timestamp, # uint256
            vendor,                # string
            trace_info,             # string
            fruit_id
        ).transact({'from': web3.eth.accounts[0]})

        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        # print(f"Transaction successful: {tx_hash}")
        return receipt
    except Exception as e:
        print(f"Error during blockchain transaction: {e}")
        raise

def get_fruit(fruit_id):
    try:
        result = contract.functions.getFruit(fruit_id).call()
        # Convert Unix timestamps back to readable dates if needed
        supply_date = datetime.utcfromtimestamp(result[2]).strftime('%d-%m-%Y')
        expiry_date = datetime.utcfromtimestamp(result[3]).strftime('%d-%m-%Y')
        return (result[0], result[1], supply_date, expiry_date, result[4], result[5])
    except Exception as e:
        print(f"Error fetching fruit data from blockchain: {e}")
        raise
