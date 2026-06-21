"""
Script principal: orquestra todo o fluxo de publicação automática.

Fluxo:
  1. Sorteia um tema não publicado da planilha
  2. Gera o roteiro (título, tópicos, prompt de imagem, legenda) via GPT
  3. Gera a imagem do infográfico via GPT Image Mini
  4. Salva a imagem em imagens/ (será comitada pelo workflow do GitHub Actions)
  5. Publica no Instagram (feed), usando a URL "raw" do GitHub para a imagem
  6. Publica a mesma imagem também como Story (best effort — não bloqueia o
     restante do fluxo se falhar)
  7. Marca o tema como Publicado=True na planilha

Importante: o commit da imagem + planilha de volta ao repositório é feito
pelo workflow do GitHub Actions (não por este script), pois a imagem precisa
estar no repositório ANTES de a URL raw.githubusercontent.com ficar acessível.
Por isso este script é dividido em duas etapas, controladas pelo workflow:
  - etapa "gerar": sorteia tema, gera roteiro e imagem, salva tudo localmente
  - etapa "publicar": depois do commit/push, publica no Instagram e marca a planilha
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.planilha import sortear_tema, marcar_como_publicado
from src.roteiro import gerar_roteiro
from src.imagem import gerar_imagem
from src.instagram import publicar_no_instagram, publicar_story_no_instagram

CAMINHO_PLANILHA = "data/temas.xlsx"
PASTA_IMAGENS = "imagens"
ARQUIVO_ESTADO = "estado_execucao.json"

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")
GITHUB_BRANCH = os.environ.get("GITHUB_REF_NAME", "main")


def etapa_gerar():
    tema_escolhido = sortear_tema(CAMINHO_PLANILHA)
    print(f"Tema sorteado: {tema_escolhido['tema']} (linha {tema_escolhido['row']})")

    roteiro = gerar_roteiro(tema_escolhido["tema"], tema_escolhido["categoria"])
    print(f"Roteiro gerado: {roteiro['titulo']}")

    nome_arquivo = f"infografico_{tema_escolhido['id']}.png"
    caminho_imagem = os.path.join(PASTA_IMAGENS, nome_arquivo)
    gerar_imagem(roteiro["prompt_imagem"], caminho_imagem)
    print(f"Imagem salva em {caminho_imagem}")

    estado = {
        "row": tema_escolhido["row"],
        "caminho_imagem": caminho_imagem,
        "legenda": roteiro["legenda_instagram"],
    }
    with open(ARQUIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)

    print("Etapa 'gerar' concluída. Pronto para commit/push da imagem.")


def etapa_publicar():
    with open(ARQUIVO_ESTADO, "r", encoding="utf-8") as f:
        estado = json.load(f)

    if not GITHUB_REPOSITORY:
        raise RuntimeError(
            "Variável de ambiente GITHUB_REPOSITORY não encontrada. "
            "Esta etapa deve rodar dentro do GitHub Actions."
        )

    image_url = (
        f"https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/"
        f"{GITHUB_BRANCH}/{estado['caminho_imagem']}"
    )
    print(f"URL pública da imagem: {image_url}")

    media_id = publicar_no_instagram(image_url, estado["legenda"])
    print(f"Publicado no feed com sucesso. media_id={media_id}")

    # A publicação do Story é "best effort": se falhar por qualquer motivo
    # (instabilidade da API, etc.), não deve impedir o restante do fluxo,
    # já que o post no feed (a parte principal) já foi concluído com sucesso.
    try:
        story_id = publicar_story_no_instagram(image_url)
        print(f"Publicado também como Story. story_id={story_id}")
    except Exception as e:
        print(f"Aviso: falha ao publicar Story (feed não foi afetado). Erro: {e}")

    marcar_como_publicado(CAMINHO_PLANILHA, estado["row"])
    print("Planilha atualizada (Publicado=True).")

    os.remove(ARQUIVO_ESTADO)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("gerar", "publicar"):
        print("Uso: python src/main.py [gerar|publicar]")
        sys.exit(1)

    if sys.argv[1] == "gerar":
        etapa_gerar()
    else:
        etapa_publicar()
