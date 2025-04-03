import os
import tempfile
import PyPDF2
import base64
from io import BytesIO
from PIL import Image
import streamlit as st
from database import Database
from encryption import FileEncryption

def validate_file(uploaded_file, allowed_types):
    """
    Validate file type and size.
    Returns (is_valid, message)
    """
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file type
    file_type = uploaded_file.type
    file_name = uploaded_file.name
    file_size = uploaded_file.size
    
    # Size limit: 100MB
    size_limit = 100 * 1024 * 1024
    
    if file_size > size_limit:
        return False, f"File size exceeds limit (100MB). Current size: {file_size/1024/1024:.2f}MB"
    
    if file_type not in allowed_types:
        return False, f"Invalid file type: {file_type}. Allowed types: {', '.join(allowed_types)}"
    
    return True, "File is valid"

def save_uploaded_file(uploaded_file, directory="uploads"):
    """
    Save an uploaded file to disk and encrypt it.
    Returns (original_path, encrypted_path, file_size)
    """
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Save original file
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Encrypt file
    encryption = FileEncryption()
    encrypted_path = encryption.encrypt_file(file_path, os.path.join(directory, "encrypted"))
    
    return file_path, encrypted_path, file_size

def delete_file(file_path, encrypted_path):
    """Delete both the original and encrypted files."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        if encrypted_path and os.path.exists(encrypted_path):
            os.remove(encrypted_path)
        
        return True
    except Exception as e:
        st.error(f"Error deleting files: {str(e)}")
        return False

def get_pdf_preview(encrypted_path, max_pages=1):
    """
    Get a preview of the first few pages of a PDF.
    Returns a base64 encoded image of the first page.
    """
    try:
        # Decrypt the PDF
        encryption = FileEncryption()
        decrypted_data = encryption.decrypt_file(encrypted_path)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(decrypted_data)
            temp_path = temp_file.name
        
        try:
            # Extract the first page as an image
            pdf_reader = PyPDF2.PdfReader(temp_path)
            num_pages = len(pdf_reader.pages)
            
            if num_pages > 0:
                # Convert first page to image (using other libraries would be better,
                # but for simplicity we'll return info about the PDF)
                page = pdf_reader.pages[0]
                page_text = page.extract_text()[:200] + "..." if page.extract_text() else "No text available"
                
                return {
                    "success": True,
                    "num_pages": num_pages,
                    "preview_text": page_text,
                    "has_content": True
                }
            else:
                return {
                    "success": True,
                    "num_pages": 0,
                    "preview_text": "PDF has no pages",
                    "has_content": False
                }
        finally:
            # Delete the temporary file
            os.unlink(temp_path)
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "has_content": False
        }

def get_content_categories():
    """Get all unique content categories from the database."""
    db = Database()
    all_content = db.get_all_content()
    categories = set()
    
    for content in all_content:
        if content['category']:
            categories.add(content['category'])
    
    return sorted(list(categories))

def get_content_difficulties():
    """Get all unique content difficulty levels from the database."""
    return ["Beginner", "Intermediate", "Advanced", "Expert"]

def apply_custom_css():
    """Apply custom CSS to the Streamlit app."""
    with open("styles/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def create_card(title, content, card_class="card"):
    """Create a styled card with the given title and content."""
    card_html = f"""
    <div class="{card_class}">
        <h3 class="card-text">{title}</h3>
        <div class="card-text">{content}</div>
    </div>
    """
    return st.markdown(card_html, unsafe_allow_html=True)

def format_size(size_bytes):
    """Format file size in a human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    else:
        return f"{size_bytes/1024/1024:.1f} MB"
