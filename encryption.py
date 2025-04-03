import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class FileEncryption:
    def __init__(self, key_file="secure_key.key"):
        """Initialize with a key file or generate a new key."""
        self.key_file = key_file
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self):
        """Get existing key or create a new one."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                key = f.read()
        else:
            # Generate a key from password and salt
            password = os.getenv("ENCRYPTION_PASSWORD", "secure_elearning_platform").encode()
            salt = os.getenv("ENCRYPTION_SALT", "secure_salt_value").encode()
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            # Save key to file with secure permissions
            with open(self.key_file, "wb") as f:
                f.write(key)
            
            # Set permissions to readable only by owner
            os.chmod(self.key_file, 0o600)
        
        return key
    
    def encrypt_file(self, input_path, output_dir):
        """
        Encrypt a file and save it to output directory.
        Returns the path to the encrypted file.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate a secure filename
        original_filename = os.path.basename(input_path)
        file_hash = base64.urlsafe_b64encode(
            hashes.Hash(hashes.SHA256()).update(original_filename.encode()).finalize()
        ).decode()[:10]
        
        encrypted_filename = f"{file_hash}_{original_filename}.enc"
        output_path = os.path.join(output_dir, encrypted_filename)
        
        # Encrypt the file
        with open(input_path, "rb") as f_in:
            data = f_in.read()
            encrypted_data = self.cipher.encrypt(data)
            
            with open(output_path, "wb") as f_out:
                f_out.write(encrypted_data)
        
        # Set secure permissions for encrypted file
        os.chmod(output_path, 0o600)
        
        return output_path
    
    def decrypt_file(self, encrypted_path, output_path=None):
        """
        Decrypt a file.
        If output_path is provided, save to that path.
        Otherwise, return the decrypted data.
        """
        with open(encrypted_path, "rb") as f:
            encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            if output_path:
                with open(output_path, "wb") as f_out:
                    f_out.write(decrypted_data)
                return output_path
            else:
                return decrypted_data
