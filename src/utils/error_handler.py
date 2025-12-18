import logging
import traceback
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

class ErrorHandler:
    """Merkezi hata yönetim sistemi"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Logging sistemini yapılandırır"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('viventia_errors.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Viventia')
    
    def handle_error(self, error, context="", show_user=True):
        """Hataları yakalar ve işler"""
        error_msg = str(error)
        error_trace = traceback.format_exc()
        
        # Log'a yaz
        self.logger.error(f"Context: {context}")
        self.logger.error(f"Error: {error_msg}")
        self.logger.error(f"Traceback: {error_trace}")
        
        # Kullanıcıya göster
        if show_user:
            self.show_error_dialog(error_msg, context)
    
    def show_error_dialog(self, error_msg, context=""):
        """Kullanıcıya hata mesajı gösterir"""
        title = "Hata Oluştu"
        message = f"İşlem sırasında bir hata oluştu:\n\n{error_msg}"
        
        if context:
            message = f"Bağlam: {context}\n\n{message}"
        
        messagebox.showerror(title, message)
    
    def show_success(self, message, title="Başarılı"):
        """Başarı mesajı gösterir"""
        messagebox.showinfo(title, message)
    
    def show_warning(self, message, title="Uyarı"):
        """Uyarı mesajı gösterir"""
        messagebox.showwarning(title, message)
    
    def confirm_action(self, message, title="Onay"):
        """Kullanıcıdan onay ister"""
        return messagebox.askyesno(title, message)
    
    def log_info(self, message):
        """Bilgi mesajını log'a yazar"""
        self.logger.info(message)
    
    def log_warning(self, message):
        """Uyarı mesajını log'a yazar"""
        self.logger.warning(message)

# Global error handler instance
error_handler = ErrorHandler()

def safe_execute(func, *args, context="", show_error=True, **kwargs):
    """Fonksiyonları güvenli şekilde çalıştırır"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_handler.handle_error(e, context, show_error)
        return None

def validate_input(value, field_name, required=True, min_length=0, max_length=None):
    """Girdi doğrulaması yapar"""
    if required and (not value or str(value).strip() == ""):
        raise ValueError(f"{field_name} alanı zorunludur")
    
    if value and len(str(value)) < min_length:
        raise ValueError(f"{field_name} en az {min_length} karakter olmalıdır")
    
    if value and max_length and len(str(value)) > max_length:
        raise ValueError(f"{field_name} en fazla {max_length} karakter olmalıdır")
    
    return True