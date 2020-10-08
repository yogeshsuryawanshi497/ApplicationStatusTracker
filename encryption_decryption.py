'''
Script Name:    encryption_decryption.py
Path:            \IPS_DecisionFabric\Control Framework\
Description:    This script encrypts the provided password and writes it to the config_file.txt
Author:	        Harshita Rai
Revision History:
----------------------------------------------------------------------------------------------------------------------
S.No.            Date(MM/DD/YY)        Changed By               Change Description
----------------------------------------------------------------------------------------------------------------------
1.                07/16/2019            H Rai                Initial Version (IPS Decision Fabric v1.1.1)
2.                                      Y Suryawanshi        Standardized to PEP8

----------------------------------------------------------------------------------------------------------------------
'''

try:
    import base64
    import os
    import hashlib
    from Crypto import Random
    from Crypto.Cipher import AES
except Exception as IE:
    print("Unable to import all modules in", __file__, IE)


class AESCipher(object):

    def __init__(self):
        self.bs = 32
        key_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        key_path += '\\Control Framework\\key.txt'
        with open(key_path, 'rb') as f:
            self.key = f.read()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        password = base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))
        config_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        config_path += '\\config_file.txt'
        with open(config_path, 'a+') as f:
            f.write('\ndb_password~'+str(password.decode('utf-8')))
        return

    def decrypt(self, enc):
        # enc = enc.decode('utf-8')
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return(s[:-ord(s[len(s)-1:])])