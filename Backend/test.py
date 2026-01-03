from app.blockchain.land_register import register_property_on_chain
from web3 import Web3

if __name__ == "__main__":
    tx = register_property_on_chain(
        kw_id="KW-TEST-001",
        data_hash=Web3.keccak(text="test property"),
        owner="0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
    )

    print("TX HASH:", tx)
