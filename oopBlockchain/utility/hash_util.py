import hashlib
import json
from collections import OrderedDict


def hash_string_256(str):
    return hashlib.sha256(str).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block["transactions"] = [
        tx.to_ordered_dict() for tx in hashable_block["transactions"]
    ]

    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
