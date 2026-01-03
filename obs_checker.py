import requests
import time
from bs4 import BeautifulSoup
import sys
import os
from datetime import datetime

# python_server.py'den fonksiyonu import et
sys.path.append(os.path.dirname(__file__))
from python_server import get_saved_cookie


def get_user_selection_auto():
    """Sadece dönem bilgisini sorar, yılı otomatik hesaplar"""
    print("\nDönem Seçimi")
    print("-" * 30)
    
    # Şu anki tarihi al
    simdi = datetime.now()
    mevcut_yil = simdi.year
    mevcut_ay = simdi.month
    if mevcut_ay < 9:
        akademik_yil_baslangic = mevcut_yil - 1
    else:
        akademik_yil_baslangic = mevcut_yil

    while True:
        print("Hangi dönemdesiniz?")
        secim = input("Seçiminiz (1/Güz veya 2/Bahar): ").strip().lower()
        
        donem_kodu = ""
        donem_adi = ""
        
        if secim in ['1', 'güz', 'guz']:
            donem_kodu = f"{akademik_yil_baslangic}1"
            donem_adi = "Güz"
            break
            
        elif secim in ['2', 'bahar']:
            donem_kodu = f"{akademik_yil_baslangic}2"
            donem_adi = "Bahar"
            break
        else:
            print("Hatalı giriş! Lütfen sadece '1' veya '2' yazınız.\n")

    print(f"\nAlgılanan Akademik Dönem: {akademik_yil_baslangic}-{akademik_yil_baslangic+1} {donem_adi}")
    print(f"Sunucuya Gönderilecek Kod: {donem_kodu}")
    
    return donem_kodu

def check_obs_grades():
    """OBS'den belirli bir dönem için notları çek"""

    HEDEF_DONEM = get_user_selection_auto()

    cookie_value = get_saved_cookie()
    if not cookie_value:
        print("Cookie bulunamadı! Extension ile giriş yapın.")
        return False
    
    url = "https://obs.dpu.edu.tr/oibs/std/not_listesi_op.aspx"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie_value,
        "Origin": "https://obs.dpu.edu.tr",
        "Referer": "https://obs.dpu.edu.tr/oibs/std/not_listesi_op.aspx"
    }
    
    try:
        #GET isteği (ViewState kodlarını çalmak için)
        print("Sayfa verileri alınıyor...")
        session = requests.Session()
        response_get = session.get(url, headers=headers)
        
        if response_get.status_code != 200:
            print("Sayfaya erişilemedi. Cookie süresi dolmuş olabilir.")
            return False

        # HTML'i parçala gizli kodları bul
        soup = BeautifulSoup(response_get.content, "html.parser")
        
        viewstate = soup.find("input", {"id": "__VIEWSTATE"})
        viewstate_gen = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})
        event_validation = soup.find("input", {"id": "__EVENTVALIDATION"})
        
        if not viewstate:
            print("ViewState bulunamadı! OBS yapısı değişmiş veya giriş düşmüş.")
            return False

        #POST İsteği (Dönemi değiştirip veriyi çekmek için)
        print(f"Dönem {HEDEF_DONEM} olarak ayarlanıyor ve notlar çekiliyor...")
        
        payload = {
            "__EVENTTARGET": "cmbDonemler", # Dönem kutusunu tetikliyoruz
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": viewstate["value"],
            "__VIEWSTATEGENERATOR": viewstate_gen["value"] if viewstate_gen else "",
            "__EVENTVALIDATION": event_validation["value"] if event_validation else "",
            "cmbDonemler": HEDEF_DONEM,
            "txtDersAd": ""
        }
        
        # POST isteğini gönder
        response_post = session.post(url, headers=headers, data=payload)
        soup_post = BeautifulSoup(response_post.content, "html.parser")
        
        donem_select = soup_post.find("select", {"id": "cmbDonemler"})
        if donem_select:
            secili_option = donem_select.find("option", selected=True)
            if secili_option:
                gelen_donem = secili_option['value']
                
                # Eğer istediğimiz kod (hedef) ile gelen kod farklıysa,
                # sunucu bizi varsayılan döneme atmış demektir.
                if gelen_donem != HEDEF_DONEM:
                    print("\n" + "!"*60)
                    print(f"UYARI: {HEDEF_DONEM} dönemi henüz sistemde AKTİF DEĞİL!")
                    print(f"Sunucu otomatik olarak mevcut dönemi ({gelen_donem}) gösteriyor.")
                    print(f"Yanlış veri göstermemek için işlem iptal ediliyor.")
                    print("!"*60 + "\n")
                    return False

        # Tabloyu bul (ID bazen değişebilir, kontrol ediyoruz)
        rows = soup_post.select("#grd_not_listesi tr")[1:]
        
        dersler = []
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 7:
                ders_adi = cells[2].text.strip()
                
                vize_element = cells[4].find("span", string=lambda x: "Vize" in x if x else False)
                final_element = cells[4].find("span", string=lambda x: "Final" in x if x else False)
                
                vize = vize_element.text.split(":")[-1].strip() if vize_element else None
                final = final_element.text.split(":")[-1].strip() if final_element else None
                
                ort = cells[5].text.strip()
                not_degeri = cells[6].text.strip()
                durum = cells[7].text.strip()

                dersler.append({
                    "ders": ders_adi,
                    "vize": vize,
                    "final": final,
                    "ort": ort,
                    "not": not_degeri,
                    "durum": durum
                })

        if not dersler:
            print(f"{HEDEF_DONEM} dönemi için not bulunamadı veya tablo boş.")
            return False
        
        # Sonuçları yazdır
        print("=" * 75)
        print(f"Not Listesi ({HEDEF_DONEM}) - {time.strftime('%d.%m.%Y %H:%M:%S')}")
        print("=" * 75)
        
        for ders in dersler:
            print(f"\nDers: {ders['ders']}")
            print("-" * 50)
            print(f"   Vize: {ders['vize'] or 'Girilmedi'}")
            print(f"   Final: {ders['final'] or 'Girilmedi'}")
            print(f"   Ortalama: {ders['ort'] or '-'}")
            print(f"   Harf Notu: {ders['not'] or '-'}")
            print(f"   Durum: {ders['durum'] or '-'}")
        
        print("\n" + "=" * 75)
        return True
        
    except Exception as e:
        print(f"Beklenmeyen hata: {str(e)}")
        return False