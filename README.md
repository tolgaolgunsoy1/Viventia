# Viventia - İnsan Kaynakları Yönetim Sistemi

Modern masaüstü HR yönetim platformu. Python ve CustomTkinter ile geliştirilmiş, Dark Emerald temalı tek pencere uygulaması.

## 🚀 Özellikler

### 📊 Dashboard
- Gerçek zamanlı personel istatistikleri
- Performans grafikleri (Donut Chart)
- Departman dağılım analizi
- Hızlı erişim kartları

### 👥 Personel Yönetimi
- Personel ekleme/düzenleme/silme
- Detaylı personel bilgileri
- Departman bazlı filtreleme
- Scrollable liste görünümü

### 💰 Bordro Yönetimi
- Aylık bordro hesaplamaları
- Prim ve kesinti yönetimi
- Bordro raporları
- Ödeme durumu takibi

### 📅 İzin Yönetimi
- İzin talep sistemi
- Onay/red işlemleri
- İzin türü kategorileri
- İstatistiksel raporlar

### ⚙️ Sistem Ayarları
- Şirket bilgileri
- Tema ayarları
- Bordro parametreleri
- Personel politikaları

## 🛠️ Teknoloji Stack

- **Python 3.8+**
- **CustomTkinter** - Modern GUI framework
- **SQLite** - Yerel veritabanı
- **Matplotlib** - Grafik ve analitik
- **Pillow** - İkon yönetimi

## 📦 Kurulum

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/username/viventia.git
cd viventia
```

2. **Gerekli kütüphaneleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Uygulamayı başlatın:**
```bash
python main.py
```

## 🎨 Tasarım Özellikleri

### Renk Paleti (Dark Emerald Theme)
- **Ana Arka Plan:** #121212 (Derin Karbon)
- **Panel Rengi:** #1E1E1E (Yükseltilmiş Gri)
- **Vurgu Rengi:** #50C878 (Zümrüt Yeşili)
- **Metin Rengi:** #FFFFFF / #A0A0A0

### UI/UX Özellikleri
- Glassmorphism efektli kartlar
- Rounded corner tasarım (15px)
- Hover animasyonları
- Responsive layout
- Tek pencere navigasyon

## 📁 Proje Yapısı

```
Viventia/
├── main.py                 # Ana uygulama başlatıcı
├── requirements.txt        # Gerekli kütüphaneler
├── README.md              # Proje dokümantasyonu
├── src/
│   ├── ui/                # Kullanıcı arayüzü bileşenleri
│   │   ├── main_window.py
│   │   ├── sidebar.py
│   │   ├── dashboard.py
│   │   ├── personnel_page.py
│   │   ├── payroll_page.py
│   │   ├── leaves_page.py
│   │   ├── settings_page.py
│   │   ├── add_employee_modal.py
│   │   └── notification_system.py
│   ├── database/          # Veritabanı yönetimi
│   │   └── database.py
│   └── models/            # Veri modelleri
└── assets/                # Görseller ve ikonlar
```

## 🔧 Kullanım

### Personel Ekleme
1. Sol menüden "Personel" seçin
2. "+ Yeni Personel" butonuna tıklayın
3. Gerekli bilgileri doldurun
4. "Kaydet" butonuna tıklayın

### İzin Yönetimi
1. "İzinler" sayfasına gidin
2. Bekleyen talepleri görüntüleyin
3. "Onayla" veya "Reddet" butonlarını kullanın

### Bordro İşlemleri
1. "Bordro" sayfasını açın
2. İlgili ayı seçin
3. Bordro detaylarını inceleyin

## 🚀 Geliştirme Planları

- [ ] Raporlama modülü
- [ ] E-posta entegrasyonu
- [ ] Backup/restore sistemi
- [ ] Multi-language desteği
- [ ] API entegrasyonu
- [ ] Mobile responsive tasarım

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**Viventia Development Team**
- E-posta: info@viventia.com
- Website: www.viventia.com

---

*Viventia - "Yaşam/Canlılık" anlamına gelen Latince kökenli modern HR çözümü*