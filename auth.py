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
        st.session_state.login_message = f"Welcome, {user['full_name'] or username}!"
        st.session_state.login_success = True
        
        # Log login activity
        db.log_activity(user['id'], "Logged in")
        return True
    else:
        st.session_state.login_message = "Invalid username or password"
        st.session_state.login_success = False
        return False

def validate_registration_form(username, password, confirm_password, full_name, email, phone):
    """Validate registration form input."""
    if not username or not password or not full_name:
        return False, "Username, password, and full name are required."
    
    if password != confirm_password:
        return False, "Passwords do not match."
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
    # Username validation
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores."
    
    # Email validation (if provided)
    if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return False, "Please enter a valid email address."
    
    # Phone validation (if provided)
    if phone and not re.match(r'^\+?[0-9\s\-\(\)]+$', phone):
        return False, "Please enter a valid phone number."
    
    return True, ""

def register_user(username, password, full_name, email=None, phone=None):
    """Register a new user."""
    db = Database()
    
    # Check if username already exists
    if db.get_user(username):
        return False, "Username already exists"
    
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
        return True, "Registration successful! Please wait for admin validation before logging in."
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
    st.session_state.full_name = None
    st.session_state.validated = False
    st.session_state.login_message = "You have been logged out"
    st.session_state.login_success = False
    st.session_state.current_page = None

def require_login(func):
    """Decorator to require login for certain functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.logged_in:
            st.error("Please log in to access this feature")
            return None
        return func(*args, **kwargs)
    return wrapper

def require_admin(func):
    """Decorator to require admin role for certain functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.logged_in:
            st.error("Please log in to access this feature")
            return None
        if st.session_state.role != "admin":
            st.error("Admin privileges required")
            return None
        return func(*args, **kwargs)
    return wrapper

def require_validation(func):
    """Decorator to require account validation for certain functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.logged_in:
            st.error("Please log in to access this feature")
            return None
        if not st.session_state.validated:
            st.warning("Your account is awaiting validation by an administrator")
            return None
        return func(*args, **kwargs)
    return wrapper

def login_page():
    """Render the login page."""
    st.title("Zouhair E-Learning Platform")
    
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
            st.subheader("Create Student Account")
            
            new_username = st.text_input("Choose Username")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            full_name = st.text_input("Full Name")
            email = st.text_input("Email (optional)")
            phone = st.text_input("Phone Number (optional)")
            
            # Registration terms agreement
            agree = st.checkbox("I agree to the terms and conditions")
            
            register = st.form_submit_button("Register")
            
            if register:
                if not agree:
                    st.error("You must agree to the terms and conditions to register")
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
                            st.success(message)
                        else:
                            st.error(message)