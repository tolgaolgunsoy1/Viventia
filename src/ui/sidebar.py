import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, auth_manager=None):
        super().__init__(parent, fg_color="#2C3E50", width=250)
        
        self.parent = parent
        self.auth_manager = auth_manager
        self.grid_propagate(False)
        
        # Logo
        self.logo_label = ctk.CTkLabel(
            self, 
            text="VIVENTIA", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        self.logo_label.pack(pady=(30, 50))
        
        # Menü butonları
        self.buttons = {}
        menu_items = [
            ("Dashboard", "🏠"),
            ("Personel", "👥"),
            ("İşe Alım", "🎯"),
            ("Puantaj", "⏰"),
            ("Bordro", "💰"),
            ("İzinler", "📅"),
            ("Performans", "📊"),
            ("Eğitim", "📚"),
            ("Raporlar", "📊"),
            ("Yedekleme", "💾"),
            ("E-posta", "📧"),
            ("Ayarlar", "⚙️")
        ]
        
        for name, icon in menu_items:
            btn = ctk.CTkButton(
                self,
                text=f"{icon}  {name}",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color="#34495E",
                anchor="w",
                height=50,
                command=lambda n=name: self.button_click(n)
            )
            btn.pack(fill="x", padx=20, pady=5)
            self.buttons[name] = btn
        
        # İlk buton seçili
        self.buttons["Dashboard"].configure(fg_color="#34495E")
        
        # Çıkış butonu
        exit_btn = ctk.CTkButton(
            self,
            text="🚪 Çıkış",
            font=ctk.CTkFont(size=14),
            fg_color="#DC3545",
            hover_color="#C82333",
            height=50,
            command=self.exit_app
        )
        exit_btn.pack(fill="x", padx=20, pady=(20, 30), side="bottom")
        
    def button_click(self, name):
        try:
            # Tüm butonları sıfırla
            for btn in self.buttons.values():
                btn.configure(fg_color="transparent")
            
            # Seçili butonu vurgula
            self.buttons[name].configure(fg_color="#34495E")
            
            # Ana pencereye bildir
            self.after_idle(lambda: self.parent.show_page(name))
        except:
            pass
    
    def exit_app(self):
        # Uygulamayı kapat
        import sys
        self.parent.quit()
        self.parent.destroy()
        sys.exit()