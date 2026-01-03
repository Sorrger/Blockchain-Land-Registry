from web3 import Web3
import json
from pathlib import Path
from app.core.config import settings

w3 = Web3(Web3.HTTPProvider(settings.CHAIN_RPC_URL))

if not w3.is_connected():
    raise RuntimeError("Cannot connect to blockchain RPC")

abi_path = Path(__file__).parent / "abi" / "LandRegister.json"
abi = json.loads(abi_path.read_text())["abi"]

land_register = w3.eth.contract(
    address=Web3.to_checksum_address(settings.CONTRACT_ADDRESS),
    abi=abi,
)
