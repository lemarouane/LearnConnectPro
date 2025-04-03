import streamlit as st
import os
import pandas as pd
from database import Database
from utils import (
    get_pdf_preview, create_card, format_size, apply_custom_css
)
from encryption import FileEncryption
from auth import require_login
import tempfile
import base64

@require_login
def student_dashboard():
    """Student dashboard for accessing assigned content."""
    st.title("Student Dashboard")
    apply_custom_css()
    
    # Welcome message
    st.markdown(f"""
    <div class="main-bg">
        <h2>Welcome, {st.session_state.username}!</h2>
        <p>Access your learning materials below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user's content
    db = Database()
    content_list = db.get_user_content(st.session_state.user_id)
    
    if not content_list:
        st.info("No content has been assigned to you yet. Please check back later.")
        return
    
    # Content filtering options
    st.subheader("Your Learning Materials")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        content_types = ["All"] + list(set(item["type"] for item in content_list))
        filter_type = st.selectbox("Filter by Type", content_types)
    
    with col2:
        categories = ["All"] + list(set(item["category"] for item in content_list if item["category"]))
        filter_category = st.selectbox("Filter by Category", categories)
    
    with col3:
        difficulties = ["All"] + list(set(item["difficulty"] for item in content_list if item["difficulty"]))
        filter_difficulty = st.selectbox("Filter by Difficulty", difficulties)
    
    # Apply filters
    filtered_content = content_list
    if filter_type != "All":
        filtered_content = [item for item in filtered_content if item["type"] == filter_type]
    if filter_category != "All":
        filtered_content = [item for item in filtered_content if item["category"] == filter_category]
    if filter_difficulty != "All":
        filtered_content = [item for item in filtered_content if item["difficulty"] == filter_difficulty]
    
    # Display content cards
    if not filtered_content:
        st.info("No content matches your filters. Try changing the filter criteria.")
        return
    
    # Group by category
    categories = {}
    for item in filtered_content:
        category = item["category"] or "Uncategorized"
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    for category, items in categories.items():
        st.subheader(category)
        
        # Create columns for cards
        cols = st.columns(3)
        
        for i, item in enumerate(items):
            with cols[i % 3]:
                display_content_card(item)
    
    # Content viewer
    if "selected_content_id" in st.session_state and st.session_state.selected_content_id:
        display_content_viewer(st.session_state.selected_content_id)

def display_content_card(content):
    """Display a content card in the student dashboard."""
    card_html = f"""
    <div class="card">
        <h3 class="card-text">{content['title']}</h3>
        <p class="card-text">{content['type']} | {content['difficulty'] or 'No difficulty'}</p>
        <p class="card-text">{content['metadata'].get('description', '')[:100]}{'...' if len(content['metadata'].get('description', '')) > 100 else ''}</p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Details", key=f"view_{content['id']}"):
            st.session_state.selected_content_id = content['id']
            st.rerun()
    
    with col2:
        if content['type'] == 'PDF':
            if st.button("Download PDF", key=f"download_{content['id']}"):
                download_content(content)

def display_content_viewer(content_id):
    """Display a detailed content viewer for the selected content."""
    db = Database()
    content = db.get_content(content_id)
    
    if not content:
        st.error(f"Content with ID {content_id} not found")
        return
    
    st.write(f"## {content['title']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(f"**Type:** {content['type']}")
        st.write(f"**Category:** {content['category']}")
        st.write(f"**Difficulty:** {content['difficulty']}")
        
        if content['metadata'].get('description'):
            st.write("**Description:**")
            st.write(content['metadata']['description'])
        
        if content['metadata'].get('tags'):
            st.write("**Tags:**")
            tags = content['metadata']['tags']
            if isinstance(tags, list):
                st.write(", ".join(tags))
            else:
                st.write(tags)
    
    with col2:
        st.write(f"**File Size:** {format_size(content['file_size'])}")
        st.write(f"**Added On:** {content['created_at'].split()[0]}")
        
        if content['type'] == 'PDF':
            if st.button("Download PDF", key=f"download_detail_{content_id}"):
                download_content(content)
    
    # Content preview
    st.write("### Content Preview")
    
    if content['type'] == 'PDF':
        preview_result = get_pdf_preview(content['encrypted_path'])
        
        if preview_result['success']:
            st.write(f"**Number of Pages:** {preview_result['num_pages']}")
            st.write("**Preview of first page:**")
            st.text(preview_result['preview_text'])
            
            # Display PDF preview
            with st.expander("View PDF Content"):
                show_pdf_preview(content['encrypted_path'])
        else:
            st.error(f"Error previewing PDF: {preview_result.get('error', 'Unknown error')}")
    
    elif content['type'] == 'Video':
        st.write("**Video Player:**")
        show_video_player(content['encrypted_path'])
    
    # Back button
    if st.button("Back to All Content"):
        st.session_state.selected_content_id = None
        st.rerun()

def download_content(content):
    """Provide download functionality for content."""
    try:
        # Decrypt file
        encryption = FileEncryption()
        decrypted_data = encryption.decrypt_file(content['encrypted_path'])
        
        # Create a download button
        st.download_button(
            label=f"Download {content['original_filename']}",
            data=decrypted_data,
            file_name=content['original_filename'],
            mime="application/octet-stream"
        )
        
        # Log the download
        db = Database()
        db.log_activity(
            st.session_state.user_id, 
            f"Downloaded {content['type']}", 
            f"Content ID: {content['id']}, Title: {content['title']}"
        )
        
    except Exception as e:
        st.error(f"Error downloading file: {str(e)}")

def show_pdf_preview(encrypted_path):
    """Show a PDF preview using an iframe."""
    try:
        # Decrypt the PDF
        encryption = FileEncryption()
        decrypted_data = encryption.decrypt_file(encrypted_path)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(decrypted_data)
            temp_path = temp_file.name
        
        # Display the PDF using base64 encoding in an iframe
        # This is a simple approach - Streamlit has limitations for direct PDF viewing
        try:
            with open(temp_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")

def show_video_player(encrypted_path):
    """Show a video player for encrypted video content."""
    try:
        # Decrypt the video
        encryption = FileEncryption()
        decrypted_data = encryption.decrypt_file(encrypted_path)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(decrypted_data)
            temp_path = temp_file.name
        
        try:
            # Display the video using Streamlit's video function
            # This loads the entire video into memory which is not ideal for large files
            with open(temp_path, "rb") as f:
                video_bytes = f.read()
            
            st.video(video_bytes)
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    except Exception as e:
        st.error(f"Error displaying video: {str(e)}")
