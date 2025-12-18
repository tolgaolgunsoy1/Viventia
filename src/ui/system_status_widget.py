import customtkinter as ctk
import threading
import time
from ..utils.performance_monitor import performance_monitor
from ..utils.error_handler import error_handler, safe_execute

class SystemStatusWidget(ctk.CTkFrame):
    """Sistem durumu widget'ı"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#2A2A2A", corner_radius=15, height=60)
        
        self.pack_propagate(False)
        self.updating = False
        self.update_thread = None
        
        self.setup_ui()
        self.start_updates()
    
    def setup_ui(self):
        """UI bileşenlerini oluşturur"""
        # Ana container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Sol taraf - sistem durumu
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        # Durum ikonu ve metni
        status_container = ctk.CTkFrame(left_frame, fg_color="transparent")
        status_container.pack(side="left", fill="y")
        
        self.status_icon = ctk.CTkLabel(
            status_container,
            text="🟢",
            font=ctk.CTkFont(size=16)
        )
        self.status_icon.pack(side="left", padx=(0, 8))
        
        self.status_label = ctk.CTkLabel(
            status_container,
            text="Sistem Aktif",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#50C878"
        )
        self.status_label.pack(side="left")
        
        # Orta - performans göstergeleri
        middle_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        middle_frame.pack(side="left", fill="y", padx=(30, 0))
        
        # CPU göstergesi
        cpu_frame = ctk.CTkFrame(middle_frame, fg_color="transparent")
        cpu_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            cpu_frame,
            text="CPU:",
            font=ctk.CTkFont(size=10),
            text_color="#CCCCCC"
        ).pack()
        
        self.cpu_label = ctk.CTkLabel(
            cpu_frame,
            text="0%",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white"
        )
        self.cpu_label.pack()
        
        # Bellek göstergesi
        memory_frame = ctk.CTkFrame(middle_frame, fg_color="transparent")
        memory_frame.pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            memory_frame,
            text="Bellek:",
            font=ctk.CTkFont(size=10),
            text_color="#CCCCCC"
        ).pack()
        
        self.memory_label = ctk.CTkLabel(
            memory_frame,
            text="0%",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white"
        )
        self.memory_label.pack()
        
        # Veritabanı göstergesi
        db_frame = ctk.CTkFrame(middle_frame, fg_color="transparent")
        db_frame.pack(side="left")
        
        ctk.CTkLabel(
            db_frame,
            text="VT Yanıt:",
            font=ctk.CTkFont(size=10),
            text_color="#CCCCCC"
        ).pack()
        
        self.db_label = ctk.CTkLabel(
            db_frame,
            text="0ms",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white"
        )
        self.db_label.pack()
        
        # Sağ taraf - detay butonu
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        self.detail_btn = ctk.CTkButton(
            right_frame,
            text="📊 Detaylar",
            width=80,
            height=35,
            fg_color="#3A3A3A",
            hover_color="#4A4A4A",
            font=ctk.CTkFont(size=10),
            command=lambda: safe_execute(
                self.show_performance_details,
                context="Performans detayları gösterme"
            )
        )
        self.detail_btn.pack(expand=True)
    
    def start_updates(self):
        """Güncelleme döngüsünü başlatır"""
        if not self.updating:
            self.updating = True
            self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.update_thread.start()
            
            # Performans monitörünü başlat
            performance_monitor.start_monitoring()
    
    def stop_updates(self):
        """Güncelleme döngüsünü durdurur"""
        self.updating = False
        if self.update_thread:
            self.update_thread.join(timeout=1)
    
    def _update_loop(self):
        """Güncelleme döngüsü"""
        while self.updating:
            try:
                # Performans verilerini al
                stats = performance_monitor.get_current_stats()
                
                if stats:
                    # UI'yi güncelle (ana thread'de)
                    self.after(0, lambda: self._update_ui(stats))
                
                time.sleep(2)  # 2 saniyede bir güncelle
                
            except Exception as e:
                error_handler.handle_error(e, "Sistem durumu güncelleme", show_user=False)
                time.sleep(5)
    
    def _update_ui(self, stats):
        """UI bileşenlerini günceller"""
        try:
            # CPU güncelle
            cpu_percent = stats['cpu_percent']
            self.cpu_label.configure(text=f"{cpu_percent:.1f}%")
            
            # CPU rengini ayarla
            if cpu_percent > 80:
                cpu_color = "#F44336"  # Kırmızı
            elif cpu_percent > 60:
                cpu_color = "#FF9800"  # Turuncu
            else:
                cpu_color = "#50C878"  # Yeşil
            
            self.cpu_label.configure(text_color=cpu_color)
            
            # Bellek güncelle
            memory_percent = stats['memory_percent']
            self.memory_label.configure(text=f"{memory_percent:.1f}%")
            
            # Bellek rengini ayarla
            if memory_percent > 85:
                memory_color = "#F44336"
            elif memory_percent > 70:
                memory_color = "#FF9800"
            else:
                memory_color = "#50C878"
            
            self.memory_label.configure(text_color=memory_color)
            
            # Veritabanı yanıt süresi güncelle
            db_time = stats['db_response_time']
            if db_time > 0:
                self.db_label.configure(text=f"{db_time:.0f}ms")
                
                # VT yanıt süresi rengini ayarla
                if db_time > 500:
                    db_color = "#F44336"
                elif db_time > 200:
                    db_color = "#FF9800"
                else:
                    db_color = "#50C878"
                
                self.db_label.configure(text_color=db_color)
            else:
                self.db_label.configure(text="N/A", text_color="#666666")
            
            # Genel sistem durumunu güncelle
            self._update_system_status(cpu_percent, memory_percent, db_time)
            
        except Exception as e:
            error_handler.handle_error(e, "UI güncelleme", show_user=False)
    
    def _update_system_status(self, cpu_percent, memory_percent, db_time):
        """Genel sistem durumunu günceller"""
        try:
            # Kritik durum kontrolü
            if cpu_percent > 90 or memory_percent > 90 or db_time > 1000:
                self.status_icon.configure(text="🔴")
                self.status_label.configure(text="Sistem Yavaş", text_color="#F44336")
            elif cpu_percent > 70 or memory_percent > 70 or db_time > 500:
                self.status_icon.configure(text="🟡")
                self.status_label.configure(text="Sistem Meşgul", text_color="#FF9800")
            else:
                self.status_icon.configure(text="🟢")
                self.status_label.configure(text="Sistem Aktif", text_color="#50C878")
                
        except Exception as e:
            error_handler.handle_error(e, "Sistem durumu güncelleme", show_user=False)
    
    def show_performance_details(self):
        """Performans detayları penceresini gösterir"""
        try:
            detail_window = PerformanceDetailWindow(self)
            detail_window.focus()
        except Exception as e:
            error_handler.handle_error(e, "Performans detayları")
    
    def destroy(self):
        """Widget'ı yok eder"""
        self.stop_updates()
        super().destroy()

class PerformanceDetailWindow(ctk.CTkToplevel):
    """Performans detayları penceresi"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Sistem Performans Detayları")
        self.geometry("600x500")
        self.resizable(True, True)
        self.attributes("-topmost", True)
        
        # Pencereyi merkeze yerleştir
        self.center_window()
        
        self.setup_ui()
        self.load_data()
        
        # Otomatik güncelleme
        self.update_data()
    
    def center_window(self):
        """Pencereyi merkeze yerleştirir"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"600x500+{x}+{y}")
    
    def setup_ui(self):
        """UI bileşenlerini oluşturur"""
        # Başlık
        header_frame = ctk.CTkFrame(self, fg_color="#2A2A2A", height=60)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Sistem Performans İzleme",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Yenile butonu
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Yenile",
            width=80,
            height=30,
            fg_color="#50C878",
            hover_color="#45B068",
            command=self.load_data
        )
        refresh_btn.pack(side="right", padx=20, pady=15)
        
        # İçerik alanı
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#1A1A1A"
        )
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def load_data(self):
        """Performans verilerini yükler"""
        try:
            # Mevcut içeriği temizle
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Güncel istatistikler
            current_stats = performance_monitor.get_current_stats()
            if current_stats:
                self.create_current_stats_section(current_stats)
            
            # Ortalama istatistikler
            avg_stats = performance_monitor.get_average_stats(30)
            if avg_stats:
                self.create_average_stats_section(avg_stats)
            
            # Sistem bilgileri
            system_info = performance_monitor.get_system_info()
            if system_info:
                self.create_system_info_section(system_info)
                
        except Exception as e:
            error_handler.handle_error(e, "Performans verileri yükleme")
    
    def create_current_stats_section(self, stats):
        """Güncel istatistikler bölümü"""
        section_frame = ctk.CTkFrame(self.content_frame, fg_color="#2A2A2A", corner_radius=10)
        section_frame.pack(fill="x", pady=(0, 10))
        
        # Başlık
        ctk.CTkLabel(
            section_frame,
            text="📈 Güncel Performans",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # İstatistik kartları
        stats_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # CPU kartı
        self.create_stat_card(
            stats_container,
            "💻 CPU Kullanımı",
            f"{stats['cpu_percent']:.1f}%",
            self.get_performance_color(stats['cpu_percent'], 80, 60)
        )
        
        # Bellek kartı
        self.create_stat_card(
            stats_container,
            "🧠 Bellek Kullanımı",
            f"{stats['memory_percent']:.1f}%",
            self.get_performance_color(stats['memory_percent'], 85, 70)
        )
        
        # Disk kartı
        self.create_stat_card(
            stats_container,
            "💾 Disk Kullanımı",
            f"{stats['disk_percent']:.1f}%",
            self.get_performance_color(stats['disk_percent'], 90, 75)
        )
        
        # VT yanıt süresi kartı
        db_color = "#50C878"
        if stats['db_response_time'] > 500:
            db_color = "#F44336"
        elif stats['db_response_time'] > 200:
            db_color = "#FF9800"
        
        self.create_stat_card(
            stats_container,
            "🗄️ VT Yanıt Süresi",
            f"{stats['db_response_time']:.0f}ms",
            db_color
        )
    
    def create_average_stats_section(self, stats):
        """Ortalama istatistikler bölümü"""
        section_frame = ctk.CTkFrame(self.content_frame, fg_color="#2A2A2A", corner_radius=10)
        section_frame.pack(fill="x", pady=(0, 10))
        
        # Başlık
        ctk.CTkLabel(
            section_frame,
            text="📊 Son 30 Dakika Ortalaması",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Ortalama değerler
        avg_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        avg_container.pack(fill="x", padx=20, pady=(0, 15))
        
        avg_items = [
            ("Ortalama CPU", f"{stats['avg_cpu_percent']:.1f}%"),
            ("Ortalama Bellek", f"{stats['avg_memory_percent']:.1f}%"),
            ("Ortalama Disk", f"{stats['avg_disk_percent']:.1f}%"),
            ("Ortalama VT Yanıt", f"{stats['avg_db_response_time']:.0f}ms"),
            ("Veri Noktası Sayısı", str(stats['data_points']))
        ]
        
        for i, (label, value) in enumerate(avg_items):
            item_frame = ctk.CTkFrame(avg_container, fg_color="#3A3A3A", corner_radius=8)
            item_frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                item_frame,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color="#CCCCCC"
            ).pack(pady=(10, 2))
            
            ctk.CTkLabel(
                item_frame,
                text=value,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="white"
            ).pack(pady=(0, 10))
        
        # Grid yapılandırması
        for i in range(3):
            avg_container.grid_columnconfigure(i, weight=1)
    
    def create_system_info_section(self, info):
        """Sistem bilgileri bölümü"""
        section_frame = ctk.CTkFrame(self.content_frame, fg_color="#2A2A2A", corner_radius=10)
        section_frame.pack(fill="x", pady=(0, 10))
        
        # Başlık
        ctk.CTkLabel(
            section_frame,
            text="🖥️ Sistem Bilgileri",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#50C878"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Sistem bilgileri
        info_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        info_container.pack(fill="x", padx=20, pady=(0, 15))
        
        info_items = [
            ("Platform", info.get('platform', 'N/A')),
            ("İşlemci", info.get('processor', 'N/A')),
            ("Mimari", info.get('architecture', 'N/A')),
            ("Python Sürümü", info.get('python_version', 'N/A')),
            ("CPU Çekirdek Sayısı", str(info.get('cpu_count', 'N/A'))),
            ("Toplam Bellek", f"{info.get('total_memory_gb', 0):.1f} GB"),
            ("Toplam Disk", f"{info.get('total_disk_gb', 0):.1f} GB")
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(info_container, fg_color="#3A3A3A", corner_radius=5)
            item_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                item_frame,
                text=f"{label}:",
                font=ctk.CTkFont(size=11),
                text_color="#CCCCCC",
                anchor="w"
            ).pack(side="left", padx=(15, 5), pady=8)
            
            ctk.CTkLabel(
                item_frame,
                text=str(value),
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="white",
                anchor="w"
            ).pack(side="left", pady=8)
    
    def create_stat_card(self, parent, title, value, color):
        """İstatistik kartı oluşturur"""
        card = ctk.CTkFrame(parent, fg_color="#3A3A3A", corner_radius=10, width=120, height=80)
        card.pack(side="left", padx=5, pady=5)
        card.pack_propagate(False)
        
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=10),
            text_color="#CCCCCC"
        ).pack(pady=(10, 2))
        
        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=color
        ).pack(pady=(0, 10))
    
    def get_performance_color(self, value, high_threshold, medium_threshold):
        """Performans değerine göre renk döndürür"""
        if value > high_threshold:
            return "#F44336"  # Kırmızı
        elif value > medium_threshold:
            return "#FF9800"  # Turuncu
        else:
            return "#50C878"  # Yeşil
    
    def update_data(self):
        """Verileri otomatik günceller"""
        self.load_data()
        self.after(5000, self.update_data)  # 5 saniyede bir güncelle