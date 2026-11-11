#!/usr/bin/env python3
"""Gera o site da Iasmim Leão · Odontologia Estética na raiz do repositório.
Uso: python3 fonte/build.py
Todos os arquivos ficam soltos na raiz (sem subpastas)."""
import json
import re
from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).parent.parent
HOJE = "2026-11-11"

# ───────────────────────────── DADOS ─────────────────────────────
DOMINIO = "https://SEU-DOMINIO.com.br"   # trocar pelo endereço final antes de divulgar
NOME = "Iasmim Leão"
MARCA = "Iasmim Leão · Odontologia Estética"
CRO = "CRO-CE 18162"
WHATS = "5585989951456"
FONE_EXIBE = "(85) 98995-1456"
FONE_TEL = "+5585989951456"
INSTAGRAM = "https://www.instagram.com/iasmimleao/"
# Preencher quando confirmado. Com a cidade, títulos e textos passam a dizer "Dentista em <cidade>".
CIDADE = ""          # ex.: "Fortaleza"
ENDERECO = ""        # ex.: "Av. Exemplo, 100, sala 10, Bairro"
CEP = ""
# ─────────────────────────────────────────────────────────────────

EM_CIDADE = f" em {CIDADE}" if CIDADE else ""
LOCAL = f"{CIDADE}, Ceará" if CIDADE else "Ceará"

WA_ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.46 15.03L2 22l5.1-1.54A9.9 9.9 0 1 0 12.04 2Zm0 1.8a8.1 8.1 0 1 1-4.3 14.96l-.3-.19-3.03.92.94-2.94-.2-.31A8.1 8.1 0 0 1 12.04 3.8Zm-3.4 3.9c-.2 0-.5.07-.76.36-.26.28-1 .98-1 2.38 0 1.4 1.02 2.76 1.17 2.95.14.19 2 3.06 4.86 4.29 2.38 1.02 2.87.82 3.39.77.51-.05 1.66-.68 1.9-1.33.23-.66.23-1.22.16-1.34-.07-.12-.26-.19-.54-.33-.29-.14-1.67-.82-1.93-.92-.26-.09-.45-.14-.64.14-.19.29-.73.92-.9 1.11-.16.19-.33.21-.61.07-.29-.14-1.2-.44-2.29-1.41a8.6 8.6 0 0 1-1.58-1.97c-.17-.28-.02-.44.12-.58.13-.12.29-.33.43-.49.14-.17.19-.29.28-.48.1-.19.05-.35-.02-.5-.07-.13-.63-1.55-.88-2.12-.22-.52-.45-.53-.64-.54l-.52-.06Z"/></svg>')
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.25" aria-hidden="true"><path d="M2 8h12M9 3l5 5-5 5"/></svg>'

# Selo circular: recria o logotipo dela (texto em círculo ao redor do "L").
SEAL = ('<svg class="seal" viewBox="0 0 140 140" aria-hidden="true" focusable="false">'
        '<defs><path id="seal-c" d="M70 70m-54 0a54 54 0 1 1 108 0a54 54 0 1 1-108 0"/></defs>'
        '<g class="seal-ring"><text><textPath href="#seal-c" textLength="332">Iasmim Leão · Odontologia Estética · </textPath></text></g>'
        '<text class="seal-l" x="70" y="85" text-anchor="middle">L</text></svg>')

TRATAMENTOS = [  # arquivo, nome, resumo
    ("prevencao.html", "Prevenção", "Consultas de rotina, limpeza e orientação para cuidar antes de precisar tratar."),
    ("dentistica.html", "Dentística", "Restaurações e estética dental que devolvem forma, função e naturalidade."),
    ("clareamento-dental.html", "Clareamento dental", "Clareamento indicado e acompanhado pela dentista, depois de uma avaliação."),
    ("harmonizacao-orofacial.html", "Harmonização orofacial", "Procedimentos estéticos na face e nos lábios, feitos por cirurgiã-dentista."),
]


def wa(msg):
    return f"https://wa.me/{WHATS}?text={quote(msg)}"


def pic(name, alt, w, h, eager=False):
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source srcset="{name}.webp" type="image/webp">'
            f'<img src="{name}.jpg" alt="{alt}" width="{w}" height="{h}" {load}></picture>')


def case(n, titulo, modo, antes, depois, alt, w, h):
    return f"""<figure class="case reveal">
      <div class="case-pair case-pair--{modo}">
        <div class="case-half">{pic(antes, alt + ", antes do tratamento", w, h)}<span class="case-tag">Antes</span></div>
        <div class="case-half">{pic(depois, alt + ", depois do tratamento", w, h)}<span class="case-tag case-tag--after">Depois</span></div>
      </div>
      <figcaption><b>{titulo}</b><span>Caso {n:02d}</span></figcaption>
    </figure>"""


CASOS = [
    (1, "Estética do sorriso", "rows", "caso1-antes", "caso1-depois", "Sorriso em close", 600, 300),
    (2, "Clareamento dental", "rows", "caso2-antes", "caso2-depois", "Dentes em close", 600, 300),
    (3, "Estética do sorriso", "cols", "caso3-antes", "caso3-depois", "Sorriso de perfil em close", 300, 600),
]
NOTA_CASOS = (f"Casos atendidos por Iasmim Leão, {CRO}. As imagens mostram o início e o resultado final do tratamento. "
              "Cada pessoa responde de um jeito, e a indicação depende de avaliação.")

NAV = [("prevencao.html", "Prevenção"), ("dentistica.html", "Dentística"),
       ("clareamento-dental.html", "Clareamento"), ("harmonizacao-orofacial.html", "Harmonização")]


def nav_items(current):
    return "".join(f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == current else ""}>{l}</a></li>' for h, l in NAV)


def menu_items(current):
    items = [("index.html", "Início")] + NAV
    return "".join(
        f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == current else ""}><span>{i:02d}</span>{l}</a></li>'
        for i, (h, l) in enumerate(items, start=1))


def url_of(page):
    return f"{DOMINIO}/{'' if page == 'index.html' else page}"


def json_ld(page, title, desc, crumb, faq, servico):
    pessoa = {"@type": "Person", "@id": DOMINIO + "/#iasmim", "name": NOME, "jobTitle": "Cirurgiã-dentista",
              "description": "Cirurgiã-dentista, aperfeiçoada em Dentística e pós-graduanda em Harmonização.",
              "identifier": {"@type": "PropertyValue", "propertyID": "CRO", "value": "CE 18162"},
              "knowsAbout": ["Odontologia estética", "Dentística", "Clareamento dental", "Harmonização orofacial", "Prevenção em saúde bucal"],
              "image": f"{DOMINIO}/il-retrato.jpg", "url": DOMINIO + "/", "sameAs": [INSTAGRAM],
              "worksFor": {"@id": DOMINIO + "/#consultorio"}}
    consultorio = {"@type": "Dentist", "@id": DOMINIO + "/#consultorio", "name": MARCA, "url": DOMINIO + "/",
                   "description": f"Odontologia estética{EM_CIDADE}: prevenção, dentística, clareamento dental e harmonização orofacial.",
                   "telephone": FONE_TEL, "image": [f"{DOMINIO}/il-capa.jpg", f"{DOMINIO}/il-retrato.jpg"],
                   "logo": f"{DOMINIO}/logo-iasmim-leao.svg",
                   "founder": {"@id": DOMINIO + "/#iasmim"}, "employee": {"@id": DOMINIO + "/#iasmim"},
                   "areaServed": {"@type": "Place", "name": LOCAL}, "sameAs": [INSTAGRAM],
                   "medicalSpecialty": "Dentistry",
                   "contactPoint": {"@type": "ContactPoint", "telephone": FONE_TEL, "contactType": "agendamento", "availableLanguage": "pt-BR"},
                   "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Tratamentos", "itemListElement": [
                       {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d, "url": f"{DOMINIO}/{h}",
                                                          "provider": {"@id": DOMINIO + "/#consultorio"}}} for h, n, d in TRATAMENTOS]}}
    if ENDERECO and CIDADE:
        consultorio["address"] = {"@type": "PostalAddress", "streetAddress": ENDERECO, "addressLocality": CIDADE,
                                  "addressRegion": "CE", "postalCode": CEP, "addressCountry": "BR"}
    site = {"@type": "WebSite", "@id": DOMINIO + "/#site", "url": DOMINIO + "/", "name": MARCA, "inLanguage": "pt-BR",
            "publisher": {"@id": DOMINIO + "/#consultorio"}}
    web = {"@type": "WebPage", "@id": url_of(page) + "#pagina", "url": url_of(page), "name": title, "description": desc,
           "inLanguage": "pt-BR", "isPartOf": {"@id": DOMINIO + "/#site"}, "about": {"@id": DOMINIO + "/#consultorio"},
           "primaryImageOfPage": f"{DOMINIO}/il-capa.jpg", "dateModified": HOJE}
    graph = [consultorio, pessoa, site, web]
    if servico:
        graph.append({"@type": "Service", "name": servico[0], "description": servico[1], "serviceType": servico[0],
                      "provider": {"@id": DOMINIO + "/#consultorio"}, "areaServed": LOCAL, "url": url_of(page)})
    if crumb:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": DOMINIO + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url_of(page)}]})
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", r)}} for q, r in faq]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def layout(page, title, desc, body, wa_msg, crumb=None, faq=None, servico=None, robots="index, follow, max-image-preview:large"):
    w = wa(wa_msg)
    trat = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n, _ in TRATAMENTOS)
    geo = f'\n<meta name="geo.placename" content="{CIDADE}">' if CIDADE else ""
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url_of(page)}">
<meta name="author" content="{NOME}, {CRO}">
<meta name="theme-color" content="#171210">
<meta name="geo.region" content="BR-CE">{geo}
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="{MARCA}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url_of(page)}">
<meta property="og:image" content="{DOMINIO}/il-capa.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Iasmim Leão, cirurgiã-dentista, no consultório">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="serif.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
<script>document.documentElement.classList.add("js")</script>
<script type="application/ld+json">
{json_ld(page, title, desc, crumb, faq, servico)}
</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header" data-header>
  <div class="wrap header-in">
    <a class="brand" href="index.html">
      <span class="brand-mono" aria-hidden="true">L</span>
      <span><span class="brand-name">Iasmim Leão</span><span class="brand-sub">Odontologia estética</span></span>
    </a>
    <nav class="nav" aria-label="Tratamentos"><ul>{nav_items(page)}</ul></nav>
    <a class="btn btn--ivory btn--sm header-cta" href="{w}" target="_blank" rel="noopener">Agendar avaliação</a>
    <button class="menu-btn" type="button" data-menu-btn aria-expanded="false" aria-controls="menu"><span data-menu-label>Menu</span><i aria-hidden="true"></i></button>
  </div>
</header>

<div class="menu" id="menu">
  <nav aria-label="Menu"><ul class="menu-links">{menu_items(page)}</ul></nav>
  <div class="menu-foot">
    <a class="btn btn--ivory" href="{w}" target="_blank" rel="noopener">{WA_ICON}Agendar pelo WhatsApp</a>
    <p>{NOME} · Cirurgiã-dentista · {CRO}</p>
  </div>
</div>

<main id="conteudo">
{body}
</main>

<footer class="site-footer">
  <div class="wrap grid">
    <div class="footer-brand">
      <p class="serif">Iasmim Leão</p>
      <p>Odontologia estética{EM_CIDADE}. Prevenção, dentística, clareamento dental e harmonização orofacial.</p>
    </div>
    <div class="footer-col">
      <h2>Tratamentos</h2>
      <ul>{trat}</ul>
    </div>
    <div class="footer-col">
      <h2>Contato</h2>
      <ul>
        <li><a href="{w}" target="_blank" rel="noopener">WhatsApp</a></li>
        <li><a href="tel:{FONE_TEL}">{FONE_EXIBE}</a></li>
        <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h2>Site</h2>
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="index.html#sobre">Sobre</a></li>
        <li><a href="index.html#casos">Casos</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap"><div class="footer-legal">
    <p>{NOME} · Cirurgiã-dentista · {CRO}. As informações deste site têm caráter educativo e não substituem a consulta. A indicação de cada tratamento depende de avaliação.</p>
    <p>© 2026 {NOME}</p>
  </div></div>
</footer>

<div class="dock" data-dock>
  <a class="btn btn--ivory" href="{w}" target="_blank" rel="noopener">{WA_ICON}Agendar avaliação</a>
</div>

<script src="main.js" defer></script>
</body>
</html>
"""
    return html


def faq_block(items, titulo="Perguntas <em>frequentes</em>", paper=False):
    lis = "".join(f'<details><summary>{q}</summary><div class="answer"><p>{r}</p></div></details>' for q, r in items)
    return f"""
<section class="section{' section--paper' if paper else ''}" aria-labelledby="faq-t">
  <div class="wrap grid">
    <div class="faq-head reveal">
      <span class="kicker">Dúvidas</span>
      <h2 id="faq-t">{titulo}</h2>
    </div>
    <div class="faq-list reveal">{lis}</div>
  </div>
</section>"""


def cta(titulo, texto, msg, foco=None):
    """Chamada para agendamento: a pessoa escolhe o que procura e o WhatsApp já abre com a mensagem pronta."""
    opcoes = [
        ("Prevenção e limpeza", "uma consulta de prevenção e limpeza"),
        ("Dentística", "uma avaliação de dentística"),
        ("Clareamento dental", "uma avaliação para clareamento dental"),
        ("Harmonização orofacial", "uma avaliação de harmonização orofacial"),
        ("Ainda não sei", None),
    ]
    chips = ""
    for rotulo, alvo in opcoes:
        m = (f"Olá, Iasmim! Vi o seu site e gostaria de agendar {alvo}." if alvo
             else "Olá, Iasmim! Vi o seu site e gostaria de agendar uma avaliação. Ainda não sei qual tratamento é para mim.")
        cls = "chip chip--on" if rotulo == foco else "chip"
        chips += f'<li><a class="{cls}" href="{wa(m)}" target="_blank" rel="noopener">{rotulo}{ARROW}</a></li>'
    return f"""
<section class="cta ink" id="agendar" aria-labelledby="cta-t">
  <div class="wrap grid">
    <div class="cta-main reveal">
      <span class="kicker">Agendamento</span>
      <h2 id="cta-t">{titulo}</h2>
      <p class="lead">{texto}</p>
      <p class="chips-label" id="chips-l">O que você procura?</p>
      <ul class="chips" aria-labelledby="chips-l">{chips}</ul>
      <p class="cta-alt">Ou <a href="{wa(msg)}" target="_blank" rel="noopener">mande uma mensagem direta</a> para o {FONE_EXIBE}.</p>
    </div>
    <aside class="cta-card reveal" aria-label="Como funciona o agendamento">
      <div class="cta-card-head">{SEAL}<p>Como funciona</p></div>
      <ol>
        <li><b>Você escolhe e envia</b>A mensagem já abre escrita no WhatsApp.</li>
        <li><b>Tira as dúvidas</b>Pergunte o que quiser antes de marcar.</li>
        <li><b>Combina o horário</b>A avaliação é o primeiro passo do tratamento.</li>
      </ol>
      <p class="cta-card-foot">{NOME} · {CRO}</p>
    </aside>
  </div>
</section>"""


FAQ_HOME = [
    ("Como agendo uma avaliação?", f"Pelo WhatsApp, no {FONE_EXIBE}. Conte o que você procura e combinamos o melhor horário."),
    ("De quanto em quanto tempo devo ir ao dentista?", "Em geral, a cada seis meses. Na avaliação, a dentista indica o intervalo certo para você, que pode ser menor ou maior."),
    ("O que é dentística?", 'É a área da odontologia que restaura a forma, a função e a estética dos dentes, com restaurações e reconstruções em resina, por exemplo. <a href="dentistica.html">Saiba mais sobre dentística</a>.'),
    ("Clareamento dental causa sensibilidade?", 'Algumas pessoas sentem sensibilidade durante o tratamento, e ela costuma passar. Por isso o clareamento é indicado e acompanhado pela dentista. <a href="clareamento-dental.html">Veja como funciona</a>.'),
    ("Dentista pode fazer harmonização orofacial?", 'Sim. A harmonização orofacial é uma especialidade reconhecida pelo Conselho Federal de Odontologia. <a href="harmonizacao-orofacial.html">Entenda a harmonização orofacial</a>.'),
]


# ───────────────────────────── INÍCIO ─────────────────────────────
def page_index():
    msg = "Olá, Iasmim! Vi o seu site e gostaria de agendar uma avaliação."
    quem = f"Iasmim Leão · Cirurgiã-dentista{EM_CIDADE}"
    treats = "".join(
        f'<li class="treat reveal"><a href="{h}"><span class="treat-n">{i:02d}</span><h3>{n}</h3><p>{d}</p><span class="treat-go">{ARROW}</span></a></li>'
        for i, (h, n, d) in enumerate(TRATAMENTOS, start=1))
    palavras = ["Prevenção", "Dentística", "Clareamento", "Harmonização orofacial", "Odontologia estética", "Cuidado"]
    faixa = "".join(f"<span>{p}</span>" for p in palavras) * 2
    casos = "".join(case(*c) for c in CASOS)
    body = f"""
<section class="hero ink" aria-labelledby="hero-t">
  <div class="wrap">
    <div class="grid hero-grid">
      <div class="hero-text">
        <h1 id="hero-t"><span class="who">{quem}</span><span class="ln"><span>Prevenção</span></span> <span class="ln"><span>é o <em>começo.</em></span></span></h1>
        <svg class="hero-arc" viewBox="0 0 300 26" aria-hidden="true" focusable="false"><path d="M3 4 C 80 26, 220 26, 297 4" pathLength="1"/></svg>
        <p class="lead">Odontologia estética que começa pelo cuidado: avaliar, orientar e só então tratar. Dentística, clareamento dental e harmonização orofacial.</p>
        <div class="actions">
          <a class="btn btn--ivory" href="#agendar">{WA_ICON}Agendar minha avaliação</a>
          <a class="link" href="#tratamentos">Conhecer os tratamentos</a>
        </div>
        <p class="hero-note">Pelo WhatsApp, em uma mensagem. Você tira as dúvidas antes de marcar.</p>
      </div>
      <figure class="hero-figure">
        <div class="arch">{pic("il-retrato", "Iasmim Leão, cirurgiã-dentista, de roupa branca no consultório", 576, 768, eager=True)}</div>
        {SEAL}
        <figcaption>Iasmim Leão, no consultório</figcaption>
      </figure>
    </div>
    <dl class="hero-facts">
      <div><dt>Registro</dt><dd>{CRO}</dd></div>
      <div><dt>Aperfeiçoamento</dt><dd>Dentística</dd></div>
      <div><dt>Pós-graduanda</dt><dd>Harmonização</dd></div>
    </dl>
  </div>
  <div class="marquee" aria-hidden="true"><div class="marquee-track">{faixa}</div></div>
</section>

<section class="section manifesto" aria-labelledby="man-t">
  <div class="wrap grid">
    <div class="manifesto-main reveal">
      <span class="kicker">O que eu acredito</span>
      <h2 id="man-t" class="vh">Prevenção em primeiro lugar</h2>
      <p>O sorriso bonito é consequência. Antes dele vem a <em>saúde</em>: olhar com calma, explicar o que está acontecendo e cuidar do que precisa de cuidado.</p>
    </div>
    <div class="manifesto-side reveal">
      <p>Toda consulta começa por uma avaliação. A partir dela você entende as opções e decide, sem pressa, o que faz sentido para o seu caso.</p>
      <a class="link" href="prevencao.html">Como funciona a prevenção</a>
    </div>
  </div>
</section>

<section class="section section--paper" id="tratamentos" aria-labelledby="trat-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="kicker">Tratamentos</span>
        <h2 id="trat-t">Do cuidado de rotina à <em>estética.</em></h2>
      </div>
      <p class="head-b lead">Quatro frentes de atendimento. Qual delas é para você, a avaliação responde.</p>
    </div>
    <ul class="treats">{treats}</ul>
  </div>
</section>

<section class="section" id="sobre" aria-labelledby="sobre-t">
  <div class="wrap grid about">
    <figure class="about-media pic reveal">
      {pic("il-consultorio", "Iasmim Leão, de roupa branca, fotografada no espelho do consultório, com bancada e mesa ao fundo", 432, 540)}
      <figcaption>No consultório</figcaption>
    </figure>
    <div class="about-body reveal">
      <span class="kicker">Sobre</span>
      <h2 id="sobre-t">Iasmim Leão, <em>cirurgiã‑dentista.</em></h2>
      <p>Atendo com foco em odontologia estética e em prevenção. Meu trabalho passa pela dentística, pelo clareamento dental e pela harmonização orofacial, sempre a partir de uma avaliação individual.</p>
      <dl class="creds">
        <div><dt>Registro</dt><dd>{CRO}</dd></div>
        <div><dt>Formação</dt><dd>Aperfeiçoada em Dentística</dd></div>
        <div><dt>Em curso</dt><dd>Pós-graduação em Harmonização</dd></div>
      </dl>
      <div class="actions">
        <a class="btn btn--ink" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Falar com a Iasmim</a>
      </div>
    </div>
  </div>
</section>

<section class="section ink" id="casos" aria-labelledby="casos-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="kicker">Casos</span>
        <h2 id="casos-t">Resultados de <em>consultório.</em></h2>
      </div>
      <p class="head-b lead">Início e resultado final de tratamentos realizados pela Iasmim.</p>
    </div>
    <div class="cases">{casos}</div>
    <p class="cases-note reveal">{NOTA_CASOS}</p>
  </div>
</section>

<section class="section section--paper" aria-labelledby="passos-t">
  <div class="wrap">
    <div class="head grid reveal">
      <div class="head-a">
        <span class="kicker">Como funciona</span>
        <h2 id="passos-t">Três passos, <em>sem pressa.</em></h2>
      </div>
    </div>
    <ol class="steps">
      <li class="step reveal"><h3>Avaliação</h3><p>Uma conversa sobre o que incomoda e o que você espera, seguida do exame clínico.</p></li>
      <li class="step reveal" style="--d:.08s"><h3>Plano de tratamento</h3><p>Você recebe as opções explicadas em linguagem simples, com o que cada uma envolve.</p></li>
      <li class="step reveal" style="--d:.16s"><h3>Acompanhamento</h3><p>Depois do tratamento, os retornos mantêm o resultado e a saúde em dia.</p></li>
    </ol>
  </div>
</section>

<section class="section" aria-labelledby="insta-t">
  <div class="wrap grid insta">
    <div class="insta-main reveal">
      <span class="kicker">Instagram</span>
      <h2 id="insta-t" class="vh">Iasmim Leão no Instagram</h2>
      <a class="insta-handle" href="{INSTAGRAM}" target="_blank" rel="noopener"><i>@</i>iasmimleao</a>
    </div>
    <div class="insta-side reveal">
      <p>Casos, bastidores do consultório e dicas de prevenção. Mais de 18 mil pessoas acompanham por lá.</p>
      <a class="btn btn--line" href="{INSTAGRAM}" target="_blank" rel="noopener">Seguir no Instagram</a>
    </div>
  </div>
</section>

{faq_block(FAQ_HOME, paper=True)}

{cta("Sua avaliação começa com uma <em>mensagem.</em>", "Escolha o que você procura e o WhatsApp já abre com a mensagem pronta. É só enviar.", msg)}
"""
    return layout("index.html",
                  f"Iasmim Leão | Dentista{EM_CIDADE}: estética e prevenção",
                  f"Iasmim Leão, cirurgiã-dentista ({CRO}){EM_CIDADE}. Prevenção, dentística, clareamento dental e harmonização orofacial. Agende sua avaliação pelo WhatsApp.",
                  body, msg, faq=FAQ_HOME)


# ─────────────────────── páginas de tratamento ───────────────────────
def tratamento(page, nome, h1, lead, linhas, faq, extra="", msg_nome=None, foco=None):
    msg = f"Olá, Iasmim! Vi o seu site e gostaria de saber mais sobre {msg_nome or nome.lower()}."
    rows = "".join(f'<div class="row grid reveal"><h3>{t}</h3><div class="row-body">{c}</div></div>' for t, c in linhas)
    outros = "".join(f'<a class="other reveal" href="{h}"><span>Tratamento</span><b>{n}</b></a>' for h, n, _ in TRATAMENTOS if h != page)
    resumo = next(d for h, _, d in TRATAMENTOS if h == page)
    body = f"""
<section class="page-hero ink">
  <div class="wrap">
    <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a><span aria-hidden="true">/</span><span aria-current="page">{nome}</span></nav>
    <div class="grid">
      <div class="page-hero-text">
        <span class="kicker">Tratamento · {NOME}, {CRO}</span>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="actions"><a class="btn btn--ivory" href="{wa(msg)}" target="_blank" rel="noopener">{WA_ICON}Agendar avaliação</a></div>
      </div>
      <div class="page-hero-side">{SEAL}</div>
    </div>
  </div>
</section>

<section class="section page-body" aria-label="Sobre {nome.lower()}">
  <div class="wrap"><div class="rows">{rows}</div></div>
</section>
{extra}
{faq_block(faq, paper=True)}

<section class="section ink" aria-labelledby="outros-t">
  <div class="wrap">
    <div class="head grid reveal"><div class="head-a"><span class="kicker">Continue</span><h2 id="outros-t">Outros <em>tratamentos.</em></h2></div></div>
    <div class="others">{outros}</div>
  </div>
</section>

{cta("Tire suas dúvidas na <em>avaliação.</em>", "Escolha o que você procura e o WhatsApp já abre com a mensagem pronta. É só enviar.", msg, foco=foco)}
"""
    return body, msg, (nome, resumo)


def page_prevencao():
    faq = [
        ("De quanto em quanto tempo devo fazer limpeza?", "Em geral, a cada seis meses. Quem tem mais tendência a tártaro, gengivite ou cárie pode precisar de intervalos menores, definidos na avaliação."),
        ("Limpeza no dentista desgasta os dentes?", "Não. A limpeza profissional remove placa e tártaro com instrumentos próprios, sem desgastar o esmalte."),
        ("Minha gengiva sangra ao escovar. É normal?", "Não é o esperado. O sangramento costuma indicar inflamação na gengiva e merece uma avaliação."),
    ]
    body, msg, serv = tratamento(
        "prevencao.html", "Prevenção",
        f"Prevenção e limpeza dental{EM_CIDADE}: o <em>começo</em> de tudo.",
        "Consultas de rotina para acompanhar a saúde da boca e resolver cedo o que, mais tarde, daria mais trabalho.",
        [("O que é", "<p>O cuidado feito antes de existir um problema. Inclui a avaliação periódica, a limpeza profissional, que remove placa e tártaro, e a orientação de higiene para o dia a dia.</p>"),
         ("Para quem", "<p>Para todo mundo, em qualquer idade. É especialmente importante para quem está há muito tempo sem ir ao dentista ou pretende fazer um tratamento estético.</p>"),
         ("Como é a consulta", "<p>A dentista examina dentes e gengiva, faz a limpeza quando indicada e mostra onde a escovação e o fio dental podem melhorar.</p><p>Se aparecer algo que precise de tratamento, você fica sabendo ali, com as opções explicadas.</p>"),
         ("Por que antes da estética", "<p>Clareamento, restaurações e harmonização têm resultado melhor e mais seguro em uma boca saudável. Por isso a prevenção vem primeiro.</p>")],
        faq, msg_nome="a consulta de prevenção", foco="Prevenção e limpeza")
    return layout("prevencao.html", f"Prevenção e limpeza dental{EM_CIDADE} | Iasmim Leão",
                  f"Consulta de prevenção e limpeza dental{EM_CIDADE} com Iasmim Leão, cirurgiã-dentista ({CRO}): avaliação, profilaxia e orientação de higiene. Agende pelo WhatsApp.",
                  body, msg, crumb="Prevenção", faq=faq, servico=serv)


def page_dentistica():
    faq = [
        ("Restauração em resina fica da cor do dente?", "Sim. A resina é escolhida no tom do seu dente e esculpida para acompanhar o formato natural."),
        ("Quanto tempo dura uma restauração?", "Depende do tamanho, do local, da mordida e dos seus cuidados. Os retornos de rotina servem para acompanhar e fazer a manutenção."),
        ("Dá para fechar espaço entre os dentes sem aparelho?", "Em alguns casos, sim, com resina. A avaliação mostra se essa é uma boa opção para você ou se outro caminho é mais indicado."),
    ]
    extra = f"""
<section class="section ink" aria-labelledby="cd-t">
  <div class="wrap">
    <div class="head grid reveal"><div class="head-a"><span class="kicker">Casos</span><h2 id="cd-t">Estética do <em>sorriso.</em></h2></div></div>
    <div class="cases">{case(*CASOS[0])}{case(*CASOS[2])}</div>
    <p class="cases-note reveal">{NOTA_CASOS}</p>
  </div>
</section>"""
    body, msg, serv = tratamento(
        "dentistica.html", "Dentística",
        f"Dentística{EM_CIDADE}: restaurar com <em>naturalidade.</em>",
        "A área da odontologia que devolve forma, função e estética aos dentes. É a área de aperfeiçoamento da Iasmim.",
        [("O que é", "<p>A dentística cuida de restaurar os dentes. Pode incluir restaurações em resina na cor do dente, reconstrução de dentes quebrados ou desgastados e ajustes de formato.</p>"),
         ("Para quem", "<p>Para quem tem cárie, restaurações antigas ou escurecidas, dentes lascados, ou quer melhorar o formato e a harmonia do sorriso.</p>"),
         ("Como é a consulta", "<p>Depois do exame, a dentista explica o que pode ser feito e em quantas sessões. Nos procedimentos em resina, o material é aplicado e esculpido diretamente no dente.</p>"),
         ("Cuidados depois", "<p>Boa higiene e retornos periódicos ajudam a manter o resultado. A dentista orienta sobre polimento e manutenção.</p>")],
        faq, extra=extra, foco="Dentística")
    return layout("dentistica.html", f"Dentística e restaurações estéticas{EM_CIDADE} | Iasmim Leão",
                  f"Dentística{EM_CIDADE} com Iasmim Leão ({CRO}), aperfeiçoada na área: restaurações em resina e estética dental com naturalidade. Agende pelo WhatsApp.",
                  body, msg, crumb="Dentística", faq=faq, servico=serv)


def page_clareamento():
    faq = [
        ("Clareamento dental dói?", "O procedimento em si não dói. Algumas pessoas sentem sensibilidade durante o tratamento, que costuma ser passageira e é acompanhada pela dentista."),
        ("Quanto tempo dura o resultado?", "Varia de pessoa para pessoa e depende dos hábitos, como o consumo de café, vinho e cigarro. Os retornos ajudam a manter."),
        ("Clareamento estraga o esmalte?", "Quando indicado e acompanhado por um dentista, o clareamento é um procedimento seguro. O risco está em usar produtos por conta própria."),
        ("Restaurações e coroas clareiam junto?", "Não. O gel age no dente natural. Se você tem restaurações aparentes, a dentista avalia se será preciso trocá-las depois."),
    ]
    extra = f"""
<section class="section ink" aria-labelledby="cc-t">
  <div class="wrap">
    <div class="head grid reveal"><div class="head-a"><span class="kicker">Caso</span><h2 id="cc-t">Clareamento <em>dental.</em></h2></div></div>
    <div class="cases">{case(*CASOS[1])}</div>
    <p class="cases-note reveal">{NOTA_CASOS}</p>
  </div>
</section>"""
    body, msg, serv = tratamento(
        "clareamento-dental.html", "Clareamento dental",
        f"Clareamento dental{EM_CIDADE}, com <em>acompanhamento.</em>",
        "Um bom clareamento começa por saber se ele é indicado para você. A avaliação vem antes do gel.",
        [("O que é", "<p>Um tratamento que clareia a cor dos dentes naturais com um gel próprio. Pode ser feito no consultório, em casa com moldeiras sob orientação da dentista, ou combinando os dois.</p>"),
         ("Para quem", "<p>Para quem tem dentes e gengiva saudáveis e quer um sorriso mais claro. Cáries, gengiva inflamada e sensibilidade são tratadas antes.</p>"),
         ("Como é o tratamento", "<p>Na avaliação, a dentista examina a boca, registra a cor inicial e indica a técnica. Durante o tratamento, ela acompanha a evolução e a sensibilidade.</p>"),
         ("O que esperar", "<p>O resultado varia de pessoa para pessoa. Restaurações e coroas não mudam de cor com o gel, e isso é considerado no planejamento.</p>")],
        faq, extra=extra, msg_nome="o clareamento dental", foco="Clareamento dental")
    return layout("clareamento-dental.html", f"Clareamento dental{EM_CIDADE} | Iasmim Leão",
                  f"Clareamento dental{EM_CIDADE} com avaliação e acompanhamento de Iasmim Leão, cirurgiã-dentista ({CRO}). Tire suas dúvidas e agende pelo WhatsApp.",
                  body, msg, crumb="Clareamento dental", faq=faq, servico=serv)


def page_hof():
    faq = [
        ("Dentista pode fazer harmonização orofacial?", "Sim. A harmonização orofacial é uma especialidade da odontologia, reconhecida pelo Conselho Federal de Odontologia."),
        ("O resultado fica natural?", "O planejamento parte das proporções do seu rosto e do que você espera. Isso é conversado na avaliação, antes de qualquer procedimento."),
        ("Como sei qual procedimento é para mim?", "Só a avaliação responde. Nela a dentista analisa o seu rosto, ouve o que incomoda e explica as opções e os cuidados."),
    ]
    par = f"""<figure class="case single-case reveal">
      <div class="case-pair case-pair--free">
        <div class="case-half">{pic("labios-antes", "Lábios em close, antes do procedimento", 400, 500)}<span class="case-tag">Antes</span></div>
        <div class="case-half">{pic("labios-depois", "Lábios em close, depois do procedimento", 400, 500)}<span class="case-tag case-tag--after">Depois</span></div>
      </div>
      <figcaption><b>Lábios</b><span>Harmonização orofacial</span></figcaption>
    </figure>"""
    extra = f"""
<section class="section ink" aria-labelledby="ch-t">
  <div class="wrap">
    <div class="head grid reveal"><div class="head-a"><span class="kicker">Caso</span><h2 id="ch-t">Harmonização dos <em>lábios.</em></h2></div></div>
    {par}
    <p class="cases-note reveal">{NOTA_CASOS}</p>
  </div>
</section>"""
    body, msg, serv = tratamento(
        "harmonizacao-orofacial.html", "Harmonização orofacial",
        f"Harmonização orofacial{EM_CIDADE}, com olhar de <em>dentista.</em>",
        "Procedimentos estéticos na face e nos lábios, planejados a partir das proporções do seu rosto. A Iasmim é pós-graduanda em Harmonização.",
        [("O que é", "<p>Um conjunto de procedimentos que busca equilíbrio entre o sorriso e o rosto. É uma especialidade da odontologia.</p>"),
         ("Para quem", "<p>Para quem quer cuidar da estética da face e dos lábios com um profissional que conhece a fundo a anatomia da região.</p>"),
         ("Como é a consulta", "<p>A avaliação analisa o rosto, ouve as suas expectativas e verifica se há alguma contraindicação. Só depois disso o procedimento é indicado.</p>"),
         ("Cuidados", "<p>Cada procedimento tem orientações próprias para antes e depois, explicadas pela dentista. O resultado varia de pessoa para pessoa.</p>")],
        faq, extra=extra, msg_nome="a harmonização orofacial", foco="Harmonização orofacial")
    return layout("harmonizacao-orofacial.html", f"Harmonização orofacial{EM_CIDADE} | Iasmim Leão",
                  f"Harmonização orofacial{EM_CIDADE} com Iasmim Leão, cirurgiã-dentista ({CRO}) e pós-graduanda na área. Avaliação individual. Agende pelo WhatsApp.",
                  body, msg, crumb="Harmonização orofacial", faq=faq, servico=serv)


def page_404():
    body = f"""
<section class="page-hero ink" style="min-height:70vh">
  <div class="wrap">
    <span class="kicker">Erro 404</span>
    <h1>Página não <em>encontrada.</em></h1>
    <p class="lead">O endereço pode ter mudado. Volte para o início ou fale com a Iasmim.</p>
    <div class="actions"><a class="btn btn--ivory" href="index.html">Ir para o início</a></div>
  </div>
</section>"""
    return layout("404.html", "Página não encontrada | Iasmim Leão", "Página não encontrada no site de Iasmim Leão, cirurgiã-dentista.", body,
                  "Olá, Iasmim! Vi o seu site.", robots="noindex, follow")


PAGES = {"index.html": page_index, "prevencao.html": page_prevencao, "dentistica.html": page_dentistica,
         "clareamento-dental.html": page_clareamento, "harmonizacao-orofacial.html": page_hof}
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#171210"/>'
           '<circle cx="32" cy="32" r="25.5" fill="none" stroke="#dba892" stroke-width="1"/>'
           '<text x="32" y="44" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="34" fill="#f6f0e8">L</text></svg>')
LOGO_FILE = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 140" role="img" aria-label="Iasmim Leão · Odontologia Estética">'
             '<rect width="140" height="140" fill="#171210"/><defs><path id="c" d="M70 70m-54 0a54 54 0 1 1 108 0a54 54 0 1 1-108 0"/></defs>'
             '<text font-family="Arial, sans-serif" font-size="9.4" letter-spacing="3.4" fill="#f6f0e8"><textPath href="#c" textLength="332">IASMIM LEÃO · ODONTOLOGIA ESTÉTICA · </textPath></text>'
             '<text x="70" y="85" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="46" fill="#f6f0e8">L</text></svg>')
MANIFEST = {"name": MARCA, "short_name": "Iasmim Leão", "start_url": "./index.html", "display": "browser",
            "background_color": "#171210", "theme_color": "#171210", "lang": "pt-BR",
            "icons": [{"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    (OUT / "404.html").write_text(page_404(), encoding="utf-8")
    (OUT / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    (OUT / "logo-iasmim-leao.svg").write_text(LOGO_FILE, encoding="utf-8")
    (OUT / "site.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=1), encoding="utf-8")
    urls = "".join(f"  <url><loc>{url_of(n)}</loc><lastmod>{HOJE}</lastmod></url>\n" for n in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")
    print("ok:", ", ".join(PAGES))
