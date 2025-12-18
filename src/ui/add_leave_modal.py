import customtkinter as ctk
from ..database.database import Database

class AddLeaveModal(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        
        self.callback = callback
        self.db = Database()
        
        # Modal ayarları
        self.title("Yeni İzin Talebi")
        self.geometry("450x500")
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
            text="İzin Talebi Oluştur", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#50C878"
        ).pack(pady=20)
        
        # Form container
        form_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Personel seçimi
        emp_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        emp_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(emp_frame, text="Personel:", width=120, anchor="w").pack(side="left")
        
        # Personel listesi
        employees = self.db.get_employees()
        employee_names = [f"{emp[1]} ({emp[2]})" for emp in employees]
        self.employee_ids = [emp[0] for emp in employees]
        
        self.employee_combo = ctk.CTkComboBox(
            emp_frame,
            values=employee_names,
            width=250
        )
        self.employee_combo.pack(side="right")
        
        # İzin türü
        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(type_frame, text="İzin Türü:", width=120, anchor="w").pack(side="left")
        
        self.leave_type_combo = ctk.CTkComboBox(
            type_frame,
            values=["Yıllık İzin", "Hastalık İzni", "Mazeret İzni", "Doğum İzni", "Babalık İzni"],
            width=250
        )
        self.leave_type_combo.pack(side="right")
        
        # Başlangıç tarihi
        start_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        start_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(start_frame, text="Başlangıç Tarihi:", width=120, anchor="w").pack(side="left")
        
        self.start_date_entry = ctk.CTkEntry(start_frame, placeholder_text="YYYY-MM-DD", width=250)
        self.start_date_entry.pack(side="right")
        
        # Bitiş tarihi
        end_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        end_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(end_frame, text="Bitiş Tarihi:", width=120, anchor="w").pack(side="left")
        
        self.end_date_entry = ctk.CTkEntry(end_frame, placeholder_text="YYYY-MM-DD", width=250)
        self.end_date_entry.pack(side="right")
        
        # Açıklama
        reason_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        reason_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(reason_frame, text="Açıklama:", width=120, anchor="nw").pack(side="left", pady=5)
        
        self.reason_text = ctk.CTkTextbox(reason_frame, width=250, height=80)
        self.reason_text.pack(side="right")
        
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
            text="Talep Oluştur",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.save_leave
        ).pack(side="right")
        
    def save_leave(self):
        # Form verilerini al
        if not self.employee_combo.get():
            self.show_error("Lütfen personel seçin!")
            return
            
        employee_index = self.employee_combo.cget("values").index(self.employee_combo.get())
        employee_id = self.employee_ids[employee_index]
        
        data = {
            'employee_id': employee_id,
            'leave_type': self.leave_type_combo.get(),
            'start_date': self.start_date_entry.get().strip(),
            'end_date': self.end_date_entry.get().strip(),
            'reason': self.reason_text.get("1.0", "end-1c").strip()
        }
        
        # Validasyon
        if not all([data['leave_type'], data['start_date'], data['end_date']]):
            self.show_error("Lütfen tüm alanları doldurun!")
            return
            
        # Tarih formatı kontrolü
        if data['start_date'] and data['end_date']:
            try:
                from datetime import datetime
                datetime.strptime(data['start_date'], "%Y-%m-%d")
                datetime.strptime(data['end_date'], "%Y-%m-%d")
            except ValueError:
                self.show_error("Geçerli tarih formatı: YYYY-MM-DD")
                return
            
        # Veritabanına kaydet
        try:
            self.db.add_leave_request(data)
            
            # Callback çağır
            if self.callback:
                self.callback()
            
            # Başarı mesajı
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self.master, "Başarılı", "İzin talebi oluşturuldu!")
                
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