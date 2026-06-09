"""
Modul Fungsi Rekursif Utama
Mengimplementasikan KF-02 untuk simulasi Pengurutan Antrian Pemindahan Data (Merge Sort)
dan Penjadwalan Proses (Round Robin).
"""

def recursive_merge_sort(data: list[dict]) -> list[dict]:
    """
    Mengurutkan daftar file berdasarkan ukuran ('size_kb') menggunakan algoritma Merge Sort rekursif murni.
    """
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = recursive_merge_sort(data[:mid])
    right = recursive_merge_sort(data[mid:])

    return _merge(left, right)

def _merge(left: list[dict], right: list[dict]) -> list[dict]:
    """
    Fungsi pembantu (helper) untuk menggabungkan dua sub-array yang sudah terurut.
    """
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i]["size_kb"] <= right[j]["size_kb"]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def recursive_round_robin(queue: list[dict], quantum: int, current_time: int = 0, log_callback=None) -> int:
    """
    Menyimulasikan penjadwalan proses Round Robin secara rekursif murni.
    """
    if not queue:
        return current_time

    # Ambil proses dari depan antrean
    process = queue[0]
    remaining_queue = queue[1:]

    name = process["name"]
    burst = process["burst"]

    run_time = min(burst, quantum)
    new_burst = burst - run_time
    new_time = current_time + run_time

    if log_callback:
        log_callback(name, burst, run_time, new_burst, new_time)

    if new_burst > 0:
        # Masukkan kembali ke belakang antrean
        remaining_queue.append({"name": name, "burst": new_burst})

    # Rekursi ke antrean berikutnya
    return recursive_round_robin(remaining_queue, quantum, new_time, log_callback)


def recursive_total_time(processes: list[tuple[str, int]], index: int = 0) -> int:
    """
    Menjumlahkan seluruh waktu eksekusi proses secara rekursif murni (Fungsi Baseline O(n)).
    """
    if index == len(processes):
        return 0
    return processes[index][1] + recursive_total_time(processes, index + 1)
