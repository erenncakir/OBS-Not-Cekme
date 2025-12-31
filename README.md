# OBS Not Çekme

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Lisans](https://img.shields.io/badge/License-GPLv3-red.svg)](https://www.gnu.org/licenses/gpl-3.0)

Kütahya Dumlupınar Üniversitesi (DPÜ) öğrencileri için geliştirilmiş, **konsol tabanlı** bir not takip uygulamasıdır. OBS (Öğrenci Bilgi Sistemi) notlarını otomatik olarak çeker ve günceller.

## Proje Amacı

Öğrencilerin OBS sistemine sürekli giriş yapma ihtiyacını ortadan kaldırarak, not takibini basitleştirmek ve yeni not girişlerini kolayca takip etmelerini sağlamaktır.

## Temel İşlevler

* **Otomatik Güncelleme:** Uygulama, belirtilen aralıklarla (şu anda **her 30 dakikada bir**) OBS verilerini kontrol eder ve günceller.
* **Konsol Erişim:** Notları doğrudan bilgisayar konsolu üzerinden hızlıca görüntüleme imkanı sunar.
* **Pasif Takip:** Arka planda sessizce çalışarak güncel bilgileri hazırlar.

## Kurulum ve Çalıştırma

Bu uygulama Python tabanlı olduğu için öncelikle bilgisayarınızda Python kurulu olmalıdır.

### 1. Önkoşullar

* Python 3.x (Önerilir)
* `pip` (Python paket yöneticisi)

### 2. Depoyu Klonlama

Projeyi yerel makinenize indirin:

```bash
git clone [https://github.com/erenncakir/OBS-Not-Cekme.git](https://github.com/erenncakir/OBS-Not-Cekme.git)
cd OBS-Not-Cekme
```
### 3. Bağımlılıkları Yükleme
```bash
pip install beautifulsoup4 certifi charset-normalizer idna requests soupsieve urllib3
```
### 4. Kullanım (Cookie Girişi)
Uygulama, OBS sisteminde kimlik doğrulaması yapmak için güncel **Cookie** bilginizi gerektirir. Uygulamayı çalıştırdığınızda (RAR içindeki Exeyi çalıştırdığımızda) Cookie girmemizi isteyecek.
Cookie'yi almak için aşağıdaki adımları sırasıyla gerçekleştirin:

+ OBS DPÜ sitesine giriş yapın.
+ Klavyeden **F12** tuşuna basın veya sağ tıklayarak **"Siteyi İncele"** seçeneğini seçin.
+ Açılan pencerede **Network** sekmesine geçin.
+ OBS Sitesinden Not Listesi'ne tıklayın.
+ Network kısmına `not_listesi_op.aspx` gelecektir, buna tıklayın.
+ Açılan panelden gerekli Cookie bilgisini kopyalayın ve uygulamaya yapıştırın.

## Kullanılan Teknolojiler

Bu uygulama saf Python kullanılarak geliştirilmiştir.

| Kategori | Kütüphane | Amaç |
| :--- | :--- | :--- |
| **Web Kazıma** | `beautifulsoup4` | OBS sayfasındaki not verilerini çekmek için. |
| **HTTP İstekleri** | `requests` | OBS sunucusuna HTTP istekleri göndermek için. |
| **Diğer** | `certifi, idna, charset-normalizer, soupsieve, urllib3` | İstek ve veri işleme süreçleri için gerekli bağımlılıklar. |

## Gelecek Güncellemeler [Roadmap]
+ **Bildirim Sistemi** : Yeni not girişi algılandığında sesli bildirim gönderilecek.
+ **Geliştirilmiş Kimlik Doğrulaması** : Cookie kullanmak yerine, programın öğrenci numarası ve şifre ile çalıştırılabilmesi.

## Katkıda Bulunma
Hata raporları veya özellik önerileri için lütfen GitHub Issues bölümünü kullanın.

## Lisans
Bu proje **GNU Genel Kamu Lisansı sürüm 3 (GPLv3)** ile lisanslanmıştır.
