import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

class AttendancePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        
        self.create_header()
        self.create_attendance_overview()
        self.create_daily_attendance()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="Puantaj ve Devam Takibi", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
        # Tarih seçici
        date_frame = ctk.CTkFrame(header, fg_color="transparent")
        date_frame.pack(side="right", padx=20, pady=20)
        
        ctk.CTkLabel(date_frame, text="Tarih:").pack(side="left", padx=5)
        ctk.CTkEntry(
            date_frame,
            placeholder_text="DD.MM.YYYY",
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            date_frame,
            text="Rapor Al",
            fg_color="#50C878",
            width=80
        ).pack(side="left", padx=10)
        
    def create_attendance_overview(self):
        overview_frame = ctk.CTkFrame(self, fg_color="transparent")
        overview_frame.pack(fill="x", pady=(0, 20))
        
        # Sol taraf - İstatistikler
        stats_frame = ctk.CTkFrame(overview_frame, fg_color="#1E1E1E")
        stats_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            stats_frame, 
            text="Günlük Özet", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        stats = [
            ("Toplam Personel", "156", "#2196F3"),
            ("Gelen", "142", "#50C878"),
            ("İzinli", "8", "#FF9800"),
            ("Geç Gelen", "6", "#F44336"),
            ("Fazla Mesai", "23", "#9C27B0")
        ]
        
        for title, value, color in stats:
            stat_item = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_item.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(stat_item, text=title, anchor="w").pack(side="left")
            ctk.CTkLabel(stat_item, text=value, text_color=color, font=ctk.CTkFont(weight="bold")).pack(side="right")
        
        # Sağ taraf - Haftalık grafik
        chart_frame = ctk.CTkFrame(overview_frame, fg_color="#1E1E1E")
        chart_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Haftalık devam grafiği
        fig, ax = plt.subplots(figsize=(5, 3), facecolor='#1E1E1E')
        ax.set_facecolor('#1E1E1E')
        
        days = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum']
        attendance = [142, 145, 138, 149, 144]
        
        ax.plot(days, attendance, color='#50C878', marker='o', linewidth=2, markersize=6)
        ax.set_title('Haftalık Devam Durumu', color='white', fontsize=12)
        ax.set_ylabel('Katılım', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
    def create_daily_attendance(self):
        attendance_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        attendance_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            attendance_frame, 
            text="Günlük Puantaj Listesi", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        # Filtreler
        filter_frame = ctk.CTkFrame(attendance_frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(filter_frame, text="Departman:").pack(side="left", padx=5)
        ctk.CTkComboBox(
            filter_frame,
            values=["Tümü", "IT", "İK", "Muhasebe", "Satış", "Pazarlama"],
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_frame, text="Durum:").pack(side="left", padx=(20, 5))
        ctk.CTkComboBox(
            filter_frame,
            values=["Tümü", "Geldi", "Geç Geldi", "İzinli", "Gelmedi"],
            width=120
        ).pack(side="left", padx=5)
        
        # Puantaj listesi
        scrollable = ctk.CTkScrollableFrame(attendance_frame, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(scrollable, fg_color="#2A2A2A")
        header_frame.pack(fill="x", pady=(0, 10))
        
        headers = ["Personel", "Departman", "Giriş", "Çıkış", "Toplam Saat", "Fazla Mesai", "Durum"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=100
            ).grid(row=0, column=i, padx=8, pady=10)
        
        # Örnek puantaj verileri
        attendance_data = [
            ("Ahmet Yılmaz", "IT", "08:45", "18:30", "9:45", "1:45", "Geldi"),
            ("Ayşe Kaya", "İK", "09:15", "18:00", "8:45", "0:00", "Geç Geldi"),
            ("Mehmet Demir", "Satış", "-", "-", "-", "-", "İzinli"),
            ("Fatma Özkan", "Muhasebe", "08:30", "17:30", "9:00", "0:00", "Geldi"),
            ("Ali Şahin", "Pazarlama", "09:30", "19:00", "9:30", "2:00", "Geç Geldi")
        ]
        
        for attendance in attendance_data:
            self.create_attendance_row(scrollable, attendance)
            
    def create_attendance_row(self, parent, attendance_data):
        row_frame = ctk.CTkFrame(parent, fg_color="#1A1A1A")
        row_frame.pack(fill="x", pady=2)
        
        for i, value in enumerate(attendance_data):
            if i == 6:  # Durum sütunu
                if value == "Geldi":
                    color = "#50C878"
                elif value == "Geç Geldi":
                    color = "#FF9800"
                elif value == "İzinli":
                    color = "#2196F3"
                else:
                    color = "#F44336"
            elif i == 5 and value != "-" and value != "0:00":  # Fazla mesai
                color = "#9C27B0"
            else:
                color = "#FFFFFF"
                
            ctk.CTkLabel(
                row_frame, 
                text=str(value), 
                text_color=color,
                width=100
            ).grid(row=0, column=i, padx=8, pady=8)