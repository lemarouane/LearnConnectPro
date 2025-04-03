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
        
        # Save to a temporary file that will be displayed using an object tag
        temp_dir = "uploads/temp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, f"temp_{st.session_state.user_id}_{os.path.basename(encrypted_path)}")
        
        with open(temp_file_path, 'wb') as f:
            f.write(pdf_data)
        
        # Set up the PDF viewer with protections
        protect_pdf_content()
        
        # Display PDF using an object tag instead of iframe
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
        
        # Use streamlit's PDF display functionality
        with open(temp_file_path, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name=os.path.basename(encrypted_path),
                mime="application/pdf"
            )
        
        # Convert to base64 for inline display as a fallback method
        with open(temp_file_path, "rb") as file:
            base64_pdf = base64.b64encode(file.read()).decode('utf-8')
            
        # Use a more robust method with iframe and base64 data
        pdf_display = f"""
        <div style="width:100%; height:600px; overflow:hidden; border:1px solid #ccc; border-radius:5px;">
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" 
                    style="border:none;" frameborder="0" allowfullscreen>
            </iframe>
        </div>
        """
        
        # Display using streamlit components
        st.components.v1.html(pdf_display, height=620)
        
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
        
        # Save to a temporary file for preview
        temp_dir = "uploads/temp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, f"preview_{st.session_state.user_id}_{os.path.basename(encrypted_path)}")
        
        with open(temp_file_path, 'wb') as f:
            f.write(pdf_data)
        
        # Convert to base64 for inline display
        with open(temp_file_path, "rb") as file:
            base64_pdf = base64.b64encode(file.read()).decode('utf-8')
            
        # Use iframe with base64 data for more consistent display
        pdf_preview = f"""
        <div style="width:100%; height:{max_height}px; overflow:hidden; border:1px solid #ddd; border-radius:4px;">
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="{max_height}" 
                    style="border:none;" frameborder="0">
            </iframe>
        </div>
        """
        
        # Display using streamlit components for preview
        st.components.v1.html(pdf_preview, height=max_height+20)
        
    except Exception as e:
        st.error(f"Error displaying PDF preview: {str(e)}")