import customtkinter as ctk
from ..database.database import Database

class AddEmployeeModal(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        
        self.callback = callback
        self.db = Database()
        
        # Modal ayarları
        self.title("Yeni Personel Ekle")
        self.geometry("500x600")
        self.configure(fg_color="#121212")
        self.resizable(False, False)
        
        # Modal'ı merkeze al
        self.transient(parent)
        self.grab_set()
        
        self.create_form()
        
    def create_form(self):
        # Başlık
        ctk.CTkLabel(
            self, 
            text="Yeni Personel Bilgileri", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#50C878"
        ).pack(pady=20)
        
        # Form container
        form_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Form alanları
        self.entries = {}
        
        fields = [
            ("Ad Soyad", "name"),
            ("E-posta", "email"),
            ("Telefon", "phone"),
            ("Departman", "department"),
            ("Pozisyon", "position"),
            ("Maaş", "salary")
        ]
        
        for label, key in fields:
            self.create_field(form_frame, label, key)
            
        # Departman combobox
        dept_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        dept_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(dept_frame, text="Departman:", width=120, anchor="w").pack(side="left")
        
        self.dept_combo = ctk.CTkComboBox(
            dept_frame,
            values=["IT", "İK", "Muhasebe", "Satış", "Pazarlama", "Operasyon"],
            width=250
        )
        self.dept_combo.pack(side="right")
        
        # İşe giriş tarihi
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(date_frame, text="İşe Giriş Tarihi:", width=120, anchor="w").pack(side="left")
        
        self.date_entry = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD", width=250)
        self.date_entry.pack(side="right")
        
        # Butonlar
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="İptal",
            fg_color="#666666",
            hover_color="#555555",
            command=self.destroy
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="Kaydet",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.save_employee
        ).pack(side="right")
        
    def create_field(self, parent, label, key):
        if key in ["department"]:  # Skip department, handled separately
            return
            
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(field_frame, text=f"{label}:", width=120, anchor="w").pack(side="left")
        
        entry = ctk.CTkEntry(field_frame, width=250)
        entry.pack(side="right")
        
        self.entries[key] = entry
        
    def save_employee(self):
        # Form verilerini al
        data = {}
        for key, entry in self.entries.items():
            data[key] = entry.get().strip()
            
        data["department"] = self.dept_combo.get()
        data["hire_date"] = self.date_entry.get().strip()
        
        # Gelişmiş validasyon
        from ..utils.validators import Validators
        
        if not all([data["name"], data["position"]]):
            self.show_error("Lütfen zorunlu alanları doldurun!")
            return
        
        if data["email"] and not Validators.validate_email(data["email"]):
            self.show_error("Geçerli bir e-posta adresi girin!")
            return
        
        if data["phone"] and not Validators.validate_phone(data["phone"]):
            self.show_error("Geçerli bir telefon numarası girin! (05XXXXXXXXX)")
            return
            
        if not Validators.validate_salary(data["salary"]):
            self.show_error("Geçerli bir maaş tutarı girin! (0-1.000.000)")
            return
        
        data["salary"] = float(data["salary"]) if data["salary"] else 0
        
        # Güvenlik için input sanitization
        for key in data:
            if isinstance(data[key], str):
                data[key] = Validators.sanitize_input(data[key])
            
        # Veritabanına kaydet
        try:
            self.db.add_employee(data)
            
            # Callback çağır
            if self.callback:
                self.callback()
            
            # Başarı mesajı
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self.master, "Başarılı", "Personel başarıyla eklendi!")
                
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
        
        ctk.CTkLabel(
            error_window, 
            text=message, 
            text_color="#F44336",
            wraplength=250
        ).pack(expand=True)
        
        ctk.CTkButton(
            error_window,
            text="Tamam",
            command=error_window.destroy
        ).pack(pady=10)