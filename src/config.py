"""
Modul Konfigurasi
Menyimpan parameter konfigurasi global untuk sistem analisis kompleksitas.
"""

# Nilai awal pembangkit bilangan acak (seed) untuk menjamin reproduksibilitas
SEED = 42

# Jumlah pengulangan untuk setiap ukuran dataset dalam pengujian
REPEAT = 5

# Batas maksimum kedalaman tumpukan rekursi Python (dilebihkan dari 1.000.000 untuk menampung frame internal Python)
RECURSION_LIMIT = 1010000


# Daftar ukuran dataset (jumlah proses) yang akan diuji
TEST_SIZES = [
    1000,
    5000,
    10000,
    50000,
    100000,
    200000,
    500000,
    1000000
]
