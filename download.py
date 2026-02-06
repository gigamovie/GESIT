import requests
import os
import time

URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_VIDEO.mp4"

def download_video():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    print(f"📡 Menarik file...")
    try:
        with requests.get(URL, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(FILE_NAME, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            return True
    except: return False

def upload_to_catbox():
    print("📤 Mengirim ke gudang Catbox...")
    try:
        with open(FILE_NAME, 'rb') as f:
            r = requests.post('https://catbox.moe/user/api.php', data={'reqtype': 'fileupload'}, files={'fileToUpload': f}, timeout=150)
        return r.text.strip() if r.status_code == 200 else None
    except: return None

if __name__ == "__main__":
    if download_video():
        link = upload_to_catbox()
        if link:
            msg = f"✅ **GESIT SUKSES!**\n\nSiap simpan ke galeri (Link Catbox):\n🔗 {link}"
        else:
            msg = "❌ Download Oke, tapi semua server pengiriman (GoFile/Catbox) sedang sibuk."
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    else:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': "❌ Gagal menarik video."})
