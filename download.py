import requests
import os
import time

URL = os.getenv("VIDEO_URL", "").strip()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FILE_NAME = "GESIT_VIDEO.mp4"

def download_video():
    print(f"📡 Mencoba menarik file dari: {URL[:50]}...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    
    # Mencoba download hingga 3 kali jika gagal
    for i in range(3):
        try:
            with requests.get(URL, headers=headers, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(FILE_NAME, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        if chunk: f.write(chunk)
                print(f"✅ Download Sukses di percobaan ke-{i+1}")
                return True
        except Exception as e:
            print(f"⚠️ Percobaan {i+1} gagal: {e}")
            time.sleep(2)
    return False

def upload_to_gofile():
    print("🚀 Mengunggah ke GoFile...")
    try:
        server_res = requests.get("https://api.gofile.io/getServer").json()
        server = server_res['data']['server']
        with open(FILE_NAME, 'rb') as f:
            upload_res = requests.post(f"https://{server}.gofile.io/uploadFile", files={'file': f}).json()
        if upload_res['status'] == 'ok':
            return upload_res['data']['downloadPage']
    except:
        return None

if __name__ == "__main__":
    if download_video():
        link = upload_to_gofile()
        if link:
            msg = f"✅ **GESIT BERHASIL!**\n\nLink Download:\n🔗 {link}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
            print("📬 Link dikirim ke Telegram!")
    else:
        # Kirim pesan ke Telegram kalau gagal biar kamu gak nunggu
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={'chat_id': CHAT_ID, 'text': "❌ GESIT Gagal menarik file. Link mungkin mati atau diblokir."})
        print("❌ Operasi Gagal.")
