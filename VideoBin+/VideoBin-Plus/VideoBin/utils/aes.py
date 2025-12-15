from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

def aes_encrypt(data: bytes, password: str):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, 32, count=200000)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return salt, cipher.nonce, tag, ciphertext

def aes_decrypt(salt, nonce, tag, ciphertext, password: str):
    key = PBKDF2(password, salt, 32, count=200000)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
