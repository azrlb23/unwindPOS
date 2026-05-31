# unwindPOS

**Sistem Visualisasi Interaktif & Analisis Kompleksitas Algoritma Rekursif Kasir Modern**

> Proyek tugas besar mata kuliah **Perancangan dan Analisis Algoritma (PAA)**, Program Studi Informatika, Institut Teknologi Kalimantan, Balikpapan — 2026.

---

## Deskripsi

**unwindPOS** adalah aplikasi edukasi yang mendemonstrasikan dan menganalisis perilaku algoritma rekursif murni melalui simulasi kasir belanja interaktif. Nama *unwindPOS* merepresentasikan proses *unwinding* (pelepasan) tumpukan memori (*Call Stack*) yang terjadi saat fungsi rekursif mulai mengembalikan nilai akumulatif dari kedalaman terdalam hingga ke pemanggil awal — sebuah konsep kunci dalam analisis algoritma.

Proyek ini terdiri dari **dua mode operasi**:

| Mode | Entry Point | Deskripsi |
|---|---|---|
| **CLI Analyzer** | `main.py` | Pengujian benchmark otomatis di terminal untuk 8 variasi dataset (1.000 — 1.000.000 proses) dengan visualisasi grafik Matplotlib. |
| **Dashboard Interaktif** | `app.py` | Aplikasi web Streamlit dengan simulasi kasir, animasi rekursi step-by-step, benchmark real-time, dan penjelasan edukatif. |

---

## Fitur Utama

### Tab 1 — Simulasi Kasir Interaktif
- **Katalog Produk Glassmorphic:** 15 produk minimarket lengkap dengan penambahan kuantitas via tombol `+` / `-`.
- **Visualisasi Animasi Rekursi:** Animasi step-by-step yang memperlihatkan fase *winding* (turun) dan *unwinding* (naik) dari Call Stack secara real-time.
- **Pengendali Media Interaktif:** Tombol Play/Pause, Step Forward, Step Backward, pengaturan kecepatan (0.5x / 1.0x / 2.0x), Skip, dan Replay.
- **Struk Belanja Digital:** Hasil akhir total pembayaran ditampilkan dalam format struk kasir thermal dengan detail per-item.
- **Grafik Analisis Otomatis:** Pie Chart distribusi kategori, Bar Chart alokasi stack, dan Waterfall Chart kontribusi unwinding dihasilkan secara otomatis setelah kalkulasi selesai.

### Tab 2 — Benchmark Performa
- **Pengaturan Fleksibel:** Multiselect ukuran dataset N (100 — 100.000) dan slider jumlah pengulangan per N.
- **Kurva Penskalaan Waktu:** Grafik garis Plotly membandingkan waktu eksekusi aktual vs estimasi linear teoritis O(n).
- **Efisiensi per Item:** Grafik kedua menampilkan biaya waktu per item dalam mikrosekon (µs), membuktikan efisiensi konstan O(1) per elemen.
- **Metrik Dashboard:** Kartu glassmorphic menampilkan Waktu Tercepat, Waktu Terlambat, dan Indeks Skala O(n) secara real-time.

### Tab 3 — Cara Kerja Algoritma
- **Kartu Metrik Kompleksitas:** Menampilkan Kompleksitas Waktu O(n), Kompleksitas Ruang O(n), dan logika Base Case.
- **Kode Sumber Beranotasi:** Implementasi fungsi rekursif Python yang dikomentari secara detail.
- **Jejak Call Stack Visual:** Representasi visual fase Winding (indigo) dan Unwinding (hijau) dalam format struk thermal.
- **Tabel Pemetaan Konseptual:** Membandingkan entitas simulasi kasir dengan variabel proyek PAA (main.py).

---

## Struktur Proyek

```text
unwindPOS/
├── .streamlit/
│   └── config.toml         # Konfigurasi tema Streamlit (warna, font)
├── src/
│   ├── __init__.py          # Penanda paket Python
│   ├── config.py            # Parameter global (SEED, REPEAT, TEST_SIZES)
│   ├── generator.py         # Fungsi pembangkit dataset proses acak
│   ├── analyzer.py          # Algoritma rekursif utama (main.py)
│   ├── benchmark.py         # Logika pengukur waktu kinerja program
│   ├── visualizer.py        # Pembuatan grafik Matplotlib & Seaborn (CLI)
│   └── kasir.py             # Katalog produk, rekursi kasir, generator animasi
├── app.py                   # Dashboard Streamlit (entry point web)
├── main.py                  # Entry point CLI analyzer
├── style.css                # Desain UI glassmorphism kustom
├── requirements.txt         # Daftar dependensi Python
├── SRS.md                   # Spesifikasi Kebutuhan Perangkat Lunak
├── performance_chart.png    # Hasil grafik output CLI
├── .gitignore               # Konfigurasi Git ignore
└── README.md                # Dokumentasi ini
```

---

## Persyaratan Sistem

| Komponen | Spesifikasi Minimum |
|---|---|
| Python | 3.8 atau lebih baru |
| RAM | 4 GB (direkomendasikan untuk dataset besar) |
| Penyimpanan | 500 MB ruang kosong |
| Browser | Chrome, Edge, atau Firefox terbaru (untuk mode dashboard) |

---

## Instalasi & Menjalankan

### 1. Kloning Repositori

```bash
git clone https://github.com/azrlb23/unwindPOS.git
cd unwindPOS
```

### 2. Membuat Virtual Environment (Opsional)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Memasang Dependensi

```bash
pip install -r requirements.txt
```

### 4. Menjalankan Program

**Mode CLI Analyzer:**
```bash
python main.py
```
Setelah selesai, grafik hasil analisis akan muncul di jendela Matplotlib dan tersimpan otomatis sebagai `performance_chart.png`.

**Mode Dashboard Interaktif:**
```bash
streamlit run app.py
```
Aplikasi akan terbuka secara otomatis di browser pada alamat `http://localhost:8501`.

---

## Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| **Python 3.x** | Bahasa pemrograman utama |
| **Streamlit** | Framework dashboard web interaktif |
| **Plotly** | Grafik interaktif pada dashboard |
| **Matplotlib & Seaborn** | Visualisasi grafik pada mode CLI |
| **Pandas** | Pengelolaan struktur data tabel |
| **CSS Glassmorphism** | Desain UI modern dengan efek kaca buram transparan |

---

## Konsep Algoritma

### Fungsi Rekursif

```python
def recursive_total_harga(items, index=0):
    if index == len(items):   # Base Case
        return 0
    return items[index]["harga"] + recursive_total_harga(items, index + 1)
```

### Analisis Kompleksitas

| Aspek | Notasi | Penjelasan |
|---|---|---|
| Waktu | O(n) | Setiap item dikunjungi tepat 1 kali |
| Ruang | O(n) | 1 stack frame dialokasikan per item |
| Base Case | `index == len(items)` | Mengembalikan 0 saat antrean habis |
| Recurrence | `T(n) = T(n-1) + O(1)` | Relasi rekurensi linear |

---

## Lisensi

Proyek ini dikembangkan untuk keperluan akademis tugas besar mata kuliah **Perancangan dan Analisis Algoritma**, Program Studi Informatika, Institut Teknologi Kalimantan.

---

*Dibuat dengan rekursi dan semangat oleh Kelompok PAA ITK 2026.*
