import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#1E1E1E", width=250)
        
        self.parent = parent
        self.grid_propagate(False)
        
        # Logo
        self.logo_label = ctk.CTkLabel(
            self, 
            text="VIVENTIA", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#50C878"
        )
        self.logo_label.pack(pady=(30, 50))
        
        # Menü butonları
        self.buttons = {}
        menu_items = [
            ("Dashboard", "🏠"),
            ("Personel", "👥"),
            ("Bordro", "💰"),
            ("İzinler", "📅"),
            ("Ayarlar", "⚙️")
        ]
        
        for name, icon in menu_items:
            btn = ctk.CTkButton(
                self,
                text=f"{icon}  {name}",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color="#50C878",
                anchor="w",
                height=50,
                command=lambda n=name: self.button_click(n)
            )
            btn.pack(fill="x", padx=20, pady=5)
            self.buttons[name] = btn
        
        # İlk buton seçili
        self.buttons["Dashboard"].configure(fg_color="#50C878")
        
    def button_click(self, name):
        # Tüm butonları sıfırla
        for btn in self.buttons.values():
            btn.configure(fg_color="transparent")
        
        # Seçili butonu vurgula
        self.buttons[name].configure(fg_color="#50C878")
        
        # Ana pencereye bildir
        self.parent.show_page(name)