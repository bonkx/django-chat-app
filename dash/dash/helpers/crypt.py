import hashlib
import hmac
from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from django.conf import settings


def _getPrivateKey():
    # Load private key previouly generated
    with open(settings.MY_PRIVATE_PEM, "r") as myfile:
        private_key = RSA.importKey(myfile.read())
    return private_key


def _getPublicKey():
    # Load private key previouly generated
    with open(settings.MY_PUBLIC_PEM, "r") as myfile:
        public_key = RSA.importKey(myfile.read())
    return public_key


def _encrypt_with_public_key(a_message, public_key):
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_msg = encryptor.encrypt(a_message.encode())
    # print("encrypted_msg:", encrypted_msg)
    encoded_encrypted_msg = b64encode(encrypted_msg)
    # print("encoded_encrypted_msg: ", encoded_encrypted_msg)
    return encoded_encrypted_msg


def _decrypt_with_private_key(encoded_encrypted_msg, private_key):
    encryptor = PKCS1_OAEP.new(private_key)
    decoded_encrypted_msg = b64decode(encoded_encrypted_msg)
    # print("decoded_encrypted_msg: ", decoded_encrypted_msg)
    decoded_decrypted_msg = encryptor.decrypt(decoded_encrypted_msg)
    # print("decoded_decrypted_msg: ", decoded_decrypted_msg)
    return decoded_decrypted_msg


def do_encrypt(msg: str) -> str:
    key = _getPublicKey()
    encrypted = _encrypt_with_public_key(msg, key)
    return encrypted.decode()


def do_decrypt(encoded_encrypted_msg: bytes) -> str:
    key = _getPrivateKey()
    decrypted = _decrypt_with_private_key(encoded_encrypted_msg, key)
    return decrypted.decode()
