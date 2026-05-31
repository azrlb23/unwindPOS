# unwindPOS — Sistem Visualisasi & Analisis Rekursi Kasir Modern

Proyek **unwindPOS** adalah aplikasi simulasi kasir belanja interaktif sekaligus sarana edukasi visualisasi kompleksitas waktu dan memori (Call Stack) algoritma rekursif murni. unwindPOS dirancang sesuai dengan spesifikasi tugas besar mata kuliah **Perancangan dan Analisis Algoritma**, Program Studi Informatika, Institut Teknologi Kalimantan.

## Fitur Utama
1. **Pembangkitan Data Proses (KF-01):** Membangkitkan N nama proses dan waktu eksekusi acak secara konsisten dan dapat direproduksi menggunakan *seed* bernilai `42`.
2. **Komputasi Rekursif (KF-02):** Menjumlahkan total waktu eksekusi secara rekursif murni dengan modifikasi limit tumpukan rekursi Python.
3. **Pengukuran Waktu Eksekusi (KF-03 & KF-04):** Mengukur waktu eksekusi rata-rata dari 5 kali pengulangan untuk 8 variasi ukuran dataset (dari 1.000 hingga 1.000.000 proses).
4. **Pelaporan & Visualisasi (KF-05 & KF-06):** Menyajikan hasil pengujian di terminal secara real-time dan menghasilkan grafik garis hubungan antara ukuran dataset dengan waktu eksekusi.

---

## Struktur Proyek
```text
PAA/
├── src/
│   ├── __init__.py
│   ├── config.py       # Parameter global (SEED, REPEAT, TEST_SIZES, dsb.)
│   ├── generator.py    # Fungsi pembangkit dataset proses acak
│   ├── analyzer.py     # Algoritma rekursif utama
│   ├── benchmark.py    # Logika pengukur waktu kinerja program
│   └── visualizer.py   # Logika pembuatan grafik menggunakan Seaborn & Matplotlib
├── main.py             # Entry point utama program
├── requirements.txt    # Daftar dependensi eksternal Python
├── SRS.md              # Spesifikasi Kebutuhan Perangkat Lunak
└── README.md           # Dokumentasi ini
```

---

## Persyaratan Sistem
- Python 3.8 atau lebih baru
- Memori RAM minimal 4 GB (direkomendasikan untuk pengujian ukuran 1.000.000 proses)

---

## Cara Instalasi & Menjalankan

### 1. Kloning / Buka Direktori Proyek
Buka terminal Anda di direktori proyek `PAA`.

### 2. Membuat & Mengaktifkan Virtual Environment (Opsional tetapi Direkomendasikan)
Di Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Di macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Memasang Dependensi
Pasang pustaka eksternal yang dibutuhkan menggunakan perintah berikut:
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Program
Jalankan program utama melalui perintah:
```bash
python main.py
```
Setelah program selesai mengeksekusi semua variasi ukuran dataset, grafik garis hasil analisis akan muncul di jendela baru dan tersimpan otomatis dengan nama `performance_chart.png` di direktori utama.
