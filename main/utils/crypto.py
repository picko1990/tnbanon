from cryptography.fernet import Fernet
from ..config import FERNET_KEY


def encode(text, key):
    return text.encode(), key.encode()


def encrypt(text, key=FERNET_KEY):
    encoded_text, encoded_key = encode(text, key)
    encrypted_text = Fernet(encoded_key).encrypt(encoded_text)
    return encrypted_text.decode()


def decrypt(text, key=FERNET_KEY):
    encoded_text, encoded_key = encode(text, key)
    decrypted_text = Fernet(encoded_key).decrypt(encoded_text)
    return decrypted_text.decode()
