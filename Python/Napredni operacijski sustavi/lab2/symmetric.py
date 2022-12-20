from Crypto.Cipher import AES as _AES
from Crypto.Cipher import DES3 as _DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode

cipherDictionaryAES = \
    {
        "cbc": _AES.MODE_CBC,
        "ofb": _AES.MODE_OFB
    }

cipherDictionaryDES3 = \
    {
        "cbc": _DES3.MODE_CBC,
        "ofb": _DES3.MODE_OFB
    }

methodDictionary = \
    {
        "aes": _AES,
        "3-des": _DES3
    }

class Encrypter():
    def __init__(self, method: str, key: int, cipher: str):
        self.method = methodDictionary[method]
        self.key = key//8
        self.cipher = cipherDictionaryAES[cipher]
        self.initVector = get_random_bytes(self.method.block_size)
        #za DES3 treba staviti pravilnu duljinu tajnog kljuca
        if (method == "3-des"):
            self.secretKey = _DES3.adjust_key_parity(get_random_bytes(self.key * 3))
        else:  
            self.secretKey = get_random_bytes(self.key)

    def getCryptographer(self):
        return self.method.new(
            self.secretKey,
            self.cipher,
            self.initVector
        )

    def encrypt(self, message):
        #priprema poruke: enkodiranje
        if (type(message) == str):
            messageToEncrypt = message.encode("utf8")
        else:
            messageToEncrypt = message
        #                 nadopuna poruke
        messageToEncrypt = pad(messageToEncrypt, self.method.block_size)

        #kriptiranje poruke: dohvacanje kriptografa i enkodiranje
        messageEncrypted = self.getCryptographer().encrypt(messageToEncrypt)
        #formatiranje poruke
        return b64encode(messageEncrypted)

    def decrypt(self, message):
        #de-formatiranje poruke
        messageDecrypted = b64decode(message)
        #dekriptiranje poruke: analogno
        return unpad(self.getCryptographer().decrypt(messageDecrypted), self.method.block_size)