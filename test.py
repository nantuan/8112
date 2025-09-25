import requests
import sys
import random # Impor modul random
import time # Meskipun tidak terpakai, tetap dipertahankan

def kirim_pesan_telegram(pesan, bot_token, channel_id):
    """Mengirim pesan ke channel Telegram."""
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': channel_id,
        'text': pesan
    }
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        print("Pesan berhasil dikirim.")
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengirim pesan: {e}")

def baca_file_dan_kirim_acak(file_path, bot_token, channel_id, jumlah_baris=10):
    """Membaca file, memilih 10 baris acak, dan mengirimkannya sekali."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 1. Baca semua baris ke dalam list
            semua_baris = file.readlines()
            
            # Hapus baris kosong (opsional, untuk memastikan kualitas konten yang dikirim)
            baris_bersih = [baris.strip() for baris in semua_baris if baris.strip()]

            # Pastikan jumlah baris dalam file mencukupi
            if len(baris_bersih) < jumlah_baris:
                print(f"Error: Jumlah baris dalam file ({len(baris_bersih)}) kurang dari yang diminta ({jumlah_baris}).")
                # Jika baris kurang, kirim semua baris yang ada
                baris_terpilih = baris_bersih
            else:
                # 2. Pilih sejumlah 'jumlah_baris' (10) baris secara acak
                baris_terpilih = random.sample(baris_bersih, jumlah_baris)

            # 3. Gabungkan baris-baris terpilih dengan pemisah \n\n
            pesan = "\n\n".join(baris_terpilih)

            # 4. Kirim pesan
            if pesan:
                kirim_pesan_telegram(pesan, bot_token, channel_id)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Penggunaan: python3 kirim.py <BOT_TOKEN> <CHANNEL_ID> <FILE_PATH>")
        sys.exit(1)

    # Ambil argumen dari baris perintah
    bot_token = sys.argv[1]
    channel_id = sys.argv[2]
    file_path = sys.argv[3]

    # Panggil fungsi baru
    baca_file_dan_kirim_acak(file_path, bot_token, channel_id)
