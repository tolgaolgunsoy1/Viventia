import customtkinter as ctk
from tkinter import messagebox

class NotificationSystem:
    @staticmethod
    def show_success(parent, title, message):
        notification = ctk.CTkToplevel(parent)
        notification.title(title)
        notification.geometry("350x150")
        notification.configure(fg_color="#121212")
        notification.transient(parent)
        notification.grab_set()
        
        # İkon ve mesaj
        content_frame = ctk.CTkFrame(notification, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(
            content_frame,
            text="✓",
            font=ctk.CTkFont(size=30),
            text_color="#50C878"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            content_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=300
        ).pack(pady=5)
        
        ctk.CTkButton(
            content_frame,
            text="Tamam",
            fg_color="#50C878",
            command=notification.destroy,
            width=100
        ).pack(pady=10)
        
        # 3 saniye sonra otomatik kapat
        notification.after(3000, notification.destroy)
    
    @staticmethod
    def show_error(parent, title, message):
        notification = ctk.CTkToplevel(parent)
        notification.title(title)
        notification.geometry("350x150")
        notification.configure(fg_color="#121212")
        notification.transient(parent)
        notification.grab_set()
        
        content_frame = ctk.CTkFrame(notification, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(
            content_frame,
            text="⚠",
            font=ctk.CTkFont(size=30),
            text_color="#F44336"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            content_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color="#F44336",
            wraplength=300
        ).pack(pady=5)
        
        ctk.CTkButton(
            content_frame,
            text="Tamam",
            fg_color="#F44336",
            command=notification.destroy,
            width=100
        ).pack(pady=10)