import requests
import os

# Ambil data dan bersihkan spasi liar
URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_VIDEO.mp4"

def download():
    # Penyamaran agar tidak dianggap BOT (Bypass 403)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    
    print(f"📡 Mencoba menembus server...")
    try:
        with requests.get(URL, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(FILE_NAME, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    f.write(chunk)
        print("✅ File berhasil diamankan di server GitHub!")
        return True
    except Exception as e:
        print(f"❌ Gagal Total: {e}")
        return False

def kirim_ke_telegram():
    if not os.path.exists(FILE_NAME):
        return
    
    print("📤 Mengirim hasil ke Telegram...")
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(FILE_NAME, 'rb') as f:
        r = requests.post(url, data={'chat_id': CHAT_ID, 'caption': '🚀 GESIT Berhasil!'}, files={'document': f})
    print(f"📬 Status Telegram: {r.status_code}")

if __name__ == "__main__":
    if URL and download():
        kirim_ke_telegram()
    else:
        print("📭 Tidak ada file yang bisa diproses.")
