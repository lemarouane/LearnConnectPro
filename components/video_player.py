import streamlit as st
from utils import extract_youtube_id, create_youtube_embed_html, protect_pdf_content, log_screenshot_attempt

def video_player(youtube_url, title="Video Player"):
    """
    Display a video player for a YouTube video.
    
    Args:
        youtube_url: YouTube URL for the video
        title: Title to display above the video player
    """
    if not youtube_url:
        st.error("Video URL not provided.")
        return
    
    # Apply content protection
    protect_pdf_content()
    
    # Extract YouTube ID
    video_id = extract_youtube_id(youtube_url)
    
    if not video_id:
        st.error("Invalid YouTube URL.")
        return
    
    # Display title
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
    
    # Create and display YouTube embed
    embed_html = create_youtube_embed_html(video_id)
    st.markdown(embed_html, unsafe_allow_html=True)
    
    # Add warning about restrictions
    st.info("Note: This video is protected. Screenshots are limited to 3 per 15 minutes and are monitored.")

def video_thumbnail(youtube_url, max_width=300):
    """
    Display a video thumbnail with play button that expands to full player.
    
    Args:
        youtube_url: YouTube URL for the video
        max_width: Maximum width for the thumbnail display
    """
    if not youtube_url:
        st.error("Video URL not provided.")
        return
    
    # Extract YouTube ID
    video_id = extract_youtube_id(youtube_url)
    
    if not video_id:
        st.error("Invalid YouTube URL.")
        return
    
    # Create a thumbnail with play button overlay
    thumbnail_html = f"""
    <div style="max-width: {max_width}px; margin: 0 auto;">
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
            <img src="https://img.youtube.com/vi/{video_id}/0.jpg" 
                 style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; cursor: pointer;"
                 onclick="this.style.display='none'; document.getElementById('player-{video_id}').style.display='block';">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">
                <svg height="48" width="48" fill="#fff" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z"/>
                </svg>
            </div>
            <div id="player-{video_id}" style="display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
                <iframe width="100%" height="100%" src="https://www.youtube.com/embed/{video_id}" 
                        frameborder="0" allowfullscreen></iframe>
            </div>
        </div>
    </div>
    """
    
    st.markdown(thumbnail_html, unsafe_allow_html=True)