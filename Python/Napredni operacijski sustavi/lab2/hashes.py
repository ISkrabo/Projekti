from Crypto.Hash import SHA256, SHA512
from Crypto.Hash import SHA3_256, SHA3_512

SHAdictionary =\
    {
        "SHA2_256": SHA256,
        "SHA2_512": SHA512,
        "SHA3_256": SHA3_256,
        "SHA3_512": SHA3_512
    }

class SHA():
    def __init__(self, SHAtype: str, key: int):
        #dohvaca metodu za hash funkciju
        self.method = SHAdictionary[SHAtype + "_" + str(key)]
        self.key = key
        if (SHAtype == "SHA2"):
            self.hash = self.method.new()
        else:
            self.hash = self.method.new(update_after_digest=True)

    def getHash(self, message):
        #dohvacanje hash-a
        if (type(message) == str):
            message = message.encode("utf8")

        self.hash.update(message)
        return self.hash.digest()
    
    def updateHash(self, message):
        #azuriranje hash vrijednosti
        if (type(message) == str):
            message = message.encode("utf8")
        self.hash.update(message)