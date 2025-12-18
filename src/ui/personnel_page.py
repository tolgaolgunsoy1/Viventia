import customtkinter as ctk
from ..database.database import Database
from .add_employee_modal import AddEmployeeModal

class PersonnelPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        self.db = Database()
        
        # Başlık ve butonlar
        self.create_header()
        
        # Personel listesi
        self.create_employee_list()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="Personel Yönetimi", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
        ctk.CTkButton(
            header,
            text="+ Yeni Personel",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.add_employee
        ).pack(side="right", padx=20, pady=20)
        
    def create_employee_list(self):
        # Scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="#1E1E1E")
        self.scrollable_frame.pack(fill="both", expand=True)
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2A2A2A")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        headers = ["Ad Soyad", "Departman", "Pozisyon", "Maaş", "Durum", "İşlemler"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=150
            ).grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        # Personel verileri
        employees = self.db.get_employees()
        for emp in employees:
            self.create_employee_row(emp)
            
    def create_employee_row(self, employee):
        row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#1A1A1A")
        row_frame.pack(fill="x", padx=10, pady=2)
        
        # Veri alanları
        data = [employee[1], employee[2], employee[3], f"{employee[4]:,.0f} ₺", employee[6]]
        
        for i, value in enumerate(data):
            color = "#50C878" if value == "Aktif" else "#FF9800" if value == "İzinli" else "#FFFFFF"
            ctk.CTkLabel(
                row_frame, 
                text=str(value), 
                text_color=color,
                width=150
            ).grid(row=0, column=i, padx=10, pady=10, sticky="w")
        
        # İşlem butonları
        btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=5, padx=10, pady=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="Düzenle", 
            width=60, 
            height=25,
            fg_color="#2196F3",
            command=lambda: self.edit_employee(employee[0])
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame, 
            text="Sil", 
            width=60, 
            height=25,
            fg_color="#F44336",
            command=lambda: self.delete_employee(employee[0])
        ).pack(side="left", padx=2)
    
    def add_employee(self):
        modal = AddEmployeeModal(self, callback=self.refresh_employee_list)
        
    def refresh_employee_list(self):
        # Personel listesini yenile
        try:
            for widget in self.scrollable_frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and len(self.scrollable_frame.winfo_children()) > 1 and widget != self.scrollable_frame.winfo_children()[0]:
                    widget.destroy()
                    
            employees = self.db.get_employees()
            for emp in employees:
                self.create_employee_row(emp)
        except Exception as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", f"Liste yenilenemedi: {str(e)}")
    
    def edit_employee(self, employee_id):
        from .edit_employee_modal import EditEmployeeModal
        modal = EditEmployeeModal(self, employee_id, callback=self.refresh_employee_list)
    
    def delete_employee(self, employee_id):
        # Onay penceresi
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Personel Sil")
        confirm_window.geometry("300x150")
        confirm_window.configure(fg_color="#121212")
        confirm_window.transient(self)
        confirm_window.grab_set()
        
        ctk.CTkLabel(
            confirm_window,
            text="Bu personeli silmek istediğinizden emin misiniz?",
            wraplength=250
        ).pack(pady=20)
        
        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        def confirm_delete():
            self.db.delete_employee(employee_id)
            self.refresh_employee_list()
            confirm_window.destroy()
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", "Personel başarıyla silindi!")
        
        ctk.CTkButton(
            btn_frame,
            text="İptal",
            fg_color="#666666",
            command=confirm_window.destroy
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Sil",
            fg_color="#F44336",
            command=confirm_delete
        ).pack(side="left", padx=5)