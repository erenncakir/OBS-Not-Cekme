# OBS Not Çekme & Cookie Helper

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Lisans](https://img.shields.io/badge/License-GPLv3-red.svg)](https://www.gnu.org/licenses/gpl-3.0)

Kütahya Dumlupınar Üniversitesi (DPÜ) öğrencileri için geliştirilmiş, **Chrome Uzantısı destekli** ve **konsol tabanlı** bir not takip sistemidir. 

Bu proje iki ana parçadan oluşur:
1. **Chrome Uzantısı:** OBS sistemine girdiğinizde oturum (cookie) bilgisini otomatik yakalar.
2. **Python Uygulaması:** Yakalanan veriyi kullanarak notlarınızı çeker, analiz eder ve konsolda listeler.

## Proje Amacı

Öğrencilerin OBS sistemine sürekli giriş yapma veya manuel olarak F12 ile cookie kopyalama zahmetini ortadan kaldırarak, not takibini otomatize etmektir.

## Temel İşlevler

* **Otomatik Kimlik Doğrulama:** Chrome uzantısı sayesinde manuel cookie kopyalamaya son. OBS'ye girmeniz yeterlidir.
* **Güvenli İletişim:** Cookie verisi yerel sunucuda şifrelenerek (`Fernet`) saklanır.
* **Otomatik Dönem Algılama:** İçinde bulunduğunuz akademik dönemi (Güz/Bahar) otomatik hesaplar.
* **Konsol Erişim:** Notları doğrudan bilgisayar konsolu üzerinden hızlıca görüntüleme imkanı sunar.

## Kurulum

### 1. Önkoşullar
* Python 3.x
* Google Chrome (veya Chromium tabanlı bir tarayıcı)

### 2. Projeyi İndirme
Projeyi bilgisayarınıza klonlayın veya indirin:
```bash
git clone [https://github.com/erenncakir/OBS-Not-Cekme.git](https://github.com/erenncakir/OBS-Not-Cekme.git)
cd OBS-Not-Cekme
```

### 3. Python Kütüphanelerini Yükleme
```bash
pip install -r requirements.txt
```

### 4. Chrome Uzantısını Yükleme
1. Google Chrome'u açın ve adres çubuğuna chrome://extensions/ yazın.
2. Sağ üst köşedeki "Geliştirici modu" (Developer mode) anahtarını açın.
3. Sol üstte beliren "Paketlenmemiş öğe yükle" (Load unpacked) butonuna tıklayın.
4. İndirdiğiniz proje klasörünü seçin.

### Kullanım
Sistemi çalıştırmak için aşağıdaki adımları takip edin:

### Adım 1: Python Sunucusunu Başlatın
Öncelikle uzantının iletişim kuracağı sunucuyu başlatın:
```bash
python python_server.py
```

### Adım 2: OBS'ye Giriş Yapın
1. Tarayıcınızdan OBS Sistemine (obs.dpu.edu.tr) giriş yapın.
2. Not Listesi sayfasına gidin veya Chrome sağ üst köşesindeki eklenti ikonuna tıklayıp "Manuel Gönder" butonuna basın.
3. Eklenti ikonunda veya Python konsoludna "Cookie alındı ve kaydedildi!" mesajını göreceksiniz.

### Adım 3: Notları Kontrol Edin
Artık notlarınızı çekmek için ana programı çalıştırabilirsiniz:
```bash
python obs_checker.py
```
Program otomatik olarak dönem bilgisini soracak veya algılayacak, ardından notlarınızı listeleyecektir.

### Kullanılan Teknolojiler
| Kategori | Teknoloji | Amaç |
| :--- | :--- | :--- |
| **Backend** | `Flask, Flask-CORS` | Chrome uzantısından gelen verileri dinleyen yerel sunucu. |
| **Güvenlik** | `Cryptography (Fernet)` | Cookie verilerinin şifrelenerek saklanması. |
| **Web Kazıma** | `beautifulsoup4, requests` | OBS sayfasındaki not verilerini çekmek ve işlemek |
| **Browser Ext** | `Javascript, Manifest V3` | İstek ve veri işleme süreçleri için gerekli bağımlılıklar. |

### Gelecek Güncellemeler [Roadmap]
+ **Bildirim Sistemi** : Yeni not girişi algılandığında sesli bildirim gönderilecek.

## Katkıda Bulunma
Hata raporları veya özellik önerileri için lütfen GitHub Issues bölümünü kullanın.

## Lisans
Bu proje **GNU Genel Kamu Lisansı sürüm 3 (GPLv3)** ile lisanslanmıştır.
