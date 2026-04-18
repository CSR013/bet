import openai
from config import OPENAI_KEY

openai.api_key = OPENAI_KEY


def responder(pergunta):

    prompt = f"""
Você é um advogado brasileiro extremamente estratégico,
com estilo semelhante ao Harvey Specter.

Analise juridicamente com clareza, objetividade e estratégia.

Pergunta:
{pergunta}
"""

    resposta = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Advogado especialista brasileiro"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return resposta["choices"][0]["message"]["content"]