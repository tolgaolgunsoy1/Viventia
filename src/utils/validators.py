import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        pattern = r'^(\+90|0)?[5][0-9]{9}$'
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        return re.match(pattern, cleaned) is not None
    
    @staticmethod
    def validate_salary(salary):
        try:
            amount = float(salary)
            return 0 <= amount <= 1000000
        except ValueError:
            return False
    
    @staticmethod
    def validate_date(date_str, format="%Y-%m-%d"):
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def sanitize_input(text):
        if not text:
            return ""
        dangerous_chars = ["'", '"', ';', '--', '/*', '*/', '<', '>', '&']
        sanitized = str(text).strip()
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        return sanitized