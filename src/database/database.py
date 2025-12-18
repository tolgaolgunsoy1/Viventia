import sqlite3
import os
import shutil
from datetime import datetime
import logging

# Logging yapılandırması
logging.basicConfig(
    filename='viventia.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseError(Exception):
    """Veritabanı işlemleri için özel hata sınıfı"""
    pass

class Database:
    def __init__(self):
        self.db_path = "viventia.db"
        self.init_database()
    
    def init_database(self):
        """Veritabanını başlatır ve tabloları oluşturur"""
        conn = None
        try:
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

                # Örnek izin verileri
                leave_data = [
                    (1, "2024-04-15", "2024-04-19", "Yıllık İzin", "Tatil", "Bekliyor"),
                    (2, "2024-04-10", "2024-04-12", "Hastalık İzni", "Grip", "Onaylandı"),
                    (3, "2024-04-22", "2024-04-26", "Yıllık İzin", "Kişisel", "Bekliyor")
                ]
                cursor.executemany(
                    "INSERT INTO leaves (employee_id, start_date, end_date, leave_type, reason, status) VALUES (?, ?, ?, ?, ?, ?)",
                    leave_data
                )

            conn.commit()

        except sqlite3.Error as e:
            logging.error(f"Veritabanı başlatma hatası: {e}")
            raise DatabaseError(f"Veritabanı başlatma başarısız: {e}")
        finally:
            if conn:
                conn.close()
    
    def get_employees(self):
        """Tüm çalışanları getirir"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            return employees
        except sqlite3.Error as e:
            logging.error(f"Çalışanları getirme hatası: {e}")
            raise DatabaseError(f"Çalışan verileri alınamadı: {e}")
        finally:
            if conn:
                conn.close()

    def get_employee_stats(self):
        """Çalışan istatistiklerini getirir"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM employees")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'Aktif'")
            active = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM leaves WHERE status = 'Bekliyor'")
            pending_leaves = cursor.fetchone()[0]

            return total, active, pending_leaves
        except sqlite3.Error as e:
            logging.error(f"İstatistik getirme hatası: {e}")
            raise DatabaseError(f"İstatistik verileri alınamadı: {e}")
        finally:
            if conn:
                conn.close()
    
    def add_employee(self, data):
        """Yeni çalışan ekler"""
        if not self._validate_employee_data(data):
            raise DatabaseError("Geçersiz çalışan verisi")

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO employees (name, department, position, salary, hire_date, email, phone, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Aktif')
            """, (data['name'], data['department'], data['position'],
                   data['salary'], data['hire_date'], data['email'], data['phone']))

            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            logging.error(f"Çalışan ekleme hatası (integrity): {e}")
            raise DatabaseError("Bu çalışan zaten mevcut veya gerekli alanlar eksik")
        except sqlite3.Error as e:
            logging.error(f"Çalışan ekleme hatası: {e}")
            raise DatabaseError(f"Çalışan eklenemedi: {e}")
        finally:
            if conn:
                conn.close()

    def delete_employee(self, employee_id):
        """Çalışanı siler"""
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise DatabaseError("Geçersiz çalışan ID")

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            if cursor.rowcount == 0:
                raise DatabaseError("Çalışan bulunamadı")
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Çalışan silme hatası: {e}")
            raise DatabaseError(f"Çalışan silinemedi: {e}")
        finally:
            if conn:
                conn.close()

    def update_employee_status(self, employee_id, status):
        """Çalışan durumunu günceller"""
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise DatabaseError("Geçersiz çalışan ID")
        if status not in ['Aktif', 'İzinli', 'Pasif', 'İşten Ayrıldı']:
            raise DatabaseError("Geçersiz durum")

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE employees SET status = ? WHERE id = ?", (status, employee_id))
            if cursor.rowcount == 0:
                raise DatabaseError("Çalışan bulunamadı")
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Durum güncelleme hatası: {e}")
            raise DatabaseError(f"Durum güncellenemedi: {e}")
        finally:
            if conn:
                conn.close()
    
    def _validate_employee_data(self, data):
        """Çalışan verilerini doğrular"""
        required_fields = ['name', 'department', 'position', 'salary', 'hire_date', 'email', 'phone']
        for field in required_fields:
            if field not in data or not data[field]:
                return False

        # Email format kontrolü
        import re
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            return False

        # Maaş kontrolü
        try:
            salary = float(data['salary'])
            if salary < 0:
                return False
        except (ValueError, TypeError):
            return False

        return True

    def add_leave_request(self, data):
        """İzin talebi ekler"""
        if not self._validate_leave_data(data):
            raise DatabaseError("Geçersiz izin verisi")

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO leaves (employee_id, start_date, end_date, leave_type, reason, status)
                VALUES (?, ?, ?, ?, ?, 'Bekliyor')
            """, (data['employee_id'], data['start_date'], data['end_date'],
                   data['leave_type'], data['reason']))

            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"İzin talebi ekleme hatası: {e}")
            raise DatabaseError(f"İzin talebi eklenemedi: {e}")
        finally:
            if conn:
                conn.close()

    def approve_leave(self, leave_id):
        """İzni onaylar"""
        if not isinstance(leave_id, int) or leave_id <= 0:
            raise DatabaseError("Geçersiz izin ID")

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE leaves SET status = 'Onaylandı' WHERE id = ?", (leave_id,))
            if cursor.rowcount == 0:
                raise DatabaseError("İzin talebi bulunamadı")
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"İzin onaylama hatası: {e}")
            raise DatabaseError(f"İzin onaylanamadı: {e}")
        finally:
            if conn:
                conn.close()

    def reject_leave(self, leave_id):
        """İzni reddeder"""
        if not isinstance(leave_id, int) or leave_id <= 0:
            raise DatabaseError("Geçersiz izin ID")

        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE leaves SET status = 'Reddedildi' WHERE id = ?", (leave_id,))
            if cursor.rowcount == 0:
                raise DatabaseError("İzin talebi bulunamadı")
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"İzin reddetme hatası: {e}")
            raise DatabaseError(f"İzin reddedilemedi: {e}")
        finally:
            if conn:
                conn.close()

    def get_leaves(self):
        """İzin taleplerini getirir"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.id, e.name, l.leave_type, l.start_date, l.end_date,
                       l.reason, l.status
                FROM leaves l
                JOIN employees e ON l.employee_id = e.id
                ORDER BY l.id DESC
            """)
            leaves = cursor.fetchall()
            return leaves
        except sqlite3.Error as e:
            logging.error(f"İzin getirme hatası: {e}")
            raise DatabaseError(f"İzin verileri alınamadı: {e}")
        finally:
            if conn:
                conn.close()

    def _validate_leave_data(self, data):
        """İzin verilerini doğrular"""
        required_fields = ['employee_id', 'start_date', 'end_date', 'leave_type', 'reason']
        for field in required_fields:
            if field not in data or not data[field]:
                return False

        # Tarih format kontrolü
        from datetime import datetime
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
            if end_date < start_date:
                return False
        except ValueError:
            return False

        return True

    def create_backup(self, backup_dir="backups"):
        """Veritabanı yedeği oluşturur"""
        try:
            # Backup klasörünü oluştur
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # Backup dosya adı
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"viventia_backup_{timestamp}.db")

            # Veritabanını kopyala
            shutil.copy2(self.db_path, backup_path)

            logging.info(f"Veritabanı yedeği oluşturuldu: {backup_path}")
            return backup_path

        except Exception as e:
            logging.error(f"Yedek oluşturma hatası: {e}")
            raise DatabaseError(f"Yedek oluşturma başarısız: {e}")

    def restore_backup(self, backup_path):
        """Veritabanı yedeğini geri yükler"""
        if not os.path.exists(backup_path):
            raise DatabaseError("Yedek dosyası bulunamadı")

        try:
            # Mevcut veritabanını yedekle
            temp_backup = f"{self.db_path}.temp"
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, temp_backup)

            # Yedeği geri yükle
            shutil.copy2(backup_path, self.db_path)

            # Geçici yedeği sil
            if os.path.exists(temp_backup):
                os.remove(temp_backup)

            logging.info(f"Veritabanı yedeği geri yüklendi: {backup_path}")

        except Exception as e:
            # Hata durumunda eski veritabanıyı geri yükle
            if os.path.exists(temp_backup):
                shutil.copy2(temp_backup, self.db_path)
                os.remove(temp_backup)
            logging.error(f"Yedek geri yükleme hatası: {e}")
            raise DatabaseError(f"Yedek geri yükleme başarısız: {e}")

    def get_backup_list(self, backup_dir="backups"):
        """Mevcut yedek dosyalarını listeler"""
        try:
            if not os.path.exists(backup_dir):
                return []

            backups = []
            for file in os.listdir(backup_dir):
                if file.startswith("viventia_backup_") and file.endswith(".db"):
                    file_path = os.path.join(backup_dir, file)
                    file_size = os.path.getsize(file_path)
                    modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                    backups.append({
                        'filename': file,
                        'path': file_path,
                        'size': file_size,
                        'date': modified_time
                    })

            # Tarihe göre sırala (en yeni önce)
            backups.sort(key=lambda x: x['date'], reverse=True)
            return backups

        except Exception as e:
            logging.error(f"Yedek listesi alma hatası: {e}")
            return []