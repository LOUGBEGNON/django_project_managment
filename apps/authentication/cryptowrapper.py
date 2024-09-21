from cryptography.fernet import Fernet
from django.conf import settings


class CryptoWrapper:
    """ """

    default_key = settings.PROJECT_MANAGMENT_MASTER_KEY

    key = None

    def __init__(self):
        """ """
        self.key = self.generateKey()

    def generateKey(self):
        key = Fernet.generate_key()
        return key

    def encrypt(self, filename, key=None):
        if not key:
            key = self.key

        # using the generated key
        fernet = Fernet(key)

        # opening the original file to encrypt
        with open(filename, "rb") as f:
            original = f.read()

        # encrypting the file
        encrypted = fernet.encrypt(original)

        # opening the file in write mode and
        # writing the encrypted data
        with open(filename + ".encrypted", "wb") as f:
            f.write(encrypted)

        return encrypted

    def decrypt(self, filename, key=None):
        if not key:
            key = self.key

        # using the key
        fernet = Fernet(key)

        # opening the encrypted file
        with open(filename, "rb") as f:
            encrypted = f.read()

        # decrypting the file
        decrypted = fernet.decrypt(encrypted)

        return decrypted.decode()
