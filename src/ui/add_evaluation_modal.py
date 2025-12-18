import customtkinter as ctk
from ..database.database import Database

class AddEvaluationModal(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        
        self.callback = callback
        self.db = Database()
        
        self.title("Performans Değerlendirmesi")
        self.geometry("500x650")
        self.configure(fg_color="#121212")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.create_form()
        
    def create_form(self):
        ctk.CTkLabel(
            self, 
            text="Yeni Performans Değerlendirmesi", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#50C878"
        ).pack(pady=20)
        
        form_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Personel seçimi
        emp_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        emp_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(emp_frame, text="Değerlendirilen:", width=120, anchor="w").pack(side="left")
        
        employees = self.db.get_employees()
        employee_names = [f"{emp[1]} ({emp[2]})" for emp in employees]
        self.employee_ids = [emp[0] for emp in employees]
        
        self.employee_combo = ctk.CTkComboBox(
            emp_frame,
            values=employee_names,
            width=250
        )
        self.employee_combo.pack(side="right")
        
        # Değerlendiren seçimi
        eval_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        eval_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(eval_frame, text="Değerlendiren:", width=120, anchor="w").pack(side="left")
        
        self.evaluator_combo = ctk.CTkComboBox(
            eval_frame,
            values=employee_names,
            width=250
        )
        self.evaluator_combo.pack(side="right")
        
        # Dönem
        period_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        period_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(period_frame, text="Dönem:", width=120, anchor="w").pack(side="left")
        
        self.period_combo = ctk.CTkComboBox(
            period_frame,
            values=["2024 Q1", "2024 Q2", "2024 Q3", "2024 Q4"],
            width=250
        )
        self.period_combo.pack(side="right")
        
        # Puan
        score_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        score_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(score_frame, text="Puan (1-5):", width=120, anchor="w").pack(side="left")
        
        self.score_slider = ctk.CTkSlider(score_frame, from_=1, to=5, number_of_steps=8, width=200)
        self.score_slider.set(3)
        self.score_slider.pack(side="right", padx=(0, 50))\n        
        self.score_label = ctk.CTkLabel(score_frame, text="3.0", width=50)
        self.score_label.pack(side="right")
        
        self.score_slider.configure(command=self.update_score_label)
        
        # Hedefler
        goals_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        goals_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(goals_frame, text="Hedefler:", width=120, anchor="nw").pack(side="left", pady=5)
        
        self.goals_text = ctk.CTkTextbox(goals_frame, width=250, height=80)
        self.goals_text.pack(side="right")
        
        # Geri bildirim
        feedback_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        feedback_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(feedback_frame, text="Geri Bildirim:", width=120, anchor="nw").pack(side="left", pady=5)
        
        self.feedback_text = ctk.CTkTextbox(feedback_frame, width=250, height=80)
        self.feedback_text.pack(side="right")
        
        # Butonlar
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="İptal",
            fg_color="#666666",
            command=self.destroy
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="Kaydet",
            fg_color="#50C878",
            command=self.save_evaluation
        ).pack(side="right")
        
    def update_score_label(self, value):
        self.score_label.configure(text=f"{value:.1f}")
        
    def save_evaluation(self):
        if not all([self.employee_combo.get(), self.evaluator_combo.get(), self.period_combo.get()]):
            self.show_error("Lütfen tüm alanları doldurun!")
            return
            
        employee_index = self.employee_combo.cget("values").index(self.employee_combo.get())
        employee_id = self.employee_ids[employee_index]
        
        evaluator_index = self.evaluator_combo.cget("values").index(self.evaluator_combo.get())
        evaluator_id = self.employee_ids[evaluator_index]
        
        score = int(self.score_slider.get())
        goals = self.goals_text.get("1.0", "end-1c").strip()
        feedback = self.feedback_text.get("1.0", "end-1c").strip()
        
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO performance (employee_id, evaluator_id, period, score, 
                                       goals, feedback, evaluation_date)
                VALUES (?, ?, ?, ?, ?, ?, date('now'))
            """, (employee_id, evaluator_id, self.period_combo.get(), 
                  score, goals, feedback))
            
            conn.commit()
            conn.close()
            
            if self.callback:
                self.callback()
            
            from .notification_system import NotificationSystem
            NotificationSystem.show_success(self.master, "Başarılı", "Performans değerlendirmesi kaydedildi!")
                
            self.destroy()
            
        except Exception as e:
            self.show_error(f"Kayıt hatası: {str(e)}")
            
    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Hata")
        error_window.geometry("300x150")
        error_window.configure(fg_color="#121212")
        error_window.transient(self)
        error_window.grab_set()
        
        ctk.CTkLabel(error_window, text=message, text_color="#F44336", wraplength=250).pack(expand=True)
        ctk.CTkButton(error_window, text="Tamam", command=error_window.destroy).pack(pady=10)