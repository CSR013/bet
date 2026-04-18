import re
from pdf_analyzer import extrair_texto_pdf

def extrair_dados(caminho):

    texto=extrair_texto_pdf(caminho)

    nomes=re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+',texto)

    cpf=re.findall(r'\d{3}\.\d{3}\.\d{3}-\d{2}',texto)

    cnpj=re.findall(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}',texto)

    valores=re.findall(r'R\$\s?\d+[.,]?\d*',texto)

    return {

"nomes":nomes,

"cpf":cpf,

"cnpj":cnpj,

"valores":valores
}