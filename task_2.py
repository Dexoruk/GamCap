import pandas as pd
import json

with open("eth_blocks.json", "r") as f:
    blocks = json.load(f)

transactions = []
for block in blocks:
    for tx in block["transactions"]:
        transactions.append(tx)

df = pd.DataFrame(transactions)

# Task2.1
print(df.groupby("to")["value"].sum().nlargest(10))

# Task2.2
contract_df = df[df["to"].notnull()]
print(contract_df.groupby("to")["hash"].nunique().nlargest(5))

# Task2.3
df["blockNumber"] = df["blockNumber"].apply(lambda x: int(x, 16))
df["timestamp"] = pd.to_datetime(df["blockNumber"], unit="s")

hourly_data = df.set_index("timestamp").resample("H").agg({"gasPrice": "max", "hash": "count"})
hourly_data["gasPrice_zscore"] = (hourly_data["gasPrice"] - hourly_data["gasPrice"].mean()) / hourly_data["gasPrice"].std()
hourly_data["transaction_count_zscore"] = (hourly_data["hash"] - hourly_data["hash"].mean()) / hourly_data["hash"].std()

unusual_spikes = hourly_data[(hourly_data["gasPrice_zscore"] > 2) | (hourly_data["transaction_count_zscore"] > 2)]
print(unusual_spikes)
