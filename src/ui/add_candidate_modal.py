import customtkinter as ctk
from ..database.database import Database

class AddCandidateModal(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        
        self.callback = callback
        self.db = Database()
        
        self.title("Yeni Aday Ekle")
        self.geometry("500x550")
        self.configure(fg_color="#121212")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.create_form()
        
    def create_form(self):
        ctk.CTkLabel(
            self, 
            text="Aday Bilgileri", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#50C878"
        ).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.entries = {}
        
        fields = [
            ("Aday Adı", "candidate_name"),
            ("E-posta", "candidate_email"),
            ("Pozisyon", "position")
        ]
        
        for label, key in fields:
            self.create_field(form_frame, label, key)
            
        # Departman
        dept_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        dept_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(dept_frame, text="Departman:", width=120, anchor="w").pack(side="left")
        
        self.dept_combo = ctk.CTkComboBox(
            dept_frame,
            values=["IT", "İK", "Muhasebe", "Satış", "Pazarlama", "Operasyon"],
            width=250
        )
        self.dept_combo.pack(side="right")
        
        # Mülakat tarihi
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(date_frame, text="Mülakat Tarihi:", width=120, anchor="w").pack(side="left")
        
        self.date_entry = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD", width=250)
        self.date_entry.pack(side="right")
        
        # Notlar
        notes_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        notes_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(notes_frame, text="Notlar:", width=120, anchor="nw").pack(side="left", pady=5)
        
        self.notes_text = ctk.CTkTextbox(notes_frame, width=250, height=80)
        self.notes_text.pack(side="right")
        
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
            text="Kaydet",
            fg_color="#50C878",
            command=self.save_candidate
        ).pack(side="right")
        
    def create_field(self, parent, label, key):
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(field_frame, text=f"{label}:", width=120, anchor="w").pack(side="left")
        
        entry = ctk.CTkEntry(field_frame, width=250)
        entry.pack(side="right")
        
        self.entries[key] = entry
        
    def save_candidate(self):
        data = {}
        for key, entry in self.entries.items():
            data[key] = entry.get().strip()
            
        data["department"] = self.dept_combo.get()
        data["interview_date"] = self.date_entry.get().strip()
        data["notes"] = self.notes_text.get("1.0", "end-1c").strip()
        
        if not all([data["candidate_name"], data["position"]]):
            self.show_error("Lütfen zorunlu alanları doldurun!")
            return
            
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO recruitment (position, department, candidate_name, candidate_email, 
                                       interview_date, notes, status)
                VALUES (?, ?, ?, ?, ?, ?, 'Başvuru')
            """, (data["position"], data["department"], data["candidate_name"], 
                  data["candidate_email"], data["interview_date"], data["notes"]))
            
            conn.commit()
            conn.close()
            
            if self.callback:
                self.callback()
            
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self.master, "Başarılı", "Aday başarıyla eklendi!")
                
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