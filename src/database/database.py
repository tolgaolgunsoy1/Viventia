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
        
        # Gelişmiş Personel tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tc_no TEXT UNIQUE,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                manager_id INTEGER,
                salary REAL,
                hire_date DATE,
                contract_type TEXT DEFAULT 'Belirsiz',
                status TEXT DEFAULT 'Aktif',
                email TEXT,
                phone TEXT,
                address TEXT,
                birth_date DATE,
                education TEXT,
                experience_years INTEGER DEFAULT 0,
                FOREIGN KEY (manager_id) REFERENCES employees (id)
            )
        ''')
        
        # Organizasyon yapısı
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER,
                manager_id INTEGER,
                budget REAL,
                FOREIGN KEY (parent_id) REFERENCES departments (id),
                FOREIGN KEY (manager_id) REFERENCES employees (id)
            )
        ''')
        
        # İşe alım süreci
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recruitment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position TEXT NOT NULL,
                department TEXT,
                candidate_name TEXT,
                candidate_email TEXT,
                status TEXT DEFAULT 'Başvuru',
                interview_date DATE,
                notes TEXT,
                created_date DATE DEFAULT CURRENT_DATE
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
                approved_by INTEGER,
                FOREIGN KEY (employee_id) REFERENCES employees (id),
                FOREIGN KEY (approved_by) REFERENCES employees (id)
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
                overtime_hours REAL DEFAULT 0,
                overtime_pay REAL DEFAULT 0,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # Yan haklar
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benefits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                benefit_type TEXT,
                amount REAL,
                start_date DATE,
                end_date DATE,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # Puantaj
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                date DATE,
                check_in TIME,
                check_out TIME,
                total_hours REAL,
                overtime_hours REAL DEFAULT 0,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        # Performans değerlendirme
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                evaluator_id INTEGER,
                period TEXT,
                score INTEGER,
                goals TEXT,
                feedback TEXT,
                evaluation_date DATE,
                FOREIGN KEY (employee_id) REFERENCES employees (id),
                FOREIGN KEY (evaluator_id) REFERENCES employees (id)
            )
        ''')
        
        # Eğitim kayıtları
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                training_name TEXT,
                provider TEXT,
                start_date DATE,
                end_date DATE,
                status TEXT DEFAULT 'Planlandı',
                cost REAL,
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