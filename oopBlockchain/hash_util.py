import hashlib
import json


def hash_string_256(str):
    return hashlib.sha256(str).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
