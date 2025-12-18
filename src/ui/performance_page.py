import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PerformancePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        
        self.create_header()
        self.create_performance_overview()
        self.create_evaluation_list()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="Performans Yönetimi", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.pack(side="right", padx=20, pady=20)
        
        ctk.CTkComboBox(
            controls_frame,
            values=["2024 Q1", "2024 Q2", "2024 Q3", "2024 Q4"],
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            controls_frame,
            text="+ Yeni Değerlendirme",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.add_evaluation
        ).pack(side="left", padx=10)
        
    def create_performance_overview(self):
        overview_frame = ctk.CTkFrame(self, fg_color="transparent")
        overview_frame.pack(fill="x", pady=(0, 20))
        
        # Sol taraf - Performans dağılımı
        chart_frame = ctk.CTkFrame(overview_frame, fg_color="#1E1E1E")
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Performans grafiği
        fig, ax = plt.subplots(figsize=(5, 3), facecolor='#1E1E1E')
        ax.set_facecolor('#1E1E1E')
        
        categories = ['Mükemmel', 'İyi', 'Orta', 'Gelişmeli']
        values = [25, 45, 20, 10]
        colors = ['#50C878', '#2196F3', '#FF9800', '#F44336']
        
        bars = ax.bar(categories, values, color=colors)
        ax.set_title('Performans Dağılımı (%)', color='white', fontsize=12)
        ax.tick_params(colors='white')
        
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                   f'{value}%', ha='center', va='bottom', color='white')
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sağ taraf - KPI'lar
        kpi_frame = ctk.CTkFrame(overview_frame, fg_color="#1E1E1E")
        kpi_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            kpi_frame, 
            text="Performans KPI'ları", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        kpis = [
            ("Ortalama Puan", "4.2/5.0", "#50C878"),
            ("Tamamlanan Hedefler", "%87", "#2196F3"),
            ("Gelişim Planı", "23 kişi", "#FF9800"),
            ("Terfi Adayları", "8 kişi", "#9C27B0")
        ]
        
        for title, value, color in kpis:
            kpi_item = ctk.CTkFrame(kpi_frame, fg_color="transparent")
            kpi_item.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(kpi_item, text=title, anchor="w").pack(side="left")
            ctk.CTkLabel(kpi_item, text=value, text_color=color).pack(side="right")
            
    def create_evaluation_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        list_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            list_frame, 
            text="Son Değerlendirmeler", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(list_frame, fg_color="#2A2A2A")
        header_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        headers = ["Personel", "Değerlendiren", "Dönem", "Puan", "Hedef Tamamlama", "Durum"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=120
            ).grid(row=0, column=i, padx=10, pady=10)
        
        # Örnek değerlendirme verileri
        evaluations = [
            ("Ahmet Yılmaz", "Mehmet Kaya", "2024 Q1", "4.5", "%92", "Tamamlandı"),
            ("Ayşe Demir", "Fatma Özkan", "2024 Q1", "4.2", "%88", "Tamamlandı"),
            ("Murat Şahin", "Ali Veli", "2024 Q1", "3.8", "%75", "Devam Ediyor")
        ]
        
        for evaluation in evaluations:
            self.create_evaluation_row(list_frame, evaluation)
            
    def create_evaluation_row(self, parent, eval_data):
        row_frame = ctk.CTkFrame(parent, fg_color="#1A1A1A")
        row_frame.pack(fill="x", padx=20, pady=2)
        
        for i, value in enumerate(eval_data):
            if i == 3:  # Puan sütunu
                score = float(value)
                if score >= 4.0:
                    color = "#50C878"
                elif score >= 3.0:
                    color = "#FF9800"
                else:
                    color = "#F44336"
            elif i == 5:  # Durum sütunu
                color = "#50C878" if value == "Tamamlandı" else "#FF9800"
            else:
                color = "#FFFFFF"
                
            ctk.CTkLabel(
                row_frame, 
                text=str(value), 
                text_color=color,
                width=120
            ).grid(row=0, column=i, padx=10, pady=8)
    
    def add_evaluation(self):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Bilgi", "Performans değerlendirme özelliği yakında eklenecek!")