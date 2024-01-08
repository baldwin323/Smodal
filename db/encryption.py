import os  # added import to fetch environment variables
from Crypto.Cipher import AES
from Crypto import Random
import hashlib, base64

class EncryptionManager:
    
    def __init__(self):
        # Changed to use environment variable "ENCRYPTION_KEY" for initializing
        if "ENCRYPTION_KEY" in os.environ:
            self.key = hashlib.sha256(os.environ["ENCRYPTION_KEY"].encode()).digest()
        else:
            raise EnvironmentError("ENCRYPTION_KEY not present in environment variables.")  # raise an error if the environment variable is not present. 
            
    def encrypt(self, plaintext):
        try:
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            ciphertext = cipher.encrypt(plaintext.encode())
            return base64.b64encode(iv + ciphertext).decode('utf-8')
        except Exception as e:
            print(f"Encryption Error: {e}")
            return None

    def decrypt(self, ciphertext):
        try:
            ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
            iv = ciphertext[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CFB, iv)
            plaintext = cipher.decrypt(ciphertext[AES.block_size:]).decode('utf-8')
            return plaintext
        except Exception as e:
            print(f"Decryption Error: {e}")
            return None