import threading
import time
import sys
import os

# Mevcut modülleri içe aktar
from python_server import app
from obs_checker import check_obs_grades

def run_flask_server():
    """Flask sunucusunu sessizce arka planda çalıştırır"""
    # Flask loglarını kapatmak istersen:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Sunucuyu başlat
    app.run(host='localhost', port=5000, debug=False, use_reloader=False)

def main():
    print("=" * 50)
    print("🚀 OBS Not Çekme Başlatılıyor...")
    print("=" * 50)

    server_thread = threading.Thread(target=run_flask_server, daemon=True)
    server_thread.start()
    
    print("✅ Sunucu arka planda aktif (http://localhost:5000)")
    print("✅ Not kontrol sistemi devreye alınıyor...")
    print("-" * 50)

    kontrol_araligi = 30 * 60  # 30 dakika
    
    try:
        while True:
            basarili = check_obs_grades()
            
            if basarili:
                print(f"\nSonraki kontrol {kontrol_araligi // 60 } dakika sonra...")
                time.sleep(kontrol_araligi)
            else:
                print("\nBir durum oluştu (Cookie yok veya hata). 1 dakika sonra tekrar denenecek...")
                time.sleep(60)
                
    except KeyboardInterrupt:
        print("\nProgram kapatılıyor...")
        sys.exit(0)

if __name__ == "__main__":
    main()