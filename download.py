import requests
import os
import time

# Ambil data dari Secrets
URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_VIDEO.mp4"

def download_video():
    print(f"📡 GESIT Memulai Operasi...")
    # Header sakti agar tidak diblokir server video
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': '*/*',
    }
    
    with requests.get(URL, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        print(f"📦 Ukuran File: {total_size / (1024*1024):.2f} MB")
        
        with open(FILE_NAME, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
    print("✅ Video berhasil ditarik ke Server GitHub.")

def upload_to_gofile():
    print("🚀 Meluncur ke GoFile (Server Super Kencang)...")
    try:
        # 1. Dapatkan server terbaik
        server_res = requests.get("https://api.gofile.io/getServer").json()
        server = server_res['data']['server']
        
        # 2. Upload file
        with open(FILE_NAME, 'rb') as f:
            upload_res = requests.post(
                f"https://{server}.gofile.io/uploadFile",
                files={'file': f}
            ).json()
        
        if upload_res['status'] == 'ok':
            return upload_res['data']['downloadPage']
    except Exception as e:
        print(f"❌ Gagal Upload: {e}")
    return None

def kirim_notif(link):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    pesan = (
        "🚀 **GESIT DOWNLOAD SELESAI!**\n\n"
        "File siap diambil dengan kecepatan penuh:\n"
        f"🔗 [KLIK DI SINI UNTUK SIMPAN]({link})\n\n"
        "_Tips: Klik link, lalu tekan tombol download di browser HP._"
    )
    payload = {
        'chat_id': CHAT_ID,
        'text': pesan,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': False
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    if not URL:
        print("❌ Mana link videonya? Input kosong!")
    else:
        try:
            start_time = time.time()
            download_video()
            link = upload_to_gofile()
            
            if link:
                kirim_notif(link)
                durasi = time.time() - start_time
                print(f"⚡ Operasi selesai dalam {durasi:.2f} detik!")
            else:
                print("❌ Gagal mendapatkan link GoFile.")
        except Exception as e:
            print(f"💥 ERROR: {e}")
