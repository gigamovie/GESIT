import os
import requests
import subprocess
import time

URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_ULTRA.mp4"

def download_hybrid(url):
    print(f"🚀 Memulai Download Ultra: {url}")
    try:
        # Perintah sakti: yt-dlp mencari link, lalu dilempar ke aria2c untuk disedot kencang
        cmd = [
            'yt-dlp', 
            '-f', 'mp4/best', 
            '--external-downloader', 'aria2c', 
            '--external-downloader-args', '-x 16 -s 16 -k 1M', 
            '-o', FILE_NAME, 
            url
        ]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"❌ Gagal: {e}")
        return False

def upload_catbox():
    print("📤 Mengirim ke Catbox...")
    if not os.path.exists(FILE_NAME): return None
    try:
        with open(FILE_NAME, 'rb') as f:
            r = requests.post('https://catbox.moe/user/api.php', 
                            data={'reqtype': 'fileupload'}, 
                            files={'fileToUpload': f}, timeout=300)
        return r.text.strip() if r.status_code == 200 else None
    except: return None

if __name__ == "__main__":
    if not URL:
        print("Link Kosong!")
    else:
        start_time = time.time()
        if download_hybrid(URL):
            link = upload_catbox()
            durasi = time.time() - start_time
            if link:
                msg = f"⚡ **GESIT ULTRA SELESAI!**\n\n⏱ Waktu: {durasi:.1f} detik\n🔗 [DOWNLOAD DISINI]({link})"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                # Hapus file setelah upload agar tidak memenuhi storage
                if os.path.exists(FILE_NAME): os.remove(FILE_NAME)
