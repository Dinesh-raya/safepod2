"""Encryption service for securing content at rest"""
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Tuple

class EncryptionService:
    """Service for encrypting and decrypting content"""
    
    def __init__(self):
        pass
    
    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        """Derive a key from a password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def generate_salt(self) -> bytes:
        """Generate a random salt for key derivation"""
        return os.urandom(16)
    
    def encrypt_content(self, content: str, encryption_key: bytes) -> str:
        """Encrypt content with a key"""
        f = Fernet(encryption_key)
        encrypted_content = f.encrypt(content.encode())
        return encrypted_content.decode()
    
    def decrypt_content(self, encrypted_content: str, encryption_key: bytes) -> str:
        """Decrypt content with a key"""
        f = Fernet(encryption_key)
        decrypted_content = f.decrypt(encrypted_content.encode())
        return decrypted_content.decode()

# Global instance
encryption_service = EncryptionService()