import customtkinter as ctk
from ..security.auth_manager import AuthManager

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.auth_manager = AuthManager()
        self.main_app = None
        
        self.title("Viventia - Giriş")
        self.geometry("400x500")
        self.configure(fg_color="#121212")
        self.resizable(False, False)
        
        # Pencereyi merkeze al
        self.center_window()
        
        self.create_login_form()
        
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"400x500+{x}+{y}")
        
    def create_login_form(self):
        # Logo
        ctk.CTkLabel(
            self,
            text="VIVENTIA",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(60, 20))
        
        ctk.CTkLabel(
            self,
            text="İnsan Kaynakları Yönetim Sistemi",
            font=ctk.CTkFont(size=14),
            text_color="#A0A0A0"
        ).pack(pady=(0, 40))
        
        # Form container
        form_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", width=300, height=250)
        form_frame.pack(pady=20, padx=50, fill="both", expand=True)
        form_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            form_frame,
            text="Giriş Yap",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(30, 20))
        
        # Kullanıcı adı
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Kullanıcı Adı",
            width=250,
            height=40
        )
        self.username_entry.pack(pady=10)
        
        # Şifre
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Şifre",
            show="*",
            width=250,
            height=40
        )
        self.password_entry.pack(pady=10)
        
        # Giriş butonu
        login_btn = ctk.CTkButton(
            form_frame,
            text="Giriş Yap",
            command=self.login,
            fg_color="#50C878",
            hover_color="#45B56B",
            width=250,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        login_btn.pack(pady=20)
        
        # Enter tuşu ile giriş
        self.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Demo bilgileri
        demo_frame = ctk.CTkFrame(self, fg_color="#2A2A2A")
        demo_frame.pack(pady=10, padx=50, fill="x")
        
        ctk.CTkLabel(
            demo_frame,
            text="Demo Giriş: admin / admin123",
            font=ctk.CTkFont(size=12),
            text_color="#A0A0A0"
        ).pack(pady=10)
        
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_error("Kullanıcı adı ve şifre gerekli!")
            return
            
        if self.auth_manager.login(username, password):
            self.destroy()
            self.open_main_app()
        else:
            self.show_error("Geçersiz kullanıcı adı veya şifre!")
            self.password_entry.delete(0, 'end')
            
    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Hata")
        error_window.geometry("300x150")
        error_window.configure(fg_color="#121212")
        error_window.transient(self)
        error_window.grab_set()
        
        # Pencereyi merkeze al
        x = self.winfo_x() + 50
        y = self.winfo_y() + 100
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