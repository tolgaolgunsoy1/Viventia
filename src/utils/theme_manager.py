# Professional Color Scheme for Viventia HR System

class ThemeManager:
    # Professional monochromatic color palette
    COLORS = {
        # Primary colors (shades of blue-gray)
        'primary': '#2C3E50',           # Dark blue-gray
        'primary_light': '#34495E',     # Medium blue-gray
        'primary_dark': '#1A252F',      # Darker blue-gray
        
        # Background colors
        'bg_primary': '#F8F9FA',        # Light gray background
        'bg_secondary': '#FFFFFF',      # White background
        'bg_dark': '#2C3E50',          # Dark background
        'bg_card': '#FFFFFF',          # Card background
        
        # Text colors
        'text_primary': '#2C3E50',      # Dark text
        'text_secondary': '#6C757D',    # Gray text
        'text_light': '#FFFFFF',        # White text
        'text_muted': '#ADB5BD',        # Muted text
        
        # Status colors (minimal and professional)
        'success': '#28A745',           # Green for success
        'warning': '#FFC107',           # Amber for warning
        'danger': '#DC3545',            # Red for danger
        'info': '#17A2B8',             # Blue for info
        
        # Neutral colors
        'border': '#DEE2E6',           # Light border
        'hover': '#E9ECEF',            # Hover state
        'disabled': '#6C757D',         # Disabled state
    }
    
    @classmethod
    def get_color(cls, color_name):
        return cls.COLORS.get(color_name, '#2C3E50')