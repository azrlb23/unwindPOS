def get_mergesort_steps(arr_input):
    """
    Menghasilkan jejak langkah (trace) dari algoritma Merge Sort rekursif.
    Setiap step berisi kondisi array saat ini, indeks yang sedang diproses, dan pesan deskriptif.
    """
    steps = []
    arr = list(arr_input)
    
    def _ms(start, end, depth):
        if end - start <= 1:
            steps.append({
                "action": "base",
                "arr": list(arr),
                "bounds": [start, end],
                "depth": depth,
                "msg": f"Base Case: Array pada indeks {start} hanya memiliki 1 elemen ({arr[start]}). Tidak perlu dipecah lagi karena 1 elemen pasti terurut."
            })
            return
            
        mid = (start + end) // 2
        
        steps.append({
            "action": "divide",
            "arr": list(arr),
            "bounds": [start, end],
            "mid": mid,
            "depth": depth,
            "msg": f"Fase Divide: Memecah kelompok array (indeks {start} s.d. {end-1}) menjadi bagian Kiri ({start} s.d. {mid-1}) dan Kanan ({mid} s.d. {end-1})."
        })
        
        _ms(start, mid, depth + 1)
        _ms(mid, end, depth + 1)
        
        _merge(start, mid, end, depth)
        
    def _merge(start, mid, end, depth):
        left = arr[start:mid]
        right = arr[mid:end]
        merged = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            steps.append({
                "action": "compare",
                "arr": list(arr),
                "bounds": [start, end],
                "compare_indices": [start + i, mid + j],
                "depth": depth,
                "msg": f"Fase Conquer (Bandingkan): Apakah {left[i]} (Kiri) lebih kecil atau sama dengan {right[j]} (Kanan)? Pilih yang terkecil."
            })
            if left[i] <= right[j]:
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
            
        # Update original array
        arr[start:end] = merged
        
        steps.append({
            "action": "merge_done",
            "arr": list(arr),
            "bounds": [start, end],
            "depth": depth,
            "msg": f"Fase Conquer (Selesai): Sub-array indeks {start} hingga {end-1} berhasil digabungkan secara terurut menjadi {arr[start:end]}."
        })

    steps.append({
        "action": "init",
        "arr": list(arr),
        "bounds": [0, len(arr)],
        "depth": 0,
        "msg": f"Mulai Simulasi Merge Sort untuk array berukuran {len(arr)} elemen. Algoritma akan mencari Base Case terlebih dahulu."
    })
    
    _ms(0, len(arr), 1)
    
    steps.append({
        "action": "done",
        "arr": list(arr),
        "bounds": [0, len(arr)],
        "depth": 0,
        "msg": "Proses Selesai! Seluruh pecahan array telah berhasil digabungkan kembali dalam kondisi terurut sempurna."
    })
    return steps


def get_roundrobin_steps(processes, quantum):
    """
    Menghasilkan jejak langkah (trace) dari algoritma Round Robin rekursif.
    Setiap step berisi kondisi antrean (queue), proses yang sedang di-CPU, dan pesan.
    """
    steps = []
    queue = [[p[0], p[1]] for p in processes]
    current_time = 0
    
    steps.append({
        "action": "init",
        "queue": [list(p) for p in queue],
        "active": None,
        "time": current_time,
        "msg": f"Mulai Simulasi Round Robin. Terdapat {len(queue)} proses awal dalam antrean dengan batas waktu (Quantum) = {quantum} detik."
    })
    
    def _rr(q, curr_time):
        if not q:
            steps.append({
                "action": "done",
                "queue": [],
                "active": None,
                "time": curr_time,
                "msg": "Base Case Tercapai: Antrean sudah kosong. Semua proses telah berhasil dilayani oleh CPU."
            })
            return curr_time
            
        name, burst = q[0]
        remaining = q[1:]
        
        steps.append({
            "action": "pop",
            "queue": [list(p) for p in remaining],
            "active": [name, burst],
            "time": curr_time,
            "msg": f"CPU mengambil {name} dari antrean terdepan. {name} membutuhkan total {burst} detik untuk diselesaikan."
        })
        
        run_time = min(burst, quantum)
        new_burst = burst - run_time
        curr_time += run_time
        
        if new_burst > 0:
            remaining.append([name, new_burst])
            steps.append({
                "action": "requeue",
                "queue": [list(p) for p in remaining],
                "active": None,
                "time": curr_time,
                "msg": f"Interupsi (Preemptive)! Jatah {run_time}s untuk {name} habis. {name} dipaksa keluar dari CPU dan masuk ke belakang antrean dengan sisa {new_burst}s."
            })
        else:
            steps.append({
                "action": "finish",
                "queue": [list(p) for p in remaining],
                "active": None,
                "time": curr_time,
                "msg": f"Selesai! {name} menghabiskan {run_time}s dan berhasil menyelesaikan seluruh tugasnya tanpa melebihi batas kuantum."
            })
            
        return _rr(remaining, curr_time)

    _rr(queue, current_time)
    return steps
