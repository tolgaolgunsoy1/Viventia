import customtkinter as ctk
from ..utils.error_handler import error_handler, safe_execute

class EnhancedSidebar(ctk.CTkFrame):
    def __init__(self, parent, auth_manager=None):
        super().__init__(parent, fg_color="#1E1E1E", width=280, corner_radius=0)
        
        self.parent = parent
        self.auth_manager = auth_manager
        self.grid_propagate(False)
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI bileşenlerini oluşturur"""
        # Logo bölümü
        self.create_logo_section()
        
        # Kullanıcı bilgi kartı
        self.create_user_card()
        
        # Menü butonları
        self.create_menu_buttons()
        
        # Alt bölüm
        self.create_footer()
    
    def create_logo_section(self):
        """Logo bölümünü oluşturur"""
        logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        logo_frame.pack(fill="x", padx=20, pady=(20, 10))
        logo_frame.pack_propagate(False)
        
        # Logo
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="VIVENTIA",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#50C878"
        )
        logo_label.pack(pady=10)
        
        # Slogan
        slogan_label = ctk.CTkLabel(
            logo_frame,
            text="İnsan Kaynakları Yönetimi",
            font=ctk.CTkFont(size=11),
            text_color="#A0A0A0"
        )
        slogan_label.pack()
    
    def create_user_card(self):
        """Kullanıcı bilgi kartını oluşturur"""
        if not self.auth_manager or not self.auth_manager.current_user:
            return
            
        user_card = ctk.CTkFrame(self, fg_color="#2A2A2A", corner_radius=15, height=80)
        user_card.pack(fill="x", padx=20, pady=(0, 20))
        user_card.pack_propagate(False)
        
        # Avatar
        avatar_frame = ctk.CTkFrame(user_card, fg_color="#50C878", corner_radius=25, width=50, height=50)
        avatar_frame.place(x=15, y=15)
        avatar_frame.pack_propagate(False)
        
        avatar_text = self.auth_manager.current_user['username'][0].upper()
        ctk.CTkLabel(
            avatar_frame,
            text=avatar_text,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Kullanıcı bilgileri
        info_frame = ctk.CTkFrame(user_card, fg_color="transparent")
        info_frame.place(x=75, y=15, width=180, height=50)
        
        username_label = ctk.CTkLabel(
            info_frame,
            text=self.auth_manager.current_user['username'],
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="white",
            anchor="w"
        )
        username_label.pack(anchor="w")
        
        role_text = {
            'admin': '🔑 Yönetici',
            'hr_manager': '💼 İK Yöneticisi', 
            'user': '👥 Kullanıcı'
        }
        
        role_label = ctk.CTkLabel(
            info_frame,
            text=role_text.get(self.auth_manager.current_user['role'], 'Kullanıcı'),
            font=ctk.CTkFont(size=10),
            text_color="#50C878",
            anchor="w"
        )
        role_label.pack(anchor="w")
    
    def create_menu_buttons(self):
        """Menü butonlarını oluşturur"""
        self.buttons = {}
        
        # Menü kategorileri
        menu_categories = [
            {
                "title": "ANA MENÜ",
                "items": [
                    ("Dashboard", "🏠", True),
                    ("Personel", "👥", True),
                    ("İşe Alım", "🎯", True)
                ]
            },
            {
                "title": "İŞLEMLER",
                "items": [
                    ("Puantaj", "⏰", True),
                    ("Bordro", "💰", True),
                    ("İzinler", "📅", True),
                    ("Performans", "📊", True)
                ]
            },
            {
                "title": "YÖNETİM",
                "items": [
                    ("Eğitim", "📚", True),
                    ("Raporlar", "📈", True),
                    ("Yedekleme", "💾", self._check_admin_access()),
                    ("Ayarlar", "⚙️", self._check_admin_access())
                ]
            }
        ]
        
        for category in menu_categories:
            # Kategori başlığı
            category_label = ctk.CTkLabel(
                self,
                text=category["title"],
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color="#666666",
                anchor="w"
            )
            category_label.pack(fill="x", padx=30, pady=(15, 5))
            
            # Kategori butonları
            for name, icon, enabled in category["items"]:
                if enabled:
                    btn = ctk.CTkButton(
                        self,
                        text=f"{icon}  {name}",
                        font=ctk.CTkFont(size=13),
                        fg_color="transparent",
                        hover_color="#50C878",
                        anchor="w",
                        height=45,
                        corner_radius=10,
                        command=lambda n=name: safe_execute(
                            self.button_click, n, 
                            context=f"Menü buton tıklama: {n}"
                        )
                    )
                    btn.pack(fill="x", padx=20, pady=2)
                    self.buttons[name] = btn
        
        # İlk buton seçili
        if "Dashboard" in self.buttons:
            self.buttons["Dashboard"].configure(fg_color="#50C878")
    
    def create_footer(self):
        """Alt bölümü oluşturur"""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        footer_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        footer_frame.pack_propagate(False)
        
        # Çıkış butonu
        logout_btn = ctk.CTkButton(
            footer_frame,
            text="🚪 Çıkış Yap",
            font=ctk.CTkFont(size=12),
            fg_color="#F44336",
            hover_color="#D32F2F",
            height=40,
            corner_radius=10,
            command=lambda: safe_execute(
                self.logout, 
                context="Çıkış yapma işlemi"
            )
        )
        logout_btn.pack(fill="x")
    
    def _check_admin_access(self):
        """Admin erişim kontrolü"""
        if not self.auth_manager or not self.auth_manager.current_user:
            return False
        return self.auth_manager.current_user['role'] in ['admin', 'hr_manager']
    
    def button_click(self, name):
        """Menü buton tıklama işlemi"""
        try:
            # Tüm butonları sıfırla
            for btn in self.buttons.values():
                btn.configure(fg_color="transparent")
            
            # Seçili butonu vurgula
            if name in self.buttons:
                self.buttons[name].configure(fg_color="#50C878")
            
            # Ana pencereye bildir
            if hasattr(self.parent, 'show_page'):
                self.parent.show_page(name)
            
            error_handler.log_info(f"Sayfa değiştirildi: {name}")
            
        except Exception as e:
            error_handler.handle_error(e, f"Menü navigasyonu: {name}")
    
    def logout(self):
        """Çıkış işlemi"""
        try:
            if error_handler.confirm_action(
                "Çıkış yapmak istediğinizden emin misiniz?",
                "Çıkış Onayı"
            ):
                if self.auth_manager:
                    self.auth_manager.logout()
                
                error_handler.log_info("Kullanıcı çıkış yaptı")
                
                # Ana pencereyi kapat ve login'e dön
                self.parent.destroy()
                
                from .login_window import LoginWindow
                login_app = LoginWindow()
                login_app.mainloop()
                
        except Exception as e:
            error_handler.handle_error(e, "Çıkış işlemi")
    
    def update_user_info(self):
        """Kullanıcı bilgilerini günceller"""
        try:
            # Kullanıcı kartını yeniden oluştur
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget.cget("fg_color") == "#2A2A2A":
                    widget.destroy()
                    break
            
            self.create_user_card()
            
        except Exception as e:
            error_handler.handle_error(e, "Kullanıcı bilgisi güncelleme")