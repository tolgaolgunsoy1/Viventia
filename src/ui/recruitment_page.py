import customtkinter as ctk
from ..database.database import Database

class RecruitmentPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        self.db = Database()
        
        self.create_header()
        self.create_stats()
        self.create_candidate_list()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="İşe Alım Yönetimi", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
        ctk.CTkButton(
            header,
            text="+ Yeni Aday",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.add_candidate
        ).pack(side="right", padx=20, pady=20)
        
    def create_stats(self):
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats = [
            ("Açık Pozisyonlar", "12", "#FF9800"),
            ("Aktif Başvurular", "45", "#2196F3"),
            ("Mülakatlar", "8", "#9C27B0"),
            ("Bu Ay İşe Alınan", "3", "#50C878")
        ]
        
        for title, value, color in stats:
            card = ctk.CTkFrame(stats_frame, fg_color="#1E1E1E")
            card.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(
                card, 
                text=value, 
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=color
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                card, 
                text=title, 
                font=ctk.CTkFont(size=12),
                text_color="#A0A0A0"
            ).pack(pady=(0, 20))
            
    def create_candidate_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        list_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            list_frame, 
            text="Aday Takip Listesi", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(list_frame, fg_color="#2A2A2A")
        header_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        headers = ["Aday Adı", "Pozisyon", "Departman", "Durum", "Mülakat Tarihi", "İşlemler"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=120
            ).grid(row=0, column=i, padx=10, pady=10)
        
        # Örnek aday verileri
        candidates = [
            ("Ahmet Kaya", "Yazılım Geliştirici", "IT", "Mülakat", "25.04.2024"),
            ("Zeynep Yılmaz", "Pazarlama Uzmanı", "Pazarlama", "CV İnceleme", "28.04.2024"),
            ("Murat Demir", "Muhasebeci", "Muhasebe", "Teklif", "22.04.2024")
        ]
        
        for candidate in candidates:
            self.create_candidate_row(list_frame, candidate)
            
    def create_candidate_row(self, parent, candidate_data):
        row_frame = ctk.CTkFrame(parent, fg_color="#1A1A1A")
        row_frame.pack(fill="x", padx=20, pady=2)
        
        for i, value in enumerate(candidate_data):
            if i == 3:  # Durum sütunu
                if value == "Teklif":
                    color = "#50C878"
                elif value == "Mülakat":
                    color = "#FF9800"
                else:
                    color = "#2196F3"
            else:
                color = "#FFFFFF"
                
            ctk.CTkLabel(
                row_frame, 
                text=str(value), 
                text_color=color,
                width=120
            ).grid(row=0, column=i, padx=10, pady=8)
        
        # İşlem butonları
        btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=5, padx=10, pady=5)
        
        ctk.CTkButton(
            btn_frame, 
            text="Görüşme", 
            width=70, 
            height=25,
            fg_color="#2196F3",
            command=lambda: self.schedule_interview(candidate_data[0])
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame, 
            text="İşe Al", 
            width=60, 
            height=25,
            fg_color="#50C878",
            command=lambda: self.hire_candidate(candidate_data[0])
        ).pack(side="left", padx=2)
    
    def add_candidate(self):
        from .add_candidate_modal import AddCandidateModal
        modal = AddCandidateModal(self, callback=self.refresh_candidate_list)
    
    def refresh_candidate_list(self):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "Aday listesi güncellendi!")
    
    def schedule_interview(self, candidate_name):
        # Mülakat tarihi güncelleme
        import sqlite3
        from datetime import datetime, timedelta
        
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            # Gelecek hafta için tarih belirle
            interview_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            cursor.execute("""
                UPDATE recruitment 
                SET status = 'Mülakat', interview_date = ?
                WHERE candidate_name = ?
            """, (interview_date, candidate_name))
            
            conn.commit()
            conn.close()
            
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", f"{candidate_name} için mülakat {interview_date} tarihine planlandı!")
            
        except Exception as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", f"Mülakat planlama hatası: {str(e)}")
    
    def hire_candidate(self, candidate_name):
        # Adayı işe alma
        import sqlite3
        
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            # Önce aday bilgilerini al
            cursor.execute("""
                SELECT position, department, candidate_email
                FROM recruitment 
                WHERE candidate_name = ?
            """, (candidate_name,))
            
            result = cursor.fetchone()
            if result:
                position, department, email = result
                
                # Personel tablosuna ekle
                cursor.execute("""
                    INSERT INTO employees (name, department, position, salary, hire_date, email, phone, status)
                    VALUES (?, ?, ?, ?, date('now'), ?, '', 'Aktif')
                """, (candidate_name, department, position, 10000, email))
                
                # İşe alım durumunu güncelle
                cursor.execute("""
                    UPDATE recruitment 
                    SET status = 'İşe Alındı'
                    WHERE candidate_name = ?
                """, (candidate_name,))
                
                conn.commit()
                
                from .notification_system import NotificationSystem
                NotificationSystem.show_success(self, "Başarılı", f"{candidate_name} başarıyla işe alındı ve personel listesine eklendi!")
            
            conn.close()
            
        except Exception as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", f"İşe alma hatası: {str(e)}")