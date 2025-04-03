import streamlit as st
import os
from auth import initialize_session_state, login_page, logout_user
from components.admin_dashboard import admin_dashboard
from components.student_dashboard import student_dashboard
from utils import apply_custom_css

# Set page config
st.set_page_config(
    page_title="Secure E-Learning Platform",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/encrypted", exist_ok=True)
os.makedirs("styles", exist_ok=True)

# Initialize session state
initialize_session_state()

# Main application
def main():
    # Apply custom CSS
    apply_custom_css()
    
    # Sidebar
    with st.sidebar:
        st.title("🔒 Secure E-Learning")
        
        if st.session_state.logged_in:
            st.write(f"Logged in as: **{st.session_state.username}**")
            st.write(f"Role: **{st.session_state.role}**")
            
            if st.button("Logout"):
                logout_user()
                st.rerun()
        
        # Navigation links if logged in
        if st.session_state.logged_in:
            st.markdown("---")
            st.subheader("Navigation")
            
            if st.session_state.role == "admin":
                if st.button("Admin Dashboard"):
                    st.session_state.current_page = "admin"
                    st.rerun()
            
            if st.button("My Learning Materials"):
                st.session_state.current_page = "student"
                st.rerun()
    
    # Show login page if not logged in
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Show appropriate dashboard based on role and current page
    if "current_page" not in st.session_state:
        if st.session_state.role == "admin":
            st.session_state.current_page = "admin"
        else:
            st.session_state.current_page = "student"
    
    if st.session_state.current_page == "admin" and st.session_state.role == "admin":
        admin_dashboard()
    else:
        student_dashboard()

if __name__ == "__main__":
    main()
