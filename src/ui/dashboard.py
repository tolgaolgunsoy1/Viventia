import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from ..database.database import Database

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        self.db = Database()
        
        # Üst bilgi paneli
        self.create_header()
        
        # Veri kartları
        self.create_data_cards()
        
        # Analitik bölge
        self.create_analytics()
        
        # Personel tablosu
        self.create_employee_table()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=60)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        # Arama çubuğu
        search = ctk.CTkEntry(
            header, 
            placeholder_text="Personel ara...",
            width=300,
            height=35
        )
        search.pack(side="left", padx=20, pady=12)
        
        # Kullanıcı bilgisi
        user_frame = ctk.CTkFrame(header, fg_color="transparent")
        user_frame.pack(side="right", padx=20, pady=12)
        
        ctk.CTkLabel(
            user_frame, 
            text="Admin User", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="right", padx=10)
        
    def create_data_cards(self):
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 20))
        
        # Veritabanından gerçek veriler
        total, active, pending_leaves = self.db.get_employee_stats()
        efficiency = int((active / total * 100)) if total > 0 else 0
        
        cards_data = [
            ("Toplam Personel", str(total), "#50C878"),
            ("Aktif Görevde", str(active), "#4CAF50"),
            ("Bekleyen İzinler", str(pending_leaves), "#FF9800"),
            ("Aylık Verimlilik", f"%{efficiency}", "#2196F3")
        ]
        
        for i, (title, value, color) in enumerate(cards_data):
            card = ctk.CTkFrame(cards_frame, fg_color="#1E1E1E")
            card.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(
                card, 
                text=value, 
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color=color
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                card, 
                text=title, 
                font=ctk.CTkFont(size=12),
                text_color="#A0A0A0"
            ).pack(pady=(0, 20))
            
    def create_analytics(self):
        analytics_frame = ctk.CTkFrame(self, fg_color="transparent")
        analytics_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Sol taraf - Performans grafiği
        chart_frame = ctk.CTkFrame(analytics_frame, fg_color="#1E1E1E")
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Matplotlib grafik
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#1E1E1E')
        ax.set_facecolor('#1E1E1E')
        
        # Donut chart
        sizes = [65, 20, 15]
        colors = ['#50C878', '#FF9800', '#F44336']
        labels = ['Aktif', 'İzinli', 'Pasif']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                         autopct='%1.1f%%', startangle=90,
                                         wedgeprops=dict(width=0.5))
        
        for text in texts + autotexts:
            text.set_color('white')
            
        ax.set_title('Personel Durumu', color='white', fontsize=14, pad=20)
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sağ taraf - Departman dağılımı
        dept_frame = ctk.CTkFrame(analytics_frame, fg_color="#1E1E1E")
        dept_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            dept_frame, 
            text="Departman Dağılımı", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        departments = [
            ("IT", 45), ("İK", 25), ("Muhasebe", 30), 
            ("Satış", 35), ("Pazarlama", 21)
        ]
        
        for dept, count in departments:
            dept_item = ctk.CTkFrame(dept_frame, fg_color="transparent")
            dept_item.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(dept_item, text=dept, anchor="w").pack(side="left")
            ctk.CTkLabel(dept_item, text=str(count), text_color="#50C878").pack(side="right")
            
    def create_employee_table(self):
        table_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        table_frame.pack(fill="x", pady=(0, 0))
        
        # Başlık
        ctk.CTkLabel(
            table_frame, 
            text="Son Eklenen Personel", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10))
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20)
        
        headers = ["Ad Soyad", "Departman", "Pozisyon", "Durum"]
        for header in headers:
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                text_color="#A0A0A0"
            ).pack(side="left", expand=True)
            
        # Örnek veriler
        employees = [
            ("Ahmet Yılmaz", "IT", "Yazılım Geliştirici", "Aktif"),
            ("Ayşe Kaya", "İK", "İK Uzmanı", "Aktif"),
            ("Mehmet Demir", "Satış", "Satış Temsilcisi", "İzinli")
        ]
        
        for emp in employees:
            emp_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
            emp_frame.pack(fill="x", padx=20, pady=2)
            
            for i, data in enumerate(emp):
                color = "#50C878" if data == "Aktif" else "#FF9800" if data == "İzinli" else "#FFFFFF"
                ctk.CTkLabel(
                    emp_frame, 
                    text=data, 
                    text_color=color
                ).pack(side="left", expand=True)