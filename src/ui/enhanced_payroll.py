import customtkinter as ctk
from ..database.database import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EnhancedPayrollPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F0F0F")
        self.db = Database()
        
        self.create_header()
        self.create_payroll_summary()
        self.create_charts_section()
        self.create_payroll_list()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=15, height=80)
        header.pack(fill="x", padx=20, pady=(20, 15))
        header.pack_propagate(False)
        
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=20, pady=15)
        
        ctk.CTkLabel(
            left_frame,
            text="💰 Bordro Yönetimi",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#50C878"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_frame,
            text="Nisan 2024 - Maaş hesaplamaları ve ödemeler",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        ).pack(anchor="w")
        
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20, pady=15)
        
        ctk.CTkButton(
            right_frame,
            text="🧮 Bordro Hesapla",
            fg_color="#50C878",
            hover_color="#45B56B",
            width=130,
            height=40,
            command=self.calculate_payroll
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            right_frame,
            text="📊 Rapor Al",
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=100,
            height=40,
            command=self.generate_report
        ).pack(side="right", padx=5)
        
        # Ay seçici
        ctk.CTkComboBox(
            right_frame,
            values=["Ocak 2024", "Şubat 2024", "Mart 2024", "Nisan 2024"],
            width=120,
            height=40,
            fg_color="#252525"
        ).pack(side="right", padx=5)
        
    def create_payroll_summary(self):
        summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        summary_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        summary_data = [
            ("💵 Toplam Brüt", "1.847.500 ₺", "#50C878", "maaş"),
            ("🎁 Toplam Prim", "125.000 ₺", "#2196F3", "prim"),
            ("📉 Toplam Kesinti", "289.200 ₺", "#FF9800", "kesinti"),
            ("💳 Net Ödeme", "1.683.300 ₺", "#9C27B0", "ödeme")
        ]
        
        for title, amount, color, desc in summary_data:
            card = ctk.CTkFrame(summary_frame, fg_color="#1A1A1A", corner_radius=15)
            card.pack(side="left", fill="both", expand=True, padx=8)
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(pady=20)
            
            ctk.CTkLabel(
                content,
                text=amount,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=color
            ).pack()
            
            ctk.CTkLabel(
                content,
                text=title,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white"
            ).pack()
            
            ctk.CTkLabel(
                content,
                text=desc,
                font=ctk.CTkFont(size=10),
                text_color="#666666"
            ).pack()
            
    def create_charts_section(self):
        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Sol grafik - Maaş dağılımı
        left_chart = ctk.CTkFrame(charts_frame, fg_color="#1A1A1A", corner_radius=15)
        left_chart.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            left_chart,
            text="📊 Departman Maaş Dağılımı",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(15, 10))
        
        self.create_salary_chart(left_chart)
        
        # Sağ grafik - Aylık trend
        right_chart = ctk.CTkFrame(charts_frame, fg_color="#1A1A1A", corner_radius=15)
        right_chart.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            right_chart,
            text="📈 Aylık Bordro Trendi",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(15, 10))
        
        self.create_trend_chart(right_chart)
        
    def create_salary_chart(self, parent):
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#1A1A1A')
        ax.set_facecolor('#1A1A1A')
        
        departments = ['IT', 'Satış', 'Muhasebe', 'İK', 'Pazarlama']
        salaries = [450000, 320000, 280000, 180000, 150000]
        colors = ['#50C878', '#2196F3', '#FF9800', '#9C27B0', '#F44336']
        
        bars = ax.bar(departments, salaries, color=colors)
        
        # Değerleri bars üzerine ekle
        for bar, salary in zip(bars, salaries):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5000,
                   f'{salary/1000:.0f}K₺', ha='center', va='bottom', 
                   color='white', fontsize=9)
        
        ax.set_ylabel('Toplam Maaş (₺)', color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=9)
        ax.grid(True, alpha=0.2, color='white')
        
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_alpha(0.3)
            
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_trend_chart(self, parent):
        fig, ax = plt.subplots(figsize=(4, 3), facecolor='#1A1A1A')
        ax.set_facecolor('#1A1A1A')
        
        months = ['Eki', 'Kas', 'Ara', 'Oca', 'Şub', 'Mar', 'Nis']
        gross_pay = [1650, 1720, 1850, 1680, 1750, 1820, 1847]
        net_pay = [1420, 1480, 1590, 1450, 1510, 1570, 1683]
        
        ax.plot(months, gross_pay, color='#50C878', marker='o', linewidth=2, label='Brüt Maaş')
        ax.plot(months, net_pay, color='#2196F3', marker='s', linewidth=2, label='Net Maaş')
        
        ax.set_ylabel('Toplam Maaş (K₺)', color='white', fontsize=10)
        ax.tick_params(colors='white', labelsize=9)
        ax.grid(True, alpha=0.2, color='white')
        ax.legend(loc='upper left', fontsize=9)
        
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_alpha(0.3)
            
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_payroll_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=15)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Başlık
        header_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="📋 Nisan 2024 Bordro Listesi",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(side="left")
        
        # Filtreler
        filter_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        filter_frame.pack(side="right")
        
        ctk.CTkComboBox(
            filter_frame,
            values=["Tümü", "Ödendi", "Bekliyor", "Onay Bekliyor"],
            width=120,
            height=30,
            fg_color="#252525"
        ).pack(side="right", padx=5)
        
        # Bordro listesi
        self.payroll_scroll = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.payroll_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.load_payroll_data()
        
    def load_payroll_data(self):
        # Örnek bordro verileri
        payroll_data = [
            ("Ahmet Yılmaz", "IT", 15000, 2500, 2200, 15300, "Ödendi"),
            ("Ayşe Kaya", "İK", 12000, 1800, 1750, 12050, "Ödendi"),
            ("Mehmet Demir", "Satış", 10000, 1500, 1450, 10050, "Bekliyor"),
            ("Fatma Özkan", "Muhasebe", 11000, 1200, 1600, 10600, "Ödendi"),
            ("Ali Şahin", "Pazarlama", 9500, 1000, 1350, 9150, "Bekliyor"),
            ("Zeynep Yurt", "IT", 14000, 2200, 2050, 14150, "Ödendi"),
            ("Murat Kaya", "Satış", 11500, 1800, 1675, 11625, "Onay Bekliyor")
        ]
        
        for payroll in payroll_data:
            self.create_payroll_card(payroll)
            
    def create_payroll_card(self, payroll_data):
        card = ctk.CTkFrame(self.payroll_scroll, fg_color="#252525", corner_radius=12)
        card.pack(fill="x", pady=5)
        
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="x", padx=20, pady=15)
        
        # Sol taraf - Personel bilgisi
        left_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        # Avatar
        avatar = ctk.CTkFrame(left_frame, fg_color="#50C878", corner_radius=25, width=50, height=50)
        avatar.pack(side="left", padx=(0, 15))
        avatar.pack_propagate(False)
        
        ctk.CTkLabel(
            avatar,
            text=payroll_data[0][0].upper(),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Bilgiler
        info_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            info_frame,
            text=payroll_data[0],  # İsim
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=payroll_data[1],  # Departman
            font=ctk.CTkFont(size=11),
            text_color="#50C878",
            anchor="w"
        ).pack(anchor="w")
        
        # Orta - Maaş detayları
        middle_frame = ctk.CTkFrame(card_content, fg_color="#1A1A1A", corner_radius=8)
        middle_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        middle_content = ctk.CTkFrame(middle_frame, fg_color="transparent")
        middle_content.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Üst satır
        top_row = ctk.CTkFrame(middle_content, fg_color="transparent")
        top_row.pack(fill="x")
        
        ctk.CTkLabel(
            top_row,
            text=f"💰 Brüt: {payroll_data[2]:,} ₺",
            font=ctk.CTkFont(size=11),
            text_color="#FFD700"
        ).pack(side="left")
        
        ctk.CTkLabel(
            top_row,
            text=f"🎁 Prim: {payroll_data[3]:,} ₺",
            font=ctk.CTkFont(size=11),
            text_color="#2196F3"
        ).pack(side="right")
        
        # Alt satır
        bottom_row = ctk.CTkFrame(middle_content, fg_color="transparent")
        bottom_row.pack(fill="x", pady=(5, 0))
        
        ctk.CTkLabel(
            bottom_row,
            text=f"📉 Kesinti: {payroll_data[4]:,} ₺",
            font=ctk.CTkFont(size=11),
            text_color="#FF9800"
        ).pack(side="left")
        
        ctk.CTkLabel(
            bottom_row,
            text=f"💳 Net: {payroll_data[5]:,} ₺",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#50C878"
        ).pack(side="right")
        
        # Sağ taraf - Durum ve butonlar
        right_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        # Durum
        status_color = "#50C878" if payroll_data[6] == "Ödendi" else "#FF9800" if payroll_data[6] == "Bekliyor" else "#2196F3"
        status_label = ctk.CTkLabel(
            right_frame,
            text=payroll_data[6],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=status_color
        )
        status_label.pack(pady=(0, 10))
        
        # Butonlar
        if payroll_data[6] != "Ödendi":
            ctk.CTkButton(
                right_frame,
                text="✅ Onayla" if payroll_data[6] == "Onay Bekliyor" else "💳 Öde",
                width=80,
                height=30,
                fg_color="#50C878",
                hover_color="#45B56B",
                command=lambda: self.process_payment(payroll_data[0])
            ).pack(pady=2)
            
        ctk.CTkButton(
            right_frame,
            text="📄 Detay",
            width=80,
            height=30,
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=lambda: self.show_payroll_detail(payroll_data[0])
        ).pack(pady=2)
        
    def calculate_payroll(self):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "Bordro hesaplamaları tamamlandı!")
        
    def generate_report(self):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "Bordro raporu oluşturuldu!")
        
    def process_payment(self, employee_name):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", f"{employee_name} için ödeme işlemi tamamlandı!")
        
    def show_payroll_detail(self, employee_name):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Bilgi", f"{employee_name} bordro detayları görüntüleniyor...")