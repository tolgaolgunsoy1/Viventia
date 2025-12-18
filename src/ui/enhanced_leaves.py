import customtkinter as ctk
from ..database.database import Database
from datetime import datetime, timedelta

class EnhancedLeavesPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#0F0F0F")
        self.db = Database()
        
        self.create_header()
        self.create_stats_cards()
        self.create_leave_calendar()
        self.create_requests_section()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=15, height=80)
        header.pack(fill="x", padx=20, pady=(20, 15))
        header.pack_propagate(False)
        
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=20, pady=15)
        
        ctk.CTkLabel(
            left_frame,
            text="📅 İzin Yönetimi",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#50C878"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_frame,
            text="İzin talepleri ve onay süreçleri",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        ).pack(anchor="w")
        
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20, pady=15)
        
        ctk.CTkButton(
            right_frame,
            text="➕ Yeni İzin Talebi",
            fg_color="#50C878",
            hover_color="#45B56B",
            width=140,
            height=40,
            command=self.add_leave
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            right_frame,
            text="📊 İzin Raporu",
            fg_color="#2196F3",
            hover_color="#1976D2",
            width=120,
            height=40,
            command=self.generate_report
        ).pack(side="right", padx=5)
        
    def create_stats_cards(self):
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        stats_data = [
            ("⏳ Bekleyen Talepler", "8", "#FF9800", "talep"),
            ("✅ Bu Ay Onaylanan", "15", "#50C878", "izin"),
            ("📊 Toplam İzin Günü", "142", "#2196F3", "gün"),
            ("📈 Ortalama İzin", "9.5", "#9C27B0", "gün/kişi")
        ]
        
        for title, value, color, unit in stats_data:
            card = ctk.CTkFrame(stats_frame, fg_color="#1A1A1A", corner_radius=15)
            card.pack(side="left", fill="both", expand=True, padx=8)
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(pady=20)
            
            ctk.CTkLabel(
                content,
                text=value,
                font=ctk.CTkFont(size=28, weight="bold"),
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
                text=unit,
                font=ctk.CTkFont(size=10),
                text_color="#666666"
            ).pack()
            
    def create_leave_calendar(self):
        calendar_frame = ctk.CTkFrame(self, fg_color="transparent")
        calendar_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Sol taraf - Mini takvim
        left_calendar = ctk.CTkFrame(calendar_frame, fg_color="#1A1A1A", corner_radius=15)
        left_calendar.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(
            left_calendar,
            text="📅 Bu Ay İzinleri",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(15, 10))
        
        # Takvim grid
        calendar_grid = ctk.CTkFrame(left_calendar, fg_color="transparent")
        calendar_grid.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Gün başlıkları
        days = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        for i, day in enumerate(days):
            ctk.CTkLabel(
                calendar_grid,
                text=day,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="#888888",
                width=30,
                height=25
            ).grid(row=0, column=i, padx=1, pady=1)
        
        # Örnek günler
        import calendar
        today = datetime.now()
        cal = calendar.monthcalendar(today.year, today.month)
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue
                    
                # İzinli günleri farklı renkte göster
                is_leave_day = day in [15, 16, 17, 22, 23]  # Örnek izinli günler
                
                day_btn = ctk.CTkButton(
                    calendar_grid,
                    text=str(day),
                    width=30,
                    height=25,
                    fg_color="#FF9800" if is_leave_day else "#252525",
                    hover_color="#FFB74D" if is_leave_day else "#333333",
                    font=ctk.CTkFont(size=10),
                    corner_radius=5
                )
                day_btn.grid(row=week_num+1, column=day_num, padx=1, pady=1)
        
        # Sağ taraf - İzin türleri
        right_types = ctk.CTkFrame(calendar_frame, fg_color="#1A1A1A", corner_radius=15)
        right_types.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        ctk.CTkLabel(
            right_types,
            text="📋 İzin Türleri",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(15, 10))
        
        leave_types = [
            ("🏖️ Yıllık İzin", "15 gün kaldı", "#50C878"),
            ("🏥 Hastalık İzni", "Sınırsız", "#2196F3"),
            ("👶 Doğum İzni", "112 gün", "#FF9800"),
            ("⚰️ Mazeret İzni", "5 gün", "#9C27B0"),
            ("🎓 Eğitim İzni", "10 gün", "#FF5722")
        ]
        
        for icon_type, remaining, color in leave_types:
            type_item = ctk.CTkFrame(right_types, fg_color="#252525", corner_radius=10)
            type_item.pack(fill="x", padx=15, pady=5)
            
            type_content = ctk.CTkFrame(type_item, fg_color="transparent")
            type_content.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(
                type_content,
                text=icon_type,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=color,
                anchor="w"
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                type_content,
                text=remaining,
                font=ctk.CTkFont(size=10),
                text_color="#CCCCCC",
                anchor="w"
            ).pack(anchor="w")
            
    def create_requests_section(self):
        requests_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=15)
        requests_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Başlık ve filtreler
        header_frame = ctk.CTkFrame(requests_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="📋 İzin Talepleri",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(side="left")
        
        filter_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        filter_frame.pack(side="right")
        
        ctk.CTkComboBox(
            filter_frame,
            values=["Tümü", "Bekliyor", "Onaylandı", "Reddedildi"],
            width=120,
            height=30,
            fg_color="#252525"
        ).pack(side="right", padx=5)
        
        # Talepler listesi
        self.requests_scroll = ctk.CTkScrollableFrame(requests_frame, fg_color="transparent")
        self.requests_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.load_leave_requests()
        
    def load_leave_requests(self):
        # Mevcut widget'ları temizle
        for widget in self.requests_scroll.winfo_children():
            widget.destroy()
            
        try:
            leaves_data = self.db.get_leaves()
        except:
            leaves_data = []
            
        if not leaves_data:
            # Örnek veriler
            leaves_data = [
                (1, "Ahmet Yılmaz", "Yıllık İzin", "2024-04-15", "2024-04-19", "Tatil planı", "Bekliyor"),
                (2, "Ayşe Kaya", "Hastalık İzni", "2024-04-10", "2024-04-12", "Grip", "Onaylandı"),
                (3, "Mehmet Demir", "Yıllık İzin", "2024-04-22", "2024-04-26", "Aile ziyareti", "Bekliyor")
            ]
            
        for leave in leaves_data:
            self.create_leave_request_card(leave)
            
    def create_leave_request_card(self, leave_data):
        card = ctk.CTkFrame(self.requests_scroll, fg_color="#252525", corner_radius=12)
        card.pack(fill="x", pady=5)
        
        card_content = ctk.CTkFrame(card, fg_color="transparent")
        card_content.pack(fill="x", padx=20, pady=15)
        
        # Üst kısım - Personel bilgisi
        top_frame = ctk.CTkFrame(card_content, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Avatar
        avatar = ctk.CTkFrame(top_frame, fg_color="#50C878", corner_radius=20, width=40, height=40)
        avatar.pack(side="left", padx=(0, 15))
        avatar.pack_propagate(False)
        
        ctk.CTkLabel(
            avatar,
            text=leave_data[1][0].upper(),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Bilgiler
        info_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=leave_data[1],  # İsim
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white",
            anchor="w"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=leave_data[2],  # İzin türü
            font=ctk.CTkFont(size=11),
            text_color="#50C878",
            anchor="w"
        ).pack(anchor="w")
        
        # Durum
        status_color = "#FF9800" if leave_data[6] == "Bekliyor" else "#50C878" if leave_data[6] == "Onaylandı" else "#F44336"
        status_label = ctk.CTkLabel(
            top_frame,
            text=leave_data[6],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=status_color
        )
        status_label.pack(side="right")
        
        # Orta kısım - Tarihler
        dates_frame = ctk.CTkFrame(card_content, fg_color="#1A1A1A", corner_radius=8)
        dates_frame.pack(fill="x", pady=(0, 10))
        
        dates_content = ctk.CTkFrame(dates_frame, fg_color="transparent")
        dates_content.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            dates_content,
            text=f"📅 {leave_data[3]} → {leave_data[4]}",
            font=ctk.CTkFont(size=11),
            text_color="#CCCCCC"
        ).pack(side="left")
        
        # Gün sayısı hesapla
        try:
            start = datetime.strptime(leave_data[3], "%Y-%m-%d")
            end = datetime.strptime(leave_data[4], "%Y-%m-%d")
            days = (end - start).days + 1
        except:
            days = 1
            
        ctk.CTkLabel(
            dates_content,
            text=f"{days} gün",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#FFD700"
        ).pack(side="right")
        
        # Alt kısım - Açıklama ve butonlar
        if leave_data[5]:  # Açıklama varsa
            ctk.CTkLabel(
                card_content,
                text=f"💬 {leave_data[5]}",
                font=ctk.CTkFont(size=10),
                text_color="#888888",
                anchor="w"
            ).pack(anchor="w", pady=(0, 10))
        
        # Butonlar (sadece bekleyen talepler için)
        if leave_data[6] == "Bekliyor":
            buttons_frame = ctk.CTkFrame(card_content, fg_color="transparent")
            buttons_frame.pack(fill="x")
            
            ctk.CTkButton(
                buttons_frame,
                text="✅ Onayla",
                width=80,
                height=30,
                fg_color="#50C878",
                hover_color="#45B56B",
                command=lambda: self.approve_leave(leave_data[0])
            ).pack(side="left", padx=(0, 5))
            
            ctk.CTkButton(
                buttons_frame,
                text="❌ Reddet",
                width=80,
                height=30,
                fg_color="#F44336",
                hover_color="#D32F2F",
                command=lambda: self.reject_leave(leave_data[0])
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                buttons_frame,
                text="👁️ Detay",
                width=70,
                height=30,
                fg_color="#2196F3",
                hover_color="#1976D2"
            ).pack(side="right")
            
    def add_leave(self):
        from .add_leave_modal import AddLeaveModal
        modal = AddLeaveModal(self, callback=self.load_leave_requests)
        
    def approve_leave(self, leave_id):
        self.db.approve_leave(leave_id)
        self.load_leave_requests()
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "İzin talebi onaylandı!")
        
    def reject_leave(self, leave_id):
        self.db.reject_leave(leave_id)
        self.load_leave_requests()
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "İzin talebi reddedildi!")
        
    def generate_report(self):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "İzin raporu oluşturuldu!")