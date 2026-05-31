"""
Modul Pembangkit Data Proses
Mengimplementasikan KF-01 untuk membangkitkan data proses acak yang reproduksibel.
"""

import random
from src.config import SEED


def generate_processes(n: int) -> list[tuple[str, int]]:
    """
    Membangkitkan N proses acak dengan nama 'P{id}' dan waktu eksekusi 1-10.
    Jika n <= 0, mengembalikan list kosong.
    """
    if n <= 0:
        return []

    # Mengatur seed acak agar hasil tetap konsisten dan dapat direproduksi
    random.seed(SEED)

    # Menggunakan list comprehension agar efisien dan singkat
    return [(f"P{i + 1}", random.randint(1, 10)) for i in range(n)]
