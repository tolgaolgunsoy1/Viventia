import json
import os
from ..utils.error_handler import error_handler

class LanguageManager:
    """Çok dilli destek yöneticisi"""

    def __init__(self, default_language='tr'):
        self.current_language = default_language
        self.translations = {}
        self.available_languages = ['tr', 'en']
        self.load_translations()

    def load_translations(self):
        """Tüm çevirileri yükler"""
        try:
            translations_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'translations')

            for lang in self.available_languages:
                translation_file = os.path.join(translations_dir, f'{lang}.json')
                if os.path.exists(translation_file):
                    with open(translation_file, 'r', encoding='utf-8') as f:
                        self.translations[lang] = json.load(f)
                else:
                    # Varsayılan çeviri oluştur
                    self.translations[lang] = self.get_default_translations(lang)

        except Exception as e:
            error_handler.handle_error(e, "Çeviri yükleme", show_user=False)
            # Fallback olarak Türkçe kullan
            self.translations['tr'] = self.get_default_translations('tr')

    def get_default_translations(self, language):
        """Varsayılan çevirileri döndürür"""
        if language == 'tr':
            return {
                # Genel
                "app_title": "Viventia - İnsan Kaynakları Yönetim Sistemi",
                "login": "Giriş",
                "logout": "Çıkış",
                "username": "Kullanıcı Adı",
                "password": "Şifre",
                "cancel": "İptal",
                "save": "Kaydet",
                "delete": "Sil",
                "edit": "Düzenle",
                "add": "Ekle",
                "search": "Ara",
                "filter": "Filtrele",

                # Menü
                "dashboard": "Dashboard",
                "personnel": "Personel",
                "recruitment": "İşe Alım",
                "attendance": "Puantaj",
                "payroll": "Bordro",
                "leaves": "İzinler",
                "performance": "Performans",
                "training": "Eğitim",
                "reports": "Raporlar",
                "backup": "Yedekleme",
                "email": "E-posta",
                "settings": "Ayarlar",

                # Personel
                "employee_name": "Ad Soyad",
                "department": "Departman",
                "position": "Pozisyon",
                "salary": "Maaş",
                "hire_date": "İşe Giriş Tarihi",
                "status": "Durum",
                "email": "E-posta",
                "phone": "Telefon",
                "active": "Aktif",
                "inactive": "Pasif",

                # İzinler
                "leave_request": "İzin Talebi",
                "annual_leave": "Yıllık İzin",
                "sick_leave": "Hastalık İzni",
                "start_date": "Başlangıç Tarihi",
                "end_date": "Bitiş Tarihi",
                "reason": "Sebep",
                "approved": "Onaylandı",
                "rejected": "Reddedildi",
                "pending": "Bekliyor",

                # Mesajlar
                "success": "Başarılı",
                "error": "Hata",
                "warning": "Uyarı",
                "confirm": "Onayla",
                "yes": "Evet",
                "no": "Hayır",

                # Hata mesajları
                "connection_error": "Bağlantı hatası",
                "database_error": "Veritabanı hatası",
                "validation_error": "Doğrulama hatası",
                "permission_denied": "İzin reddedildi"
            }
        elif language == 'en':
            return {
                # General
                "app_title": "Viventia - Human Resources Management System",
                "login": "Login",
                "logout": "Logout",
                "username": "Username",
                "password": "Password",
                "cancel": "Cancel",
                "save": "Save",
                "delete": "Delete",
                "edit": "Edit",
                "add": "Add",
                "search": "Search",
                "filter": "Filter",

                # Menu
                "dashboard": "Dashboard",
                "personnel": "Personnel",
                "recruitment": "Recruitment",
                "attendance": "Attendance",
                "payroll": "Payroll",
                "leaves": "Leaves",
                "performance": "Performance",
                "training": "Training",
                "reports": "Reports",
                "backup": "Backup",
                "email": "Email",
                "settings": "Settings",

                # Personnel
                "employee_name": "Full Name",
                "department": "Department",
                "position": "Position",
                "salary": "Salary",
                "hire_date": "Hire Date",
                "status": "Status",
                "email": "Email",
                "phone": "Phone",
                "active": "Active",
                "inactive": "Inactive",

                # Leaves
                "leave_request": "Leave Request",
                "annual_leave": "Annual Leave",
                "sick_leave": "Sick Leave",
                "start_date": "Start Date",
                "end_date": "End Date",
                "reason": "Reason",
                "approved": "Approved",
                "rejected": "Rejected",
                "pending": "Pending",

                # Messages
                "success": "Success",
                "error": "Error",
                "warning": "Warning",
                "confirm": "Confirm",
                "yes": "Yes",
                "no": "No",

                # Error messages
                "connection_error": "Connection error",
                "database_error": "Database error",
                "validation_error": "Validation error",
                "permission_denied": "Permission denied"
            }
        else:
            return {}

    def set_language(self, language):
        """Dil ayarlar"""
        if language in self.available_languages:
            self.current_language = language
            error_handler.log_info(f"Dil değiştirildi: {language}")
            return True
        return False

    def get_text(self, key, default=None):
        """Çeviri metnini döndürür"""
        try:
            translations = self.translations.get(self.current_language, {})
            return translations.get(key, default or key)
        except Exception as e:
            error_handler.handle_error(e, f"Çeviri alma: {key}", show_user=False)
            return key

    def get_available_languages(self):
        """Mevcut dilleri döndürür"""
        return self.available_languages

    def get_current_language(self):
        """Mevcut dili döndürür"""
        return self.current_language

    def save_translation_file(self, language, translations):
        """Çeviri dosyasını kaydeder"""
        try:
            translations_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'translations')
            os.makedirs(translations_dir, exist_ok=True)

            translation_file = os.path.join(translations_dir, f'{language}.json')
            with open(translation_file, 'w', encoding='utf-8') as f:
                json.dump(translations, f, indent=2, ensure_ascii=False)

            # Bellekte güncelle
            self.translations[language] = translations
            error_handler.log_info(f"Çeviri dosyası kaydedildi: {language}")

        except Exception as e:
            error_handler.handle_error(e, f"Çeviri dosyası kaydetme: {language}")

# Global language manager instance
language_manager = LanguageManager()

# Convenience function
def _(key, default=None):
    """Çeviri kısayolu"""
    return language_manager.get_text(key, default)