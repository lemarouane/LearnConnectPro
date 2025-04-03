import streamlit as st
import os
from auth import initialize_session_state, login_page, require_login, require_admin, require_validation, logout_user
from components.admin_dashboard import admin_dashboard
from components.student_dashboard import student_dashboard
from utils import apply_custom_css
import sqlite3

# Configure Streamlit page
st.set_page_config(
    page_title="Zouhair E-Learning Platform",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Make sure required directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/encrypted", exist_ok=True)

def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Apply custom CSS
    apply_custom_css()
    
    # Display logout button in sidebar if logged in
    if st.session_state.logged_in:
        st.sidebar.title(f"Welcome, {st.session_state.full_name or st.session_state.username}")
        
        # Display user role
        role_badge = "👨‍💼 Admin" if st.session_state.role == "admin" else "👨‍🎓 Student"
        st.sidebar.markdown(f"**Role:** {role_badge}")
        
        # Display validation status for students
        if st.session_state.role == "student":
            validation_status = "✅ Validated" if st.session_state.validated else "❌ Not Validated"
            st.sidebar.markdown(f"**Status:** {validation_status}")
        
        # Logout button
        if st.sidebar.button("Logout"):
            logout_user()
            st.rerun()
        
        st.sidebar.markdown("---")
    
    # Main content based on authentication state
    if not st.session_state.logged_in:
        # Show login page
        login_page()
    else:
        # Show appropriate dashboard based on role
        if st.session_state.role == "admin":
            # Admin dashboard
            admin_dashboard()
        elif st.session_state.role == "student":
            # Check if user is validated
            if st.session_state.validated:
                # Show student dashboard
                student_dashboard()
            else:
                # Show awaiting validation message
                st.warning("Your account is awaiting validation by an administrator. Please check back later.")
                
                st.markdown("""
                ## What happens next?
                
                1. An administrator will review your registration details.
                2. Once approved, you'll be able to access the platform's content.
                3. You'll be assigned to specific levels, subjects, and courses based on your needs.
                
                Thank you for your patience!
                """)
        else:
            # Unknown role
            st.error("Unknown user role. Please contact support.")

if __name__ == "__main__":
    main()