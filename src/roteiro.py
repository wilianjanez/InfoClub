"""
Geração do roteiro do infográfico e da legenda do post, usando a API da OpenAI (GPT).
"""
import json
import os
from openai import OpenAI

MODELO_TEXTO = "gpt-4o-mini"

SYSTEM_PROMPT = """Você é um diretor de arte e redator especializado em infográficos densos e ricos
para redes sociais, no estilo de páginas educativas profissionais (referência: infográficos completos
tipo "Os Benefícios dos Chás", com título forte, subtítulo, texto de abertura, 6 a 8 pontos numerados
com ícone + título curto + descrição de uma linha cada, um bloco de dicas extras, e uma frase de
fechamento). NUNCA gere um infográfico raso com poucos tópicos soltos — o conteúdo deve ser denso
e informativo, como uma página de revista, mesmo mantendo a leitura fácil.

A paleta de cores e o estilo visual (fundo claro ou escuro, paleta de cores, ilustrações ou ícones
flat) devem ser escolhidos por você de acordo com o que combina melhor com o TEMA e a CATEGORIA
recebidos — por exemplo, temas de saúde/bem-estar podem pedir um visual clean e claro, enquanto
temas de tecnologia ou curiosidades podem pedir um visual mais vibrante ou escuro. Varie a paleta
entre execuções para não ficar repetitivo, mas sempre com bom contraste e legibilidade.

Responda APENAS em JSON válido, sem markdown, sem texto fora do JSON, no formato exato:
{
  "titulo": "título principal, curto e impactante, em português, max 6 palavras",
  "subtitulo": "linha de apoio ao título, em português, max 10 palavras",
  "introducao": "1-2 frases de abertura explicando o tema, em português",
  "estilo_visual": "descrição curta em português do estilo escolhido para este tema (ex: 'fundo claro, paleta pastel verde e azul, ícones de linha fina' ou 'fundo escuro, cores neon rosa e amarelo, ícones preenchidos')",
  "topicos": [
    {"numero": 1, "icone": "nome do ícone em inglês (ex: shield, heart, leaf)", "titulo_topico": "título curto do ponto", "descricao_topico": "uma frase curta explicando o ponto"},
    {"numero": 2, "icone": "...", "titulo_topico": "...", "descricao_topico": "..."}
  ],
  "dicas_extra": ["dica curta 1", "dica curta 2", "dica curta 3"],
  "frase_fechamento": "frase de impacto para fechar o infográfico, em português",
  "legenda_instagram": "legenda em português do Brasil para o post do Instagram, com 2-3 frases envolventes seguidas de 8 a 12 hashtags relevantes ao tema e à categoria, misturando hashtags amplas (ex: #curiosidades #vocesabia) com específicas do tema"
}

IMPORTANTE: "topicos" deve ter entre 6 e 8 itens, sempre. Cada descricao_topico deve ter informação
real e específica sobre o tema (não genérica), em no máximo 12 palavras.
"""


def _montar_prompt_imagem(dados: dict) -> str:
    """Monta o prompt de imagem em inglês a partir do roteiro estruturado,
    garantindo que o gerador de imagem receba todo o conteúdo textual exato."""
    topicos_texto = "\n".join(
        f"  {t['numero']}. [{t['icone']} icon] {t['titulo_topico']}: {t['descricao_topico']}"
        for t in dados["topicos"]
    )
    dicas_texto = "; ".join(dados.get("dicas_extra", []))

    return f"""Create a dense, professional, magazine-style vertical portrait infographic (1024x1536,
2:3 portrait orientation, taller than wide), modern flat design. Visual style: {dados['estilo_visual']}.

Layout, top to bottom:
1. Bold large title at the top: "{dados['titulo']}"
2. Subtitle below it: "{dados['subtitulo']}"
3. Short intro paragraph: "{dados['introducao']}"
4. A grid or numbered list of {len(dados['topicos'])} sections, each with a flat icon, a short bold
   title, and a one-line description. Render this exact content for each section:
{topicos_texto}
5. A highlighted tips box with these short tips: {dicas_texto}
6. A closing bold statement at the bottom: "{dados['frase_fechamento']}"

All text must be rendered exactly as given, in Portuguese, crisp and legible, high contrast against
the background, professional infographic typography, clear visual hierarchy, generous spacing between
sections so it doesn't look cluttered despite the density of content. Keep every text element fully
inside a safe margin away from all four edges of the vertical canvas — no title, word, or icon should
ever be cut off or touch the border. If needed, use smaller font sizes rather than letting text overflow.
No watermarks, no logos."""


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

    obrigatorios = [
        "titulo", "subtitulo", "introducao", "estilo_visual",
        "topicos", "dicas_extra", "frase_fechamento", "legenda_instagram",
    ]
    faltando = [campo for campo in obrigatorios if campo not in dados]
    if faltando:
        raise ValueError(f"Resposta do GPT incompleta, faltando: {faltando}")

    if not (6 <= len(dados["topicos"]) <= 8):
        raise ValueError(
            f"Esperado entre 6 e 8 tópicos, recebido {len(dados['topicos'])}."
        )

    dados["prompt_imagem"] = _montar_prompt_imagem(dados)

    return dados
