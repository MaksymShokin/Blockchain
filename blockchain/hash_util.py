import hashlib
import json


def hash_string_256(str):
    return hashlib.sha256(str).hexdigest()


def hash_block(block):
    return hash_string_256(json.dumps(block, sort_keys=True).encode())
