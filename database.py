import sqlite3
import os
import json
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_path="zouhair_elearning.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary database tables if they don't exist."""
        # Users table (both admin and students)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            validated BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Levels table (e.g., Bac+2, Bac+3)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Subjects/Matieres table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            level_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (level_id) REFERENCES levels(id),
            UNIQUE(name, level_id)
        )
        ''')
        
        # Courses table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            content_type TEXT NOT NULL,
            content_path TEXT,
            youtube_url TEXT,
            subject_id INTEGER,
            level_id INTEGER,
            difficulty TEXT NOT NULL,
            image_path TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            FOREIGN KEY (level_id) REFERENCES levels(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
        ''')
        
        # User-Level assignments
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            level_id INTEGER,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (level_id) REFERENCES levels(id),
            UNIQUE(user_id, level_id)
        )
        ''')
        
        # User-Subject assignments
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject_id INTEGER,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (subject_id) REFERENCES subjects(id),
            UNIQUE(user_id, subject_id)
        )
        ''')
        
        # User-Course assignments
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            UNIQUE(user_id, course_id)
        )
        ''')
        
        # Screenshot tracking
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS screenshot_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
        ''')
        
        # Activity logs
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Commit changes
        self.conn.commit()
        
        # Create admin user if not exists
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
        if self.cursor.fetchone()[0] == 0:
            from auth import hash_password
            admin_hash = hash_password("admin123")
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, role, full_name, validated) VALUES (?, ?, ?, ?, ?)",
                ("admin", admin_hash, "admin", "Zouhair Admin", 1)
            )
            self.conn.commit()
    
    # User Management
    def add_user(self, username, password_hash, role, full_name=None, email=None, phone=None):
        """Add a new user to the database."""
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, role, full_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
                (username, password_hash, role, full_name, email, phone)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_user(self, username):
        """Get user information by username."""
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "password_hash": user[2],
                "role": user[3],
                "full_name": user[4],
                "email": user[5],
                "phone": user[6],
                "validated": user[7],
                "created_at": user[8]
            }
        return None
    
    def get_user_by_id(self, user_id):
        """Get user information by ID."""
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = self.cursor.fetchone()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "password_hash": user[2],
                "role": user[3],
                "full_name": user[4],
                "email": user[5],
                "phone": user[6],
                "validated": user[7],
                "created_at": user[8]
            }
        return None
    
    def get_all_users(self, role=None, validated=None):
        """Get all users, optionally filtered by role and validation status."""
        query = "SELECT * FROM users"
        params = []
        
        if role is not None or validated is not None:
            query += " WHERE"
            
            if role is not None:
                query += " role = ?"
                params.append(role)
                
                if validated is not None:
                    query += " AND validated = ?"
                    params.append(validated)
            elif validated is not None:
                query += " validated = ?"
                params.append(validated)
        
        query += " ORDER BY created_at DESC"
        
        self.cursor.execute(query, params)
        
        users = []
        for user in self.cursor.fetchall():
            users.append({
                "id": user[0],
                "username": user[1],
                "password_hash": user[2],
                "role": user[3],
                "full_name": user[4],
                "email": user[5],
                "phone": user[6],
                "validated": user[7],
                "created_at": user[8]
            })
        return users
    
    def update_user(self, user_id, **kwargs):
        """Update user details."""
        valid_fields = ["username", "password_hash", "full_name", "email", "phone", "validated"]
        
        updates = []
        params = []
        
        for field, value in kwargs.items():
            if field in valid_fields:
                updates.append(f"{field} = ?")
                params.append(value)
        
        if not updates:
            return False
        
        params.append(user_id)
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.conn.commit()
        
        return self.cursor.rowcount > 0
    
    def validate_user(self, user_id, validate=True):
        """Set a user's validation status."""
        self.cursor.execute(
            "UPDATE users SET validated = ? WHERE id = ?",
            (1 if validate else 0, user_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def delete_user(self, user_id):
        """Delete a user."""
        # Delete all user assignments first
        self.cursor.execute("DELETE FROM user_levels WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM user_subjects WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM user_courses WHERE user_id = ?", (user_id,))
        
        # Then delete the user
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        
        return self.cursor.rowcount > 0
    
    # Level Management
    def add_level(self, name, description=None):
        """Add a new level."""
        try:
            self.cursor.execute(
                "INSERT INTO levels (name, description) VALUES (?, ?)",
                (name, description)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_level(self, level_id):
        """Get level by ID."""
        self.cursor.execute("SELECT * FROM levels WHERE id = ?", (level_id,))
        level = self.cursor.fetchone()
        if level:
            return {
                "id": level[0],
                "name": level[1],
                "description": level[2],
                "created_at": level[3]
            }
        return None
    
    def get_all_levels(self):
        """Get all levels."""
        self.cursor.execute("SELECT * FROM levels ORDER BY name")
        
        levels = []
        for level in self.cursor.fetchall():
            levels.append({
                "id": level[0],
                "name": level[1],
                "description": level[2],
                "created_at": level[3]
            })
        return levels
    
    def update_level(self, level_id, name=None, description=None):
        """Update level details."""
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if not updates:
            return False
        
        params.append(level_id)
        
        query = f"UPDATE levels SET {', '.join(updates)} WHERE id = ?"
        
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_level(self, level_id):
        """Delete a level."""
        # Check if level is in use
        self.cursor.execute("SELECT COUNT(*) FROM subjects WHERE level_id = ?", (level_id,))
        if self.cursor.fetchone()[0] > 0:
            return False
        
        self.cursor.execute("DELETE FROM levels WHERE id = ?", (level_id,))
        self.conn.commit()
        
        return self.cursor.rowcount > 0
    
    # Subject Management
    def add_subject(self, name, level_id, description=None):
        """Add a new subject."""
        try:
            self.cursor.execute(
                "INSERT INTO subjects (name, level_id, description) VALUES (?, ?, ?)",
                (name, level_id, description)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_subject(self, subject_id):
        """Get subject by ID."""
        self.cursor.execute("""
        SELECT s.*, l.name as level_name 
        FROM subjects s
        JOIN levels l ON s.level_id = l.id
        WHERE s.id = ?
        """, (subject_id,))
        
        subject = self.cursor.fetchone()
        if subject:
            return {
                "id": subject[0],
                "name": subject[1],
                "description": subject[2],
                "level_id": subject[3],
                "created_at": subject[4],
                "level_name": subject[5]
            }
        return None
    
    def get_all_subjects(self, level_id=None):
        """Get all subjects, optionally filtered by level."""
        query = """
        SELECT s.*, l.name as level_name 
        FROM subjects s
        JOIN levels l ON s.level_id = l.id
        """
        
        params = []
        if level_id:
            query += " WHERE s.level_id = ?"
            params.append(level_id)
        
        query += " ORDER BY s.name"
        
        self.cursor.execute(query, params)
        
        subjects = []
        for subject in self.cursor.fetchall():
            subjects.append({
                "id": subject[0],
                "name": subject[1],
                "description": subject[2],
                "level_id": subject[3],
                "created_at": subject[4],
                "level_name": subject[5]
            })
        return subjects
    
    def update_subject(self, subject_id, name=None, level_id=None, description=None):
        """Update subject details."""
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        
        if level_id:
            updates.append("level_id = ?")
            params.append(level_id)
        
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if not updates:
            return False
        
        params.append(subject_id)
        
        query = f"UPDATE subjects SET {', '.join(updates)} WHERE id = ?"
        
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False
    
    def delete_subject(self, subject_id):
        """Delete a subject."""
        # Check if subject is in use
        self.cursor.execute("SELECT COUNT(*) FROM courses WHERE subject_id = ?", (subject_id,))
        if self.cursor.fetchone()[0] > 0:
            return False
        
        self.cursor.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
        self.conn.commit()
        
        return self.cursor.rowcount > 0
    
    # Course Management
    def add_course(self, title, content_type, subject_id, level_id, difficulty, 
                  description=None, content_path=None, youtube_url=None, 
                  image_path=None, created_by=None):
        """Add a new course."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            self.cursor.execute('''
            INSERT INTO courses (
                title, description, content_type, content_path, youtube_url,
                subject_id, level_id, difficulty, image_path, created_by, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                title, description, content_type, content_path, youtube_url,
                subject_id, level_id, difficulty, image_path, created_by, current_time
            ))
            
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_course(self, course_id):
        """Get course by ID."""
        self.cursor.execute("""
        SELECT c.*, s.name as subject_name, l.name as level_name 
        FROM courses c
        JOIN subjects s ON c.subject_id = s.id
        JOIN levels l ON c.level_id = l.id
        WHERE c.id = ?
        """, (course_id,))
        
        course = self.cursor.fetchone()
        if course:
            return {
                "id": course[0],
                "title": course[1],
                "description": course[2],
                "content_type": course[3],
                "content_path": course[4],
                "youtube_url": course[5],
                "subject_id": course[6],
                "level_id": course[7],
                "difficulty": course[8],
                "image_path": course[9],
                "created_by": course[10],
                "created_at": course[11],
                "updated_at": course[12],
                "subject_name": course[13],
                "level_name": course[14]
            }
        return None
    
    def get_all_courses(self, subject_id=None, level_id=None, difficulty=None):
        """Get all courses, optionally filtered by subject, level, and difficulty."""
        query = """
        SELECT c.*, s.name as subject_name, l.name as level_name 
        FROM courses c
        JOIN subjects s ON c.subject_id = s.id
        JOIN levels l ON c.level_id = l.id
        """
        
        where_clauses = []
        params = []
        
        if subject_id:
            where_clauses.append("c.subject_id = ?")
            params.append(subject_id)
        
        if level_id:
            where_clauses.append("c.level_id = ?")
            params.append(level_id)
        
        if difficulty:
            where_clauses.append("c.difficulty = ?")
            params.append(difficulty)
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " ORDER BY c.created_at DESC"
        
        self.cursor.execute(query, params)
        
        courses = []
        for course in self.cursor.fetchall():
            courses.append({
                "id": course[0],
                "title": course[1],
                "description": course[2],
                "content_type": course[3],
                "content_path": course[4],
                "youtube_url": course[5],
                "subject_id": course[6],
                "level_id": course[7],
                "difficulty": course[8],
                "image_path": course[9],
                "created_by": course[10],
                "created_at": course[11],
                "updated_at": course[12],
                "subject_name": course[13],
                "level_name": course[14]
            })
        return courses
    
    def update_course(self, course_id, **kwargs):
        """Update course details."""
        valid_fields = [
            "title", "description", "content_type", "content_path", 
            "youtube_url", "subject_id", "level_id", "difficulty", "image_path"
        ]
        
        updates = []
        params = []
        
        for field, value in kwargs.items():
            if field in valid_fields:
                updates.append(f"{field} = ?")
                params.append(value)
        
        if not updates:
            return False
        
        # Add updated_at timestamp
        updates.append("updated_at = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        params.append(course_id)
        
        query = f"UPDATE courses SET {', '.join(updates)} WHERE id = ?"
        
        self.cursor.execute(query, params)
        self.conn.commit()
        
        return self.cursor.rowcount > 0
    
    def delete_course(self, course_id):
        """Delete a course."""
        # Get course file paths before deletion
        self.cursor.execute("SELECT content_path, image_path FROM courses WHERE id = ?", (course_id,))
        paths = self.cursor.fetchone()
        
        # Delete course assignments
        self.cursor.execute("DELETE FROM user_courses WHERE course_id = ?", (course_id,))
        
        # Delete the course
        self.cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        self.conn.commit()
        
        return paths if paths else (None, None)
    
    # Assignment Management
    def assign_level_to_user(self, user_id, level_id):
        """Assign a level to a user."""
        try:
            self.cursor.execute(
                "INSERT INTO user_levels (user_id, level_id) VALUES (?, ?)",
                (user_id, level_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def assign_subject_to_user(self, user_id, subject_id):
        """Assign a subject to a user."""
        try:
            self.cursor.execute(
                "INSERT INTO user_subjects (user_id, subject_id) VALUES (?, ?)",
                (user_id, subject_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def assign_course_to_user(self, user_id, course_id):
        """Assign a course to a user."""
        try:
            self.cursor.execute(
                "INSERT INTO user_courses (user_id, course_id) VALUES (?, ?)",
                (user_id, course_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def unassign_level_from_user(self, user_id, level_id):
        """Remove level assignment from a user."""
        self.cursor.execute(
            "DELETE FROM user_levels WHERE user_id = ? AND level_id = ?",
            (user_id, level_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def unassign_subject_from_user(self, user_id, subject_id):
        """Remove subject assignment from a user."""
        self.cursor.execute(
            "DELETE FROM user_subjects WHERE user_id = ? AND subject_id = ?",
            (user_id, subject_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def unassign_course_from_user(self, user_id, course_id):
        """Remove course assignment from a user."""
        self.cursor.execute(
            "DELETE FROM user_courses WHERE user_id = ? AND course_id = ?",
            (user_id, course_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_user_levels(self, user_id):
        """Get levels assigned to a user."""
        self.cursor.execute("""
        SELECT l.* FROM levels l
        JOIN user_levels ul ON l.id = ul.level_id
        WHERE ul.user_id = ?
        ORDER BY l.name
        """, (user_id,))
        
        levels = []
        for level in self.cursor.fetchall():
            levels.append({
                "id": level[0],
                "name": level[1],
                "description": level[2],
                "created_at": level[3]
            })
        return levels
    
    def get_user_subjects(self, user_id):
        """Get subjects assigned to a user."""
        self.cursor.execute("""
        SELECT s.*, l.name as level_name FROM subjects s
        JOIN user_subjects us ON s.id = us.subject_id
        JOIN levels l ON s.level_id = l.id
        WHERE us.user_id = ?
        ORDER BY s.name
        """, (user_id,))
        
        subjects = []
        for subject in self.cursor.fetchall():
            subjects.append({
                "id": subject[0],
                "name": subject[1],
                "description": subject[2],
                "level_id": subject[3],
                "created_at": subject[4],
                "level_name": subject[5]
            })
        return subjects
    
    def get_user_courses(self, user_id, subject_id=None, difficulty=None):
        """Get courses assigned to a user, optionally filtered by subject and difficulty."""
        query = """
        SELECT c.*, s.name as subject_name, l.name as level_name FROM courses c
        JOIN user_courses uc ON c.id = uc.course_id
        JOIN subjects s ON c.subject_id = s.id
        JOIN levels l ON c.level_id = l.id
        WHERE uc.user_id = ?
        """
        
        params = [user_id]
        
        if subject_id:
            query += " AND c.subject_id = ?"
            params.append(subject_id)
        
        if difficulty:
            query += " AND c.difficulty = ?"
            params.append(difficulty)
        
        query += " ORDER BY c.created_at DESC"
        
        self.cursor.execute(query, params)
        
        courses = []
        for course in self.cursor.fetchall():
            courses.append({
                "id": course[0],
                "title": course[1],
                "description": course[2],
                "content_type": course[3],
                "content_path": course[4],
                "youtube_url": course[5],
                "subject_id": course[6],
                "level_id": course[7],
                "difficulty": course[8],
                "image_path": course[9],
                "created_by": course[10],
                "created_at": course[11],
                "updated_at": course[12],
                "subject_name": course[13],
                "level_name": course[14]
            })
        return courses
    
    def get_users_assigned_to_level(self, level_id):
        """Get users assigned to a specific level."""
        self.cursor.execute("""
        SELECT u.* FROM users u
        JOIN user_levels ul ON u.id = ul.user_id
        WHERE ul.level_id = ? AND u.role = 'student'
        ORDER BY u.username
        """, (level_id,))
        
        users = []
        for user in self.cursor.fetchall():
            users.append({
                "id": user[0],
                "username": user[1],
                "password_hash": user[2],
                "role": user[3],
                "full_name": user[4],
                "email": user[5],
                "phone": user[6],
                "validated": user[7],
                "created_at": user[8]
            })
        return users
    
    def get_users_assigned_to_subject(self, subject_id):
        """Get users assigned to a specific subject."""
        self.cursor.execute("""
        SELECT u.* FROM users u
        JOIN user_subjects us ON u.id = us.user_id
        WHERE us.subject_id = ? AND u.role = 'student'
        ORDER BY u.username
        """, (subject_id,))
        
        users = []
        for user in self.cursor.fetchall():
            users.append({
                "id": user[0],
                "username": user[1],
                "password_hash": user[2],
                "role": user[3],
                "full_name": user[4],
                "email": user[5],
                "phone": user[6],
                "validated": user[7],
                "created_at": user[8]
            })
        return users
    
    def get_users_assigned_to_course(self, course_id):
        """Get users assigned to a specific course."""
        self.cursor.execute("""
        SELECT u.* FROM users u
        JOIN user_courses uc ON u.id = uc.user_id
        WHERE uc.course_id = ? AND u.role = 'student'
        ORDER BY u.username
        """, (course_id,))
        
        users = []
        for user in self.cursor.fetchall():
            users.append({
                "id": user[0],
                "username": user[1],
                "password_hash": user[2],
                "role": user[3],
                "full_name": user[4],
                "email": user[5],
                "phone": user[6],
                "validated": user[7],
                "created_at": user[8]
            })
        return users
    
    # Screenshot tracking
    def log_screenshot(self, user_id, course_id):
        """Log a screenshot for tracking."""
        self.cursor.execute(
            "INSERT INTO screenshot_logs (user_id, course_id) VALUES (?, ?)",
            (user_id, course_id)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_recent_screenshots(self, user_id, course_id=None, minutes=15):
        """Get count of screenshots within the last X minutes."""
        time_limit = (datetime.now() - timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
        
        if course_id:
            self.cursor.execute("""
            SELECT COUNT(*) FROM screenshot_logs
            WHERE user_id = ? AND course_id = ? AND timestamp > ?
            """, (user_id, course_id, time_limit))
        else:
            self.cursor.execute("""
            SELECT COUNT(*) FROM screenshot_logs
            WHERE user_id = ? AND timestamp > ?
            """, (user_id, time_limit))
        
        return self.cursor.fetchone()[0]
    
    # Activity logging
    def log_activity(self, user_id, action, details=None):
        """Log user activity."""
        self.cursor.execute(
            "INSERT INTO activity_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, action, details)
        )
        self.conn.commit()
    
    def get_activity_logs(self, limit=50, user_id=None):
        """Get recent activity logs, optionally filtered by user."""
        if user_id:
            self.cursor.execute("""
            SELECT al.*, u.username FROM activity_logs al
            JOIN users u ON al.user_id = u.id
            WHERE al.user_id = ?
            ORDER BY al.timestamp DESC
            LIMIT ?
            """, (user_id, limit))
        else:
            self.cursor.execute("""
            SELECT al.*, u.username FROM activity_logs al
            JOIN users u ON al.user_id = u.id
            ORDER BY al.timestamp DESC
            LIMIT ?
            """, (limit,))
        
        logs = []
        for log in self.cursor.fetchall():
            logs.append({
                "id": log[0],
                "user_id": log[1],
                "action": log[2],
                "details": log[3],
                "timestamp": log[4],
                "username": log[5]
            })
        return logs
    
    def close(self):
        """Close database connection."""
        self.conn.close()