import requests
import os
import time

URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_VIDEO.mp4"

def download_video():
    # Header yang SANGAT LENGKAP agar dikira Chrome asli di Windows 11
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    
    print(f"📡 Memulai operasi penyamaran ke: {URL[:30]}...")
    
    session = requests.Session() # Gunakan Session agar lebih stabil
    
    for i in range(2):
        try:
            with session.get(URL, headers=headers, stream=True, timeout=45) as r:
                r.raise_for_status()
                with open(FILE_NAME, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        if chunk: f.write(chunk)
                return True
        except Exception as e:
            print(f"⚠️ Gagal di percobaan {i+1}: {e}")
            time.sleep(3)
    return False

def upload_to_gofile():
    try:
        server_res = requests.get("https://api.gofile.io/getServer", timeout=10).json()
        server = server_res['data']['server']
        with open(FILE_NAME, 'rb') as f:
            upload_res = requests.post(f"https://{server}.gofile.io/uploadFile", files={'file': f}, timeout=60).json()
        return upload_res['data']['downloadPage'] if upload_res['status'] == 'ok' else None
    except:
        return None

if __name__ == "__main__":
    if not URL:
        print("URL Kosong")
    elif download_video():
        link = upload_to_gofile()
        msg = f"✅ **GESIT BERHASIL!**\n\nSiap simpan ke galeri:\n🔗 {link}" if link else "❌ Download Oke, tapi Gagal Upload ke GoFile."
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    else:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': "❌ Server video masih memblokir akses GESIT."})
