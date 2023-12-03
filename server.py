import socket
import threading
import time

# Database untuk antrian setiap klinik
data_antrean = {}

# Database untuk klinik yang buka
data_klinik = {"Klinik Mata", "Klinik Gigi", "Klinik Anak"}

# Fungsi untuk proses pendaftaran pasien
def pendaftaran_pasien(data):
    klinik, nomor_rekam_medis, nama, tanggal_lahir = data.split("|")
    
    # Memeriksa apakah klinik valid
    if klinik not in data_klinik:
        return f"{klinik} tidak buka atau tidak valid."

    # Membuat nomor antrian
    if klinik not in data_antrean:
        data_antrean[klinik] = []

    nomor_antrean = len(data_antrean[klinik]) + 1

    data_antrean[klinik].append({
        "nomor_antrean": nomor_antrean,
        "nomor_rekam_medis": nomor_rekam_medis,
        "nama": nama,
        "tanggal_lahir": tanggal_lahir,
        "timestamp": time.time()
    })

    # Perkiraan waktu antrean
    perkiraan_waktu = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + nomor_antrean * 15))

    return f"Berhasil mendaftar di {klinik}, Nomor antrean : {nomor_antrean}. \nPerkiraan waktu antrean: {perkiraan_waktu}"

# Fungsi untuk menangani koneksi dari setiap client
def handle_client(client_socket):
    data = client_socket.recv(1024).decode("utf-8")
    respons = pendaftaran_pasien(data)
    client_socket.send(respons.encode("utf-8"))
    client_socket.close()

# Fungsi untuk menjalankan server
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5555))
    server_socket.listen(5)
    print("Server berjalan...")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    run_server()
