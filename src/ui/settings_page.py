import customtkinter as ctk
from .settings_manager import SettingsManager

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        self.settings_manager = SettingsManager()
        self.widgets = {}
        
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
        
        # Mevcut ayarları yükle
        current_settings = self.settings_manager.get_all_settings()
        
        # Genel Ayarlar
        self.create_section(container, "Genel Ayarlar", [
            ("Şirket Adı", "entry", current_settings.get("company_name", "Viventia Teknoloji A.Ş.")),
            ("Tema", "combo", ["Koyu Tema", "Açık Tema"]),
            ("Dil", "combo", ["Türkçe", "English"]),
            ("Otomatik Kaydet", "switch", current_settings.get("auto_save", True))
        ])
        
        # Personel Ayarları
        self.create_section(container, "Personel Ayarları", [
            ("Varsayılan İzin Günü", "entry", str(current_settings.get("default_leave_days", 15))),
            ("Deneme Süresi (Ay)", "entry", str(current_settings.get("probation_months", 3))),
            ("Mesai Başlangıç", "entry", current_settings.get("work_start_time", "09:00")),
            ("Mesai Bitiş", "entry", current_settings.get("work_end_time", "18:00"))
        ])
        
        # Bordro Ayarları
        self.create_section(container, "Bordro Ayarları", [
            ("SGK Oranı (%)", "entry", str(current_settings.get("sgk_rate", 14))),
            ("Gelir Vergisi (%)", "entry", str(current_settings.get("income_tax_rate", 15))),
            ("İşsizlik Sigortası (%)", "entry", str(current_settings.get("unemployment_rate", 1))),
            ("Otomatik Hesaplama", "switch", current_settings.get("auto_calculation", True))
        ])
        
        # Butonlar
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(
            btn_frame,
            text="Ayarları Kaydet",
            fg_color="#50C878",
            hover_color="#45B56B",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.save_settings
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Yedek Oluştur",
            fg_color="#2196F3",
            hover_color="#1976D2",
            height=40,
            command=self.create_backup
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Yedek Geri Yükle",
            fg_color="#FF9800",
            hover_color="#F57C00",
            height=40,
            command=self.restore_backup
        ).pack(side="left", padx=10)
        
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
            
            # Widget'ı sakla
            self.widgets[f"{title}_{label}"] = (widget, widget_type)
            
        # Alt boşluk
        ctk.CTkFrame(section, fg_color="transparent", height=20).pack()
        
    def save_settings(self):
        # Tüm widget'lardan değerleri topla
        new_settings = {}
        
        try:
            for key, (widget, widget_type) in self.widgets.items():
                section, field = key.split("_", 1)
                
                if widget_type == "entry":
                    value = widget.get().strip()
                    # Sayısal değerler için dönüştürme
                    if field in ["Varsayılan İzin Günü", "Deneme Süresi (Ay)", "SGK Oranı (%)", "Gelir Vergisi (%)", "İşsizlik Sigortası (%)"]:
                        try:
                            value = int(value) if field in ["Varsayılan İzin Günü", "Deneme Süresi (Ay)"] else float(value)
                        except ValueError:
                            value = 0
                elif widget_type == "combo":
                    value = widget.get()
                elif widget_type == "switch":
                    value = widget.get() == 1
                
                # Ayar anahtarına dönüştür
                setting_key = self.get_setting_key(field)
                if setting_key:
                    new_settings[setting_key] = value
            
            # Ayarları kaydet
            if self.settings_manager.save_settings(new_settings):
                from .notification_system import NotificationSystem
                NotificationSystem.show_success(self, "Başarılı", "Ayarlar başarıyla kaydedildi!")
            else:
                from .notification_system import NotificationSystem
                NotificationSystem.show_error(self, "Hata", "Ayarlar kaydedilemedi!")
                
        except Exception as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", f"Ayar kaydetme hatası: {str(e)}")
    
    def get_setting_key(self, field_name):
        mapping = {
            "Şirket Adı": "company_name",
            "Tema": "theme",
            "Dil": "language",
            "Otomatik Kaydet": "auto_save",
            "Varsayılan İzin Günü": "default_leave_days",
            "Deneme Süresi (Ay)": "probation_months",
            "Mesai Başlangıç": "work_start_time",
            "Mesai Bitiş": "work_end_time",
            "SGK Oranı (%)": "sgk_rate",
            "Gelir Vergisi (%)": "income_tax_rate",
            "İşsizlik Sigortası (%)": "unemployment_rate",
            "Otomatik Hesaplama": "auto_calculation"
        }
        return mapping.get(field_name)
    
    def create_backup(self):
        from ..utils.backup_manager import BackupManager
        
        try:
            backup_manager = BackupManager()
            backup_path = backup_manager.create_backup()
            
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", f"Yedek oluşturuldu:\n{backup_path}")
            
        except Exception as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", str(e))
    
    def restore_backup(self):
        from ..utils.backup_manager import BackupManager
        import tkinter.filedialog as fd
        
        try:
            backup_manager = BackupManager()
            backups = backup_manager.list_backups()
            
            if not backups:
                from .notification_system import NotificationSystem
                NotificationSystem.show_error(self, "Hata", "Hiç yedek dosyası bulunamadı!")
                return
            
            # Basit dosya seçici
            backup_path = fd.askopenfilename(
                title="Yedek Dosyası Seçin",
                filetypes=[("Veritabanı Dosyaları", "*.db")],
                initialdir="backups"
            )
            
            if backup_path:
                backup_manager.restore_backup(backup_path)
                
                from .notification_system import NotificationSystem
                NotificationSystem.show_success(self, "Başarılı", "Yedek başarıyla geri yüklendi!\nUygulama yeniden başlatılacak.")
                
                # Uygulamayı yeniden başlat
                import sys
                import os
                os.execl(sys.executable, sys.executable, *sys.argv)
            
        except Exception as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", str(e))