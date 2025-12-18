import time
import psutil
import threading
from datetime import datetime, timedelta
import sqlite3
from ..utils.error_handler import error_handler

class PerformanceMonitor:
    """Sistem performans izleme sınıfı"""
    
    def __init__(self):
        self.monitoring = False
        self.monitor_thread = None
        self.performance_data = []
        self.max_data_points = 100
        
    def start_monitoring(self):
        """Performans izlemeyi başlatır"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            error_handler.log_info("Performans izleme başlatıldı")
    
    def stop_monitoring(self):
        """Performans izlemeyi durdurur"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        error_handler.log_info("Performans izleme durduruldu")
    
    def _monitor_loop(self):
        """Performans izleme döngüsü"""
        while self.monitoring:
            try:
                # Sistem bilgilerini topla
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                # Veritabanı performansını ölç
                db_response_time = self._measure_db_performance()
                
                # Veri noktası oluştur
                data_point = {
                    'timestamp': datetime.now(),
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used_gb': memory.used / (1024**3),
                    'memory_total_gb': memory.total / (1024**3),
                    'disk_percent': disk.percent,
                    'disk_used_gb': disk.used / (1024**3),
                    'disk_total_gb': disk.total / (1024**3),
                    'db_response_time': db_response_time
                }
                
                # Veri listesine ekle
                self.performance_data.append(data_point)
                
                # Maksimum veri noktası sayısını aş
                if len(self.performance_data) > self.max_data_points:
                    self.performance_data.pop(0)
                
                # Kritik durumları kontrol et
                self._check_critical_conditions(data_point)
                
                time.sleep(5)  # 5 saniye bekle
                
            except Exception as e:
                error_handler.handle_error(e, "Performans izleme", show_user=False)
                time.sleep(10)  # Hata durumunda daha uzun bekle
    
    def _measure_db_performance(self):
        """Veritabanı performansını ölçer"""
        try:
            start_time = time.time()
            
            # Basit bir sorgu çalıştır
            conn = sqlite3.connect("viventia.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM employees")
            cursor.fetchone()
            conn.close()
            
            end_time = time.time()
            return (end_time - start_time) * 1000  # milisaniye cinsinden
            
        except Exception as e:
            error_handler.handle_error(e, "Veritabanı performans ölçümü", show_user=False)
            return -1
    
    def _check_critical_conditions(self, data_point):
        """Kritik durumları kontrol eder"""
        try:
            # CPU kullanımı %90'ın üzerinde
            if data_point['cpu_percent'] > 90:
                error_handler.log_warning(f"Yüksek CPU kullanımı: %{data_point['cpu_percent']}")
            
            # Bellek kullanımı %85'in üzerinde
            if data_point['memory_percent'] > 85:
                error_handler.log_warning(f"Yüksek bellek kullanımı: %{data_point['memory_percent']}")
            
            # Disk kullanımı %90'ın üzerinde
            if data_point['disk_percent'] > 90:
                error_handler.log_warning(f"Yüksek disk kullanımı: %{data_point['disk_percent']}")
            
            # Veritabanı yanıt süresi 1000ms'den fazla
            if data_point['db_response_time'] > 1000:
                error_handler.log_warning(f"Yavaş veritabanı yanıtı: {data_point['db_response_time']:.2f}ms")
                
        except Exception as e:
            error_handler.handle_error(e, "Kritik durum kontrolü", show_user=False)
    
    def get_current_stats(self):
        """Güncel istatistikleri getirir"""
        if not self.performance_data:
            return None
        
        latest = self.performance_data[-1]
        return {
            'cpu_percent': latest['cpu_percent'],
            'memory_percent': latest['memory_percent'],
            'disk_percent': latest['disk_percent'],
            'db_response_time': latest['db_response_time'],
            'timestamp': latest['timestamp']
        }
    
    def get_performance_history(self, minutes=30):
        """Belirtilen dakika için performans geçmişini getirir"""
        if not self.performance_data:
            return []
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            data for data in self.performance_data 
            if data['timestamp'] >= cutoff_time
        ]
    
    def get_average_stats(self, minutes=30):
        """Belirtilen dakika için ortalama istatistikleri getirir"""
        history = self.get_performance_history(minutes)
        
        if not history:
            return None
        
        total_points = len(history)
        avg_cpu = sum(data['cpu_percent'] for data in history) / total_points
        avg_memory = sum(data['memory_percent'] for data in history) / total_points
        avg_disk = sum(data['disk_percent'] for data in history) / total_points
        avg_db_time = sum(data['db_response_time'] for data in history if data['db_response_time'] > 0) / total_points
        
        return {
            'avg_cpu_percent': avg_cpu,
            'avg_memory_percent': avg_memory,
            'avg_disk_percent': avg_disk,
            'avg_db_response_time': avg_db_time,
            'data_points': total_points
        }
    
    def export_performance_data(self, filename=None):
        """Performans verilerini dosyaya aktarır"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"performance_data_{timestamp}.json"
            
            import json
            
            # Datetime objelerini string'e çevir
            export_data = []
            for data in self.performance_data:
                export_item = data.copy()
                export_item['timestamp'] = data['timestamp'].isoformat()
                export_data.append(export_item)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            error_handler.log_info(f"Performans verileri aktarıldı: {filename}")
            return filename
            
        except Exception as e:
            error_handler.handle_error(e, "Performans verisi aktarma")
            return None
    
    def get_system_info(self):
        """Sistem bilgilerini getirir"""
        try:
            import platform
            
            return {
                'platform': platform.platform(),
                'processor': platform.processor(),
                'architecture': platform.architecture()[0],
                'python_version': platform.python_version(),
                'cpu_count': psutil.cpu_count(),
                'total_memory_gb': psutil.virtual_memory().total / (1024**3),
                'total_disk_gb': psutil.disk_usage('/').total / (1024**3)
            }
            
        except Exception as e:
            error_handler.handle_error(e, "Sistem bilgisi alma", show_user=False)
            return {}

# Global performans monitörü
performance_monitor = PerformanceMonitor()