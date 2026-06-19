"""
Renova o IG_ACCESS_TOKEN antes que ele expire (tokens duram 60 dias) e atualiza
automaticamente o Secret correspondente no repositório GitHub via API do GitHub.

Pensado para rodar em um workflow agendado (ex: a cada 45 dias), separado do
workflow de publicação. Precisa de um GITHUB_TOKEN com permissão de escrita em
Secrets (permissions: secrets: write) ou um PAT (Personal Access Token) com
escopo 'repo' guardado em um Secret próprio (ex: GH_PAT_PARA_SECRETS).
"""
import base64
import os
import sys

import requests
from nacl import encoding, public

from instagram import renovar_token

GITHUB_API_BASE = "https://api.github.com"


def _criptografar_secret(valor_publico_b64: str, valor_secreto: str) -> str:
    """Criptografa um valor usando a chave pública do repositório (libsodium/NaCl),
    conforme exigido pela API de Secrets do GitHub."""
    chave_publica = public.PublicKey(valor_publico_b64.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(chave_publica)
    criptografado = sealed_box.encrypt(valor_secreto.encode("utf-8"))
    return base64.b64encode(criptografado).decode("utf-8")


def atualizar_secret_no_github(repo: str, nome_secret: str, valor: str, github_token: str) -> None:
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
    }

    chave_resp = requests.get(
        f"{GITHUB_API_BASE}/repos/{repo}/actions/secrets/public-key",
        headers=headers,
        timeout=30,
    )
    chave_resp.raise_for_status()
    chave_publica_b64 = chave_resp.json()["key"]
    key_id = chave_resp.json()["key_id"]

    valor_criptografado = _criptografar_secret(chave_publica_b64, valor)

    put_resp = requests.put(
        f"{GITHUB_API_BASE}/repos/{repo}/actions/secrets/{nome_secret}",
        headers=headers,
        json={"encrypted_value": valor_criptografado, "key_id": key_id},
        timeout=30,
    )
    put_resp.raise_for_status()


def main():
    token_atual = os.environ["IG_ACCESS_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    github_token = os.environ["GH_PAT_PARA_SECRETS"]

    print("Renovando token do Instagram...")
    resultado = renovar_token(token_atual)
    novo_token = resultado["access_token"]
    expires_in_dias = resultado.get("expires_in", 0) / 86400
    print(f"Novo token obtido. Válido por aproximadamente {expires_in_dias:.0f} dias.")

    print(f"Atualizando o Secret IG_ACCESS_TOKEN no repositório {repo}...")
    atualizar_secret_no_github(repo, "IG_ACCESS_TOKEN", novo_token, github_token)
    print("Secret IG_ACCESS_TOKEN atualizado com sucesso.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERRO ao renovar o token: {e}", file=sys.stderr)
        sys.exit(1)
