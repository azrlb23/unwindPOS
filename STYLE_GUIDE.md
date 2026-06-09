# unwindPOS — Design System & Style Guide

> Panduan lengkap untuk mereplikasi tampilan profesional glassmorphism unwindPOS ke proyek Streamlit lainnya.

---

## 1. Konfigurasi Tema Streamlit

Buat file `.streamlit/config.toml`:

```toml
[theme]
base                     = "light"
primaryColor             = "#6366f1"
backgroundColor          = "#f4f1ec"
secondaryBackgroundColor = "#ebe7e0"
textColor                = "#1a1a2e"
font                     = "sans serif"

[browser]
gatherUsageStats = false
```

---

## 2. Palet Warna

### Warna Utama (Brand)

| Token | Hex | Fungsi |
|---|---|---|
| `--indigo` | `#6366f1` | Aksen utama, link, highlight aktif |
| `--indigo-dark` | `#4338ca` | Teks aksen kuat, header tabel |
| `--cyan` | `#06b6d4` | Aksen sekunder, gradient partner |
| `--emerald` | `#10b981` | Sukses, fase naik (unwinding) |
| `--amber` | `#f59e0b` | Peringatan, base case |

### Warna Netral (Surface & Text)

| Token | Hex | Fungsi |
|---|---|---|
| `--bg` | `#f4f1ec` | Latar belakang utama (warm cream) |
| `--bg-secondary` | `#ebe7e0` | Latar belakang sekunder |
| `--surface` | `#fffdf8` | Permukaan kartu terang (receipt) |
| `--dark` | `#1a1a2e` | Teks utama, header gelap |
| `--dark-hover` | `#2d2d4e` | Hover tombol primer |
| `--text` | `#4a4637` | Teks paragraf |
| `--text-muted` | `#9a9385` | Label, keterangan |
| `--text-faint` | `#b8b0a4` | Kategori, subtext |
| `--border` | `#e2ddd5` | Garis pemisah, border tab |
| `--border-light` | `#d4cfc5` | Border struk belanja |
| `--border-dotted` | `#e8e3da` | Garis titik-titik |

### Warna Transparan (Glass)

| Token | Nilai | Fungsi |
|---|---|---|
| `--glass-bg` | `rgba(255, 255, 255, 0.45)` | Latar kartu glassmorphic |
| `--glass-bg-hover` | `rgba(255, 255, 255, 0.6)` | Hover kartu |
| `--glass-border` | `rgba(255, 255, 255, 0.6)` | Border kaca |
| `--glass-inset` | `rgba(255, 255, 255, 0.8)` | Inset shadow highlight |
| `--shadow` | `rgba(26, 26, 46, 0.02)` | Bayangan halus |

---

## 3. Tipografi

### Import Google Fonts

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap');
```

### Penggunaan Font

| Font | Peran | Contoh Penggunaan |
|---|---|---|
| **DM Sans** | Body default | Paragraf, label, tombol |
| **Space Grotesk** | Display & heading | Judul kartu, metrik, section label |
| **JetBrains Mono** | Monospace & data | Harga, kode, struk, trace |

### Skala Ukuran

| Elemen | Size | Weight |
|---|---|---|
| Hero title (`.hdr h1`) | `1.7rem` | 700 |
| Metric value (`.mc-val`) | `1.6rem` | 700 |
| Card name (`.pc-name`) | `0.82rem` | 600 |
| Price (`.pc-price`) | `0.85rem` | 500 |
| Section label (`.sl`) | `0.65rem` | 600, uppercase, `letter-spacing: 0.15em` |
| Body text | `0.78rem` | 400 |
| Micro label (`.mc-lbl`) | `0.65rem` | 400, uppercase, `letter-spacing: 0.1em` |

---

## 4. Komponen Inti

### 4.1 Glass Card (Kartu Utama)

```css
.glass-card {
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    box-shadow: 0 4px 16px 0 rgba(26, 26, 46, 0.02),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.8);
    border-radius: 14px;
    padding: 1rem;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.glass-card:hover {
    transform: translateY(-2px);
    background: rgba(255, 255, 255, 0.6);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: 0 8px 24px 0 rgba(99, 102, 241, 0.06),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.9);
}
```

### 4.2 Metric Card

```css
.mc {
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 4px 16px 0 rgba(26, 26, 46, 0.02);
    text-align: center;
}
.mc-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem; font-weight: 700;
    color: #6366f1;
}
.mc-lbl {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9a9385;
    margin-top: 0.2rem;
}
```

**Pemakaian di Python (Streamlit):**
```python
st.markdown('''
<div class="mc">
    <div class="mc-val">Rp 44.000</div>
    <div class="mc-lbl">Total Belanja</div>
</div>
''', unsafe_allow_html=True)
```

### 4.3 Section Label

```css
.sl {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.65rem; font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #9a9385;
    margin-bottom: 0.6rem;
}
```

### 4.4 Dark Header Banner

```css
.hdr {
    position: relative;
    background: #1a1a2e;
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    overflow: hidden;
}
.hdr::before {
    content: '';
    position: absolute;
    top: -60px; right: -40px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(99,102,241,0.35) 0%, transparent 70%);
    border-radius: 50%;
}
.hdr::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 350px; height: 200px;
    background: radial-gradient(ellipse, rgba(6,182,212,0.25) 0%, transparent 70%);
}
.hdr h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.7rem; font-weight: 700;
    color: #ffffff; margin: 0;
}
.hdr p { color: rgba(255,255,255,0.55); font-size: 0.78rem; }
.hdr-pill {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.12);
    color: rgba(255,255,255,0.7);
    border-radius: 100px;
    padding: 0.3rem 0.85rem;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
}
```

### 4.5 Receipt / Thermal Paper Card

```css
.receipt {
    background: #fffdf8;
    border: 1px dashed #d4cfc5;
    border-radius: 4px;
    padding: 1.3rem 1.4rem;
    box-shadow: 2px 3px 10px rgba(0,0,0,0.06);
    font-family: 'JetBrains Mono', monospace;
}
.receipt::after {
    content: '';
    position: absolute;
    bottom: -6px; left: 0; right: 0; height: 6px;
    background:
        linear-gradient(135deg, #fffdf8 33.33%, transparent 33.33%) -6px 0,
        linear-gradient(225deg, #fffdf8 33.33%, transparent 33.33%) -6px 0;
    background-size: 12px 6px;
}
```

### 4.6 Comparison Table

```css
.comp-table {
    width: 100%; border-collapse: collapse; font-size: 0.8rem;
}
.comp-table th {
    text-align: left;
    padding: 0.7rem 0.9rem;
    background: rgba(99, 102, 241, 0.06);
    color: #4338ca;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    border-bottom: 2px solid rgba(99, 102, 241, 0.12);
}
.comp-table td {
    padding: 0.7rem 0.9rem;
    border-bottom: 1px solid rgba(26, 26, 46, 0.05);
    color: #4a4637;
}
.comp-table tr:hover td { background: rgba(255, 255, 255, 0.2); }
```

### 4.7 Success Banner

```css
.success-banner {
    background: rgba(16, 185, 129, 0.06);
    border: 1px solid rgba(16, 185, 129, 0.22);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.8rem;
    color: #065f46;
    font-weight: 500;
    backdrop-filter: blur(12px);
}
```

### 4.8 Chart Description Card

```css
.chart-desc {
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 12px;
    padding: 0.8rem 1.1rem;
    font-size: 0.74rem;
    color: #4a4637;
    line-height: 1.45;
}
.chart-desc strong {
    font-family: 'Space Grotesk', sans-serif;
    color: #1a1a2e;
}
```

---

## 5. Latar Belakang Gradient Mesh

```css
.stApp {
    background: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.04) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(6, 182, 212, 0.04) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.04) 0px, transparent 50%),
                #f4f1ec;
}
```

> Gradient mesh ini memberikan kedalaman refractive pada komponen glass tanpa mengganggu keterbacaan konten.

---

## 6. Override Widget Streamlit

### Tabs

```css
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid #e2ddd5;
}
.stTabs [data-baseweb="tab"] {
    color: #9a9385; font-weight: 500; font-size: 0.82rem;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: #1a1a2e !important; font-weight: 600;
    border-bottom: 2px solid #6366f1 !important;
}
```

### Buttons

```css
.stButton>button {
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    border: 1px solid #e2ddd5 !important;
    transition: 0.12s;
}
.stButton>button:hover {
    border-color: #6366f1 !important;
    color: #6366f1 !important;
}
.stButton>button[kind="primary"] {
    background: #1a1a2e !important;
    color: #fff !important;
    border: none !important;
}
```

### Multiselect

```css
div[data-baseweb="select"] {
    background: rgba(255, 255, 255, 0.3) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(255, 255, 255, 0.5) !important;
    border-radius: 8px !important;
}
span[data-baseweb="tag"] {
    background: rgba(99, 102, 241, 0.08) !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 6px !important;
    color: #4338ca !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
}
ul[role="listbox"] {
    background: rgba(255, 255, 255, 0.92) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 25px rgba(26, 26, 46, 0.08) !important;
}
```

### Slider

```css
div[data-baseweb="slider"] > div > div > div {
    background: linear-gradient(90deg, #6366f1, #06b6d4) !important;
}
div[role="slider"] {
    background: #ffffff !important;
    border: 2px solid #6366f1 !important;
    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.3) !important;
    transition: transform 0.1s ease !important;
}
div[role="slider"]:hover {
    transform: scale(1.15) !important;
    border-color: #06b6d4 !important;
}
```

---

## 7. Animasi

### Pulse Glow (untuk elemen aktif)

```css
@keyframes pulse-glow {
    0%   { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.25); }
    70%  { box-shadow: 0 0 0 5px rgba(99, 102, 241, 0); }
    100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
}
.active-element {
    animation: pulse-glow 1.8s infinite ease-in-out;
}
```

### Card Hover Lift

```css
.hoverable {
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.hoverable:hover {
    transform: translateY(-2px);
}
```

---

## 8. Plotly Chart Styling

Gunakan konfigurasi layout ini agar grafik Plotly menyatu dengan tema:

```python
C = {"indigo": "#6366f1", "cyan": "#06b6d4", "emerald": "#10b981"}

fig.update_layout(
    xaxis=dict(
        showgrid=False, color="#9a9385",
        tickfont=dict(family="Space Grotesk", size=9)
    ),
    yaxis=dict(
        showgrid=True, gridcolor="#ebe7e0", zeroline=False,
        color="#9a9385",
        tickfont=dict(family="JetBrains Mono", size=9)
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#9a9385"),
    legend=dict(
        bgcolor="rgba(255,255,255,0.75)",
        bordercolor="#e2ddd5", borderwidth=1,
        font=dict(size=10, family="DM Sans")
    ),
    hovermode="x unified",
    margin=dict(t=20, b=40, l=60, r=20),
    height=360,
)
```

---

## 9. Boilerplate Awal untuk Proyek Baru

### `style.css` (minimal starter)

```css
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap');

*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: radial-gradient(at 0% 0%, rgba(99,102,241,0.04) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(6,182,212,0.04) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139,92,246,0.04) 0px, transparent 50%),
                #f4f1ec;
}
.block-container { padding: 1.2rem 2rem; max-width: 1440px; }

/* — Tambahkan komponen dari Section 4 sesuai kebutuhan — */
```

### `app.py` (minimal starter)

```python
import streamlit as st

st.set_page_config(page_title="Nama Proyek", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown('''
<div class="hdr">
    <div class="hdr-inner">
        <div>
            <h1>Nama Proyek</h1>
            <p>Deskripsi singkat proyek</p>
        </div>
        <div class="hdr-tag">
            <span class="hdr-pill">v1.0</span>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Konten utama
tab1, tab2 = st.tabs(["Tab Pertama", "Tab Kedua"])

with tab1:
    st.markdown('<div class="sl">Section Label</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('''
        <div class="mc">
            <div class="mc-val" style="color: #6366f1;">42</div>
            <div class="mc-lbl">Metrik Satu</div>
        </div>
        ''', unsafe_allow_html=True)
```

---

## 10. Prinsip Desain

| Prinsip | Implementasi |
|---|---|
| **Warm Neutrals** | Hindari putih murni `#fff`. Gunakan krem hangat `#f4f1ec` sebagai latar. |
| **Glassmorphism** | Selalu kombinasikan `backdrop-filter: blur()` + `border semi-transparan` + `inset shadow putih`. |
| **Tipografi Hierarkis** | Space Grotesk untuk judul, DM Sans untuk teks, JetBrains Mono untuk data. |
| **Warna Bermakna** | Indigo = aksi utama, Cyan = aksen sekunder, Emerald = sukses, Amber = peringatan. |
| **Micro-animation** | Gunakan `cubic-bezier(0.16, 1, 0.3, 1)` untuk hover lift, `ease-in-out` untuk glow. |
| **Tanpa Emoji** | Gunakan tipografi dan warna sebagai pengganti ikon emoji untuk kesan profesional. |

---

*Style guide ini diekstrak dari proyek [unwindPOS](https://github.com/azrlb23/unwindPOS).*
