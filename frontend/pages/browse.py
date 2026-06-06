import streamlit as st
from utils.api import get_items
from utils.style import badge_status, badge_tipe, KATEGORI_ICON
from datetime import datetime

BASE_URL = "http://localhost:8000"

KATEGORI_OPTIONS = ["", "elektronik", "dokumen", "pakaian", "aksesoris", "alat_tulis", "tas", "lainnya"]
STATUS_OPTIONS   = ["", "aktif", "diproses", "selesai"]
TIPE_OPTIONS     = ["", "hilang", "ditemukan"]


def format_date(dt_str):
    try:
        return datetime.fromisoformat(dt_str).strftime("%d %b %Y")
    except Exception:
        return dt_str


def render():
    st.markdown("""
    <div class="rf-page-header">
        <div class="rf-page-title">🔍 Cari Barang</div>
        <div class="rf-page-sub">Temukan barang hilang atau yang sudah ditemukan di kampus ITS</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter bar ────────────────────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="rf-card" style="padding:1rem 1.25rem;">', unsafe_allow_html=True)
        f1, f2, f3, f4, f5 = st.columns([2.5, 1.5, 1.5, 1.5, 1])

        with f1:
            search = st.text_input("", placeholder="🔍  Cari nama barang...",
                                   label_visibility="collapsed")
        with f2:
            tipe_label = st.selectbox("Tipe", ["Semua Tipe", "Hilang", "Ditemukan"],
                                      label_visibility="collapsed")
            tipe = "" if tipe_label == "Semua Tipe" else tipe_label.lower()
        with f3:
            kat_label = st.selectbox(
                "Kategori",
                ["Semua Kategori", "Elektronik", "Dokumen", "Pakaian",
                 "Aksesoris", "Alat Tulis", "Tas", "Lainnya"],
                label_visibility="collapsed"
            )
            kategori = "" if kat_label == "Semua Kategori" else kat_label.lower().replace(" ", "_")
        with f4:
            status_label = st.selectbox("Status", ["Semua Status", "Aktif", "Diproses", "Selesai"],
                                        label_visibility="collapsed")
            status = "" if status_label == "Semua Status" else status_label.lower()
        with f5:
            cari = st.button("Cari", use_container_width=True, type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Fetch data ────────────────────────────────────────────────────────────
    with st.spinner("Memuat data..."):
        items, code = get_items(
            tipe=tipe or None,
            kategori=kategori or None,
            status=status or None,
            search=search or None,
            limit=50,
        )

    if code != 200:
        st.error("Gagal memuat data.")
        return

    # ── Result count ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="font-size:13px;color:#667085;margin:.75rem 0 1rem;">
        Menampilkan <strong style="color:#101828;">{len(items)}</strong> laporan
    </div>
    """, unsafe_allow_html=True)

    if not items:
        st.markdown("""
        <div class="rf-empty">
            <div class="rf-empty-icon">🔍</div>
            <div class="rf-empty-text">Tidak ada hasil ditemukan</div>
            <div class="rf-empty-sub">Coba ubah kata kunci atau filter pencarian</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Grid kartu barang ─────────────────────────────────────────────────────
    cols_per_row = 3
    for i in range(0, len(items), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(items):
                break
            item = items[idx]
            with col:
                icon = KATEGORI_ICON.get(item.get("kategori", ""), "📦")
                foto_url = item.get("foto_url")

                # Foto atau placeholder
                if foto_url:
                    img_html = f'<img src="{BASE_URL}{foto_url}" class="rf-item-img" alt="foto">'
                else:
                    img_html = f'<div class="rf-item-img-placeholder">{icon}</div>'

                deskripsi = item.get("deskripsi") or "Tidak ada deskripsi"
                if len(deskripsi) > 70:
                    deskripsi = deskripsi[:70] + "..."

                st.markdown(f"""
                <div class="rf-item-card">
                    {img_html}
                    <div class="rf-item-body">
                        <div class="rf-item-title">{item['nama_barang']}</div>
                        <div class="rf-item-meta">📍 {item['lokasi']}</div>
                        <div class="rf-item-meta">
                            {icon} {item.get('kategori','').replace('_',' ').title()}
                        </div>
                        <div style="font-size:12px;color:#667085;margin-top:.4rem;
                                    line-height:1.5;">{deskripsi}</div>
                    </div>
                    <div class="rf-item-footer">
                        {badge_tipe(item.get('tipe',''))}
                        {badge_status(item.get('status',''))}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Info tambahan
                st.markdown(f"""
                <div style="font-size:11px;color:#667085;text-align:center;
                            margin-top:4px;margin-bottom:.5rem;">
                    👤 {item.get('owner',{}).get('nama','?')} •
                    📅 {format_date(item.get('created_at',''))}
                </div>
                """, unsafe_allow_html=True)