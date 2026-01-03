from app.blockchain.client import w3, land_register
from app.core.config import settings
from web3 import Web3

def register_property_on_chain(
    kw_id: str,
    data_hash: bytes,
    owner: str,
) -> str:
    nonce = w3.eth.get_transaction_count(settings.NOTARY_ADDRESS)

    tx = land_register.functions.registerProperty(
        kw_id,
        data_hash,
        Web3.to_checksum_address(owner),
    ).build_transaction({
        "from": settings.NOTARY_ADDRESS,
        "nonce": nonce,
        "gas": 300_000,
        "gasPrice": w3.to_wei("1", "gwei"),
    })

    signed_tx = w3.eth.account.sign_transaction(
        tx,
        private_key=settings.NOTARY_PRIVATE_KEY,
    )

    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt.transactionHash.hex()
