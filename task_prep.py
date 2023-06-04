import json
import requests
import time
from tqdm import tqdm

url = "https://eth.llamarpc.com"
headers = {"content-type": "application/json"}

def get_block(block_number):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "id": block_number,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response["result"]

blocks = []
with tqdm(total=5001, desc="Fetching Blocks") as pbar:
  for block_num in range(17000000, 17005001):
      block = get_block(block_num)
      blocks.append(block)
      time.sleep(0.01)
      pbar.update(1)

with open("eth_blocks.json", "w") as f:
    json.dump(blocks, f)
