import os
from database import Database
from encryption import FileEncryption
import mimetypes
import shutil

class ContentManager:
    """Class for managing educational content (PDFs and videos)."""
    
    def __init__(self, upload_dir="uploads", encrypted_dir="uploads/encrypted"):
        """Initialize with directories for uploads and encrypted files."""
        self.upload_dir = upload_dir
        self.encrypted_dir = encrypted_dir
        self.db = Database()
        self.encryption = FileEncryption()
        
        # Ensure directories exist
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.encrypted_dir, exist_ok=True)
    
    def add_content(self, file_obj, title, content_type, metadata, difficulty, category, user_id):
        """
        Add new content to the system.
        
        Args:
            file_obj: File object from Streamlit uploader
            title: Content title
            content_type: "PDF" or "Video"
            metadata: Dictionary of additional metadata
            difficulty: Difficulty level
            category: Content category
            user_id: ID of the user adding the content
            
        Returns:
            content_id: ID of the newly added content
        """
        # Validate content type
        if content_type not in ["PDF", "Video"]:
            raise ValueError("Content type must be either 'PDF' or 'Video'")
        
        # Save uploaded file
        file_path = os.path.join(self.upload_dir, file_obj.name)
        with open(file_path, "wb") as f:
            f.write(file_obj.getbuffer())
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Encrypt file
        encrypted_path = self.encryption.encrypt_file(file_path, self.encrypted_dir)
        
        # Add to database
        content_id = self.db.add_content(
            title=title,
            content_type=content_type,
            file_path=file_path,
            encrypted_path=encrypted_path,
            original_filename=file_obj.name,
            file_size=file_size,
            metadata=metadata,
            difficulty=difficulty,
            category=category,
            added_by=user_id
        )
        
        return content_id
    
    def get_content(self, content_id):
        """Get content details by ID."""
        return self.db.get_content(content_id)
    
    def update_content(self, content_id, **kwargs):
        """Update content metadata."""
        return self.db.update_content(content_id, **kwargs)
    
    def delete_content(self, content_id):
        """Delete content and associated files."""
        file_path, encrypted_path = self.db.delete_content(content_id)
        
        # Delete files if they exist
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        if encrypted_path and os.path.exists(encrypted_path):
            os.remove(encrypted_path)
    
    def get_content_data(self, content_id):
        """
        Get decrypted content data for a specific content ID.
        Returns the content data as bytes and the MIME type.
        """
        content = self.db.get_content(content_id)
        if not content:
            return None, None
        
        # Decrypt the file
        decrypted_data = self.encryption.decrypt_file(content['encrypted_path'])
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(content['original_filename'])
        if not mime_type:
            if content['type'] == 'PDF':
                mime_type = 'application/pdf'
            elif content['type'] == 'Video':
                mime_type = 'video/mp4'
            else:
                mime_type = 'application/octet-stream'
        
        return decrypted_data, mime_type
    
    def assign_to_user(self, content_id, user_id):
        """Assign content to a specific user."""
        return self.db.assign_content(content_id, user_id)
    
    def unassign_from_user(self, content_id, user_id):
        """Remove content assignment from a user."""
        return self.db.unassign_content(content_id, user_id)
    
    def get_user_content(self, user_id):
        """Get all content assigned to a specific user."""
        return self.db.get_user_content(user_id)
    
    def get_assigned_users(self, content_id):
        """Get all users assigned to a specific content."""
        return self.db.get_content_assignments(content_id)
