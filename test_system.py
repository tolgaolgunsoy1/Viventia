#!/usr/bin/env python3
"""
Viventia HR Sistemi Test Scripti
Tüm sistem bileşenlerini test eder ve doğrular
"""

import sys
import os
import sqlite3
import traceback
from datetime import datetime

def test_imports():
    """Gerekli modüllerin import edilebilirliğini test eder"""
    print("Modul import testleri...")
    
    modules_to_test = [
        ('customtkinter', 'CustomTkinter GUI framework'),
        ('matplotlib', 'Grafik ve chart kütüphanesi'),
        ('PIL', 'Pillow görüntü işleme'),
        ('psutil', 'Sistem performans izleme'),
        ('bcrypt', 'Şifre hashleme'),
        ('sqlite3', 'SQLite veritabanı'),
        ('threading', 'Thread yönetimi'),
        ('datetime', 'Tarih/saat işlemleri'),
        ('json', 'JSON veri işleme'),
        ('logging', 'Log sistemi')
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name} - {description}")
        except ImportError as e:
            print(f"  ❌ {module_name} - {description} - HATA: {e}")
            failed_imports.append(module_name)
    
    if failed_imports:
        print(f"\n⚠️  Eksik modüller: {', '.join(failed_imports)}")
        print("Çözüm: pip install -r requirements.txt")
        return False
    
    print("✅ Tüm modüller başarıyla import edildi\n")
    return True

def test_database():
    """Veritabanı bağlantısını ve tablolarını test eder"""
    print("🗄️  Veritabanı testleri...")
    
    try:
        # Veritabanı bağlantısı
        conn = sqlite3.connect("viventia.db")
        cursor = conn.cursor()
        
        # Tabloların varlığını kontrol et
        required_tables = [
            'employees', 'departments', 'recruitment', 'leaves', 
            'payroll', 'benefits', 'attendance', 'performance', 'training'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = []
        for table in required_tables:
            if table in existing_tables:
                print(f"  ✅ Tablo '{table}' mevcut")
            else:
                print(f"  ❌ Tablo '{table}' eksik")
                missing_tables.append(table)
        
        if missing_tables:
            print(f"\n⚠️  Eksik tablolar: {', '.join(missing_tables)}")
            conn.close()
            return False
        
        # Örnek veri kontrolü
        cursor.execute("SELECT COUNT(*) FROM employees")
        employee_count = cursor.fetchone()[0]
        print(f"  📊 Toplam çalışan sayısı: {employee_count}")
        
        cursor.execute("SELECT COUNT(*) FROM leaves")
        leave_count = cursor.fetchone()[0]
        print(f"  📊 Toplam izin kaydı: {leave_count}")
        
        conn.close()
        print("✅ Veritabanı testleri başarılı\n")
        return True
        
    except Exception as e:
        print(f"❌ Veritabanı hatası: {e}")
        return False

def test_file_structure():
    """Proje dosya yapısını test eder"""
    print("📁 Dosya yapısı testleri...")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'src/__init__.py',
        'src/ui/__init__.py',
        'src/ui/main_window.py',
        'src/ui/enhanced_sidebar.py',
        'src/ui/login_window.py',
        'src/ui/notification_system.py',
        'src/ui/system_status_widget.py',
        'src/database/__init__.py',
        'src/database/database.py',
        'src/security/__init__.py',
        'src/security/auth_manager.py',
        'src/utils/__init__.py',
        'src/utils/error_handler.py',
        'src/utils/performance_monitor.py',
        'src/utils/validators.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - EKSIK")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Eksik dosyalar: {', '.join(missing_files)}")
        return False
    
    print("✅ Tüm gerekli dosyalar mevcut\n")
    return True

def test_ui_components():
    """UI bileşenlerinin import edilebilirliğini test eder"""
    print("🖥️  UI bileşen testleri...")
    
    ui_components = [
        ('src.ui.main_window', 'MainWindow'),
        ('src.ui.enhanced_sidebar', 'EnhancedSidebar'),
        ('src.ui.login_window', 'LoginWindow'),
        ('src.ui.notification_system', 'NotificationSystem'),
        ('src.ui.system_status_widget', 'SystemStatusWidget'),
        ('src.ui.enhanced_dashboard', 'EnhancedDashboard'),
        ('src.ui.enhanced_personnel', 'EnhancedPersonnelPage'),
        ('src.ui.enhanced_leaves', 'EnhancedLeavesPage'),
        ('src.ui.enhanced_payroll', 'EnhancedPayrollPage')
    ]
    
    failed_components = []
    
    for module_path, class_name in ui_components:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {module_path}.{class_name}")
        except Exception as e:
            print(f"  ❌ {module_path}.{class_name} - HATA: {e}")
            failed_components.append(f"{module_path}.{class_name}")
    
    if failed_components:
        print(f"\n⚠️  Başarısız bileşenler: {', '.join(failed_components)}")
        return False
    
    print("✅ Tüm UI bileşenleri başarıyla yüklendi\n")
    return True

def test_security_system():
    """Güvenlik sistemini test eder"""
    print("🔐 Güvenlik sistemi testleri...")
    
    try:
        from src.security.auth_manager import AuthManager
        
        # AuthManager oluştur
        auth = AuthManager()
        print("  ✅ AuthManager başarıyla oluşturuldu")
        
        # Test kullanıcısı oluştur
        test_result = auth.create_user("test_user", "test123", "user")
        if test_result:
            print("  ✅ Test kullanıcısı oluşturuldu")
            
            # Giriş testi
            login_result = auth.login("test_user", "test123")
            if login_result:
                print("  ✅ Kullanıcı girişi başarılı")
                
                # Çıkış testi
                auth.logout()
                print("  ✅ Kullanıcı çıkışı başarılı")
            else:
                print("  ❌ Kullanıcı girişi başarısız")
                return False
        else:
            print("  ⚠️  Test kullanıcısı zaten mevcut (normal)")
        
        print("✅ Güvenlik sistemi testleri başarılı\n")
        return True
        
    except Exception as e:
        print(f"❌ Güvenlik sistemi hatası: {e}")
        return False

def test_error_handling():
    """Hata yönetim sistemini test eder"""
    print("⚠️  Hata yönetim sistemi testleri...")
    
    try:
        from src.utils.error_handler import error_handler, safe_execute
        
        # Log testi
        error_handler.log_info("Test log mesajı")
        print("  ✅ Log sistemi çalışıyor")
        
        # Safe execute testi
        def test_function():
            return "Test başarılı"
        
        result = safe_execute(test_function, context="Test fonksiyonu")
        if result == "Test başarılı":
            print("  ✅ Safe execute çalışıyor")
        else:
            print("  ❌ Safe execute hatası")
            return False
        
        print("✅ Hata yönetim sistemi testleri başarılı\n")
        return True
        
    except Exception as e:
        print(f"❌ Hata yönetim sistemi hatası: {e}")
        return False

def test_performance_monitor():
    """Performans izleme sistemini test eder"""
    print("📊 Performans izleme testleri...")
    
    try:
        from src.utils.performance_monitor import performance_monitor
        
        # Sistem bilgilerini al
        system_info = performance_monitor.get_system_info()
        if system_info:
            print("  ✅ Sistem bilgileri alındı")
            print(f"    - Platform: {system_info.get('platform', 'N/A')}")
            print(f"    - CPU Çekirdek: {system_info.get('cpu_count', 'N/A')}")
            print(f"    - Toplam Bellek: {system_info.get('total_memory_gb', 0):.1f} GB")
        else:
            print("  ❌ Sistem bilgileri alınamadı")
            return False
        
        print("✅ Performans izleme testleri başarılı\n")
        return True
        
    except Exception as e:
        print(f"❌ Performans izleme hatası: {e}")
        return False

def generate_test_report(results):
    """Test sonuçlarının raporunu oluşturur"""
    print("📋 TEST RAPORU")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"Toplam Test: {total_tests}")
    print(f"Başarılı: {passed_tests}")
    print(f"Başarısız: {failed_tests}")
    print(f"Başarı Oranı: {(passed_tests/total_tests)*100:.1f}%")
    print()
    
    for test_name, result in results.items():
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{test_name}: {status}")
    
    print("=" * 50)
    
    if failed_tests == 0:
        print("🎉 TÜM TESTLER BAŞARILI!")
        print("Viventia HR Sistemi çalışmaya hazır.")
    else:
        print("⚠️  BAZI TESTLER BAŞARISIZ!")
        print("Lütfen hataları düzeltin ve tekrar test edin.")
    
    # Raporu dosyaya kaydet
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test_report_{timestamp}.txt"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"Viventia HR Sistemi Test Raporu\n")
            f.write(f"Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Toplam Test: {total_tests}\n")
            f.write(f"Başarılı: {passed_tests}\n")
            f.write(f"Başarısız: {failed_tests}\n")
            f.write(f"Başarı Oranı: {(passed_tests/total_tests)*100:.1f}%\n\n")
            
            for test_name, result in results.items():
                status = "BAŞARILI" if result else "BAŞARISIZ"
                f.write(f"{test_name}: {status}\n")
        
        print(f"\n📄 Test raporu '{report_file}' dosyasına kaydedildi.")
        
    except Exception as e:
        print(f"⚠️  Rapor kaydetme hatası: {e}")

def main():
    """Ana test fonksiyonu"""
    print("Viventia HR Sistemi Test Sureci Baslatiliyor...")
    print("=" * 60)
    print()
    
    # Test sonuçları
    test_results = {}
    
    try:
        # Testleri sırayla çalıştır
        test_results["Modül Import"] = test_imports()
        test_results["Dosya Yapısı"] = test_file_structure()
        test_results["Veritabanı"] = test_database()
        test_results["UI Bileşenleri"] = test_ui_components()
        test_results["Güvenlik Sistemi"] = test_security_system()
        test_results["Hata Yönetimi"] = test_error_handling()
        test_results["Performans İzleme"] = test_performance_monitor()
        
    except KeyboardInterrupt:
        print("\n⚠️  Test süreci kullanıcı tarafından durduruldu.")
        return
    
    except Exception as e:
        print(f"\n❌ Kritik test hatası: {e}")
        print(f"Detaylar: {traceback.format_exc()}")
        return
    
    # Rapor oluştur
    print()
    generate_test_report(test_results)

if __name__ == "__main__":
    main()
    input("\nDevam etmek için Enter'a basın...")