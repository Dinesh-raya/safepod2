"""Test script for encryption service"""
import base64
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.encryption_service import encryption_service

def test_encryption():
    """Test the encryption and decryption functionality"""
    print("Testing encryption service...")
    
    # Test data
    test_content = "This is a secret message that should be encrypted!"
    test_password = "my_secure_password_123!"
    
    try:
        # Generate a salt
        salt = encryption_service.generate_salt()
        print(f"Generated salt: {base64.urlsafe_b64encode(salt).decode()}")
        
        # Derive key from password
        key = encryption_service.derive_key_from_password(test_password, salt)
        print(f"Derived key: {key}")
        
        # Encrypt content
        encrypted_content = encryption_service.encrypt_content(test_content, key)
        print(f"Encrypted content: {encrypted_content}")
        
        # Decrypt content
        decrypted_content = encryption_service.decrypt_content(encrypted_content, key)
        print(f"Decrypted content: {decrypted_content}")
        
        # Verify
        if test_content == decrypted_content:
            print("✅ Encryption/Decryption test PASSED")
            return True
        else:
            print("❌ Encryption/Decryption test FAILED")
            return False
            
    except Exception as e:
        print(f"❌ Encryption test FAILED with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_encryption()
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)