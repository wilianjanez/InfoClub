"""
Geração da imagem do infográfico usando o modelo GPT Image 1 Mini (OpenAI).
Formato retrato (1024x1536), compatível com o range de aspect ratio aceito
pelo Instagram para posts de feed (1.91:1 a 4:5 / 3:4) — evita cortes na exibição.
"""
import base64
import os
from openai import OpenAI

MODELO_IMAGEM = "gpt-image-1-mini"
TAMANHO = "1024x1536"  # retrato — formato recomendado para feed do Instagram em 2026
QUALIDADE = "high"  # low | medium | high — high prioriza legibilidade de texto, custo maior


def gerar_imagem(prompt_imagem: str, caminho_saida: str) -> str:
    """
    Gera a imagem a partir do prompt e salva em caminho_saida (PNG).
    Retorna o caminho do arquivo salvo.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    response = client.images.generate(
        model=MODELO_IMAGEM,
        prompt=prompt_imagem,
        size=TAMANHO,
        quality=QUALIDADE,
        n=1,
    )

    imagem_b64 = response.data[0].b64_json
    imagem_bytes = base64.b64decode(imagem_b64)

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    with open(caminho_saida, "wb") as f:
        f.write(imagem_bytes)

    return caminho_saida
