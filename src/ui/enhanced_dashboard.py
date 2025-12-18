import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from ..database.database import Database
from datetime import datetime, timedelta

class EnhancedDashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F0F0F")
        self.db = Database()
        
        self.create_header()
        self.create_quick_stats()
        self.create_charts_section()
        self.create_recent_activities()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=15, height=80)
        header.pack(fill="x", padx=20, pady=(20, 15))
        header.pack_propagate(False)
        
        # Sol taraf - Hoşgeldin mesajı
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=20, pady=15)
        
        ctk.CTkLabel(
            left_frame,
            text="📊 Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#50C878"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_frame,
            text=f"Bugün: {datetime.now().strftime('%d %B %Y')}",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        ).pack(anchor="w")
        
        # Sağ taraf - Hızlı işlemler
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20, pady=15)
        
        ctk.CTkButton(
            right_frame,
            text="🔄 Yenile",
            width=80,
            height=35,
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=self.refresh_data
        ).pack(side="right", padx=5)
        
    def create_quick_stats(self):
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Gerçek veriler
        total, active, pending_leaves = self.db.get_employee_stats()
        
        stats_data = [
            ("👥 Toplam Personel", str(total), "#50C878", "kişi"),
            ("✅ Aktif Çalışan", str(active), "#4CAF50", "kişi"),
            ("⏳ Bekleyen İzinler", str(pending_leaves), "#FF9800", "talep"),
            ("📈 Verimlilik", f"%{int((active/total*100)) if total > 0 else 0}", "#2196F3", "oran")
        ]
        
        for i, (title, value, color, unit) in enumerate(stats_data):
            card = ctk.CTkFrame(stats_frame, fg_color="#1A1A1A", corner_radius=15)
            card.pack(side="left", fill="both", expand=True, padx=8)
            
            # İkon ve değer
            value_frame = ctk.CTkFrame(card, fg_color="transparent")
            value_frame.pack(pady=20)
            
            ctk.CTkLabel(
                value_frame,
                text=value,
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color=color
            ).pack()
            
            ctk.CTkLabel(
                value_frame,
                text=title,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white"
            ).pack()
            
            ctk.CTkLabel(
                value_frame,
                text=unit,
                font=ctk.CTkFont(size=10),
                text_color="#666666"
            ).pack()
            
    def create_charts_section(self):
        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Sol grafik - Departman dağılımı
        left_chart = ctk.CTkFrame(charts_frame, fg_color="#1A1A1A", corner_radius=15)
        left_chart.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            left_chart,
            text="📊 Departman Dağılımı",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(15, 10))
        
        self.create_department_chart(left_chart)
        
        # Sağ grafik - Performans trendi
        right_chart = ctk.CTkFrame(charts_frame, fg_color="#1A1A1A", corner_radius=15)
        right_chart.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            right_chart,
            text="📈 Aylık Performans",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(15, 10))
        
        self.create_performance_chart(right_chart)
        
    def create_department_chart(self, parent):
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#1A1A1A')
        ax.set_facecolor('#1A1A1A')
        
        # Örnek departman verileri
        departments = ['IT', 'İK', 'Satış', 'Muhasebe', 'Pazarlama']
        sizes = [30, 15, 25, 20, 10]
        colors = ['#50C878', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=departments, colors=colors, 
                                         autopct='%1.1f%%', startangle=90,
                                         wedgeprops=dict(width=0.6))
        
        for text in texts + autotexts:
            text.set_color('white')
            text.set_fontsize(9)
            
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_performance_chart(self, parent):
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#1A1A1A')
        ax.set_facecolor('#1A1A1A')
        
        # Son 6 ay performans verisi
        months = ['Eki', 'Kas', 'Ara', 'Oca', 'Şub', 'Mar']
        performance = [85, 88, 92, 87, 90, 94]
        
        ax.plot(months, performance, color='#50C878', marker='o', linewidth=3, markersize=6)
        ax.fill_between(months, performance, alpha=0.3, color='#50C878')
        
        ax.set_ylim(80, 100)
        ax.set_ylabel('Performans (%)', color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=9)
        ax.grid(True, alpha=0.2, color='white')
        
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_alpha(0.3)
            
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_recent_activities(self):
        activities_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=15)
        activities_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            activities_frame,
            text="🕒 Son Aktiviteler",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(15, 10))
        
        # Aktivite listesi
        activities = [
            ("👤 Yeni personel eklendi", "Ahmet Yılmaz - IT Departmanı", "2 saat önce", "#50C878"),
            ("📅 İzin talebi onaylandı", "Ayşe Kaya - 5 günlük yıllık izin", "4 saat önce", "#2196F3"),
            ("💰 Bordro hesaplandı", "Mart 2024 bordroları hazır", "1 gün önce", "#FF9800"),
            ("📊 Performans değerlendirmesi", "Q1 değerlendirmeleri tamamlandı", "2 gün önce", "#9C27B0")
        ]
        
        for title, desc, time, color in activities:
            activity_item = ctk.CTkFrame(activities_frame, fg_color="#252525", corner_radius=10)
            activity_item.pack(fill="x", padx=15, pady=5)
            
            item_content = ctk.CTkFrame(activity_item, fg_color="transparent")
            item_content.pack(fill="x", padx=15, pady=10)
            
            # Sol taraf - bilgi
            info_frame = ctk.CTkFrame(item_content, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)
            
            ctk.CTkLabel(
                info_frame,
                text=title,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color,
                anchor="w"
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=desc,
                font=ctk.CTkFont(size=10),
                text_color="#CCCCCC",
                anchor="w"
            ).pack(anchor="w")
            
            # Sağ taraf - zaman
            ctk.CTkLabel(
                item_content,
                text=time,
                font=ctk.CTkFont(size=9),
                text_color="#888888"
            ).pack(side="right", pady=5)
            
        ctk.CTkFrame(activities_frame, fg_color="transparent", height=10).pack()
        
    def refresh_data(self):
        # Verileri yenile
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "Dashboard verileri güncellendi!")
        
        # Sayfayı yeniden yükle
        for widget in self.winfo_children():
            widget.destroy()
            
        self.create_header()
        self.create_quick_stats()
        self.create_charts_section()
        self.create_recent_activities()