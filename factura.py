from fpdf import FPDF
from datetime import datetime

class PDF_Factura(FPDF):
    def header(self):
        # Configurar fuente para el título del negocio
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 10, "ESTUDIO DE TATUAJES", ln=True, align="C")
        
        # Subtítulo o eslogan
        self.set_font("Helvetica", "I", 10)
        self.cell(0, 5, "Arte y Precisión en tu Piel", ln=True, align="C")
        
        # Línea de separación
        self.ln(10)
        self.line(10, 30, 200, 30)

    def footer(self):
        # Posición a 1.5 cm del final de la página
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def generar_pdf_factura(nombre, cedula, telefono, servicio, precio):
    pdf = PDF_Factura()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # Datos de la factura
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Fecha: {fecha_actual}", ln=True)
    pdf.ln(5)
    
    # Cuadro de información del cliente
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "DATOS DEL CLIENTE", ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 8, f"Nombre: {nombre}", ln=True)
    pdf.cell(0, 8, f"Cédula: {cedula}", ln=True)
    pdf.cell(0, 8, f"Teléfono: {telefono}", ln=True)
    
    pdf.ln(10)
    
    # Detalle del Servicio (Tabla simple)
    pdf.set_font("Helvetica", "B", 12)
    # Encabezados de columna
    pdf.cell(130, 10, "Descripción del Servicio", border=1, align="L")
    pdf.cell(60, 10, "Total", border=1, align="C", ln=True)
    
    # Contenido del servicio
    pdf.set_font("Helvetica", size=12)
    pdf.cell(130, 15, f"Tatuaje / Servicio: {servicio}", border=1, align="L")
    pdf.cell(60, 15, f"${precio:,.2f}", border=1, align="C", ln=True)
    
    pdf.ln(15)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "¡Gracias por confiar en nuestro arte!", align="C")
    
    # Retorna el PDF convertido en bytes (datos puros) para que Streamlit lo pueda descargar
    return pdf.output()