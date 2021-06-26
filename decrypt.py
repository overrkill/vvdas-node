from Crypto import Cipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode

def decrypt(data):
    with open("node/pvk") as pvkf:
        pvk = pvkf.read()
        pvk_object = RSA.import_key(pvk)
        cp_rsa = PKCS1_OAEP.new(pvk_object)
        return cp_rsa.decrypt(b64decode(data)).decode('utf-8')