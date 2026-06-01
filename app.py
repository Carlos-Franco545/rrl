from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
import os

app = Flask(__name__)

# --- CONFIGURACIÓN DE PLANTILLAS PDF ---
# Asegúrate de que estos archivos estén en la raíz de tu proyecto junto a app.py
PDF_CEDULA = "CEDULA_REGISTRO_ALUMNO.pdf"
PDF_FICHA = "FICHA_INSCRIPCION.pdf"
PDF_TECNOLOGIA = "Seleccion_tecnologia.pdf"
PDF_AUTORIZACION = "AUTORIZACION_USO_IMAGEN.pdf"

def formato_fecha(fecha_iso):
    """Convierte fechas de formato HTML (YYYY-MM-DD) a formato escolar (DD/MM/YYYY)."""
    if not fecha_iso:
        return ""
    try:
        partes = fecha_iso.split("-")
        if len(partes) == 3:
            year, month, day = partes
            return f"{day}/{month}/{year}"
    except:
        pass
    return fecha_iso

# --- RUTAS PARA MOSTRAR LAS PÁGINAS (HTML) ---

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/formulario")
def formulario1():
    return render_template("formulario.html")

@app.route("/tecnologias")
def formulario2():
    return render_template("tecnologias.html")

@app.route("/ficha")
def formulario3():
    return render_template("ficha.html")

@app.route("/autorizacion")
def formulario4():
    return render_template("autorizacion.html")


# --- PROCESADORES DE FORMULARIOS (POST) ---

@app.route("/generar_cedula", methods=["POST"])
def generar_cedula():
    data = request.form.to_dict()
    
    # Formatear campos de fecha si vienen en el formulario
    if "fecha2" in data:
        data["fecha2"] = formato_fecha(data["fecha2"])
    if "fechaNacAlu" in data:
        data["fechaNacAlu"] = formato_fecha(data["fechaNacAlu"])
    if "fechaNacPadre" in data:
        data["fechaNacPadre"] = formato_fecha(data["fechaNacPadre"])
    if "fechaNacMadre" in data:
        data["fechaNacMadre"] = formato_fecha(data["fechaNacMadre"])
    if "fechaNacTutor" in data:
        data["fechaNacTutor"] = formato_fecha(data["fechaNacTutor"])

    # Manejo manual para Checkboxes de Género en el PDF basado en el Radio de HTML
    # Nota: Ajusta 'generoHombre' y 'generoMujer' por los nombres internos reales de tu PDF
    if data.get("generoHAlu") == "H":
        data["generoHombre"] = "/Yes"
        data["generoMujer"] = "/Off"
    elif data.get("generoHAlu") == "M":
        data["generoHombre"] = "/Off"
        data["generoMujer"] = "/Yes"

    output = "cedula_registro_final.pdf"
    
    reader = PdfReader(PDF_CEDULA)
    writer = PdfWriter()
    writer.append(reader)

    # Rellenar todas las páginas del PDF de forma nativa
    for page in writer.pages:
        writer.update_page_form_field_values(page, data)

    with open(output, "wb") as output_stream:
        writer.write(output_stream)

    return send_file(output, as_attachment=True)


@app.route("/generar", methods=["POST"])
def generar_ficha():
    data = request.form.to_dict()

    # Corrección de parches lógicos debido a los valores del HTML de la ficha:
    # 1. Apoyo Psicológico envía 'Caminando' para SÍ y 'Transporte' para NO
    if data.get("psico") == "Caminando":
        data["psico"] = "Si"
    elif data.get("psico") == "Transporte":
        data["psico"] = "No"

    # 2. El campo 'sindorme' (typo de tu HTML) también envía 'Caminando'/'Transporte'
    if data.get("sindorme") == "Caminando":
        data["sindorme"] = "Si"
    elif data.get("sindorme") == "Transporte":
        data["sindorme"] = "No"

    output = "ficha_inscripcion_final.pdf"
    
    reader = PdfReader(PDF_FICHA)
    writer = PdfWriter()
    writer.append(reader)

    for page in writer.pages:
        writer.update_page_form_field_values(page, data)

    with open(output, "wb") as output_stream:
        writer.write(output_stream)

    return send_file(output, as_attachment=True)


@app.route("/generar_tecnologia", methods=["POST"])
def generar_tecnologia():
    data = request.form.to_dict()
    output = "seleccion_tecnologia_final.pdf"
    
    reader = PdfReader(PDF_TECNOLOGIA)
    writer = PdfWriter()
    writer.append(reader)

    # pypdf mapea de forma directa las llaves del HTML (tecnologia1, tecnologia2, Alumno, etc.)
    for page in writer.pages:
        writer.update_page_form_field_values(page, data)

    with open(output, "wb") as output_stream:
        writer.write(output_stream)

    return send_file(output, as_attachment=True)


@app.route("/generar_autorizacion", methods=["POST"])
def generar_autorizacion():
    # Ojo: Requiere que hayas corregido los name="" vacíos en tu archivo autorizacion.html
    # de acuerdo a la propuesta previa (tutor, Alumno, grado, grupo, lugarFecha, telContacto, firmaTutor)
    data = request.form.to_dict()
    output = "autorizacion_imagen_final.pdf"
    
    reader = PdfReader(PDF_AUTORIZACION)
    writer = PdfWriter()
    writer.append(reader)

    for page in writer.pages:
        writer.update_page_form_field_values(page, data)

    with open(output, "wb") as output_stream:
        writer.write(output_stream)

    return send_file(output, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)