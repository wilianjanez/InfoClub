"""
Script isolado para TESTAR se a publicação de Story funciona no fluxo
"Instagram API with Instagram Login" (graph.instagram.com) já configurado.

Não faz parte do pipeline normal do bot — é só para validação manual.
Usa a imagem mais recente já gerada na pasta imagens/ (reaproveitando um post
já publicado no feed) para tentar publicar como Story também.

Uso: python src/testar_story.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.instagram import publicar_story_no_instagram

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")
GITHUB_BRANCH = os.environ.get("GITHUB_REF_NAME", "main")


def encontrar_imagem_mais_recente() -> str:
    pasta_imagens = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "imagens")
    arquivos = [
        f for f in os.listdir(pasta_imagens)
        if f.lower().endswith((".png", ".jpg", ".jpeg")) and f != ".gitkeep"
    ]
    if not arquivos:
        raise RuntimeError("Nenhuma imagem encontrada na pasta imagens/ para testar.")
    arquivos_completos = [os.path.join(pasta_imagens, f) for f in arquivos]
    mais_recente = max(arquivos_completos, key=os.path.getmtime)
    return os.path.basename(mais_recente)


if __name__ == "__main__":
    if not GITHUB_REPOSITORY:
        raise RuntimeError(
            "Variável de ambiente GITHUB_REPOSITORY não encontrada. "
            "Este script deve rodar dentro do GitHub Actions."
        )

    nome_arquivo = encontrar_imagem_mais_recente()
    image_url = f"https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/{GITHUB_BRANCH}/imagens/{nome_arquivo}"
    print(f"Testando publicação de Story com a imagem: {image_url}")

    try:
        media_id = publicar_story_no_instagram(image_url)
        print(f"SUCESSO! Story publicado. media_id={media_id}")
        print("Isso confirma que media_type=STORIES FUNCIONA no fluxo atual.")
    except Exception as e:
        print(f"FALHOU. Erro: {e}")
        print("Isso confirma a limitação documentada pela Meta para este fluxo.")
        raise
