import openai
from config import OPENAI_KEY

openai.api_key = OPENAI_KEY


def gerar(descricao):

    prompt = f"""
Crie um acordo jurídico estratégico profissional brasileiro.

Situação:
{descricao}

Estruture:

- identificação das partes
- contexto do conflito
- proposta estratégica
- cláusulas de segurança jurídica
- penalidades
- prazos
- cláusula de confidencialidade
- foro

Estilo firme e estratégico semelhante ao advogado Harvey Specter.
"""

    resposta = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Advogado especialista estratégico"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return resposta["choices"][0]["message"]["content"]