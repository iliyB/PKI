from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5


def encrypt_file(filename: str, private_key, public_key):

    with open(filename, 'rb') as source_file:
        source_byte = source_file.read()

        hash = SHA.new(source_byte)

        signature = PKCS1_v1_5.new(private_key)
        signature = signature.sign(hash)
        cipherrsa = PKCS1_OAEP.new(public_key)
        sig = cipherrsa.encrypt(signature[:128])
        sig = sig + cipherrsa.encrypt(signature[128:])

        cipher = PKCS1_OAEP.new(public_key)

        sessionkey = Random.new().read(32)
        iv = Random.new().read(16)

        obj = AES.new(sessionkey, AES.MODE_CFB, iv)
        ciphertext = iv + obj.encrypt(source_byte)

        sessionkey = cipher.encrypt(sessionkey)

        return sig + sessionkey + ciphertext

def decrypt_file(filename: str, private_key, public_key):

    with open(filename, 'rb') as source_file:
        source_byte = source_file.read()

        signature = source_byte[:512]
        sessionkey = source_byte[512:512+256]
        iv = source_byte[512+256:512+256+16]
        obj = source_byte[512+256+16:100000000000000000000]

        cipherrsa = PKCS1_OAEP.new(private_key)

        sessionkey = cipherrsa.decrypt(sessionkey)


        obj_ = AES.new(sessionkey, AES.MODE_CFB, iv)
        plaintext = obj_.decrypt(iv + obj)
        plaintext = plaintext[16:]

        cipherrsa = PKCS1_OAEP.new(private_key)
        sig = cipherrsa.decrypt(signature[:256])
        sig = sig + cipherrsa.decrypt(signature[256:])

        myhash = SHA.new(plaintext)
        signature = PKCS1_v1_5.new(public_key)

        b = False
        if signature.verify(myhash, sig):
            b = True

        return (b, plaintext)
