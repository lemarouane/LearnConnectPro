import bcrypt
import streamlit as st
from database import Database

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
    if 'login_message' not in st.session_state:
        st.session_state.login_message = None
    if 'login_success' not in st.session_state:
        st.session_state.login_success = False

def login_user(username, password):
    """Authenticate a user and set session state."""
    db = Database()
    user = db.get_user(username)
    
    if user and verify_password(password, user['password_hash']):
        st.session_state.logged_in = True
        st.session_state.user_id = user['id']
        st.session_state.username = user['username']
        st.session_state.role = user['role']
        st.session_state.login_message = f"Welcome, {username}!"
        st.session_state.login_success = True
        
        # Log login activity
        db.log_activity(user['id'], "Logged in")
        return True
    else:
        st.session_state.login_message = "Invalid username or password"
        st.session_state.login_success = False
        return False

def register_user(username, password, role="student"):
    """Register a new user."""
    if not username or not password:
        return False, "Username and password are required"
    
    db = Database()
    
    # Check if username already exists
    if db.get_user(username):
        return False, "Username already exists"
    
    # Hash password and create user
    hashed_password = hash_password(password)
    success = db.add_user(username, hashed_password, role)
    
    if success:
        return True, "Registration successful! You can now log in."
    else:
        return False, "Registration failed. Please try again."

def logout_user():
    """Log out the current user."""
    if st.session_state.logged_in:
        user_id = st.session_state.user_id
        db = Database()
        db.log_activity(user_id, "Logged out")
    
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.login_message = "You have been logged out"
    st.session_state.login_success = False

def require_login(func):
    """Decorator to require login for certain functions."""
    def wrapper(*args, **kwargs):
        if not st.session_state.logged_in:
            st.error("Please log in to access this feature")
            return None
        return func(*args, **kwargs)
    return wrapper

def require_admin(func):
    """Decorator to require admin role for certain functions."""
    def wrapper(*args, **kwargs):
        if not st.session_state.logged_in:
            st.error("Please log in to access this feature")
            return None
        if st.session_state.role != "admin":
            st.error("Admin privileges required")
            return None
        return func(*args, **kwargs)
    return wrapper

def login_page():
    """Render the login page."""
    st.title("E-Learning Platform")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                login_user(username, password)
                if st.session_state.login_success:
                    st.rerun()
        
        if st.session_state.login_message and not st.session_state.login_success:
            st.error(st.session_state.login_message)
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            register = st.form_submit_button("Register")
            
            if register:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success, message = register_user(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
