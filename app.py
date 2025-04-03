import streamlit as st
import os
from auth import initialize_session_state, login_page, require_login, require_admin, require_validation, logout_user
from components.admin_dashboard import admin_dashboard
from components.student_dashboard import student_dashboard
from utils import apply_custom_css
import sqlite3

# Configure Streamlit page
st.set_page_config(
    page_title="Plateforme E-Learning Zouhair",
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
        st.sidebar.title(f"Bienvenue, {st.session_state.full_name or st.session_state.username}")
        
        # Display user role
        role_badge = "👨‍💼 Administrateur" if st.session_state.role == "admin" else "👨‍🎓 Étudiant"
        st.sidebar.markdown(f"**Rôle:** {role_badge}")
        
        # Display validation status for students
        if st.session_state.role == "student":
            validation_status = "✅ Validé" if st.session_state.validated else "❌ Non validé"
            st.sidebar.markdown(f"**Statut:** {validation_status}")
        
        # Logout button
        if st.sidebar.button("Déconnexion"):
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
                st.warning("Votre compte est en attente de validation par un administrateur. Veuillez vérifier ultérieurement.")
                
                st.markdown("""
                ## Que se passe-t-il ensuite ?
                
                1. Un administrateur examinera vos informations d'inscription.
                2. Une fois approuvé, vous pourrez accéder au contenu de la plateforme.
                3. Vous serez affecté à des niveaux, des sujets et des cours spécifiques en fonction de vos besoins.
                
                Merci pour votre patience !
                """)
        else:
            # Unknown role
            st.error("Rôle utilisateur inconnu. Veuillez contacter le support.")

if __name__ == "__main__":
    main()