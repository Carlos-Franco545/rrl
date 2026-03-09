from flask import Flask, render_template, request, send_file
from pdfrw import PdfReader, PdfWriter, PdfDict

app = Flask(__name__)

PDF_TEMPLATE = "Seleccion_tecnologia.pdf"


@app.route("/")
def index():
    return render_template("tecnologias.html")


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
                        annotation.update(
                            PdfDict(V='{}'.format(valor))
                        )

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