import customtkinter as ctk
from ..security.auth_manager import AuthManager

class UserManagementModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.auth_manager = AuthManager()
        
        self.title("Kullanıcı Yönetimi")
        self.geometry("600x500")
        self.configure(fg_color="#121212")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.create_interface()
        
    def create_interface(self):
        # Başlık
        ctk.CTkLabel(
            self, 
            text="👥 Kullanıcı Yönetimi", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#50C878"
        ).pack(pady=20)
        
        # Yeni kullanıcı ekleme
        add_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        add_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            add_frame, 
            text="Yeni Kullanıcı Ekle", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Form alanları
        form_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        form_frame.pack(padx=20, pady=(0, 15))
        
        # Kullanıcı adı
        user_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        user_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(user_frame, text="Kullanıcı Adı:", width=100, anchor="w").pack(side="left")
        self.username_entry = ctk.CTkEntry(user_frame, width=150)
        self.username_entry.pack(side="left", padx=10)
        
        # Şifre
        pass_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        pass_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(pass_frame, text="Şifre:", width=100, anchor="w").pack(side="left")
        self.password_entry = ctk.CTkEntry(pass_frame, width=150, show="*")
        self.password_entry.pack(side="left", padx=10)
        
        # Rol
        role_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        role_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(role_frame, text="Rol:", width=100, anchor="w").pack(side="left")
        self.role_combo = ctk.CTkComboBox(
            role_frame, 
            values=["admin", "hr_manager", "user"],
            width=150
        )
        self.role_combo.pack(side="left", padx=10)
        
        ctk.CTkButton(
            form_frame,
            text="➕ Kullanıcı Ekle",
            fg_color="#50C878",
            command=self.add_user
        ).pack(pady=10)
        
        # Mevcut kullanıcılar listesi
        list_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            list_frame, 
            text="Mevcut Kullanıcılar", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Kullanıcı listesi
        self.users_frame = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.users_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        self.load_users()
        
    def add_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_combo.get()
        
        if not all([username, password, role]):
            self.show_error("Tüm alanları doldurun!")
            return
            
        try:
            import sqlite3
            conn = sqlite3.connect(self.auth_manager.db_path)
            cursor = conn.cursor()
            
            # Kullanıcı var mı kontrol et
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
            if cursor.fetchone()[0] > 0:
                self.show_error("Bu kullanıcı adı zaten mevcut!")
                conn.close()
                return
            
            # Yeni kullanıcı ekle
            password_hash = self.auth_manager.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            
            conn.commit()
            conn.close()
            
            # Formu temizle
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.role_combo.set("user")
            
            # Listeyi yenile
            self.load_users()
            
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", f"Kullanıcı '{username}' eklendi!")
            
        except Exception as e:
            self.show_error(f"Hata: {str(e)}")
            
    def load_users(self):
        # Mevcut widget'ları temizle
        for widget in self.users_frame.winfo_children():
            widget.destroy()
            
        try:
            import sqlite3
            conn = sqlite3.connect(self.auth_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, username, role, is_active FROM users ORDER BY username")
            users = cursor.fetchall()
            conn.close()
            
            for user in users:
                user_id, username, role, is_active = user
                
                user_frame = ctk.CTkFrame(self.users_frame, fg_color="#2A2A2A")
                user_frame.pack(fill="x", pady=2)
                
                # Kullanıcı bilgileri
                info_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"👤 {username}",
                    font=ctk.CTkFont(size=14, weight="bold")
                ).pack(anchor="w")
                
                role_text = {"admin": "🔑 Admin", "hr_manager": "💼 İK Yöneticisi", "user": "👥 Kullanıcı"}
                ctk.CTkLabel(
                    info_frame,
                    text=role_text.get(role, role),
                    font=ctk.CTkFont(size=12),
                    text_color="#50C878" if is_active else "#F44336"
                ).pack(anchor="w")
                
                # Butonlar
                if username != "admin":  # Admin silinemez
                    btn_frame = ctk.CTkFrame(user_frame, fg_color="transparent")
                    btn_frame.pack(side="right", padx=15, pady=10)
                    
                    status_text = "Pasifleştir" if is_active else "Aktifleştir"
                    status_color = "#FF9800" if is_active else "#50C878"
                    
                    ctk.CTkButton(
                        btn_frame,
                        text=status_text,
                        width=80,
                        height=30,
                        fg_color=status_color,
                        command=lambda uid=user_id, active=is_active: self.toggle_user_status(uid, not active)
                    ).pack(side="left", padx=2)
                    
                    ctk.CTkButton(
                        btn_frame,
                        text="Sil",
                        width=60,
                        height=30,
                        fg_color="#F44336",
                        command=lambda uid=user_id, uname=username: self.delete_user(uid, uname)
                    ).pack(side="left", padx=2)
                    
        except Exception as e:
            self.show_error(f"Kullanıcılar yüklenemedi: {str(e)}")
            
    def toggle_user_status(self, user_id, new_status):
        try:
            import sqlite3
            conn = sqlite3.connect(self.auth_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE users SET is_active = ? WHERE id = ?", (new_status, user_id))
            conn.commit()
            conn.close()
            
            self.load_users()
            
            status_text = "aktifleştirildi" if new_status else "pasifleştirildi"
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self, "Başarılı", f"Kullanıcı {status_text}!")
            
        except Exception as e:
            self.show_error(f"Hata: {str(e)}")
            
    def delete_user(self, user_id, username):
        # Onay penceresi
        confirm = ctk.CTkToplevel(self)
        confirm.title("Kullanıcı Sil")
        confirm.geometry("300x150")
        confirm.configure(fg_color="#121212")
        confirm.transient(self)
        confirm.grab_set()
        
        ctk.CTkLabel(
            confirm,
            text=f"'{username}' kullanıcısını silmek istediğinizden emin misiniz?",
            wraplength=250
        ).pack(pady=20)
        
        btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        def do_delete():
            try:
                import sqlite3
                conn = sqlite3.connect(self.auth_manager.db_path)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                conn.close()
                
                confirm.destroy()
                self.load_users()
                
                from .notification_system import NotificationSystem
                NotificationSystem.show_success(self, "Başarılı", f"Kullanıcı '{username}' silindi!")
                
            except Exception as e:
                self.show_error(f"Hata: {str(e)}")
        
        ctk.CTkButton(btn_frame, text="İptal", fg_color="#666666", command=confirm.destroy).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Sil", fg_color="#F44336", command=do_delete).pack(side="left", padx=5)
        
    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Hata")
        error_window.geometry("300x150")
        error_window.configure(fg_color="#121212")
        error_window.transient(self)
        error_window.grab_set()
        
        ctk.CTkLabel(error_window, text=message, text_color="#F44336", wraplength=250).pack(expand=True)
        ctk.CTkButton(error_window, text="Tamam", command=error_window.destroy).pack(pady=10)