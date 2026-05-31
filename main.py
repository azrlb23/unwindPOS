"""
Entry Point Utama (main.py)
Menjalankan analisis kompleksitas algoritma rekursif sesuai spesifikasi SRS.
"""

from src.benchmark import run_all_benchmarks
from src.visualizer import plot_performance


def print_progress(size: int, avg_time: float):
    """
    Callback untuk mencetak ringkasan hasil ke terminal sesuai spesifikasi KF-05.
    """
    print(f"Jumlah Proses : {size}")
    print(f"Rata-rata Waktu : {avg_time:.6f} detik")
    print("-" * 40)


def main():
    """
    Fungsi utama untuk mengoordinasi jalannya program dari pengujian hingga visualisasi.
    """
    print("=" * 55)
    print(" SISTEM ANALISIS KOMPLEKSITAS ALGORITMA REKURSIF ")
    print(" Optimasi Pemindahan Data dan Penjadwalan Proses ")
    print("=" * 55)
    print("Memulai pengujian...\n")

    # Menjalankan benchmark dengan callback pencetakan hasil (KF-04 & KF-05)
    results = run_all_benchmarks(callback=print_progress)

    print("\nPengujian selesai!")

    # Membuat dan menampilkan visualisasi grafik kinerja (KF-06)
    plot_performance(results)


if __name__ == "__main__":
    main()
