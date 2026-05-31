"""
Modul Pengukur Kinerja (Benchmarking)
Mengimplementasikan KF-03 dan KF-04 untuk mengukur waktu eksekusi rata-rata.
"""

import sys
import time
from src.config import REPEAT, RECURSION_LIMIT, TEST_SIZES
from src.generator import generate_processes
from src.analyzer import recursive_total_time


def run_single_benchmark(processes: list[tuple[str, int]]) -> float:
    """
    Mengukur rata-rata waktu eksekusi dari recursive_total_time sebanyak REPEAT kali (KF-03).
    """
    total_duration = 0.0
    for _ in range(REPEAT):
        start_time = time.perf_counter()
        recursive_total_time(processes)
        end_time = time.perf_counter()
        total_duration += (end_time - start_time)

    return total_duration / REPEAT


def run_all_benchmarks(callback=None) -> list[dict]:
    """
    Menjalankan pengujian multi-ukuran dataset yang dikonfigurasi (KF-04).
    Mengatur batas rekursi sebelum eksekusi.
    """
    # Menaikkan batas rekursi agar tidak terjadi Stack Overflow
    sys.setrecursionlimit(RECURSION_LIMIT)
    results = []

    for size in TEST_SIZES:
        processes = generate_processes(size)
        avg_time = run_single_benchmark(processes)
        results.append({
            "Jumlah Proses": size,
            "Rata-rata Waktu Eksekusi": avg_time
        })
        if callback:
            callback(size, avg_time)

    return results
