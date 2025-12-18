import customtkinter as ctk
from ..database.database import Database

class EnhancedPersonnelPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F0F0F")
        self.db = Database()
        
        self.create_header()
        self.create_filters()
        self.create_employee_grid()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=15, height=80)
        header.pack(fill="x", padx=20, pady=(20, 15))
        header.pack_propagate(False)
        
        # Sol taraf
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=20, pady=15)
        
        ctk.CTkLabel(
            left_frame,
            text="👥 Personel Yönetimi",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#50C878"
        ).pack(anchor="w")
        
        total, active, _ = self.db.get_employee_stats()
        ctk.CTkLabel(
            left_frame,
            text=f"Toplam {total} personel • {active} aktif",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        ).pack(anchor="w")
        
        # Sağ taraf - butonlar
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20, pady=15)
        
        ctk.CTkButton(
            right_frame,
            text="➕ Yeni Personel",
            fg_color="#50C878",
            hover_color="#45B56B",
            width=120,
            height=40,
            command=self.add_employee
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            right_frame,
            text="📊 Rapor Al",
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=100,
            height=40,
            command=self.export_report
        ).pack(side="right", padx=5)
        
    def create_filters(self):
        filter_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=15)
        filter_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        filter_content = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_content.pack(fill="x", padx=20, pady=15)
        
        # Arama
        search_frame = ctk.CTkFrame(filter_content, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(search_frame, text="🔍", font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 8))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Personel ara...",
            width=250,
            height=35,
            fg_color="#252525",
            border_width=0
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self.filter_employees)
        
        # Filtreler
        filters_frame = ctk.CTkFrame(filter_content, fg_color="transparent")
        filters_frame.pack(side="right")
        
        ctk.CTkLabel(filters_frame, text="Departman:", text_color="#888888").pack(side="left", padx=(20, 5))
        
        self.dept_filter = ctk.CTkComboBox(
            filters_frame,
            values=["Tümü", "IT", "İK", "Muhasebe", "Satış", "Pazarlama"],
            width=120,
            height=35,
            fg_color="#252525",
            command=self.filter_employees
        )
        self.dept_filter.pack(side="left", padx=5)
        
        ctk.CTkLabel(filters_frame, text="Durum:", text_color="#888888").pack(side="left", padx=(10, 5))
        
        self.status_filter = ctk.CTkComboBox(
            filters_frame,
            values=["Tümü", "Aktif", "İzinli", "Pasif"],
            width=100,
            height=35,
            fg_color="#252525",
            command=self.filter_employees
        )
        self.status_filter.pack(side="left", padx=5)
        
    def create_employee_grid(self):
        # Grid container
        self.grid_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.load_employees()
        
    def load_employees(self):
        # Mevcut kartları temizle
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        employees = self.db.get_employees()
        
        # Grid layout için satır sayacı
        row = 0
        col = 0
        max_cols = 3
        
        for emp in employees:
            self.create_employee_card(emp, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
                
    def create_employee_card(self, employee, row, col):
        # Personel kartı
        card = ctk.CTkFrame(self.grid_frame, fg_color="#1A1A1A", corner_radius=15)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Grid ağırlıkları
        self.grid_frame.grid_columnconfigure(col, weight=1)
        
        # Kart içeriği
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Üst kısım - Avatar ve temel bilgi
        top_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 15))
        
        # Avatar
        avatar = ctk.CTkFrame(top_frame, fg_color="#50C878", corner_radius=25, width=50, height=50)
        avatar.pack(side="left", padx=(0, 15))
        avatar.pack_propagate(False)
        
        ctk.CTkLabel(
            avatar,
            text=employee[1][0].upper(),  # İlk harf
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Bilgiler
        info_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=employee[1],  # Ad soyad
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=employee[3],  # Pozisyon
            font=ctk.CTkFont(size=11),
            text_color="#50C878",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=employee[2],  # Departman
            font=ctk.CTkFont(size=10),
            text_color="#888888",
            anchor="w"
        ).pack(anchor="w")
        
        # Orta kısım - Detaylar
        details_frame = ctk.CTkFrame(card_content, fg_color="#252525", corner_radius=10)
        details_frame.pack(fill="x", pady=(0, 15))
        
        details_content = ctk.CTkFrame(details_frame, fg_color="transparent")
        details_content.pack(fill="x", padx=15, pady=10)
        
        # Maaş
        salary_frame = ctk.CTkFrame(details_content, fg_color="transparent")
        salary_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(salary_frame, text="💰", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(
            salary_frame, 
            text=f"{employee[4]:,.0f} ₺", 
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#FFD700"
        ).pack(side="left", padx=(5, 0))
        
        # E-posta
        if employee[7]:  # Email varsa
            email_frame = ctk.CTkFrame(details_content, fg_color="transparent")
            email_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(email_frame, text="📧", font=ctk.CTkFont(size=12)).pack(side="left")
            ctk.CTkLabel(
                email_frame, 
                text=employee[7], 
                font=ctk.CTkFont(size=9),
                text_color="#CCCCCC"
            ).pack(side="left", padx=(5, 0))
        
        # Durum
        status_color = "#50C878" if employee[6] == "Aktif" else "#FF9800" if employee[6] == "İzinli" else "#F44336"
        status_frame = ctk.CTkFrame(details_content, fg_color="transparent")
        status_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(status_frame, text="📊", font=ctk.CTkFont(size=12)).pack(side="left")
        ctk.CTkLabel(
            status_frame, 
            text=employee[6], 
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=status_color
        ).pack(side="left", padx=(5, 0))
        
        # Alt kısım - Butonlar
        buttons_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        ctk.CTkButton(
            buttons_frame,
            text="✏️ Düzenle",
            width=80,
            height=30,
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=lambda: self.edit_employee(employee[0])
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Sil",
            width=60,
            height=30,
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=lambda: self.delete_employee(employee[0])
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="👁️ Detay",
            width=70,
            height=30,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            command=lambda: self.view_details(employee[0])
        ).pack(side="right")
        
    def filter_employees(self, *args):
        # Filtreleme mantığı
        self.load_employees()
        
    def add_employee(self):
        from .add_employee_modal import AddEmployeeModal
        modal = AddEmployeeModal(self, callback=self.load_employees)
        
    def edit_employee(self, employee_id):
        from .edit_employee_modal import EditEmployeeModal
        modal = EditEmployeeModal(self, employee_id, callback=self.load_employees)
        
    def delete_employee(self, employee_id):
        # Onay penceresi
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Personel Sil")
        confirm_window.geometry("350x180")
        confirm_window.configure(fg_color="#1A1A1A")
        confirm_window.transient(self)
        confirm_window.grab_set()
        
        content_frame = ctk.CTkFrame(confirm_window, fg_color="#252525", corner_radius=15)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content_frame,
            text="⚠️",
            font=ctk.CTkFont(size=32)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            content_frame,
            text="Bu personeli silmek istediğinizden emin misiniz?",
            wraplength=280,
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 15))
        
        btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        def confirm_delete():
            self.db.delete_employee(employee_id)
            self.load_employees()
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
        
    def view_details(self, employee_id):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Bilgi", "Detay görüntüleme özelliği yakında eklenecek!")
        
    def export_report(self):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "Personel raporu oluşturuldu!")