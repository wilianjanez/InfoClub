"""
Geração da imagem do infográfico usando o modelo GPT Image 1 Mini (OpenAI) — opção econômica.
"""
import base64
import os
from openai import OpenAI

MODELO_IMAGEM = "gpt-image-1-mini"
TAMANHO = "1024x1024"
QUALIDADE = "medium"  # low | medium | high — medium equilibra custo e legibilidade de texto


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
