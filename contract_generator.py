import openai
from config import OPENAI_KEY

openai.api_key = OPENAI_KEY


def gerar(tipo):

    prompt = f"""
Crie um contrato jurídico brasileiro completo e profissional.

Tipo do contrato:
{tipo}

O contrato deve conter:

- identificação das partes
- objeto
- obrigações
- prazos
- penalidades
- rescisão
- foro

Formato profissional jurídico.
"""

    resposta = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Advogado especialista brasileiro"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return resposta["choices"][0]["message"]["content"]