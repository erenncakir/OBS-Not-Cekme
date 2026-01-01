from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Extension'dan gelen isteklere izin ver

# Şifreleme anahtarı (ilk çalıştırmada oluştur)
KEY_FILE = 'secret.key'
COOKIE_FILE = 'cookie_encrypted.dat'

def get_or_create_key():
    """Şifreleme anahtarını al veya oluştur"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        return key

# Şifreleme nesnesi
cipher = Fernet(get_or_create_key())

@app.route('/health', methods=['GET'])
def health_check():
    """Sunucunun çalışıp çalışmadığını kontrol et"""
    return jsonify({"status": "ok", "message": "Python sunucusu çalışıyor!"}), 200

@app.route('/receive_cookie', methods=['POST'])
def receive_cookie():
    """Extension'dan cookie al ve şifrele"""
    try:
        data = request.json
        cookie = data.get('cookie')
        timestamp = data.get('timestamp')
        
        if not cookie:
            return jsonify({"error": "Cookie bulunamadı"}), 400
        
        # Cookie'yi şifrele
        encrypted_cookie = cipher.encrypt(cookie.encode())
        
        # Dosyaya kaydet
        with open(COOKIE_FILE, 'wb') as f:
            f.write(encrypted_cookie)
        
        # Log dosyasına kaydet (debug için)
        log_data = {
            "timestamp": timestamp,
            "received": datetime.now().isoformat(),
            "cookie_length": len(cookie)
        }
        
        with open('cookie_log.json', 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"✓ Cookie alındı ve kaydedildi! ({timestamp})")
        return jsonify({"status": "success", "message": "Cookie kaydedildi"}), 200
        
    except Exception as e:
        print(f"✗ Hata: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_saved_cookie():
    """Kaydedilmiş cookie'yi çöz ve döndür"""
    try:
        if not os.path.exists(COOKIE_FILE):
            return None
        
        with open(COOKIE_FILE, 'rb') as f:
            encrypted_cookie = f.read()
        
        # Şifreyi çöz
        decrypted_cookie = cipher.decrypt(encrypted_cookie).decode()
        return decrypted_cookie
        
    except Exception as e:
        print(f"Cookie çözme hatası: {str(e)}")
        return None

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 OBS Cookie Sunucusu Başlatılıyor...")
    print("=" * 50)
    print("📡 Sunucu: http://localhost:5000")
    print("🔒 Şifreleme: Aktif")
    print("=" * 50)
    
    app.run(host='localhost', port=5000, debug=False)