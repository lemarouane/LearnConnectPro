import os
import base64
import tempfile
from datetime import datetime
from encryption import FileEncryption
from database import Database
import streamlit as st
import io
import re
from PIL import Image

def validate_file(uploaded_file, allowed_types):
    """
    Validate file type and size.
    Returns (is_valid, message)
    """
    if not uploaded_file:
        return False, "No file uploaded"
    
    # Extract file extension
    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()
    
    # Validate file type
    if ext not in allowed_types:
        return False, f"File type not allowed. Please upload one of: {', '.join(allowed_types)}"
    
    # Validate file size (max 50MB)
    if uploaded_file.size > 50 * 1024 * 1024:
        return False, "File too large. Maximum size is 50MB"
    
    return True, ""

def save_uploaded_file(uploaded_file, directory="uploads"):
    """
    Save an uploaded file to disk and encrypt it.
    Returns (original_path, encrypted_path, file_size)
    """
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    encrypted_dir = os.path.join(directory, "encrypted")
    os.makedirs(encrypted_dir, exist_ok=True)
    
    # Save file temporarily
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Encrypt file
    encryption = FileEncryption()
    encrypted_path = encryption.encrypt_file(file_path, encrypted_dir)
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    return file_path, encrypted_path, file_size

def delete_file(file_path, encrypted_path):
    """Delete both the original and encrypted files."""
    if os.path.exists(file_path):
        os.remove(file_path)
    
    if os.path.exists(encrypted_path):
        os.remove(encrypted_path)
    
    return True

def get_pdf_preview(encrypted_path, max_pages=1):
    """
    Get a preview of the first few pages of a PDF.
    Returns a base64 encoded image of the first page.
    """
    try:
        # Decrypt PDF temporarily
        encryption = FileEncryption()
        pdf_data = encryption.decrypt_file(encrypted_path)
        
        # Use PyPDF2 to render the first page
        from PyPDF2 import PdfReader
        from PIL import Image
        import io
        
        # Create a PDF reader object
        reader = PdfReader(io.BytesIO(pdf_data))
        
        # For simplicity, just return info about the PDF
        # In a real implementation, you would render the page to an image
        num_pages = len(reader.pages)
        first_page = reader.pages[0]
        
        # Return placeholder image data
        # In a real implementation, you'd render the page to an image
        return f"PDF Preview: {num_pages} pages"
        
    except Exception as e:
        st.error(f"Error generating PDF preview: {str(e)}")
        return None

def get_content_categories():
    """Get all unique content categories from the database."""
    db = Database()
    subjects = db.get_all_subjects()
    return subjects

def get_content_difficulties():
    """Get all unique content difficulty levels from the database."""
    return ["easy", "medium", "hard"]

def apply_custom_css():
    """Apply custom CSS to the Streamlit app."""
    custom_css = """
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
            font-weight: bold;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 4px 4px 0px 0px;
            padding: 10px 16px;
            border: 1px solid #ddd;
        }
        .stTabs [aria-selected="true"] {
            background-color: #f0f2f6;
            border-bottom: none;
        }
        
        .content-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .content-card h3 {
            margin-top: 0;
            color: #1f5baa;
        }
        
        .content-card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .difficulty-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        
        .difficulty-easy {
            background-color: #d4edda;
            color: #155724;
        }
        
        .difficulty-medium {
            background-color: #fff3cd;
            color: #856404;
        }
        
        .difficulty-hard {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .user-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 12px;
            background-color: white;
        }
        
        .validated-badge {
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: bold;
        }
        
        .validated-true {
            background-color: #d4edda;
            color: #155724;
        }
        
        .validated-false {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .form-container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #eee;
        }
        
        /* YouTube Embed Styling */
        .youtube-container {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
            height: 0;
            overflow: hidden;
        }
        
        .youtube-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }
        
        /* PDF Viewer Styling */
        .pdf-container {
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
        }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

def create_card(title, content, card_class="card"):
    """Create a styled card with the given title and content."""
    card_html = f"""
    <div class="{card_class}">
        <h3>{title}</h3>
        <div>{content}</div>
    </div>
    """
    return card_html

def format_size(size_bytes):
    """Format file size in a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def extract_youtube_id(url):
    """Extract YouTube video ID from URL."""
    # Regular expressions to match various YouTube URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\s]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^\?\s]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^\?\s]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def create_youtube_embed_html(video_id, width="100%", height="400"):
    """Create HTML for a YouTube embedded player."""
    if not video_id:
        return "<p>Invalid YouTube URL</p>"
    
    html = f"""
    <div class="youtube-container">
        <iframe 
            src="https://www.youtube.com/embed/{video_id}" 
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
    </div>
    """
    return html

def log_screenshot_attempt(user_id, course_id):
    """
    Log a screenshot attempt and check if it's allowed.
    Returns (allowed, message)
    """
    db = Database()
    
    # Get current count
    recent_count = db.get_recent_screenshots(user_id, course_id, minutes=15)
    
    # Check if limit exceeded
    if recent_count >= 3:
        return False, "Screenshot limit reached (3 per 15 minutes). Please try again later."
    
    # Log the new attempt
    db.log_screenshot(user_id, course_id)
    
    # Calculate remaining
    remaining = 3 - (recent_count + 1)
    return True, f"Screenshot taken. You have {remaining} screenshot{'s' if remaining != 1 else ''} remaining in this 15-minute period."

def protect_pdf_content():
    """Add JavaScript to protect PDF content."""
    js = """
    <script>
        // Disable right-click
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
        }, false);
        
        // Disable keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Prevent Ctrl+S, Ctrl+P, Ctrl+U, F12
            if (
                (e.ctrlKey && (e.keyCode == 83 || e.keyCode == 80 || e.keyCode == 85)) || 
                e.keyCode == 123
            ) {
                e.preventDefault();
                return false;
            }
        });
        
        // Detect screenshot attempts
        document.addEventListener('keyup', function(e) {
            // PrintScreen key detection
            if (e.keyCode == 44) {
                notifyScreenshot();
            }
        });
        
        // Function to notify the server about screenshot
        function notifyScreenshot() {
            fetch('/log_screenshot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    course_id: currentCourseId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (!data.allowed) {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    </script>
    """
    return st.markdown(js, unsafe_allow_html=True)