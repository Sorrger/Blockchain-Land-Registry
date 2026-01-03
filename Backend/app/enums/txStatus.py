from enum import Enum

class TxStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    failed = "failed"