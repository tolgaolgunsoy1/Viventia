@echo off
title Viventia HR Sistemi
color 0A

echo.
echo ========================================
echo    VIVENTIA - INSAN KAYNAKLARI SISTEMI
echo ========================================
echo.

REM Python'un kurulu olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python 3.8+ yukleyin: https://python.org
    pause
    exit /b 1
)

echo Python bulundu. Sistem baslatiiliyor...
echo.

REM Gerekli kütüphaneleri kontrol et ve yükle
echo Gerekli kutuphaneler kontrol ediliyor...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo.
    echo UYARI: Bazi kutuphaneler yuklenemedi.
    echo Manuel yukleme icin: pip install -r requirements.txt
    echo.
)

REM Uygulamayı başlat
echo.
echo Viventia HR Sistemi baslatiliyor...
echo.
python main.py

REM Hata durumunda bekle
if errorlevel 1 (
    echo.
    echo HATA: Uygulama beklenmedik bir hatayla karsilasti.
    echo Detaylar icin 'critical_error.log' dosyasini kontrol edin.
    echo.
    pause
)

echo.
echo Viventia HR Sistemi kapatildi.
pause