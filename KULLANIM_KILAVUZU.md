# Viventia HR Sistemi - Kullanım Kılavuzu

## 📋 İçindekiler
1. [Sistem Gereksinimleri](#sistem-gereksinimleri)
2. [Kurulum](#kurulum)
3. [İlk Çalıştırma](#ilk-çalıştırma)
4. [Kullanıcı Arayüzü](#kullanıcı-arayüzü)
5. [Modüller](#modüller)
6. [Güvenlik](#güvenlik)
7. [Yedekleme](#yedekleme)
8. [Sorun Giderme](#sorun-giderme)

## 🖥️ Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi:** Windows 10/11, macOS 10.14+, Linux Ubuntu 18.04+
- **Python:** 3.8 veya üzeri
- **RAM:** 4 GB (8 GB önerilir)
- **Disk Alanı:** 500 MB boş alan
- **Ekran Çözünürlüğü:** 1366x768 (1920x1080 önerilir)

### Gerekli Python Kütüphaneleri
```
customtkinter==5.2.0
matplotlib==3.7.2
pillow==10.0.0
psutil==5.9.5
bcrypt==4.0.1
reportlab==4.0.4
```

## 📦 Kurulum

### 1. Projeyi İndirin
```bash
git clone https://github.com/username/viventia.git
cd viventia
```

### 2. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Sistem Testini Çalıştırın
```bash
python test_system.py
```

## 🚀 İlk Çalıştırma

### Windows'ta
1. `start_viventia.bat` dosyasını çift tıklayın
2. Veya komut satırından: `python main.py`

### macOS/Linux'ta
```bash
python3 main.py
```

### İlk Giriş Bilgileri
- **Kullanıcı Adı:** admin
- **Şifre:** admin123
- **Rol:** Yönetici

> ⚠️ **Güvenlik Uyarısı:** İlk girişten sonra mutlaka şifrenizi değiştirin!

## 🖥️ Kullanıcı Arayüzü

### Ana Pencere Bileşenleri

#### 1. Sidebar (Sol Menü)
- **Logo ve Slogan:** Viventia branding
- **Kullanıcı Kartı:** Aktif kullanıcı bilgileri
- **Menü Kategorileri:**
  - Ana Menü: Dashboard, Personel, İşe Alım
  - İşlemler: Puantaj, Bordro, İzinler, Performans
  - Yönetim: Eğitim, Raporlar, Yedekleme, Ayarlar

#### 2. Üst Bar
- **Sistem Durumu:** Gerçek zamanlı performans göstergeleri
- **Hızlı Erişim:** Bildirimler, Raporlar, Ayarlar
- **Performans İzleme:** CPU, Bellek, Disk kullanımı

#### 3. Ana İçerik Alanı
- Seçilen modülün arayüzü
- Dinamik içerik yükleme
- Responsive tasarım

## 📊 Modüller

### 1. Dashboard
**Özellikler:**
- Gerçek zamanlı istatistikler
- Performans grafikleri (Donut Chart)
- Departman dağılım analizi
- Son aktiviteler feed'i
- Hızlı erişim kartları

**Kullanım:**
- Sistem açıldığında otomatik yüklenir
- Grafikleri tıklayarak detaylara erişin
- Kartlar üzerinden hızlı işlemler yapın

### 2. Personel Yönetimi
**Özellikler:**
- Grid tabanlı personel listesi
- Avatar destekli kart görünümü
- Gelişmiş filtreleme ve arama
- CRUD işlemleri (Ekleme, Düzenleme, Silme)
- Departman bazlı gruplandırma

**Kullanım:**
1. **Yeni Personel Ekleme:**
   - "+ Yeni Personel" butonuna tıklayın
   - Formu doldurun (tüm alanlar zorunlu)
   - "Kaydet" butonuna tıklayın

2. **Personel Düzenleme:**
   - Personel kartındaki "Düzenle" butonuna tıklayın
   - Bilgileri güncelleyin
   - "Güncelle" butonuna tıklayın

3. **Personel Silme:**
   - Personel kartındaki "Sil" butonuna tıklayın
   - Onay verin

### 3. İzin Yönetimi
**Özellikler:**
- Mini takvim görünümü
- İzin türü panelleri
- İzin talep kartları
- Onay/Red workflow'u
- İstatistiksel raporlar

**Kullanım:**
1. **İzin Talebi Oluşturma:**
   - "+ Yeni İzin Talebi" butonuna tıklayın
   - Personel, tarih ve izin türünü seçin
   - Açıklama ekleyin
   - "Talep Oluştur" butonuna tıklayın

2. **İzin Onaylama/Reddetme:**
   - Bekleyen talepler listesinden talebi seçin
   - "Onayla" veya "Reddet" butonuna tıklayın
   - Gerekirse açıklama ekleyin

### 4. Bordro Yönetimi
**Özellikler:**
- Finansal grafikler ve analizler
- Maaş dağılım analizi
- Ödeme işleme sistemi
- Bordro hesaplamaları
- Prim ve kesinti yönetimi

**Kullanım:**
1. **Bordro Hesaplama:**
   - İlgili ayı seçin
   - "Bordro Hesapla" butonuna tıklayın
   - Sonuçları inceleyin

2. **Ödeme İşleme:**
   - Hesaplanmış bordroları seçin
   - "Ödemeleri İşle" butonuna tıklayın
   - Onay verin

### 5. Performans İzleme
**Özellikler:**
- Sistem performans metrikleri
- Gerçek zamanlı izleme
- Geçmiş veri analizi
- Performans raporları
- Kritik durum uyarıları

**Kullanım:**
- Üst bardaki "📊 Detaylar" butonuna tıklayın
- Performans geçmişini inceleyin
- Sistem bilgilerini görüntüleyin

## 🔐 Güvenlik

### Kullanıcı Rolleri
1. **Admin (Yönetici)**
   - Tüm modüllere erişim
   - Kullanıcı yönetimi
   - Sistem ayarları
   - Yedekleme işlemleri

2. **HR Manager (İK Yöneticisi)**
   - Personel yönetimi
   - İzin onaylama
   - Bordro işlemleri
   - Raporlar

3. **User (Kullanıcı)**
   - Kendi bilgilerini görüntüleme
   - İzin talebi oluşturma
   - Temel raporlar

### Güvenlik Özellikleri
- **Şifre Hashleme:** bcrypt ile güvenli şifre saklama
- **Oturum Yönetimi:** Güvenli giriş/çıkış
- **Audit Logging:** Tüm işlemler loglanır
- **Input Validation:** Girdi doğrulama ve sanitizasyon
- **Role-based Access:** Rol tabanlı erişim kontrolü

## 💾 Yedekleme

### Otomatik Yedekleme
- Sistem günlük otomatik yedek alır
- Yedekler `backups/` klasöründe saklanır
- En fazla 30 günlük yedek tutulur

### Manuel Yedekleme
1. "Yedekleme" modülüne gidin
2. "Yedek Oluştur" butonuna tıklayın
3. Yedek dosyası oluşturulur

### Yedek Geri Yükleme
1. "Yedekleme" modülüne gidin
2. Geri yüklenecek yedeği seçin
3. "Geri Yükle" butonuna tıklayın
4. Onay verin

## 🔧 Sorun Giderme

### Sık Karşılaşılan Sorunlar

#### 1. Uygulama Açılmıyor
**Çözüm:**
```bash
# Python versiyonunu kontrol edin
python --version

# Kütüphaneleri yeniden yükleyin
pip install -r requirements.txt --force-reinstall

# Test scriptini çalıştırın
python test_system.py
```

#### 2. Veritabanı Hatası
**Çözüm:**
- `viventia.db` dosyasını silin (yedek alın!)
- Uygulamayı yeniden başlatın
- Veritabanı otomatik oluşturulacak

#### 3. Performans Sorunları
**Çözüm:**
- Sistem kaynaklarını kontrol edin
- Gereksiz uygulamaları kapatın
- Performans detaylarını inceleyin

#### 4. Giriş Yapamıyorum
**Çözüm:**
- Kullanıcı adı/şifre kontrolü yapın
- Caps Lock kontrolü yapın
- Admin ile giriş yapıp şifre sıfırlayın

### Log Dosyaları
- **Uygulama Logları:** `viventia_errors.log`
- **Kritik Hatalar:** `critical_error.log`
- **Test Raporları:** `test_report_*.txt`

### Destek
Sorun yaşadığınızda:
1. Log dosyalarını kontrol edin
2. Test scriptini çalıştırın
3. Hata mesajlarını kaydedin
4. Destek ekibiyle iletişime geçin

## 📞 İletişim

**Viventia Development Team**
- E-posta: info@viventia.com
- Website: www.viventia.com
- Destek: support@viventia.com

---

## 📝 Sürüm Notları

### v1.0.0 (Mevcut)
- ✅ Temel HR modülleri
- ✅ Modern UI/UX tasarım
- ✅ Güvenlik sistemi
- ✅ Performans izleme
- ✅ Yedekleme sistemi
- ✅ Hata yönetimi

### Gelecek Sürümler
- 🔄 Raporlama modülü genişletme
- 🔄 E-posta entegrasyonu
- 🔄 Multi-language desteği
- 🔄 API entegrasyonu
- 🔄 Mobile responsive tasarım

---

*Bu kılavuz Viventia HR Sistemi v1.0.0 için hazırlanmıştır.*