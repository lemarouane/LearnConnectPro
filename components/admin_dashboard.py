import streamlit as st
from database import Database
from content_manager import ContentManager
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import validate_file, save_uploaded_file, delete_file, format_size, apply_custom_css
import os
from datetime import datetime, timedelta
from components.pdf_viewer import pdf_preview
from components.video_player import video_thumbnail

def admin_dashboard():
    """Admin dashboard for managing content and users."""
    # Apply custom styling for admin dashboard
    st.markdown("""
    <style>
    .admin-header {
        color: #1565C0;
        padding: 1rem 0;
        border-bottom: 2px solid #1565C0;
        margin-bottom: 1.5rem;
    }
    .stat-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 0.25rem 0.75rem rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1565C0;
        margin: 0.5rem 0;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .admin-sidebar {
        padding: 1rem;
        border-radius: 5px;
    }
    .admin-sidebar .css-1d391kg {
        background-color: #f0f2f6;
    }
    .menu-item {
        margin-bottom: 0.5rem;
        padding: 0.75rem;
        border-radius: 5px;
        transition: background-color 0.2s;
    }
    .menu-item:hover {
        background-color: #e9ecef;
    }
    .admin-welcome {
        font-size: 1.2rem;
        color: #495057;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="admin-header">Tableau de Bord Administrateur</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="admin-welcome">Bienvenue, Admin {st.session_state.full_name or st.session_state.username}!</p>', unsafe_allow_html=True)
    
    # Custom modern sidebar styling
    st.sidebar.markdown("""
    <style>
    .sidebar-header {
        color: #ffffff;
        background: linear-gradient(135deg, #1565C0, #0D47A1);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .admin-info {
        text-align: center;
        margin-bottom: 25px;
        color: #0D47A1;
        font-weight: 600;
        font-size: 16px;
    }
    
    /* Style for buttons in the sidebar */
    .nav-container {
        margin-bottom: 80px;  /* Space for footer */
    }
    
    .stButton > button {
        text-align: left !important;
        margin-bottom: 5px;
        border-radius: 7px;
        transition: all 0.3s ease;
        font-weight: 500;
        display: flex;
        align-items: center;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background-color: #1565C0;
        color: white;
    }
    
    .stButton > button[data-baseweb="button"][kind="primary"]:hover {
        background-color: #0D47A1;
    }
    
    .stButton > button[data-baseweb="button"][kind="secondary"] {
        background-color: #f0f7ff;
        color: #333;
        border: 1px solid #e0e0e0;
    }
    
    .stButton > button[data-baseweb="button"][kind="secondary"]:hover {
        background-color: #e3f2fd;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Modern sidebar header
    st.sidebar.markdown('<div class="sidebar-header"><h2>Plateforme E-Learning</h2></div>', unsafe_allow_html=True)
    
    # Admin info without profile image
    st.sidebar.markdown(f'<div class="admin-info">{st.session_state.full_name or st.session_state.username}<br><small>Administrateur</small></div>', unsafe_allow_html=True)
    
    # Create navigation items with icons
    nav_options = [
        ("Aperçu du Tableau de Bord", "📊"),
        ("Gestion du Contenu", "📚"),
        ("Gestion des Utilisateurs", "👥"),
        ("Gestion des Niveaux", "🏆"),
        ("Gestion des Matières", "📝"),
        ("Journaux d'Activité", "📋")
    ]
    
    # Hidden radio button for navigation state management
    admin_page = st.sidebar.radio(
        "Navigation",
        [option[0] for option in nav_options],
        label_visibility="collapsed"
    )
    
    # Custom navigation using standard Streamlit components with improved styling
    st.sidebar.markdown("<div class='nav-container'>", unsafe_allow_html=True)
    
    for i, (option, icon) in enumerate(nav_options):
        if st.sidebar.button(
            f"{icon} {option}",
            key=f"nav_{i}",
            on_click=lambda o=option: st.session_state.update({"admin_page": o}),
            use_container_width=True,
            type="primary" if admin_page == option else "secondary"
        ):
            admin_page = option
            
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    # Make sure admin_page is always a session variable
    if "admin_page" in st.session_state:
        admin_page = st.session_state.admin_page
        
    # Footer with extra space to prevent overlap
    st.sidebar.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style="position: fixed; bottom: 20px; left: 20px; right: 20px; text-align: center; font-size: 12px; color: #777; padding-top: 10px; border-top: 1px solid #eee;">
        <div>Plateforme E-Learning Zouhair</div>
        <div>© 2025 Tous Droits Réservés</div>
    </div>
    """, unsafe_allow_html=True)
    
    if admin_page == "Aperçu du Tableau de Bord":
        dashboard_overview()
    elif admin_page == "Gestion du Contenu":
        content_management()
    elif admin_page == "Gestion des Utilisateurs":
        user_management()
    elif admin_page == "Gestion des Niveaux":
        level_management()
    elif admin_page == "Gestion des Matières":
        subject_management()
    elif admin_page == "Journaux d'Activité":
        activity_logs()
        
def dashboard_overview():
    """Dashboard overview with statistics and charts."""
    st.header("Aperçu de la Plateforme")
    
    db = Database()
    
    # Get statistics
    total_students = len(db.get_all_users(role="student"))
    validated_students = len(db.get_all_users(role="student", validated=1))
    total_courses = len(db.get_all_courses())
    
    # Get levels and subjects statistics
    levels = db.get_all_levels()
    total_levels = len(levels)
    subjects = db.get_all_subjects()
    total_subjects = len(subjects)
    
    # Recent activity
    recent_activities = db.get_activity_logs(limit=5)
    
    # Display statistics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Total Étudiants</div>
            <div class="stat-value">{}</div>
            <div>({} validés)</div>
        </div>
        """.format(total_students, validated_students), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Total Cours</div>
            <div class="stat-value">{}</div>
            <div>Ressources Éducatives</div>
        </div>
        """.format(total_courses), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Niveaux</div>
            <div class="stat-value">{}</div>
            <div>Niveaux Éducatifs</div>
        </div>
        """.format(total_levels), unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Matières</div>
            <div class="stat-value">{}</div>
            <div>Domaines de Matières</div>
        </div>
        """.format(total_subjects), unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Content distribution by difficulty
    st.subheader("Distribution du Contenu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create data for content by difficulty
        all_courses = db.get_all_courses()
        difficulty_counts = {}
        
        for course in all_courses:
            difficulty = course['difficulty']
            if difficulty in difficulty_counts:
                difficulty_counts[difficulty] += 1
            else:
                difficulty_counts[difficulty] = 1
        
        if difficulty_counts:
            # Create a pie chart
            fig_difficulty = px.pie(
                names=list(difficulty_counts.keys()),
                values=list(difficulty_counts.values()),
                title="Contenu par Niveau de Difficulté",
                color_discrete_sequence=px.colors.sequential.Blues
            )
            fig_difficulty.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_difficulty, use_container_width=True)
        else:
            st.info("Aucune donnée disponible pour le graphique de distribution par difficulté.")
    
    with col2:
        # Create data for content by type
        content_type_counts = {"PDF": 0, "YouTube": 0}
        
        for course in all_courses:
            content_type = course['content_type']
            if content_type in content_type_counts:
                content_type_counts[content_type] += 1
        
        if all_courses:
            # Create a bar chart
            fig_type = px.bar(
                x=list(content_type_counts.keys()),
                y=list(content_type_counts.values()),
                title="Contenu par Type",
                labels={'x': 'Type de Contenu', 'y': 'Nombre'},
                color=list(content_type_counts.values()),
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.info("Aucune donnée disponible pour le graphique de distribution par type.")
    
    # User activity timeline
    st.subheader("Activités Récentes")
    
    # Create DataTable for recent activities
    if recent_activities:
        activity_df = pd.DataFrame(recent_activities)
        
        # Format timestamp for better readability
        activity_df['formatted_time'] = pd.to_datetime(activity_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Get usernames for user_ids
        usernames = {}
        for activity in recent_activities:
            if activity['user_id'] not in usernames:
                user = db.get_user_by_id(activity['user_id'])
                if user:
                    usernames[activity['user_id']] = user['username']
                else:
                    usernames[activity['user_id']] = f"User {activity['user_id']}"
        
        activity_df['username'] = activity_df['user_id'].map(usernames)
        
        # Display as a styled table
        st.dataframe(
            activity_df[['username', 'action', 'formatted_time']].rename(
                columns={'username': 'User', 'action': 'Action', 'formatted_time': 'Timestamp'}
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aucune activité récente à afficher.")

def content_management():
    """Content management section of the admin dashboard."""
    st.header("Gestion du Contenu")
    
    # Tabs for different content management functions
    tab1, tab2 = st.tabs(["Ajouter du Contenu", "Gérer le Contenu"])
    
    with tab1:
        add_content_form()
    
    with tab2:
        view_content_table()
        
        # Check if content details view is requested
        if "view_content_id" in st.session_state and st.session_state.view_content_id:
            display_content_details(st.session_state.view_content_id)

def add_content_form():
    """Form for adding new content."""
    st.subheader("Ajouter Nouveau Contenu")
    
    db = Database()
    content_manager = ContentManager()
    
    # Get subjects and levels for dropdown
    subjects = db.get_all_subjects()
    
    if not subjects:
        st.warning("Please add levels and subjects before adding content.")
        return
    
    # Convert to options for the form
    subject_names = [f"{s['name']} ({s['level_name']})" for s in subjects]
    subject_ids = [s['id'] for s in subjects]
    
    with st.form("add_content_form"):
        st.markdown("### Content Information")
        
        title = st.text_input("Course Title", placeholder="Enter a descriptive title")
        
        # Subject/Level selection
        subject_index = st.selectbox(
            "Subject", 
            range(len(subject_names)), 
            format_func=lambda i: subject_names[i]
        )
        selected_subject_id = subject_ids[subject_index]
        
        # Get level ID from the selected subject
        selected_subject = next((s for s in subjects if s['id'] == selected_subject_id), None)
        selected_level_id = selected_subject['level_id'] if selected_subject else None
        
        # Difficulty selection
        difficulty = st.selectbox(
            "Difficulty Level",
            content_manager.get_difficulty_levels()
        )
        
        # Content type selection
        content_type = st.selectbox("Content Type", ["PDF", "YouTube"])
        
        # Content upload/input based on type
        if content_type == "PDF":
            uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
            youtube_url = None
        else:  # YouTube
            uploaded_file = None
            youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        
        # Description
        description = st.text_area("Description (optional)", placeholder="Enter course description...")
        
        # Submit button
        submit = st.form_submit_button("Add Content")
        
        if submit:
            if not title:
                st.error("Please enter a course title.")
                return
            
            if content_type == "PDF" and not uploaded_file:
                st.error("Please upload a PDF file.")
                return
            
            if content_type == "YouTube" and not youtube_url:
                st.error("Please enter a YouTube URL.")
                return
            
            # Process the content based on type
            try:
                metadata = {"description": description} if description else {}
                
                if content_type == "PDF":
                    # Validate the file
                    is_valid, message = validate_file(uploaded_file, [".pdf"])
                    if not is_valid:
                        st.error(message)
                        return
                    
                    # Add to content manager
                    content_id = content_manager.add_content(
                        file_obj=uploaded_file,
                        title=title,
                        content_type="PDF",
                        metadata=metadata,
                        difficulty=difficulty,
                        category=selected_subject_id,
                        user_id=st.session_state.user_id
                    )
                    
                else:  # YouTube
                    # Add to content manager
                    content_id = content_manager.add_content(
                        file_obj=youtube_url,
                        title=title,
                        content_type="YouTube",
                        metadata=metadata,
                        difficulty=difficulty,
                        category=selected_subject_id,
                        user_id=st.session_state.user_id
                    )
                
                # Update level_id
                if content_id and selected_level_id:
                    content_manager.update_content(content_id, level_id=selected_level_id)
                
                if content_id:
                    st.success(f"Content added successfully with ID: {content_id}")
                    # Log activity
                    db.log_activity(
                        st.session_state.user_id,
                        f"Added {content_type} content: {title}"
                    )
                else:
                    st.error("Failed to add content. Please try again.")
                
            except Exception as e:
                st.error(f"Error adding content: {str(e)}")

def view_content_table():
    """Display a table of existing content."""
    st.subheader("Gérer le Contenu Existant")
    
    db = Database()
    content_manager = ContentManager()
    
    # Get subjects and levels for filtering
    subjects = db.get_all_subjects()
    levels = db.get_all_levels()
    
    # Filtering options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Level filter
        level_options = ["All Levels"] + [level["name"] for level in levels]
        selected_level = st.selectbox("Filter by Level", level_options)
        selected_level_id = next((level["id"] for level in levels if level["name"] == selected_level), None)
    
    with col2:
        # Subject filter (depends on level)
        if selected_level == "All Levels":
            subject_filter_list = subjects
        else:
            subject_filter_list = [s for s in subjects if s["level_id"] == selected_level_id]
        
        subject_options = ["All Subjects"] + [subject["name"] for subject in subject_filter_list]
        selected_subject = st.selectbox("Filter by Subject", subject_options)
        selected_subject_id = next((subject["id"] for subject in subject_filter_list if subject["name"] == selected_subject), None)
    
    with col3:
        # Difficulty filter
        difficulty_options = ["All Difficulties"] + content_manager.get_difficulty_levels()
        selected_difficulty = st.selectbox("Filter by Difficulty", difficulty_options)
    
    # Get courses based on filters
    if selected_level == "All Levels":
        filtered_level_id = None
    else:
        filtered_level_id = selected_level_id
    
    if selected_subject == "All Subjects":
        filtered_subject_id = None
    else:
        filtered_subject_id = selected_subject_id
    
    if selected_difficulty == "All Difficulties":
        filtered_difficulty = None
    else:
        filtered_difficulty = selected_difficulty
    
    # Get filtered courses
    try:
        courses = db.get_all_courses(
            subject_id=filtered_subject_id,
            level_id=filtered_level_id,
            difficulty=filtered_difficulty
        )
    except Exception as e:
        st.error(f"Error loading courses: {str(e)}")
        courses = []
    
    if not courses:
        st.info("No courses found with the selected filters.")
        return
    
    # Display courses in a table with actions
    st.write(f"Showing {len(courses)} courses")
    
    # Custom styling for the course list
    st.markdown("""
    <style>
    .course-item {
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f9f9f9;
    }
    .course-title {
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 5px;
    }
    .course-meta {
        color: #666;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # List courses with action buttons
    for course in courses:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class="course-item">
                <div class="course-title">{course['title']}</div>
                <div class="course-meta">
                    <strong>Subject:</strong> {course['subject_name']} | 
                    <strong>Level:</strong> {course['level_name']} | 
                    <strong>Difficulty:</strong> {course['difficulty']} | 
                    <strong>Type:</strong> {course['content_type']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            if st.button("View/Edit", key=f"view_{course['id']}"):
                st.session_state.view_content_id = course['id']
                st.rerun()

def display_content_details(content_id):
    """Display details of selected content and provide management options."""
    db = Database()
    content_manager = ContentManager()
    
    content = content_manager.get_content(content_id)
    
    if not content:
        st.error("Content not found.")
        return
    
    # Section header
    st.markdown("---")
    st.subheader(f"Content Details: {content['title']}")
    
    # Back button
    if st.button("← Back to Content List"):
        st.session_state.view_content_id = None
        st.rerun()
    
    # Content information
    col1, col2 = st.columns(2)
    
    with col1:
        # Content details 
        st.markdown(f"**Title:** {content['title']}")
        st.markdown(f"**Type:** {content['content_type']}")
        st.markdown(f"**Difficulty:** {content['difficulty']}")
        st.markdown(f"**Subject:** {content['subject_name']}")
        st.markdown(f"**Level:** {content['level_name']}")
        
        # Description
        if content['description']:
            try:
                description = json.loads(content['description'])
                if isinstance(description, dict) and "description" in description:
                    st.markdown("**Description:**")
                    st.markdown(description["description"])
            except:
                st.markdown("**Description:**")
                st.markdown(content['description'])
        
        # Edit form
        with st.expander("Edit Content"):
            with st.form("edit_content_form"):
                # Get subjects and levels for dropdowns
                subjects = db.get_all_subjects()
                
                subject_names = [f"{s['name']} ({s['level_name']})" for s in subjects]
                subject_ids = [s['id'] for s in subjects]
                
                current_subject_index = next((i for i, sid in enumerate(subject_ids) if sid == content['subject_id']), 0)
                
                # Form fields
                new_title = st.text_input("Title", value=content['title'])
                
                new_subject_index = st.selectbox(
                    "Subject", 
                    range(len(subject_names)), 
                    format_func=lambda i: subject_names[i],
                    index=current_subject_index
                )
                new_subject_id = subject_ids[new_subject_index]
                
                selected_subject = next((s for s in subjects if s['id'] == new_subject_id), None)
                new_level_id = selected_subject['level_id'] if selected_subject else None
                
                new_difficulty = st.selectbox(
                    "Difficulty",
                    content_manager.get_difficulty_levels(),
                    index=content_manager.get_difficulty_levels().index(content['difficulty'])
                )
                
                # Description 
                try:
                    desc_value = json.loads(content['description']).get("description", "") if content['description'] else ""
                except:
                    desc_value = content['description'] or ""
                    
                new_description = st.text_area("Description", value=desc_value)
                
                # Submit button
                submit_edit = st.form_submit_button("Save Changes")
                
                if submit_edit:
                    # Update content
                    updated = content_manager.update_content(
                        content_id,
                        title=new_title,
                        difficulty=new_difficulty,
                        metadata={"description": new_description},
                        subject_id=new_subject_id,
                        level_id=new_level_id
                    )
                    
                    if updated:
                        st.success("Content updated successfully.")
                        # Log activity
                        db.log_activity(
                            st.session_state.user_id,
                            f"Updated content: {new_title}"
                        )
                        st.rerun()
                    else:
                        st.error("Failed to update content.")
    
    with col2:
        # Content preview based on type
        st.markdown("**Preview:**")
        
        if content['content_type'] == "PDF" and content['content_path']:
            # PDF preview
            if os.path.exists(content['content_path']):
                pdf_preview(content['content_path'])
            else:
                st.error("PDF file not found.")
        
        elif content['content_type'] == "YouTube" and content['youtube_url']:
            # YouTube preview
            video_thumbnail(content['youtube_url'])
        
        # Student assignment section
        st.markdown("---")
        st.markdown("**Assign to Students:**")
        
        # Get unassigned students
        all_students = db.get_all_users(role="student", validated=1)
        assigned_students = db.get_users_assigned_to_course(content_id)
        
        assigned_ids = [student['id'] for student in assigned_students]
        unassigned_students = [student for student in all_students if student['id'] not in assigned_ids]
        
        # Display assigned students with option to unassign
        if assigned_students:
            st.markdown("**Currently Assigned:**")
            
            for student in assigned_students:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"{student['full_name']} ({student['username']})")
                with cols[1]:
                    if st.button("Unassign", key=f"unassign_{student['id']}"):
                        if content_manager.unassign_from_user(content_id, student['id']):
                            st.success(f"Unassigned {student['username']} from this content.")
                            # Log activity
                            db.log_activity(
                                st.session_state.user_id,
                                f"Unassigned student {student['username']} from content ID {content_id}"
                            )
                            st.rerun()
                        else:
                            st.error("Failed to unassign student.")
        else:
            st.info("No students currently assigned to this content.")
        
        # Display unassigned students with option to assign
        if unassigned_students:
            st.markdown("**Available Students:**")
            
            for student in unassigned_students:
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"{student['full_name']} ({student['username']})")
                with cols[1]:
                    if st.button("Assign", key=f"assign_{student['id']}"):
                        if content_manager.assign_to_user(content_id, student['id']):
                            st.success(f"Assigned {student['username']} to this content.")
                            # Log activity
                            db.log_activity(
                                st.session_state.user_id,
                                f"Assigned student {student['username']} to content ID {content_id}"
                            )
                            st.rerun()
                        else:
                            st.error("Failed to assign student.")
        else:
            st.info("No available students to assign.")
    
    # Delete content section
    st.markdown("---")
    delete_col1, delete_col2 = st.columns([3, 1])
    
    with delete_col1:
        st.warning("Deleting content will permanently remove it and all its assignments.")
    
    with delete_col2:
        # Two-step deletion to prevent accidental clicks
        if "confirm_delete" not in st.session_state:
            st.session_state.confirm_delete = False
            
        if not st.session_state.confirm_delete:
            if st.button("Delete Content"):
                st.session_state.confirm_delete = True
                st.rerun()
        else:
            if st.button("Cancel"):
                st.session_state.confirm_delete = False
                st.rerun()
            
            if st.button("Confirm Delete", type="primary"):
                if content_manager.delete_content(content_id):
                    # Log activity
                    db.log_activity(
                        st.session_state.user_id,
                        f"Deleted content: {content['title']}"
                    )
                    
                    st.session_state.view_content_id = None
                    st.session_state.confirm_delete = False
                    st.success("Content deleted successfully.")
                    st.rerun()
                else:
                    st.error("Failed to delete content.")

def user_management():
    """User management section of the admin dashboard."""
    st.header("Gestion des Utilisateurs")
    
    db = Database()
    
    # Custom styling for user management
    st.markdown("""
    <style>
    .user-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .user-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .user-card h3 {
        color: #1565C0;
        margin-top: 0;
        margin-bottom: 10px;
    }
    .validated-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
        margin-left: 10px;
    }
    .validated-true {
        background-color: #d4edda;
        color: #155724;
    }
    .validated-false {
        background-color: #f8d7da;
        color: #721c24;
    }
    .action-button {
        width: 100%;
        margin-bottom: 5px;
    }
    .user-table {
        width: 100%;
        border-collapse: collapse;
    }
    .user-table th {
        background-color: #f0f2f6;
        padding: 8px 12px;
        text-align: left;
        border-bottom: 2px solid #dee2e6;
    }
    .user-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #dee2e6;
    }
    .user-table tr:hover {
        background-color: #f8f9fa;
    }
    .data-table {
        font-family: Arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 20px;
    }
    .data-table th {
        background-color: #1565C0;
        color: white;
        padding: 12px;
        text-align: left;
    }
    .data-table td {
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }
    .data-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .data-table tr:hover {
        background-color: #f1f1f1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tabs for different user management functions
    tab1, tab2 = st.tabs(["Pending Validations", "All Users"])
    
    with tab1:
        st.subheader("Students Awaiting Validation")
        
        # Get pending students
        pending_students = db.get_all_users(role="student", validated=0)
        
        if not pending_students:
            st.info("No students pending validation.")
        else:
            st.write(f"{len(pending_students)} students waiting for validation")
            
            # Create a DataFrame for better table display
            if pending_students:
                pending_df = pd.DataFrame(pending_students)
                pending_df['full_name'] = pending_df['full_name'].fillna(pending_df['username'])
                pending_df['email'] = pending_df['email'].fillna('Not provided')
                pending_df['phone'] = pending_df['phone'].fillna('Not provided')
                
                # Display in a table
                st.dataframe(
                    pending_df[['username', 'full_name', 'email', 'phone', 'created_at']].rename(
                        columns={
                            'username': 'Username',
                            'full_name': 'Full Name',
                            'email': 'Email',
                            'phone': 'Phone',
                            'created_at': 'Registered On'
                        }
                    ),
                    use_container_width=True,
                    hide_index=True
                )
            
            # Action cards for each pending student
            for student in pending_students:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="user-card">
                            <h3>{student['full_name'] or student['username']}</h3>
                            <p><strong>Username:</strong> {student['username']}</p>
                            <p><strong>Email:</strong> {student['email'] or 'Not provided'}</p>
                            <p><strong>Phone:</strong> {student['phone'] or 'Not provided'}</p>
                            <p><strong>Registered:</strong> {student['created_at']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        if st.button("✅ Validate", key=f"validate_{student['id']}"):
                            if db.validate_user(student['id'], validate=True):
                                # Log activity
                                db.log_activity(
                                    st.session_state.user_id,
                                    f"Validated student account: {student['username']}"
                                )
                                st.success(f"User {student['username']} validated successfully.")
                                st.rerun()
                            else:
                                st.error("Failed to validate user.")
                        
                        if st.button("🗑️ Delete", key=f"delete_pending_{student['id']}"):
                            if db.delete_user(student['id']):
                                # Log activity
                                db.log_activity(
                                    st.session_state.user_id,
                                    f"Deleted pending student account: {student['username']}"
                                )
                                st.success(f"User {student['username']} deleted successfully.")
                                st.rerun()
                            else:
                                st.error("Failed to delete user.")
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
    
    with tab2:
        st.subheader("All Users")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            role_filter = st.selectbox("Filter by Role", ["All", "student", "admin"])
        
        with col2:
            validation_filter = st.selectbox("Filter by Validation", ["All", "Validated", "Not Validated"])
        
        # Apply filters
        if role_filter == "All":
            role_param = None
        else:
            role_param = role_filter
        
        if validation_filter == "All":
            validation_param = None
        elif validation_filter == "Validated":
            validation_param = 1
        else:
            validation_param = 0
        
        # Get filtered users
        users = db.get_all_users(role=role_param, validated=validation_param)
        
        if not users:
            st.info("No users found with the selected filters.")
        else:
            st.write(f"Showing {len(users)} users")
            
            # Create a DataFrame for all users
            users_df = pd.DataFrame(users)
            users_df['full_name'] = users_df['full_name'].fillna(users_df['username'])
            users_df['email'] = users_df['email'].fillna('Not provided')
            users_df['phone'] = users_df['phone'].fillna('Not provided')
            users_df['role'] = users_df['role'].apply(lambda x: x.title())
            users_df['validated'] = users_df['validated'].apply(
                lambda x: "✅ Validated" if x else "❌ Not Validated"
            )
            
            # Display in a table
            st.dataframe(
                users_df[['username', 'full_name', 'role', 'validated', 'email', 'phone', 'created_at']].rename(
                    columns={
                        'username': 'Username', 
                        'full_name': 'Full Name',
                        'role': 'Role',
                        'validated': 'Status',
                        'email': 'Email',
                        'phone': 'Phone',
                        'created_at': 'Registered On'
                    }
                ),
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("""
            <div style="padding: 10px 15px; background-color: #f0f7ff; border-left: 4px solid #1565C0; margin: 20px 0; border-radius: 4px;">
                <strong>User Management:</strong> Select a user card below to manage individual users.
            </div>
            """, unsafe_allow_html=True)
            
            for user in users:
                # Create a card for each user
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    validation_status = "✅ Validated" if user['validated'] else "❌ Not Validated"
                    
                    st.markdown(f"""
                    <div class="user-card">
                        <h3>{user['full_name'] or user['username']}</h3>
                        <p><strong>Username:</strong> {user['username']} 
                           <span class="validated-badge validated-{str(user['validated']).lower()}">{validation_status}</span></p>
                        <p><strong>Role:</strong> {user['role'].title()}</p>
                        <p><strong>Email:</strong> {user['email'] or 'Not provided'}</p>
                        <p><strong>Phone:</strong> {user['phone'] or 'Not provided'}</p>
                        <p><strong>Registered:</strong> {user['created_at']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Skip for the current admin user
                    if user['id'] != st.session_state.user_id:
                        if user['validated']:
                            if st.button("Revoke", key=f"revoke_{user['id']}"):
                                if db.validate_user(user['id'], validate=False):
                                    # Log activity
                                    db.log_activity(
                                        st.session_state.user_id,
                                        f"Revoked validation for user: {user['username']}"
                                    )
                                    st.success(f"User {user['username']} validation revoked.")
                                    st.rerun()
                                else:
                                    st.error("Failed to revoke user validation.")
                        else:
                            if st.button("Validate", key=f"val_all_{user['id']}"):
                                if db.validate_user(user['id'], validate=True):
                                    # Log activity
                                    db.log_activity(
                                        st.session_state.user_id,
                                        f"Validated user account: {user['username']}"
                                    )
                                    st.success(f"User {user['username']} validated successfully.")
                                    st.rerun()
                                else:
                                    st.error("Failed to validate user.")
                        
                        # Don't show delete button for the current admin user
                        if st.button("Delete", key=f"del_all_{user['id']}"):
                            if db.delete_user(user['id']):
                                # Log activity
                                db.log_activity(
                                    st.session_state.user_id,
                                    f"Deleted user account: {user['username']}"
                                )
                                st.success(f"User {user['username']} deleted successfully.")
                                st.rerun()
                            else:
                                st.error("Failed to delete user.")
                    else:
                        st.write("Current Admin User")
                
                # Add an expander for user assignments
                if user['role'] == "student":
                    with st.expander("View/Manage Assignments"):
                        st.markdown("#### User Assignments")
                        
                        # Get user's assignments
                        user_levels = db.get_user_levels(user['id'])
                        user_subjects = db.get_user_subjects(user['id'])
                        user_courses = db.get_user_courses(user['id'])
                        
                        # Levels tab
                        if st.button("Manage Levels", key=f"manage_levels_{user['id']}"):
                            st.session_state.manage_user_levels = user['id']
                            st.rerun()
                        
                        if "manage_user_levels" in st.session_state and st.session_state.manage_user_levels == user['id']:
                            st.markdown("##### Assigned Levels")
                            
                            # Display currently assigned levels with unassign option
                            if user_levels:
                                for level in user_levels:
                                    cols = st.columns([3, 1])
                                    with cols[0]:
                                        st.write(f"{level['name']}")
                                    with cols[1]:
                                        if st.button("Unassign", key=f"unassign_level_{user['id']}_{level['id']}"):
                                            if db.unassign_level_from_user(user['id'], level['id']):
                                                # Log activity
                                                db.log_activity(
                                                    st.session_state.user_id,
                                                    f"Unassigned level {level['name']} from user {user['username']}"
                                                )
                                                st.success(f"Level {level['name']} unassigned from user.")
                                                st.rerun()
                                            else:
                                                st.error("Failed to unassign level.")
                            else:
                                st.info("No levels assigned to this user.")
                            
                            # Display available levels to assign
                            st.markdown("##### Available Levels")
                            all_levels = db.get_all_levels()
                            assigned_level_ids = [level['id'] for level in user_levels]
                            unassigned_levels = [level for level in all_levels if level['id'] not in assigned_level_ids]
                            
                            if unassigned_levels:
                                for level in unassigned_levels:
                                    cols = st.columns([3, 1])
                                    with cols[0]:
                                        st.write(f"{level['name']}")
                                    with cols[1]:
                                        if st.button("Assign", key=f"assign_level_{user['id']}_{level['id']}"):
                                            if db.assign_level_to_user(user['id'], level['id']):
                                                # Log activity
                                                db.log_activity(
                                                    st.session_state.user_id,
                                                    f"Assigned level {level['name']} to user {user['username']}"
                                                )
                                                st.success(f"Level {level['name']} assigned to user.")
                                                st.rerun()
                                            else:
                                                st.error("Failed to assign level.")
                            else:
                                st.info("No available levels to assign.")
                                
                            # Close button
                            if st.button("Close Level Management", key=f"close_levels_{user['id']}"):
                                st.session_state.manage_user_levels = None
                                st.rerun()
                        
                        # Subjects tab
                        if st.button("Manage Subjects", key=f"manage_subjects_{user['id']}"):
                            st.session_state.manage_user_subjects = user['id']
                            st.rerun()
                        
                        if "manage_user_subjects" in st.session_state and st.session_state.manage_user_subjects == user['id']:
                            st.markdown("##### Assigned Subjects")
                            
                            # Display currently assigned subjects with unassign option
                            if user_subjects:
                                for subject in user_subjects:
                                    cols = st.columns([3, 1])
                                    with cols[0]:
                                        st.write(f"{subject['name']} ({subject['level_name']})")
                                    with cols[1]:
                                        if st.button("Unassign", key=f"unassign_subject_{user['id']}_{subject['id']}"):
                                            if db.unassign_subject_from_user(user['id'], subject['id']):
                                                # Log activity
                                                db.log_activity(
                                                    st.session_state.user_id,
                                                    f"Unassigned subject {subject['name']} from user {user['username']}"
                                                )
                                                st.success(f"Subject {subject['name']} unassigned from user.")
                                                st.rerun()
                                            else:
                                                st.error("Failed to unassign subject.")
                            else:
                                st.info("No subjects assigned to this user.")
                            
                            # Display available subjects to assign (only from assigned levels)
                            st.markdown("##### Available Subjects")
                            
                            # Get all subjects from user's assigned levels
                            assigned_level_ids = [level['id'] for level in user_levels]
                            all_level_subjects = []
                            
                            for level_id in assigned_level_ids:
                                level_subjects = db.get_all_subjects(level_id=level_id)
                                all_level_subjects.extend(level_subjects)
                            
                            # Filter out already assigned subjects
                            assigned_subject_ids = [subject['id'] for subject in user_subjects]
                            unassigned_subjects = [subject for subject in all_level_subjects if subject['id'] not in assigned_subject_ids]
                            
                            if unassigned_subjects:
                                for subject in unassigned_subjects:
                                    cols = st.columns([3, 1])
                                    with cols[0]:
                                        st.write(f"{subject['name']} ({subject['level_name']})")
                                    with cols[1]:
                                        if st.button("Assign", key=f"assign_subject_{user['id']}_{subject['id']}"):
                                            if db.assign_subject_to_user(user['id'], subject['id']):
                                                # Log activity
                                                db.log_activity(
                                                    st.session_state.user_id,
                                                    f"Assigned subject {subject['name']} to user {user['username']}"
                                                )
                                                st.success(f"Subject {subject['name']} assigned to user.")
                                                st.rerun()
                                            else:
                                                st.error("Failed to assign subject.")
                            else:
                                if user_levels:
                                    st.info("No available subjects to assign from the user's assigned levels.")
                                else:
                                    st.warning("Please assign levels to this user first.")
                                    
                            # Close button
                            if st.button("Close Subject Management", key=f"close_subjects_{user['id']}"):
                                st.session_state.manage_user_subjects = None
                                st.rerun()
                        
                        # Courses tab
                        if st.button("Manage Courses", key=f"manage_courses_{user['id']}"):
                            st.session_state.manage_user_courses = user['id']
                            st.rerun()
                        
                        if "manage_user_courses" in st.session_state and st.session_state.manage_user_courses == user['id']:
                            st.markdown("##### Assigned Courses")
                            
                            # Display currently assigned courses with unassign option
                            if user_courses:
                                for course in user_courses:
                                    cols = st.columns([3, 1])
                                    with cols[0]:
                                        st.write(f"{course['title']} - {course['subject_name']} ({course['difficulty']})")
                                    with cols[1]:
                                        if st.button("Unassign", key=f"unassign_course_{user['id']}_{course['id']}"):
                                            if db.unassign_course_from_user(user['id'], course['id']):
                                                # Log activity
                                                db.log_activity(
                                                    st.session_state.user_id,
                                                    f"Unassigned course {course['title']} from user {user['username']}"
                                                )
                                                st.success(f"Course {course['title']} unassigned from user.")
                                                st.rerun()
                                            else:
                                                st.error("Failed to unassign course.")
                            else:
                                st.info("No courses assigned to this user.")
                            
                            # Display available courses to assign (only from assigned subjects)
                            st.markdown("##### Available Courses")
                            
                            # Get subject IDs that the user is assigned to
                            assigned_subject_ids = [subject['id'] for subject in user_subjects]
                            
                            # Get all courses from those subjects
                            all_available_courses = []
                            for subject_id in assigned_subject_ids:
                                subject_courses = db.get_all_courses(subject_id=subject_id)
                                all_available_courses.extend(subject_courses)
                            
                            # Filter out already assigned courses
                            assigned_course_ids = [course['id'] for course in user_courses]
                            unassigned_courses = [course for course in all_available_courses if course['id'] not in assigned_course_ids]
                            
                            if unassigned_courses:
                                for course in unassigned_courses:
                                    cols = st.columns([3, 1])
                                    with cols[0]:
                                        st.write(f"{course['title']} - {course['subject_name']} ({course['difficulty']})")
                                    with cols[1]:
                                        if st.button("Assign", key=f"assign_course_{user['id']}_{course['id']}"):
                                            if db.assign_course_to_user(user['id'], course['id']):
                                                # Log activity
                                                db.log_activity(
                                                    st.session_state.user_id,
                                                    f"Assigned course {course['title']} to user {user['username']}"
                                                )
                                                st.success(f"Course {course['title']} assigned to user.")
                                                st.rerun()
                                            else:
                                                st.error("Failed to assign course.")
                            else:
                                if user_subjects:
                                    st.info("No available courses to assign from the user's assigned subjects.")
                                else:
                                    st.warning("Please assign subjects to this user first.")
                                    
                            # Close button
                            if st.button("Close Course Management", key=f"close_courses_{user['id']}"):
                                st.session_state.manage_user_courses = None
                                st.rerun()
                
                st.markdown("---")

def level_management():
    """Level management section of the admin dashboard."""
    st.header("Gestion des Niveaux")
    
    db = Database()
    
    # Tabs for different level management functions
    tab1, tab2 = st.tabs(["Add Level", "Manage Levels"])
    
    with tab1:
        st.subheader("Add New Level")
        
        with st.form("add_level_form"):
            level_name = st.text_input("Level Name", placeholder="e.g., Bac+2, Bac+3")
            level_description = st.text_area("Description (optional)", placeholder="Brief description of this level...")
            submit = st.form_submit_button("Add Level")
            
            if submit:
                if not level_name:
                    st.error("Please enter a level name.")
                else:
                    level_id = db.add_level(level_name, level_description)
                    if level_id:
                        # Log activity
                        db.log_activity(
                            st.session_state.user_id,
                            f"Added new level: {level_name}"
                        )
                        st.success(f"Level '{level_name}' added successfully.")
                        st.rerun()
                    else:
                        st.error("Failed to add level. Name may already exist.")
    
    with tab2:
        st.subheader("Manage Existing Levels")
        
        levels = db.get_all_levels()
        
        if not levels:
            st.info("No levels found. Please add a level first.")
        else:
            for level in levels:
                with st.expander(f"{level['name']}"):
                    # Display level details
                    st.markdown(f"**Description:** {level['description'] or 'No description provided'}")
                    st.markdown(f"**Created at:** {level['created_at']}")
                    
                    # Get usage statistics
                    subjects_count = len(db.get_all_subjects(level_id=level['id']))
                    students_count = len(db.get_users_assigned_to_level(level['id']))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Subjects", subjects_count)
                    with col2:
                        st.metric("Assigned Students", students_count)
                    
                    # Edit form
                    with st.form(f"edit_level_{level['id']}"):
                        new_name = st.text_input("Level Name", value=level['name'])
                        new_description = st.text_area("Description", value=level['description'] or "")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            update = st.form_submit_button("Update Level")
                        
                        if update:
                            if not new_name:
                                st.error("Level name cannot be empty.")
                            else:
                                updated = db.update_level(level['id'], new_name, new_description)
                                if updated:
                                    # Log activity
                                    db.log_activity(
                                        st.session_state.user_id,
                                        f"Updated level: {level['name']} to {new_name}"
                                    )
                                    st.success("Level updated successfully.")
                                    st.rerun()
                                else:
                                    st.error("Failed to update level. Name may already exist.")
                    
                    # Delete level (only if no subjects are associated)
                    if subjects_count == 0 and students_count == 0:
                        if st.button(f"Delete Level", key=f"delete_level_{level['id']}"):
                            if db.delete_level(level['id']):
                                # Log activity
                                db.log_activity(
                                    st.session_state.user_id,
                                    f"Deleted level: {level['name']}"
                                )
                                st.success(f"Level '{level['name']}' deleted successfully.")
                                st.rerun()
                            else:
                                st.error("Failed to delete level.")
                    else:
                        st.warning("Cannot delete level because it has associated subjects or students. "
                                  "Remove all associations first.")

def subject_management():
    """Subject management section of the admin dashboard."""
    st.header("Gestion des Matières")
    
    db = Database()
    
    # Tabs for different subject management functions
    tab1, tab2 = st.tabs(["Add Subject", "Manage Subjects"])
    
    with tab1:
        st.subheader("Add New Subject")
        
        # Get all levels for dropdown
        levels = db.get_all_levels()
        
        if not levels:
            st.warning("Please add at least one level before adding subjects.")
            return
        
        with st.form("add_subject_form"):
            subject_name = st.text_input("Subject Name", placeholder="e.g., Mathematics, Physics")
            
            level_names = [level["name"] for level in levels]
            level_ids = [level["id"] for level in levels]
            
            level_index = st.selectbox(
                "Level", 
                range(len(level_names)), 
                format_func=lambda i: level_names[i]
            )
            selected_level_id = level_ids[level_index]
            
            subject_description = st.text_area("Description (optional)", placeholder="Brief description of this subject...")
            submit = st.form_submit_button("Add Subject")
            
            if submit:
                if not subject_name:
                    st.error("Please enter a subject name.")
                else:
                    subject_id = db.add_subject(subject_name, selected_level_id, subject_description)
                    if subject_id:
                        # Log activity
                        db.log_activity(
                            st.session_state.user_id,
                            f"Added new subject: {subject_name} in level {level_names[level_index]}"
                        )
                        st.success(f"Subject '{subject_name}' added successfully.")
                        st.rerun()
                    else:
                        st.error("Failed to add subject. Name may already exist for this level.")
    
    with tab2:
        st.subheader("Manage Existing Subjects")
        
        # Filter by level
        levels = db.get_all_levels()
        
        if not levels:
            st.info("No levels found. Please add a level first.")
            return
        
        level_options = ["All Levels"] + [level["name"] for level in levels]
        selected_level = st.selectbox("Filter by Level", level_options)
        
        # Get filtered subjects
        if selected_level == "All Levels":
            subjects = db.get_all_subjects()
        else:
            selected_level_id = next((level["id"] for level in levels if level["name"] == selected_level), None)
            subjects = db.get_all_subjects(level_id=selected_level_id)
        
        if not subjects:
            st.info("No subjects found with the selected filter.")
        else:
            for subject in subjects:
                with st.expander(f"{subject['name']} ({subject['level_name']})"):
                    # Display subject details
                    st.markdown(f"**Description:** {subject['description'] or 'No description provided'}")
                    st.markdown(f"**Level:** {subject['level_name']}")
                    st.markdown(f"**Created at:** {subject['created_at']}")
                    
                    # Get usage statistics
                    courses_count = len(db.get_all_courses(subject_id=subject['id']))
                    students_count = len(db.get_users_assigned_to_subject(subject['id']))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Courses", courses_count)
                    with col2:
                        st.metric("Assigned Students", students_count)
                    
                    # Edit form
                    with st.form(f"edit_subject_{subject['id']}"):
                        new_name = st.text_input("Subject Name", value=subject['name'])
                        
                        level_names = [level["name"] for level in levels]
                        level_ids = [level["id"] for level in levels]
                        current_level_index = level_ids.index(subject['level_id'])
                        
                        new_level_index = st.selectbox(
                            "Level", 
                            range(len(level_names)), 
                            format_func=lambda i: level_names[i],
                            index=current_level_index
                        )
                        new_level_id = level_ids[new_level_index]
                        
                        new_description = st.text_area("Description", value=subject['description'] or "")
                        
                        update = st.form_submit_button("Update Subject")
                        
                        if update:
                            if not new_name:
                                st.error("Subject name cannot be empty.")
                            else:
                                updated = db.update_subject(subject['id'], new_name, new_level_id, new_description)
                                if updated:
                                    # Log activity
                                    db.log_activity(
                                        st.session_state.user_id,
                                        f"Updated subject: {subject['name']} to {new_name}"
                                    )
                                    st.success("Subject updated successfully.")
                                    st.rerun()
                                else:
                                    st.error("Failed to update subject. Name may already exist for this level.")
                    
                    # Delete subject (only if no courses are associated)
                    if courses_count == 0 and students_count == 0:
                        if st.button(f"Delete Subject", key=f"delete_subject_{subject['id']}"):
                            if db.delete_subject(subject['id']):
                                # Log activity
                                db.log_activity(
                                    st.session_state.user_id,
                                    f"Deleted subject: {subject['name']}"
                                )
                                st.success(f"Subject '{subject['name']}' deleted successfully.")
                                st.rerun()
                            else:
                                st.error("Failed to delete subject.")
                    else:
                        st.warning("Cannot delete subject because it has associated courses or students. "
                                  "Remove all associations first.")

def activity_logs():
    """Activity logs section of the admin dashboard."""
    st.header("Journaux d'Activité")
    
    # Apply custom styling
    st.markdown("""
    <style>
    .activity-header {
        color: #1565C0;
        padding: 1rem 0;
        border-bottom: 2px solid #1565C0;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1565C0;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    db = Database()
    
    # Get all users for filter dropdown
    users = db.get_all_users()
    user_options = ["All Users"] + [user["username"] for user in users]
    
    # Filter options in a container with better styling
    with st.container():
        st.markdown("### 📊 Filter Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_user = st.selectbox("👤 Filter by User", user_options)
        
        with col2:
            # Time range filter
            time_options = ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"]
            selected_time = st.selectbox("⏰ Time Range", time_options)
        
        with col3:
            limit_options = [10, 25, 50, 100]
            selected_limit = st.selectbox("📄 Number of Logs", limit_options, index=1)
    
    # Get filtered logs
    if selected_user == "All Users":
        logs = db.get_activity_logs(limit=selected_limit)
    else:
        selected_user_id = next((user["id"] for user in users if user["username"] == selected_user), None)
        logs = db.get_activity_logs(limit=selected_limit, user_id=selected_user_id)
    
    if not logs:
        st.info("No activity logs found with the selected filters.")
        return
    
    # Activity Overview Section
    st.markdown("### 📈 Activity Overview")
    
    # Calculate metrics
    total_logs = len(logs)
    unique_users = len(set(log['username'] for log in logs))
    recent_logs = len([log for log in logs if (datetime.now() - datetime.strptime(log['timestamp'], '%Y-%m-%d %H:%M:%S')).days < 1])
    
    # Display metrics in cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Total Activities</div>
        </div>
        """.format(total_logs), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Active Users</div>
        </div>
        """.format(unique_users), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">Recent Activities (24h)</div>
        </div>
        """.format(recent_logs), unsafe_allow_html=True)
    
    # Create charts
    st.markdown("### 📊 Activity Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Activity by user chart
        user_activity = pd.DataFrame(logs).groupby('username').size().reset_index(name='count')
        fig_users = px.bar(
            user_activity,
            x='username',
            y='count',
            title='Activities by User',
            color='count',
            color_continuous_scale='blues'
        )
        fig_users.update_layout(showlegend=False)
        st.plotly_chart(fig_users, use_container_width=True)
    
    with col2:
        # Activity timeline
        df_logs = pd.DataFrame(logs)
        df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
        df_logs['date'] = df_logs['timestamp'].dt.date
        daily_activity = df_logs.groupby('date').size().reset_index(name='count')
        
        fig_timeline = px.line(
            daily_activity,
            x='date',
            y='count',
            title='Activity Timeline',
            markers=True
        )
        fig_timeline.update_traces(line_color='#1565C0')
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Display detailed logs in a modern table
    st.markdown("### 📋 Detailed Activity Logs")
    
    # Convert logs to DataFrame for better display
    df_display = pd.DataFrame(logs)
    df_display['timestamp'] = pd.to_datetime(df_display['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df_display = df_display[['timestamp', 'username', 'action', 'details']].rename(columns={
        'timestamp': 'Timestamp',
        'username': 'User',
        'action': 'Action',
        'details': 'Details'
    })
    
    # Style the DataFrame
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Timestamp": st.column_config.DatetimeColumn(
                "Timestamp",
                help="When the activity occurred",
                format="DD/MM/YYYY HH:mm:ss"
            ),
            "User": st.column_config.TextColumn(
                "User",
                help="User who performed the action",
                width="medium"
            ),
            "Action": st.column_config.TextColumn(
                "Action",
                help="Type of activity",
                width="large"
            ),
            "Details": st.column_config.TextColumn(
                "Details",
                help="Additional information",
                width="large"
            )
        }
    )