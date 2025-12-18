import customtkinter as ctk
from src.ui.login_window import LoginWindow

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    
    # Giriş penceresi ile başlat
    login_app = LoginWindow()
    login_app.mainloop()

if __name__ == "__main__":
    main()