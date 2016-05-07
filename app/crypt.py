# -*- coding: utf-8 -*-
import hashlib
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import AES
from Crypto import Random

class MyCrypt():
    def __init__(self, key):
        self.key = hashlib.md5(key).hexdigest()
        self.iv = b'0000000000000000'
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')
