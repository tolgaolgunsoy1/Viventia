@echo off
echo Viventia HR Yönetim Sistemi başlatılıyor...
echo.

REM Gerekli kütüphaneleri kontrol et
python -c "import customtkinter, matplotlib, sqlite3" 2>nul
if errorlevel 1 (
    echo Gerekli kütüphaneler yükleniyor...
    pip install -r requirements.txt
)

echo Uygulama başlatılıyor...
python main.py

pause