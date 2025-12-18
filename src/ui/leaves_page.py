import customtkinter as ctk
from datetime import datetime, timedelta

class LeavesPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        
        # Başlık ve filtreler
        self.create_header()
        
        # İzin istatistikleri
        self.create_stats()
        
        # İzin talepleri listesi
        self.create_leaves_list()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="İzin Yönetimi", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
        # Filtre ve butonlar
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.pack(side="right", padx=20, pady=20)
        
        status_combo = ctk.CTkComboBox(
            controls_frame,
            values=["Tümü", "Bekliyor", "Onaylandı", "Reddedildi"],
            width=120
        )
        status_combo.pack(side="left", padx=5)
        
        ctk.CTkButton(
            controls_frame,
            text="+ Yeni İzin",
            fg_color="#50C878",
            hover_color="#45B56B",
            width=100
        ).pack(side="left", padx=10)
        
    def create_stats(self):
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats = [
            ("Bekleyen Talepler", "8", "#FF9800"),
            ("Bu Ay Onaylanan", "15", "#50C878"),
            ("Toplam İzin Günü", "142", "#2196F3"),
            ("Ortalama İzin", "9.5 gün", "#9C27B0")
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
            
    def create_leaves_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        list_frame.pack(fill="both", expand=True)
        
        # Başlık
        ctk.CTkLabel(
            list_frame, 
            text="İzin Talepleri", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        # Scrollable frame
        scrollable = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(scrollable, fg_color="#2A2A2A")
        header_frame.pack(fill="x", pady=(0, 10))
        
        headers = ["Personel", "İzin Türü", "Başlangıç", "Bitiş", "Gün", "Durum", "İşlemler"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=100
            ).grid(row=0, column=i, padx=10, pady=10)
        
        # Örnek izin verileri
        leaves_data = [
            ("Ahmet Yılmaz", "Yıllık İzin", "15.04.2024", "19.04.2024", "5", "Bekliyor"),
            ("Ayşe Kaya", "Hastalık İzni", "10.04.2024", "12.04.2024", "3", "Onaylandı"),
            ("Mehmet Demir", "Yıllık İzin", "22.04.2024", "26.04.2024", "5", "Bekliyor"),
            ("Fatma Özkan", "Mazeret İzni", "08.04.2024", "08.04.2024", "1", "Onaylandı"),
            ("Ali Şahin", "Yıllık İzin", "01.05.2024", "10.05.2024", "10", "Reddedildi")
        ]
        
        for data in leaves_data:
            self.create_leave_row(scrollable, data)
            
    def create_leave_row(self, parent, leave_data):
        row_frame = ctk.CTkFrame(parent, fg_color="#1A1A1A")
        row_frame.pack(fill="x", pady=2)
        
        # Veri alanları
        for i, value in enumerate(leave_data):
            if i == 5:  # Durum sütunu
                if value == "Bekliyor":
                    color = "#FF9800"
                elif value == "Onaylandı":
                    color = "#50C878"
                else:
                    color = "#F44336"
            else:
                color = "#FFFFFF"
                
            ctk.CTkLabel(
                row_frame, 
                text=str(value), 
                text_color=color,
                width=100
            ).grid(row=0, column=i, padx=10, pady=8)
        
        # İşlem butonları (sadece bekleyen talepler için)
        if leave_data[5] == "Bekliyor":
            btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            btn_frame.grid(row=0, column=6, padx=10, pady=5)
            
            ctk.CTkButton(
                btn_frame, 
                text="Onayla", 
                width=60, 
                height=25,
                fg_color="#50C878"
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(
                btn_frame, 
                text="Reddet", 
                width=60, 
                height=25,
                fg_color="#F44336"
            ).pack(side="left", padx=2)