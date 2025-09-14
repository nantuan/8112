import requests
import sys
import time

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

def baca_file_dan_kirim_chunk(file_path, bot_token, channel_id, chunk_size=10):
    """Membaca file, memecah per 10 baris, dan mengirimkannya."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            baris_chunk = []
            for i, baris in enumerate(file):
                baris_chunk.append(baris)
                if (i + 1) % chunk_size == 0:
                    pesan = "\n\n".join(baris_chunk).strip()
                    if pesan:
                        kirim_pesan_telegram(pesan, bot_token, channel_id)
                    baris_chunk = []
                    time.sleep(1)
            
            if baris_chunk:
                pesan = "\n\n".join(baris_chunk).strip()
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

    bot_token = sys.argv[1]
    channel_id = sys.argv[2]
    file_path = sys.argv[3]

    baca_file_dan_kirim_chunk(file_path, bot_token, channel_id)
