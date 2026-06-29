from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject 
import os

app = Flask(__name__)

PDF_CEDULA = "CEDULA_REGISTRO_ALUMNO.pdf"
PDF_FICHA = "FICHA_INSCRIPCION.pdf"
PDF_TECNOLOGIA = "Seleccion_tecnologia.pdf"
PDF_AUTORIZACION = "AUTORIZACION_USO_IMAGEN.pdf"

PDF_TEC = "Seleccion_de_Tecnologias(blanco).pdf"
PDF_FIC = "ficha inscripcion(blanco).pdf"
PDF_AUT = "AUTORIZACIÓN DE USO DE IMÁGENES(blanco).pdf"

def formato_fecha(fecha_iso):
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

@app.route("/volver")
def volver():
    return render_template("index.html")


# ==========================================
# RUTAS PARA DESCARGAR DOCUMENTOS ORIGINALES
# ==========================================

@app.route("/descargar/cedula")
def descargar_cedula():
    return send_file(PDF_CEDULA, as_attachment=True)

@app.route("/descargar/ficha")
def descargar_ficha():
    return send_file(PDF_FIC, as_attachment=True)

@app.route("/descargar/tecnologia")
def descargar_tecnologia():
    return send_file(PDF_TEC, as_attachment=True)

@app.route("/descargas/autorizacion")
def descargar_autorizacion():
    return send_file(PDF_AUT, as_attachment=True)


# ==========================================
# RUTAS PARA GENERAR DOCUMENTOS RELLENADOS
# ==========================================

@app.route("/generar_cedula", methods=["POST"])
def generar_cedula():
    data = request.form.to_dict()  
    for campo_fecha in ["fecha2", "fechaNacAlu", "fechaNacPadre", "fechaNacMadre", "fechaNacTutor"]:
        if campo_fecha in data:
            data[campo_fecha] = formato_fecha(data[campo_fecha])

    output = "cedula_registro_final.pdf"
    
    reader = PdfReader(PDF_CEDULA)
    writer = PdfWriter()
    writer.append(reader)

    if "/AcroForm" in writer._root_object:
        writer._root_object["/AcroForm"].update({
            NameObject("/NeedAppearances"): BooleanObject(True)
        })

    for page in writer.pages:
        writer.update_page_form_field_values(page, data)

    with open(output, "wb") as output_stream:
        writer.write(output_stream)

    return send_file(output, as_attachment=True)


@app.route("/generar", methods=["POST"])
def generar_ficha():
    data = request.form.to_dict()

    for clave, valor in data.items():
        if isinstance(valor, str) and "&" in valor:
            data[clave] = valor.replace("&", ", ")

    if data.get("psico") == "Caminando":
        data["psico"] = "Si"
    elif data.get("psico") == "Transporte":
        data["psico"] = "No"

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

    for clave, valor in data.items():
        if isinstance(valor, str) and "&" in valor:
            data[clave] = valor.replace("&", ", ")
    
    reader = PdfReader(PDF_TECNOLOGIA)
    writer = PdfWriter()
    writer.append(reader)

    for page in writer.pages:
        writer.update_page_form_field_values(page, data)

    with open(output, "wb") as output_stream:
        writer.write(output_stream)

    return send_file(output, as_attachment=True)

@app.route("/generar_autorizacion", methods=["POST"])
def generar_autorizacion():
    data = request.form.to_dict()
    output = "autorizacion_imagen_final.pdf"

    for clave, valor in data.items():
        if isinstance(valor, str) and "&" in valor:
            data[clave] = valor.replace("&", ", ")
    
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