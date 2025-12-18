import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = "viventia_settings.json"
        self.default_settings = {
            "company_name": "Viventia Teknoloji A.Ş.",
            "theme": "Koyu Tema",
            "language": "Türkçe",
            "auto_save": True,
            "default_leave_days": 15,
            "probation_months": 3,
            "work_start_time": "09:00",
            "work_end_time": "18:00",
            "sgk_rate": 14,
            "income_tax_rate": 15,
            "unemployment_rate": 1,
            "auto_calculation": True
        }
        self.load_settings()
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self.default_settings.copy()
        except Exception:
            self.settings = self.default_settings.copy()
    
    def save_settings(self, new_settings):
        try:
            self.settings.update(new_settings)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    def get_setting(self, key):
        return self.settings.get(key, self.default_settings.get(key))
    
    def get_all_settings(self):
        return self.settings.copy()