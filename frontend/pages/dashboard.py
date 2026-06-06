import streamlit as st
from utils.api import get_dashboard_stats
from utils.style import badge_status, badge_tipe, KATEGORI_ICON
from datetime import datetime

BASE_URL = "http://localhost:8000"


def format_date(dt_str):
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d %b %Y, %H:%M")
    except Exception:
        return dt_str


def render():
    user = st.session_state.user or {}
    nama = user.get("nama", "").split()[0]

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="rf-page-header">
        <div class="rf-page-title">Halo, {nama}! 👋</div>
        <div class="rf-page-sub">Selamat datang di ReFound — platform kehilangan &amp; penemuan barang ITS</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fetch data ─────────────────────────────────────────────────────────────
    with st.spinner("Memuat data..."):
        stats, code = get_dashboard_stats()

    if code != 200:
        st.error("Gagal memuat data dashboard.")
        return

    # ── Stat cards ─────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="rf-stat">
            <div class="rf-stat-icon" style="background:#FEF3F2;">🔴</div>
            <div class="rf-stat-num">{stats['total_hilang']}</div>
            <div class="rf-stat-label">Total Barang Hilang</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="rf-stat">
            <div class="rf-stat-icon" style="background:#ECFDF3;">🟢</div>
            <div class="rf-stat-num">{stats['total_ditemukan']}</div>
            <div class="rf-stat-label">Total Barang Ditemukan</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="rf-stat">
            <div class="rf-stat-icon" style="background:#EBF4FF;">✅</div>
            <div class="rf-stat-num">{stats['total_selesai']}</div>
            <div class="rf-stat-label">Laporan Selesai</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

    # ── Statistik kategori + Laporan terbaru ─────────────────────────────────
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("""
        <div class="rf-card">
            <div style="font-size:15px;font-weight:700;color:#101828;margin-bottom:1rem;">
                📊 Statistik Kategori
            </div>
        """, unsafe_allow_html=True)

        stat_kat = stats.get("statistik_kategori", {})
        if stat_kat:
            total = sum(stat_kat.values()) or 1
            for kat, jumlah in sorted(stat_kat.items(), key=lambda x: -x[1]):
                icon = KATEGORI_ICON.get(kat, "📦")
                pct = int(jumlah / total * 100)
                st.markdown(f"""
                <div style="margin-bottom:.75rem;">
                    <div style="display:flex;justify-content:space-between;
                                font-size:13px;color:#344054;margin-bottom:4px;">
                        <span>{icon} {kat.replace("_"," ").title()}</span>
                        <span style="font-weight:600;">{jumlah}</span>
                    </div>
                    <div style="background:#EAECF0;border-radius:99px;height:6px;">
                        <div style="background:#0074CC;height:6px;border-radius:99px;
                                    width:{pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="rf-empty" style="padding:1.5rem 0;">
                <div class="rf-empty-icon">📊</div>
                <div class="rf-empty-text">Belum ada data</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="rf-card" style="padding:0;">
            <div style="padding:1.25rem 1.5rem;border-bottom:1px solid #EAECF0;">
                <div style="font-size:15px;font-weight:700;color:#101828;">
                    🕐 Laporan Terbaru
                </div>
            </div>
        """, unsafe_allow_html=True)

        laporan = stats.get("laporan_terbaru", [])
        if laporan:
            rows_html = ""
            for item in laporan:
                icon = KATEGORI_ICON.get(item.get("kategori", ""), "📦")
                tipe_html = badge_tipe(item.get("tipe", ""))
                status_html = badge_status(item.get("status", ""))
                rows_html += f"""
                <tr>
                    <td>
                        <div style="font-weight:600;color:#101828;font-size:13px;">
                            {icon} {item['nama_barang']}
                        </div>
                        <div style="font-size:11px;color:#667085;margin-top:2px;">
                            📍 {item['lokasi']}
                        </div>
                    </td>
                    <td>{tipe_html}</td>
                    <td>{status_html}</td>
                    <td style="font-size:12px;color:#667085;">
                        {format_date(item['created_at'])}
                    </td>
                </tr>
                """
            st.markdown(f"""
            <table class="rf-table">
                <thead>
                    <tr>
                        <th>Barang</th>
                        <th>Tipe</th>
                        <th>Status</th>
                        <th>Tanggal</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="rf-empty">
                <div class="rf-empty-icon">📋</div>
                <div class="rf-empty-text">Belum ada laporan</div>
                <div class="rf-empty-sub">Jadilah yang pertama melaporkan!</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Quick actions ─────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:15px;font-weight:700;color:#101828;margin-bottom:.75rem;">
        ⚡ Aksi Cepat
    </div>
    """, unsafe_allow_html=True)

    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("🔴  Laporkan Kehilangan", use_container_width=True, type="primary"):
            st.session_state.page = "lapor"
            st.session_state.prefill_tipe = "hilang"
            st.rerun()
    with qa2:
        if st.button("🟢  Laporkan Penemuan", use_container_width=True):
            st.session_state.page = "lapor"
            st.session_state.prefill_tipe = "ditemukan"
            st.rerun()
    with qa3:
        if st.button("🔍  Cari Barang", use_container_width=True):
            st.session_state.page = "browse"
            st.rerun()