"""
Modul Visualisasi Kinerja
Mengimplementasikan KF-06 untuk menggambar grafik hubungan N dengan waktu eksekusi.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_performance(results: list[dict], output_path: str = "performance_chart.png"):
    """
    Membuat grafik garis kinerja hubungan N vs Waktu Eksekusi (KF-06).
    Fungsi ringkas (di bawah 20 baris) sesuai KNF-03.
    """
    df = pd.DataFrame(results)
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # Grafik garis dengan penanda titik (marker="o")
    sns.lineplot(
        data=df, x="Jumlah Proses", y="Rata-rata Waktu Eksekusi",
        marker="o", linewidth=2, markersize=8
    )
    plt.title("Hubungan Jumlah Proses dengan Waktu Eksekusi (Recursive Function)", fontsize=14, pad=15)
    plt.xlabel("Jumlah Proses (N)", fontsize=12)
    plt.ylabel("Rata-rata Waktu Eksekusi (detik)", fontsize=12)
    # Format label sumbu X dengan titik pemisah ribuan agar lebih rapi dan terbaca
    labels = [f"{x:,}".replace(",", ".") for x in df["Jumlah Proses"]]
    plt.xticks(df["Jumlah Proses"], labels=labels, rotation=45)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"\nGrafik kinerja berhasil disimpan ke: {output_path}")
    try:
        plt.show()
    except Exception as e:
        print(f"Peringatan: Tidak dapat menampilkan jendela GUI grafik ({e}).")
