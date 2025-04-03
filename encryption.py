import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class FileEncryption:
    def __init__(self, key_file="secure_key.key"):
        """Initialize with a key file or generate a new key."""
        self.key_file = key_file
        self.key = self._get_or_create_key()
        self.fernet = Fernet(self.key)
    
    def _get_or_create_key(self):
        """Get existing key or create a new one."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as file:
                key = file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as file:
                file.write(key)
        return key
    
    def encrypt_file(self, input_path, output_dir):
        """
        Encrypt a file and save it to output directory.
        Returns the path to the encrypted file.
        """
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Get base filename
        base_name = os.path.basename(input_path)
        encrypted_path = os.path.join(output_dir, f"{base_name}.enc")
        
        # Read file data
        with open(input_path, "rb") as file:
            data = file.read()
        
        # Encrypt data
        encrypted_data = self.fernet.encrypt(data)
        
        # Save encrypted data
        with open(encrypted_path, "wb") as file:
            file.write(encrypted_data)
        
        return encrypted_path
    
    def decrypt_file(self, encrypted_path, output_path=None):
        """
        Decrypt a file.
        If output_path is provided, save to that path.
        Otherwise, return the decrypted data.
        """
        # Read encrypted data
        with open(encrypted_path, "rb") as file:
            encrypted_data = file.read()
        
        # Decrypt data
        decrypted_data = self.fernet.decrypt(encrypted_data)
        
        if output_path:
            # Create directory if needed
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save decrypted data
            with open(output_path, "wb") as file:
                file.write(decrypted_data)
            return output_path
        else:
            # Return the decrypted data
            return decrypted_data