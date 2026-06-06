GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* ── Reset & Base ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Sembunyikan elemen default Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Warna & Variabel ─────────────────────────────────────────── */
:root {
    --blue-primary:   #0074CC;
    --blue-light:     #EBF4FF;
    --blue-hover:     #005FA3;
    --gray-50:        #F5F7FA;
    --gray-100:       #EAECF0;
    --gray-200:       #D0D5DD;
    --gray-500:       #667085;
    --gray-700:       #344054;
    --gray-900:       #101828;
    --green:          #12B76A;
    --green-light:    #ECFDF3;
    --orange:         #F79009;
    --orange-light:   #FFFAEB;
    --red:            #F04438;
    --red-light:      #FEF3F2;
    --white:          #FFFFFF;
    --shadow-sm:      0 1px 3px rgba(16,24,40,.06), 0 1px 2px rgba(16,24,40,.04);
    --shadow-md:      0 4px 8px -2px rgba(16,24,40,.08), 0 2px 4px -2px rgba(16,24,40,.04);
    --radius:         12px;
    --radius-sm:      8px;
}

/* ── Layout utama ─────────────────────────────────────────────── */
.main .block-container {
    padding: 2rem 2.5rem 2rem 2.5rem !important;
    max-width: 1200px !important;
}

/* ── Sidebar ──────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--gray-100) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebarNav"] { display: none !important; }

/* ── Card ─────────────────────────────────────────────────────── */
.rf-card {
    background: var(--white);
    border: 1px solid var(--gray-100);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
    transition: box-shadow .2s;
}
.rf-card:hover { box-shadow: var(--shadow-md); }

/* ── Stat card ────────────────────────────────────────────────── */
.rf-stat {
    background: var(--white);
    border: 1px solid var(--gray-100);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--shadow-sm);
}
.rf-stat-icon {
    width: 44px; height: 44px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    margin-bottom: .75rem;
}
.rf-stat-num {
    font-size: 28px; font-weight: 700;
    color: var(--gray-900); line-height: 1;
    margin-bottom: .25rem;
}
.rf-stat-label {
    font-size: 13px; color: var(--gray-500); font-weight: 500;
}

/* ── Badge status ─────────────────────────────────────────────── */
.rf-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 2px 10px; border-radius: 999px;
    font-size: 12px; font-weight: 600;
}
.rf-badge-aktif    { background: var(--blue-light);   color: var(--blue-primary); }
.rf-badge-diproses { background: var(--orange-light); color: var(--orange); }
.rf-badge-selesai  { background: var(--green-light);  color: var(--green); }
.rf-badge-hilang   { background: var(--red-light);    color: var(--red); }
.rf-badge-ditemukan{ background: var(--green-light);  color: var(--green); }

/* ── Item card ────────────────────────────────────────────────── */
.rf-item-card {
    background: var(--white);
    border: 1px solid var(--gray-100);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    transition: box-shadow .2s, transform .2s;
    height: 100%;
}
.rf-item-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
.rf-item-img {
    width: 100%; height: 160px;
    object-fit: cover; display: block;
}
.rf-item-img-placeholder {
    width: 100%; height: 160px;
    background: var(--gray-50);
    display: flex; align-items: center; justify-content: center;
    font-size: 40px; color: var(--gray-200);
}
.rf-item-body { padding: 1rem; }
.rf-item-title {
    font-size: 15px; font-weight: 600;
    color: var(--gray-900); margin-bottom: .35rem;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.rf-item-meta {
    font-size: 12px; color: var(--gray-500);
    display: flex; align-items: center; gap: 4px;
    margin-bottom: .2rem;
}
.rf-item-footer {
    padding: .75rem 1rem;
    border-top: 1px solid var(--gray-100);
    display: flex; justify-content: space-between; align-items: center;
}

/* ── Page header ──────────────────────────────────────────────── */
.rf-page-header {
    margin-bottom: 1.75rem;
}
.rf-page-title {
    font-size: 22px; font-weight: 700;
    color: var(--gray-900); margin: 0;
}
.rf-page-sub {
    font-size: 14px; color: var(--gray-500); margin-top: 2px;
}

/* ── Section label ────────────────────────────────────────────── */
.rf-section {
    font-size: 12px; font-weight: 600;
    color: var(--gray-500); text-transform: uppercase;
    letter-spacing: .06em; margin: 1.5rem 0 .5rem;
}

/* ── Tombol Streamlit ─────────────────────────────────────────── */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all .2s !important;
}
.stButton > button[kind="primary"] {
    background: var(--blue-primary) !important;
    border-color: var(--blue-primary) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--blue-hover) !important;
    border-color: var(--blue-hover) !important;
}

/* ── Input fields ─────────────────────────────────────────────── */
.stTextInput input, .stSelectbox select,
.stTextArea textarea {
    border-radius: var(--radius-sm) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    border-color: var(--gray-200) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--blue-primary) !important;
    box-shadow: 0 0 0 3px rgba(0,116,204,.12) !important;
}

/* ── Alert / pesan ────────────────────────────────────────────── */
.stAlert {
    border-radius: var(--radius-sm) !important;
}

/* ── Divider ──────────────────────────────────────────────────── */
.rf-divider {
    border: none; border-top: 1px solid var(--gray-100);
    margin: 1.25rem 0;
}

/* ── Tabel laporan ────────────────────────────────────────────── */
.rf-table { width: 100%; border-collapse: collapse; }
.rf-table th {
    font-size: 12px; font-weight: 600; color: var(--gray-500);
    text-transform: uppercase; letter-spacing: .05em;
    padding: .75rem 1rem; border-bottom: 1px solid var(--gray-100);
    text-align: left; background: var(--gray-50);
}
.rf-table td {
    font-size: 14px; color: var(--gray-700);
    padding: .85rem 1rem; border-bottom: 1px solid var(--gray-100);
    vertical-align: middle;
}
.rf-table tr:last-child td { border-bottom: none; }
.rf-table tr:hover td { background: var(--gray-50); }

/* ── Empty state ──────────────────────────────────────────────── */
.rf-empty {
    text-align: center; padding: 3rem 1rem;
    color: var(--gray-500);
}
.rf-empty-icon { font-size: 48px; margin-bottom: .75rem; }
.rf-empty-text { font-size: 15px; font-weight: 500; }
.rf-empty-sub  { font-size: 13px; margin-top: .25rem; }
</style>
"""


def badge_status(status: str) -> str:
    icons = {"aktif": "🔵", "diproses": "🟡", "selesai": "🟢"}
    return f'<span class="rf-badge rf-badge-{status}">{icons.get(status,"●")} {status.capitalize()}</span>'


def badge_tipe(tipe: str) -> str:
    icons = {"hilang": "🔴", "ditemukan": "🟢"}
    return f'<span class="rf-badge rf-badge-{tipe}">{icons.get(tipe,"●")} {tipe.capitalize()}</span>'


KATEGORI_ICON = {
    "elektronik": "💻",
    "dokumen":    "📄",
    "pakaian":    "👕",
    "aksesoris":  "👜",
    "alat_tulis": "✏️",
    "tas":        "🎒",
    "lainnya":    "📦",
}