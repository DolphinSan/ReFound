import streamlit as st
from utils.api import get_items, update_item, update_status, delete_item
from utils.style import badge_status, badge_tipe, KATEGORI_ICON
from datetime import datetime

BASE_URL = "http://localhost:8000"

KATEGORI_LIST = ["elektronik", "dokumen", "pakaian", "aksesoris", "alat_tulis", "tas", "lainnya"]
STATUS_LIST   = ["aktif", "diproses", "selesai"]


def format_date(dt_str):
    try:
        return datetime.fromisoformat(dt_str).strftime("%d %b %Y, %H:%M")
    except Exception:
        return dt_str


def render():
    st.markdown("""
    <div class="rf-page-header">
        <div class="rf-page-title">📋 Laporan Saya</div>
        <div class="rf-page-sub">Kelola semua laporan barang yang pernah Anda buat</div>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.user or {}
    user_id = user.get("id")

    # ── Fetch semua item lalu filter milik user ───────────────────────────────
    with st.spinner("Memuat laporan..."):
        all_items, code = get_items(limit=100)

    if code != 200:
        st.error("Gagal memuat data.")
        return

    # Filter hanya milik user ini
    items = [i for i in all_items if i.get("user_id") == user_id]

    if not items:
        st.markdown("""
        <div class="rf-empty">
            <div class="rf-empty-icon">📋</div>
            <div class="rf-empty-text">Anda belum membuat laporan</div>
            <div class="rf-empty-sub">Klik tombol di bawah untuk membuat laporan pertama Anda</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("➕  Buat Laporan Pertama", type="primary"):
            st.session_state.page = "lapor"
            st.rerun()
        return

    # ── Ringkasan milik user ──────────────────────────────────────────────────
    total_hilang   = sum(1 for i in items if i["tipe"] == "hilang")
    total_ditemukan = sum(1 for i in items if i["tipe"] == "ditemukan")
    total_selesai  = sum(1 for i in items if i["status"] == "selesai")

    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, str(len(items)),      "Total Laporan",    "#EBF4FF", "#0074CC"),
        (c2, str(total_hilang),    "Barang Hilang",    "#FEF3F2", "#F04438"),
        (c3, str(total_ditemukan), "Barang Ditemukan", "#ECFDF3", "#12B76A"),
        (c4, str(total_selesai),   "Selesai",          "#F0FDF4", "#16A34A"),
    ]
    for col, num, label, bg, color in metrics:
        with col:
            st.markdown(f"""
            <div class="rf-stat">
                <div class="rf-stat-num" style="color:{color};">{num}</div>
                <div class="rf-stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

    # ── Tombol buat laporan baru ──────────────────────────────────────────────
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("➕  Buat Laporan Baru", type="primary", use_container_width=True):
            st.session_state.page = "lapor"
            st.rerun()

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    # ── Daftar laporan ────────────────────────────────────────────────────────
    for item in items:
        icon = KATEGORI_ICON.get(item.get("kategori", ""), "📦")
        item_id = item["id"]
        key = f"item_{item_id}"

        with st.expander(
            f"{icon}  {item['nama_barang']}  —  {item.get('tipe','').upper()}  |  {item.get('status','').upper()}",
            expanded=False,
        ):
            col_info, col_foto = st.columns([2, 1])

            with col_info:
                st.markdown(f"""
                <div style="font-size:13px;color:#344054;line-height:2;">
                    <div>{badge_tipe(item['tipe'])} &nbsp; {badge_status(item['status'])}</div>
                    <div style="margin-top:.5rem;">
                        <strong>📍 Lokasi:</strong> {item['lokasi']}<br>
                        <strong>🏷️ Kategori:</strong>
                            {item.get('kategori','').replace('_',' ').title()}<br>
                        <strong>📅 Dibuat:</strong> {format_date(item['created_at'])}<br>
                        <strong>📝 Deskripsi:</strong>
                            {item.get('deskripsi') or '<em style="color:#9CA3AF;">Tidak ada deskripsi</em>'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_foto:
                foto_url = item.get("foto_url")
                if foto_url:
                    st.image(f"{BASE_URL}{foto_url}", use_column_width=True)
                else:
                    st.markdown(f"""
                    <div style="background:#F5F7FA;border-radius:10px;height:120px;
                                display:flex;align-items:center;justify-content:center;
                                font-size:36px;color:#D0D5DD;">
                        {icon}
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr class='rf-divider'>", unsafe_allow_html=True)

            # ── Tab: Update Status | Edit | Hapus ─────────────────────────────
            tab_status, tab_edit, tab_hapus = st.tabs([
                "🔄 Update Status", "✏️ Edit Laporan", "🗑️ Hapus"
            ])

            # Tab Update Status
            with tab_status:
                st.markdown(
                    "<div style='font-size:13px;color:#667085;margin-bottom:.5rem;'>"
                    "Perbarui status laporan ini:</div>",
                    unsafe_allow_html=True
                )
                col_sel, col_upd = st.columns([2, 1])
                with col_sel:
                    new_status = st.selectbox(
                        "Status baru",
                        STATUS_LIST,
                        index=STATUS_LIST.index(item["status"]) if item["status"] in STATUS_LIST else 0,
                        key=f"sel_status_{key}",
                        label_visibility="collapsed",
                        format_func=lambda x: {
                            "aktif":    "🔵 Aktif",
                            "diproses": "🟡 Diproses",
                            "selesai":  "🟢 Selesai",
                        }.get(x, x)
                    )
                with col_upd:
                    if st.button("Simpan", key=f"btn_status_{key}", use_container_width=True,
                                 type="primary"):
                        with st.spinner("Menyimpan..."):
                            res, code2 = update_status(item_id, new_status)
                        if code2 == 200:
                            st.success("Status berhasil diperbarui!")
                            st.rerun()
                        else:
                            st.error(res.get("detail", "Gagal update status."))

            # Tab Edit
            with tab_edit:
                with st.form(f"form_edit_{key}"):
                    e_nama = st.text_input(
                        "Nama Barang", value=item["nama_barang"], key=f"e_nama_{key}"
                    )
                    e_col1, e_col2 = st.columns(2)
                    with e_col1:
                        e_kat = st.selectbox(
                            "Kategori", KATEGORI_LIST,
                            index=KATEGORI_LIST.index(item["kategori"])
                                  if item["kategori"] in KATEGORI_LIST else 0,
                            key=f"e_kat_{key}",
                            format_func=lambda x: {
                                "elektronik": "💻 Elektronik",
                                "dokumen":    "📄 Dokumen",
                                "pakaian":    "👕 Pakaian",
                                "aksesoris":  "👜 Aksesoris",
                                "alat_tulis": "✏️ Alat Tulis",
                                "tas":        "🎒 Tas",
                                "lainnya":    "📦 Lainnya",
                            }.get(x, x)
                        )
                    with e_col2:
                        e_lok = st.text_input(
                            "Lokasi", value=item["lokasi"], key=f"e_lok_{key}"
                        )
                    e_desk = st.text_area(
                        "Deskripsi",
                        value=item.get("deskripsi") or "",
                        key=f"e_desk_{key}",
                        height=100,
                    )
                    e_status = st.selectbox(
                        "Status", STATUS_LIST,
                        index=STATUS_LIST.index(item["status"])
                              if item["status"] in STATUS_LIST else 0,
                        key=f"e_status_{key}",
                        format_func=lambda x: {
                            "aktif":    "🔵 Aktif",
                            "diproses": "🟡 Diproses",
                            "selesai":  "🟢 Selesai",
                        }.get(x, x)
                    )
                    save_edit = st.form_submit_button(
                        "💾  Simpan Perubahan", use_container_width=True, type="primary"
                    )

                if save_edit:
                    if not e_nama or not e_lok:
                        st.error("Nama barang dan lokasi wajib diisi.")
                    else:
                        with st.spinner("Menyimpan perubahan..."):
                            res, code3 = update_item(item_id, {
                                "nama_barang": e_nama,
                                "kategori":    e_kat,
                                "lokasi":      e_lok,
                                "deskripsi":   e_desk or None,
                                "status":      e_status,
                            })
                        if code3 == 200:
                            st.success("Laporan berhasil diperbarui!")
                            st.rerun()
                        else:
                            st.error(res.get("detail", "Gagal menyimpan perubahan."))

            # Tab Hapus
            with tab_hapus:
                st.markdown(f"""
                <div style="background:#FEF3F2;border:1px solid #FECDCA;border-radius:8px;
                            padding:.85rem 1rem;font-size:13px;color:#B42318;margin-bottom:.75rem;">
                    ⚠️ <strong>Perhatian:</strong> Laporan <strong>{item['nama_barang']}</strong>
                    akan dihapus permanen dan tidak bisa dikembalikan.
                </div>
                """, unsafe_allow_html=True)

                konfirmasi = st.checkbox(
                    f"Saya yakin ingin menghapus laporan ini",
                    key=f"chk_hapus_{key}"
                )
                if st.button(
                    "🗑️  Hapus Laporan", key=f"btn_hapus_{key}",
                    disabled=not konfirmasi,
                    use_container_width=True,
                ):
                    with st.spinner("Menghapus..."):
                        status_code = delete_item(item_id)
                    if status_code == 204:
                        st.success("Laporan berhasil dihapus.")
                        st.rerun()
                    else:
                        st.error("Gagal menghapus laporan.")