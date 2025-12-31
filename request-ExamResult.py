import requests
import time
from bs4 import BeautifulSoup

#OBS DPU Öğrencileri için yapılmıştır.
while(True):

    print("Cookie'yi giriniz.")
    cookieValue = str(input())
    if cookieValue == "":
        print("Lütfen bir cookie girişi yapınız.")
    else:
            while(True):
                dersler = []
                dersler.clear()
                headers = {
                    "accept": "*/*",
                    "cookie": cookieValue,
                    "cache-control": "no-cache",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "origin": "https://obs.dpu.edu.tr",
                    "referer": "https://obs.dpu.edu.tr/oibs/std/index.aspx?curOp=0"
                    }

                URl = "https://obs.dpu.edu.tr/oibs/std/not_listesi_op.aspx"
                response = requests.get(URl, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                rows = soup.select("#grd_not_listesi tr")[1:]
                    
                    
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) > 7:
                        ders_adi = cells[2].text.strip()

                        # Vize notunu al
                        vize_element = cells[4].find("span", string=lambda x: "Vize" in x if x else False)
                        final_element = cells[4].find("span", string=lambda x: "Final" in x if x else False)
                        vize = None
                        final = None
                        if vize_element:
                            vize = vize_element.text.split(":")[-1].strip()
                        if final_element:
                            final = final_element.text.split(":")[-1].strip()
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
                    print("Veri bulunamadı cookie'yi doğru girip girmediğinizi kontrol ediniz veya yenileyiniz.")
                    break
                else:
                    print("↓" * 75)
                    for ders in dersler:
                        print(f"Ders : {ders['ders']}")
                        print("-" * 25)
                        print(f"Vize: {ders['vize']}, Final: {ders['final']}, Ort: {ders['ort']}, Not: {ders['not']}, Durum: {ders['durum']}\n")
                    print("↑" * 75)
                    kacSaniyedeBir = 30*60
                    time.sleep(kacSaniyedeBir)
            break