import socket
from datetime import datetime

def register_to_server(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 5555))
    client.send(data.encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    print(response)
    client.close()

# Fungsi untuk memeriksa apakah string tanggal valid
def is_valid_date(date_string):
    try:
        # Coba mengurai string tanggal sesuai dengan format "YYYY-MM-DD"
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    print("Selamat datang di Program Antrean Registrasi Medis")
    print("Silakan registrasi untuk mendapatkan nomor antrean.")
    print("")

    while True:
        print("==========Daftar Klinik==========")
        print("Klinik Umum | 08.00 - 23.00 \nKlinik Mata | 09.00 - 22.00 \nKlinik Gigi | 08.00 - 22.00")
        clinic = input("Pilih klinik : ")

        # Memeriksa apakah klinik valid
        if clinic not in {"Klinik Umum", "Klinik Mata", "Klinik Gigi"}:
            print(f"{clinic} tidak buka atau tidak valid.")
        else:
            break

    medical_record_number = input("Masukkan nomor rekam medis: ")
    name = input("Masukkan nama: ")

    
    while True:
        birth_date = input("Masukkan tanggal lahir (YYYY-MM-DD): ")

        if not is_valid_date(birth_date):
            print("Format tanggal lahir tidak valid. Harap masukkan dengan format YYYY-MM-DD.")
        else:
            break

    #birth_date = input("Masukkan tanggal lahir (YYYY-MM-DD): ")

    # Format data: Klinik|NomorRekamMedis|Nama|TanggalLahir
    data = f"{clinic}|{medical_record_number}|{name}|{birth_date}"

    register_to_server(data)
