from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder


def string_to_signing_key(string):
    return SigningKey(string, encoder=HexEncoder)


def string_to_verify_key(string):
    return VerifyKey(string, encoder=HexEncoder)


def nacl_to_string(nacl):
    return nacl.encode(encoder=HexEncoder).decode()


def get_account_number(signing_key):
    if not isinstance(signing_key, SigningKey):
        signing_key = string_to_signing_key(signing_key)
    return nacl_to_string(signing_key.verify_key)


def generate_signing_key():
    return nacl_to_string(SigningKey.generate())
