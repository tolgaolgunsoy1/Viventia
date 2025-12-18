import customtkinter as ctk
from ..database.database import Database

class EditEmployeeModal(ctk.CTkToplevel):
    def __init__(self, parent, employee_id, callback=None):
        super().__init__(parent)
        
        self.employee_id = employee_id
        self.callback = callback
        self.db = Database()
        
        self.title("Personel Düzenle")
        self.geometry("500x600")
        self.configure(fg_color="#121212")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.load_employee_data()
        self.create_form()
        
    def load_employee_data(self):
        employees = self.db.get_employees()
        self.employee_data = None
        for emp in employees:
            if emp[0] == self.employee_id:
                self.employee_data = emp
                break
                
    def create_form(self):
        ctk.CTkLabel(
            self, 
            text="Personel Bilgilerini Düzenle", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#50C878"
        ).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.entries = {}
        
        fields = [
            ("Ad Soyad", "name", self.employee_data[1]),
            ("E-posta", "email", self.employee_data[7]),
            ("Telefon", "phone", self.employee_data[8]),
            ("Pozisyon", "position", self.employee_data[3]),
            ("Maaş", "salary", str(self.employee_data[4]))
        ]
        
        for label, key, value in fields:
            self.create_field(form_frame, label, key, value)
            
        # Departman
        dept_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        dept_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(dept_frame, text="Departman:", width=120, anchor="w").pack(side="left")
        
        self.dept_combo = ctk.CTkComboBox(
            dept_frame,
            values=["IT", "İK", "Muhasebe", "Satış", "Pazarlama", "Operasyon"],
            width=250
        )
        self.dept_combo.set(self.employee_data[2])
        self.dept_combo.pack(side="right")
        
        # Durum
        status_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(status_frame, text="Durum:", width=120, anchor="w").pack(side="left")
        
        self.status_combo = ctk.CTkComboBox(
            status_frame,
            values=["Aktif", "İzinli", "Pasif"],
            width=250
        )
        self.status_combo.set(self.employee_data[6])
        self.status_combo.pack(side="right")
        
        # Butonlar
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="İptal",
            fg_color="#666666",
            command=self.destroy
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="Güncelle",
            fg_color="#50C878",
            command=self.update_employee
        ).pack(side="right")
        
    def create_field(self, parent, label, key, value):
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(field_frame, text=f"{label}:", width=120, anchor="w").pack(side="left")
        
        entry = ctk.CTkEntry(field_frame, width=250)
        entry.insert(0, value)
        entry.pack(side="right")
        
        self.entries[key] = entry
        
    def update_employee(self):
        data = {}
        for key, entry in self.entries.items():
            data[key] = entry.get().strip()
            
        data["department"] = self.dept_combo.get()
        data["status"] = self.status_combo.get()
        
        if not data["name"]:
            self.show_error("Ad Soyad boş olamaz!")
            return
            
        try:
            data["salary"] = float(data["salary"]) if data["salary"] else 0
        except ValueError:
            self.show_error("Geçerli bir maaş tutarı girin!")
            return
            
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE employees 
                SET name=?, department=?, position=?, salary=?, email=?, phone=?, status=?
                WHERE id=?
            """, (data["name"], data["department"], data["position"], 
                  data["salary"], data["email"], data["phone"], data["status"], self.employee_id))
            
            conn.commit()
            conn.close()
            
            if self.callback:
                self.callback()
            
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self.master, "Başarılı", "Personel bilgileri güncellendi!")
                
            self.destroy()
            
        except Exception as e:
            self.show_error(f"Güncelleme hatası: {str(e)}")
            
    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Hata")
        error_window.geometry("300x150")
        error_window.configure(fg_color="#121212")
        error_window.transient(self)
        error_window.grab_set()
        
        ctk.CTkLabel(error_window, text=message, text_color="#F44336", wraplength=250).pack(expand=True)
        ctk.CTkButton(error_window, text="Tamam", command=error_window.destroy).pack(pady=10)