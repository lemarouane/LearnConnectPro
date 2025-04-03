import streamlit as st
import os
from auth import initialize_session_state, login_page, require_login, require_admin, require_validation, logout_user
from components.admin_dashboard import admin_dashboard
from components.student_dashboard import student_dashboard
from components.ui import initialize_ui, render_sidebar_menu, display_header, display_main_header
from translations import t
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
os.makedirs("uploads/temp", exist_ok=True)

def main():
    """Main application entry point."""
    # Initialize session state
    initialize_session_state()
    
    # Initialize UI components
    initialize_ui()
    
    # Main content based on authentication state
    if not st.session_state.logged_in:
        # Show login page
        login_page()
    else:
        # Display header
        display_header()
        
        # Render the sidebar with icons
        selected_menu = render_sidebar_menu()
        
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
                st.warning(t("validation_required"))
                
                display_main_header(t("welcome_message"))
                
                st.markdown(f"""
                ## {t("what_happens_next")}
                
                1. {t("admin_review")}
                2. {t("once_approved")}
                3. {t("will_be_assigned")}
                
                {t("thank_you")}
                """)
        else:
            # Unknown role
            st.error(t("unknown_role"))

if __name__ == "__main__":
    main()