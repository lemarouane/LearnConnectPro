import streamlit as st
import os
import pandas as pd
from database import Database
from utils import (
    validate_file, save_uploaded_file, delete_file, 
    get_pdf_preview, get_content_categories, get_content_difficulties,
    create_card, format_size, apply_custom_css
)
from auth import require_admin

@require_admin
def admin_dashboard():
    """Admin dashboard for managing content and users."""
    st.title("Admin Dashboard")
    apply_custom_css()
    
    tabs = st.tabs(["Content Management", "User Management", "Activity Logs"])
    
    with tabs[0]:
        content_management()
    
    with tabs[1]:
        user_management()
    
    with tabs[2]:
        activity_logs()

def content_management():
    """Content management section of the admin dashboard."""
    st.header("Content Management")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Add New Content")
        add_content_form()
    
    with col2:
        st.subheader("Existing Content")
        view_content_table()

def add_content_form():
    """Form for adding new content."""
    with st.form("upload_form"):
        title = st.text_input("Content Title")
        content_type = st.selectbox("Content Type", ["PDF", "Video"])
        
        uploaded_file = st.file_uploader(
            "Upload File", 
            type=["pdf", "mp4", "webm", "ogg"] if content_type == "Video" else ["pdf"]
        )
        
        category = st.selectbox(
            "Category", 
            [""] + get_content_categories() + ["New Category"]
        )
        
        if category == "New Category":
            category = st.text_input("Enter New Category")
        
        difficulty = st.selectbox("Difficulty Level", [""] + get_content_difficulties())
        
        metadata = {}
        metadata_col1, metadata_col2 = st.columns(2)
        
        with metadata_col1:
            metadata["description"] = st.text_area("Description", height=100)
        
        with metadata_col2:
            metadata["tags"] = st.text_input("Tags (comma separated)")
        
        submit = st.form_submit_button("Upload Content")
        
        if submit:
            if not title:
                st.error("Please enter a title")
                return
            
            if not uploaded_file:
                st.error("Please upload a file")
                return
            
            if not category:
                st.error("Please select or enter a category")
                return
            
            if not difficulty:
                st.error("Please select a difficulty level")
                return
            
            # Process file upload
            allowed_types = ["application/pdf"] if content_type == "PDF" else [
                "video/mp4", "video/webm", "video/ogg"
            ]
            
            is_valid, message = validate_file(uploaded_file, allowed_types)
            
            if not is_valid:
                st.error(message)
                return
            
            # Save and encrypt file
            original_path, encrypted_path, file_size = save_uploaded_file(uploaded_file)
            
            # Process tags
            if metadata["tags"]:
                metadata["tags"] = [tag.strip() for tag in metadata["tags"].split(",")]
            
            # Add to database
            db = Database()
            content_id = db.add_content(
                title=title,
                content_type=content_type,
                file_path=original_path,
                encrypted_path=encrypted_path,
                original_filename=uploaded_file.name,
                file_size=file_size,
                metadata=metadata,
                difficulty=difficulty,
                category=category,
                added_by=st.session_state.user_id
            )
            
            if content_id:
                st.success(f"Content uploaded successfully! ID: {content_id}")
                st.rerun()
            else:
                st.error("Error uploading content")

def view_content_table():
    """Display a table of existing content."""
    db = Database()
    content_list = db.get_all_content()
    
    if not content_list:
        st.info("No content available. Add some content to get started!")
        return
    
    # Create a DataFrame for display
    df_data = []
    for item in content_list:
        df_data.append({
            "ID": item["id"],
            "Title": item["title"],
            "Type": item["type"],
            "Category": item["category"],
            "Difficulty": item["difficulty"],
            "Size": format_size(item["file_size"]),
            "Added": item["created_at"].split()[0]  # Just the date part
        })
    
    df = pd.DataFrame(df_data)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Filter by Type", ["All"] + list(df["Type"].unique()))
    with col2:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(df["Category"].unique()))
    with col3:
        filter_difficulty = st.selectbox("Filter by Difficulty", ["All"] + list(df["Difficulty"].unique()))
    
    # Apply filters
    filtered_df = df.copy()
    if filter_type != "All":
        filtered_df = filtered_df[filtered_df["Type"] == filter_type]
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == filter_category]
    if filter_difficulty != "All":
        filtered_df = filtered_df[filtered_df["Difficulty"] == filter_difficulty]
    
    # Display table
    st.dataframe(filtered_df, use_container_width=True)
    
    # Content details and actions
    st.subheader("Content Details")
    selected_id = st.number_input("Enter Content ID to view details or manage", min_value=1, step=1)
    if st.button("Load Content Details"):
        display_content_details(selected_id)

def display_content_details(content_id):
    """Display details of selected content and provide management options."""
    db = Database()
    content = db.get_content(content_id)
    
    if not content:
        st.error(f"Content with ID {content_id} not found")
        return
    
    # Display content details
    st.write("### Content Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Title:** {content['title']}")
        st.write(f"**Type:** {content['type']}")
        st.write(f"**Category:** {content['category']}")
        st.write(f"**Difficulty:** {content['difficulty']}")
        st.write(f"**Original Filename:** {content['original_filename']}")
        st.write(f"**File Size:** {format_size(content['file_size'])}")
    
    with col2:
        st.write("**Metadata:**")
        if content['metadata'].get('description'):
            st.write(f"Description: {content['metadata']['description']}")
        if content['metadata'].get('tags'):
            st.write(f"Tags: {', '.join(content['metadata']['tags']) if isinstance(content['metadata']['tags'], list) else content['metadata']['tags']}")
        
        st.write(f"**Added By:** User ID {content['added_by']}")
        st.write(f"**Created:** {content['created_at']}")
        st.write(f"**Last Updated:** {content['updated_at']}")
    
    # Preview (if PDF)
    if content['type'] == 'PDF':
        st.write("### PDF Preview")
        preview_result = get_pdf_preview(content['encrypted_path'])
        
        if preview_result['success']:
            st.write(f"**Number of Pages:** {preview_result['num_pages']}")
            st.write(f"**Preview of first page:**")
            st.text(preview_result['preview_text'])
        else:
            st.error(f"Error previewing PDF: {preview_result.get('error', 'Unknown error')}")
    
    # User assignments
    st.write("### Assigned Users")
    assigned_users = db.get_content_assignments(content_id)
    
    if assigned_users:
        assigned_df = pd.DataFrame([
            {"User ID": user["id"], "Username": user["username"], "Role": user["role"], "Assigned At": user["assigned_at"]}
            for user in assigned_users
        ])
        st.dataframe(assigned_df, use_container_width=True)
    else:
        st.info("No users assigned to this content yet")
    
    # Assign to users
    st.write("### Assign to Users")
    users = db.get_all_users(role="student")
    if users:
        user_options = {f"{user['id']} - {user['username']}": user['id'] for user in users}
        selected_user = st.selectbox("Select User", list(user_options.keys()))
        
        if st.button("Assign to Selected User"):
            user_id = user_options[selected_user]
            success = db.assign_content(content_id, user_id)
            if success:
                st.success(f"Content assigned to user {selected_user}")
                st.rerun()
            else:
                st.error("Error assigning content to user")
    else:
        st.info("No student users available to assign content")
    
    # Edit content
    st.write("### Edit Content")
    with st.form(f"edit_content_{content_id}"):
        new_title = st.text_input("Title", value=content['title'])
        new_category = st.selectbox(
            "Category", 
            get_content_categories() + ["New Category"],
            index=get_content_categories().index(content['category']) if content['category'] in get_content_categories() else 0
        )
        
        if new_category == "New Category":
            new_category = st.text_input("Enter New Category")
        
        new_difficulty = st.selectbox(
            "Difficulty", 
            get_content_difficulties(),
            index=get_content_difficulties().index(content['difficulty']) if content['difficulty'] in get_content_difficulties() else 0
        )
        
        new_description = st.text_area(
            "Description", 
            value=content['metadata'].get('description', '')
        )
        
        new_tags = st.text_input(
            "Tags (comma separated)", 
            value=', '.join(content['metadata'].get('tags', [])) if isinstance(content['metadata'].get('tags', []), list) else content['metadata'].get('tags', '')
        )
        
        if st.form_submit_button("Update Content"):
            new_metadata = content['metadata'].copy()
            new_metadata['description'] = new_description
            new_metadata['tags'] = [tag.strip() for tag in new_tags.split(',')] if new_tags else []
            
            success = db.update_content(
                content_id=content_id,
                title=new_title,
                metadata=new_metadata,
                difficulty=new_difficulty,
                category=new_category
            )
            
            if success:
                st.success("Content updated successfully")
                st.rerun()
            else:
                st.error("Error updating content")
    
    # Delete content
    st.write("### Delete Content")
    if st.button("Delete This Content", key=f"delete_{content_id}"):
        confirm = st.checkbox("Confirm deletion? This action cannot be undone.")
        if confirm:
            file_path, encrypted_path = db.delete_content(content_id)
            if file_path and encrypted_path:
                delete_file(file_path, encrypted_path)
                st.success("Content deleted successfully")
                st.rerun()
            else:
                st.error("Error deleting content")

def user_management():
    """User management section of the admin dashboard."""
    st.header("User Management")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Add New User")
        with st.form("add_user_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["student", "admin"])
            
            if st.form_submit_button("Add User"):
                if not username or not password:
                    st.error("Username and password are required")
                else:
                    from auth import register_user
                    success, message = register_user(username, password, role)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
    
    with col2:
        st.subheader("Existing Users")
        db = Database()
        users = db.get_all_users()
        
        if users:
            user_df = pd.DataFrame([
                {"ID": user["id"], "Username": user["username"], "Role": user["role"], "Created": user["created_at"]}
                for user in users
            ])
            st.dataframe(user_df, use_container_width=True)
        else:
            st.info("No users found")

def activity_logs():
    """Activity logs section of the admin dashboard."""
    st.header("Activity Logs")
    
    db = Database()
    logs = db.get_activity_logs(limit=100)
    
    if logs:
        log_df = pd.DataFrame([
            {"ID": log["id"], "User": log["username"], "Action": log["action"], 
             "Details": log["details"], "Timestamp": log["timestamp"]}
            for log in logs
        ])
        st.dataframe(log_df, use_container_width=True)
    else:
        st.info("No activity logs found")
