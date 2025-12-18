import customtkinter as ctk
from .sidebar import Sidebar
from .dashboard import Dashboard
from .personnel_page import PersonnelPage
from .payroll_page import PayrollPage
from .leaves_page import LeavesPage
from .settings_page import SettingsPage

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Pencere ayarları
        self.title("Viventia - İnsan Kaynakları Yönetim Sistemi")
        self.geometry("1400x900")
        self.configure(fg_color="#121212")
        
        # Grid yapılandırması
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Bileşenler
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
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
            elif page_name == "Bordro":
                self.pages[page_name] = PayrollPage(self)
            elif page_name == "İzinler":
                self.pages[page_name] = LeavesPage(self)
            elif page_name == "Ayarlar":
                self.pages[page_name] = SettingsPage(self)
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
        self.current_page.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)