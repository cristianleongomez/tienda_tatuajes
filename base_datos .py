import sqlite3
import streamlit as st
# Importamos la función que acabamos de crear en el otro archivo
from factura import generar_pdf_factura

# --- CONFIGURACIÓN Y BASE DE DATOS ---
def inicializar_base_datos():
    """Crea la base de datos y la tabla de clientes si no existen."""
    conexion = sqlite3.connect("tatuajes.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cedula TEXT NOT NULL UNIQUE,
            telefono TEXT,
            notas_medicas TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Inicializamos la base de datos al cargar la app
inicializar_base_datos()


# --- INTERFAZ DE STREAMLIT ---
st.title("🎨 Estudio de Tatuajes - Control Interno")

# --- SECCIÓN 1: REGISTRO DE CLIENTES ---
st.header("1. Registrar Nuevo Cliente")

# Usamos un formulario para que no se recargue la página con cada letra que se escribe
with st.form("form_cliente", clear_on_submit=True):
    nombre = st.text_input("Nombre completo del cliente")
    cedula = st.text_input("Número de Cédula / Documento")
    telefono = st.text_input("Teléfono de contacto")
    notas = st.text_area("Notas médicas / Alergias")
    
    boton_guardar = st.form_submit_button("Guardar Cliente")

if boton_guardar:
    if nombre and cedula:
        try:
            conexion = sqlite3.connect("tatuajes.db")
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, cedula, telefono, notas_medicas) VALUES (?, ?, ?, ?)", 
                (nombre, cedula, telefono, notas)
            )
            conexion.commit()
            conexion.close()
            st.success(f"¡Cliente {nombre} registrado con éxito!")
        except sqlite3.IntegrityError:
            st.error("Error: Ya existe un cliente registrado con ese número de cédula.")
    else:
        st.error("El nombre y la cédula son obligatorios.")

st.markdown("---") # Línea divisoria visual


# --- SECCIÓN 2: FACTURACIÓN ---
st.header("2. Generar Factura de Venta")

# Campos necesarios para la factura
servicio_tatuaje = st.text_input("Descripción del tatuaje realizado (Ej: Realismo Manga)")
precio_tatuaje = st.number_input("Precio del servicio ($)", min_value=0.0, step=5000.0)

# Verificación de datos antes de permitir la impresión
# Nota: "nombre" y "cedula" se toman de los inputs de la Sección 1 si se llenan en la misma sesión.
if nombre and cedula and servicio_tatuaje and precio_tatuaje > 0:
    try:
        # Generamos los datos del PDF en memoria
        pdf_bytes = generar_pdf_factura(nombre, cedula, telefono, servicio_tatuaje, precio_tatuaje)
        
        # Botón nativo de Streamlit para descargar archivos
        st.download_button(
            label="📄 Generar e Imprimir Factura (PDF)",
            data=pdf_bytes,
            file_name=f"factura_{cedula}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error al generar el PDF: {e}")
else:
    st.caption("⚠️ Completa los datos del cliente (Sección 1) y del servicio (Sección 2) para habilitar el botón de la factura.")