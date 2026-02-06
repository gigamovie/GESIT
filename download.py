import requests
import os
import time

# Mengambil link dari input GitHub Actions
url = os.getenv("VIDEO_URL")
nama_file = "GESIT_DOWNLOAD.mp4"

def unduh_gesit():
    print("=========================================")
    print("🚀 GESIT: Downloader Super Cepat Dimulai")
    print("=========================================")
    print(f"🔗 Sumber: {url}")
    
    start_time = time.time()
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            
            with open(nama_file, 'wb') as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=1024*1024): # Potongan 1MB
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        # Log sederhana agar kita tahu proses berjalan
                        if total_size > 0:
                            done = int(50 * downloaded / total_size)
                            print(f"\r📦 Progress: [{'=' * done}{' ' * (50-done)}] {downloaded//(1024*1024)}MB", end="")
            
        end_time = time.time()
        print(f"\n\n✅ GESIT Selesai dalam {round(end_time - start_time, 2)} detik!")
        
    except Exception as e:
        print(f"\n❌ Gagal mengunduh: {e}")

if __name__ == "__main__":
    if url:
        unduh_gesit()
    else:
        print("❌ Error: Link tidak ditemukan di sistem GESIT!")
