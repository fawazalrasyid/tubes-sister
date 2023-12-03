import socket
#Fungsi untuk Melakukan Registrasi ke Server:

def register_to_server(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 5555))
    client.send(data.encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    print(response)
    client.close()
#Input Data Dari Pengguna:

if __name__ == "__main__":
    print("Selamat datang di Program Antrean Registrasi Medis")
    print("Silakan registrasi untuk mendapatkan nomor antrean.")

    clinic = input("Pilih klinik (Klinik Umum, Klinik Mata, Klinik Gigi): ")
    medical_record_number = input("Masukkan nomor rekam medis: ")
    name = input("Masukkan nama: ")
    birth_date = input("Masukkan tanggal lahir (YYYY-MM-DD): ")

    # Format data: Klinik|NomorRekamMedis|Nama|TanggalLahir
    data = f"{clinic}|{medical_record_number}|{name}|{birth_date}"

    register_to_server(data)
