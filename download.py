import os
import subprocess
import requests
import time
import re

# Ambil data dari Environment GitHub
URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "HASIL_GESIT.mp4"

def send_telegram(message):
    print(f"💬 Telegram: {message}")
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})

def download_engine(url):
    print(f"🚀 Memulai download: {url}")
    
    # User-Agent agar terlihat seperti browser asli (Anti-Bot)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    
    # Jika link YouTube, gunakan yt-dlp sebagai otak dan aria2c sebagai otot
    if "youtube.com" in url or "youtu.be" in url:
        print("📺 Mendeteksi Link YouTube, mengaktifkan mode Bypass...")
        cmd = [
            'yt-dlp',
            '--user-agent', user_agent,
            '--no-check-certificate',
            '-f', 'mp4/best',
            '--external-downloader', 'aria2c',
            '--external-downloader-args', '-x 16 -s 16 -k 1M',
            '-o', FILE_NAME,
            url
        ]
    else:
        # Jika Direct Link, langsung tembak pakai Aria2
        print("🔗 Mendeteksi Direct Link, mengaktifkan Turbo Speed...")
        cmd = [
            'aria2c',
            '--user-agent', user_agent,
            '-x', '16',
            '-s', '16',
            '-k', '1M',
            '--allow-overwrite=true',
            '-o', FILE_NAME,
            url
        ]

    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error Mesin: {e}")
        return False

def upload_to_catbox(file_path):
    print("📤 Mengirim file ke Catbox...")
    if not os.path.exists(file_path):
        return None
    
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                'https://catbox.moe/user/api.php',
                data={'reqtype': 'fileupload'},
                files={'fileToUpload': f},
                timeout=600 # Timeout 10 menit untuk file besar
            )
        if response.status_code == 200:
            return response.text.strip()
    except Exception as e:
        print(f"❌ Gagal upload: {e}")
    return None

if __name__ == "__main__":
    if not URL:
        print("⚠️ URL tidak ditemukan!")
    else:
        start_time = time.time()
        
        # 1. Jalankan Download
        success = download_video(URL) if 'download_video' in globals() else download_engine(URL)
        
        if success and os.path.exists(FILE_NAME):
            # 2. Upload ke Catbox
            download_url = upload_to_catbox(FILE_NAME)
            durasi = time.time() - start_time
            
            if download_url:
                msg = (f"✅ **DOWNLOAD BERHASIL!**\n\n"
                       f"⏱ **Waktu:** {durasi:.1f} detik\n"
                       f"🔗 **Link:** {download_url}")
                send_telegram(msg)
            else:
                send_telegram("❌ Download sukses, tapi gagal upload ke Catbox.")
            
            # 3. Bersihkan file di server GitHub agar hemat ruang
            os.remove(FILE_NAME)
        else:
            send_telegram("❌ Gagal mendownload video. Coba cek link atau gunakan link lain.")
