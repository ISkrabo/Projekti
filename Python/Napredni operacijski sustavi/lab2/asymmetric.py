from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA as _RSA
from Crypto.Signature import pkcs1_15

class RSA:
    def __init__(self, key: int):
        #exp je 65537 jer je obično toliko u praksi
        #takodjer ne deklariram self.exp varijablu jer je po default-u
        #taj exp postavljen na 65537 po default-u u RSA.generate (za generiranje ključeva)
        self.method = _RSA
        self.key = self.method.generate(key)

    def encrypt(self, message):
        if (type(message) == str):
            messageToEncrypt = message.encode("utf8")
        else:
            messageToEncrypt = message
        #vrsi padding
        return PKCS1_OAEP.new(self.key).encrypt(messageToEncrypt)

    def decrypt(self, message):
        return PKCS1_OAEP.new(self.key).decrypt(message)

    #digitalno potpisivanje
    def sign(self, message):
        return pkcs1_15.new(self.key).sign(message)