import requests
import os

URL = os.getenv("VIDEO_URL").strip() # .strip() untuk hapus spasi liar
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_VIDEO.mp4"

def kirim_ke_telegram():
    print("📤 Mengirim ke Telegram...")
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    try:
        with open(FILE_NAME, 'rb') as f:
            payload = {'chat_id': CHAT_ID, 'caption': '🚀 GESIT: Berhasil Bypass!'}
            files = {'document': f}
            r = requests.post(url, data=payload, files=files)
        print(f"✅ Status Kirim: {r.status_code}")
    except Exception as e:
        print(f"❌ Gagal kirim: {e}")

def download():
    print(f"📥 GESIT Sedang Menyamar & Mendownload...")
    
    # HEADER INI PENTING: Biar disangka Browser asli
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://earnvids.com/',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        with requests.get(URL, headers=headers, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(FILE_NAME, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
        print("✅ Download Selesai.")
        kirim_ke_telegram()
    except Exception as e:
        print(f"❌ Error Download: {e}")

if __name__ == "__main__":
    if URL:
        download()
    else:
        print("❌ URL tidak ditemukan!")
