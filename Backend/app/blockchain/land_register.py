from web3 import Web3
from app.blockchain.client import w3, land_register
from app.core.config import settings

def register_property_on_chain(
    kw_id: str,
    data_hash: bytes, 
    owner: str,
) -> str:
    """
    Registers the property on the smart contract.
    """
    nonce = w3.eth.get_transaction_count(settings.NOTARY_ADDRESS)

    # Convert arbitrary data (like '123') to 32 bytes required by Solidity bytes32
    if isinstance(data_hash, bytes) and len(data_hash) != 32:
        # If it's not exactly 32 bytes, we hash it to ensure it fits
        data_hash = Web3.keccak(data_hash)

    tx = land_register.functions.registerProperty(
        kw_id,
        data_hash,
        Web3.to_checksum_address(owner),
    ).build_transaction({
        "from": settings.NOTARY_ADDRESS,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("20", "gwei"),
    })

    signed_tx = w3.eth.account.sign_transaction(
        tx,
        private_key=settings.NOTARY_PRIVATE_KEY,
    )

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt.transactionHash.hex()

def transfer_property_on_chain(
    kw_id: str,
    new_owner_wallet: str,
) -> str:
    """
    Calls the transferProperty function on the smart contract.
    """
    nonce = w3.eth.get_transaction_count(settings.NOTARY_ADDRESS)

    tx = land_register.functions.transferProperty(
        kw_id,
        Web3.to_checksum_address(new_owner_wallet),
    ).build_transaction({
        "from": settings.NOTARY_ADDRESS,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("20", "gwei"),
    })

    signed_tx = w3.eth.account.sign_transaction(
        tx,
        private_key=settings.NOTARY_PRIVATE_KEY,
    )

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return receipt.transactionHash.hex()