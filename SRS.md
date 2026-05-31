# Spesifikasi Kebutuhan Perangkat Lunak (SRS)

**Judul Sistem:** Sistem Analisis Kompleksitas Algoritma Rekursif untuk Optimasi Pemindahan Data dan Penjadwalan Proses
**Versi Dokumen:** 1.0
**Tanggal:** 30 Mei 2026
**Program Studi:** Informatika — Institut Teknologi Kalimantan
**Mata Kuliah:** Perancangan dan Analisis Algoritma

---

## Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
2. [Deskripsi Umum Sistem](#2-deskripsi-umum-sistem)
3. [Kebutuhan Fungsional](#3-kebutuhan-fungsional)
4. [Kebutuhan Non-Fungsional](#4-kebutuhan-non-fungsional)
5. [Deskripsi Antarmuka](#5-deskripsi-antarmuka)
6. [Deskripsi Data](#6-deskripsi-data)
7. [Batasan Sistem](#7-batasan-sistem)
8. [Asumsi dan Ketergantungan](#8-asumsi-dan-ketergantungan)
9. [Diagram Alur Sistem](#9-diagram-alur-sistem)
10. [Matriks Keterlacakan Kebutuhan](#10-matriks-keterlacakan-kebutuhan)

---

## 1. Pendahuluan

### 1.1 Tujuan Dokumen

Dokumen ini merupakan Spesifikasi Kebutuhan Perangkat Lunak (SRS) untuk sistem analisis kompleksitas algoritma rekursif yang dikembangkan sebagai tugas besar mata kuliah Perancangan dan Analisis Algoritma. Dokumen ini menjelaskan seluruh kebutuhan fungsional dan non-fungsional sistem secara terstruktur dan lengkap sebagai acuan pengembangan dan pengujian.

### 1.2 Ruang Lingkup Sistem

Sistem ini adalah program berbasis Python yang dirancang untuk:

- Membangkitkan dataset proses secara otomatis dalam berbagai ukuran
- Menghitung akumulasi total waktu eksekusi seluruh proses menggunakan algoritma rekursif
- Mengukur dan mencatat waktu eksekusi nyata dari algoritma tersebut
- Menghasilkan laporan statistik dan visualisasi grafik kinerja algoritma

Sistem ini bukan merupakan sistem penjadwalan proses secara nyata, melainkan simulasi dan analisis kinerja algoritma rekursif dalam konteks penjadwalan dan pemindahan data.

### 1.3 Definisi, Akronim, dan Singkatan

| Istilah | Penjelasan |
|---|---|
| SRS | Spesifikasi Kebutuhan Perangkat Lunak |
| Rekursi | Teknik pemrograman di mana sebuah fungsi memanggil dirinya sendiri |
| Kondisi Dasar | Kondisi penghenti dalam fungsi rekursif sehingga tidak terjadi pengulangan tak terbatas |
| Tumpukan Pemanggilan | Mekanisme penyimpanan sementara dalam memori untuk setiap lapisan pemanggilan fungsi rekursif |
| Kompleksitas Waktu | Ukuran pertumbuhan waktu eksekusi algoritma terhadap ukuran masukan |
| Kompleksitas Ruang | Ukuran pertumbuhan penggunaan memori algoritma terhadap ukuran masukan |
| N | Jumlah proses yang menjadi masukan algoritma |
| O(n) | Notasi Big-O yang menyatakan kompleksitas linear |

### 1.4 Referensi

- Kumar, Shailesh. (2021). CR-Sparse: Hardware accelerated functional algorithms for sparse signal processing in Python using JAX. *Journal of Open Source Software*, 6(68), 3917.
- Smirnov, V., et al. (2021). Recursive MAGUS: Scalable and accurate multiple sequence alignment. *PLoS Computational Biology*, 17(10).
- Zaidi, et al. (2021). Reliability and consistency in benchmarking of computational systems.
- Dokumentasi resmi Python 3.x: https://docs.python.org

---

## 2. Deskripsi Umum Sistem

### 2.1 Perspektif Sistem

Sistem ini berdiri sendiri sebagai skrip Python yang dijalankan secara lokal. Sistem tidak memerlukan koneksi jaringan, basis data eksternal, atau antarmuka pengguna grafis. Seluruh interaksi terjadi melalui keluaran di terminal dan tampilan grafik yang dihasilkan oleh pustaka Matplotlib.

```
+--------------------+
|   Pengguna (CLI)   |
+--------------------+
          |
          | menjalankan skrip
          v
+--------------------+       +------------------------+
| Pembangkit Data    | ----> | Fungsi Rekursif Utama  |
| generate_processes |       | recursive_total_time   |
+--------------------+       +------------------------+
                                        |
                                        v
                             +------------------------+
                             | Pengukur Waktu         |
                             | time.perf_counter()    |
                             +------------------------+
                                        |
                                        v
                             +------------------------+
                             | Penyimpan Hasil        |
                             | pandas DataFrame       |
                             +------------------------+
                                        |
                                        v
                             +------------------------+
                             | Visualisasi Grafik     |
                             | Matplotlib + Seaborn   |
                             +------------------------+
```

### 2.2 Fungsi Utama Sistem

Sistem memiliki empat fungsi utama:

1. **Pembangkitan Data** — Membuat daftar proses secara otomatis dengan nama dan waktu eksekusi acak
2. **Komputasi Rekursif** — Menjumlahkan seluruh waktu eksekusi menggunakan fungsi rekursif murni
3. **Pengukuran Kinerja** — Mencatat waktu eksekusi nyata untuk setiap skenario pengujian
4. **Pelaporan dan Visualisasi** — Menyajikan hasil dalam bentuk tabel statistik dan grafik garis

### 2.3 Karakteristik Pengguna

| Jenis Pengguna | Deskripsi | Tingkat Keahlian |
|---|---|---|
| Mahasiswa | Pengguna utama yang menjalankan dan menganalisis hasil sistem | Menengah (paham Python dasar) |
| Dosen | Penilai yang membaca laporan dan hasil visualisasi | Tinggi (paham algoritma dan analisis kompleksitas) |

### 2.4 Batasan Umum

- Sistem ditulis dalam Python 3.x
- Sistem hanya berjalan pada lingkungan dengan Python dan pustaka yang diperlukan terpasang
- Rekursi murni digunakan tanpa konversi ke perulangan iteratif
- Batas kedalaman tumpukan dinaikkan secara manual menggunakan `sys.setrecursionlimit`

---

## 3. Kebutuhan Fungsional

### KF-01 — Pembangkitan Data Proses

**Deskripsi:** Sistem harus mampu membangkitkan daftar proses secara otomatis berdasarkan jumlah yang diminta.

**Masukan:** Bilangan bulat positif N yang menyatakan jumlah proses yang ingin dibangkitkan.

**Proses:**
1. Sistem membuat daftar kosong
2. Untuk setiap indeks dari 0 hingga N-1, sistem membuat nama proses dengan format `P{indeks+1}`
3. Sistem membangkitkan waktu eksekusi acak berupa bilangan bulat antara 1 hingga 10
4. Setiap pasangan nama dan waktu eksekusi disimpan sebagai elemen dalam daftar

**Keluaran:** Daftar berisi N pasangan data berformat `(nama_proses, waktu_eksekusi)`

**Kondisi Khusus:**
- Nilai awal pembangkit bilangan acak ditetapkan pada angka 42 untuk menjamin hasil yang dapat direproduksi
- Jika N bernilai 0, fungsi mengembalikan daftar kosong

---

### KF-02 — Komputasi Total Waktu Secara Rekursif

**Deskripsi:** Sistem harus mampu menghitung total waktu eksekusi dari seluruh proses dalam daftar menggunakan algoritma rekursif murni.

**Masukan:** Daftar proses hasil KF-01 dan nilai indeks awal (secara bawaan bernilai 0).

**Proses:**
1. Sistem memeriksa apakah indeks saat ini sudah sama dengan panjang daftar
2. Jika ya, sistem mengembalikan nilai 0 sebagai kondisi dasar
3. Jika tidak, sistem mengambil waktu eksekusi pada posisi indeks saat ini
4. Sistem memanggil dirinya sendiri dengan indeks yang bertambah satu
5. Sistem mengembalikan penjumlahan waktu saat ini dengan hasil pemanggilan rekursif

**Keluaran:** Satu nilai bilangan bulat yang merupakan total waktu eksekusi seluruh proses

**Kondisi Khusus:**
- Kedalaman rekursi maksimum sama dengan N
- Untuk N di atas 1.000, diperlukan penyesuaian batas kedalaman tumpukan

---

### KF-03 — Pengukuran Waktu Eksekusi

**Deskripsi:** Sistem harus mampu mengukur waktu nyata yang dibutuhkan fungsi rekursif untuk menyelesaikan komputasi pada setiap ukuran dataset.

**Masukan:** Daftar proses dan jumlah pengulangan pengujian (REPEAT = 5).

**Proses:**
1. Sistem mencatat waktu mulai menggunakan `time.perf_counter()`
2. Sistem menjalankan fungsi rekursif utama
3. Sistem mencatat waktu selesai menggunakan `time.perf_counter()`
4. Sistem menghitung selisih waktu selesai dan waktu mulai
5. Proses diulang sebanyak REPEAT kali
6. Sistem menghitung rata-rata dari seluruh pengulangan

**Keluaran:** Nilai rata-rata waktu eksekusi dalam satuan detik dengan presisi enam angka desimal

---

### KF-04 — Pengujian Multi-Ukuran Dataset

**Deskripsi:** Sistem harus menjalankan pengujian secara otomatis untuk delapan variasi ukuran dataset yang telah ditetapkan.

**Ukuran Dataset yang Diuji:**

| No | Jumlah Proses |
|---|---|
| 1 | 1.000 |
| 2 | 5.000 |
| 3 | 10.000 |
| 4 | 50.000 |
| 5 | 100.000 |
| 6 | 200.000 |
| 7 | 500.000 |
| 8 | 1.000.000 |

**Proses:** Untuk setiap ukuran, sistem menjalankan KF-01, KF-02, dan KF-03 secara berurutan, lalu menyimpan hasilnya ke dalam struktur data tabel.

---

### KF-05 — Pelaporan Statistik

**Deskripsi:** Sistem harus mencetak ringkasan hasil pengujian ke terminal untuk setiap ukuran dataset yang telah diuji.

**Keluaran Terminal:**
```
Jumlah Proses : [N]
Rata-rata Waktu : [X.XXXXXX] detik
```

---

### KF-06 — Visualisasi Grafik Kinerja

**Deskripsi:** Sistem harus menghasilkan grafik garis yang menampilkan hubungan antara jumlah proses dan rata-rata waktu eksekusi.

**Spesifikasi Grafik:**

| Elemen | Keterangan |
|---|---|
| Jenis grafik | Grafik garis dengan penanda titik |
| Sumbu X | Jumlah proses (N) dengan skala linear |
| Sumbu Y | Rata-rata waktu eksekusi dalam detik dengan skala linear |
| Judul | Hubungan Jumlah Proses dengan Waktu Eksekusi (Recursive Function) |
| Ukuran gambar | 10 x 6 inci |
| Tema | whitegrid dari pustaka Seaborn |
| Label sumbu X | Diputar 45 derajat untuk keterbacaan |

---

## 4. Kebutuhan Non-Fungsional

### KNF-01 — Kinerja

- Sistem harus mampu menyelesaikan satu siklus pengujian penuh (delapan ukuran dataset, masing-masing lima kali pengulangan) dalam waktu tidak lebih dari 30 menit pada perangkat keras standar
- Pengukuran waktu harus menggunakan `time.perf_counter()` untuk menjamin presisi tinggi

### KNF-02 — Keandalan

- Sistem harus menghasilkan hasil yang konsisten apabila dijalankan ulang dengan nilai awal pembangkit bilangan acak yang sama
- Variasi antarpengulangan pada ukuran dataset yang sama tidak boleh melebihi 15 persen dari rata-rata

### KNF-03 — Kemudahan Pemeliharaan

- Kode harus ditulis dengan nama variabel yang deskriptif dan mudah dipahami
- Setiap fungsi utama harus memiliki tanggung jawab tunggal dan tidak melebihi 20 baris kode
- Nilai konfigurasi seperti ukuran dataset dan jumlah pengulangan harus didefinisikan sebagai variabel terpisah di bagian atas program

### KNF-04 — Portabilitas

- Sistem harus dapat dijalankan pada sistem operasi Windows, macOS, dan Linux
- Sistem hanya bergantung pada pustaka yang tersedia melalui pip dan tidak memerlukan pemasangan manual di luar itu

### KNF-05 — Keterbacaan Keluaran

- Waktu eksekusi harus ditampilkan dengan enam angka desimal
- Grafik harus memiliki judul, label sumbu, dan keterangan penanda yang jelas

---

## 5. Deskripsi Antarmuka

### 5.1 Antarmuka Pengguna

Sistem tidak memiliki antarmuka pengguna grafis. Seluruh interaksi dilakukan melalui:

- **Terminal / Command Prompt** — untuk menjalankan skrip dan membaca keluaran teks
- **Jendela grafik Matplotlib** — untuk melihat grafik visualisasi yang muncul secara otomatis setelah pengujian selesai

### 5.2 Antarmuka Perangkat Keras

Tidak ada kebutuhan perangkat keras khusus. Sistem berjalan pada komputer umum dengan spesifikasi minimum:

| Komponen | Spesifikasi Minimum |
|---|---|
| Prosesor | Prosesor 64-bit, kecepatan 1.5 GHz |
| Memori RAM | 4 GB |
| Ruang penyimpanan | 500 MB ruang kosong |

### 5.3 Antarmuka Perangkat Lunak

| Perangkat Lunak | Versi Minimum | Fungsi |
|---|---|---|
| Python | 3.8 | Bahasa pemrograman utama |
| random | Bawaan Python | Pembangkitan data acak |
| time | Bawaan Python | Pengukuran waktu eksekusi |
| sys | Bawaan Python | Penyesuaian batas rekursi |
| pandas | 1.3.0 | Pengelolaan tabel hasil |
| matplotlib | 3.4.0 | Pembuatan grafik |
| seaborn | 0.11.0 | Penataan tema grafik |

---

## 6. Deskripsi Data

### 6.1 Struktur Data Masukan

**Nama:** `processes`
**Tipe:** `list` berisi `tuple`
**Format setiap elemen:** `(str, int)`

| Bidang | Tipe | Deskripsi | Batasan |
|---|---|---|---|
| `process_name` | `str` | Nama unik proses | Format `P{i+1}`, contoh: `P1`, `P2`, ..., `P1000000` |
| `execution_time` | `int` | Waktu eksekusi proses | Bilangan bulat antara 1 hingga 10 |

**Contoh:**
```python
[
  ("P1", 6),
  ("P2", 3),
  ("P3", 9),
  ...
  ("P1000000", 4)
]
```

### 6.2 Struktur Data Keluaran

**Nama:** `results`
**Tipe:** `list` berisi `dict`, kemudian diubah menjadi `pandas.DataFrame`

| Bidang | Tipe | Deskripsi |
|---|---|---|
| `Jumlah Proses` | `int` | Ukuran dataset yang diuji |
| `Rata-rata Waktu Eksekusi` | `float` | Rata-rata waktu dalam detik dari 5 pengulangan |

**Contoh Isi Tabel:**

| Jumlah Proses | Rata-rata Waktu Eksekusi |
|---|---|
| 1.000 | 0.000376 |
| 5.000 | 0.001328 |
| 10.000 | 0.003162 |
| 50.000 | 0.014323 |
| 100.000 | 0.029493 |
| 200.000 | 0.060427 |
| 500.000 | 0.180389 |
| 1.000.000 | 0.367285 |

---

## 7. Batasan Sistem

### 7.1 Batasan Rekursi Python

Python secara bawaan membatasi kedalaman rekursi pada 1.000 lapisan. Oleh karena itu, sistem secara eksplisit menaikkan batas ini menjadi 1.000.001 melalui perintah:

```python
sys.setrecursionlimit(1000001)
```

Tanpa pengaturan ini, sistem akan berhenti dengan galat `RecursionError: maximum recursion depth exceeded` ketika memproses dataset berukuran di atas 1.000 proses.

### 7.2 Batasan Memori

Setiap lapisan rekursi menyimpan satu bingkai data dalam tumpukan memori yang berisi nilai `index` dan `current_time`. Untuk N = 1.000.000, terdapat satu juta bingkai aktif secara bersamaan. Hal ini membutuhkan memori yang cukup besar dan dapat menyebabkan kegagalan pada sistem dengan RAM terbatas.

### 7.3 Batasan Paralelisme

Sistem tidak menggunakan pemrosesan paralel atau pemrosesan bersamaan. Seluruh komputasi berjalan secara berurutan pada satu inti prosesor, sehingga waktu pengujian bergantung sepenuhnya pada kecepatan satu inti tersebut.

### 7.4 Batasan Implementasi Rekursif

Sistem menggunakan rekursi murni tanpa optimasi ekor. Python tidak melakukan optimasi rekursi ekor secara bawaan, sehingga setiap pemanggilan tetap mengonsumsi ruang tumpukan baru.

---

## 8. Asumsi dan Ketergantungan

### 8.1 Asumsi

| Kode | Asumsi |
|---|---|
| A-01 | Seluruh nilai waktu eksekusi diasumsikan valid, tidak ada nilai nol atau negatif |
| A-02 | Jumlah total proses sudah diketahui sebelum fungsi rekursif dipanggil |
| A-03 | Sistem beroperasi dalam kondisi ideal dengan penggunaan CPU dan RAM oleh proses latar belakang yang minimal |
| A-04 | Nilai awal bilangan acak ditetapkan pada 42 untuk menjamin reproduksibilitas hasil |
| A-05 | Pengukuran menggunakan `time.perf_counter()` dianggap memiliki presisi yang cukup untuk tujuan analisis ini |

### 8.2 Ketergantungan

| Kode | Ketergantungan | Dampak jika Tidak Terpenuhi |
|---|---|---|
| K-01 | Python versi 3.8 atau lebih baru harus terpasang | Sistem tidak dapat dijalankan |
| K-02 | Pustaka pandas, matplotlib, dan seaborn harus terpasang | Sistem tidak dapat menghasilkan tabel dan grafik |
| K-03 | RAM yang tersedia minimal 4 GB untuk dataset berukuran 1.000.000 | Sistem dapat berhenti karena kehabisan memori |
| K-04 | Batas kedalaman rekursi harus dinaikkan sebelum fungsi rekursif dipanggil | Sistem gagal pada dataset berukuran di atas 1.000 |

---

## 9. Diagram Alur Sistem

### 9.1 Alur Utama Program

```
MULAI
  |
  v
Atur nilai awal bilangan acak (seed = 42)
Naikkan batas rekursi menjadi 1.000.001
  |
  v
Untuk setiap ukuran N dalam [1000, 5000, 10000, 50000,
                              100000, 200000, 500000, 1000000]:
  |
  +---> Bangkitkan daftar N proses (generate_processes)
  |
  +---> Ulangi sebanyak 5 kali:
  |       |
  |       +---> Catat waktu mulai
  |       +---> Jalankan recursive_total_time(processes)
  |       +---> Catat waktu selesai
  |       +---> Simpan selisih waktu
  |
  +---> Hitung rata-rata dari 5 pengulangan
  +---> Simpan (N, rata-rata waktu) ke dalam daftar hasil
  +---> Cetak ringkasan ke terminal
  |
  v
Ubah daftar hasil menjadi tabel pandas
  |
  v
Buat grafik garis dari tabel hasil
  |
  v
Tampilkan grafik
  |
SELESAI
```

### 9.2 Alur Fungsi Rekursif

```
recursive_total_time(processes, index)
  |
  v
Apakah index == len(processes)?
  |
  +-- YA  --> Kembalikan 0  (kondisi dasar)
  |
  +-- TIDAK
        |
        v
      Ambil current_time = processes[index][1]
        |
        v
      Panggil recursive_total_time(processes, index + 1)
        |
        v
      Kembalikan current_time + hasil pemanggilan rekursif
```

---

## 10. Matriks Keterlacakan Kebutuhan

Tabel berikut memetakan setiap kebutuhan fungsional ke bagian kode yang mengimplementasikannya serta ke bagian laporan yang membahasnya.

| Kode Kebutuhan | Deskripsi | Fungsi di Kode | Bagian Laporan |
|---|---|---|---|
| KF-01 | Pembangkitan data proses | `generate_processes(n)` | Bab 5.1, Bab 7 |
| KF-02 | Komputasi rekursif | `recursive_total_time(processes, index)` | Bab 6, Bab 7, Bab 9 |
| KF-03 | Pengukuran waktu eksekusi | Blok `time.perf_counter()` | Bab 5.2, Bab 7, Bab 8 |
| KF-04 | Pengujian multi-ukuran dataset | Perulangan `for size in test_sizes` | Bab 5.1, Bab 8 |
| KF-05 | Pelaporan statistik ke terminal | Blok `print()` di dalam perulangan | Bab 8 |
| KF-06 | Visualisasi grafik kinerja | Blok `sns.lineplot()` dan `plt.show()` | Bab 5.2, Bab 8 |
| KNF-01 | Kinerja pengukuran | `time.perf_counter()` | Bab 5.3 |
| KNF-02 | Keandalan hasil | `random.seed(42)` | Bab 5.3 |
| A-04 | Nilai awal bilangan acak | `random.seed(42)` | Bab 5.3 |
| K-04 | Batas kedalaman rekursi | `sys.setrecursionlimit(1000001)` | Bab 5.3, Bab 7 |

---

*Dokumen ini disusun oleh Kelompok Tugas Besar Mata Kuliah Perancangan dan Analisis Algoritma, Program Studi Informatika, Institut Teknologi Kalimantan, Balikpapan, 2026.*