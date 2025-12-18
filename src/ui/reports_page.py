import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        
        self.create_header()
        self.create_report_categories()
        self.create_analytics_dashboard()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="İK Raporlama ve Analitik", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
        ctk.CTkButton(
            header,
            text="📊 Rapor Oluştur",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.generate_report
        ).pack(side="right", padx=20, pady=20)
        
    def create_report_categories(self):
        categories_frame = ctk.CTkFrame(self, fg_color="transparent")
        categories_frame.pack(fill="x", pady=(0, 20))
        
        # Rapor kategorileri
        categories = [
            ("Personel Raporları", "#2196F3", ["Personel Listesi", "Departman Analizi", "Yaş Dağılımı"]),
            ("Bordro Raporları", "#50C878", ["Maaş Analizi", "Prim Raporları", "Vergi Hesaplamaları"]),
            ("Devam Raporları", "#FF9800", ["Puantaj Özeti", "İzin Kullanımı", "Fazla Mesai"]),
            ("Performans Raporları", "#9C27B0", ["Değerlendirme Sonuçları", "Hedef Takibi", "KPI Analizi"])
        ]
        
        for i, (title, color, reports) in enumerate(categories):
            if i % 2 == 0:
                row_frame = ctk.CTkFrame(categories_frame, fg_color="transparent")
                row_frame.pack(fill="x", padx=10, pady=5)
            
            category_card = ctk.CTkFrame(row_frame, fg_color="#1E1E1E")
            category_card.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(
                category_card, 
                text=title, 
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            ).pack(pady=(20, 10))
            
            for report in reports:
                report_btn = ctk.CTkButton(
                    category_card,
                    text=report,
                    fg_color="transparent",
                    hover_color=color,
                    anchor="w",
                    height=30
                )
                report_btn.pack(fill="x", padx=20, pady=2)
            
            ctk.CTkFrame(category_card, fg_color="transparent", height=20).pack()
            
    def create_analytics_dashboard(self):
        analytics_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        analytics_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            analytics_frame, 
            text="İK Analitik Dashboard", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        # Grafik alanı
        charts_container = ctk.CTkFrame(analytics_frame, fg_color="transparent")
        charts_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Sol grafik - Turnover analizi
        left_chart = ctk.CTkFrame(charts_container, fg_color="#2A2A2A")
        left_chart.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        fig1, ax1 = plt.subplots(figsize=(4, 3), facecolor='#2A2A2A')
        ax1.set_facecolor('#2A2A2A')
        
        months = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz']
        turnover = [5.2, 4.8, 6.1, 3.9, 4.5, 5.7]
        
        ax1.plot(months, turnover, color='#F44336', marker='o', linewidth=2)
        ax1.set_title('Aylık Turnover Oranı (%)', color='white', fontsize=10)
        ax1.tick_params(colors='white', labelsize=8)
        ax1.grid(True, alpha=0.3)
        
        canvas1 = FigureCanvasTkAgg(fig1, left_chart)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Sağ grafik - Departman dağılımı
        right_chart = ctk.CTkFrame(charts_container, fg_color="#2A2A2A")
        right_chart.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        fig2, ax2 = plt.subplots(figsize=(4, 3), facecolor='#2A2A2A')
        ax2.set_facecolor('#2A2A2A')
        
        departments = ['IT', 'Satış', 'İK', 'Muhasebe', 'Pazarlama']
        sizes = [30, 25, 15, 20, 10]
        colors = ['#50C878', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
        
        wedges, texts, autotexts = ax2.pie(sizes, labels=departments, colors=colors, 
                                          autopct='%1.1f%%', startangle=90)
        
        for text in texts + autotexts:
            text.set_color('white')
            text.set_fontsize(8)
            
        ax2.set_title('Departman Dağılımı', color='white', fontsize=10)
        
        canvas2 = FigureCanvasTkAgg(fig2, right_chart)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Alt KPI'lar
        kpi_frame = ctk.CTkFrame(analytics_frame, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        kpis = [
            ("Ortalama Maaş", "₺12.450", "#50C878"),
            ("Çalışan Memnuniyeti", "%87", "#2196F3"),
            ("Eğitim ROI", "%145", "#FF9800"),
            ("İşe Alım Süresi", "18 gün", "#9C27B0")
        ]
        
        for title, value, color in kpis:
            kpi_card = ctk.CTkFrame(kpi_frame, fg_color="#2A2A2A")
            kpi_card.pack(side="left", fill="both", expand=True, padx=5)
            
            ctk.CTkLabel(
                kpi_card, 
                text=value, 
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=color
            ).pack(pady=(15, 5))
            
            ctk.CTkLabel(
                kpi_card, 
                text=title, 
                font=ctk.CTkFont(size=10),
                text_color="#A0A0A0"
            ).pack(pady=(0, 15))
    
    def generate_report(self):
        # Kapsamlı İK raporu oluştur
        import sqlite3
        from datetime import datetime
        
        try:
            conn = sqlite3.connect("viventia.db")
            cursor = conn.cursor()
            
            # İstatistikleri topla
            cursor.execute("SELECT COUNT(*) FROM employees")
            total_employees = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'Aktif'")
            active_employees = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(salary) FROM employees WHERE status = 'Aktif'")
            avg_salary = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
            dept_stats = cursor.fetchall()
            
            cursor.execute("SELECT COUNT(*) FROM leaves WHERE status = 'Bekliyor'")
            pending_leaves = cursor.fetchone()[0]
            
            conn.close()
            
            # Rapor içeriği oluştur
            today = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            report_content = f"""VİVENTİA İNSAN KAYNAKLARI RAPORU
{'='*60}
Tarih: {today}

GENEL İSTATİSTİKLER
{'-'*30}
Toplam Personel: {total_employees}
Aktif Personel: {active_employees}
Ortalama Maaş: {avg_salary:,.2f} ₺
Bekleyen İzin Talepleri: {pending_leaves}

DEPARTMAN DAĞILIMI
{'-'*30}
"""
            
            for dept, count in dept_stats:
                report_content += f"{dept}: {count} kişi\n"
            
            report_content += f"""

PERFORMANS ÖZETİ
{'-'*30}
Çalışan Memnuniyeti: %87
Ortalama Performans: 4.2/5.0
Eğitim Tamamlama: %94
Turnover Oranı: %5.2

Bu rapor Viventia İK Sistemi tarafından otomatik oluşturulmuştur.
"""
            
            # Dosyaya kaydet
            filename = f"ik_raporu_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report_content)
            
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", f"İK raporu oluşturuldu: {filename}")
            
        except Exception as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", f"Rapor oluşturma hatası: {str(e)}")