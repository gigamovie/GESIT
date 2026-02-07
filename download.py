import requests
import os
import time

URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_VIDEO.mp4"

def download_video():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    print("📥 Menarik file ke server...")
    try:
        with requests.get(URL, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(FILE_NAME, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
            return True
    except Exception as e:
        print(f"Gagal download: {e}")
        return False

def upload_catbox():
    try:
        with open(FILE_NAME, 'rb') as f:
            r = requests.post('https://catbox.moe/user/api.php', data={'reqtype': 'fileupload'}, files={'fileToUpload': f}, timeout=120)
        return r.text.strip() if r.status_code == 200 else None
    except: return None

def upload_gofile():
    try:
        server = requests.get("https://api.gofile.io/getServer").json()['data']['server']
        with open(FILE_NAME, 'rb') as f:
            r = requests.post(f"https://{server}.gofile.io/uploadFile", files={'file': f}).json()
        return r['data']['downloadPage'] if r['status'] == 'ok' else None
    except: return None

if __name__ == "__main__":
    if download_video():
        # Coba Catbox dulu, kalau gagal coba GoFile
        link = upload_catbox() or upload_gofile()
        
        if link:
            msg = f"✅ **GESIT SUKSES!**\n\nVideo siap disimpan:\n🔗 {link}"
        else:
            msg = "❌ Video berhasil didownload, tapi semua gudang (Catbox/GoFile) penuh."
        requests.post(f"https://api.api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    else:
        # Jika masih 403 Forbidden
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': "❌ Gagal: Link ini memblokir akses server (IP-Lock). Coba gunakan link dari downloader pihak ketiga."})
