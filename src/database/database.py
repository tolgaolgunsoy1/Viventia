import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = "viventia.db"
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Personel tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL,
                hire_date DATE,
                status TEXT DEFAULT 'Aktif',
                email TEXT,
                phone TEXT
            )
        ''')
        
        # İzin tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                start_date DATE,
                end_date DATE,
                leave_type TEXT,
                status TEXT DEFAULT 'Bekliyor',
                reason TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # Bordro tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payroll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                month TEXT,
                base_salary REAL,
                bonus REAL DEFAULT 0,
                deductions REAL DEFAULT 0,
                net_salary REAL,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # Örnek veri ekle
        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            sample_data = [
                ("Ahmet Yılmaz", "IT", "Yazılım Geliştirici", 15000, "2023-01-15", "Aktif", "ahmet@viventia.com", "555-0101"),
                ("Ayşe Kaya", "İK", "İK Uzmanı", 12000, "2023-02-20", "Aktif", "ayse@viventia.com", "555-0102"),
                ("Mehmet Demir", "Satış", "Satış Temsilcisi", 10000, "2023-03-10", "İzinli", "mehmet@viventia.com", "555-0103"),
                ("Fatma Özkan", "Muhasebe", "Muhasebeci", 11000, "2023-01-05", "Aktif", "fatma@viventia.com", "555-0104"),
                ("Ali Şahin", "Pazarlama", "Pazarlama Uzmanı", 9500, "2023-04-12", "Aktif", "ali@viventia.com", "555-0105")
            ]
            cursor.executemany(
                "INSERT INTO employees (name, department, position, salary, hire_date, status, email, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                sample_data
            )
        
        conn.commit()
        conn.close()
    
    def get_employees(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        conn.close()
        return employees
    
    def get_employee_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM employees")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'Aktif'")
        active = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM leaves WHERE status = 'Bekliyor'")
        pending_leaves = cursor.fetchone()[0]
        
        conn.close()
        return total, active, pending_leaves