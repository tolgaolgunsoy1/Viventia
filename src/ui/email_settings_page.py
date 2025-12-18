import customtkinter as ctk
from ..utils.email_service import email_service
from ..utils.error_handler import error_handler

class EmailSettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#121212")

        # Başlık
        self.create_header()

        # E-posta yapılandırma formu
        self.create_email_config_form()

        # Test bölümü
        self.create_test_section()

        # Mevcut ayarları yükle
        self.load_current_config()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#1E1E1E", height=80)
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="E-posta Bildirim Ayarları",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=20)

        ctk.CTkLabel(
            header,
            text="📧",
            font=ctk.CTkFont(size=32)
        ).pack(side="right", padx=20, pady=20)

    def create_email_config_form(self):
        config_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        config_frame.pack(fill="x", pady=(0, 20), padx=20)

        ctk.CTkLabel(
            config_frame,
            text="SMTP Yapılandırması",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(20, 10))

        # Form alanları
        form_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=(0, 20))

        # SMTP Server
        server_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        server_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(server_frame, text="SMTP Sunucusu:", width=150, anchor="w").pack(side="left")
        self.server_entry = ctk.CTkEntry(server_frame, width=300)
        self.server_entry.pack(side="left", padx=(10, 0))

        # Port
        port_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        port_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(port_frame, text="Port:", width=150, anchor="w").pack(side="left")
        self.port_entry = ctk.CTkEntry(port_frame, width=300)
        self.port_entry.pack(side="left", padx=(10, 0))

        # Kullanıcı adı
        username_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        username_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(username_frame, text="Kullanıcı Adı:", width=150, anchor="w").pack(side="left")
        self.username_entry = ctk.CTkEntry(username_frame, width=300)
        self.username_entry.pack(side="left", padx=(10, 0))

        # Şifre
        password_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(password_frame, text="Şifre:", width=150, anchor="w").pack(side="left")
        self.password_entry = ctk.CTkEntry(password_frame, width=300, show="*")
        self.password_entry.pack(side="left", padx=(10, 0))

        # Gönderen e-posta
        from_email_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        from_email_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(from_email_frame, text="Gönderen E-posta:", width=150, anchor="w").pack(side="left")
        self.from_email_entry = ctk.CTkEntry(from_email_frame, width=300)
        self.from_email_entry.pack(side="left", padx=(10, 0))

        # TLS kullanımı
        tls_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        tls_frame.pack(fill="x", pady=5)

        self.tls_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            tls_frame,
            text="TLS Kullan (Güvenli bağlantı)",
            variable=self.tls_var
        ).pack(side="left")

        # Kaydet butonu
        ctk.CTkButton(
            config_frame,
            text="💾 Ayarları Kaydet",
            fg_color="#50C878",
            hover_color="#45B56B",
            command=self.save_config
        ).pack(pady=(10, 20))

    def create_test_section(self):
        test_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        test_frame.pack(fill="x", pady=(0, 20), padx=20)

        ctk.CTkLabel(
            test_frame,
            text="Bağlantı Testi",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF9800"
        ).pack(pady=(20, 10))

        # Test e-posta
        test_email_frame = ctk.CTkFrame(test_frame, fg_color="transparent")
        test_email_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(test_email_frame, text="Test E-posta Adresi:").pack(side="left")
        self.test_email_entry = ctk.CTkEntry(test_email_frame, width=300)
        self.test_email_entry.pack(side="left", padx=(10, 0))

        # Test butonları
        buttons_frame = ctk.CTkFrame(test_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        ctk.CTkButton(
            buttons_frame,
            text="🔗 Bağlantıyı Test Et",
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=self.test_connection
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            buttons_frame,
            text="📧 Test E-posta Gönder",
            fg_color="#FF9800",
            hover_color="#E68900",
            command=self.send_test_email
        ).pack(side="left")

    def load_current_config(self):
        """Mevcut yapılandırmayı yükler"""
        config = email_service.config

        self.server_entry.insert(0, config.get('smtp_server', ''))
        self.port_entry.insert(0, str(config.get('smtp_port', 587)))
        self.username_entry.insert(0, config.get('username', ''))
        self.password_entry.insert(0, config.get('password', ''))
        self.from_email_entry.insert(0, config.get('from_email', ''))
        self.tls_var.set(config.get('use_tls', True))

    def save_config(self):
        """Yapılandırmayı kaydeder"""
        try:
            config = {
                'smtp_server': self.server_entry.get().strip(),
                'smtp_port': int(self.port_entry.get().strip()),
                'username': self.username_entry.get().strip(),
                'password': self.password_entry.get().strip(),
                'from_email': self.from_email_entry.get().strip(),
                'use_tls': self.tls_var.get()
            }

            # Validasyon
            if not config['smtp_server']:
                raise ValueError("SMTP sunucusu gerekli")
            if not config['username']:
                raise ValueError("Kullanıcı adı gerekli")
            if not config['password']:
                raise ValueError("Şifre gerekli")

            email_service.save_config(config)

            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", "E-posta ayarları kaydedildi!")

        except ValueError as e:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", str(e))
        except Exception as e:
            error_handler.handle_error(e, "E-posta ayarları kaydetme")

    def test_connection(self):
        """SMTP bağlantısını test eder"""
        success, message = email_service.test_connection()

        if success:
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", message)
        else:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Bağlantı Hatası", message)

    def send_test_email(self):
        """Test e-posta gönderir"""
        test_email = self.test_email_entry.get().strip()

        if not test_email:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", "Test e-posta adresi gerekli")
            return

        subject = "Viventia HR - E-posta Testi"
        body = """
        Merhaba,

        Bu bir test e-postasıdır. E-posta yapılandırmanız çalışıyor!

        Viventia İnsan Kaynakları Sistemi
        """

        html_body = """
        <html>
        <body>
            <h2>E-posta Testi</h2>
            <p>Merhaba,</p>
            <p>Bu bir <strong>test e-postasıdır</strong>. E-posta yapılandırmanız çalışıyor!</p>
            <p>Viventia İnsan Kaynakları Sistemi</p>
        </body>
        </html>
        """

        if email_service.send_email(test_email, subject, body, html_body):
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", f"Test e-posta {test_email} adresine gönderildi!")
        else:
            from .notification_system import NotificationSystem
            NotificationSystem.show_error(self, "Hata", "Test e-posta gönderilemedi")