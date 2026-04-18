import pdfplumber

def extrair_texto_pdf(caminho):

    texto=""

    with pdfplumber.open(caminho) as pdf:

        for pagina in pdf.pages:

            texto+=pagina.extract_text()+"\n"

    return texto