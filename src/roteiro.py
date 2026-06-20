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

Todo infográfico precisa de uma imagem central de destaque (hero image) que mostre de forma realista
e reconhecível o assunto principal do tema — por exemplo: se o tema é sobre um animal específico,
uma ilustração realista desse animal exato (não um ícone genérico); se é sobre um país, uma cena ou
marco reconhecível desse país; se é sobre uma máquina/mecanismo, uma ilustração técnica realista
desse objeto; se é sobre um conceito abstrato (ex: "o que é inflação"), uma cena ou objeto que
represente bem o conceito de forma concreta. Essa imagem central é o elemento mais importante para
prender a atenção e ensinar visualmente o que é o assunto — não pule essa etapa.

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
  "assunto_visual_principal": "descrição detalhada em inglês, para o gerador de imagem, do assunto exato que deve aparecer de forma realista e reconhecível na imagem central de destaque (ex: 'a realistic illustration of a wombat, a stocky Australian marsupial with short legs, brown fur and a flat snout, shown in its natural burrow habitat')",
  "topicos": [
    {"numero": 1, "icone": "nome do ícone em inglês (ex: shield, heart, leaf)", "titulo_topico": "título curto do ponto", "descricao_topico": "uma frase curta explicando o ponto"},
    {"numero": 2, "icone": "...", "titulo_topico": "...", "descricao_topico": "..."}
  ],
  "dicas_extra": ["dica curta 1", "dica curta 2"],
  "frase_fechamento": "frase de impacto para fechar o infográfico, em português",
  "legenda_instagram": "legenda em português do Brasil para o post do Instagram, com 2-3 frases envolventes seguidas de 8 a 12 hashtags relevantes ao tema e à categoria, misturando hashtags amplas (ex: #curiosidades #vocesabia) com específicas do tema"
}

IMPORTANTE: "topicos" deve ter NO MÁXIMO 8 itens e NO MÍNIMO 6 itens — nunca 9 ou mais, nunca menos
de 6. Conte os itens antes de responder. Cada descricao_topico deve ter informação real e específica
sobre o tema (não genérica), em no máximo 12 palavras. "assunto_visual_principal" deve ser detalhado
o suficiente (características físicas, cores, formato) para que o gerador de imagem consiga desenhar
o item correto, mesmo sem saber previamente como ele é.
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

CRITICAL LAYOUT CONSTRAINT: All 7 sections below MUST fit completely within the 1024x1536 canvas,
from top edge to bottom edge, with nothing cut off, overflowing, or hidden. Before finalizing, mentally
reserve a fixed vertical budget for each section so the last section (closing statement) is fully
visible with safe margin to the bottom edge. The hero illustration (section 3) should take no more
than 25% of the total canvas height — keep it impactful but compact, prioritizing leaving enough room
for all later sections, especially the closing statement, which must never be cropped.

TOP MARGIN IS CRITICAL: leave at least 60px of empty padding above the title — the title text must
start well below the top edge, never touching or being cut by it. This applies even more strictly
than other margins, because many viewing apps slightly crop the very top of square/portrait images.
The title's full height (including ascenders and any accents) must be 100% visible with clear empty
space above it.

Layout, top to bottom (each section must be smaller/more compact if needed to fit everything in):
1. Bold title at the top: "{dados['titulo']}"
2. Subtitle below it: "{dados['subtitulo']}"
3. A hero illustration area (max 25% of canvas height) featuring: {dados['assunto_visual_principal']}.
   This realistic illustration of the main subject must be clearly recognizable and accurate.
4. Short intro paragraph: "{dados['introducao']}"
5. A grid or numbered list of {len(dados['topicos'])} sections, each with a flat icon, a short bold
   title, and a one-line description. Render this exact content for each section:
{topicos_texto}
6. A highlighted tips box with these short tips: {dicas_texto}
7. A closing bold statement at the bottom, fully visible with margin below it: "{dados['frase_fechamento']}"

All text must be rendered exactly as given, in Portuguese, crisp and legible, high contrast against
the background, professional infographic typography, clear visual hierarchy. Use a clean, simple,
highly legible sans-serif or rounded font for ALL text — avoid decorative, handwritten, artistic, or
stylized fonts, since they distort accents and letters and make Portuguese words hard to read correctly.
Spelling and accentuation must be 100% exact, with no altered, swapped, or missing accent marks.
Use compact spacing between sections rather than generous spacing if that's what it takes to fit all
7 sections fully inside the canvas. Keep every text element fully inside a safe margin away from all
four edges — no title, word, icon, or section (especially the last one) should ever be cut off or
touch the border. Reduce font sizes or icon sizes as needed rather than letting any content overflow
past the bottom edge. No watermarks, no logos."""


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
        "titulo", "subtitulo", "introducao", "estilo_visual", "assunto_visual_principal",
        "topicos", "dicas_extra", "frase_fechamento", "legenda_instagram",
    ]
    faltando = [campo for campo in obrigatorios if campo not in dados]
    if faltando:
        raise ValueError(f"Resposta do GPT incompleta, faltando: {faltando}")

    if len(dados["topicos"]) > 8:
        dados["topicos"] = dados["topicos"][:8]

    if len(dados["topicos"]) < 6:
        raise ValueError(
            f"Esperado no mínimo 6 tópicos, recebido {len(dados['topicos'])}."
        )

    dados["prompt_imagem"] = _montar_prompt_imagem(dados)

    return dados
