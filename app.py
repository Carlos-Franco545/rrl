from flask import Flask, render_template, request, send_file
from pdfrw import PdfReader, PdfWriter, PdfDict

app = Flask(__name__)
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

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/formulario")
def formulario1():
    return render_template("formulario.html")


@app.route("/tecnologias")
def formulario2():
    return render_template("tecnologias.html")


@app.route("/formulario3")
def formulario3():
    return render_template("formulario3.html")

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

                    campo = annotation.T[1:-1]

                    if campo in data:

                        valor = str(data[campo])

                        if "FECHA" in campo.upper() or "NACIMIENTO" in campo.upper():
                            valor = formato_fecha(valor)

                        annotation.update(PdfDict(V=valor))

                    # checkbox genero
                    if campo == "generoHAlu":
                        marcar_checkbox(annotation, data.get("generoAlu") == "H")

                    if campo == "generoMAlu":
                        marcar_checkbox(annotation, data.get("generoAlu") == "M")

    output = "registro.pdf"
    PdfWriter().write(output, pdf)

    return send_file(output, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
