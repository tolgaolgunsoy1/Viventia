import customtkinter as ctk
from ..database.database import Database

class AddTrainingModal(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        
        self.callback = callback
        self.db = Database()
        
        self.title("Eğitim Planla")
        self.geometry("500x600")
        self.configure(fg_color="#121212")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.create_form()
        
    def create_form(self):
        ctk.CTkLabel(
            self, 
            text="Yeni Eğitim Planla", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#50C878"
        ).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.entries = {}
        
        fields = [
            ("Eğitim Adı", "training_name"),
            ("Eğitmen", "provider"),
            ("Başlangıç Tarihi", "start_date"),
            ("Bitiş Tarihi", "end_date"),
            ("Maliyet", "cost")
        ]
        
        for label, key in fields:
            self.create_field(form_frame, label, key)
            
        # Personel seçimi
        emp_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        emp_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(emp_frame, text="Katılımcı:", width=120, anchor="w").pack(side="left")
        
        employees = self.db.get_employees()
        employee_names = [f"{emp[1]} ({emp[2]})" for emp in employees]
        self.employee_ids = [emp[0] for emp in employees]
        
        self.employee_combo = ctk.CTkComboBox(
            emp_frame,
            values=employee_names,
            width=250
        )
        self.employee_combo.pack(side="right")
        
        # Kategori
        cat_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cat_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(cat_frame, text="Kategori:", width=120, anchor="w").pack(side="left")
        
        self.category_combo = ctk.CTkComboBox(
            cat_frame,
            values=["Teknik", "Liderlik", "Kişisel Gelişim", "Uyum", "Güvenlik"],
            width=250
        )
        self.category_combo.pack(side="right")
        
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
            text="Planla",
            fg_color="#50C878",
            command=self.save_training
        ).pack(side="right")
        
    def create_field(self, parent, label, key):
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(field_frame, text=f"{label}:", width=120, anchor="w").pack(side="left")
        
        if key in ["start_date", "end_date"]:
            entry = ctk.CTkEntry(field_frame, placeholder_text="YYYY-MM-DD", width=250)
        elif key == "cost":
            entry = ctk.CTkEntry(field_frame, placeholder_text="0.00", width=250)
        else:
            entry = ctk.CTkEntry(field_frame, width=250)
            
        entry.pack(side="right")
        self.entries[key] = entry
        
    def save_training(self):
        data = {}
        for key, entry in self.entries.items():
            data[key] = entry.get().strip()
            
        if not self.employee_combo.get():
            self.show_error("Lütfen katılımcı seçin!")
            return
            
        employee_index = self.employee_combo.cget("values").index(self.employee_combo.get())
        employee_id = self.employee_ids[employee_index]
        
        if not all([data["training_name"], data["provider"], data["start_date"]]):
            self.show_error("Lütfen zorunlu alanları doldurun!")
            return
            
        try:
            cost = float(data["cost"]) if data["cost"] else 0
        except ValueError:
            self.show_error("Geçerli bir maliyet girin!")
            return
            
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO training (employee_id, training_name, provider, start_date, 
                                    end_date, status, cost)
                VALUES (?, ?, ?, ?, ?, 'Planlandı', ?)
            """, (employee_id, data["training_name"], data["provider"], 
                  data["start_date"], data["end_date"], cost))
            
            conn.commit()
            conn.close()
            
            if self.callback:
                self.callback()
            
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self.master, "Başarılı", "Eğitim başarıyla planlandı!")
                
            self.destroy()
            
        except Exception as e:
            self.show_error(f"Kayıt hatası: {str(e)}")
            
    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Hata")
        error_window.geometry("300x150")
        error_window.configure(fg_color="#121212")
        error_window.transient(self)
        error_window.grab_set()
        
        ctk.CTkLabel(error_window, text=message, text_color="#F44336", wraplength=250).pack(expand=True)
        ctk.CTkButton(error_window, text="Tamam", command=error_window.destroy).pack(pady=10)