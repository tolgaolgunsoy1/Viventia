import re
from datetime import datetime

class Validators:
    """Veri doğrulama yardımcı sınıfı"""

    @staticmethod
    def validate_email(email):
        """E-posta formatını doğrular"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        """Türk telefon numarası formatını doğrular"""
        if not phone:
            return False
        # 05XX XXX XX XX formatı
        pattern = r'^05[0-9]{2}\s?[0-9]{3}\s?[0-9]{2}\s?[0-9]{2}$'
        return re.match(pattern, phone) is not None

    @staticmethod
    def validate_salary(salary):
        """Maaş tutarını doğrular"""
        if not salary:
            return True  # Opsiyonel alan
        try:
            value = float(salary.replace(',', '').replace(' ', ''))
            return 0 <= value <= 1000000  # 0-1M arası
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def validate_date(date_str):
        """Tarih formatını doğrular (YYYY-MM-DD)"""
        if not date_str:
            return False
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def sanitize_input(text):
        """Güvenlik için input'u temizler"""
        if not text:
            return text
        # HTML taglarını ve özel karakterleri temizle
        import html
        text = html.escape(text)
        # SQL injection koruması için temel temizlik
        text = text.replace("'", "''").replace('"', '""')
        return text

    @staticmethod
    def validate_name(name):
        """İsim formatını doğrular"""
        if not name or len(name.strip()) < 2:
            return False
        # Sadece harf, boşluk ve Türkçe karakterler
        pattern = r'^[a-zA-ZçğıöşüÇĞİÖŞÜ\s]+$'
        return re.match(pattern, name.strip()) is not None

    @staticmethod
    def validate_positive_number(value):
        """Pozitif sayı doğrular"""
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False