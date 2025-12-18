import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        
        # Başlık
        self.create_header()
        
        # Ayar kategorileri
        self.create_settings_sections()
        
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header, 
            text="Sistem Ayarları", 
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)
        
    def create_settings_sections(self):
        # Ana container
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)
        
        # Genel Ayarlar
        self.create_section(container, "Genel Ayarlar", [
            ("Şirket Adı", "entry", "Viventia Teknoloji A.Ş."),
            ("Tema", "combo", ["Koyu Tema", "Açık Tema"]),
            ("Dil", "combo", ["Türkçe", "English"]),
            ("Otomatik Kaydet", "switch", True)
        ])
        
        # Personel Ayarları
        self.create_section(container, "Personel Ayarları", [
            ("Varsayılan İzin Günü", "entry", "15"),
            ("Deneme Süresi (Ay)", "entry", "3"),
            ("Mesai Başlangıç", "entry", "09:00"),
            ("Mesai Bitiş", "entry", "18:00")
        ])
        
        # Bordro Ayarları
        self.create_section(container, "Bordro Ayarları", [
            ("SGK Oranı (%)", "entry", "14"),
            ("Gelir Vergisi (%)", "entry", "15"),
            ("İşsizlik Sigortası (%)", "entry", "1"),
            ("Otomatik Hesaplama", "switch", True)
        ])
        
        # Kaydet butonu
        ctk.CTkButton(
            container,
            text="Ayarları Kaydet",
            fg_color="#50C878",
            hover_color="#45B56B",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.save_settings
        ).pack(pady=30)
        
    def create_section(self, parent, title, settings):
        # Bölüm çerçevesi
        section = ctk.CTkFrame(parent, fg_color="#1E1E1E")
        section.pack(fill="x", padx=20, pady=10)
        
        # Başlık
        ctk.CTkLabel(
            section, 
            text=title, 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#50C878"
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Ayarlar
        for label, widget_type, default in settings:
            row = ctk.CTkFrame(section, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(
                row, 
                text=label, 
                width=200,
                anchor="w"
            ).pack(side="left", padx=(0, 20))
            
            if widget_type == "entry":
                widget = ctk.CTkEntry(row, width=200)
                widget.insert(0, str(default))
            elif widget_type == "combo":
                widget = ctk.CTkComboBox(row, values=default, width=200)
                widget.set(default[0])
            elif widget_type == "switch":
                widget = ctk.CTkSwitch(row, text="")
                if default:
                    widget.select()
                    
            widget.pack(side="right")
            
        # Alt boşluk
        ctk.CTkFrame(section, fg_color="transparent", height=20).pack()
        
    def save_settings(self):
        # Ayarları kaydet
        print("Ayarlar kaydedildi!")