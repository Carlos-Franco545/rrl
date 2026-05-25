from flask import Flask, render_template, request, send_file
from pdfrw import PdfReader, PdfWriter, PdfDict

app = Flask(__name__)

# NOTA: Asegúrate de usar el nombre del PDF que contenga todos los campos (Tecnologías y Datos del Alumno)
PDF_TEMPLATE = "CEDULA_REGISTRO_ALUMNO.pdf"

def formato_fecha(fecha_iso):
    try:
        partes = fecha_iso.split("-")
        if len(partes) == 3:
            year, month, day = partes
            return f"{day}/{month}/{year}"
    except:
        pass
    return fecha_iso

# --- RUTAS DE NAVEGACIÓN ---

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


# --- PROCESAMIENTO DEL FORMULARIO Y PDF ---

@app.route("/generar", methods=["POST"])
def generar():
    data = request.form
    pdf = PdfReader(PDF_TEMPLATE)

    def marcar_checkbox(annotation, valor):
        if valor:
            annotation.update(PdfDict(V='/Yes'))
        else:
            annotation.update(PdfDict(V='/Off'))

    for page in pdf.pages:
        annotations = page.get('/Annots')
        if annotations:
            for annotation in annotations:
                if annotation.Subtype == '/Widget' and annotation.T:
                    # Extraer el nombre del campo del PDF
                    campo = annotation.T[1:-1]

                    # 1. Llenado de campos de texto estándar
                    if campo in data:
                        valor = str(data[campo])
                        
                        # Formatear si es un campo de fecha
                        if "FECHA" in campo.upper() or "NACIMIENTO" in campo.upper():
                            valor = formato_fecha(valor)
                            
                        annotation.update(PdfDict(V=valor))

                    # 2. Checkboxes de Género
                    if campo == "generoHAlu":
                        marcar_checkbox(annotation, data.get("generoAlu") == "H")
                    if campo == "generoMAlu":
                        marcar_checkbox(annotation, data.get("generoAlu") == "M")

                    # 3. Checkboxes de Selección de Tecnología
                    if campo == "tecnologia1_confec":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Confeccíon del Vestido e Industria Textil")
                    if campo == "tecnologia1_disenoA":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Diseño y Creacion Artesanal")
                    if campo == "tecnologia1_disenoP":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Diseño y Creacíon Prastica")
                    if campo == "tecnologia1_circu":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Circuitos Electricos")
                    if campo == "tecnologia1_inf":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Informática")
                    if campo == "tecnologia1_tur":
                        marcar_checkbox(annotation, data.get("tecnologia1") == "Turismo")

    output = "registro.pdf"
    PdfWriter().write(output, pdf)

    return send_file(output, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)