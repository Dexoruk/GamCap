from web3 import Web3
import pandas as pd
import time
from tqdm import tqdm

#I used this stack overflow submission for help: https://stackoverflow.com/questions/52222758/erc20-tokens-transferred-information-from-transaction-hash

w3 = Web3(Web3.HTTPProvider("https://eth.llamarpc.com"))

TRANSFER_EVENT_SIGNATURE = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

token_transfers = {}
address_received = {}
with tqdm(total=5001, desc="Fetching Blocks") as pbar:
    for block_number in range(17000000, 17005001):
        block = w3.eth.get_block(block_number, full_transactions=True)
        for tx in block.transactions:
            tx_receipt = w3.eth.get_transaction_receipt(tx["hash"])
            for log in tx_receipt["logs"]:
                if log["topics"][0] == TRANSFER_EVENT_SIGNATURE:
                    token_transfers[log["address"]] += 1
                    address_received[log["topics"][2]] += w3.toInt(log["data"])
    time.sleep(0.01)
    pbar.update(1)

token_transfers = {k: int(v) for k, v in token_transfers.items()}
address_received = {k: int(v) for k, v in address_received.items()}

df_token_transfers = pd.DataFrame(list(token_transfers.items()), columns=["Token", "Transfer Count"])
df_address_received = pd.DataFrame(list(address_received.items()), columns=["Address", "Tokens Received"])

df_token_transfers["Transfer Count"] = pd.to_numeric(df_token_transfers["Transfer Count"], errors="coerce")
df_address_received["Tokens Received"] = pd.to_numeric(df_address_received["Tokens Received"], errors="coerce")

# Task3.2
top_10_tokens = df_token_transfers.nlargest(10, "Transfer Count")
print(top_10_tokens)

# Task3.3
top_10_addresses = df_address_received.nlargest(10, "Tokens Received")
print(top_10_addresses)

# Task3.4
token_frequency_analysis = df_token_transfers.describe()
print(token_frequency_analysis)
