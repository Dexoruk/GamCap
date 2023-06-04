import pandas as pd
import json

with open("eth_blocks.json", "r") as f:
    blocks = json.load(f)

transactions = []
for block in blocks:
    for tx in block["transactions"]:
        transactions.append(tx)

df = pd.DataFrame(transactions)



# Task1.1
df["gasPrice"] = df["gasPrice"].apply(lambda x: int(x, 16))
print(df["gasPrice"].mean())

# Task1.2
df["value"] = df["value"].apply(lambda x: int(x, 16) / 10**18)
total_ether_transferred = df["value"].sum()
print(total_ether_transferred)
