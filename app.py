from flask import Flask, render_template, request, send_file
from pdfrw import PdfReader, PdfWriter, PdfDict

app = Flask(__name__)

# Definimos las plantillas de PDF para cada caso
PDF_CEDULA = "CEDULA_REGISTRO_ALUMNO.pdf"
PDF_FICHA = "FICHA_INSCRIPCION.pdf"
PDF_TECNOLOGIA = "Seleccion_tecnologia.pdf"
PDF_AUTORIZACION = "AUTORIZACION_USO_IMAGEN.pdf"

def formato_fecha(fecha_iso):
    """Convierte fechas de formato YYYY-MM-DD a DD/MM/YYYY."""
    try:
        partes = fecha_iso.split("-")
        if len(partes) == 3:
            year, month, day = partes
            return f"{day}/{month}/{year}"
    except:
        pass
    return fecha_iso

def marcar_checkbox(annotation, condicion):
    """Marca o desmarca un checkbox en el PDF según una condición lógica."""
    if condicion:
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
    # Corregido: apuntaba a tecnologias.html pero tu archivo se llama tecnologia.html
    return render_template("tecnologia.html")

@app.route("/ficha")
def formulario3():
    return render_template("ficha.html")

@app.route("/autorizacion")
def formulario4():
    return render_template("autorizacion.html")


# --- PROGRAMA 1: CÉDULA DE REGISTRO ALUMNO ---

@app.route("/generar_cedula", methods=["POST"])
def generar_cedula():
    data = request.form
    pdf = PdfReader(PDF_CEDULA)

    for page in pdf.pages:
        annotations = page.get('/Annots')
        if annotations:
            for annotation in annotations:
                if annotation.Subtype == '/Widget' and annotation.T:
                    # Extraer nombre del campo en el PDF
                    campo = annotation.T[1:-1]

                    # 1. Llenado automático de campos de texto estándar
                    if campo in data:
                        valor = str(data[campo])
                        if "FECHA" in campo.upper() or "NACIMIENTO" in campo.upper():
                            valor = formato_fecha(valor)
                        annotation.update(PdfDict(V=valor))

                    # 2. Checkboxes de Género (Basados en el name="generoHAlu" del HTML)
                    # Nota: Asume que en el PDF los campos se llaman 'generoHombre' y 'generoMujer'
                    if campo == "generoHombre":
                        marcar_checkbox(annotation, data.get("generoHAlu") == "H")
                    if campo == "generoMujer":
                        marcar_checkbox(annotation, data.get("generoHAlu") == "M")

                    # 3. Checkboxes de Convivencia con el Padre
                    if campo == "viveConPadreSi":
                        marcar_checkbox(annotation, data.get("vivePadre") == "X" and "Si" in annotation.get('/TR', ''))
                    
    # Forzar renderizado visual de campos
    if not pdf.Root.AcroForm:
        pdf.Root.AcroForm = PdfDict()
    pdf.Root.AcroForm.update(PdfDict(NeedAppearances=True))

    output = "cedula_registro_final.pdf"
    PdfWriter().write(output, pdf)
    return send_file(output, as_attachment=True)


# --- PROGRAMA 2: FICHA DE INSCRIPCIÓN ---

@app.route("/generar", methods=["POST"])
def generar_ficha():
    data = request.form
    pdf = PdfReader(PDF_FICHA)

    for page in pdf.pages:
        annotations = page.get('/Annots')
        if annotations:
            for annotation in annotations:
                if annotation.Subtype == '/Widget' and annotation.T:
                    campo = annotation.T[1:-1]

                    # 1. Campos de texto estándar (Alumno, curpAlu, grado, etc.)
                    if campo in data:
                        valor = str(data[campo])
                        annotation.update(PdfDict(V=valor))

                    # 2. Manejo de Radios estándar (Beca, Padres Viven, Separados, Lengua, etc.)
                    # Mapea directamente los valores 'si' / 'no' enviados desde el HTML
                    if campo in ["beca", "padresViven", "separados", "lengua", "medicamento", "cardiaca", "asma", "api", "dis", "compu", "internet", "EduEs", "trab", "zurdo", "netZur"]:
                        val_html = data.get(campo)
                        # Condición: si el campo del PDF espera 'Si' o 'No'
                        if "SI" in campo.upper() or val_html == "si":
                            marcar_checkbox(annotation, val_html == "si")

                    # 3. Solución de parches para los botones con valores erróneos en el HTML
                    # Apoyo Psicológico: En tu HTML mandas 'Caminando' para SÍ y 'Transporte' para NO
                    if campo == "psico":
                        marcar_checkbox(annotation, data.get("psico") == "Caminando")
                    
                    # Síndromes/Espectros: Igualmente mandas 'Caminando' para SÍ y 'Transporte' para NO
                    if campo == "sindorme":
                        marcar_checkbox(annotation, data.get("sindorme") == "Caminando")

                    # Traslado Metodo
                    if campo == "loHaceCaminando":
                        marcar_checkbox(annotation, data.get("loHace") == "Caminando")
                    if campo == "loHaceTransporte":
                        marcar_checkbox(annotation, data.get("loHace") == "Transporte")

    if not pdf.Root.AcroForm:
        pdf.Root.AcroForm = PdfDict()
    pdf.Root.AcroForm.update(PdfDict(NeedAppearances=True))

    output = "ficha_inscripcion_final.pdf"
    PdfWriter().write(output, pdf)
    return send_file(output, as_attachment=True)


# --- PROGRAMA 3: SELECCIÓN DE TECNOLOGÍA ---

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

                    # 1. Campos de texto compartidos (Alumno, grado, grupo, tutor, etc.)
                    if campo in data:
                        valor = str(data[campo])
                        annotation.update(PdfDict(V=valor))

                    # 2. Transcripción explícita de opciones seleccionadas
                    # Si el campo del PDF coincide exactamente con el name del select
                    if campo == "tecnologia1":
                        annotation.update(PdfDict(V=str(data.get("tecnologia1", ""))))
                    if campo == "tecnologia2":
                        annotation.update(PdfDict(V=str(data.get("tecnologia2", ""))))

    if not pdf.Root.AcroForm:
        pdf.Root.AcroForm = PdfDict()
    pdf.Root.AcroForm.update(PdfDict(NeedAppearances=True))

    output = "seleccion_tecnologia_final.pdf"
    PdfWriter().write(output, pdf)
    return send_file(output, as_attachment=True)


# --- PROGRAMA 4: AUTORIZACIÓN DE USO DE IMAGEN ---

@app.route("/generar_autorizacion", methods=["POST"])
def generar_autorizacion():
    data = request.form
    pdf = PdfReader(PDF_AUTORIZACION)

    for page in pdf.pages:
        annotations = page.get('/Annots')
        if annotations:
            for annotation in annotations:
                if annotation.Subtype == '/Widget' and annotation.T:
                    campo = annotation.T[1:-1]

                    # Utiliza las variables asignadas en la propuesta de corrección de autorizacion.html
                    # (tutor, Alumno, grado, grupo, lugarFecha, telContacto, firmaTutor)
                    if campo in data:
                        valor = str(data[campo])
                        annotation.update(PdfDict(V=valor))

    if not pdf.Root.AcroForm:
        pdf.Root.AcroForm = PdfDict()
    pdf.Root.AcroForm.update(PdfDict(NeedAppearances=True))

    output = "autorizacion_imagen_final.pdf"
    PdfWriter().write(output, pdf)
    return send_file(output, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)