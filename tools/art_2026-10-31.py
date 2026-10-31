"""Artes de 31/10/2026: Reel VOCÊ SABIA? Dieta mediterrânea (5 telas, 1080x1920 + MP4) e carrossel Série Arraigo parte 2 (7 slides, 1080x1350).
Uso: ART_OUT=2026-10-31 python3 tools/art_2026-10-31.py [cultura|imigracao]
"""
import base64, asyncio, os, subprocess, sys, math
from playwright.async_api import async_playwright

B = os.path.dirname(os.path.abspath(__file__)) + '/../'
OUT = os.environ.get('ART_OUT', B + 'saida/') + '/'
os.makedirs(OUT, exist_ok=True)
LOGO = 'data:image/png;base64,' + base64.b64encode(open(B + 'marca/logo-espanha-sem-segredo.png', 'rb').read()).decode()
G = '#0F3D3A'; G2 = '#1E5550'; GOLD = '#C9A24A'; TERRA = '#B8573A'; IV = '#F5F1E8'; INK = '#24292C'; SAND = '#E9DFC9'; PALEG = '#F3D79A'

CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;overflow:hidden;font-family:Inter,Arial,sans-serif;position:relative}
.serif{font-family:Lora,Georgia,serif}.abs{position:absolute}
.foot{position:absolute;left:80px;right:80px;display:flex;align-items:center;gap:18px}
.foot img{width:68px;height:68px}.foot .n{font-family:Lora,serif;font-style:italic;font-size:30px;letter-spacing:.12em}
.kick{font-size:28px;letter-spacing:.2em;font-weight:700;text-transform:uppercase}'''


def bracket(top, size=200):
    return f'<svg class=abs style="right:56px;top:{top}px" width="{size}" height="{size}" viewBox="0 0 {size} {size}"><path d="M0 2H{size - 2}V{size}" fill="none" stroke="{GOLD}" stroke-width="4"/></svg>'


def foot(col, bottom):
    return f'<div class=foot style="bottom:{bottom}px"><img src="{LOGO}"><span class=n style="color:{col}">Espanha Sem Segredo</span></div>'


def page(h, bg, inner):
    return f'<html><head><meta charset=utf8><style>{CSS} body{{height:{h}px;background:{bg}}}</style></head><body>{inner}</body></html>'


def sv(inner, vb='0 0 920 340'):
    return f'<svg width="100%" height="100%" viewBox="{vb}">{inner}</svg>'


def human(cx, y, s, col, head=None):
    h = head or col
    r = 15 * s
    return (f'<circle cx="{cx}" cy="{y + r}" r="{r}" fill="{h}"/>'
            f'<rect x="{cx - 20 * s}" y="{y + 2.4 * r}" width="{40 * s}" height="{58 * s}" rx="{14 * s}" fill="{col}"/>'
            f'<rect x="{cx - 20 * s}" y="{y + 2.4 * r + 44 * s}" width="{16 * s}" height="{40 * s}" rx="{6 * s}" fill="{col}"/>'
            f'<rect x="{cx + 4 * s}" y="{y + 2.4 * r + 44 * s}" width="{16 * s}" height="{40 * s}" rx="{6 * s}" fill="{col}"/>')


def closing(h, fontes, extra='', logo=300, bottom=70):
    top = 150 if h == 1350 else 330
    t = top + logo + 50
    return page(h, IV, f'''{bracket(56 if h == 1350 else 150)}
<div class=abs style="left:0;right:0;top:{top}px;display:flex;justify-content:center"><img src="{LOGO}" width="{logo}" height="{logo}"></div>
<div class="abs serif" style="left:80px;right:80px;top:{t}px;text-align:center;font-size:66px;line-height:1.14;font-weight:700;color:{G}">Aqui você fica por dentro de tudo sobre a Espanha</div>
<div class=abs style="left:50%;margin-left:-65px;top:{t + 66 * 3 + 30}px;width:130px;height:5px;background:{GOLD}"></div>
<div class="abs serif" style="left:80px;right:80px;top:{t + 66 * 3 + 64}px;text-align:center;font-size:52px;font-weight:700;color:{TERRA}">Espanha Sem Segredo</div>
<div class=abs style="left:80px;right:80px;top:{t + 66 * 3 + 140}px;text-align:center;font-size:38px;color:{G}">Siga <b>@espanhasemsegredo</b></div>
{extra}
<div class=abs style="left:90px;right:90px;bottom:{bottom}px;text-align:center;font-size:24px;line-height:1.5;color:{G};opacity:.9">{fontes}<br>Conteúdo informativo, não é assessoria jurídica.</div>''')



def cslide(bg, ink, accent, kick, title, body, ill, tsize=62, lines=1):
    fy = int(170 + lines * tsize * 1.1 + 28); by = fy + 32; it = by + 235; ih = 1215 - it
    return page(1350, bg, f'''{bracket(56)}
<div class=abs style="left:80px;top:96px"><div class=kick style="color:{accent}">{kick}</div></div>
<div class="abs serif" style="left:80px;top:170px;width:880px;font-size:{tsize}px;line-height:1.1;font-weight:700;color:{ink}">{title}</div>
<div class=abs style="left:80px;top:{fy}px;width:130px;height:5px;background:{GOLD}"></div>
<div class=abs style="left:80px;top:{by}px;width:900px;font-size:37px;line-height:1.38;color:{ink}">{body}</div>
<div class=abs style="left:80px;top:{it}px;width:920px;height:{ih}px">{ill}</div>
{foot(ink, 50)}''')



def reel_slide(bg, ink, accent, kick, big, ill):
    return page(1920, bg, f'''{bracket(150, 190)}
<div class=abs style="left:80px;top:170px"><div class=kick style="color:{accent}">{kick}</div><div style="margin-top:14px;width:120px;height:4px;background:{GOLD}"></div></div>
<div class="abs serif" style="left:80px;top:290px;width:900px;font-size:80px;line-height:1.1;font-weight:700;color:{ink}">{big}</div>
<div class=abs style="left:60px;top:800px;width:960px;height:760px">{ill}</div>
{foot(ink, 150)}''')



async def render(S, prefix, h):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': h})
        for i, htm in enumerate(S):
            await pg.set_content(htm)
            await pg.wait_for_timeout(400)
            await pg.screenshot(path=OUT + f'{prefix}-{i + 1}.png')
        await b.close()



# ================================================================ CULTURA: dieta mediterrânea (5 telas)
def culture():
    K = 'VOCÊ SABIA? | ESPANHA'
    V = '0 0 960 760'
    ground = lambda c: f'<rect x="40" y="690" width="880" height="26" rx="13" fill="{c}"/>'

    def leaf(x, y, rot, l, col):
        return f'<ellipse transform="translate({x} {y}) rotate({rot})" rx="{l * .2}" ry="{l * .5}" fill="{col}"/>'

    def olive(x, y, r, col, hi):
        return f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 1.25}" fill="{col}"/><ellipse cx="{x - r * .3}" cy="{y - r * .4}" rx="{r * .2}" ry="{r * .4}" fill="{hi}" opacity=".6"/>'

    # 1 capa: galho de oliveira + azeite + pão sobre a mesa
    ly = lambda x: 330 - 0.2857 * (x - 120)
    lv = ''.join(leaf(170 + i * 52, ly(170 + i * 52) + (-34 if i % 2 else 34), (-35 if i % 2 else 35) - 16, 130, [G2, G][i % 2]) for i in range(10))
    ill1 = sv(f'''{ground(GOLD)}
<path d="M120 330C300 300 480 250 680 170" stroke="{PALEG}" stroke-width="12" fill="none" stroke-linecap="round"/>
{lv}{olive(300, ly(300) + 26, 26, G, PALEG)}{olive(440, ly(440) + 26, 26, TERRA, PALEG)}{olive(580, ly(580) + 26, 26, G, PALEG)}
<path d="M640 420L760 420L780 690L620 690Z" fill="{GOLD}"/><rect x="660" y="360" width="80" height="70" rx="10" fill="{GOLD}"/><rect x="672" y="330" width="56" height="40" rx="8" fill="{TERRA}"/>
<path d="M640 560H760" stroke="{G}" stroke-width="8"/><path d="M650 600H750" stroke="{G}" stroke-width="8"/>
<path d="M130 690C110 540 220 480 340 520C460 480 560 540 540 690Z" fill="{TERRA}"/><path d="M200 640C260 590 320 590 380 640M290 560C330 540 370 545 410 575" stroke="{PALEG}" stroke-width="10" fill="none" stroke-linecap="round" opacity=".8"/>''', V)
    # 2 2013: selo/rolo de pergaminho com o ano
    ill2 = sv(f'''{ground(G)}
<rect x="170" y="90" width="620" height="520" rx="22" fill="{G}"/>
<rect x="170" y="70" width="620" height="44" rx="22" fill="{GOLD}"/><rect x="170" y="590" width="620" height="44" rx="22" fill="{GOLD}"/>
<text x="480" y="400" text-anchor="middle" font-family="Lora" font-weight="700" font-size="230" fill="{IV}">2013</text>
<path d="M270 190H690M270 480H690" stroke="{PALEG}" stroke-width="5" stroke-dasharray="2 14" stroke-linecap="round"/>
<text x="480" y="170" text-anchor="middle" font-family="Inter" font-weight="800" font-size="28" letter-spacing="8" fill="{PALEG}">INSCRIÇÃO NA UNESCO</text>
<g transform="translate(740 560)"><path d="M-34 20L-48 110L0 84L48 110L34 20Z" fill="{TERRA}"/><circle r="64" fill="{TERRA}"/><circle r="50" fill="none" stroke="{PALEG}" stroke-width="4" stroke-dasharray="6 5"/><path d="M-22 -2L-6 14L24 -18" fill="none" stroke="{PALEG}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>''', V)
    # 3 mais que comida: mesa com pessoas compartilhando um prato
    ill3 = sv(f'''{ground(GOLD)}
<rect x="130" y="470" width="700" height="26" rx="13" fill="{G}"/><rect x="190" y="496" width="22" height="194" fill="{G}"/><rect x="750" y="496" width="22" height="194" fill="{G}"/>
<ellipse cx="480" cy="460" rx="190" ry="34" fill="{TERRA}"/><ellipse cx="480" cy="450" rx="150" ry="22" fill="{GOLD}"/>
{olive(420, 436, 16, G, PALEG)}{olive(470, 428, 16, TERRA, PALEG)}{olive(520, 436, 16, G, PALEG)}
{human(250, 250, 2.0, G2)}{human(480, 190, 2.0, TERRA)}{human(710, 250, 2.0, G2)}
<g transform="translate(160 140)"><rect width="130" height="56" rx="28" fill="{IV}"/><path d="M26 56L18 84L46 56Z" fill="{IV}"/><path d="M26 28H104" stroke="{TERRA}" stroke-width="8" stroke-linecap="round"/></g>
<g transform="translate(680 120)"><rect width="130" height="56" rx="28" fill="{IV}"/><path d="M104 56L112 84L84 56Z" fill="{IV}"/><path d="M26 28H104" stroke="{G}" stroke-width="8" stroke-linecap="round"/></g>''', V)
    # 4 sete países: anel de 7 marcadores com Espanha ao centro
    names = ['Chipre', 'Croácia', 'Grécia', 'Itália', 'Marrocos', 'Portugal']
    ring = ''
    for i, nm in enumerate(names):
        a = -math.pi / 2 + i * 2 * math.pi / 6
        cx = 480 + 300 * math.cos(a); cy = 360 + 270 * math.sin(a)
        ring += f'<line x1="480" y1="360" x2="{cx:.0f}" y2="{cy:.0f}" stroke="{GOLD}" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/><g transform="translate({cx:.0f} {cy:.0f})"><rect x="-90" y="-30" width="180" height="60" rx="30" fill="{G}"/><text y="10" text-anchor="middle" font-family="Inter" font-weight="700" font-size="30" fill="{IV}">{nm}</text></g>'
    ill4 = sv(f'''{ring}<circle cx="480" cy="360" r="112" fill="{IV}" stroke="{GOLD}" stroke-width="8"/><text x="480" y="372" text-anchor="middle" font-family="Lora" font-weight="700" font-size="48" fill="{TERRA}">Espanha</text>
<text x="480" y="418" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="5" fill="{G}">7 PAÍSES</text>''', V)
    S = [
        reel_slide(G, IV, PALEG, K, 'Dieta mediterrânea: <span style="color:%s;font-style:italic">Patrimônio Imaterial</span> da UNESCO' % PALEG, ill1),
        reel_slide(IV, G, TERRA, K, '2013: entrou na Lista do Patrimônio Cultural Imaterial', ill2),
        reel_slide(TERRA, IV, PALEG, K, 'Segundo a UNESCO, vai além da comida: saberes, habilidades, rituais, símbolos e tradições', ill3.replace(f'fill="{G}"', f'fill="{G2}"')),
        reel_slide(SAND, G, TERRA, K, 'A inscrição reúne sete países, incluindo a Espanha', ill4),
        closing(1920, 'Fonte: UNESCO, Patrimônio Cultural Imaterial. Consulta em 23/10/2026.', logo=400, bottom=160),
    ]
    return S


# ================================================================ IMIGRAÇÃO: Série Arraigo 2 (sociolaboral)
def imig():
    K = 'Série Arraigo · Parte 2 de 4'
    # capa: pasta de trabalho + contrato + caneta
    cover = page(1350, G, f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:repeating-linear-gradient(135deg,rgba(201,162,74,.07) 0 2px,transparent 2px 38px)"></div>
<svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">
<rect x="150" y="760" width="780" height="360" rx="34" fill="{TERRA}"/><path d="M400 760V700C400 668 424 646 456 646H624C656 646 680 668 680 700V760" fill="none" stroke="{TERRA}" stroke-width="30"/>
<rect x="150" y="900" width="780" height="22" fill="{G}" opacity=".35"/><rect x="496" y="880" width="88" height="82" rx="14" fill="{GOLD}"/>
<g transform="translate(250 470) rotate(-6)"><rect width="360" height="440" rx="18" fill="{IV}"/>
<path d="M44 70H316M44 120H316M44 170H250" stroke="{G}" stroke-width="12" stroke-linecap="round" opacity=".3"/>
<path d="M44 360C80 310 100 400 140 350C170 310 190 390 230 340" stroke="{TERRA}" stroke-width="8" fill="none" stroke-linecap="round"/><text x="44" y="300" font-family="Inter" font-weight="800" font-size="26" letter-spacing="6" fill="{G}">CONTRATO</text></g>
<g transform="translate(700 400) rotate(28)"><rect width="34" height="360" rx="10" fill="{GOLD}"/><path d="M0 360H34L17 410Z" fill="{PALEG}"/><rect y="0" width="34" height="50" rx="10" fill="{TERRA}"/></g>
<circle cx="800" cy="610" r="0" fill="none"/>
</svg>
{bracket(56)}
<div class=abs style="left:80px;top:96px"><span class=kick style="color:{GOLD}">Imigração · Série Arraigo</span></div>
<div class="abs serif" style="left:80px;top:160px;width:880px;font-size:76px;line-height:1.08;font-weight:700;color:{IV}">Parte 2 de 4: <span style="color:{GOLD};font-style:italic">arraigo sociolaboral</span></div>
<div class=abs style="left:80px;top:330px;width:900px;font-size:38px;line-height:1.38;color:{IV}">Para quem já vive e trabalha na Espanha.</div>
{foot(IV, 50)}''')
    # 2 para quem é: mapa estilizado + anel de 24 meses
    seg = ''.join(f'<path d="M{660 + 150 * math.cos(a):.1f} {170 + 150 * math.sin(a):.1f} L{660 + 108 * math.cos(a):.1f} {170 + 108 * math.sin(a):.1f}" stroke="{TERRA if i < 24 else G}" stroke-width="13" stroke-linecap="round"/>'
                  for i in range(24) for a in [-math.pi / 2 + i * 2 * math.pi / 24])
    ill2 = sv(f'''<path d="M70 120L170 60L330 70L450 110L420 190L440 250L360 300L240 292L130 300L90 230L110 180Z" fill="{G}"/>
<circle cx="300" cy="170" r="30" fill="{TERRA}"/><circle cx="300" cy="170" r="12" fill="{IV}"/><path d="M300 200V250" stroke="{TERRA}" stroke-width="8" stroke-linecap="round"/>
{seg}<text x="660" y="168" text-anchor="middle" font-family="Lora" font-weight="700" font-size="70" fill="{G}">2</text>
<text x="660" y="206" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="5" fill="{G}">ANOS</text>
<text x="660" y="352" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" fill="{TERRA}">ausências: até 90 dias</text>''', '0 0 860 370')
    # 3 contrato: folha com carimbo + relógio 20h
    ill3 = sv(f'''<rect x="60" y="20" width="400" height="330" rx="20" fill="{IV}"/>
<text x="90" y="80" font-family="Inter" font-weight="800" font-size="26" letter-spacing="6" fill="{TERRA}">CONTRATO</text>
<path d="M90 120H430M90 164H430M90 208H360" stroke="{G}" stroke-width="12" stroke-linecap="round" opacity=".3"/>
<path d="M92 300C130 250 150 340 190 290C220 250 240 330 280 280" stroke="{TERRA}" stroke-width="7" fill="none" stroke-linecap="round"/>
<g transform="translate(680 180)"><circle r="150" fill="{G}"/><circle r="128" fill="{IV}"/>
{''.join(f'<path d="M{104 * math.cos(a):.1f} {104 * math.sin(a):.1f}L{122 * math.cos(a):.1f} {122 * math.sin(a):.1f}" stroke="{G}" stroke-width="7" stroke-linecap="round"/>' for a in [k * math.pi / 6 for k in range(12)])}
<path d="M0 0V-80M0 0L52 30" stroke="{TERRA}" stroke-width="14" stroke-linecap="round"/><circle r="12" fill="{G}"/>
<text y="226" text-anchor="middle" font-family="Inter" font-weight="800" font-size="28" letter-spacing="3" fill="{PALEG}">20 H / SEMANA</text></g>''', '0 0 920 420')
    # 4 empregador: prédio de escritórios + dois selos
    wins = ''.join(f'<rect x="{150 + c * 70}" y="{90 + r * 64}" width="40" height="38" rx="5" fill="{IV}" opacity="{.95 if (r + c) % 3 else .45}"/>' for r in range(3) for c in range(4))
    ill4 = sv(f'''<rect x="30" y="170" width="110" height="170" rx="8" fill="{G2}"/><rect x="120" y="40" width="330" height="300" rx="10" fill="{G}"/><rect x="170" y="14" width="230" height="40" rx="8" fill="{G2}"/><path d="M285 14V-10" stroke="{G}" stroke-width="6"/><path d="M285 -10H325L310 2L325 14H285Z" fill="{TERRA}"/>
{wins}<rect x="250" y="262" width="72" height="78" rx="4" fill="{GOLD}"/><path d="M286 262V340" stroke="{G}" stroke-width="4"/>
<g transform="translate(600 120)"><circle r="68" fill="{TERRA}"/><circle r="54" fill="none" stroke="{IV}" stroke-width="4" stroke-dasharray="6 5"/><path d="M-26 0L-8 18L28 -20" fill="none" stroke="{IV}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>
<g transform="translate(600 280)"><circle r="68" fill="{GOLD}"/><circle r="54" fill="none" stroke="{G}" stroke-width="4" stroke-dasharray="6 5"/><path d="M-26 0L-8 18L28 -20" fill="none" stroke="{G}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>
<text x="700" y="128" font-family="Inter" font-weight="800" font-size="26" fill="{G}" letter-spacing="2">FAZENDA</text><text x="700" y="288" font-family="Inter" font-weight="800" font-size="26" fill="{G}" letter-spacing="2">SEGURIDADE</text>''', '0 0 920 390')
    # 5 o que não vale: lojinha por conta própria com sinal de proibido
    ill5 = sv(f'''<rect x="150" y="150" width="340" height="190" fill="{IV}"/>
<path d="M120 150L160 60H480L520 150Z" fill="{TERRA}"/>{''.join(f'<path d="M{120 + i * 80} 150L{160 + i * 80 - 10} 60H{200 + i * 80 - 10}L{200 + i * 80} 150Z" fill="{PALEG}" opacity=".85"/>' for i in (1, 3, 5) if False)}
<path d="M120 150Q160 190 200 150Q240 190 280 150Q320 190 360 150Q400 190 440 150Q480 190 520 150" fill="{TERRA}"/>
<rect x="200" y="210" width="80" height="130" rx="6" fill="{G}"/><rect x="320" y="210" width="130" height="80" rx="6" fill="{G}"/>
<g transform="translate(680 190)"><circle r="120" fill="none" stroke="{IV}" stroke-width="26"/><path d="M-84 -84L84 84" stroke="{IV}" stroke-width="26" stroke-linecap="round"/></g>
<text x="680" y="360" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" letter-spacing="4" fill="{PALEG}">CONTA PRÓPRIA</text>''', '0 0 920 380')
    # 6 como pedir e duração: pilha de papéis, carimbo e selo 1 ano
    ill6 = sv(f'''<rect x="90" y="70" width="330" height="270" rx="14" fill="{G}" opacity=".18" transform="rotate(-4 255 200)"/>
<rect x="100" y="50" width="330" height="270" rx="14" fill="{IV}" stroke="{G}" stroke-width="6"/>
<path d="M140 110H390M140 156H390M140 202H320" stroke="{G}" stroke-width="12" stroke-linecap="round" opacity=".3"/>
<g transform="translate(330 270) rotate(-12)"><rect x="-90" y="-34" width="180" height="68" rx="10" fill="none" stroke="{TERRA}" stroke-width="7"/><text y="14" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" letter-spacing="6" fill="{TERRA}">PEDIDO</text></g>
<g transform="translate(700 180)"><path d="M-34 90L-52 190L0 160L52 190L34 90Z" fill="{GOLD}"/><circle r="110" fill="{G}"/><circle r="92" fill="none" stroke="{PALEG}" stroke-width="4" stroke-dasharray="8 7"/>
<text y="22" text-anchor="middle" font-family="Lora" font-weight="700" font-size="92" fill="{IV}">1</text><text y="64" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" letter-spacing="6" fill="{PALEG}">ANO</text></g>''', '0 0 920 420')
    S = [
        cover,
        cslide(IV, G, TERRA, K, 'Para quem é', 'Quem tem pelo menos 2 anos de permanência continuada na Espanha, com ausências de até 90 dias no total, e não é solicitante de proteção internacional.', ill2),
        cslide(TERRA, IV, PALEG, K, 'O contrato', 'Um ou mais contratos de trabalho, com salário mínimo ou o do convênio coletivo, somando no mínimo 20 horas por semana. Contratos temporários precisam passar de 90 dias.', ill3.replace(f'fill="{G}"', f'fill="{G2}"', 1), tsize=62),
        cslide(SAND, G, TERRA, K, 'O empregador', 'Precisa estar em dia com as obrigações com a Fazenda e a Seguridade Social e ter meios para manter o contrato de trabalho.', ill4),
        cslide(G, IV, PALEG, K, 'O que não vale', 'O arraigo sociolaboral é para trabalho por conta alheia. A atividade por conta própria não entra neste tipo de autorização.', ill5),
        cslide(IV, G, TERRA, K, 'Como pedir e duração', 'Oficina de Extranjería do seu domicílio, presencial ou pela sede eletrônica, com antecedentes penais e taxa. A ficha oficial prevê resposta em até 3 meses. A autorização vale 1 ano.', ill6, tsize=58),
        closing(1350, 'Amanhã, parte 3: arraigo socioformativo<br>Fonte: Ministerio de Inclusão, consulta em 28/10/2026.'.replace('Inclusão', 'Inclusión'), logo=250, bottom=50),
    ]
    return S


which = sys.argv[1:] or ['cultura', 'imigracao']
if 'imigracao' in which:
    asyncio.run(render(imig(), 'imigracao', 1350))
if 'cultura' in which:
    S = culture()
    asyncio.run(render(S, 'cultura', 1920))
    n = len(S); d = 3.5; f = 0.4
    cmd = ['ffmpeg', '-y', '-loglevel', 'error']
    for i in range(n):
        cmd += ['-loop', '1', '-t', str(d), '-i', OUT + f'cultura-{i + 1}.png']
    flt = ''.join(f'[{i}:v]format=yuv420p,fade=t=in:st=0:d={f},fade=t=out:st={d - f}:d={f}[v{i}];' for i in range(n))
    flt += ''.join(f'[v{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0[o]'
    cmd += ['-filter_complex', flt, '-map', '[o]', '-r', '30', '-pix_fmt', 'yuv420p', OUT + 'reel-cultura.mp4']
    subprocess.run(cmd, check=True)
