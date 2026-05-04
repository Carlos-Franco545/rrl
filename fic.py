from flask import Flask, request,render_template, send_file
from pdfrw import PdfReader, PdfWriter, PdfDict
import io

app = Flask(__name__)

PDF_TEMPLATE = "ficha.pdf" # tu PDF base

@app.route("/")
def index():
    return render_template("ficha.html")

@app.route('/generar', methods=['POST'])
def llenar_pdf():


    data = request.form
    pdf = PdfReader(PDF_TEMPLATE)

    # Rellenar campos
    for page in pdf.pages:
        if page.Annots:
            for field in page.Annots:
                if field.T:
                    key = field.T[1:-1]  # quitar paréntesis

                    if key in data:
                        field.update(PdfDict(V=str(data.get(key))))

    # 🔥 IMPORTANTE: hacer visibles los datos
    if pdf.Root.AcroForm:
        pdf.Root.AcroForm.update(PdfDict(NeedAppearances=True))

    # Guardar en memoria (NO en archivo)
    buffer = io.BytesIO()
    PdfWriter().write(buffer, pdf)
    buffer.seek(0)

    # Nombre dinámico (opcional)
    nombre = data.get("Alumno", "ficha")
    filename = f"{nombre}.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )