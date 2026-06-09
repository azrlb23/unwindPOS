"""
Entry Point Utama (main.py)
Aplikasi CLI interaktif untuk Simulasi Pengurutan Antrian Pemindahan Data (Merge Sort)
dan Penjadwalan Proses (Round Robin), sesuai spesifikasi Tugas Besar PAA.
"""
import sys
import random
import time
import subprocess
from src.analyzer import recursive_merge_sort, recursive_round_robin

def print_header():
    print("=" * 60)
    print(" SISTEM ANALISIS ALGORITMA REKURSIF (TUBES PAA) ")
    print(" 1. Merge Sort (Pengurutan Antrean Data)")
    print(" 2. Round Robin (Penjadwalan Proses CPU)")
    print("=" * 60)

def simulate_merge_sort():
    print("\n[ Simulasi Merge Sort - Pengurutan Pemindahan Data ]")
    try:
        n = int(input("Masukkan jumlah antrean file (contoh: 5): "))
    except ValueError:
        print("Input tidak valid!")
        return

    # Generate random files
    files = [{"nama": f"File_Data_{i+1}.bin", "size_kb": random.randint(100, 9999)} for i in range(n)]
    
    print("\nData Sebelum Diurutkan (Berdasarkan Ukuran KB):")
    for f in files:
        print(f" - {f['nama']} : {f['size_kb']} KB")
        
    print("\nSedang mengurutkan data (Merge Sort Recursive)...")
    start_time = time.perf_counter()
    sorted_files = recursive_merge_sort(files)
    end_time = time.perf_counter()
    
    print("\nData Setelah Diurutkan:")
    for f in sorted_files:
        print(f" - {f['nama']} : {f['size_kb']} KB")
        
    print(f"\nWaktu Eksekusi Algoritma: {(end_time - start_time):.6f} detik\n")


def simulate_round_robin():
    print("\n[ Simulasi Round Robin - Penjadwalan Proses ]")
    try:
        n = int(input("Masukkan jumlah proses (contoh: 3): "))
        q = int(input("Masukkan batas waktu Quantum (contoh: 4): "))
    except ValueError:
        print("Input tidak valid!")
        return

    # Generate random processes
    queue = [{"name": f"Proses_{i+1}", "burst": random.randint(5, 20)} for i in range(n)]
    
    print("\nAntrean Proses Awal:")
    for p in queue:
        print(f" - {p['name']} : {p['burst']} detik")
        
    print(f"\nMulai Simulasi dengan Quantum = {q}...\n")
    
    def log_step(name, burst, run_time, new_burst, new_time):
        print(f"[Waktu {new_time-run_time:03d} -> {new_time:03d}] {name} diproses selama {run_time}s | Sisa Waktu: {new_burst}s")

    start_time = time.perf_counter()
    total_time = recursive_round_robin(queue, q, log_callback=log_step)
    end_time = time.perf_counter()
    
    print(f"\nSemua proses selesai! Total waktu sistem: {total_time} detik.")
    print(f"Waktu Eksekusi Algoritma: {(end_time - start_time):.6f} detik\n")

def run_streamlit():
    print("\nMembuka Visualisasi Web (Streamlit)...")
    try:
        subprocess.Popen(["streamlit", "run", "app.py"], shell=True)
        print("Streamlit berjalan di background. Silakan cek browser Anda.\n")
    except Exception as e:
        print(f"Gagal menjalankan Streamlit: {e}\n")


def main():
    while True:
        print_header()
        print("Pilih Menu:")
        print("1. Simulasi Pengurutan Data (Merge Sort)")
        print("2. Simulasi Penjadwalan Proses (Round Robin)")
        print("3. Buka Web Visualisasi Interaktif")
        print("4. Keluar Program")
        
        pilihan = input("Masukkan pilihan (1-4): ")
        
        if pilihan == '1':
            simulate_merge_sort()
            input("Tekan Enter untuk kembali ke menu...")
        elif pilihan == '2':
            simulate_round_robin()
            input("Tekan Enter untuk kembali ke menu...")
        elif pilihan == '3':
            run_streamlit()
        elif pilihan == '4':
            print("Terima kasih. Program dihentikan.")
            sys.exit(0)
        else:
            print("Pilihan tidak valid!\n")

if __name__ == "__main__":
    main()
