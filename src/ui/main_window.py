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
        
        # Pencereyi maksimize et
        self.state('zoomed')
        
        # Pencere ayarları
        self.title("Viventia - İnsan Kaynakları Yönetim Sistemi")
        self.geometry("1500x950")
        self.configure(fg_color="#0F0F0F")
        
        # Pencere ikonunu ayarla
        try:
            self.iconbitmap(default="")
        except:
            pass
        
        # Grid yapılandırması
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Bileşenler
        self.sidebar = Sidebar(self, self.auth_manager)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        # Tema ayarları
        self.configure_theme()
        
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
                from .enhanced_dashboard import EnhancedDashboard
                self.pages[page_name] = EnhancedDashboard(self)
            elif page_name == "Personel":
                from .enhanced_personnel import EnhancedPersonnelPage
                self.pages[page_name] = EnhancedPersonnelPage(self)
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
        top_bar = ctk.CTkFrame(self, fg_color="#1A1A1A", height=60, corner_radius=15)
        top_bar.grid(row=0, column=1, sticky="ew", padx=20, pady=(20, 0))
        top_bar.grid_propagate(False)
        
        if self.auth_manager and self.auth_manager.current_user:
            # Sol taraf - kullanıcı bilgisi
            left_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
            left_frame.pack(side="left", fill="y", padx=20, pady=15)
            
            # Kullanıcı avatarı
            avatar = ctk.CTkFrame(left_frame, fg_color="#50C878", corner_radius=20, width=40, height=40)
            avatar.pack(side="left", padx=(0, 15))
            avatar.pack_propagate(False)
            
            ctk.CTkLabel(
                avatar,
                text=self.auth_manager.current_user['username'][0].upper(),
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="white"
            ).pack(expand=True)
            
            # Kullanıcı bilgileri
            info_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="y")
            
            ctk.CTkLabel(
                info_frame,
                text=f"Hoşgeldin, {self.auth_manager.current_user['username']}",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="white",
                anchor="w"
            ).pack(anchor="w")
            
            role_text = {
                'admin': '🔑 Yönetici',
                'hr_manager': '💼 İK Yöneticisi',
                'user': '👥 Kullanıcı'
            }
            
            ctk.CTkLabel(
                info_frame,
                text=role_text.get(self.auth_manager.current_user['role'], self.auth_manager.current_user['role']),
                font=ctk.CTkFont(size=10),
                text_color="#50C878",
                anchor="w"
            ).pack(anchor="w")
            
            # Sağ taraf - butonlar
            right_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
            right_frame.pack(side="right", fill="y", padx=20, pady=15)
            
            ctk.CTkButton(
                right_frame,
                text="🔔",
                width=40,
                height=40,
                fg_color="#2196F3",
                hover_color="#1976D2",
                corner_radius=20,
                command=self.show_notifications
            ).pack(side="right", padx=5)
            
            ctk.CTkButton(
                right_frame,
                text="🚀 Çıkış",
                fg_color="#F44336",
                hover_color="#D32F2F",
                width=90,
                height=40,
                corner_radius=20,
                command=self.logout
            ).pack(side="right", padx=5)
    
    def show_notifications(self):
        from .notification_system import NotificationSystem
        NotificationSystem.show_success(self, "Bildirimler", "Yeni bildiriminiz yok.")
    
    def configure_theme(self):
        # Modern tema ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
    
    def logout(self):
        if self.auth_manager:
            self.auth_manager.logout()
        self.destroy()
        from .login_window import LoginWindow
        login_app = LoginWindow()
        login_app.mainloop()