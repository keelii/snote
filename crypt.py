# -*- coding: utf-8 -*-
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

class MyCrypt():
    def __init__(self, key):
        self.key = hashlib.md5(key).hexdigest()
        self.mode = AES.MODE_CBC
        self.iv = b'0000000000000000'
        self.padding = '\0'

    def encrypt(self, text):
        cipher = AES.new(self.key, self.mode, self.iv)
        length = 16
        count = text.count('')

        if count < length:
            add = (length - count) + 1
            text += (self.padding * add)
        elif count > length:
            add = (length - (count % length)) + 1
            text += (self.padding * add)
        self.ciphertext = cipher.encrypt(text)
        return self.ciphertext

    def decrypt(self, text):
        cipher = AES.new(self.key, self.mode, self.iv)
        plain_text = cipher.decrypt(text)
        return plain_text.rstrip("\0")

# key = '1234567890abcdef'
# data = '天下之患，最不可为者，名为治平无事，而其实有不测之忧，坐观其变，而不为之所，则恐至于不可救，起而强为之则天下狃于治平之安，而不吾信 ——《苏东坡 晁错论》'
# ec = MyCrypt(key)
# encrpt_data = ec.encrypt(data)
# decrpt_data = ec.decrypt(encrpt_data)

# print '----------'
# print encrpt_data
# print '----------'
# print decrpt_data.decode('utf-8')
# print '----------'
