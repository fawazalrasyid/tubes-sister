import socket
import threading
import time

# Database untuk antrian setiap klinik
data_antrean = {}

# Database untuk klinik yang buka
data_klinik = {"Klinik Mata", "Klinik Gigi", "Klinik Umum"}

# Database untuk jam buka dan tutup klinik
jadwal_klinik = {
   "Klinik Umum": {"buka": 8, "tutup": 22},
    "Klinik Mata": {"buka": 9, "tutup": 22},
    "Klinik Gigi": {"buka": 8, "tutup": 22},
}


# Fungsi untuk proses pendaftaran pasien
def pendaftaran_pasien(data):
    klinik, nomor_rekam_medis, nama, tanggal_lahir = data.split("|")

    waktu_pasien = 15 * 60
    #max_pasien = ( jadwal_klinik[klinik]["tutup"] - jadwal_klinik[klinik]["buka"] ) / (waktu_pasien / 3600)
    max_pasien = 10
    
    # Reset queue for the current day
    today = time.strftime("%Y-%m-%d")
    data_antrean[today] = data_antrean.get(today, [])

    # Cek apakah mendaftar di luar jam buka klinik
    waktu_sekarang = time.localtime()
    jam_sekarang = waktu_sekarang.tm_hour

    if jam_sekarang < jadwal_klinik[klinik]["buka"]:
        # Mendaftar sebelum jam buka
        if len(data_antrean[today]) >= max_pasien :
            hari_mendatang = 1
            while True:
                next_day = time.strftime("%Y-%m-%d", time.localtime(time.time() + hari_mendatang * 24 * 3600))
                data_antrean[next_day] = data_antrean.get(next_day, [])

                if len(data_antrean[next_day]) < max_pasien:
                    nomor_antrean = len(data_antrean[next_day]) + 1

                    data_antrean[next_day].append({
                        "nomor_antrean": nomor_antrean,
                        "nomor_rekam_medis": nomor_rekam_medis,
                        "nama": nama,
                        "tanggal_lahir": tanggal_lahir,
                        "timestamp": time.time()
                    })

                    waktu_buka = time.mktime(waktu_sekarang[:3] + (jadwal_klinik[klinik]["buka"], 0, 0, 0, 0, 0))
                    perkiraan_waktu = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(waktu_buka + nomor_antrean * waktu_pasien))
                    
                    return f"Berhasil mendaftar di {klinik}, Nomor antrean: {nomor_antrean}.\nPerkiraan waktu antrean: {perkiraan_waktu}"
                
                hari_mendatang += 1
        else:
            # Mendaftar saat klinik masih buka dan tidak full
            nomor_antrean = len(data_antrean[today]) + 1

            data_antrean[today].append({
                "nomor_antrean": nomor_antrean,
                "nomor_rekam_medis": nomor_rekam_medis,
                "nama": nama,
                "tanggal_lahir": tanggal_lahir,
                "timestamp": time.time()
            })

            perkiraan_waktu = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + nomor_antrean * waktu_pasien))

            return f"Berhasil mendaftar di {klinik}, Nomor antrean: {nomor_antrean}.\nPerkiraan waktu antrean: {perkiraan_waktu}"

    # Mendaftar saat klinik sudah tutup
    if jam_sekarang >= jadwal_klinik[klinik]["tutup"]:
        # Cek apakah hari ini sudah penuh, jika ya, cari hari berikutnya yang belum penuh
        hari_mendatang = 1
        while True:
            next_day = time.strftime("%Y-%m-%d", time.localtime(time.time() + hari_mendatang * 24 * 3600))
            data_antrean[next_day] = data_antrean.get(next_day, [])

            if len(data_antrean[next_day]) < max_pasien:
                nomor_antrean = len(data_antrean[next_day]) + 1

                data_antrean[next_day].append({
                    "nomor_antrean": nomor_antrean,
                    "nomor_rekam_medis": nomor_rekam_medis,
                    "nama": nama,
                    "tanggal_lahir": tanggal_lahir,
                    "timestamp": time.time()
                })
                waktu_buka = time.mktime(waktu_sekarang[:3] + (jadwal_klinik[klinik]["buka"], 0, 0, 0, 0, 0))
                perkiraan_waktu = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(waktu_buka + hari_mendatang * 24 * 3600 + nomor_antrean * waktu_pasien))
                    
                return f"Berhasil mendaftar di {klinik}, Nomor antrean: {nomor_antrean}.\nPerkiraan waktu antrean: {perkiraan_waktu}"
            
            hari_mendatang += 1

    # Mendaftar saat klinik masih buka
    if jadwal_klinik[klinik]["buka"] <= jam_sekarang < jadwal_klinik[klinik]["tutup"]:
        # Cek apakah hari ini sudah penuh, jika ya, cari hari berikutnya yang belum penuh
        if len(data_antrean[today]) >= max_pasien:
            hari_mendatang = 1
            while True:
                next_day = time.strftime("%Y-%m-%d", time.localtime(time.time() + hari_mendatang * 24 * 3600))
                data_antrean[next_day] = data_antrean.get(next_day, [])

                if len(data_antrean[next_day]) < max_pasien:
                    nomor_antrean = len(data_antrean[next_day]) + 1

                    data_antrean[next_day].append({
                        "nomor_antrean": nomor_antrean,
                        "nomor_rekam_medis": nomor_rekam_medis,
                        "nama": nama,
                        "tanggal_lahir": tanggal_lahir,
                        "timestamp": time.time()
                    })

                    waktu_buka = time.mktime(waktu_sekarang[:3] + (jadwal_klinik[klinik]["buka"], 0, 0, 0, 0, 0))
                    perkiraan_waktu = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(waktu_buka + hari_mendatang * 24 * 3600 + nomor_antrean * waktu_pasien))
                    
                    return f"Berhasil mendaftar di {klinik}, Nomor antrean: {nomor_antrean}.\nPerkiraan waktu antrean: {perkiraan_waktu}"
                
                hari_mendatang += 1
        else:
            # Mendaftar saat klinik masih buka dan tidak full
            nomor_antrean = len(data_antrean[today]) + 1

            data_antrean[today].append({
                "nomor_antrean": nomor_antrean,
                "nomor_rekam_medis": nomor_rekam_medis,
                "nama": nama,
                "tanggal_lahir": tanggal_lahir,
                "timestamp": time.time()
            })

            perkiraan_waktu = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + nomor_antrean * waktu_pasien))

            return f"Berhasil mendaftar di {klinik}, Nomor antrean: {nomor_antrean}.\nPerkiraan waktu antrean: {perkiraan_waktu}"

    return "Waktu mendaftar tidak valid."


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
    