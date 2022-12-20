import json
import os
from typing import Dict

import symmetric
import asymmetric
import hashes

class Signature():
    def __init__(self, hashData, encrypter = None):
        #hash funkcija i RSA enkripcija potpisa
        self.hash = hashes.SHA(hashData[0], hashData[1])
        self.hashType = hashData[0]
        self.hashKey = hashData[1]
        self.encrypter = encrypter
        if encrypter is None:
            self.encrypter = asymmetric.RSA(1024)
        else:
            self.encrypter = encrypter

    def sign(self, message):
        #izracunava hash i s njime stvara potpis
        hashNew = hashes.SHA(self.hashType, self.hashKey)
        hashNew.updateHash(message)
        signature = self.encrypter.sign(hashNew.hash)
        return signature

    def verify(self, message, signature):
        #provjera ispravnosti
        self.hash.updateHash(message)
        signatureVerify = self.encrypter.sign(self.hash.hash)
        if (signature == signatureVerify):
            return True
        return False

class Envelope():
    def __init__(self, encoder, encrypter = None):
        #AES ili DES3 enkoder, RSA za enkripciju kljuca
        self.encoder = symmetric.Encrypter(*encoder)
        if encrypter is None:
            self.encrypter = asymmetric.RSA(1024)
        else:
            self.encrypter = encrypter
        
    def envelop(self, message):
        #vraca skup poruka i kljuc
        return (self.encoder.encrypt(message), self.encrypter.encrypt(self.encoder.secretKey))

    def open(self, data, key, encoderType):
        #otvara dobiveni podatak s kljucom
        decryptedKey = self.encrypter.decrypt(key)
        newEncoder = symmetric.Encrypter(*encoderType)
        newEncoder.initVector = self.encoder.initVector
        newEncoder.secretKey = decryptedKey
        return newEncoder.decrypt(data)

class Seal():
    def __init__(self, symmetricData, hashData):
        self.envelope = Envelope(symmetricData)
        self.signature = Signature(hashData)

        self.symmetricData = symmetricData
        self.hashData = hashData

    def closeSeal(self, message):
        #stvara omotnicu iz poruke te tu omotnicu enkrptira
        data, key = self.envelope.envelop(message)
        signature = self.signature.sign(data + key)

        return data, key, signature

    def openSeal(self, data, key, signature):
        #provjerava ispravnost enkripcije
        signatureChecker = Signature(self.hashData, self.signature.encrypter)

        if(signatureChecker.verify(data + key, signature)):
            print("Provjera sigurnosti je prosla")
        else:
            print("Sigurnost je narusena!")
            return ("err")
        
        return self.envelope.open(data, key, self.symmetricData)

