import os
import requests
import subprocess
import time

URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_TURBO.mp4"

def download_turbo(url):
    print(f"🚀 Memulai Download Turbo: {url}")
    try:
        # Menggunakan aria2c: 16 koneksi, membagi file jadi 16 bagian
        cmd = [
            'aria2c', 
            '-x', '16',      # 16 koneksi per server
            '-s', '16',      # Bagi file jadi 16 bagian
            '-j', '16',      # Maksimal 16 download simultan
            '-k', '1M',      # Ukuran bagian terkecil 1MB
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '-o', FILE_NAME,
            url
        ]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"❌ Turbo Gagal: {e}")
        return False

def upload_catbox():
    print("📤 Mengirim hasil ke Catbox...")
    try:
        with open(FILE_NAME, 'rb') as f:
            r = requests.post('https://catbox.moe/user/api.php', 
                            data={'reqtype': 'fileupload'}, 
                            files={'fileToUpload': f}, timeout=300)
        return r.text.strip() if r.status_code == 200 else None
    except: return None

if __name__ == "__main__":
    if not URL:
        print("URL Kosong!")
    else:
        start_time = time.time()
        if download_turbo(URL):
            link = upload_catbox()
            durasi = time.time() - start_time
            if link:
                msg = f"⚡ **TURBO GESIT SELESAI!**\n\n⏱ Waktu: {durasi:.1f} detik\n🔗 [DOWNLOAD SEKARANG]({link})"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
