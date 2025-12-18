import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime, timedelta
from ..database.database import Database

class EnhancedDashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F0F0F")
        self.db = Database()
        
        # Ana scroll frame
        self.main_scroll = ctk.CTkScrollableFrame(
            self, 
            fg_color="#0F0F0F",
            scrollbar_button_color="#50C878",
            scrollbar_button_hover_color="#45B068"
        )
        self.main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_welcome_section()
        self.create_quick_stats()
        self.create_charts_section()
        self.create_recent_activities()
        self.create_quick_actions()
        
    def create_welcome_section(self):
        """Hoşgeldin bölümü"""
        welcome_frame = ctk.CTkFrame(self.main_scroll, fg_color="#1A1A1A", corner_radius=15, height=120)
        welcome_frame.pack(fill="x", pady=(0, 20))
        welcome_frame.pack_propagate(False)
        
        # Sol taraf - Hoşgeldin mesajı
        left_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=30, pady=25)
        
        current_time = datetime.now()
        if current_time.hour < 12:
            greeting = "Günaydın"
        elif current_time.hour < 18:
            greeting = "İyi günler"
        else:
            greeting = "İyi akşamlar"
        
        ctk.CTkLabel(
            left_frame,
            text=f"{greeting}! 👋",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#50C878",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_frame,
            text=f"Bugün {current_time.strftime('%d %B %Y, %A')}",
            font=ctk.CTkFont(size=14),
            text_color="#CCCCCC",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        ctk.CTkLabel(
            left_frame,
            text="Viventia HR Dashboard'a hoşgeldiniz",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))
        
        # Sağ taraf - Hızlı bilgiler
        right_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=30, pady=25)
        
        # Sistem durumu
        status_card = ctk.CTkFrame(right_frame, fg_color="#2A2A2A", corner_radius=10, width=200, height=70)
        status_card.pack()
        status_card.pack_propagate(False)
        
        ctk.CTkLabel(
            status_card,
            text="🟢 Sistem Durumu",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(10, 2))
        
        ctk.CTkLabel(
            status_card,
            text="Tüm sistemler çalışıyor",
            font=ctk.CTkFont(size=10),
            text_color="#CCCCCC"
        ).pack(pady=(0, 10))
    
    def create_quick_stats(self):
        """Hızlı istatistikler"""
        stats_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Başlık
        ctk.CTkLabel(
            stats_frame,
            text="📊 Genel Bakış",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(0, 15))
        
        # İstatistik kartları container
        cards_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
        cards_container.pack(fill="x")
        
        # Veritabanından gerçek veriler al
        try:
            total, active, pending_leaves = self.db.get_employee_stats()
            employees = self.db.get_employees()
            
            # Departman sayısı
            departments = set(emp[2] for emp in employees if emp[2])  # emp[2] = department
            dept_count = len(departments)
            
            # Bu ay işe başlayanlar
            current_month = datetime.now().strftime("%Y-%m")
            new_hires = len([emp for emp in employees if emp[5] and emp[5].startswith(current_month)])  # emp[5] = hire_date
            
        except Exception as e:
            total, active, pending_leaves, dept_count, new_hires = 0, 0, 0, 0, 0
        
        # Kart verileri
        cards_data = [
            {
                "title": "Toplam Personel",
                "value": str(total),
                "icon": "👥",
                "color": "#50C878",
                "bg_color": "#1A2F1A"
            },
            {
                "title": "Aktif Çalışan",
                "value": str(active),
                "icon": "✅",
                "color": "#4CAF50",
                "bg_color": "#1A2A1A"
            },
            {
                "title": "Bekleyen İzinler",
                "value": str(pending_leaves),
                "icon": "📅",
                "color": "#FF9800",
                "bg_color": "#2A1F0A"
            },
            {
                "title": "Departman Sayısı",
                "value": str(dept_count),
                "icon": "🏢",
                "color": "#2196F3",
                "bg_color": "#0A1A2A"
            },
            {
                "title": "Bu Ay Yeni",
                "value": str(new_hires),
                "icon": "🆕",
                "color": "#9C27B0",
                "bg_color": "#2A0A2A"
            }
        ]
        
        # Kartları oluştur
        for i, card_data in enumerate(cards_data):
            card = ctk.CTkFrame(
                cards_container, 
                fg_color=card_data["bg_color"], 
                corner_radius=15,
                width=200,
                height=120
            )
            card.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            card.pack_propagate(False)
            
            # İkon
            ctk.CTkLabel(
                card,
                text=card_data["icon"],
                font=ctk.CTkFont(size=24)
            ).pack(pady=(15, 5))
            
            # Değer
            ctk.CTkLabel(
                card,
                text=card_data["value"],
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color=card_data["color"]
            ).pack(pady=(0, 2))
            
            # Başlık
            ctk.CTkLabel(
                card,
                text=card_data["title"],
                font=ctk.CTkFont(size=11),
                text_color="#CCCCCC"
            ).pack(pady=(0, 15))
        
        # Grid yapılandırması
        for i in range(5):
            cards_container.grid_columnconfigure(i, weight=1)
    
    def create_charts_section(self):
        """Grafik bölümü"""
        charts_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        charts_frame.pack(fill="x", pady=(0, 20))
        
        # Başlık
        ctk.CTkLabel(
            charts_frame,
            text="📈 Analitik Veriler",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(0, 15))
        
        # Grafik container
        charts_container = ctk.CTkFrame(charts_frame, fg_color="transparent")
        charts_container.pack(fill="x")
        
        # Sol grafik - Personel durumu (Donut Chart)
        left_chart_frame = ctk.CTkFrame(charts_container, fg_color="#1A1A1A", corner_radius=15)
        left_chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.create_status_chart(left_chart_frame)
        
        # Sağ grafik - Departman dağılımı (Bar Chart)
        right_chart_frame = ctk.CTkFrame(charts_container, fg_color="#1A1A1A", corner_radius=15)
        right_chart_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.create_department_chart(right_chart_frame)
    
    def create_status_chart(self, parent):
        """Personel durumu donut chart"""
        # Başlık
        ctk.CTkLabel(
            parent,
            text="Personel Durumu",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 10))
        
        # Matplotlib figure
        fig, ax = plt.subplots(figsize=(5, 4), facecolor='#1A1A1A')
        ax.set_facecolor('#1A1A1A')
        
        try:
            employees = self.db.get_employees()
            status_counts = {}
            for emp in employees:
                status = emp[6] if len(emp) > 6 and emp[6] else "Aktif"  # emp[6] = status
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                labels = list(status_counts.keys())
                sizes = list(status_counts.values())
                colors = ['#50C878', '#FF9800', '#F44336', '#2196F3'][:len(labels)]
            else:
                labels = ['Veri Yok']
                sizes = [1]
                colors = ['#666666']
                
        except Exception as e:
            labels = ['Aktif', 'İzinli', 'Pasif']
            sizes = [70, 20, 10]
            colors = ['#50C878', '#FF9800', '#F44336']
        
        # Donut chart oluştur
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops=dict(width=0.6, edgecolor='#1A1A1A'),
            textprops={'color': 'white', 'fontsize': 10}
        )
        
        # Merkez daire
        centre_circle = plt.Circle((0, 0), 0.40, fc='#1A1A1A')
        fig.gca().add_artist(centre_circle)
        
        ax.axis('equal')
        
        # Canvas oluştur
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        plt.close(fig)
    
    def create_department_chart(self, parent):
        """Departman dağılımı bar chart"""
        # Başlık
        ctk.CTkLabel(
            parent,
            text="Departman Dağılımı",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 10))
        
        # Matplotlib figure
        fig, ax = plt.subplots(figsize=(5, 4), facecolor='#1A1A1A')
        ax.set_facecolor('#1A1A1A')
        
        try:
            employees = self.db.get_employees()
            dept_counts = {}
            for emp in employees:
                dept = emp[2] if len(emp) > 2 and emp[2] else "Diğer"  # emp[2] = department
                dept_counts[dept] = dept_counts.get(dept, 0) + 1
            
            if dept_counts:
                departments = list(dept_counts.keys())
                counts = list(dept_counts.values())
            else:
                departments = ['Veri Yok']
                counts = [0]
                
        except Exception as e:
            departments = ['IT', 'İK', 'Satış', 'Muhasebe', 'Pazarlama']
            counts = [15, 8, 12, 6, 9]
        
        # Bar chart oluştur
        bars = ax.bar(departments, counts, color='#50C878', alpha=0.8, edgecolor='#45B068')
        
        # Grafik stilini ayarla
        ax.set_xlabel('Departmanlar', color='white', fontsize=10)
        ax.set_ylabel('Personel Sayısı', color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=9)
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Bar üzerinde değerleri göster
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   str(count), ha='center', va='bottom', color='white', fontsize=9)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Canvas oluştur
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        plt.close(fig)
    
    def create_recent_activities(self):
        """Son aktiviteler"""
        activities_frame = ctk.CTkFrame(self.main_scroll, fg_color="#1A1A1A", corner_radius=15)
        activities_frame.pack(fill="x", pady=(0, 20))
        
        # Başlık
        header_frame = ctk.CTkFrame(activities_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="🕒 Son Aktiviteler",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(side="left")
        
        ctk.CTkButton(
            header_frame,
            text="Tümünü Gör",
            width=80,
            height=25,
            fg_color="#50C878",
            hover_color="#45B068",
            font=ctk.CTkFont(size=10)
        ).pack(side="right")
        
        # Aktivite listesi
        activities_list = ctk.CTkFrame(activities_frame, fg_color="transparent")
        activities_list.pack(fill="x", padx=20, pady=(0, 20))
        
        # Örnek aktiviteler
        activities = [
            {
                "icon": "👤",
                "title": "Yeni personel eklendi",
                "description": "Ahmet Yılmaz - IT Departmanı",
                "time": "2 saat önce",
                "color": "#50C878"
            },
            {
                "icon": "📅",
                "title": "İzin talebi onaylandı",
                "description": "Ayşe Kaya - Yıllık İzin",
                "time": "4 saat önce",
                "color": "#2196F3"
            },
            {
                "icon": "💰",
                "title": "Bordro işlendi",
                "description": "Aralık 2024 bordroları",
                "time": "1 gün önce",
                "color": "#FF9800"
            },
            {
                "icon": "📊",
                "title": "Performans değerlendirmesi",
                "description": "Q4 değerlendirmeleri tamamlandı",
                "time": "2 gün önce",
                "color": "#9C27B0"
            }
        ]
        
        for activity in activities:
            activity_item = ctk.CTkFrame(activities_list, fg_color="#2A2A2A", corner_radius=10)
            activity_item.pack(fill="x", pady=5)
            
            # Sol taraf - ikon
            icon_frame = ctk.CTkFrame(activity_item, fg_color=activity["color"], corner_radius=20, width=40, height=40)
            icon_frame.pack(side="left", padx=15, pady=15)
            icon_frame.pack_propagate(False)
            
            ctk.CTkLabel(
                icon_frame,
                text=activity["icon"],
                font=ctk.CTkFont(size=16),
                text_color="white"
            ).pack(expand=True)
            
            # Orta - içerik
            content_frame = ctk.CTkFrame(activity_item, fg_color="transparent")
            content_frame.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=15)
            
            ctk.CTkLabel(
                content_frame,
                text=activity["title"],
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
                anchor="w"
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                content_frame,
                text=activity["description"],
                font=ctk.CTkFont(size=10),
                text_color="#CCCCCC",
                anchor="w"
            ).pack(anchor="w")
            
            # Sağ taraf - zaman
            ctk.CTkLabel(
                activity_item,
                text=activity["time"],
                font=ctk.CTkFont(size=9),
                text_color="#888888"
            ).pack(side="right", padx=15, pady=15)
    
    def create_quick_actions(self):
        """Hızlı işlemler"""
        actions_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 20))
        
        # Başlık
        ctk.CTkLabel(
            actions_frame,
            text="⚡ Hızlı İşlemler",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w", pady=(0, 15))
        
        # Buton container
        buttons_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_container.pack(fill="x")
        
        # Hızlı işlem butonları
        quick_actions = [
            {
                "text": "👤 Yeni Personel",
                "color": "#50C878",
                "hover_color": "#45B068"
            },
            {
                "text": "📅 İzin Talebi",
                "color": "#2196F3",
                "hover_color": "#1976D2"
            },
            {
                "text": "💰 Bordro İşle",
                "color": "#FF9800",
                "hover_color": "#F57C00"
            },
            {
                "text": "📊 Rapor Al",
                "color": "#9C27B0",
                "hover_color": "#7B1FA2"
            },
            {
                "text": "⚙️ Ayarlar",
                "color": "#607D8B",
                "hover_color": "#455A64"
            }
        ]
        
        for i, action in enumerate(quick_actions):
            btn = ctk.CTkButton(
                buttons_container,
                text=action["text"],
                fg_color=action["color"],
                hover_color=action["hover_color"],
                width=180,
                height=50,
                font=ctk.CTkFont(size=12, weight="bold"),
                corner_radius=12
            )
            btn.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
        
        # Grid yapılandırması
        for i in range(5):
            buttons_container.grid_columnconfigure(i, weight=1)