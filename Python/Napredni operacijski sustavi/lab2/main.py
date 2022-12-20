import symmetric
import asymmetric
import hashes
import digital
from base64 import b64encode

###     METODE      ###

#ispisuje izracunate podatke, enkripciju i dekripciju
def printData(Method):
    if(not Method.method.__name__.endswith("RSA")):
        print("Inicijalni vektor:   " + Method.initVector.hex())
        print("Tajni kljuc:         " + Method.secretKey.hex())

    if(Method.method.__name__.endswith("RSA")):
        print("Javni eksponent:     " + str(Method.key.n))
        print("Privatni eksponent:  " + str(Method.key.d))

    #kriptiranje
    messageEncrypted = Method.encrypt(message)
    if(Method.method.__name__.endswith("RSA")):
        print("Enkriptirana poruka: " + b64encode(messageEncrypted).decode("utf8"))
    else:
        print("Enkriptirana poruka: " + messageEncrypted.decode("utf8"))
    #dekriptiranje
    messageDecrypted = Method.decrypt(messageEncrypted)
    print("Dekriptirana poruka: " + messageDecrypted.decode("utf8"))

#funkcija koja mijenja drugi simbol u danom skupu byte-ova
def changeData(data):
    data = data.hex()
    dataList = list(data)
    if (dataList[1] == "a"):
        dataList[1] = "b"
    else:
        dataList[1] = "a"
    data = ''.join(dataList)
    data = bytes.fromhex(data)
    return data


###        MAIN         ###
message = "Ovo je poruka koja se koristi u drugom (2.) labosu predmeta Napredni operacijski sustavi."
print("\n\nOriginalna poruka koja ce se koristiti u zadatku:")
print(message + "\n")

###     Simetricni      ###
print("\nSimetricni kriptosustavi:")
print("Odabrani nacini kriptiranja: CBC i OFB")

#aes
for x in (128, 192, 256):
    print("\nKriptosustav AES " + str(x) + ", kriptiranje CBC")
    AES = symmetric.Encrypter("aes", x, "cbc")

    printData(AES)

    print("\nKriptosustav AES " + str(x) + ", kriptiranje OFB")
    AES = symmetric.Encrypter("aes", x, "ofb")

    printData(AES)

#des3
print("\nKriptosustav 3-DES, kriptiranje CBC")
DES3 = symmetric.Encrypter("3-des", 64, "cbc")

printData(DES3)

print("\nKriptosustav 3-DES, kriptiranje OFB")
DES3 = symmetric.Encrypter("3-des", 64, "ofb")

printData(DES3)

###     Asimetricni     ###
print("\n\nZa RSA ce se koristiti iduca vrijednost poruke koja ce se enkriptirati")
message = "123454321"
print(message)

print("\nAsimetricni kriptosustavi:")
print("Odabrane duljine kljuca: 1024, 2048 i 3072. Modul e je defaultnog iznosa 65537")

# pronasao sam navedene duljine kljuca s interneta, stoga njih koristim
for x in (1024, 2048, 3072):
    print("\nKriptosustav RSA s duljinom kljuca " + str(x) + " bitova")
    RSA = asymmetric.RSA(x)
    printData(RSA)

###         HASH         ###
print("\nHash funkcije:")
print("Koriste se SHA-256 i SHA-512 (za SHA2) te SHA3-256 i SHA3-512 (za SHA3)")

for x in ("SHA2", "SHA3"):
    print()
    for y in (256, 512):
        SHA = hashes.SHA(x, y)
        print("Funkcija " + x + " s duljinom sazetka " + str(y))
        print("Hash poruke glasi: " + SHA.getHash(message).hex())

###    Digitalni potpis    ###
print("\nProvjera digitalnog potpisa pomocu SHA-512 i SHA3-512")

signatures = [("SHA2", 512), ("SHA3", 512)]
for x in signatures:
    print("\n" + x[0])
    digitalSignature = digital.Signature(x)
    signedMessage = digitalSignature.sign(message)
    print("Primljeni potpis poruke glasi: " + signedMessage.hex())
    isCorrect = digitalSignature.verify(message, signedMessage)
    if (isCorrect):
        print("Potpis je ispravan")
    else:
        print("Potpis nije ispravan")

###   Digitalna omotnica   ###
print("\nProvjera digitalne omotnice pomocu AES i DES3 kriptiranja")

envelopes = [("AES", ("aes", 128, "cbc")), ("DES", ("3-des", 64, "cbc"))]
for x in envelopes:
    print("\n" + x[0])
    digitalEnvelope = digital.Envelope(x[1])
    data, key = digitalEnvelope.envelop(message)
    print("Enkriptirani podaci su:\n     Enkriptirana poruka: " + data.hex() + "\n     Enkriptirani kljuc:  " + key.hex() + "\n")

    dataDecrypted = digitalEnvelope.open(data, key, x[1])

    if (dataDecrypted.decode("utf8") == message):
        print("Dekriptirana poruka je ista kao original")
    else:
        print("Dekriptirana poruka je drugacija")

###    Digitalni pecat     ###
print("\n\nProvjera digitalnog pecata pomocu AES, SHA3 i RSA")

digitalSeal = digital.Seal(("aes", 128, "cbc"), ("SHA3", 512))
encodedMessage, encodedKey, encodedSignature = digitalSeal.closeSeal(message)

print("Dobiveni zapecaceni podaci su:\n      Enkriptirana poruka: " + encodedMessage.decode("utf8") + \
                                    "\n      Enkriptirani kljuc:  " + encodedKey.hex() + \
                                    "\n      Enkriptirani potpis: " + encodedSignature.hex())

print("\nOtvaranje poruke:")
decodedMessage = digitalSeal.openSeal(encodedMessage, encodedKey, encodedSignature)
if (decodedMessage != "err"):
    if (decodedMessage.decode("utf8") == message):
        print("Dekriptirana poruka je ista kao original")
    else:
        print("Dekriptirana poruka je drugacija")

print("\nProvjera sa mijenjanim podacima")
for i in (1, 2):
    print()
    encodedMessage2, encodedKey2, encodedSignature2 = encodedMessage, encodedKey, encodedSignature
    if (i == 1):
        print("Mijenjanje dobivenog potpisa")
        encodedSignature2 = changeData(encodedSignature2)
    else:
        print("Mijenjanje dobivenih podataka")
        encodedMessage2 = changeData(encodedMessage2)

    print("Otvaranje poruke:")
    decodedMessage = digitalSeal.openSeal(encodedMessage2, encodedKey2, encodedSignature2)