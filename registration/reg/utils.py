from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


def create_signature(private_key, certificate: {}) -> bytes:

    hash = _get_hash_from_json(certificate)

    signature = PKCS1_v1_5.new(private_key)
    signature = signature.sign(hash)

    return signature


def check_signature(public_key, certificate: {}, _signature: bytes) -> bool:

    hash = _get_hash_from_json(certificate)

    signature = PKCS1_v1_5.new(public_key)

    return signature.verify(hash, _signature)


def _get_hash_from_json(json: {}) -> bytes:
    string = ""
    for key, value in json.items():
        string += str(value)

    byte = bytes(string, encoding='utf-8')

    return SHA.new(byte)
