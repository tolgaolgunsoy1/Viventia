import customtkinter as ctk
from datetime import datetime

class PayrollPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        
        # Başlık
        self.create_header()
        
        # Bordro özeti
        self.create_summary()
        
        # Bordro listesi
        self.create_payroll_list()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="Bordro Yönetimi", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
        # Ay seçici
        month_frame = ctk.CTkFrame(header, fg_color="transparent")
        month_frame.pack(side="right", padx=20, pady=20)
        
        ctk.CTkLabel(month_frame, text="Ay:").pack(side="left", padx=5)
        
        month_combo = ctk.CTkComboBox(
            month_frame,
            values=["Ocak 2024", "Şubat 2024", "Mart 2024", "Nisan 2024"],
            width=120
        )
        month_combo.pack(side="left", padx=5)
        month_combo.set("Nisan 2024")
        
    def create_summary(self):
        summary_frame = ctk.CTkFrame(self, fg_color="transparent")
        summary_frame.pack(fill="x", pady=(0, 20))
        
        summaries = [
            ("Toplam Maaş", "1.847.500 ₺", "#50C878"),
            ("Toplam Prim", "125.000 ₺", "#2196F3"),
            ("Toplam Kesinti", "89.200 ₺", "#FF9800"),
            ("Net Ödeme", "1.883.300 ₺", "#4CAF50")
        ]
        
        for title, amount, color in summaries:
            card = ctk.CTkFrame(summary_frame, fg_color="#1E1E1E")
            card.pack(side="left", fill="both", expand=True, padx=10)
            
            ctk.CTkLabel(
                card, 
                text=amount, 
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=color
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                card, 
                text=title, 
                font=ctk.CTkFont(size=12),
                text_color="#A0A0A0"
            ).pack(pady=(0, 20))
            
    def create_payroll_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        list_frame.pack(fill="both", expand=True)
        
        # Başlık
        ctk.CTkLabel(
            list_frame, 
            text="Nisan 2024 Bordro Listesi", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(list_frame, fg_color="#2A2A2A")
        header_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        headers = ["Personel", "Brüt Maaş", "Prim", "Kesinti", "Net Maaş", "Durum"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=i, padx=15, pady=10)
        
        # Örnek bordro verileri
        payroll_data = [
            ("Ahmet Yılmaz", "15.000", "2.500", "1.200", "16.300", "Ödendi"),
            ("Ayşe Kaya", "12.000", "1.800", "950", "12.850", "Ödendi"),
            ("Mehmet Demir", "10.000", "1.500", "800", "10.700", "Bekliyor"),
            ("Fatma Özkan", "11.000", "1.200", "900", "11.300", "Ödendi"),
            ("Ali Şahin", "9.500", "1.000", "750", "9.750", "Bekliyor")
        ]
        
        for data in payroll_data:
            row_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=2)
            
            for i, value in enumerate(data):
                if i == 5:  # Durum sütunu
                    color = "#50C878" if value == "Ödendi" else "#FF9800"
                elif i in [1, 2, 3, 4]:  # Para sütunları
                    value = value + " ₺"
                    color = "#FFFFFF"
                else:
                    color = "#FFFFFF"
                    
                ctk.CTkLabel(
                    row_frame, 
                    text=value, 
                    text_color=color
                ).grid(row=0, column=i, padx=15, pady=5)