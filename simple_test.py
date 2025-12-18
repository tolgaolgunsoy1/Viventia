#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Viventia HR Sistemi Basit Test Scripti
"""

import sys
import os

def test_basic_imports():
    """Temel modulleri test eder"""
    print("Temel modul testleri...")
    
    modules = ['customtkinter', 'matplotlib', 'PIL', 'sqlite3']
    success = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"  OK: {module}")
        except ImportError as e:
            print(f"  HATA: {module} - {e}")
            success = False
    
    return success

def test_file_structure():
    """Dosya yapısını test eder"""
    print("\nDosya yapisi testleri...")
    
    files = [
        'main.py',
        'src/ui/main_window.py',
        'src/database/database.py',
        'src/security/auth_manager.py'
    ]
    
    success = True
    for file in files:
        if os.path.exists(file):
            print(f"  OK: {file}")
        else:
            print(f"  EKSIK: {file}")
            success = False
    
    return success

def test_database():
    """Veritabanını test eder"""
    print("\nVeritabani testleri...")
    
    try:
        from src.database.database import Database
        db = Database()
        print("  OK: Veritabani baglantisi")
        return True
    except Exception as e:
        print(f"  HATA: Veritabani - {e}")
        return False

def main():
    print("Viventia HR Sistemi Basit Test")
    print("=" * 40)
    
    results = []
    results.append(test_basic_imports())
    results.append(test_file_structure())
    results.append(test_database())
    
    print("\n" + "=" * 40)
    success_count = sum(results)
    total_count = len(results)
    
    print(f"Sonuc: {success_count}/{total_count} test basarili")
    
    if success_count == total_count:
        print("TUM TESTLER BASARILI!")
        print("Sistem calisir durumda.")
    else:
        print("BAZI TESTLER BASARISIZ!")
        print("Lutfen hatalari duzeltin.")

if __name__ == "__main__":
    main()
    input("\nDevam etmek icin Enter'a basin...")