import customtkinter as ctk
from ..security.auth_manager import AuthManager

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.auth_manager = AuthManager()
        self.main_app = None
        
        self.title("Viventia - Giriş")
        self.geometry("450x400")
        self.configure(fg_color="#0F0F0F")
        self.resizable(False, False)
        
        # Pencereyi merkeze al
        self.center_window()
        
        self.create_login_form()
        
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"450x400+{x}+{y}")
        
    def create_login_form(self):
        # Logo ve başlık
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=(40, 20))
        
        ctk.CTkLabel(
            logo_frame,
            text="🏛️",
            font=ctk.CTkFont(size=48)
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="VIVENTIA",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color="#50C878"
        ).pack()
        
        ctk.CTkLabel(
            logo_frame,
            text="İnsan Kaynakları Yönetim Sistemi",
            font=ctk.CTkFont(size=13),
            text_color="#A0A0A0"
        ).pack(pady=(5, 0))
        
        # Form container
        form_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=15)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(
            form_frame,
            text="Giriş Yap",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(30, 25))
        
        # Kullanıcı adı
        username_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        username_frame.pack(pady=8)
        
        ctk.CTkLabel(
            username_frame,
            text="👤",
            font=ctk.CTkFont(size=20)
        ).pack(side="left", padx=(0, 10))
        
        self.username_entry = ctk.CTkEntry(
            username_frame,
            placeholder_text="Kullanıcı Adı",
            width=220,
            height=45,
            font=ctk.CTkFont(size=13),
            corner_radius=10
        )
        self.username_entry.pack(side="left")
        
        # Şifre
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(pady=8)
        
        ctk.CTkLabel(
            password_frame,
            text="🔒",
            font=ctk.CTkFont(size=20)
        ).pack(side="left", padx=(0, 10))
        
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Şifre",
            show="•",
            width=220,
            height=45,
            font=ctk.CTkFont(size=13),
            corner_radius=10
        )
        self.password_entry.pack(side="left")
        
        # Giriş butonu
        login_btn = ctk.CTkButton(
            form_frame,
            text="➡️  Giriş Yap",
            command=self.login,
            fg_color="#50C878",
            hover_color="#45B56B",
            width=270,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            corner_radius=10
        )
        login_btn.pack(pady=20)
        
        # Enter tuşu ile giriş
        self.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        

        

    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_error("⚠️ Kullanıcı adı ve şifre gerekli!")
            return
            
        if self.auth_manager.login(username, password):
            self.destroy()
            self.open_main_app()
        else:
            self.show_error("❌ Geçersiz kullanıcı adı veya şifre!")
            self.password_entry.delete(0, 'end')
            
    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Hata")
        error_window.geometry("300x150")
        error_window.configure(fg_color="#121212")
        error_window.transient(self)
        error_window.grab_set()
        
        # Pencereyi merkeze al
        x = self.winfo_x() + 75
        y = self.winfo_y() + 125
        error_window.geometry(f"300x150+{x}+{y}")
        
        ctk.CTkLabel(
            error_window,
            text=message,
            text_color="#F44336",
            wraplength=250
        ).pack(expand=True)
        
        ctk.CTkButton(
            error_window,
            text="Tamam",
            command=error_window.destroy,
            fg_color="#F44336"
        ).pack(pady=10)
        
    def open_main_app(self):
        from .main_window import MainWindow
        self.main_app = MainWindow(self.auth_manager)
        self.main_app.mainloop()