import streamlit as st
import sqlite3
from factura import generar_pdf_factura

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="INK STUDIO PRO",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── ESTILOS GLOBALES ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Raleway:wght@300;400;500;600&display=swap');

/* ── FONDO Y BASE ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0d0d !important;
    color: #e8e0d5 !important;
}
[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(180,140,60,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 90%, rgba(180,140,60,0.05) 0%, transparent 50%);
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── TIPOGRAFÍA GLOBAL ── */
html, body, p, div, span, label, [class*="st-"] {
    font-family: 'Raleway', sans-serif !important;
}

/* ── HEADER PRINCIPAL ── */
.ink-header {
    text-align: center;
    padding: 3rem 0 2rem;
}
.ink-header::before {
    content: '';
    display: block;
    width: 60px; height: 2px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 0 auto 1.2rem;
}
.ink-header h1 {
    font-family: 'Cinzel', serif !important;
    font-size: 3.2rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.25em;
    background: linear-gradient(135deg, #c9a84c 0%, #f0d080 50%, #c9a84c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
    line-height: 1.1 !important;
}
.ink-header p {
    font-family: 'Raleway', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.5em;
    color: #6b6355 !important;
    text-transform: uppercase;
    margin-top: 0.5rem !important;
}
.ink-header::after {
    content: '';
    display: block;
    width: 60px; height: 2px;
    background: linear-gradient(90deg, transparent, #c9a84c, transparent);
    margin: 1.2rem auto 0;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'Cinzel', serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em;
    color: #c9a84c !important;
    text-transform: uppercase;
    margin-bottom: 1.5rem !important;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.section-title::after {
    content: '';
    flex: 1; height: 1px;
    background: linear-gradient(90deg, #c9a84c44, transparent);
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
    background: #1a1a1a !important;
    border: 1px solid #2e2820 !important;
    border-radius: 3px !important;
    color: #e8e0d5 !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.3s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 1px #c9a84c33 !important;
    outline: none !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stNumberInput"] label {
    color: #8a7d6a !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 500 !important;
}

/* ── BOTONES ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1e1a14 0%, #2a2218 100%) !important;
    border: 1px solid #c9a84c !important;
    color: #c9a84c !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.2em;
    font-weight: 700 !important;
    padding: 0.7rem 2rem !important;
    border-radius: 2px !important;
    text-transform: uppercase;
    transition: all 0.3s ease !important;
    width: 100%;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #c9a84c 0%, #f0d080 100%) !important;
    color: #0d0d0d !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── BOTÓN DOWNLOAD ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #c9a84c 0%, #8b6914 100%) !important;
    border: none !important;
    color: #0d0d0d !important;
    font-family: 'Cinzel', serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.2em;
    font-weight: 700 !important;
    padding: 0.8rem 2rem !important;
    border-radius: 2px !important;
    width: 100%;
    transition: all 0.3s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    box-shadow: 0 6px 25px rgba(201,168,76,0.4) !important;
    transform: translateY(-2px) !important;
}

/* ── MÉTRICA ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1a1508 0%, #0f0d06 100%) !important;
    border: 1px solid #c9a84c55 !important;
    border-radius: 4px !important;
    padding: 1.5rem !important;
}
[data-testid="stMetricValue"] {
    color: #c9a84c !important;
    font-family: 'Cinzel', serif !important;
    font-size: 2.5rem !important;
}
[data-testid="stMetricLabel"] {
    color: #8a7d6a !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em;
}

/* ── TARJETA CLIENTE ── */
.client-card {
    background: linear-gradient(135deg, #131310 0%, #0f0f0d 100%);
    border: 1px solid #2e2820;
    border-radius: 4px;
    padding: 1.8rem;
    margin: 1rem 0;
    position: relative;
}
.client-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #c9a84c, #8b6914);
    border-radius: 4px 0 0 4px;
}
.client-card-name {
    font-family: 'Cinzel', serif;
    font-size: 1.4rem;
    color: #c9a84c;
    margin-bottom: 0.6rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}
.client-card-info {
    font-size: 0.85rem;
    color: #8a7d6a;
    margin: 0.25rem 0;
    letter-spacing: 0.05em;
}
.client-card-info span { color: #e8e0d5; }

/* ── VIP BADGE ── */
.vip-badge {
    background: linear-gradient(135deg, #c9a84c, #8b6914);
    color: #0d0d0d;
    font-family: 'Cinzel', serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    padding: 0.3rem 0.9rem;
    border-radius: 2px;
}

/* ── HISTORIAL ITEMS ── */
.historial-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.9rem 1.2rem;
    margin: 0.4rem 0;
    background: #111111;
    border-left: 2px solid #2e2820;
    border-radius: 0 3px 3px 0;
    transition: border-color 0.3s;
}
.historial-item:hover { border-left-color: #c9a84c; }
.historial-fecha { font-size: 0.72rem; color: #5a5248; letter-spacing: 0.08em; }
.historial-servicio { font-size: 0.9rem; color: #e8e0d5; }
.historial-precio {
    font-family: 'Cinzel', serif;
    color: #c9a84c;
    font-size: 0.95rem;
    font-weight: 700;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0 !important;
    border-bottom: 1px solid #2e2820 !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'Cinzel', serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.15em !important;
    color: #5a5248 !important;
    padding: 0.8rem 2rem !important;
    border: none !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #c9a84c !important;
    border-bottom: 2px solid #c9a84c !important;
}
[data-testid="stTabs"] [role="tab"]:hover { color: #e8e0d5 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d0d0d; }
::-webkit-scrollbar-thumb { background: #2e2820; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c9a84c; }
</style>
""", unsafe_allow_html=True)


# ── BASE DE DATOS ─────────────────────────────────────────────────────────────
def asegurar_tablas_existen():
    con = sqlite3.connect("tatuajes.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL, cedula TEXT NOT NULL UNIQUE,
        telefono TEXT, notas_medicas TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS facturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula_cliente TEXT NOT NULL, servicio TEXT NOT NULL,
        precio REAL NOT NULL, fecha TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    con.commit(); con.close()

asegurar_tablas_existen()


# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ink-header">
    <h1>INK STUDIO</h1>
    <p>Sistema Profesional de Gestión</p>
</div>
""", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "✦  Nuevo Cliente",
    "✦  Facturación",
    "✦  Historial & Fidelidad",
])


# ╔═══════════════════════════╗
# ║    TAB 1 — NUEVO CLIENTE ║
# ╚═══════════════════════════╝
with tab1:
    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✦ Registrar Nuevo Cliente</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        nombre   = st.text_input("Nombre completo")
        cedula   = st.text_input("Cédula / Documento")
    with col2:
        telefono = st.text_input("Teléfono de contacto")
        notas    = st.text_area("Notas médicas / Alergias", height=122)

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    if st.button("Guardar Cliente", key="btn_guardar"):
        if nombre and cedula:
            try:
                con = sqlite3.connect("tatuajes.db")
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO clientes (nombre, cedula, telefono, notas_medicas) VALUES (?, ?, ?, ?)",
                    (nombre, cedula, telefono, notas)
                )
                con.commit(); con.close()
                st.success(f"✅  Cliente **{nombre}** registrado con éxito.")
            except sqlite3.IntegrityError:
                st.error("⚠️  Esta cédula ya está registrada en el sistema.")
        else:
            st.error("❌  Nombre y Cédula son obligatorios.")


# ╔═══════════════════════════╗
# ║    TAB 2 — FACTURACIÓN   ║
# ╚═══════════════════════════╝
with tab2:
    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✦ Generar Factura de Servicio</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        cedula_f   = st.text_input("Cédula del cliente a facturar")
        servicio   = st.text_input("Descripción del servicio")
    with col2:
        precio     = st.number_input("Precio del servicio ($)", min_value=0.0, step=10000.0)
        st.markdown('<div style="height:1.45rem"></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    if st.button("Generar Factura PDF", key="btn_factura"):
        if not cedula_f or not servicio or precio == 0:
            st.error("❌  Completa todos los campos antes de generar la factura.")
        else:
            con = sqlite3.connect("tatuajes.db")
            cur = con.cursor()
            cur.execute("SELECT nombre, telefono FROM clientes WHERE cedula = ?", (cedula_f,))
            cliente = cur.fetchone()
            con.close()

            if not cliente:
                st.error("❌  Cédula no encontrada. Registra al cliente primero en **Nuevo Cliente**.")
            else:
                nombre_c, tel_c = cliente
                try:
                    con = sqlite3.connect("tatuajes.db")
                    cur = con.cursor()
                    cur.execute(
                        "INSERT INTO facturas (cedula_cliente, servicio, precio) VALUES (?, ?, ?)",
                        (cedula_f, servicio, precio)
                    )
                    con.commit(); con.close()
                except sqlite3.Error as e:
                    st.error(f"Error al guardar en BD: {e}"); st.stop()

                try:
                    pdf_bytes = bytes(generar_pdf_factura(nombre_c, cedula_f, tel_c, servicio, precio))
                    st.success(f"✅  Visita registrada para **{nombre_c}**. Descarga tu factura:")
                    st.download_button(
                        label="⬇  Descargar Factura PDF",
                        data=pdf_bytes,
                        file_name=f"factura_{cedula_f}.pdf",
                        mime="application/pdf",
                    )
                except Exception as e:
                    st.error(f"Error al generar PDF: {e}")


# ╔═══════════════════════════════╗
# ║  TAB 3 — HISTORIAL FIDELIDAD ║
# ╚═══════════════════════════════╝
with tab3:
    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✦ Consultar Historial del Cliente</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        cedula_b = st.text_input("Cédula del cliente a consultar")
    with col2:
        st.markdown('<div style="height:1.55rem"></div>', unsafe_allow_html=True)
        buscar = st.button("Buscar", key="btn_buscar")

    if buscar:
        if not cedula_b:
            st.warning("⚠️  Ingresa una cédula para buscar.")
        else:
            con = sqlite3.connect("tatuajes.db")
            cur = con.cursor()
            cur.execute("SELECT nombre, telefono, notas_medicas FROM clientes WHERE cedula = ?", (cedula_b,))
            cliente = cur.fetchone()

            if cliente:
                cur.execute("SELECT COUNT(*) FROM facturas WHERE cedula_cliente = ?", (cedula_b,))
                total = cur.fetchone()[0]
                cur.execute(
                    "SELECT servicio, precio, fecha FROM facturas WHERE cedula_cliente = ? ORDER BY fecha DESC",
                    (cedula_b,)
                )
                historial = cur.fetchall()
                con.close()

                vip = '<span class="vip-badge">★ VIP</span>' if total >= 5 else ''
                st.markdown(f"""
                <div class="client-card">
                    <div class="client-card-name">{cliente[0]} {vip}</div>
                    <div class="client-card-info">📞 Teléfono: <span>{cliente[1] or 'N/A'}</span></div>
                    <div class="client-card-info">🩺 Notas médicas: <span>{cliente[2] or 'Ninguna'}</span></div>
                </div>
                """, unsafe_allow_html=True)

                col_m, _ = st.columns([1, 2])
                with col_m:
                    st.metric("✨ Visitas al Estudio", f"{total}")

                if total >= 5:
                    st.balloons()
                    st.success("🏆  ¡Cliente VIP! Considera ofrecerle un descuento especial.")

                if historial:
                    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">✦ Detalle de Visitas</div>', unsafe_allow_html=True)
                    for srv, prec, fecha in historial:
                        st.markdown(f"""
                        <div class="historial-item">
                            <div>
                                <div class="historial-fecha">{fecha[:10] if fecha else '—'}</div>
                                <div class="historial-servicio">{srv}</div>
                            </div>
                            <div class="historial-precio">${prec:,.0f}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Este cliente aún no tiene visitas registradas.")
            else:
                con.close()
                st.warning("🔍  No existe ningún cliente con esa cédula.")


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:4rem; padding:2rem 0 1rem;">
    <div style="width:40px;height:1px;background:linear-gradient(90deg,transparent,#c9a84c,transparent);margin:0 auto 1rem;"></div>
    <p style="color:#2e2820;font-size:0.7rem;letter-spacing:0.3em;text-transform:uppercase;">
        Ink Studio Pro · Sistema de Gestión
    </p>
</div>
""", unsafe_allow_html=True)