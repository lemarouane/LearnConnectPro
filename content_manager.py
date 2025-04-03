import os
import json
import tempfile
import shutil
from datetime import datetime
from encryption import FileEncryption
from database import Database

class ContentManager:
    """Class for managing educational content (PDFs and videos)."""
    
    def __init__(self, upload_dir="uploads", encrypted_dir="uploads/encrypted"):
        """Initialize with directories for uploads and encrypted files."""
        self.upload_dir = upload_dir
        self.encrypted_dir = encrypted_dir
        self.encryption = FileEncryption()
        self.db = Database()
        
        # Ensure directories exist
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.encrypted_dir, exist_ok=True)
    
    def add_content(self, file_obj, title, content_type, metadata, difficulty, category, user_id):
        """
        Add new content to the system.
        
        Args:
            file_obj: File object from Streamlit uploader (PDF) or YouTube URL
            title: Content title
            content_type: "PDF" or "YouTube"
            metadata: Dictionary of additional metadata
            difficulty: Difficulty level
            category: Content category
            user_id: ID of the user adding the content
            
        Returns:
            content_id: ID of the newly added content
        """
        # Convert metadata to JSON string if provided
        metadata_json = json.dumps(metadata) if metadata else None
        
        # Handle content based on type
        if content_type == "PDF":
            # Save uploaded file
            file_path = os.path.join(self.upload_dir, file_obj.name)
            with open(file_path, "wb") as f:
                f.write(file_obj.getbuffer())
            
            # Encrypt file
            encrypted_path = self.encryption.encrypt_file(file_path, self.encrypted_dir)
            
            # Register in database
            content_id = self.db.add_course(
                title=title,
                content_type=content_type,
                content_path=encrypted_path,
                youtube_url=None,
                difficulty=difficulty,
                description=metadata_json,
                subject_id=category,
                level_id=None,  # Will be updated after creation
                image_path=None,
                created_by=user_id
            )
            
            # Clean up original file
            if os.path.exists(file_path):
                os.remove(file_path)
                
            return content_id
        
        elif content_type == "YouTube":
            # Save YouTube URL directly
            youtube_url = file_obj  # In this case, file_obj is the URL string
            
            content_id = self.db.add_course(
                title=title,
                content_type=content_type,
                content_path=None,
                youtube_url=youtube_url,
                difficulty=difficulty,
                description=metadata_json,
                subject_id=category,
                level_id=None,  # Will be updated after creation
                image_path=None,
                created_by=user_id
            )
            
            return content_id
        
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
    
    def get_content(self, content_id):
        """Get content details by ID."""
        return self.db.get_course(content_id)
    
    def update_content(self, content_id, **kwargs):
        """Update content metadata."""
        valid_fields = [
            "title", "difficulty", "description", "level_id", "subject_id", "image_path"
        ]
        
        # Filter valid fields
        update_data = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        # Convert metadata to JSON if provided
        if "metadata" in kwargs:
            update_data["description"] = json.dumps(kwargs["metadata"])
        
        return self.db.update_course(content_id, **update_data)
    
    def delete_content(self, content_id):
        """Delete content and associated files."""
        # Get content details
        content = self.get_content(content_id)
        
        if not content:
            return False
        
        # Delete from database (returns file paths)
        result = self.db.delete_course(content_id)
        
        # Delete files if they exist
        if content["content_path"] and os.path.exists(content["content_path"]):
            os.remove(content["content_path"])
        
        if content["image_path"] and os.path.exists(content["image_path"]):
            os.remove(content["image_path"])
        
        return True
    
    def get_content_data(self, content_id):
        """
        Get decrypted content data for a specific content ID.
        Returns the content data as bytes and the MIME type.
        """
        content = self.get_content(content_id)
        
        if not content:
            return None, None
        
        # Handle based on content type
        if content["content_type"] == "PDF":
            encrypted_path = content["content_path"]
            
            if not os.path.exists(encrypted_path):
                return None, None
            
            # Decrypt content
            decrypted_data = self.encryption.decrypt_file(encrypted_path)
            
            return decrypted_data, "application/pdf"
        
        elif content["content_type"] == "YouTube":
            # For YouTube, just return the URL
            return content["youtube_url"], "video/youtube"
        
        return None, None
    
    def assign_to_user(self, content_id, user_id):
        """Assign content to a specific user."""
        return self.db.assign_course_to_user(user_id, content_id)
    
    def unassign_from_user(self, content_id, user_id):
        """Remove content assignment from a user."""
        return self.db.unassign_course_from_user(user_id, content_id)
    
    def get_user_content(self, user_id):
        """Get all content assigned to a specific user."""
        return self.db.get_user_courses(user_id)
    
    def get_assigned_users(self, content_id):
        """Get all users assigned to a specific content."""
        return self.db.get_users_assigned_to_course(content_id)
    
    def get_difficulty_levels(self):
        """Get list of available difficulty levels."""
        return ["easy", "medium", "hard"]