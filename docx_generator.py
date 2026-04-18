from docx import Document

def gerar_docx(texto):

    doc=Document()

    for linha in texto.split("\n"):

        doc.add_paragraph(linha)

    caminho="arquivo.docx"

    doc.save(caminho)

    return caminho