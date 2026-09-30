import os
from dotenv import load_dotenv

load_dotenv()

BLOCKCHAIN_MODE = os.getenv("BLOCKCHAIN_MODE", "dummy")

ETH_RPC_URL = os.getenv("ETH_RPC_URL", "")
ETH_WS_URL = os.getenv("ETH_WS_URL", "")