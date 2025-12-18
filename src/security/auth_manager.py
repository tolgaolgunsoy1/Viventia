import hashlib
import sqlite3
import json
from datetime import datetime

class AuthManager:
    def __init__(self):
        self.db_path = "viventia.db"
        self.init_auth_tables()
        self.current_user = None
        
    def init_auth_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                employee_id INTEGER,
                created_date DATE DEFAULT CURRENT_DATE,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                table_name TEXT,
                record_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            demo_users = [
                ("admin", "admin123", "admin"),
                ("hr_manager", "hr123", "hr_manager"),
                ("user", "user123", "user")
            ]
            
            for username, password, role in demo_users:
                password_hash = self.hash_password(password)
                cursor.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                    (username, password_hash, role)
                )
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id, username, role, employee_id FROM users WHERE username = ? AND password_hash = ? AND is_active = 1",
            (username, password_hash)
        )
        
        user = cursor.fetchone()
        if user:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'role': user[2],
                'employee_id': user[3]
            }
            self.log_action("LOGIN")
            conn.close()
            return True
        
        conn.close()
        return False
    
    def has_permission(self, action):
        if not self.current_user:
            return False
            
        role = self.current_user['role']
        permissions = {
            'admin': ['all'],
            'hr_manager': ['view_all', 'edit_employees', 'approve_leaves'],
            'user': ['view_own', 'request_leave']
        }
        
        user_permissions = permissions.get(role, [])
        return 'all' in user_permissions or action in user_permissions
    
    def log_action(self, action, table_name=None, record_id=None):
        if not self.current_user:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (user_id, action, table_name, record_id)
            VALUES (?, ?, ?, ?)
        ''', (self.current_user['id'], action, table_name, record_id))
        
        conn.commit()
        conn.close()