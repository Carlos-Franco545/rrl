from flask import Flask, render_template, request, send_file
from pdfrw import PdfReader, PdfWriter, PdfDict

app = Flask(__name__)

# Definimos las plantillas de PDF para cada caso
PDF_CEDULA = "CEDULA_REGISTRO_ALUMNO.pdf"
PDF_TECNOLOGIA = "Seleccion_tecnologia.pdf"

def formato_fecha(fecha_iso):
    try:
        partes = fecha_iso.split("-")
        if len(partes) == 3:
            year, month, day = partes
            return f"{day}/{month}/{year}"
    except:
        pass
    return fecha_iso

def marcar_checkbox(annotation, valor):
    if valor:
        annotation.update(PdfDict(V='/Yes'))
    else:
        annotation.update(PdfDict(V='/Off'))

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


# --- PROGRAMA 1: GENERAR CÉDULA DE REGISTRO ALUMNO ---

@app.route("/generar_cedula", methods=["POST"])
def generar_cedula():
    data = request.form
    pdf = PdfReader(PDF_CEDULA)

    for page in pdf.pages:
        annotations = page.get('/Annots')
        if annotations:
            for annotation in annotations:
                if annotation.Subtype == '/Widget' and annotation.T:
                    campo = annotation.T[1:-1]

                    if campo in data:
                        valor = str(data[campo])
                        if "FECHA" in campo.upper() or "NACIMIENTO" in campo.upper():
                            valor = formato_fecha(valor)
                        annotation.update(PdfDict(V=valor))

                    # Checkboxes exclusivos de la Cédula (Género)
                    if campo == "generoHAlu":
                        marcar_checkbox(annotation, data.get("generoAlu") == "H")
                    if campo == "generoMAlu":
                        marcar_checkbox(annotation, data.get("generoAlu") == "M")

    output = "cedula_registro_final.pdf"
    PdfWriter().write(output, pdf)
    return send_file(output, as_attachment=True)


# --- PROGRAMA 2: GENERAR SELECCIÓN DE TECNOLOGÍA ---

@app.route("/generar_tecnologia", methods=["POST"])
def generar_tecnologia():
    data = request.form
    pdf = PdfReader(PDF_TECNOLOGIA)

    for page in pdf.pages:
        annotations = page.get('/Annots')
        if annotations:
            for annotation in annotations:
                if annotation.Subtype == '/Widget' and annotation.T:
                    campo = annotation.T[1:-1]

                    if campo in data:
                        valor = str(data[campo])
                        annotation.update(PdfDict(V='{}'.format(valor)))

                    # Checkboxes exclusivos de Tecnologías
                    if campo == "tecnologia1":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Confeccíon del Vestido e Industria Textil")
                    if campo == "tecnologia1":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Diseño y Creacion Artesanal")
                    if campo == "tecnologia1":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Diseño y Creacíon Prastica")
                    if campo == "tecnologia1":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Circuitos Electricos")
                    if campo == "tecnologia1":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Informática")
                    if campo == "tecnologia1":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Turismo")

                    if campo == "tecnologia2":
                        marcar_checkbox(annotation, data.get("tecnologia2") == "Confeccíon del Vestido e Industria Textil")
                    if campo == "tecnologia2":
                        marcar_checkbox(annotation, data.get("tecnologia2") == "Diseño y Creacion Artesanal")
                    if campo == "tecnologia2":
                        marcar_checkbox(annotation, data.get("tecnologia2") == "Diseño y Creacíon Prastica")
                    if campo == "tecnologia2":
                        marcar_checkbox(annotation, data.get("tecnologia2") == "Circuitos Electricos")
                    if campo == "tecnologia2":
                        marcar_checkbox(annotation, data.get("tecnologia2") == "Informática")
                    if campo == "tecnologia2":
                        marcar_checkbox(annotation, data.get("tecnologia2") == "Turismo")

    output = "seleccion_tecnologia_final.pdf"
    PdfWriter().write(output, pdf)
    return send_file(output, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)