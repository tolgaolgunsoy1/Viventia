import customtkinter as ctk

class TrainingPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        
        self.create_header()
        self.create_training_stats()
        self.create_training_calendar()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="Eğitim ve Gelişim", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
        ctk.CTkButton(
            header,
            text="+ Eğitim Planla",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.add_training
        ).pack(side="right", padx=20, pady=20)
        
    def create_training_stats(self):
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats = [
            ("Aktif Eğitimler", "15", "#2196F3"),
            ("Tamamlanan", "42", "#50C878"),
            ("Katılımcı Sayısı", "156", "#FF9800"),
            ("Eğitim Bütçesi", "₺85.000", "#9C27B0")
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
            
    def create_training_calendar(self):
        calendar_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        calendar_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            calendar_frame, 
            text="Eğitim Takvimi", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        # Filtreler
        filter_frame = ctk.CTkFrame(calendar_frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(filter_frame, text="Kategori:").pack(side="left", padx=5)
        ctk.CTkComboBox(
            filter_frame,
            values=["Tümü", "Teknik", "Liderlik", "Kişisel Gelişim", "Uyum"],
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_frame, text="Durum:").pack(side="left", padx=(20, 5))
        ctk.CTkComboBox(
            filter_frame,
            values=["Tümü", "Planlandı", "Devam Ediyor", "Tamamlandı"],
            width=120
        ).pack(side="left", padx=5)
        
        # Eğitim listesi
        scrollable = ctk.CTkScrollableFrame(calendar_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(scrollable, fg_color="#2A2A2A")
        header_frame.pack(fill="x", pady=(0, 10))
        
        headers = ["Eğitim Adı", "Kategori", "Eğitmen", "Tarih", "Süre", "Katılımcı", "Durum"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=100
            ).grid(row=0, column=i, padx=8, pady=10)
        
        # Örnek eğitim verileri
        trainings = [
            ("Python Programlama", "Teknik", "Ahmet Kaya", "25-29.04.2024", "5 gün", "12", "Devam Ediyor"),
            ("Liderlik Becerileri", "Liderlik", "Ayşe Demir", "02-03.05.2024", "2 gün", "8", "Planlandı"),
            ("İletişim Teknikleri", "Kişisel Gelişim", "Murat Özkan", "15-16.04.2024", "2 gün", "15", "Tamamlandı"),
            ("Proje Yönetimi", "Teknik", "Fatma Yılmaz", "08-12.05.2024", "5 gün", "10", "Planlandı")
        ]
        
        for training in trainings:
            self.create_training_row(scrollable, training)
            
    def create_training_row(self, parent, training_data):
        row_frame = ctk.CTkFrame(parent, fg_color="#1A1A1A")
        row_frame.pack(fill="x", pady=2)
        
        for i, value in enumerate(training_data):
            if i == 6:  # Durum sütunu
                if value == "Tamamlandı":
                    color = "#50C878"
                elif value == "Devam Ediyor":
                    color = "#FF9800"
                else:
                    color = "#2196F3"
            else:
                color = "#FFFFFF"
                
            ctk.CTkLabel(
                row_frame, 
                text=str(value), 
                text_color=color,
                width=100
            ).grid(row=0, column=i, padx=8, pady=8)
    
    def add_training(self):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Bilgi", "Eğitim planlama özelliği yakında eklenecek!")