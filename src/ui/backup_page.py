import customtkinter as ctk
import os
from datetime import datetime
from ..database.database import Database, DatabaseError

class BackupPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")
        self.db = Database()

        # Başlık ve butonlar
        self.create_header()

        # Backup işlemleri
        self.create_backup_section()

        # Restore işlemleri
        self.create_restore_section()

        # Backup listesi
        self.create_backup_list()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="Veritabanı Yedekleme & Geri Yükleme",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)

    def create_backup_section(self):
        backup_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        backup_frame.pack(fill="x", pady=(0, 20), padx=20)

        ctk.CTkLabel(
            backup_frame,
            text="Yedek Oluştur",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            backup_frame,
            text="Veritabanının anlık yedeğini oluşturun. Yedek dosyaları 'backups' klasörüne kaydedilir.",
            wraplength=600
        ).pack(pady=(0, 20))

        ctk.CTkButton(
            backup_frame,
            text="🔄 Yedek Oluştur",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.create_backup
        ).pack(pady=(0, 20))

    def create_restore_section(self):
        restore_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        restore_frame.pack(fill="x", pady=(0, 20), padx=20)

        ctk.CTkLabel(
            restore_frame,
            text="Yedekten Geri Yükle",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF9800"
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            restore_frame,
            text="⚠️  UYARI: Bu işlem mevcut verilerin üzerine yazacaktır. Önemli verileriniz varsa önce yedek alın!",
            text_color="#F44336",
            wraplength=600
        ).pack(pady=(0, 10))

        # Dosya seçimi
        file_frame = ctk.CTkFrame(restore_frame, fg_color="transparent")
        file_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(file_frame, text="Yedek Dosyası:").pack(side="left")

        self.backup_file_entry = ctk.CTkEntry(file_frame, width=400)
        self.backup_file_entry.pack(side="left", padx=(10, 0))

        ctk.CTkButton(
            file_frame,
            text="📁 Seç",
            width=60,
            command=self.select_backup_file
        ).pack(side="right")

        ctk.CTkButton(
            restore_frame,
            text="🔄 Geri Yükle",
            fg_color="#FF9800",
            hover_color="#E68900",
            command=self.restore_backup
        ).pack(pady=(10, 20))

    def create_backup_list(self):
        list_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        ctk.CTkLabel(
            list_frame,
            text="Mevcut Yedekler",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))

        # Scrollable frame for backup list
        self.backup_scrollable = ctk.CTkScrollableFrame(list_frame, fg_color="#2A2A2A")
        self.backup_scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.refresh_backup_list()

    def create_backup(self):
        try:
            backup_path = self.db.create_backup()

            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", f"Yedek oluşturuldu:\n{os.path.basename(backup_path)}")

            self.refresh_backup_list()

        except DatabaseError as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", str(e))

    def select_backup_file(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Yedek Dosyası Seç",
            filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")],
            initialdir="backups"
        )
        if file_path:
            self.backup_file_entry.delete(0, "end")
            self.backup_file_entry.insert(0, file_path)

    def restore_backup(self):
        backup_path = self.backup_file_entry.get().strip()

        if not backup_path:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", "Lütfen bir yedek dosyası seçin!")
            return

        # Onay penceresi
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Geri Yükleme Onayı")
        confirm_window.geometry("400x200")
        confirm_window.configure(fg_color="#121212")
        confirm_window.transient(self)
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text="Bu işlem mevcut tüm verilerin üzerine yazacaktır!\nDevam etmek istediğinizden emin misiniz?",
            wraplength=350,
            text_color="#F44336"
        ).pack(pady=20)

        def confirm_restore():
            confirm_window.destroy()
            try:
                self.db.restore_backup(backup_path)

                from .notification_system import NotificationSystem
                NotificationSystem.show_success(self, "Başarılı", "Veritabanı başarıyla geri yüklendi!")

                # Uygulamayı yeniden başlatma uyarısı
                restart_window = ctk.CTkToplevel(self)
                restart_window.title("Yeniden Başlatma Gerekli")
                restart_window.geometry("300x150")
                restart_window.configure(fg_color="#121212")
                restart_window.transient(self)
                restart_window.grab_set()

                ctk.CTkLabel(
                    restart_window,
                    text="Değişikliklerin etkili olması için\nuygulamayı yeniden başlatın.",
                    wraplength=250
                ).pack(pady=20)

                ctk.CTkButton(
                    restart_window,
                    text="Tamam",
                    command=restart_window.destroy
                ).pack(pady=10)

            except DatabaseError as e:
                from .notification_system import NotificationSystem
                NotificationSystem.show_error(self, "Hata", str(e))

        btn_frame = ctk.CTkFrame(confirm_window, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="İptal",
            fg_color="#666666",
            command=confirm_window.destroy
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Geri Yükle",
            fg_color="#F44336",
            command=confirm_restore
        ).pack(side="right", padx=5)

    def refresh_backup_list(self):
        # Mevcut listeyi temizle
        for widget in self.backup_scrollable.winfo_children():
            widget.destroy()

        try:
            backups = self.db.get_backup_list()

            if not backups:
                ctk.CTkLabel(
                    self.backup_scrollable,
                    text="Henüz yedek bulunmuyor.",
                    text_color="#A0A0A0"
                ).pack(pady=20)
                return

            for backup in backups:
                backup_item = ctk.CTkFrame(self.backup_scrollable, fg_color="#1A1A1A")
                backup_item.pack(fill="x", padx=10, pady=2)

                # Dosya bilgileri
                info_frame = ctk.CTkFrame(backup_item, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

                ctk.CTkLabel(
                    info_frame,
                    text=backup['filename'],
                    font=ctk.CTkFont(weight="bold")
                ).pack(anchor="w")

                size_mb = backup['size'] / (1024 * 1024)
                ctk.CTkLabel(
                    info_frame,
                    text=f"Boyut: {size_mb:.2f} MB | Tarih: {backup['date'].strftime('%d.%m.%Y %H:%M')}",
                    text_color="#A0A0A0",
                    font=ctk.CTkFont(size=12)
                ).pack(anchor="w")

                # İşlem butonları
                btn_frame = ctk.CTkFrame(backup_item, fg_color="transparent")
                btn_frame.pack(side="right", padx=10, pady=5)

                ctk.CTkButton(
                    btn_frame,
                    text="Geri Yükle",
                    width=80,
                    height=25,
                    fg_color="#FF9800",
                    command=lambda path=backup['path']: self.quick_restore(path)
                ).pack(side="left", padx=2)

        except Exception as e:
            ctk.CTkLabel(
                self.backup_scrollable,
                text=f"Yedek listesi yüklenemedi: {str(e)}",
                text_color="#F44336"
            ).pack(pady=20)

    def quick_restore(self, backup_path):
        """Hızlı geri yükleme - dosya seçimi atlanır"""
        self.backup_file_entry.delete(0, "end")
        self.backup_file_entry.insert(0, backup_path)
        self.restore_backup()