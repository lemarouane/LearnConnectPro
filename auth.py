import bcrypt
import streamlit as st
from database import Database
import re
from functools import wraps

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'full_name' not in st.session_state:
        st.session_state.full_name = None
    if 'validated' not in st.session_state:
        st.session_state.validated = False
    if 'login_message' not in st.session_state:
        st.session_state.login_message = None
    if 'login_success' not in st.session_state:
        st.session_state.login_success = False
    if 'screenshot_count' not in st.session_state:
        st.session_state.screenshot_count = 0
    if 'last_screenshot_time' not in st.session_state:
        st.session_state.last_screenshot_time = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = None

def login_user(username, password):
    """Authenticate a user and set session state."""
    db = Database()
    user = db.get_user(username)
    
    if user and verify_password(password, user['password_hash']):
        st.session_state.logged_in = True
        st.session_state.user_id = user['id']
        st.session_state.username = user['username']
        st.session_state.role = user['role']
        st.session_state.full_name = user['full_name']
        st.session_state.validated = user['validated']
        st.session_state.login_message = f"Bienvenue, {user['full_name'] or username}!"
        st.session_state.login_success = True
        
        # Log login activity
        db.log_activity(user['id'], "Connexion")
        return True
    else:
        st.session_state.login_message = "Nom d'utilisateur ou mot de passe invalide"
        st.session_state.login_success = False
        return False

def validate_registration_form(username, password, confirm_password, full_name, email, phone):
    """Validate registration form input."""
    if not username or not password or not full_name:
        return False, "Le nom d'utilisateur, le mot de passe et le nom complet sont obligatoires."
    
    if password != confirm_password:
        return False, "Les mots de passe ne correspondent pas."
    
    if len(password) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères."
    
    # Username validation
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Le nom d'utilisateur ne peut contenir que des lettres, des chiffres et des tirets bas."
    
    # Email validation (if provided)
    if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return False, "Veuillez entrer une adresse email valide."
    
    # Phone validation (if provided)
    if phone and not re.match(r'^\+?[0-9\s\-\(\)]+$', phone):
        return False, "Veuillez entrer un numéro de téléphone valide."
    
    return True, ""

def register_user(username, password, full_name, email=None, phone=None):
    """Register a new user."""
    db = Database()
    
    # Check if username already exists
    if db.get_user(username):
        return False, "Ce nom d'utilisateur existe déjà"
    
    # Hash password and create user
    hashed_password = hash_password(password)
    user_id = db.add_user(
        username=username, 
        password_hash=hashed_password, 
        role="student",
        full_name=full_name,
        email=email,
        phone=phone
    )
    
    if user_id:
        return True, "Inscription réussie ! Veuillez attendre la validation de votre compte par un administrateur."
    else:
        return False, "L'inscription a échoué. Veuillez réessayer."

def logout_user():
    """Log out the current user."""
    if st.session_state.logged_in:
        user_id = st.session_state.user_id
        db = Database()
        db.log_activity(user_id, "Déconnexion")
    
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.full_name = None
    st.session_state.validated = False
    st.session_state.login_message = "Vous avez été déconnecté"
    st.session_state.login_success = False
    st.session_state.current_page = None

def require_login(func):
    """Decorator to require login for certain functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.logged_in:
            st.error("Veuillez vous connecter pour accéder à cette fonctionnalité")
            return None
        return func(*args, **kwargs)
    return wrapper

def require_admin(func):
    """Decorator to require admin role for certain functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.logged_in:
            st.error("Veuillez vous connecter pour accéder à cette fonctionnalité")
            return None
        if st.session_state.role != "admin":
            st.error("Privilèges d'administrateur requis")
            return None
        return func(*args, **kwargs)
    return wrapper

def require_validation(func):
    """Decorator to require account validation for certain functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.logged_in:
            st.error("Veuillez vous connecter pour accéder à cette fonctionnalité")
            return None
        if not st.session_state.validated:
            st.warning("Votre compte est en attente de validation par un administrateur")
            return None
        return func(*args, **kwargs)
    return wrapper

def login_page():
    """Render the login page."""
    st.title("Plateforme E-Learning Zouhair")
    
    # Custom CSS for styling
    st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
            font-weight: bold;
        }
        div.stButton > button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")
            
            if submit:
                login_user(username, password)
                if st.session_state.login_success:
                    st.rerun()
        
        if st.session_state.login_message and not st.session_state.login_success:
            st.error(st.session_state.login_message)
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Créer un compte étudiant")
            
            new_username = st.text_input("Choisir un nom d'utilisateur")
            new_password = st.text_input("Choisir un mot de passe", type="password")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password")
            
            full_name = st.text_input("Nom complet")
            email = st.text_input("Email (optionnel)")
            phone = st.text_input("Numéro de téléphone (optionnel)")
            
            # Registration terms agreement
            agree = st.checkbox("J'accepte les conditions d'utilisation")
            
            register = st.form_submit_button("S'inscrire")
            
            if register:
                if not agree:
                    st.error("Vous devez accepter les conditions d'utilisation pour vous inscrire")
                else:
                    is_valid, message = validate_registration_form(
                        new_username, new_password, confirm_password, full_name, email, phone
                    )
                    
                    if not is_valid:
                        st.error(message)
                    else:
                        success, message = register_user(
                            new_username, new_password, full_name, email, phone
                        )
                        if success:
                            st.success("Inscription réussie ! Veuillez attendre la validation de votre compte par un administrateur.")
                        else:
                            st.error(f"Échec de l'inscription : {message}")