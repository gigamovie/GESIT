import requests
import os

URL = os.getenv("VIDEO_URL")
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_VIDEO.mp4"

def kirim_ke_telegram():
    print("📤 Mengirim ke Telegram...")
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    with open(FILE_NAME, 'rb') as f:
        # Menambahkan caption agar terlihat rapi
        payload = {'chat_id': CHAT_ID, 'caption': '🚀 File GESIT sudah mendarat!'}
        files = {'document': f}
        r = requests.post(url, data=payload, files=files)
    
    if r.status_code == 200:
        print("✅ Berhasil dikirim ke Telegram!")
    else:
        print(f"❌ Gagal: {r.text}")

def download():
    print(f"📥 GESIT sedang menarik file...")
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        with open(FILE_NAME, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                f.write(chunk)
    print("✅ Download Selesai.")
    kirim_ke_telegram()

if __name__ == "__main__":
    download()
