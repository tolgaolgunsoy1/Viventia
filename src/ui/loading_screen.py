import customtkinter as ctk
import threading
import time

class LoadingScreen(ctk.CTkToplevel):
    def __init__(self, parent, title="Yükleniyor...", message="Lütfen bekleyin..."):
        super().__init__(parent)
        
        self.title("Viventia")
        self.geometry("400x200")
        self.configure(fg_color="#0A0A0A")
        self.resizable(False, False)
        
        # Pencereyi merkeze al
        self.center_window()
        
        # Modal yap
        self.transient(parent)
        self.grab_set()
        
        self.create_loading_ui(title, message)
        
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (200 // 2)
        self.geometry(f"400x200+{x}+{y}")
        
    def create_loading_ui(self, title, message):
        # Ana container
        main_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo
        logo_frame = ctk.CTkFrame(main_frame, fg_color="#50C878", corner_radius=20, width=40, height=40)
        logo_frame.pack(pady=(30, 15))
        logo_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            logo_frame,
            text="V",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(expand=True)
        
        # Başlık
        ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(pady=(0, 10))
        
        # Mesaj
        ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=12),
            text_color="#CCCCCC"
        ).pack(pady=(0, 20))
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(
            main_frame,
            width=300,
            height=8,
            progress_color="#50C878",
            fg_color="#252525"
        )
        self.progress.pack(pady=(0, 30))
        self.progress.set(0)
        
        # Animasyon başlat
        self.animate_progress()
        
    def animate_progress(self):
        def animate():
            for i in range(101):
                self.progress.set(i / 100)
                time.sleep(0.02)
                
        thread = threading.Thread(target=animate)
        thread.daemon = True
        thread.start()
        
    def close_loading(self):
        self.destroy()