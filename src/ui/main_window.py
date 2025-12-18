import customtkinter as ctk
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
from .backup_page import BackupPage
from ..utils.error_handler import error_handler, safe_execute

class MainWindow(ctk.CTk):
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        
        # Pencereyi maksimize et
        self.state('zoomed')
        
        # Pencere ayarları
        self.title("Viventia - İnsan Kaynakları Yönetim Sistemi")
        self.geometry("1500x950")
        self.configure(fg_color="#1A1A1A")
        
        # Pencere ikonunu ayarla
        try:
            self.iconbitmap(default="")
        except:
            pass
        
        # Grid yapılandırması
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Bileşenler
        from .sidebar import Sidebar
        self.sidebar = Sidebar(self, self.auth_manager)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        # Tema ayarları
        self.configure_theme()
        
        # Üst bar - kullanıcı bilgisi
        self.create_top_bar()
        
        # Hata yakalama
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Sayfalar
        self.pages = {}
        self.current_page = None
        
        # İlk sayfa olarak dashboard'u göster
        self.show_page("Dashboard")
        
    def show_page(self, page_name):
        """Sayfa gösterme işlemi"""
        def _show_page():
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
                    from .enhanced_payroll import EnhancedPayrollPage
                    self.pages[page_name] = EnhancedPayrollPage(self)
                elif page_name == "İzinler":
                    from .enhanced_leaves import EnhancedLeavesPage
                    self.pages[page_name] = EnhancedLeavesPage(self)
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
                elif page_name == "Yedekleme":
                    self.pages[page_name] = BackupPage(self)
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
        
        safe_execute(_show_page, context=f"Sayfa gösterme: {page_name}")
    
    def create_top_bar(self):
        """Üst bar oluşturma"""
        top_bar = ctk.CTkFrame(self, fg_color="#2B2B2B", height=70, corner_radius=15)
        top_bar.grid(row=0, column=1, sticky="ew", padx=20, pady=(20, 0))
        top_bar.grid_propagate(False)
        
        # Sol taraf - sistem durumu
        left_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=5)
        
        # Basit sistem durumu
        status_label = ctk.CTkLabel(
            left_frame,
            text="🟢 Sistem Aktif",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#4ECDC4"
        )
        status_label.pack(expand=True)
        
        # Sağ taraf - hızlı erişim
        right_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20, pady=15)
        
        # Hızlı erişim butonları
        quick_buttons = [
            ("🔔", "Bildirimler", "#2196F3", self.show_notifications),
            ("📊", "Raporlar", "#FF9800", lambda: self.show_page("Raporlar")),
            ("⚙️", "Ayarlar", "#9C27B0", lambda: self.show_page("Ayarlar"))
        ]
        
        for icon, tooltip, color, command in quick_buttons:
            btn = ctk.CTkButton(
                right_frame,
                text=icon,
                width=40,
                height=40,
                fg_color=color,
                hover_color=self._darken_color(color),
                corner_radius=20,
                command=lambda cmd=command: safe_execute(cmd, context=f"Hızlı erişim: {tooltip}")
            )
            btn.pack(side="right", padx=3)
            
            # Tooltip ekle (basit implementasyon)
            self._add_tooltip(btn, tooltip)
    
    def show_notifications(self):
        """Bildirim panelini gösterir"""
        try:
            from .notification_system import NotificationPanel
            panel = NotificationPanel(self)
            panel.focus()
        except Exception as e:
            error_handler.show_success("Yeni bildiriminiz yok.", "Bildirimler")
    
    def configure_theme(self):
        """Tema yapılandırması"""
        try:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("green")
            error_handler.log_info("Tema başarıyla yapılandırıldı")
        except Exception as e:
            error_handler.handle_error(e, "Tema yapılandırması", show_user=False)
    
    def logout(self):
        """Çıkış işlemi"""
        def _logout():
            if self.auth_manager:
                self.auth_manager.logout()
            self.destroy()
            from .login_window import LoginWindow
            login_app = LoginWindow()
            login_app.mainloop()
        
        safe_execute(_logout, context="Çıkış işlemi")
    
    def on_closing(self):
        """Pencere kapatma işlemi"""
        import sys
        self.quit()
        self.destroy()
        sys.exit()
    
    def _darken_color(self, color):
        """Rengi koyulaştırır"""
        color_map = {
            "#2196F3": "#1976D2",
            "#FF9800": "#F57C00", 
            "#9C27B0": "#7B1FA2"
        }
        return color_map.get(color, color)
    
    def _add_tooltip(self, widget, text):
        """Basit tooltip ekleme"""
        def on_enter(event):
            widget.configure(cursor="hand2")
        
        def on_leave(event):
            widget.configure(cursor="")
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)