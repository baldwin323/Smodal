
from Crypto.Cipher import AES
from Crypto import Random
import hashlib, base64

class EncryptionManager:
    
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plaintext):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(plaintext.encode())
        return base64.b64encode(iv + ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:]).decode('utf-8')
        return plaintext