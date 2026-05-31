"""
Modul Kasir (src/kasir.py)
Menyediakan katalog produk, logika rekursif khusus kasir,
dan generator langkah-langkah animasi untuk visualisasi Streamlit.
"""

# ─── Katalog Produk ────────────────────────────────────────────────────────────
KATALOG: list[dict] = [
    {"id":  1, "nama": "Indomie Goreng",    "harga":  3500, "emoji": "🍜", "kategori": "Makanan"},
    {"id":  2, "nama": "Aqua 600ml",        "harga":  4000, "emoji": "💧", "kategori": "Minuman"},
    {"id":  3, "nama": "Roti Tawar",        "harga": 12000, "emoji": "🍞", "kategori": "Makanan"},
    {"id":  4, "nama": "Telur 1 Butir",     "harga":  2500, "emoji": "🥚", "kategori": "Sembako"},
    {"id":  5, "nama": "Susu UHT 200ml",    "harga":  8500, "emoji": "🥛", "kategori": "Minuman"},
    {"id":  6, "nama": "Minyak Goreng 1L",  "harga": 19000, "emoji": "🫙", "kategori": "Sembako"},
    {"id":  7, "nama": "Beras 1kg",         "harga": 14000, "emoji": "🌾", "kategori": "Sembako"},
    {"id":  8, "nama": "Gula Pasir 1kg",    "harga": 16000, "emoji": "🍬", "kategori": "Sembako"},
    {"id":  9, "nama": "Kopi Sachet",       "harga":  2000, "emoji": "☕", "kategori": "Minuman"},
    {"id": 10, "nama": "Teh Celup",         "harga":  5000, "emoji": "🍵", "kategori": "Minuman"},
    {"id": 11, "nama": "Sabun Mandi",       "harga":  6500, "emoji": "🧼", "kategori": "Kebersihan"},
    {"id": 12, "nama": "Sampo Sachet",      "harga":  1500, "emoji": "🧴", "kategori": "Kebersihan"},
    {"id": 13, "nama": "Biskuit Roma",      "harga":  7000, "emoji": "🍪", "kategori": "Makanan"},
    {"id": 14, "nama": "Kerupuk 1 Pak",     "harga":  5000, "emoji": "🥨", "kategori": "Makanan"},
    {"id": 15, "nama": "Sirup ABC 525ml",   "harga": 22000, "emoji": "🍹", "kategori": "Minuman"},
]

# ID → produk lookup
_ID_MAP: dict[int, dict] = {p["id"]: p for p in KATALOG}


def get_product(product_id: int) -> dict | None:
    """Kembalikan data produk berdasarkan ID, atau None jika tidak ada."""
    return _ID_MAP.get(product_id)


# ─── Konversi Keranjang ────────────────────────────────────────────────────────
def keranjang_ke_items(keranjang: dict[int, int]) -> list[tuple[str, int]]:
    """
    Konversi keranjang {product_id: qty} ke list (nama, harga) per unit.
    Contoh: {1: 3} → [("Indomie Goreng", 3500), ("Indomie Goreng", 3500), ("Indomie Goreng", 3500)]
    """
    result: list[tuple[str, int]] = []
    for pid, qty in keranjang.items():
        prod = _ID_MAP.get(pid)
        if prod and qty > 0:
            for _ in range(qty):
                result.append((prod["nama"], prod["harga"]))
    return result


# ─── Fungsi Rekursif Kasir ─────────────────────────────────────────────────────
def recursive_total_harga(items: list[tuple[str, int]], index: int = 0) -> int:
    """
    Hitung total harga seluruh item secara rekursif murni.
    Kondisi dasar : index == len(items) → kembalikan 0.
    Rekursi       : harga[index] + recursive_total_harga(items, index + 1).
    Kompleksitas  : O(n) waktu, O(n) ruang (stack).
    """
    if index == len(items):
        return 0
    return items[index][1] + recursive_total_harga(items, index + 1)


# ─── Generator Langkah Animasi ─────────────────────────────────────────────────
def get_rekursi_steps(items: list[tuple[str, int]]) -> list[dict]:
    """
    Kembalikan setiap langkah rekursi untuk animasi step-by-step.

    Setiap langkah berisi:
        fase        : 'turun' | 'dasar' | 'naik'
        index       : indeks saat ini dalam list items
        nama        : nama item
        harga       : harga item
        depth       : kedalaman tumpukan (0-based)
        akumulasi   : total yang dikembalikan (None saat fase turun)
        deskripsi   : teks penjelasan langkah
    """
    steps: list[dict] = []
    n = len(items)

    # ── Fase turun (panggil rekursi lebih dalam) ──────────────────────────────
    for i in range(n):
        steps.append({
            "fase": "turun",
            "index": i,
            "nama": items[i][0],
            "harga": items[i][1],
            "depth": i,
            "akumulasi": None,
            "deskripsi": (
                f"recursive_total_harga(items, {i})\n"
                f"  → ambil harga[{i}] = Rp{items[i][1]:,}  |  panggil index {i+1}"
            ),
        })

    # ── Kondisi dasar ─────────────────────────────────────────────────────────
    steps.append({
        "fase": "dasar",
        "index": n,
        "nama": "— Kondisi Dasar —",
        "harga": 0,
        "depth": n,
        "akumulasi": 0,
        "deskripsi": (
            f"recursive_total_harga(items, {n})\n"
            f"  → index {n} == len(items) {n}  →  return 0"
        ),
    })

    # ── Fase naik (kembalikan nilai ke pemanggil) ─────────────────────────────
    running = 0
    for i in range(n - 1, -1, -1):
        prev = running
        running += items[i][1]
        steps.append({
            "fase": "naik",
            "index": i,
            "nama": items[i][0],
            "harga": items[i][1],
            "depth": i,
            "akumulasi": running,
            "deskripsi": (
                f"recursive_total_harga(items, {i})  kembali\n"
                f"  → Rp{items[i][1]:,} + Rp{prev:,} = Rp{running:,}"
            ),
        })

    return steps
