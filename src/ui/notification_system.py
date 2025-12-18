import customtkinter as ctk
from tkinter import messagebox
import threading
import time
from datetime import datetime

class NotificationSystem:
    notifications = []
    
    @staticmethod
    def show_success(parent, title, message):
        """Başarı bildirimi gösterir"""
        NotificationSystem._add_notification("success", title, message)
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_error(parent, title, message):
        """Hata bildirimi gösterir"""
        NotificationSystem._add_notification("error", title, message)
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_warning(parent, title, message):
        """Uyarı bildirimi gösterir"""
        NotificationSystem._add_notification("warning", title, message)
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_info(parent, title, message):
        """Bilgi bildirimi gösterir"""
        NotificationSystem._add_notification("info", title, message)
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_question(parent, title, message):
        """Soru bildirimi gösterir"""
        return messagebox.askyesno(title, message)
    
    @staticmethod
    def show_toast(parent, message, type="info", duration=3000):
        """Toast bildirimi gösterir"""
        toast = ToastNotification(parent, message, type, duration)
        toast.show()
    
    @staticmethod
    def _add_notification(type, title, message):
        """Bildirim geçmişine ekler"""
        notification = {
            "type": type,
            "title": title,
            "message": message,
            "timestamp": datetime.now(),
            "read": False
        }
        NotificationSystem.notifications.insert(0, notification)
        
        # En fazla 50 bildirim tut
        if len(NotificationSystem.notifications) > 50:
            NotificationSystem.notifications = NotificationSystem.notifications[:50]
    
    @staticmethod
    def get_notifications():
        """Tüm bildirimleri getirir"""
        return NotificationSystem.notifications
    
    @staticmethod
    def get_unread_count():
        """Okunmamış bildirim sayısını getirir"""
        return len([n for n in NotificationSystem.notifications if not n["read"]])
    
    @staticmethod
    def mark_all_read():
        """Tüm bildirimleri okundu olarak işaretle"""
        for notification in NotificationSystem.notifications:
            notification["read"] = True

class ToastNotification:
    def __init__(self, parent, message, type="info", duration=3000):
        self.parent = parent
        self.message = message
        self.type = type
        self.duration = duration
        self.toast_window = None
    
    def show(self):
        """Toast bildirimini gösterir"""
        try:
            self.toast_window = ctk.CTkToplevel(self.parent)
            self.toast_window.title("")
            self.toast_window.geometry("350x100")
            self.toast_window.resizable(False, False)
            self.toast_window.attributes("-topmost", True)
            self.toast_window.overrideredirect(True)
            
            # Pencereyi sağ alt köşeye yerleştir
            x = self.parent.winfo_screenwidth() - 370
            y = self.parent.winfo_screenheight() - 150
            self.toast_window.geometry(f"350x100+{x}+{y}")
            
            # Renk seçimi
            colors = {
                "success": "#4CAF50",
                "error": "#F44336",
                "warning": "#FF9800",
                "info": "#2196F3"
            }
            
            icons = {
                "success": "✅",
                "error": "❌",
                "warning": "⚠️",
                "info": "ℹ️"
            }
            
            color = colors.get(self.type, "#2196F3")
            icon = icons.get(self.type, "ℹ️")
            
            # Ana frame
            main_frame = ctk.CTkFrame(
                self.toast_window, 
                fg_color=color, 
                corner_radius=15,
                border_width=2,
                border_color="#FFFFFF"
            )
            main_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            # İçerik frame
            content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=15, pady=15)
            
            # İkon ve mesaj
            header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            header_frame.pack(fill="x")
            
            icon_label = ctk.CTkLabel(
                header_frame,
                text=icon,
                font=ctk.CTkFont(size=20),
                text_color="white"
            )
            icon_label.pack(side="left", padx=(0, 10))
            
            message_label = ctk.CTkLabel(
                header_frame,
                text=self.message,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="white",
                wraplength=250,
                anchor="w"
            )
            message_label.pack(side="left", fill="x", expand=True)
            
            # Kapatma butonu
            close_btn = ctk.CTkButton(
                header_frame,
                text="×",
                width=25,
                height=25,
                fg_color="transparent",
                hover_color="rgba(255,255,255,0.1)",
                text_color="white",
                font=ctk.CTkFont(size=16, weight="bold"),
                command=self.close
            )
            close_btn.pack(side="right")
            
            # Animasyon efekti
            self._animate_in()
            
            # Otomatik kapanma
            threading.Timer(self.duration / 1000, self.close).start()
            
        except Exception as e:
            print(f"Toast notification error: {e}")
    
    def _animate_in(self):
        """Giriş animasyonu"""
        try:
            # Başlangıçta şeffaf
            self.toast_window.attributes("-alpha", 0.0)
            
            # Yavaşça görünür yap
            for i in range(1, 11):
                alpha = i / 10.0
                self.toast_window.attributes("-alpha", alpha)
                self.toast_window.update()
                time.sleep(0.02)
        except:
            pass
    
    def close(self):
        """Toast bildirimini kapatır"""
        try:
            if self.toast_window and self.toast_window.winfo_exists():
                # Çıkış animasyonu
                for i in range(10, 0, -1):
                    alpha = i / 10.0
                    self.toast_window.attributes("-alpha", alpha)
                    self.toast_window.update()
                    time.sleep(0.02)
                
                self.toast_window.destroy()
        except:
            pass

class NotificationPanel(ctk.CTkToplevel):
    """Bildirim paneli"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Bildirimler")
        self.geometry("400x500")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        
        # Pencereyi merkeze yerleştir
        self.center_window()
        
        self.setup_ui()
        self.load_notifications()
    
    def center_window(self):
        """Pencereyi ekranın merkezine yerleştirir"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"400x500+{x}+{y}")
    
    def setup_ui(self):
        """UI bileşenlerini oluşturur"""
        # Başlık
        header_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", height=60)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📢 Bildirimler",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Tümünü okundu işaretle butonu
        mark_read_btn = ctk.CTkButton(
            header_frame,
            text="Tümünü Okundu İşaretle",
            width=150,
            height=30,
            fg_color="#50C878",
            hover_color="#45B068",
            command=self.mark_all_read
        )
        mark_read_btn.pack(side="right", padx=20, pady=15)
        
        # Bildirim listesi
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#1A1A1A",
            scrollbar_button_color="#50C878",
            scrollbar_button_hover_color="#45B068"
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def load_notifications(self):
        """Bildirimleri yükler"""
        notifications = NotificationSystem.get_notifications()
        
        if not notifications:
            no_notif_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="📭 Henüz bildiriminiz yok",
                font=ctk.CTkFont(size=14),
                text_color="#666666"
            )
            no_notif_label.pack(pady=50)
            return
        
        for notification in notifications:
            self.create_notification_item(notification)
    
    def create_notification_item(self, notification):
        """Bildirim öğesi oluşturur"""
        # Renk seçimi
        colors = {
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FF9800",
            "info": "#2196F3"
        }
        
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        color = colors.get(notification["type"], "#2196F3")
        icon = icons.get(notification["type"], "ℹ️")
        
        # Ana frame
        item_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2A2A2A" if notification["read"] else "#3A3A3A",
            corner_radius=10,
            height=80
        )
        item_frame.pack(fill="x", pady=5)
        item_frame.pack_propagate(False)
        
        # Sol taraf - ikon
        icon_frame = ctk.CTkFrame(item_frame, fg_color=color, corner_radius=25, width=50, height=50)
        icon_frame.place(x=15, y=15)
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        icon_label.pack(expand=True)
        
        # Sağ taraf - içerik
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.place(x=80, y=10, width=280, height=60)
        
        # Başlık
        title_label = ctk.CTkLabel(
            content_frame,
            text=notification["title"],
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white",
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        # Mesaj
        message_label = ctk.CTkLabel(
            content_frame,
            text=notification["message"][:50] + "..." if len(notification["message"]) > 50 else notification["message"],
            font=ctk.CTkFont(size=10),
            text_color="#CCCCCC",
            anchor="w"
        )
        message_label.pack(anchor="w")
        
        # Zaman
        time_str = notification["timestamp"].strftime("%d.%m.%Y %H:%M")
        time_label = ctk.CTkLabel(
            content_frame,
            text=time_str,
            font=ctk.CTkFont(size=9),
            text_color="#888888",
            anchor="w"
        )
        time_label.pack(anchor="w", side="bottom")
    
    def mark_all_read(self):
        """Tüm bildirimleri okundu işaretle"""
        NotificationSystem.mark_all_read()
        
        # UI'yi güncelle
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.load_notifications()
        
        # Toast göster
        NotificationSystem.show_toast(
            self.master,
            "Tüm bildirimler okundu olarak işaretlendi",
            "success"
        )