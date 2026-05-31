"""
Modul Fungsi Rekursif Utama
Mengimplementasikan KF-02 untuk menghitung total waktu eksekusi seluruh proses.
"""


def recursive_total_time(processes: list[tuple[str, int]], index: int = 0) -> int:
    """
    Menjumlahkan seluruh waktu eksekusi proses secara rekursif murni.
    Kondisi dasar: jika indeks mencapai akhir daftar, kembalikan 0.
    """
    # 1. Memeriksa apakah indeks saat ini sudah sama dengan panjang daftar (Kondisi Dasar)
    if index == len(processes):
        return 0

    # 2. Mengambil waktu eksekusi pada posisi indeks saat ini
    current_time = processes[index][1]

    # 3. Rekursi: jumlahkan waktu saat ini dengan hasil pemanggilan berikutnya
    return current_time + recursive_total_time(processes, index + 1)
