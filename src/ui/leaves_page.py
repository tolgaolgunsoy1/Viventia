import customtkinter as ctk
from datetime import datetime, timedelta

class LeavesPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1A1A1A")
        
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
            fg_color="#4ECDC4",
            hover_color="#45B7B8",
            width=100,
            command=self.add_leave
        ).pack(side="left", padx=10)
        
    def create_stats(self):
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats = [
            ("Bekleyen Talepler", "8", "#FF9800"),
            ("Bu Ay Onaylanan", "15", "#4ECDC4"),
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
        self.scrollable = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tablo başlıkları
        header_frame = ctk.CTkFrame(self.scrollable, fg_color="#2A2A2A")
        header_frame.pack(fill="x", pady=(0, 10))
        
        headers = ["Personel", "İzin Türü", "Başlangıç", "Bitiş", "Gün", "Durum", "İşlemler"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=100
            ).grid(row=0, column=i, padx=10, pady=10)
        
        # Veritabanından izin verilerini al
        try:
            from ..database.database import Database
            db = Database()
            leaves_data = db.get_leaves()
        except Exception:
            leaves_data = [
                (1, "Ahmet Yılmaz", "Yıllık İzin", "2024-04-15", "2024-04-19", "Tatil", "Bekliyor"),
                (2, "Ayşe Kaya", "Hastalık İzni", "2024-04-10", "2024-04-12", "Grip", "Onaylandı")
            ]
        
        for leave in leaves_data:
            # Calculate days between dates
            from datetime import datetime
            try:
                start = datetime.strptime(leave[3], "%Y-%m-%d")
                end = datetime.strptime(leave[4], "%Y-%m-%d")
                days = (end - start).days + 1
            except:
                days = 1
            
            # Format data for display
            display_data = (
                leave[0],  # leave_id
                leave[1],  # employee_name
                leave[2],  # leave_type
                leave[3],  # start_date
                leave[4],  # end_date
                str(days), # calculated days
                leave[6]   # status
            )
            self.create_leave_row(self.scrollable, display_data)
            
    def create_leave_row(self, parent, leave_data):
        row_frame = ctk.CTkFrame(parent, fg_color="#1A1A1A")
        row_frame.pack(fill="x", pady=2)
        
        # Veri alanları (skip first element which is ID)
        display_data = leave_data[1:]  # Skip ID
        for i, value in enumerate(display_data):
            if i == 5:  # Durum sütunu
                if value == "Bekliyor":
                    color = "#FF9800"
                elif value == "Onaylandı":
                    color = "#4ECDC4"
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
        if display_data[5] == "Bekliyor":  # Status column
            btn_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            btn_frame.grid(row=0, column=6, padx=10, pady=5)
            
            ctk.CTkButton(
                btn_frame, 
                text="Onayla", 
                width=60, 
                height=25,
                fg_color="#4ECDC4",
                command=lambda: self.approve_leave(leave_data[0])
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(
                btn_frame, 
                text="Reddet", 
                width=60, 
                height=25,
                fg_color="#F44336",
                command=lambda: self.reject_leave(leave_data[0])
            ).pack(side="left", padx=2)
    
    def approve_leave(self, leave_id):
        from ..database.database import Database
        db = Database()
        db.approve_leave(leave_id)
        self.refresh_leaves_list()
        
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "İzin talebi onaylandı!")
    
    def reject_leave(self, leave_id):
        from ..database.database import Database
        db = Database()
        db.reject_leave(leave_id)
        self.refresh_leaves_list()
        
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Başarılı", "İzin talebi reddedildi!")
    
    def refresh_leaves_list(self):
        # Clear existing data
        try:
            for widget in self.scrollable.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and len(self.scrollable.winfo_children()) > 1 and widget != self.scrollable.winfo_children()[0]:
                    widget.destroy()
        except Exception:
            pass
        
        # Reload data
        from ..database.database import Database
        db = Database()
        leaves_data = db.get_leaves()
        
        for leave in leaves_data:
            from datetime import datetime
            try:
                start = datetime.strptime(leave[3], "%Y-%m-%d")
                end = datetime.strptime(leave[4], "%Y-%m-%d")
                days = (end - start).days + 1
            except:
                days = 1
            
            display_data = (
                leave[0], leave[1], leave[2], leave[3], 
                leave[4], str(days), leave[6]
            )
            self.create_leave_row(self.scrollable, display_data)
    
    def add_leave(self):
        from .add_leave_modal import AddLeaveModal
        modal = AddLeaveModal(self, callback=self.refresh_leaves_list)