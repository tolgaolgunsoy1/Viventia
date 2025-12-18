import customtkinter as ctk
import sys
import os
import traceback
from src.ui.login_window import LoginWindow
from src.utils.error_handler import error_handler
from src.database.database import Database

def check_dependencies():
    """Gerekli kütüphaneleri kontrol eder"""
    required_modules = [
        'customtkinter',
        'matplotlib', 
        'PIL',
        'psutil',
        'bcrypt'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"Eksik kütüphaneler: {', '.join(missing_modules)}\n\n"
        error_msg += "Lütfen şu komutu çalıştırın:\n"
        error_msg += "pip install -r requirements.txt"
        
        print(error_msg)
        input("Devam etmek için Enter'a basın...")
        return False
    
    return True

def initialize_database():
    """Veritabanını başlatır"""
    try:
        db = Database()
        error_handler.log_info("Veritabanı başarıyla başlatıldı")
        return True
    except Exception as e:
        error_handler.handle_error(e, "Veritabanı başlatma")
        return False

def setup_application():
    """Uygulama ayarlarını yapar"""
    try:
        # Tema ayarları
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Log dosyası için dizin oluştur
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Yedek dizini oluştur
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        error_handler.log_info("Uygulama ayarları tamamlandı")
        return True
        
    except Exception as e:
        error_handler.handle_error(e, "Uygulama ayarlama")
        return False

def main():
    """Ana uygulama fonksiyonu"""
    try:
        print("Viventia HR Sistemi başlatılıyor...")
        
        # Gerekli kütüphaneleri kontrol et
        if not check_dependencies():
            return
        
        # Uygulama ayarlarını yap
        if not setup_application():
            return
        
        # Veritabanını başlat
        if not initialize_database():
            return
        
        print("Sistem başarıyla başlatıldı. Giriş penceresi açılıyor...")
        
        # Giriş penceresi ile başlat
        login_app = LoginWindow()
        login_app.mainloop()
        
    except KeyboardInterrupt:
        print("\nUygulama kullanıcı tarafından durduruldu.")
        
    except Exception as e:
        error_msg = f"Kritik hata: {str(e)}\n\n"
        error_msg += f"Detaylar:\n{traceback.format_exc()}"
        
        print(error_msg)
        
        # Hata dosyasına yaz
        try:
            with open("critical_error.log", "w", encoding="utf-8") as f:
                f.write(error_msg)
            print("\nHata detayları 'critical_error.log' dosyasına kaydedildi.")
        except:
            pass
        
        input("\nDevam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()