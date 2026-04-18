import openai
from config import OPENAI_KEY

openai.api_key = OPENAI_KEY


def detectar(texto):

    prompt = f"""
Analise o contrato abaixo e identifique cláusulas abusivas segundo o direito brasileiro.

Contrato:
{texto}

Responder:

- cláusulas abusivas encontradas
- riscos jurídicos
- sugestões de correção
- score de segurança jurídica (0 a 100)
"""

    resposta = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Advogado especialista em revisão contratual"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return resposta["choices"][0]["message"]["content"]