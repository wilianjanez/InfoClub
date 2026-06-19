"""
Publicação no Instagram via Meta Graph API (container -> publish).
A API exige uma URL pública para a imagem — usamos a URL "raw" do GitHub
(o caminho da imagem já comitada no repositório).
"""
import os
import time
import requests

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def publicar_no_instagram(image_url: str, legenda: str) -> str:
    """
    Cria o container de mídia e publica no Instagram.
    Retorna o ID da publicação.
    """
    ig_user_id = os.environ["IG_USER_ID"]
    access_token = os.environ["IG_ACCESS_TOKEN"]

    # Passo 1: criar container
    container_resp = requests.post(
        f"{GRAPH_API_BASE}/{ig_user_id}/media",
        params={
            "image_url": image_url,
            "caption": legenda,
            "access_token": access_token,
        },
        timeout=30,
    )
    container_resp.raise_for_status()
    container_id = container_resp.json()["id"]

    # Pequena espera para garantir que o container processou (imagens são rápidas,
    # mas evitamos publicar antes de o status ficar FINISHED).
    _aguardar_processamento(container_id, access_token)

    # Passo 2: publicar o container
    publish_resp = requests.post(
        f"{GRAPH_API_BASE}/{ig_user_id}/media_publish",
        params={
            "creation_id": container_id,
            "access_token": access_token,
        },
        timeout=30,
    )
    publish_resp.raise_for_status()
    media_id = publish_resp.json()["id"]

    return media_id


def _aguardar_processamento(container_id: str, access_token: str, tentativas: int = 5) -> None:
    for _ in range(tentativas):
        status_resp = requests.get(
            f"{GRAPH_API_BASE}/{container_id}",
            params={"fields": "status_code", "access_token": access_token},
            timeout=30,
        )
        status_resp.raise_for_status()
        status = status_resp.json().get("status_code")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError(f"Container {container_id} falhou no processamento.")
        time.sleep(3)
    # Se não confirmou FINISHED após as tentativas, segue tentando publicar de qualquer forma
    # (imagens normalmente processam em segundos; isso é uma rede de segurança).
