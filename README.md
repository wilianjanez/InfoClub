# Agente de Infográficos Automáticos para Instagram

Publica automaticamente, 3x ao dia, um infográfico sobre um tema sorteado de uma planilha,
gerado por IA (texto + imagem), direto no Instagram — tudo via GitHub Actions.

## Como funciona

```
GitHub Actions (cron, 3x/dia)
   │
   ├─ 1. Lê data/temas.xlsx e sorteia um tema com Publicado = FALSE
   ├─ 2. Envia o tema para o GPT (gpt-4o-mini), que gera:
   │      título, tópicos, prompt de imagem e legenda do post
   ├─ 3. Envia o prompt de imagem para o GPT Image 1 Mini, que gera o infográfico
   ├─ 4. Comita a imagem gerada no repositório (pasta imagens/)
   ├─ 5. Publica no Instagram via Graph API, usando a URL "raw" do GitHub
   │      como endereço público da imagem
   └─ 6. Marca o tema como Publicado = TRUE na planilha e comita a atualização
```

## Estrutura do projeto

```
.
├── .github/workflows/publicar.yml   # workflow do GitHub Actions (cron 3x/dia)
├── data/temas.xlsx                  # planilha com 1000 temas prontos
├── imagens/                         # imagens geradas (comitadas automaticamente)
├── src/
│   ├── planilha.py                  # leitura/atualização da planilha
│   ├── roteiro.py                   # geração do roteiro via GPT
│   ├── imagem.py                    # geração da imagem via GPT Image Mini
│   ├── instagram.py                 # publicação via Graph API
│   └── main.py                      # orquestração (etapas "gerar" e "publicar")
├── scripts_auxiliares/              # scripts usados só para (re)gerar a planilha
│   ├── gerar_temas_lista.py         # lista-fonte dos 1000 temas iniciais, por categoria
│   ├── gerar_temas_extra_v2.py      # lista-fonte extra: países, animais, mecânica
│   ├── popular_planilha_1000.py     # grava os 1000 temas iniciais do zero
│   └── adicionar_temas_extra.py     # adiciona novos temas sem apagar os existentes
└── requirements.txt
```

## Setup — passo a passo

### 1. Planilha de temas

A planilha `data/temas.xlsx` já vem com **1.379 temas únicos**, distribuídos em 30
categorias — incluindo blocos de alta adesão visual como **Países e Culturas** (148 temas),
**Animais Específicos** (128 temas, por espécie) e **Máquinas e Mecânica** (103 temas sobre
funcionamento de motores, eletrodomésticos e veículos), além de Ciência, Saúde, Tecnologia,
Curiosidades, Meio Ambiente, Astronomia, Corpo Humano, Profissões e Processos, e mais.

Com 3 publicações por dia, isso cobre **mais de 1 ano de conteúdo sem repetir nenhum tema**.

Colunas:

| Coluna | Descrição |
|---|---|
| `ID` | identificador numérico único |
| `Tema` | o tema em si (texto livre) |
| `Categoria` | categoria do tema (usada como contexto para o GPT) |
| `Publicado` | `TRUE`/`FALSE` — controla o que já foi postado |
| `DataPublicacao` | preenchida automaticamente pelo script |

Para adicionar novos temas manualmente, edite a planilha e adicione linhas com
`Publicado = FALSE`. Quando todos os temas estiverem com `Publicado = TRUE`, o script
vai falhar avisando que não há temas disponíveis — é hora de adicionar mais linhas.

> **Para regenerar a planilha do zero** (apaga o histórico de `Publicado`), edite
> `scripts_auxiliares/gerar_temas_lista.py` e `gerar_temas_extra_v2.py`, depois rode:
> ```bash
> python scripts_auxiliares/popular_planilha_1000.py
> python scripts_auxiliares/adicionar_temas_extra.py
> ```
>
> **Para apenas adicionar novos temas** a uma planilha já em produção (preserva o que
> já foi publicado), edite a lista desejada em `scripts_auxiliares/gerar_temas_extra_v2.py`
> e rode só:
> ```bash
> python scripts_auxiliares/adicionar_temas_extra.py
> ```
> Esse script detecta e ignora automaticamente temas que já existem na planilha,
> e continua a numeração de `ID` a partir do maior ID já usado.

### 2. Conta do Instagram

Pré-requisitos na conta que vai publicar:
1. Conta Instagram convertida para **Profissional** (Business ou Creator).
2. Vinculada a uma **Página do Facebook**.
3. Conectada ao **mesmo App no Meta for Developers** que você já usa na sua outra automação
   (já que esse app já tem a permissão `instagram_business_content_publish` aprovada).
4. Gere, para essa conta especificamente, o **Instagram Business Account ID** e o
   **Access Token** (token de longa duração, recomenda-se o token de 60 dias renovável).

### 3. Conta OpenAI

1. Crie uma conta em platform.openai.com e gere uma **API Key**.
2. Garanta que a chave tem acesso aos modelos `gpt-4o-mini` e `gpt-image-1-mini`.

### 4. Secrets do repositório GitHub

Em **Settings → Secrets and variables → Actions**, crie:

| Secret | Valor |
|---|---|
| `OPENAI_API_KEY` | sua chave da API da OpenAI |
| `IG_USER_ID` | Instagram Business Account ID da conta que vai publicar |
| `IG_ACCESS_TOKEN` | Access Token dessa conta |

### 5. Repositório público

Para usar GitHub Actions sem limite de minutos, mantenha o repositório **público**.
Isso também é necessário para a URL `raw.githubusercontent.com` da imagem funcionar sem
autenticação (a API do Instagram precisa acessar a imagem livremente).

### 6. Testar manualmente antes de ativar o cron

Vá em **Actions → Publicar Infografico Instagram → Run workflow** para disparar uma
execução manual (`workflow_dispatch`) e validar o fluxo de ponta a ponta antes de
depender só do agendamento automático.

## Horários de publicação

Definidos em `.github/workflows/publicar.yml`, em UTC (GitHub Actions não trabalha com
fuso horário local):

| Horário Brasil (BRT, UTC-3) | Horário UTC (cron) |
|---|---|
| 09:00 | `0 12 * * *` |
| 14:00 | `0 17 * * *` |
| 19:00 | `0 22 * * *` |

Ajuste os valores de `cron` no workflow se quiser outros horários.
Lembre-se: o Brasil não usa mais horário de verão desde 2019, então essa conversão
é fixa (não precisa ajustar sazonalmente).

## Custos estimados

| Item | Custo |
|---|---|
| GitHub Actions (repo público) | R$ 0 |
| GPT-4o-mini (texto, 3x/dia) | poucos centavos/mês |
| GPT Image 1 Mini (90 imagens/mês) | ~R$ 10–15/mês |
| Hospedagem de imagem (GitHub raw) | R$ 0 |
| Instagram Graph API | R$ 0 |

## Limitações conhecidas

- Horários do GitHub Actions podem atrasar 10–30 min em períodos de pico.
- Workflows agendados são desativados após 60 dias **sem nenhum commit** no repositório —
  como o próprio bot comita a cada execução, isso não deve ocorrer na prática.
- A qualidade de texto dentro de imagens geradas por IA não é perfeita. Se notar erros de
  texto recorrentes nos infográficos, considere migrar o modelo de imagem em `src/imagem.py`
  para um com melhor renderização de texto (ex: Gemini 3 Pro Image ou Flux Pro 1.1).
- Limite da API do Instagram: 100 publicações via API por período de 24h — bem acima do
  uso previsto aqui (3/dia).
