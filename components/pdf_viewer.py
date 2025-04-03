import streamlit as st
import base64
import os
import fitz  # PyMuPDF
from PIL import Image
import io
from encryption import FileEncryption
from utils import protect_pdf_content, log_screenshot_attempt
from translations import t  # Import translation function

def pdf_viewer(encrypted_path, title=None):
    """
    Display a PDF viewer for an encrypted PDF file.
    
    Args:
        encrypted_path: Path to the encrypted PDF file
        title: Title to display above the viewer
    """
    if title is None:
        title = t("pdf_viewer")
        
    if not os.path.exists(encrypted_path):
        st.error(t("pdf_not_found"))
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
        if st.button(t("take_screenshot")):
            allowed, message = log_screenshot_attempt(
                st.session_state.user_id, 
                st.session_state.get('current_course_id')
            )
            if allowed:
                st.success(message)
            else:
                st.error(message)
        
        # Convert the PDF to images for display
        
        # Open the PDF with PyMuPDF
        doc = fitz.open(temp_file_path)
        images = []
        
        # Display as individual pages
        st.markdown(f"### {t('pdf_viewer')}")
        
        # Create an expander for pages
        with st.expander(t("view"), expanded=True):
            for page_num in range(min(len(doc), 10)):  # Limit to first 10 pages for performance
                page = doc.load_page(page_num)
                
                # Render page to an image (higher resolution for better quality)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_data = pix.tobytes("png")
                
                # Display the page image
                st.markdown(f"**{t('page')} {page_num + 1}**")
                st.image(img_data, caption=f"{t('page')} {page_num + 1}", use_container_width=True)
                st.markdown("---")
                
            if len(doc) > 10:
                st.info(t("pdf_page_limit").format(total_pages=len(doc)))
        
        # Close the document
        doc.close()
        
        # Additional protections warning
        st.info(t("pdf_protection"))
        
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
        st.error(t("pdf_not_found"))
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
        
        # Convert the PDF to an image for preview
        
        # Open the PDF with PyMuPDF
        doc = fitz.open(temp_file_path)
        
        if len(doc) > 0:
            # Get the first page
            page = doc.load_page(0)
            
            # Render page to an image
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))  # Lower resolution for preview
            img_data = pix.tobytes("png")
            
            # Display the first page as preview
            st.image(img_data, caption=t("pdf_preview"), width=300)
        
        # Close the document
        doc.close()
        
    except Exception as e:
        st.error(f"Error displaying PDF preview: {str(e)}")