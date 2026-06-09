"""app.py — KasirRekursif · Unified Visualizer & Controllable Glassmorphic UI"""
import sys, time, pathlib
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

sys.setrecursionlimit(1_100_000)

from src.kasir import KATALOG, get_product, keranjang_ke_items, recursive_total_harga, get_rekursi_steps
from src.generator import generate_processes
from src.analyzer import recursive_merge_sort
from src.visualizer_core import get_mergesort_steps, get_roundrobin_steps
import random

st.set_page_config(page_title="unwindPOS", layout="wide", initial_sidebar_state="collapsed")

# ── Load external CSS ──
css = pathlib.Path("style.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ── Palette ref for Plotly (not in CSS) ──
C = dict(indigo="#6366f1", dark="#1a1a2e", warm="#f4f1ec", paper="#fffdf8",
         cyan="#06b6d4", green="#10b981", amber="#f59e0b", purple="#8b5cf6",
         muted="#9a9385", border="#e2ddd5", card="#ffffff")

# ── State ──
for k, v in {
    "keranjang": {},
    "bench_results": None,
    "last_total": None,
    "trace_page": 0,
    "visualizing": False,
    "anim_running": False,
    "anim_step_index": 0,
    "anim_speed": 0.2,
    "items_flat": [],
    "steps": [],
    "ms_arr": [],
    "ms_steps": [],
    "ms_anim_idx": 0,
    "ms_running": False,
    "rr_queue": [],
    "rr_quantum": 4,
    "rr_steps": [],
    "rr_anim_idx": 0,
    "rr_running": False,
    "bench_demo_steps": [],
    "bench_demo_idx": 0,
    "bench_demo_running": False,
    "bench_demo_n": 10
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helper for Live Chart ──
def draw_live_recursion_chart(items, step):
    n = len(items)
    fase = step["fase"]
    idx = step["index"]

    colors = []
    for j in range(n):
        if fase == "dasar":
            colors.append("rgba(99, 102, 241, 0.4)")  # Indigo-200 translucent
        elif fase == "turun":
            if j < idx:
                colors.append("rgba(99, 102, 241, 0.4)")
            elif j == idx:
                colors.append("#6366f1")  # Active indigo
            else:
                colors.append("#e2ddd5")  # Warm-gray
        elif fase == "naik":
            if j < idx:
                colors.append("rgba(99, 102, 241, 0.4)")
            elif j == idx:
                colors.append("#34d399")  # Active returning emerald
            else:
                colors.append("#10b981")  # Emerald resolved

    names = [f"Item {j}" for j in range(n)]
    prices = [item[1] for item in items]

    fig = go.Figure(go.Bar(
        x=names, y=prices,
        marker_color=colors,
        text=[f"Rp {p:,}" for p in prices],
        textposition="outside",
        cliponaxis=False,
        textfont=dict(family="Space Grotesk", size=9, color="#1a1a2e"),
        hovertemplate="<b>%{x}</b><br>Harga: Rp %{y:,}<extra></extra>"
    ))

    fig.update_layout(
        xaxis=dict(
            tickfont=dict(size=9, family="Space Grotesk"),
            color="#9a9385",
            showline=False,
            showgrid=False
        ),
        yaxis=dict(
            visible=False  # Hide Y axis completely for clean widget look
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#9a9385"),
        margin=dict(t=15, b=10, l=10, r=10), height=180,
    )
    return fig

# ── Header ──
st.markdown("""
<div class="hdr">
  <div class="hdr-inner">
    <div>
      <h1>unwindPOS</h1>
      <p>Perancangan &amp; Analisis Algoritma &middot; Institut Teknologi Kalimantan</p>
    </div>
    <div class="hdr-tag">
      <span class="hdr-pill">O(n) time</span>
      <span class="hdr-pill">O(n) space</span>
      <span class="hdr-pill">python recursion</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

tab1, tab_ms, tab_rr, tab2, tab3 = st.tabs(["Simulasi Kasir", "Merge Sort (Visual)", "Round Robin (Visual)", "Benchmark", "Cara Kerja"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_cat, col_cart = st.columns([6, 4], gap="large")

    # ── Katalog ──
    with col_cat:
        st.markdown('<div class="sl">Katalog Produk</div>', unsafe_allow_html=True)
        kat_list = ["Semua"] + sorted({p["kategori"] for p in KATALOG})
        kat_sel = st.selectbox("Filter", kat_list, label_visibility="collapsed")
        tampil = KATALOG if kat_sel == "Semua" else [p for p in KATALOG if p["kategori"] == kat_sel]

        for row in [tampil[i:i+3] for i in range(0, len(tampil), 3)]:
            cols = st.columns(3, gap="small")
            for col, prod in zip(cols, row):
                with col:
                    qty = st.session_state.keranjang.get(prod["id"], 0)
                    st.markdown(f'''<div class="pc">
                        <div class="pc-name">{prod["nama"]}</div>
                        <div class="pc-cat">{prod["kategori"]}</div>
                        <div class="pc-price">Rp {prod["harga"]:,}</div>
                    </div>''', unsafe_allow_html=True)
                    c1, c2, c3 = st.columns([1, 1, 1])
                    with c1:
                        if st.button("+", key=f"a{prod['id']}", use_container_width=True):
                            st.session_state.keranjang[prod["id"]] = qty + 1
                            st.session_state.last_total = None
                            st.session_state.trace_page = 0
                            st.session_state.visualizing = False
                            st.session_state.anim_running = False
                            st.rerun()
                    with c2:
                        st.markdown(f'<div class="qty-display">{qty}</div>', unsafe_allow_html=True)
                    with c3:
                        if st.button("−", key=f"r{prod['id']}", use_container_width=True, disabled=qty == 0):
                            if qty > 1:
                                st.session_state.keranjang[prod["id"]] = qty - 1
                            else:
                                st.session_state.keranjang.pop(prod["id"], None)
                            st.session_state.last_total = None
                            st.session_state.trace_page = 0
                            st.session_state.visualizing = False
                            st.session_state.anim_running = False
                            st.rerun()

    # ── Receipt Cart ──
    with col_cart:
        st.markdown('<div class="sl">Struk Belanja</div>', unsafe_allow_html=True)
        keranjang = st.session_state.keranjang

        if not keranjang:
            st.markdown('<div class="receipt"><div class="receipt-empty">Keranjang kosong — tambahkan item dari katalog.</div></div>', unsafe_allow_html=True)
        else:
            now = time.strftime("%d/%m/%Y %H:%M")
            rows_html = ""
            grand = 0
            for pid, qty in keranjang.items():
                prod = get_product(pid)
                if prod:
                    sub = prod["harga"] * qty
                    grand += sub
                    rows_html += f'<div class="receipt-row"><span class="receipt-rn">{prod["nama"]}</span><span class="receipt-rq">x{qty}</span><span class="receipt-rs">Rp {sub:,}</span></div>'

            total_html = ""
            if st.session_state.last_total is not None:
                total_html = f'<div class="receipt-total"><span>TOTAL</span><span>Rp {st.session_state.last_total:,}</span></div>'

            # Build HTML string flat to prevent Streamlit markdown parser from indent-wrapping it
            receipt_html = (
                f'<div class="receipt">'
                f'<div class="receipt-hdr">'
                f'<div class="receipt-hdr-title">unwindPOS</div>'
                f'<div class="receipt-hdr-sub">{now} &mdash; ITK Balikpapan</div>'
                f'</div>'
                f'{rows_html}'
                f'{total_html}'
                f'</div>'
            )
            st.markdown(receipt_html, unsafe_allow_html=True)

        st.markdown("")
        cA, cB = st.columns(2)
        with cA:
            if st.button("Kosongkan", use_container_width=True, disabled=not keranjang):
                st.session_state.keranjang = {}
                st.session_state.last_total = None
                st.session_state.trace_page = 0
                st.session_state.visualizing = False
                st.session_state.anim_running = False
                st.rerun()
        with cB:
            hitung = st.button("Hitung Total", use_container_width=True, type="primary", disabled=not keranjang)

        # ── Donut chart ──
        if keranjang:
            kat_tot = {}
            for pid, qty in keranjang.items():
                prod = get_product(pid)
                if prod:
                    kat_tot[prod["kategori"]] = kat_tot.get(prod["kategori"], 0) + prod["harga"] * qty
            if kat_tot:
                cat_colors = {"Makanan": C["amber"], "Minuman": C["cyan"], "Sembako": C["green"], "Kebersihan": C["purple"]}
                colors = [cat_colors.get(k, C["muted"]) for k in kat_tot]
                
                # Grand total for annotation
                g_total = sum(kat_tot.values())
                
                fig_pie = go.Figure(go.Pie(
                    labels=list(kat_tot.keys()), values=list(kat_tot.values()),
                    hole=0.68, marker_colors=colors,
                    textinfo="percent",
                    textfont=dict(family="Space Grotesk", size=10, color="#ffffff"),
                    hovertemplate="<b>%{label}</b><br>Total: Rp %{value:,}<extra></extra>"
                ))
                fig_pie.update_layout(
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=9, family="DM Sans"),
                        bgcolor="rgba(0,0,0,0)"
                    ),
                    annotations=[dict(
                        text=f'<span style="font-family:Space Grotesk;font-size:9px;color:#9a9385;text-transform:uppercase;letter-spacing:0.05em">Total</span><br><b style="font-family:JetBrains Mono;font-size:12px;color:#1a1a2e">Rp {g_total:,}</b>',
                        showarrow=False,
                        x=0.5, y=0.5
                    )],
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, b=40, l=10, r=10), height=230,
                )
                st.plotly_chart(fig_pie, use_container_width=True, theme=None)
                st.markdown('''
                <div class="chart-desc">
                    <strong>Proporsi Kategori Belanja</strong><br>
                    Membagi nilai total belanja berdasarkan kategori produk untuk memberikan gambaran ke mana anggaran didistribusikan.
                </div>
                ''', unsafe_allow_html=True)

    # ── Recursion animation & results ──
    if keranjang:
        if hitung:
            items_flat = keranjang_ke_items(keranjang)
            st.session_state.items_flat = items_flat
            st.session_state.steps = get_rekursi_steps(items_flat)
            st.session_state.anim_step_index = 0
            st.session_state.anim_running = True
            st.session_state.anim_speed = 0.2
            st.session_state.visualizing = True
            st.session_state.last_total = recursive_total_harga(items_flat)
            st.rerun()

        # Render Active Animation Panel
        elif st.session_state.visualizing:
            items_flat = st.session_state.items_flat
            steps = st.session_state.steps
            idx = st.session_state.anim_step_index
            total_steps = len(steps)
            is_completed = (idx >= total_steps - 1)

            st.markdown("---")
            st.markdown('<div class="sl">Visualisasi Proses Rekursi</div>', unsafe_allow_html=True)

            # Controller Panel Layout
            c_ctrl1, c_ctrl2, c_ctrl3, c_ctrl4, c_ctrl5 = st.columns([2, 2, 2, 2, 2])
            with c_ctrl1:
                # Play/Pause or Replay
                if is_completed:
                    if st.button("Replay", use_container_width=True):
                        st.session_state.anim_step_index = 0
                        st.session_state.anim_running = True
                        st.rerun()
                else:
                    play_label = "Pause" if st.session_state.anim_running else "Play"
                    if st.button(play_label, use_container_width=True):
                        st.session_state.anim_running = not st.session_state.anim_running
                        st.rerun()
            with c_ctrl2:
                # Step Backward
                if st.button("Step Back", use_container_width=True, disabled=st.session_state.anim_running or idx == 0):
                    st.session_state.anim_step_index = max(0, idx - 1)
                    st.rerun()
            with c_ctrl3:
                # Step Forward
                if st.button("Step Forward", use_container_width=True, disabled=st.session_state.anim_running or is_completed):
                    st.session_state.anim_step_index = min(total_steps - 1, idx + 1)
                    st.rerun()
            with c_ctrl4:
                # Speed Toggles (0.5x, 1x, 2x)
                speeds = [0.4, 0.2, 0.05]
                speed_labels = ["0.5x", "1.0x", "2.0x"]
                current_speed = st.session_state.anim_speed
                try:
                    speed_idx = speeds.index(current_speed)
                except ValueError:
                    speed_idx = 1
                next_speed_idx = (speed_idx + 1) % len(speeds)
                speed_btn_label = f"Speed: {speed_labels[speed_idx]}"
                if st.button(speed_btn_label, use_container_width=True, disabled=is_completed):
                    st.session_state.anim_speed = speeds[next_speed_idx]
                    st.rerun()
            with c_ctrl5:
                # Skip
                if st.button("Skip", use_container_width=True, disabled=is_completed):
                    st.session_state.anim_step_index = total_steps - 1
                    st.session_state.anim_running = False
                    st.rerun()

            # Progress Indicator
            progress_pct = (idx + 1) / total_steps
            st.progress(progress_pct, text=f"Langkah {idx + 1} dari {total_steps}")

            # Columns for current State trace
            col_tr, col_sk = st.columns([6, 4], gap="large")
            shown = steps[:idx + 1]

            # Construct call stack
            call_stack = []
            for s in shown:
                if s["fase"] in ("turun", "dasar"):
                    call_stack.append(s)
                elif s["fase"] == "naik" and call_stack:
                    call_stack.pop()

            with col_tr:
                # Pagination logic for Trace
                page_size = 10
                shown_len = len(shown)
                total_pages = (shown_len - 1) // page_size + 1
                
                # Clamp trace_page to valid bounds
                st.session_state.trace_page = max(0, min(st.session_state.trace_page, total_pages - 1))
                page = st.session_state.trace_page
                start_idx = page * page_size
                end_idx = min(start_idx + page_size, shown_len)
                
                st.markdown(f'<div class="sl">Trace Rekursi (Langkah {start_idx + 1} - {end_idx} dari {shown_len})</div>', unsafe_allow_html=True)
                for s in shown[start_idx:end_idx]:
                    f = s["fase"]
                    badge_label = "Fase Turun" if f == "turun" else ("Base Case" if f == "dasar" else "Fase Naik")
                    st.markdown(f'''
                    <div class="trace-card trace-card-{f}">
                        <span class="trace-badge trace-badge-{f}">{badge_label}</span>
                        <div style="color: #1a1a2e; line-height: 1.4;">{s["deskripsi"]}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Pagination controls
                if total_pages > 1:
                    pcol1, pcol2, pcol3 = st.columns([3, 4, 3])
                    with pcol1:
                        if st.button("Sebelumnya", key="prev_trace", disabled=page == 0, use_container_width=True):
                            st.session_state.trace_page = page - 1
                            st.rerun()
                    with pcol2:
                        st.markdown(f'<div style="text-align: center; font-size: 0.78rem; color: #9a9385; margin-top: 6px;">Halaman {page + 1} dari {total_pages}</div>', unsafe_allow_html=True)
                    with pcol3:
                        if st.button("Berikutnya", key="next_trace", disabled=page == total_pages - 1, use_container_width=True):
                            st.session_state.trace_page = page + 1
                            st.rerun()

            with col_sk:
                st.markdown('<div class="sl">Call Stack & Space Gauge</div>', unsafe_allow_html=True)
                
                # Space complexity gauge
                stack_depth = len(call_stack)
                max_depth = len(items_flat)
                st.markdown(f'''
                <div class="mc" style="margin-bottom: 1rem; padding: 0.8rem 1rem;">
                    <div class="mc-val" style="font-size: 1.3rem;">{stack_depth} / {max_depth}</div>
                    <div class="mc-lbl">Stack Depth (Space Complexity)</div>
                </div>
                ''', unsafe_allow_html=True)

                if not call_stack:
                    st.markdown('<div class="stk stk-base">Stack Kosong</div>', unsafe_allow_html=True)
                else:
                    for frame in reversed(call_stack[-8:]):
                        is_active = (frame == call_stack[-1]) and not is_completed
                        css = "stk-base" if frame["fase"] == "dasar" else ("stk-active" if is_active else "stk")
                        st.markdown(f'<div class="stk {css}">f(items, {frame["index"]}) {frame["nama"][:16]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="sl">Visualisasi Live State Rekursi</div>', unsafe_allow_html=True)
            fig_live = draw_live_recursion_chart(items_flat, steps[idx])
            st.plotly_chart(fig_live, use_container_width=True, theme=None)
            
            st.markdown('''
            <div class="chart-desc">
                <strong>Status Call Stack Rekursi</strong><br>
                Menunjukkan kondisi pemrosesan memori saat ini:
                <ul>
                    <li><span class="legend-dot" style="background:rgba(99, 102, 241, 0.4)"></span> <strong>Di Stack:</strong> Item terdaftar di stack memori, menunggu pemanggilan selesai.</li>
                    <li><span class="legend-dot" style="background:#6366f1"></span> <strong>Aktif (Turun):</strong> Fungsi sedang memanggil index ini (fase turun).</li>
                    <li><span class="legend-dot" style="background:#34d399"></span> <strong>Aktif (Naik):</strong> Fungsi menerima nilai kembali (fase naik).</li>
                    <li><span class="legend-dot" style="background:#10b981"></span> <strong>Selesai (Resolved):</strong> Nilai item telah diakumulasikan.</li>
                    <li><span class="legend-dot" style="background:#e2ddd5"></span> <strong>Belum Dikunjungi:</strong> Item belum tersentuh proses rekursi.</li>
                </ul>
            </div>
            ''', unsafe_allow_html=True)

            # Inline final results when completed
            if is_completed:
                # Waterfall
                st.markdown('<div class="sl">Akumulasi Nilai — Fase Naik</div>', unsafe_allow_html=True)
                naik = [s for s in steps if s["fase"] == "naik"]
                if naik:
                    names = [s["nama"][:12] for s in reversed(naik)]
                    prices = [s["harga"] for s in reversed(naik)]
                    wf = go.Figure(go.Waterfall(
                        orientation="v", measure=["relative"] * len(prices),
                        x=names, y=prices,
                        connector=dict(line=dict(color="#6366f1", width=1.5, dash="dot")),
                        increasing=dict(marker_color="rgba(16, 185, 129, 0.8)"),
                        text=[f"+Rp{p:,}" for p in prices], textposition="outside",
                        cliponaxis=False,
                        textfont=dict(family="JetBrains Mono", size=9, color="#1a1a2e"),
                        hovertemplate="<b>%{x}</b><br>Akumulasi: Rp %{y:,}<extra></extra>"
                    ))
                    wf.update_layout(
                        xaxis=dict(
                            tickfont=dict(size=9, family="Space Grotesk"),
                            color="#9a9385",
                            showline=False,
                            showgrid=False
                        ),
                        yaxis=dict(
                            title="Akumulasi (Rp)",
                            tickfont=dict(size=9, family="JetBrains Mono"),
                            color="#9a9385",
                            gridcolor="#ebe7e0",
                            zeroline=False
                        ),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="DM Sans", color=C["muted"]),
                        margin=dict(t=20, b=40, l=55, r=10), height=300,
                    )
                    st.plotly_chart(wf, use_container_width=True, theme=None)
                    
                    st.markdown('''
                    <div class="chart-desc">
                        <strong>Waterfall Akumulasi Harga (Fase Naik)</strong><br>
                        Menunjukkan bagaimana total harga dihitung secara bertahap saat rekursi kembali naik (unwinding). Setiap anak tangga merepresentasikan kontribusi harga barang yang ditambahkan ke sub-total sebelumnya, hingga mencapai total harga belanja akhir di puncak rekursi.
                    </div>
                    ''', unsafe_allow_html=True)

                st.markdown(f'<div class="success-banner">Selesai — Total: Rp {st.session_state.last_total:,} | Kedalaman: {len(items_flat)} level</div>', unsafe_allow_html=True)

            # Rerun timer
            if st.session_state.anim_running and not is_completed:
                time.sleep(st.session_state.anim_speed)
                st.session_state.anim_step_index += 1
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# TAB MERGE SORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab_ms:
    st.markdown('<div class="sl">Pengaturan Merge Sort</div>', unsafe_allow_html=True)
    c_ms_ctrl, c_ms_vis = st.columns([3, 7], gap="large")
    
    with c_ms_ctrl:
        st.markdown('<div class="ctrl-card-title">Pengaturan Merge Sort</div>', unsafe_allow_html=True)
        n_ms = st.slider("Jumlah Elemen Array (N)", 4, 32, 16, step=2, key="n_ms")
        if st.button("Generate & Mulai Simulasi", key="btn_ms_gen", use_container_width=True, type="primary"):
            st.session_state.ms_arr = [random.randint(10, 99) for _ in range(n_ms)]
            st.session_state.ms_steps = get_mergesort_steps(st.session_state.ms_arr)
            st.session_state.ms_anim_idx = 0
            st.session_state.ms_running = True
            st.rerun()
        
    with c_ms_vis:
        if st.session_state.ms_steps:
            steps = st.session_state.ms_steps
            idx = st.session_state.ms_anim_idx
            step = steps[idx]
            is_done = (idx >= len(steps) - 1)
            
            st.markdown('<div class="sl">Visualisasi Array</div>', unsafe_allow_html=True)
            
            c_p, c_b, c_f, c_s = st.columns(4)
            with c_p:
                if st.button("Play/Pause", key="ms_play", use_container_width=True, disabled=is_done):
                    st.session_state.ms_running = not st.session_state.ms_running
                    st.rerun()
            with c_b:
                if st.button("Step Back", key="ms_back", use_container_width=True, disabled=st.session_state.ms_running or idx == 0):
                    st.session_state.ms_anim_idx = max(0, idx - 1)
                    st.rerun()
            with c_f:
                if st.button("Step Forward", key="ms_fwd", use_container_width=True, disabled=st.session_state.ms_running or is_done):
                    st.session_state.ms_anim_idx = min(len(steps) - 1, idx + 1)
                    st.rerun()
            with c_s:
                if st.button("Skip to End", key="ms_skip", use_container_width=True, disabled=is_done):
                    st.session_state.ms_anim_idx = len(steps) - 1
                    st.session_state.ms_running = False
                    st.rerun()
                    
            st.progress((idx + 1) / len(steps), text=step["msg"])
            
            arr = step["arr"]
            bounds = step["bounds"]
            action = step["action"]
            colors = []
            for i in range(len(arr)):
                if i >= bounds[0] and i < bounds[1]:
                    if action == "divide": colors.append(C["amber"])
                    elif action == "compare":
                        if "compare_indices" in step and i in step["compare_indices"]:
                            colors.append(C["indigo"])
                        else:
                            colors.append(C["cyan"])
                    elif action == "merge_done": colors.append(C["green"])
                    elif action == "base": colors.append(C["purple"])
                    else: colors.append(C["cyan"])
                else:
                    colors.append(C["border"])
                    
            fig_ms = go.Figure(go.Bar(
                x=[f"Idx {i}" for i in range(len(arr))], y=arr,
                marker_color=colors, text=arr, textposition="auto",
                textfont=dict(family="JetBrains Mono", size=12, color="#1a1a2e")
            ))
            fig_ms.update_layout(
                yaxis=dict(visible=False), xaxis=dict(visible=False),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=10, l=10, r=10), height=250
            )
            st.plotly_chart(fig_ms, use_container_width=True, config={'displayModeBar': False})
            
            if is_done:
                st.markdown('''
                <div class="success-banner" style="margin-top: 1rem;">
                    <strong>Kesimpulan Visualisasi Merge Sort:</strong><br>
                    Terbukti bahwa algoritma Merge Sort memproses pengurutan tidak dengan mengecek satu per satu secara linear, melainkan dengan memecah total <b>N</b> elemen menjadi sub-elemen terkecil (log N), lalu menaklukkan dan menggabungkannya kembali secara terurut. Efisiensi <b>O(n log n)</b> ini menjadikannya sangat optimal untuk sistem antrean pemindahan data dalam skala masif.
                </div>
                ''', unsafe_allow_html=True)
            
            if st.session_state.ms_running and not is_done:
                time.sleep(0.4)
                st.session_state.ms_anim_idx += 1
                st.rerun()
        else:
            st.info("Tekan tombol Generate & Mulai Simulasi untuk melihat visualisasi Merge Sort.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB ROUND ROBIN
# ═══════════════════════════════════════════════════════════════════════════════
with tab_rr:
    st.markdown('<div class="sl">Pengaturan Round Robin</div>', unsafe_allow_html=True)
    c_rr_ctrl, c_rr_vis = st.columns([3, 7], gap="large")
    
    with c_rr_ctrl:
        st.markdown('<div class="ctrl-card-title">Pengaturan Round Robin</div>', unsafe_allow_html=True)
        n_rr = st.slider("Jumlah Proses (N)", 3, 10, 5, key="n_rr")
        q_rr = st.slider("Quantum", 2, 10, 4, key="q_rr")
        if st.button("Generate & Mulai Simulasi", key="btn_rr_gen", use_container_width=True, type="primary"):
            st.session_state.rr_queue = [[f"P{i+1}", random.randint(5, 20)] for i in range(n_rr)]
            st.session_state.rr_quantum = q_rr
            st.session_state.rr_steps = get_roundrobin_steps(st.session_state.rr_queue, q_rr)
            st.session_state.rr_anim_idx = 0
            st.session_state.rr_running = True
            st.rerun()
        
    with c_rr_vis:
        if st.session_state.rr_steps:
            steps = st.session_state.rr_steps
            idx = st.session_state.rr_anim_idx
            step = steps[idx]
            is_done = (idx >= len(steps) - 1)
            
            st.markdown('<div class="sl">Visualisasi Antrean & CPU</div>', unsafe_allow_html=True)
            
            c_p, c_b, c_f, c_s = st.columns(4)
            with c_p:
                if st.button("Play/Pause", key="rr_play", use_container_width=True, disabled=is_done):
                    st.session_state.rr_running = not st.session_state.rr_running
                    st.rerun()
            with c_b:
                if st.button("Step Back", key="rr_back", use_container_width=True, disabled=st.session_state.rr_running or idx == 0):
                    st.session_state.rr_anim_idx = max(0, idx - 1)
                    st.rerun()
            with c_f:
                if st.button("Step Forward", key="rr_fwd", use_container_width=True, disabled=st.session_state.rr_running or is_done):
                    st.session_state.rr_anim_idx = min(len(steps) - 1, idx + 1)
                    st.rerun()
            with c_s:
                if st.button("Skip to End", key="rr_skip", use_container_width=True, disabled=is_done):
                    st.session_state.rr_anim_idx = len(steps) - 1
                    st.session_state.rr_running = False
                    st.rerun()
                    
            st.progress((idx + 1) / len(steps), text=f"Waktu: {step['time']}s | {step['msg']}")
            
            c_cpu, c_q = st.columns([3, 7])
            with c_cpu:
                st.markdown('<div style="text-align:center; font-family:Space Grotesk; font-weight:600; color:#1a1a2e; margin-bottom:10px;">Dalam CPU</div>', unsafe_allow_html=True)
                if step["active"]:
                    name, burst = step["active"]
                    st.markdown(f'''
                    <div class="pc" style="background: rgba(99,102,241,0.1); border-color: #6366f1; text-align:center; padding: 2rem 1rem;">
                        <div class="pc-name" style="font-size: 1.5rem; color:#4338ca;">{name}</div>
                        <div class="pc-price" style="font-size: 1rem;">Sisa: {burst}s</div>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown('''
                    <div class="pc" style="background: rgba(226,221,213,0.3); border-style: dashed; text-align:center; padding: 2rem 1rem; opacity: 0.7;">
                        <div class="pc-name" style="color:#9a9385;">CPU IDLE</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
            with c_q:
                st.markdown('<div style="font-family:Space Grotesk; font-weight:600; color:#1a1a2e; margin-bottom:10px;">Antrean (Queue)</div>', unsafe_allow_html=True)
                q_html = '<div style="display: flex; gap: 10px; overflow-x: auto; padding-bottom: 10px;">'
                if not step["queue"]:
                    q_html += '<div style="color:#9a9385; font-size:0.9rem; font-style:italic;">Antrean kosong</div>'
                for p in step["queue"]:
                    q_html += f'<div class="pc" style="min-width: 100px; text-align:center; flex-shrink: 0;"><div class="pc-name">{p[0]}</div><div class="pc-cat">Sisa: {p[1]}s</div></div>'
                q_html += '</div>'
                st.markdown(q_html, unsafe_allow_html=True)
                
            if is_done:
                st.markdown('''
                <div class="success-banner" style="margin-top: 1rem; border-left-color: #06b6d4; background-color: rgba(6, 182, 212, 0.05);">
                    <strong>Kesimpulan Visualisasi Round Robin:</strong><br>
                    Terbukti bahwa algoritma Round Robin memberikan <b>keadilan waktu (fairness)</b> bagi setiap proses. Proses dengan waktu eksekusi raksasa tidak diizinkan memonopoli CPU, melainkan diinterupsi secara paksa (<i>preemptive</i>) berdasarkan batas <b>Quantum</b>. Sistem ini menjamin bahwa proses kecil di belakang antrean tidak akan pernah mati menunggu (<i>starvation</i>).
                </div>
                ''', unsafe_allow_html=True)
                
            if st.session_state.rr_running and not is_done:
                time.sleep(0.6)
                st.session_state.rr_anim_idx += 1
                st.rerun()
        else:
            st.info("Tekan tombol Generate & Mulai Simulasi untuk melihat visualisasi Round Robin.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sl">Benchmark Performa</div>', unsafe_allow_html=True)

    # ── Demo Rekursi Step-by-Step ──
    st.markdown('<div class="ctrl-card-title">Demonstrasi Rekursi pada N Kecil</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-desc" style="margin-bottom:1rem;">Pilih nilai N kecil dan jalankan animasi untuk melihat bagaimana rekursi memproses setiap elemen satu per satu sebelum grafik besar dibentuk dari eksekusi ribuan elemen ini.</div>', unsafe_allow_html=True)

    demo_col_ctrl, demo_col_vis = st.columns([3, 7], gap="large")
    with demo_col_ctrl:
        demo_n = st.slider("Pilih N untuk Demo", 4, 20, 10, key="bench_demo_n_slider")
        if st.button("Jalankan Demo Rekursi", key="btn_bench_demo", type="primary", use_container_width=True):
            from src.kasir import keranjang_ke_items, get_rekursi_steps
            demo_procs = generate_processes(demo_n)
            demo_items = [(p[0], p[1] * 1000) for p in demo_procs]
            st.session_state.bench_demo_steps = get_rekursi_steps(demo_items)
            st.session_state.bench_demo_idx = 0
            st.session_state.bench_demo_running = True
            st.session_state.bench_demo_n = demo_n
            st.rerun()

    with demo_col_vis:
        if st.session_state.bench_demo_steps:
            b_steps = st.session_state.bench_demo_steps
            b_idx = st.session_state.bench_demo_idx
            b_step = b_steps[b_idx]
            b_done = (b_idx >= len(b_steps) - 1)

            bc1, bc2, bc3, bc4 = st.columns(4)
            with bc1:
                if st.button("Play/Pause", key="bench_demo_play", use_container_width=True, disabled=b_done):
                    st.session_state.bench_demo_running = not st.session_state.bench_demo_running
                    st.rerun()
            with bc2:
                if st.button("Step Back", key="bench_demo_back", use_container_width=True, disabled=st.session_state.bench_demo_running or b_idx == 0):
                    st.session_state.bench_demo_idx = max(0, b_idx - 1)
                    st.rerun()
            with bc3:
                if st.button("Step Forward", key="bench_demo_fwd", use_container_width=True, disabled=st.session_state.bench_demo_running or b_done):
                    st.session_state.bench_demo_idx = min(len(b_steps) - 1, b_idx + 1)
                    st.rerun()
            with bc4:
                if st.button("Skip", key="bench_demo_skip", use_container_width=True, disabled=b_done):
                    st.session_state.bench_demo_idx = len(b_steps) - 1
                    st.session_state.bench_demo_running = False
                    st.rerun()

            st.progress((b_idx + 1) / len(b_steps), text=b_step["deskripsi"])

            # Build items list from generated processes (as tuples)
            demo_items_flat = [(f"P{i+1}", generate_processes(st.session_state.bench_demo_n)[i][1] * 1000) for i in range(st.session_state.bench_demo_n)]

            fig_demo = draw_live_recursion_chart(demo_items_flat, b_step)
            fig_demo.update_layout(height=200)
            st.plotly_chart(fig_demo, use_container_width=True, theme=None, config={'displayModeBar': False})

            if b_done:
                total_val = sum(p[1] for p in demo_items_flat)
                st.markdown(f'''
                <div class="success-banner">
                    <strong>Rekursi selesai pada N={st.session_state.bench_demo_n}!</strong> Total akumulasi: {total_val:,} unit.
                    Algoritma ini menelusuri tepat <b>{st.session_state.bench_demo_n} elemen</b> pada fase turun, dan membalik semuanya pada fase naik &mdash;
                    itulah mengapa kompleksitasnya <b>O(n)</b>. Bayangkan ini terjadi pada N=100.000 di grafik Benchmark di bawah!
                </div>
                ''', unsafe_allow_html=True)

            if st.session_state.bench_demo_running and not b_done:
                time.sleep(0.3)
                st.session_state.bench_demo_idx += 1
                st.rerun()
        else:
            st.info("Pilih N di panel kiri dan tekan 'Jalankan Demo Rekursi' untuk melihat animasi step-by-step bagaimana rekursi memproses setiap elemen.")

    st.markdown("---")
    st.markdown('<div class="sl">Benchmark Skala Penuh</div>', unsafe_allow_html=True)
    col_ctrl, col_res = st.columns([3, 7], gap="large")

    with col_ctrl:
        st.markdown('<span id="bench-settings-marker"></span>', unsafe_allow_html=True)
        st.markdown('<div class="ctrl-card-title">Pengaturan Benchmark</div>', unsafe_allow_html=True)
        size_map = {"100": 100, "500": 500, "1.000": 1000, "5.000": 5000,
                    "10.000": 10000, "50.000": 50000, "100.000": 100000}
        sel = st.multiselect("Ukuran N:", list(size_map.keys()),
                             default=["100", "500", "1.000", "5.000", "10.000", "50.000"])
        repeat = st.slider("Pengulangan per N", 1, 10, 3)
        alg_choice = st.radio("Pilih Algoritma", ["Kasir (O(n))", "Merge Sort (O(n log n))"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        run_bench = st.button("Jalankan", type="primary", use_container_width=True)
        if st.session_state.bench_results:
            if st.button("Reset", use_container_width=True):
                st.session_state.bench_results = None
                st.rerun()

    with col_res:
        if run_bench and sel:
            sizes = [size_map[s] for s in sel]
            prog = st.progress(0, text="Memulai...")
            results = []
            for i, n in enumerate(sizes):
                prog.progress(i / len(sizes), text=f"N = {n:,} ...")
                times = []
                for _ in range(repeat):
                    if alg_choice == "Kasir (O(n))":
                        procs = generate_processes(n)
                        t0 = time.perf_counter()
                        recursive_total_harga(procs)
                        times.append(time.perf_counter() - t0)
                    else:
                        files = [{"nama": f"F{j}", "size_kb": random.randint(100, 9999)} for j in range(n)]
                        t0 = time.perf_counter()
                        recursive_merge_sort(files)
                        times.append(time.perf_counter() - t0)
                results.append({"N": n, "Waktu (detik)": sum(times) / len(times), "Algoritma": alg_choice})
            prog.progress(1.0, text="Selesai")
            st.session_state.bench_results = results

        if st.session_state.bench_results:
            df = pd.DataFrame(st.session_state.bench_results)
            
            # Calculate metrics
            min_row = df.loc[df["Waktu (detik)"].idxmin()]
            max_row = df.loc[df["Waktu (detik)"].idxmax()]
            t_max = max_row["Waktu (detik)"]
            t_min = min_row["Waktu (detik)"]
            n_max = max_row["N"]
            n_min = min_row["N"]
            import math
            alg_terpilih = df["Algoritma"].iloc[0] if "Algoritma" in df.columns else "Kasir (O(n))"
            
            if t_min > 0 and n_min > 0:
                if alg_terpilih == "Kasir (O(n))":
                    linearity_ratio = (t_max / n_max) / (t_min / n_min)
                    lbl_indeks = "Indeks Skala O(n)"
                else:
                    linearity_ratio = (t_max / (n_max * math.log2(n_max))) / (t_min / (n_min * math.log2(n_min)))
                    lbl_indeks = "Indeks Skala O(n log n)"
                linearity_text = f"{linearity_ratio:.2f}x"
            else:
                linearity_text = "-"
                lbl_indeks = "Indeks Skala"

            # Render metrics cards
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.markdown(f'''
                <div class="mc">
                    <div class="mc-val">{t_min:.6f}s</div>
                    <div class="mc-lbl">Tercepat (N={min_row["N"]:,})</div>
                </div>
                ''', unsafe_allow_html=True)
            with mc2:
                st.markdown(f'''
                <div class="mc">
                    <div class="mc-val">{t_max:.6f}s</div>
                    <div class="mc-lbl">Terlambat (N={max_row["N"]:,})</div>
                </div>
                ''', unsafe_allow_html=True)
            with mc3:
                st.markdown(f'''
                <div class="mc">
                    <div class="mc-val">{linearity_text}</div>
                    <div class="mc-lbl">{lbl_indeks}</div>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            chart_tab1, chart_tab2 = st.tabs(["Kurva Penskalaan Waktu", "Efisiensi per Item"])
            
            with chart_tab1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df["N"], y=df["Waktu (detik)"], 
                    mode="lines+markers", 
                    name="Aktual",
                    line=dict(shape="spline", smoothing=1.3, color=C["indigo"], width=3.5),
                    fill="tozeroy",
                    fillcolor="rgba(99, 102, 241, 0.06)",
                    marker=dict(size=8, color=C["indigo"], symbol="circle", line=dict(color="#ffffff", width=2)),
                    hovertemplate="N = %{x:,}<br>Waktu = <b>%{y:.6f}s</b><extra></extra>"
                ))
                if len(df) > 1:
                    n0 = df["N"].iloc[0]
                    t0 = df["Waktu (detik)"].iloc[0]
                    if alg_terpilih == "Kasir (O(n))":
                        sc = t0 / n0
                        y_teori = df["N"] * sc
                        lbl_teori = "O(n) Teoritis"
                    else:
                        sc = t0 / (n0 * math.log2(n0))
                        y_teori = df["N"].apply(lambda x: x * math.log2(x) * sc)
                        lbl_teori = "O(n log n) Teoritis"

                    fig.add_trace(go.Scatter(
                        x=df["N"], y=y_teori, 
                        mode="lines", 
                        name=lbl_teori,
                        line=dict(color="#b8b0a4", width=1.5, dash="dot"),
                        hovertemplate="Teoritis = <b>%{y:.6f}s</b><extra></extra>"
                    ))
                fig.update_layout(
                    xaxis=dict(title="N (Jumlah Item)", showgrid=False, color="#9a9385", tickfont=dict(family="Space Grotesk", size=9)),
                    yaxis=dict(title="Waktu Eksekusi (s)", showgrid=True, gridcolor="#ebe7e0", zeroline=False, color="#9a9385", tickfont=dict(family="JetBrains Mono", size=9)),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans", color="#9a9385"),
                    legend=dict(x=0.02, y=0.98, xanchor="left", yanchor="top", bgcolor="rgba(255,255,255,0.75)", bordercolor="#e2ddd5", borderwidth=1, font=dict(size=10, family="DM Sans")),
                    hovermode="x unified", margin=dict(t=20, b=40, l=60, r=20), height=360,
                )
                st.plotly_chart(fig, use_container_width=True, theme=None)
                
            with chart_tab2:
                fig_eff = go.Figure()
                df["Waktu per Item (µs)"] = (df["Waktu (detik)"] / df["N"]) * 1_000_000
                fig_eff.add_trace(go.Scatter(
                    x=df["N"], y=df["Waktu per Item (µs)"], 
                    mode="lines+markers", 
                    name="Waktu/Item (µs)",
                    line=dict(shape="spline", smoothing=1.3, color=C["cyan"], width=3.5),
                    fill="tozeroy",
                    fillcolor="rgba(6, 182, 212, 0.06)",
                    marker=dict(size=8, color=C["cyan"], symbol="circle", line=dict(color="#ffffff", width=2)),
                    hovertemplate="N = %{x:,}<br>Efisiensi = <b>%{y:.4f} µs/item</b><extra></extra>"
                ))
                if len(df) > 1:
                    avg_eff = df["Waktu per Item (µs)"].mean()
                    fig_eff.add_trace(go.Scatter(
                        x=df["N"], y=[avg_eff] * len(df), 
                        mode="lines", 
                        name="Rata-rata",
                        line=dict(color="#b8b0a4", width=1.5, dash="dot"),
                        hovertemplate="Rata-rata = <b>%{y:.4f} µs/item</b><extra></extra>"
                    ))
                fig_eff.update_layout(
                    xaxis=dict(title="N (Jumlah Item)", showgrid=False, color="#9a9385", tickfont=dict(family="Space Grotesk", size=9)),
                    yaxis=dict(title="Waktu per Item (µs)", showgrid=True, gridcolor="#ebe7e0", zeroline=False, color="#9a9385", tickfont=dict(family="JetBrains Mono", size=9)),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans", color="#9a9385"),
                    legend=dict(x=0.02, y=0.98, xanchor="left", yanchor="top", bgcolor="rgba(255,255,255,0.75)", bordercolor="#e2ddd5", borderwidth=1, font=dict(size=10, family="DM Sans")),
                    hovermode="x unified", margin=dict(t=20, b=40, l=60, r=20), height=360,
                )
                st.plotly_chart(fig_eff, use_container_width=True, theme=None)

            with st.expander("💡 Bagaimana nilai N (Ukuran Dataset) diolah dalam pengujian ini?", expanded=False):
                st.markdown('''
                <div style="font-size: 0.85rem; color: #4a4637; line-height: 1.6; padding: 0.5rem 0.5rem;">
                    <ol>
                        <li><strong>Pembangkitan Data Dummy (Generation):</strong> Sistem secara dinamis memanggil fungsi <code>generate_processes(N)</code> untuk mengalokasikan array berisikan data acak sebanyak <b>N</b> elemen ke dalam memori RAM komputer.</li>
                        <li><strong>Pengukuran Terisolasi:</strong> Penghitung waktu (<code>time.perf_counter</code>) diaktifkan secara eksklusif <i>hanya</i> saat memanggil fungsi rekursinya. Waktu untuk men-<i>generate</i> data tidak ikut dihitung, sehingga grafik 100% murni mencerminkan performa algoritma.</li>
                        <li><strong>Uji Ekstrem Rekursi:</strong> Jika N=100.000, fungsi akan menumpuk (<i>Stack</i>) pemanggilan ke dalam memori sebanyak 100.000 tingkat. Inilah mengapa program PAA ini mewajibkan peningkatan batas kedalaman dengan <code>sys.setrecursionlimit</code> agar tidak terjadi <i>RecursionError</i> atau memori jebol (<i>Stack Overflow</i>).</li>
                        <li><strong>Pengulangan untuk Akurasi (Looping):</strong> Guna menghindari hasil yang cacat akibat <i>lag</i> acak dari Sistem Operasi, algoritma diuji secara berulang (contoh: 3x per ukuran N), kemudian diambil rata-rata waktu tempuhnya.</li>
                    </ol>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sl">Detail Hasil Pengujian</div>', unsafe_allow_html=True)
            c_desc, c_tbl = st.columns([5, 5], gap="large")
            with c_desc:
                st.markdown('''
                <div class="chart-desc" style="height: 100%; margin-top: 0; padding: 1.1rem 1.3rem;">
                    <strong>Analisis Kompleksitas Waktu Aktual vs Teoritis</strong><br><br>
                    Grafik di atas membandingkan waktu eksekusi aktual dari algoritma rekursif dengan estimasi linear teoritis O(n).<br><br>
                    Karena setiap item belanja hanya diproses tepat satu kali pada setiap kedalaman rekursi, grafik waktu aktual akan membentuk garis lurus (linear), membuktikan efisiensi algoritma berada pada tingkat O(n). Indeks Skala O(n) yang stabil mengonfirmasi skalabilitas linear yang konsisten tanpa overhead memori yang eksponensial.
                </div>
                ''', unsafe_allow_html=True)
            with c_tbl:
                df_s = df.copy()
                df_s["N"] = df_s["N"].apply(lambda x: f"{x:,}")
                df_s["Waktu (detik)"] = df_s["Waktu (detik)"].apply(lambda x: f"{x:.6f}")
                st.dataframe(df_s, use_container_width=True, hide_index=True)
        else:
            st.markdown('''
            <div class="receipt" style="text-align: center; padding: 3rem 2rem;">
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 600; color: #1a1a2e; margin-bottom: 0.5rem;">Siap Memulai Pengujian</div>
                <div style="font-size: 0.8rem; color: #9a9385; max-width: 400px; margin: 0 auto 1.5rem auto; line-height: 1.5;">
                    Konfigurasikan ukuran dataset N dan jumlah pengulangan di panel kiri, kemudian klik tombol <strong>Jalankan</strong> untuk memulai analisis kompleksitas waktu secara real-time.
                </div>
            </div>
            ''', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PENJELASAN
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sl">Prinsip Kerja &amp; Spesifikasi Algoritma</div>', unsafe_allow_html=True)
    
    # Complexity metrics cards row
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        st.markdown('''
        <div class="mc">
            <div class="mc-val" style="color: #6366f1;">O(n)</div>
            <div class="mc-lbl">Kompleksitas Waktu</div>
            <div style="font-size:0.75rem; color:#9a9385; margin-top:0.4rem; line-height:1.4;">
                Setiap item belanja dikunjungi tepat 1x secara linear saat rekursi turun.
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with c_m2:
        st.markdown('''
        <div class="mc">
            <div class="mc-val" style="color: #06b6d4;">O(n)</div>
            <div class="mc-lbl">Kompleksitas Ruang</div>
            <div style="font-size:0.75rem; color:#9a9385; margin-top:0.4rem; line-height:1.4;">
                Mengalokasikan 1 stack frame memori per item secara bertumpuk hingga Base Case.
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with c_m3:
        st.markdown('''
        <div class="mc">
            <div class="mc-val" style="color: #10b981;">index == len</div>
            <div class="mc-lbl">Base Case Rekursi</div>
            <div style="font-size:0.75rem; color:#9a9385; margin-top:0.4rem; line-height:1.4;">
                Menghentikan panggilan rekursif dan mulai mengembalikan nilai 0 saat antrean habis.
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_code, col_trace = st.columns(2, gap="large")
    with col_code:
        st.markdown('<div class="ctrl-card-title">Implementasi Fungsi Rekursif</div>', unsafe_allow_html=True)
        st.code("""def recursive_total_harga(items, index=0):
    # Base Case: Antrean belanja habis
    if index == len(items):
        return 0
    # Recurrence Relation: Harga saat ini + subtotal berikutnya
    return items[index]["harga"] + recursive_total_harga(items, index + 1)
""", language="python")

        st.markdown('''
        <div class="chart-desc" style="margin-top: 1.2rem; padding: 1.1rem 1.3rem;">
            <strong>Analogi Dunia Nyata: Antrean Kasir Estafet</strong><br><br>
            Bayangkan sebuah kasir belanja estafet:
            <ol style="margin-top: 0.4rem; padding-left: 1.1rem; line-height: 1.5; font-size: 0.78rem; color:#4a4637;">
                <li>Kasir ke-0 mencatat harga barang pertama, lalu mengoper keranjang sisa belanja ke kasir ke-1.</li>
                <li>Proses ini terus berlanjut (fase turun/winding) hingga keranjang kosong mencapai kasir terakhir (Base Case).</li>
                <li>Kasir terakhir mengembalikan angka <strong>Rp 0</strong> ke kasir sebelumnya.</li>
                <li>Setiap kasir menjumlahkan harga barangnya sendiri dengan sub-total yang diterimanya, lalu mengembalikannya ke kasir di atasnya (fase naik/unwinding).</li>
            </ol>
        </div>
        ''', unsafe_allow_html=True)

    with col_trace:
        st.markdown('<div class="ctrl-card-title">Jejak Call Stack (Recursion Trace)</div>', unsafe_allow_html=True)
        st.markdown('''
        <div class="receipt" style="padding: 1.2rem 1.4rem; font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; line-height: 1.65;">
            <div style="color: #6366f1; font-weight: 600; margin-bottom: 0.4rem;">▼ FASE TURUN (Winding Stack)</div>
            <div style="padding-left: 0.6rem; border-left: 2px solid #6366f1; color: #4a4637;">
                f(items, 0) = Rp 3.500 + f(items, 1)<br>
                f(items, 1) = Rp 4.000 + f(items, 2)<br>
                f(items, 2) = Rp 12.000 + f(items, 3)<br>
                f(items, 3) = Rp 0 (Base Case dicapai)<br>
            </div>
            <div style="color: #10b981; font-weight: 600; margin-top: 1rem; margin-bottom: 0.4rem;">▲ FASE NAIK (Unwinding & Accumulation)</div>
            <div style="padding-left: 0.6rem; border-left: 2px solid #10b981; color: #4a4637;">
                f(items, 2) kembali: Rp 12.000 + Rp 0 = Rp 12.000<br>
                f(items, 1) kembali: Rp 4.000 + Rp 12.000 = Rp 16.000<br>
                f(items, 0) kembali: Rp 3.500 + Rp 16.000 = Rp 19.500<br>
            </div>
            <div style="border-top: 2px solid #1a1a2e; margin-top: 1rem; padding-top: 0.6rem; font-weight: 700; color: #1a1a2e; text-align: right; font-size:0.8rem;">
                Total Terakumulasi: Rp 19.500
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div class="sl" style="margin-top: 2rem;">Pemetaan Konseptual ke Proyek Akademis PAA</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="ctrl-card" style="padding: 1.2rem 1.4rem;">
        <div style="font-size: 0.78rem; color: #9a9385; margin-bottom: 1rem; line-height: 1.5;">
            Implementasi simulasi kasir belanja ini menggunakan <strong>struktur logika dan pembuktian matematis yang identik</strong> dengan analisis kompleksitas algoritma pemrosesan tugas pada proyek PAA (`main.py`):
        </div>
        <table class="comp-table">
            <thead>
                <tr>
                    <th>Aspek Kasir (Simulasi)</th>
                    <th>Aspek Proyek PAA (`main.py` / `analyzer.py`)</th>
                    <th>Penjelasan Logis</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Daftar Item Belanja</td>
                    <td>Dataset Proses (Processes)</td>
                    <td>Kumpulan data input linear N elemen yang diproses satu per satu.</td>
                </tr>
                <tr>
                    <td>Harga Satuan Produk</td>
                    <td>Execution Time (Waktu Proses)</td>
                    <td>Bobot kuantitatif numerik pada tiap node data yang akan dijumlahkan.</td>
                </tr>
                <tr>
                    <td>Total Pembayaran Kasir</td>
                    <td>Total Waktu Eksekusi Rekursif</td>
                    <td>Hasil akhir dari akumulasi seluruh bobot data.</td>
                </tr>
                <tr>
                    <td>Jumlah Barang Belanja (N)</td>
                    <td>Ukuran Dataset Proses (N)</td>
                    <td>Parameter penentu kedalaman tumpukan memori (Call Stack depth).</td>
                </tr>
            </tbody>
        </table>
    </div>
    ''', unsafe_allow_html=True)
