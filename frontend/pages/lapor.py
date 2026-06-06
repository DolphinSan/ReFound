import streamlit as st
from utils.api import create_item

KATEGORI_LIST = ["elektronik", "dokumen", "pakaian", "aksesoris", "alat_tulis", "tas", "lainnya"]
TIPE_LIST     = ["hilang", "ditemukan"]


def render():
    st.markdown("""
    <div class="rf-page-header">
        <div class="rf-page-title">➕ Buat Laporan</div>
        <div class="rf-page-sub">Laporkan barang yang hilang atau yang Anda temukan</div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_tip = st.columns([2, 1])

    with col_form:
        st.markdown('<div class="rf-card">', unsafe_allow_html=True)

        # Prefill tipe dari quick action dashboard
        prefill_tipe = st.session_state.pop("prefill_tipe", None)
        tipe_default = TIPE_LIST.index(prefill_tipe) if prefill_tipe in TIPE_LIST else 0

        with st.form("form_laporan", clear_on_submit=True):
            st.markdown('<div class="rf-section">Tipe Laporan</div>', unsafe_allow_html=True)
            tipe = st.radio(
                "Tipe",
                options=TIPE_LIST,
                format_func=lambda x: "🔴 Saya kehilangan barang" if x == "hilang"
                                      else "🟢 Saya menemukan barang",
                index=tipe_default,
                horizontal=True,
                label_visibility="collapsed",
            )

            st.markdown('<div class="rf-section">Detail Barang</div>', unsafe_allow_html=True)

            nama_barang = st.text_input(
                "Nama Barang *",
                placeholder="Contoh: Dompet kulit cokelat, Laptop Asus..."
            )

            col_kat, col_lok = st.columns(2)
            with col_kat:
                kategori = st.selectbox(
                    "Kategori *",
                    KATEGORI_LIST,
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
            with col_lok:
                lokasi = st.text_input(
                    "Lokasi *",
                    placeholder="Contoh: Perpustakaan lantai 2, Gedung D3..."
                )

            deskripsi = st.text_area(
                "Deskripsi",
                placeholder="Jelaskan ciri-ciri barang, warna, merek, kondisi, dll...",
                height=120,
            )

            st.markdown('<div class="rf-section">Foto Barang (opsional)</div>',
                        unsafe_allow_html=True)
            foto = st.file_uploader(
                "Upload foto",
                type=["jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed",
            )

            if foto:
                st.image(foto, caption="Preview foto", use_column_width=True)

            st.markdown("<div style='margin-top:.5rem;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button(
                "📤  Kirim Laporan", use_container_width=True, type="primary"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not nama_barang or not lokasi:
                st.error("Nama barang dan lokasi wajib diisi.")
            else:
                with st.spinner("Mengirim laporan..."):
                    data, code = create_item(
                        nama_barang=nama_barang,
                        deskripsi=deskripsi,
                        kategori=kategori,
                        lokasi=lokasi,
                        tipe=tipe,
                        foto=foto,
                    )
                if code == 201:
                    st.success(f"✅ Laporan **{data['nama_barang']}** berhasil dikirim!")
                    st.balloons()
                    if st.button("📋 Lihat laporan saya"):
                        st.session_state.page = "laporanku"
                        st.rerun()
                else:
                    st.error(data.get("detail", "Gagal mengirim laporan."))

    with col_tip:
        st.markdown("""
        <div class="rf-card">
            <div style="font-size:15px;font-weight:700;color:#101828;margin-bottom:1rem;">
                💡 Tips Laporan yang Baik
            </div>
            <div style="font-size:13px;color:#344054;line-height:1.8;">
                <div style="margin-bottom:.6rem;">
                    <strong>📌 Nama Barang</strong><br>
                    Sebutkan nama spesifik beserta warna/merek jika ada.
                </div>
                <div style="margin-bottom:.6rem;">
                    <strong>📍 Lokasi</strong><br>
                    Tulis lokasi selengkap mungkin, termasuk lantai atau ruangan.
                </div>
                <div style="margin-bottom:.6rem;">
                    <strong>📝 Deskripsi</strong><br>
                    Sertakan ciri-ciri unik agar mudah dikenali pemiliknya.
                </div>
                <div>
                    <strong>📷 Foto</strong><br>
                    Foto sangat membantu mempercepat proses pencocokan barang.
                </div>
            </div>
        </div>

        <div class="rf-card" style="margin-top:0;">
            <div style="font-size:15px;font-weight:700;color:#101828;margin-bottom:.75rem;">
                📂 Kategori Barang
            </div>
            <div style="font-size:13px;color:#344054;line-height:2;">
                💻 Elektronik &nbsp; 📄 Dokumen<br>
                👕 Pakaian &nbsp;&nbsp;&nbsp; 👜 Aksesoris<br>
                ✏️ Alat Tulis &nbsp; 🎒 Tas<br>
                📦 Lainnya
            </div>
        </div>
        """, unsafe_allow_html=True)