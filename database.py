import sqlite3
import os
import json
from datetime import datetime

class Database:
    def __init__(self, db_path="elearning.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create necessary database tables if they don't exist."""
        # Users table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Content table for both PDFs and videos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            encrypted_path TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            metadata TEXT,
            difficulty TEXT,
            category TEXT,
            added_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (added_by) REFERENCES users(id)
        )
        ''')
        
        # Content assignments table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER,
            user_id INTEGER,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES content(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
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
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ("admin", admin_hash, "admin")
            )
            self.conn.commit()
    
    def add_user(self, username, password_hash, role):
        """Add a new user to the database."""
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
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
                "created_at": user[4]
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
                "created_at": user[4]
            }
        return None
    
    def get_all_users(self, role=None):
        """Get all users, optionally filtered by role."""
        if role:
            self.cursor.execute("SELECT id, username, role, created_at FROM users WHERE role = ?", (role,))
        else:
            self.cursor.execute("SELECT id, username, role, created_at FROM users")
        
        users = []
        for user in self.cursor.fetchall():
            users.append({
                "id": user[0],
                "username": user[1],
                "role": user[2],
                "created_at": user[3]
            })
        return users
    
    def add_content(self, title, content_type, file_path, encrypted_path, original_filename, 
                   file_size, metadata, difficulty, category, added_by):
        """Add new content (PDF or video) to the database."""
        metadata_json = json.dumps(metadata) if metadata else None
        
        self.cursor.execute('''
        INSERT INTO content (
            title, type, file_path, encrypted_path, original_filename, 
            file_size, metadata, difficulty, category, added_by, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            title, content_type, file_path, encrypted_path, original_filename,
            file_size, metadata_json, difficulty, category, added_by,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        
        content_id = self.cursor.lastrowid
        self.conn.commit()
        
        # Log the activity
        self.log_activity(added_by, f"Added {content_type}", f"Title: {title}")
        
        return content_id
    
    def get_content(self, content_id):
        """Get content by ID."""
        self.cursor.execute("SELECT * FROM content WHERE id = ?", (content_id,))
        content = self.cursor.fetchone()
        if content:
            metadata = json.loads(content[7]) if content[7] else {}
            return {
                "id": content[0],
                "title": content[1],
                "type": content[2],
                "file_path": content[3],
                "encrypted_path": content[4],
                "original_filename": content[5],
                "file_size": content[6],
                "metadata": metadata,
                "difficulty": content[8],
                "category": content[9],
                "added_by": content[10],
                "created_at": content[11],
                "updated_at": content[12]
            }
        return None
    
    def get_all_content(self, content_type=None):
        """Get all content, optionally filtered by type."""
        if content_type:
            self.cursor.execute("SELECT * FROM content WHERE type = ? ORDER BY created_at DESC", (content_type,))
        else:
            self.cursor.execute("SELECT * FROM content ORDER BY created_at DESC")
        
        content_list = []
        for content in self.cursor.fetchall():
            metadata = json.loads(content[7]) if content[7] else {}
            content_list.append({
                "id": content[0],
                "title": content[1],
                "type": content[2],
                "file_path": content[3],
                "encrypted_path": content[4],
                "original_filename": content[5],
                "file_size": content[6],
                "metadata": metadata,
                "difficulty": content[8],
                "category": content[9],
                "added_by": content[10],
                "created_at": content[11],
                "updated_at": content[12]
            })
        return content_list
    
    def update_content(self, content_id, title=None, metadata=None, difficulty=None, category=None):
        """Update content details."""
        updates = []
        params = []
        
        if title:
            updates.append("title = ?")
            params.append(title)
        
        if metadata is not None:
            updates.append("metadata = ?")
            params.append(json.dumps(metadata))
        
        if difficulty:
            updates.append("difficulty = ?")
            params.append(difficulty)
        
        if category:
            updates.append("category = ?")
            params.append(category)
        
        if not updates:
            return False
        
        updates.append("updated_at = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        params.append(content_id)
        
        query = f"UPDATE content SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.conn.commit()
        return True
    
    def delete_content(self, content_id):
        """Delete content by ID."""
        # Get file paths before deletion
        self.cursor.execute("SELECT file_path, encrypted_path FROM content WHERE id = ?", (content_id,))
        paths = self.cursor.fetchone()
        
        # Delete content
        self.cursor.execute("DELETE FROM content WHERE id = ?", (content_id,))
        # Delete assignments
        self.cursor.execute("DELETE FROM content_assignments WHERE content_id = ?", (content_id,))
        self.conn.commit()
        
        return paths if paths else (None, None)
    
    def assign_content(self, content_id, user_id):
        """Assign content to a user."""
        try:
            self.cursor.execute(
                "INSERT INTO content_assignments (content_id, user_id) VALUES (?, ?)",
                (content_id, user_id)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def unassign_content(self, content_id, user_id):
        """Remove content assignment from a user."""
        self.cursor.execute(
            "DELETE FROM content_assignments WHERE content_id = ? AND user_id = ?",
            (content_id, user_id)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def get_user_content(self, user_id):
        """Get content assigned to a user."""
        self.cursor.execute("""
        SELECT c.* FROM content c
        JOIN content_assignments ca ON c.id = ca.content_id
        WHERE ca.user_id = ?
        ORDER BY c.created_at DESC
        """, (user_id,))
        
        content_list = []
        for content in self.cursor.fetchall():
            metadata = json.loads(content[7]) if content[7] else {}
            content_list.append({
                "id": content[0],
                "title": content[1],
                "type": content[2],
                "file_path": content[3],
                "encrypted_path": content[4],
                "original_filename": content[5],
                "file_size": content[6],
                "metadata": metadata,
                "difficulty": content[8],
                "category": content[9],
                "added_by": content[10],
                "created_at": content[11],
                "updated_at": content[12]
            })
        return content_list
    
    def get_content_assignments(self, content_id):
        """Get users assigned to specific content."""
        self.cursor.execute("""
        SELECT u.id, u.username, u.role, ca.assigned_at 
        FROM users u
        JOIN content_assignments ca ON u.id = ca.user_id
        WHERE ca.content_id = ?
        """, (content_id,))
        
        assigned_users = []
        for user in self.cursor.fetchall():
            assigned_users.append({
                "id": user[0],
                "username": user[1],
                "role": user[2],
                "assigned_at": user[3]
            })
        return assigned_users
    
    def log_activity(self, user_id, action, details=None):
        """Log user activity."""
        self.cursor.execute(
            "INSERT INTO activity_logs (user_id, action, details) VALUES (?, ?, ?)",
            (user_id, action, details)
        )
        self.conn.commit()
    
    def get_activity_logs(self, limit=50):
        """Get recent activity logs."""
        self.cursor.execute("""
        SELECT al.*, u.username 
        FROM activity_logs al
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
