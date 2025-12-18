import customtkinter as ctk
from ..security.auth_manager import AuthManager

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.auth_manager = AuthManager()
        self.main_app = None
        
        self.title("Viventia - Giriş")
        self.geometry("500x550")
        self.configure(fg_color="#0A0A0A")
        self.resizable(False, False)
        
        # Pencereyi merkeze al
        self.center_window()
        
        self.create_login_form()
        
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"500x550+{x}+{y}")
        
    def create_login_form(self):
        # Gradient arka plan efekti
        bg_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=0)
        bg_frame.pack(fill="both", expand=True)
        
        # Ana container
        main_container = ctk.CTkFrame(bg_frame, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Logo bölümü
        logo_section = ctk.CTkFrame(main_container, fg_color="transparent")
        logo_section.pack(pady=(0, 30))
        
        # Logo ikonu
        logo_icon = ctk.CTkFrame(logo_section, fg_color="#50C878", corner_radius=25, width=80, height=80)
        logo_icon.pack(pady=(0, 15))
        logo_icon.pack_propagate(False)
        
        ctk.CTkLabel(
            logo_icon,
            text="V",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Şirket adı
        ctk.CTkLabel(
            logo_section,
            text="VIVENTIA",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#50C878"
        ).pack()
        
        ctk.CTkLabel(
            logo_section,
            text="İnsan Kaynakları Yönetim Sistemi",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        ).pack(pady=(5, 0))
        
        # Giriş formu
        form_container = ctk.CTkFrame(main_container, fg_color="#252525", corner_radius=20)
        form_container.pack(fill="x", pady=(0, 20))
        
        # Form başlığı
        ctk.CTkLabel(
            form_container,
            text="Sisteme Giriş Yapın",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        ).pack(pady=(25, 20))
        
        # Input alanları
        inputs_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        inputs_frame.pack(padx=30, pady=(0, 25))
        
        # Kullanıcı adı alanı
        user_container = ctk.CTkFrame(inputs_frame, fg_color="#1A1A1A", corner_radius=12)
        user_container.pack(fill="x", pady=(0, 15))
        
        user_inner = ctk.CTkFrame(user_container, fg_color="transparent")
        user_inner.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            user_inner,
            text="👤",
            font=ctk.CTkFont(size=18)
        ).pack(side="left", padx=(0, 12))
        
        self.username_entry = ctk.CTkEntry(
            user_inner,
            placeholder_text="Kullanıcı Adınız",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            height=35
        )
        self.username_entry.pack(side="left", fill="x", expand=True)
        
        # Şifre alanı
        pass_container = ctk.CTkFrame(inputs_frame, fg_color="#1A1A1A", corner_radius=12)
        pass_container.pack(fill="x", pady=(0, 20))
        
        pass_inner = ctk.CTkFrame(pass_container, fg_color="transparent")
        pass_inner.pack(fill="x", padx=15, pady=12)
        
        ctk.CTkLabel(
            pass_inner,
            text="🔒",
            font=ctk.CTkFont(size=18)
        ).pack(side="left", padx=(0, 12))
        
        self.password_entry = ctk.CTkEntry(
            pass_inner,
            placeholder_text="Şifreniz",
            show="•",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            height=35
        )
        self.password_entry.pack(side="left", fill="x", expand=True)
        
        # Giriş butonu
        login_btn = ctk.CTkButton(
            inputs_frame,
            text="Giriş Yap",
            command=self.login,
            fg_color="#50C878",
            hover_color="#45B56B",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12
        )
        login_btn.pack(fill="x", pady=(0, 10))
        
        # Alt bilgi
        info_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        info_frame.pack()
        
        ctk.CTkLabel(
            info_frame,
            text="Güvenli ve hızlı İK yönetimi",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        ).pack()
        
        # Klavye kısayolları
        self.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Focus
        self.username_entry.focus()
        

        

    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_error("⚠️ Kullanıcı adı ve şifre gerekli!")
            return
            
        # Direkt giriş kontrolü
        if self.auth_manager.login(username, password):
            self.destroy()
            self.open_main_app()
        else:
            self.show_error("❌ Geçersiz kullanıcı adı veya şifre!")
            self.password_entry.delete(0, 'end')
            
    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Giriş Hatası")
        error_window.geometry("350x180")
        error_window.configure(fg_color="#1A1A1A")
        error_window.transient(self)
        error_window.grab_set()
        error_window.resizable(False, False)
        
        # Pencereyi merkeze al
        x = self.winfo_x() + 75
        y = self.winfo_y() + 185
        error_window.geometry(f"350x180+{x}+{y}")
        
        # Hata ikonu ve mesaj
        content_frame = ctk.CTkFrame(error_window, fg_color="#252525", corner_radius=15)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            content_frame,
            text="⚠️",
            font=ctk.CTkFont(size=32)
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            content_frame,
            text=message,
            text_color="#FF6B6B",
            font=ctk.CTkFont(size=13),
            wraplength=280
        ).pack(pady=(0, 15))
        
        ctk.CTkButton(
            content_frame,
            text="Tamam",
            command=error_window.destroy,
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            width=100,
            height=35,
            corner_radius=8
        ).pack(pady=(0, 20))
        
    def open_main_app(self):
        from .main_window import MainWindow
        self.main_app = MainWindow(self.auth_manager)
        self.main_app.mainloop()