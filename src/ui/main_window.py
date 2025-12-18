import customtkinter as ctk
from .sidebar import Sidebar
from .dashboard import Dashboard
from .personnel_page import PersonnelPage
from .recruitment_page import RecruitmentPage
from .attendance_page import AttendancePage
from .payroll_page import PayrollPage
from .leaves_page import LeavesPage
from .performance_page import PerformancePage
from .training_page import TrainingPage
from .reports_page import ReportsPage
from .settings_page import SettingsPage

class MainWindow(ctk.CTk):
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        
        # Pencere ayarları
        self.title("Viventia - İnsan Kaynakları Yönetim Sistemi")
        self.geometry("1400x900")
        self.configure(fg_color="#121212")
        
        # Grid yapılandırması
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Bileşenler
        self.sidebar = Sidebar(self, self.auth_manager)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        # Üst bar - kullanıcı bilgisi
        self.create_top_bar()
        
        # Sayfalar
        self.pages = {}
        self.current_page = None
        
        # İlk sayfa olarak dashboard'u göster
        self.show_page("Dashboard")
        
    def show_page(self, page_name):
        # Mevcut sayfayı gizle
        if self.current_page:
            self.current_page.grid_forget()
        
        # Sayfa yoksa oluştur
        if page_name not in self.pages:
            if page_name == "Dashboard":
                self.pages[page_name] = Dashboard(self)
            elif page_name == "Personel":
                self.pages[page_name] = PersonnelPage(self)
            elif page_name == "İşe Alım":
                self.pages[page_name] = RecruitmentPage(self)
            elif page_name == "Puantaj":
                self.pages[page_name] = AttendancePage(self)
            elif page_name == "Bordro":
                self.pages[page_name] = PayrollPage(self)
            elif page_name == "İzinler":
                self.pages[page_name] = LeavesPage(self)
            elif page_name == "Performans":
                self.pages[page_name] = PerformancePage(self)
            elif page_name == "Eğitim":
                self.pages[page_name] = TrainingPage(self)
            elif page_name == "Raporlar":
                self.pages[page_name] = ReportsPage(self)
            elif page_name == "Ayarlar":
                settings_page = SettingsPage(self)
                settings_page.auth_manager = self.auth_manager
                self.pages[page_name] = settings_page
            else:
                # Diğer sayfalar için placeholder
                self.pages[page_name] = ctk.CTkFrame(self, fg_color="#121212")
                ctk.CTkLabel(
                    self.pages[page_name], 
                    text=f"{page_name} sayfası yakında...",
                    font=ctk.CTkFont(size=24)
                ).pack(expand=True)
        
        # Yeni sayfayı göster
        self.current_page = self.pages[page_name]
        self.current_page.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
    
    def create_top_bar(self):
        top_bar = ctk.CTkFrame(self, fg_color="#1E1E1E", height=50)
        top_bar.grid(row=0, column=1, sticky="ew", padx=20, pady=(20, 0))
        top_bar.grid_propagate(False)
        
        if self.auth_manager and self.auth_manager.current_user:
            user_info = f"Hoşgeldin, {self.auth_manager.current_user['username']} ({self.auth_manager.current_user['role']})"
            ctk.CTkLabel(top_bar, text=user_info, font=ctk.CTkFont(size=12)).pack(side="left", padx=20, pady=15)
            
            ctk.CTkButton(
                top_bar,
                text="Çıkış Yap",
                fg_color="#F44336",
                hover_color="#D32F2F",
                width=80,
                height=30,
                command=self.logout
            ).pack(side="right", padx=20, pady=10)
    
    def logout(self):
        if self.auth_manager:
            self.auth_manager.logout()
        self.destroy()
        from .login_window import LoginWindow
        login_app = LoginWindow()
        login_app.mainloop()