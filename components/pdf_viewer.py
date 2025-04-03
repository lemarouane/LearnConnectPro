import streamlit as st
import base64
from encryption import FileEncryption
import os
from utils import protect_pdf_content, log_screenshot_attempt

def pdf_viewer(encrypted_path, title="PDF Viewer"):
    """
    Display a PDF viewer for an encrypted PDF file.
    
    Args:
        encrypted_path: Path to the encrypted PDF file
        title: Title to display above the viewer
    """
    if not os.path.exists(encrypted_path):
        st.error("PDF file not found.")
        return
    
    # Decrypt the PDF to memory
    try:
        encryption = FileEncryption()
        pdf_data = encryption.decrypt_file(encrypted_path)
        
        # Convert to base64 string for display
        b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
        
        # Set up the PDF viewer with protections
        protect_pdf_content()
        
        # Display PDF using an iframe with protections
        st.markdown(f"## {title}")
        
        # Monitor screenshot attempts
        if st.button("Take Screenshot (3 max per 15 minutes)"):
            allowed, message = log_screenshot_attempt(
                st.session_state.user_id, 
                st.session_state.get('current_course_id')
            )
            if allowed:
                st.success(message)
            else:
                st.error(message)
        
        # Create a unique PDF display name to prevent browser caching
        pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Additional protections warning
        st.info("Note: This document is protected. Screenshots are limited to 3 per 15 minutes and are monitored.")
        
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")

def pdf_preview(encrypted_path, max_height=300):
    """
    Display a smaller PDF preview for an encrypted PDF file.
    
    Args:
        encrypted_path: Path to the encrypted PDF file
        max_height: Maximum height for the preview iframe
    """
    if not os.path.exists(encrypted_path):
        st.error("PDF file not found.")
        return
    
    try:
        encryption = FileEncryption()
        pdf_data = encryption.decrypt_file(encrypted_path)
        
        b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
        
        # Display a smaller preview
        pdf_preview = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="{max_height}" type="application/pdf"></iframe>'
        st.markdown(pdf_preview, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error displaying PDF preview: {str(e)}")