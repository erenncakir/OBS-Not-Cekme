import threading
import time
import sys
import os

# Renkli konsol çıktısı için
from colorama import init, Fore, Style
init(autoreset=False)

# Mevcut modülleri içe aktar
from python_server import app
from obs_checker import check_obs_grades

def run_flask_server():
    """Flask sunucusunu TAMAMEN sessizce arka planda çalıştırır"""
    # Flask loglarını devre dışı bırak
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    import sys
    from flask import cli
    
    # Flask'ın banner fonksiyonunu boş bir fonksiyonla değiştir
    cli.show_server_banner = lambda *args: None

    # Sunucuyu başlat
    app.run(host='localhost', port=5000, debug=False, use_reloader=False)

def main():

    print(Fore.CYAN+"=" * 50)
    print(Fore.CYAN+" OBS Not Çekme Başlatılıyor...")
    print(Fore.CYAN+"=" * 50)

    server_thread = threading.Thread(target=run_flask_server, daemon=True)
    server_thread.start()
    
    print(Fore.GREEN+" Sunucu arka planda aktif (http://localhost:5000)")
    print(Fore.GREEN+" Not kontrol sistemi devreye alınıyor...")
    print(Fore.CYAN+"-" * 50)

    kontrol_araligi = 30 * 60  # 30 dakika
    
    try:
        while True:
            basarili = check_obs_grades()
            
            if basarili:
                print(Fore.YELLOW+f"\nSonraki kontrol {kontrol_araligi // 60 } dakika sonra...")
                time.sleep(kontrol_araligi)
            else:
                print(Fore.RED+"\nBir durum oluştu (Cookie yok veya hata). 1 dakika sonra tekrar denenecek...")
                time.sleep(60)
                
    except KeyboardInterrupt:
        print("\nProgram kapatılıyor...")
        sys.exit(0)

if __name__ == "__main__":
    main()