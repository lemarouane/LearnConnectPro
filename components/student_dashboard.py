import streamlit as st
from database import Database
from content_manager import ContentManager
from components.pdf_viewer import pdf_viewer, pdf_preview
from components.video_player import video_player, video_thumbnail
import json

def student_dashboard():
    """Student dashboard for accessing assigned content."""
    st.title("Student Dashboard")
    st.write(f"Welcome, {st.session_state.full_name or st.session_state.username}!")
    
    db = Database()
    content_manager = ContentManager()
    
    # Custom modern sidebar styling for student
    st.sidebar.markdown("""
    <style>
    .sidebar-header {
        color: #ffffff;
        background: linear-gradient(135deg, #4CAF50, #2E7D32);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .student-info {
        text-align: center;
        margin-bottom: 25px;
        color: #2E7D32;
        font-weight: 600;
        font-size: 16px;
    }
    
    .nav-item {
        display: flex;
        align-items: center;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 7px;
        transition: all 0.3s ease;
        cursor: pointer;
        text-decoration: none;
        color: #333;
        background-color: #f0f7f0;
    }
    
    .nav-item:hover {
        background-color: #e8f5e9;
        transform: translateX(5px);
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    .nav-item-active {
        background-color: #4CAF50;
        color: white;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    .nav-item-active:hover {
        background-color: #388E3C;
        color: white;
    }
    
    .nav-icon {
        margin-right: 10px;
        font-size: 20px;
        width: 25px;
        text-align: center;
    }
    
    .sidebar-footer {
        position: absolute;
        bottom: 20px;
        left: 20px;
        right: 20px;
        text-align: center;
        font-size: 12px;
        color: #777;
        padding-top: 10px;
        border-top: 1px solid #eee;
    }
    
    /* Animation for icon on hover */
    .nav-item:hover .nav-icon {
        transform: scale(1.2);
        transition: transform 0.3s ease;
    }
    
    /* Override default Streamlit radio button styling */
    div.row-widget.stRadio > div {
        flex-direction: column;
        gap: 5px;
    }
    
    .stRadio > div[role="radiogroup"] > label {
        display: none !important;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] {
        flex-direction: column;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Modern sidebar header
    st.sidebar.markdown('<div class="sidebar-header"><h2>Plateforme E-Learning</h2></div>', unsafe_allow_html=True)
    
    # Student info
    st.sidebar.markdown(f'<div class="student-info">{st.session_state.full_name or st.session_state.username}<br><small>Étudiant</small></div>', unsafe_allow_html=True)
    
    # Create navigation options with icons
    nav_options = [
        ("Mes Cours", "📚"),
        ("Profil", "👤")
    ]
    
    # Hidden radio button for navigation
    page = st.sidebar.radio(
        "Go to",
        [option[0] for option in nav_options],
        label_visibility="collapsed"
    )
    
    # Custom navigation buttons with icons
    for option, icon in nav_options:
        active_class = "nav-item-active" if page == option else ""
        st.sidebar.markdown(
            f"""
            <div class="nav-item {active_class}" 
                 onclick="document.querySelector('input[type=radio][value=\'{option}\']').click();">
                <div class="nav-icon">{icon}</div>
                <div>{option}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Footer
    st.sidebar.markdown("""
    <div class="sidebar-footer">
        <div>Plateforme E-Learning Zouhair</div>
        <div>© 2025 Tous Droits Réservés</div>
    </div>
    """, unsafe_allow_html=True)
    
    if page == "Mes Cours":
        st.header("Mes Cours")
        
        # Get student's assigned levels, subjects, and courses
        user_id = st.session_state.user_id
        
        # Get levels and subjects
        user_levels = db.get_user_levels(user_id)
        user_subjects = db.get_user_subjects(user_id)
        
        if not user_levels:
            st.info("You haven't been assigned to any levels yet. Please check back later.")
            return
        
        # Select level
        level_names = [level["name"] for level in user_levels]
        level_ids = [level["id"] for level in user_levels]
        
        selected_level_index = st.selectbox(
            "Select Level", 
            range(len(level_names)),
            format_func=lambda i: level_names[i]
        )
        
        selected_level_id = level_ids[selected_level_index]
        
        # Filter subjects by selected level
        level_subjects = [s for s in user_subjects if s["level_id"] == selected_level_id]
        
        if not level_subjects:
            st.info("You haven't been assigned to any subjects in this level yet.")
            return
        
        # Select subject
        subject_names = [subject["name"] for subject in level_subjects]
        subject_ids = [subject["id"] for subject in level_subjects]
        
        selected_subject_index = st.selectbox(
            "Select Subject", 
            range(len(subject_names)),
            format_func=lambda i: subject_names[i]
        )
        
        selected_subject_id = subject_ids[selected_subject_index]
        
        # Get courses for the selected subject
        courses = db.get_user_courses(user_id, subject_id=selected_subject_id)
        
        if not courses:
            st.info("You haven't been assigned to any courses in this subject yet.")
            return
        
        # Filter options
        st.subheader("Filter Courses")
        difficulties = ["All"] + content_manager.get_difficulty_levels()
        selected_difficulty = st.selectbox("Difficulty Level", difficulties)
        
        # Apply filters
        if selected_difficulty != "All":
            filtered_courses = [c for c in courses if c["difficulty"] == selected_difficulty]
        else:
            filtered_courses = courses
        
        if not filtered_courses:
            st.info(f"No courses found with difficulty: {selected_difficulty}")
            return
        
        # Display courses as cards
        st.subheader("Available Courses")
        
        # Use columns for better layout
        cols = st.columns(2)
        
        for i, course in enumerate(filtered_courses):
            with cols[i % 2]:
                display_content_card(course)
        
        # Check if a course is selected for viewing
        if "view_course_id" in st.session_state and st.session_state.view_course_id:
            display_content_viewer(st.session_state.view_course_id)
    
    elif page == "Profil":
        st.header("Profil Étudiant")
        
        # Display student information
        user = db.get_user_by_id(st.session_state.user_id)
        
        if user:
            st.subheader("Personal Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Username:** {user['username']}")
                st.write(f"**Full Name:** {user['full_name'] or 'Not provided'}")
            
            with col2:
                st.write(f"**Email:** {user['email'] or 'Not provided'}")
                st.write(f"**Phone:** {user['phone'] or 'Not provided'}")
            
            # Display assigned courses statistics
            st.subheader("Course Statistics")
            
            total_courses = len(db.get_user_courses(user['id']))
            courses_by_difficulty = {}
            
            for diff in content_manager.get_difficulty_levels():
                diff_courses = db.get_user_courses(user['id'], difficulty=diff)
                courses_by_difficulty[diff] = len(diff_courses)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Courses", total_courses)
            
            with col2:
                st.metric("Easy Courses", courses_by_difficulty.get("easy", 0))
            
            with col3:
                st.metric("Hard Courses", courses_by_difficulty.get("hard", 0))
            
            # Display recent activity
            st.subheader("Recent Activity")
            
            activities = db.get_activity_logs(limit=5, user_id=user['id'])
            
            if activities:
                for activity in activities:
                    st.write(f"**{activity['action']}** - {activity['timestamp']}")
            else:
                st.info("No recent activity.")
        else:
            st.error("Error loading profile information.")

def display_content_card(content):
    """Display a content card in the student dashboard."""
    card_id = f"course-{content['id']}"
    
    # Format content card with CSS classes for styling
    card_html = f"""
    <div class="content-card">
        <div class="content-card-header">
            <h3>{content['title']}</h3>
            <span class="difficulty-badge difficulty-{content['difficulty']}">{content['difficulty'].title()}</span>
        </div>
        <p><strong>Subject:</strong> {content['subject_name']}</p>
        <p><strong>Type:</strong> {content['content_type']}</p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Button to view course
    if st.button(f"View Course", key=f"view_{content['id']}"):
        st.session_state.view_course_id = content['id']
        st.session_state.current_course_id = content['id']
        st.rerun()

def display_content_viewer(content_id):
    """Display a detailed content viewer for the selected content."""
    content_manager = ContentManager()
    content = content_manager.get_content(content_id)
    
    if not content:
        st.error("Course content not found.")
        return
    
    # Create a back button
    if st.button("← Back to Courses"):
        st.session_state.view_course_id = None
        st.session_state.current_course_id = None
        st.rerun()
    
    st.title(content['title'])
    
    # Course metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Subject:** {content['subject_name']}")
    with col2:
        st.write(f"**Level:** {content['level_name']}")
    with col3:
        st.write(f"**Difficulty:** {content['difficulty'].title()}")
    
    # Course description
    if content['description']:
        try:
            description = json.loads(content['description'])
            if isinstance(description, dict) and "description" in description:
                st.markdown(description["description"])
        except:
            st.markdown(content['description'])
    
    # Display content based on type
    if content['content_type'] == "PDF":
        if content['content_path']:
            pdf_viewer(content['content_path'], title="Course Material")
        else:
            st.error("PDF file not found.")
    
    elif content['content_type'] == "YouTube":
        if content['youtube_url']:
            video_player(content['youtube_url'], title="Course Video")
        else:
            st.error("Video URL not found.")
    
    # Add a divider
    st.markdown("---")
    
    # Course notes or additional information
    st.subheader("Notes")
    st.info("Remember: All content on this platform is for your personal use only. "
            "Sharing or distribution of any materials is strictly prohibited.")

def download_content(content):
    """Provide download functionality for content."""
    # For security, we do not implement actual download functionality
    st.error("Content downloading is disabled for security reasons.")

def show_pdf_preview(encrypted_path):
    """Show a PDF preview using an iframe."""
    if encrypted_path:
        pdf_preview(encrypted_path)
    else:
        st.error("PDF file not available.")

def show_video_player(youtube_url):
    """Show a video player for YouTube content."""
    if youtube_url:
        video_thumbnail(youtube_url)
    else:
        st.error("Video URL not available.")