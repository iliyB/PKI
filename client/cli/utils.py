from django.utils import timezone
import ast

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_OAEP


def edit_current_time():
    return timezone.localtime(timezone.now())


def encrypt(public_key, certificate: {}) -> bytes:

    byte = bytes(str(certificate), encoding='utf8')
    cipher = PKCS1_OAEP.new(public_key)

    return cipher.encrypt(byte)


def decrypt(private_key, byte: bytes) -> {}:

    cipher = PKCS1_OAEP.new(private_key)
    decrypt_byte = cipher.decrypt(byte)

    return ast.literal_eval(decrypt_byte.decode('utf-8'))


def create_signature(private_key, certificate: {}) -> bytes:

    hash = _get_hash_from_json(certificate)

    signature = PKCS1_v1_5.new(private_key)
    return signature.sign(hash)


def check_signature(public_key, certificate: {}, _signature: bytes) -> bool:

    hash = _get_hash_from_json(certificate)
    signature = PKCS1_v1_5.new(public_key)

    return signature.verify(hash, _signature)


def _get_hash_from_json(json: {}) -> bytes:
    byte = _get_bytes_from_json(json)
    return SHA.new(byte)


def _get_bytes_from_json(json: {}) -> bytes:
    string = ""
    for key, value in json.items():
        string += str(value)

    return bytes(string, encoding='utf-8')
