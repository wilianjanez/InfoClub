# -*- coding: utf-8 -*-
"""
Lista-fonte de temas adicionais com alta adesão em infográfico:
países (curiosidades específicas), animais (espécies específicas) e
funcionamento de mecânicos/máquinas populares.

Esses temas são ADICIONADOS aos 1000 já existentes na planilha (não substituem).
"""

# --- PAÍSES: curiosidade/ângulo específico, não apenas o nome do país ---
paises = [
    "Japão", "Egito", "Brasil", "Índia", "China", "Rússia", "México", "França",
    "Itália", "Grécia", "Espanha", "Alemanha", "Reino Unido", "Estados Unidos",
    "Canadá", "Austrália", "Nova Zelândia", "Coreia do Sul", "Tailândia", "Vietnã",
    "Indonésia", "Turquia", "Marrocos", "África do Sul", "Quênia", "Argentina",
    "Chile", "Peru", "Colômbia", "Cuba", "Portugal", "Holanda", "Suíça",
    "Suécia", "Noruega", "Finlândia", "Islândia", "Irlanda", "Escócia",
    "Polônia", "Hungria", "Áustria", "Bélgica", "Dinamarca", "Israel",
    "Arábia Saudita", "Emirados Árabes Unidos", "Singapura", "Malásia", "Filipinas",
    "Nepal", "Mongólia", "Butão", "Madagascar", "Tanzânia", "Etiópia",
    "Nigéria", "Gana", "Jamaica", "Costa Rica", "Panamá", "Bolívia",
    "Paraguai", "Uruguai", "Venezuela", "Equador", "Croácia", "República Tcheca",
    "Romênia", "Ucrânia", "Sérvia", "Geórgia", "Cazaquistão", "Sri Lanka",
    "Camboja", "Laos", "Mianmar", "Papua-Nova Guiné", "Fiji", "Samoa",
    "Groenlândia", "Antártida", "Líbano", "Jordânia", "Irã", "Iraque",
    "Afeganistão", "Paquistão", "Bangladesh", "Coreia do Norte", "Taiwan",
    "Hong Kong", "Mônaco", "Vaticano", "San Marino", "Liechtenstein",
    "Luxemburgo", "Andorra", "Malta", "Chipre", "Albânia", "Bósnia",
    "Eslovênia", "Eslováquia", "Letônia", "Lituânia", "Estônia", "Bielorrússia",
    "Moldávia", "Argélia", "Tunísia", "Líbia", "Sudão", "Senegal",
    "Costa do Marfim", "Camarões", "Congo", "Angola", "Moçambique", "Zimbábue",
    "Zâmbia", "Namíbia", "Botsuana", "Ruanda", "Uganda", "Somália",
    "Iêmen", "Catar", "Kuwait", "Omã", "Bahrein", "Brunei",
    "Timor-Leste", "Maldivas", "Seicheles", "Maurício", "Trinidad e Tobago",
    "Bahamas", "Barbados", "Haiti", "República Dominicana", "Belize",
    "Guatemala", "Honduras", "El Salvador", "Nicarágua", "Guiana", "Suriname",
]


def gerar_temas_paises():
    extras = []
    for pais in paises:
        extras.append((f"Curiosidades sobre {pais}", "Países e Culturas"))
    return extras


# --- ANIMAIS: espécies específicas, ângulo de curiosidade/comportamento ---
animais_especificos = [
    "tigre-de-bengala", "leão africano", "panda-gigante", "urso-pardo", "urso polar",
    "lobo-cinzento", "raposa-do-ártico", "guepardo", "leopardo", "onça-pintada",
    "rinoceronte-branco", "hipopótamo", "elefante-africano", "elefante-asiático",
    "girafa", "zebra", "gorila", "chimpanzé", "orangotango", "bonobo",
    "lêmure-de-cauda-anelada", "coala", "canguru", "vombate", "ornitorrinco",
    "equidna", "diabo-da-tasmânia", "preguiça", "tamanduá-bandeira", "tatu-bola",
    "capivara", "onça-parda", "lince", "lontra-marinha", "foca-leopardo",
    "leão-marinho", "morsa", "narval", "baleia-azul", "baleia-jubarte",
    "orca", "boto-rosa", "tubarão-branco", "tubarão-martelo", "tubarão-baleia",
    "arraia-manta", "polvo-gigante", "lula-gigante", "água-viva", "estrela-do-mar",
    "cavalo-marinho", "peixe-palhaço", "peixe-balão", "peixe-voador", "salmão",
    "piranha", "enguia-elétrica", "axolote", "salamandra-gigante", "sapo-cururu",
    "rã-venenosa", "camaleão-de-madagascar", "iguana-marinha", "dragão-de-komodo",
    "jacaré-americano", "crocodilo-do-nilo", "cobra-coral", "naja", "píton-reticulada",
    "anaconda-verde", "cascavel", "tartaruga-marinha", "tartaruga-gigante-de-galápagos",
    "águia-careca", "águia-real", "falcão-peregrino", "coruja-das-torres", "coruja-branca",
    "pinguim-imperador", "albatroz", "tucano", "papagaio-cinzento-africano", "arara-azul",
    "flamingo", "pelicano", "cisne-negro", "avestruz", "ema",
    "kiwi (ave)", "urubu-rei", "colibri", "pica-pau", "corvo",
    "morcego-vampiro", "morcego-frugívoro", "ouriço-comum", "esquilo-voador",
    "castor", "lontra-de-rio", "texugo", "doninha", "fuinha",
    "porco-espinho", "hiena-malhada", "chacal", "javali", "alce",
    "rena", "bisão-americano", "búfalo-d'água", "antílope-saltador", "gnu",
    "abelha-rainha", "formiga-cortadeira", "vespa-asiática", "louva-a-deus",
    "borboleta-monarca", "besouro-rinoceronte", "aranha-viúva-negra", "tarântula",
    "escorpião-amarelo", "centopeia-gigante", "caracol-gigante-africano", "ouriço-do-mar",
    "esponja-marinha", "coral-cérebro", "peixe-leão", "barata-d'água",
]


def gerar_temas_animais():
    extras = []
    for animal in animais_especificos:
        extras.append((f"Curiosidades sobre o {animal}", "Animais Específicos"))
    return extras


# --- MECÂNICOS / MÁQUINAS POPULARES: alto interesse visual (artigo já incluso) ---
mecanicos_populares = [
    "o motor a combustão interna", "o motor elétrico de carro", "o câmbio manual",
    "o câmbio automático", "a embreagem", "o sistema de injeção eletrônica", "a turbina de avião",
    "o motor a jato", "o motor de foguete", "a transmissão automática CVT", "o diferencial do carro",
    "o sistema de suspensão automotiva", "o amortecedor", "a direção hidráulica",
    "o freio a tambor", "o sistema de arrefecimento do motor", "o radiador de carro",
    "a bomba de combustível", "a vela de ignição", "o alternador do carro", "a bateria automotiva",
    "o motor de partida (motor de arranque)", "a correia dentada", "a biela e o pistão",
    "as válvulas do motor", "o comando de válvulas", "o turbocompressor", "o intercooler",
    "o sistema de escapamento", "o catalisador automotivo", "o motor diesel",
    "o motor a hidrogênio", "o motor rotativo Wankel", "o sistema híbrido (carro híbrido)",
    "o carregador de carro elétrico", "o motor de moto dois tempos", "o motor de moto quatro tempos",
    "o guincho mecânico", "o macaco hidráulico", "o elevador hidráulico", "o guindaste de construção",
    "a escavadeira hidráulica", "o trator agrícola", "a colheitadeira", "a betoneira",
    "o compressor de ar", "a bomba de água", "o gerador de energia a diesel", "o torno mecânico",
    "a fresadora industrial", "a prensa hidráulica", "a esteira transportadora", "o robô industrial",
    "o braço robótico de fábrica", "a máquina de costura", "a máquina de lavar (mecanismo interno)",
    "a secadora de roupas", "a lava-louças", "o ar-condicionado split", "o compressor de geladeira",
    "a bomba de calor", "o exaustor industrial", "o ventilador elétrico", "o liquidificador (mecanismo)",
    "a batedeira elétrica", "o processador de alimentos", "a máquina de café expresso",
    "a máquina de costura industrial", "a impressora a laser", "a impressora 3D FDM",
    "o scanner 3D", "a fresadora CNC", "a máquina de corte a laser", "a máquina de solda MIG",
    "o motor de elevador predial", "a escada rolante", "a esteira ergométrica (mecanismo)",
    "a bicicleta ergométrica", "a catapulta medieval", "a balestra (mecanismo)", "o relógio mecânico de corda",
    "a caixa de câmbio de bicicleta", "o freio hidráulico de bicicleta", "o pedivela de bicicleta",
    "o motor de barco a hélice", "o motor fora de borda", "o submarino (sistema de mergulho)",
    "a âncora de navio", "o leme de navio", "a hélice de avião", "o trem de pouso de avião",
    "a asa de avião (mecanismo de sustentação)", "o rotor de helicóptero", "o paraquedas (mecanismo)",
    "o airbag (mecanismo de acionamento)", "o cinto de segurança retrátil", "o vidro elétrico de carro",
    "a trava elétrica de porta de carro", "o sistema de partida sem chave", "o pneu run-flat",
    "o amortecedor a gás", "o sistema de tração 4x4", "o diferencial bloqueável",
]


def gerar_temas_mecanicos():
    extras = []
    for item in mecanicos_populares:
        extras.append((f"Como funciona {item}", "Máquinas e Mecânica"))
    return extras


def gerar_novos_temas():
    """Retorna a lista combinada dos três novos blocos, sem duplicar internamente."""
    novos = []
    novos.extend(gerar_temas_paises())
    novos.extend(gerar_temas_animais())
    novos.extend(gerar_temas_mecanicos())

    vistos = set()
    unicos = []
    for tema, categoria in novos:
        if tema not in vistos:
            vistos.add(tema)
            unicos.append((tema, categoria))
    return unicos


if __name__ == "__main__":
    novos = gerar_novos_temas()
    print(f"Total de novos temas únicos: {len(novos)}")
