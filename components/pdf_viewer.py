import streamlit as st
import os
import tempfile
import base64
from encryption import FileEncryption

def pdf_viewer(encrypted_path, title="PDF Viewer"):
    """
    Display a PDF viewer for an encrypted PDF file.
    
    Args:
        encrypted_path: Path to the encrypted PDF file
        title: Title to display above the viewer
    """
    st.write(f"### {title}")
    
    try:
        # Decrypt the PDF
        encryption = FileEncryption()
        decrypted_data = encryption.decrypt_file(encrypted_path)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(decrypted_data)
            temp_path = temp_file.name
        
        try:
            # Display the PDF using base64 encoding in an iframe
            with open(temp_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # Create a container with scrolling
            pdf_container = st.container()
            
            with pdf_container:
                pdf_display = f"""
                <div style="display: flex; justify-content: center; width: 100%;">
                    <iframe src="data:application/pdf;base64,{base64_pdf}" 
                    width="800" height="600" type="application/pdf" frameborder="0"></iframe>
                </div>
                """
                st.markdown(pdf_display, unsafe_allow_html=True)
                
                # Provide a download button
                st.download_button(
                    label="Download PDF",
                    data=decrypted_data,
                    file_name=os.path.basename(encrypted_path).replace(".enc", ""),
                    mime="application/pdf"
                )
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    except Exception as e:
        st.error(f"Error displaying PDF: {str(e)}")
        return False
    
    return True

def pdf_preview(encrypted_path, max_height=300):
    """
    Display a smaller PDF preview for an encrypted PDF file.
    
    Args:
        encrypted_path: Path to the encrypted PDF file
        max_height: Maximum height for the preview iframe
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
            # Display the PDF using base64 encoding in an iframe
            with open(temp_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            pdf_display = f"""
            <div style="width: 100%; border: 1px solid #e0e0e0; border-radius: 5px; padding: 5px;">
                <iframe src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" height="{max_height}" type="application/pdf" frameborder="0"></iframe>
            </div>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    except Exception as e:
        st.error(f"Error displaying PDF preview: {str(e)}")
        return False
    
    return True
