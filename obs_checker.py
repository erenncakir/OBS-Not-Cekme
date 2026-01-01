import requests
import time
from bs4 import BeautifulSoup
import sys
import os

# python_server.py'den fonksiyonu import et
sys.path.append(os.path.dirname(__file__))
from python_server import get_saved_cookie

def check_obs_grades():
    """OBS'den notları çek"""
    # Kaydedilmiş cookie'yi al
    cookie_value = get_saved_cookie()
    
    if not cookie_value:
        print("❌ Cookie bulunamadı!")
        print("1. Chrome Extension'ı yükleyin")
        print("2. OBS'ye giriş yapın")
        print("3. Not listesine gidin")
        print("4. python_server.py'yi çalıştırın")
        return False
    
    headers = {
        "accept": "*/*",
        "cookie": cookie_value,
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://obs.dpu.edu.tr",
        "referer": "https://obs.dpu.edu.tr/oibs/std/index.aspx?curOp=0"
    }

    url = "https://obs.dpu.edu.tr/oibs/std/not_listesi_op.aspx"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Hata: HTTP {response.status_code}")
            print("Cookie'nin süresi dolmuş olabilir. Yeniden giriş yapın.")
            return False
        
        soup = BeautifulSoup(response.content, "html.parser")
        rows = soup.select("#grd_not_listesi tr")[1:]
        
        dersler = []
        
        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 7:
                ders_adi = cells[2].text.strip()

                # Vize ve final notlarını al
                vize_element = cells[4].find("span", string=lambda x: "Vize" in x if x else False)
                final_element = cells[4].find("span", string=lambda x: "Final" in x if x else False)
                
                vize = vize_element.text.split(":")[-1].strip() if vize_element else None
                final = final_element.text.split(":")[-1].strip() if final_element else None
                
                # Ort, Not ve Durum değerlerini al
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

        # Sonuçları yazdır
        if not dersler:
            print("⚠️  Veri bulunamadı. Cookie geçersiz olabilir.")
            return False
        
        print("=" * 75)
        print(f"📊 Not Listesi - {time.strftime('%d.%m.%Y %H:%M:%S')}")
        print("=" * 75)
        
        for ders in dersler:
            print(f"\n📚 Ders: {ders['ders']}")
            print("-" * 50)
            print(f"   Vize: {ders['vize'] or 'Girilmedi'}")
            print(f"   Final: {ders['final'] or 'Girilmedi'}")
            print(f"   Ortalama: {ders['ort'] or '-'}")
            print(f"   Harf Notu: {ders['not'] or '-'}")
            print(f"   Durum: {ders['durum'] or '-'}")
        
        print("\n" + "=" * 75)
        return True
        
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {str(e)}")
        return False

if __name__ == '__main__':
    print("🎓 OBS Not Takip Sistemi")
    print("=" * 75)
    
    kontrol_araligi = 30 * 60  # 30 dakika (saniye cinsinden)
    
    while True:
        basarili = check_obs_grades()
        
        if basarili:
            print(f"\n⏰ Sonraki kontrol {kontrol_araligi // 60} dakika sonra...")
            time.sleep(kontrol_araligi)
        else:
            print("\n⚠️  Hata oluştu. 5 dakika sonra tekrar denenecek...")
            time.sleep(5 * 60)  # 5 dakika bekle