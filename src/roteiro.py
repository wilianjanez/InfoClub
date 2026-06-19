"""
Geração do roteiro do infográfico e da legenda do post, usando a API da OpenAI (GPT).
"""
import json
import os
from openai import OpenAI

MODELO_TEXTO = "gpt-4o-mini"

SYSTEM_PROMPT = """Você é um diretor de arte e redator especializado em infográficos para redes sociais.
Sua tarefa é transformar um tema em um roteiro estruturado para um infográfico quadrado (1024x1024),
com visual moderno, cores vibrantes mas elegantes, ícones simples e tipografia limpa — estilo que
agrade tanto adolescentes quanto adultos e idosos (clareza acima de tudo, nada poluído).

Responda APENAS em JSON válido, sem markdown, sem texto fora do JSON, no formato exato:
{
  "titulo": "título curto e impactante em português, max 6 palavras",
  "topicos": ["tópico 1 curto", "tópico 2 curto", "tópico 3 curto", "tópico 4 curto (opcional)"],
  "prompt_imagem": "prompt detalhado em inglês para um gerador de imagens, descrevendo um infográfico moderno, flat design, com o título e os tópicos EXATOS escritos na imagem, cores e composição",
  "legenda_instagram": "legenda em português do Brasil para o post do Instagram, com 2-3 frases envolventes e 5 hashtags relevantes ao final"
}
"""


def gerar_roteiro(tema: str, categoria: str) -> dict:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    user_prompt = f"Tema: {tema}\nCategoria: {categoria}\n\nGere o roteiro do infográfico conforme o formato especificado."

    response = client.chat.completions.create(
        model=MODELO_TEXTO,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    conteudo = response.choices[0].message.content
    dados = json.loads(conteudo)

    obrigatorios = ["titulo", "topicos", "prompt_imagem", "legenda_instagram"]
    faltando = [campo for campo in obrigatorios if campo not in dados]
    if faltando:
        raise ValueError(f"Resposta do GPT incompleta, faltando: {faltando}")

    return dados
