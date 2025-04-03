import streamlit as st
import os
import tempfile
from encryption import FileEncryption

def video_player(encrypted_path, title="Video Player"):
    """
    Display a video player for an encrypted video file.
    
    Args:
        encrypted_path: Path to the encrypted video file
        title: Title to display above the video player
    """
    st.write(f"### {title}")
    
    try:
        # Decrypt the video
        encryption = FileEncryption()
        decrypted_data = encryption.decrypt_file(encrypted_path)
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(decrypted_data)
            temp_path = temp_file.name
        
        try:
            # Use streamlit's native video player
            with open(temp_path, "rb") as f:
                video_bytes = f.read()
            
            st.video(video_bytes)
            
            # Provide a download button
            st.download_button(
                label="Download Video",
                data=decrypted_data,
                file_name=os.path.basename(encrypted_path).replace(".enc", ""),
                mime="video/mp4"
            )
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)
    
    except Exception as e:
        st.error(f"Error displaying video: {str(e)}")
        return False
    
    return True

def video_thumbnail(encrypted_path, max_width=300):
    """
    Display a video thumbnail with play button that expands to full player.
    
    Args:
        encrypted_path: Path to the encrypted video file
        max_width: Maximum width for the thumbnail display
    """
    try:
        # For thumbnail, we'll just use a play button that expands to the full player
        if st.button("▶️ Play Video", key=f"play_{encrypted_path}"):
            # Decrypt the video when play is clicked
            encryption = FileEncryption()
            decrypted_data = encryption.decrypt_file(encrypted_path)
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(decrypted_data)
                temp_path = temp_file.name
            
            try:
                # Use streamlit's native video player
                with open(temp_path, "rb") as f:
                    video_bytes = f.read()
                
                st.video(video_bytes)
            finally:
                # Clean up the temporary file
                os.unlink(temp_path)
    
    except Exception as e:
        st.error(f"Error with video thumbnail: {str(e)}")
        return False
    
    return True
