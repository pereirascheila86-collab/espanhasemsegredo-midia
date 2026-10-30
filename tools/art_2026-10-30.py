"""Artes de 30/10/2026: notícia (6 slides, 1080x1350), Reel VOCÊ SABIA? Todos os Santos (6 telas, 1080x1920 + MP4)
e carrossel Série Arraigo parte 1 (7 slides, 1080x1350).
Uso: ART_OUT=2026-10-30 python3 tools/art_2026-10-30.py [noticia|cultura|imigracao]
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


# ---------------------------------------------------------------- carrossel (1350)
def cslide(bg, ink, accent, kick, title, body, ill, tsize=62, lines=1):
    fy = int(170 + lines * tsize * 1.1 + 28); by = fy + 32; it = by + 235; ih = 1215 - it
    return page(1350, bg, f'''{bracket(56)}
<div class=abs style="left:80px;top:96px"><div class=kick style="color:{accent}">{kick}</div></div>
<div class="abs serif" style="left:80px;top:170px;width:880px;font-size:{tsize}px;line-height:1.1;font-weight:700;color:{ink}">{title}</div>
<div class=abs style="left:80px;top:{fy}px;width:130px;height:5px;background:{GOLD}"></div>
<div class=abs style="left:80px;top:{by}px;width:900px;font-size:37px;line-height:1.38;color:{ink}">{body}</div>
<div class=abs style="left:80px;top:{it}px;width:920px;height:{ih}px">{ill}</div>
{foot(ink, 50)}''')


# ================================================================ NOTÍCIA
def news():
    K = 'Notícia · Espanha'
    # ícones novos: bola, medalha, trilha, prédio, megafone
    ball = lambda x, y, r, c1, c2: (f'<g transform="translate({x} {y})"><circle r="{r}" fill="{c1}"/><circle r="{r}" fill="none" stroke="{c2}" stroke-width="6"/>'
                                    f'<path d="M0 {-r * .38}L{r * .36} {-r * .12}L{r * .22} {r * .3}H{-r * .22}L{-r * .36} {-r * .12}Z" fill="{c2}"/>'
                                    f'<path d="M0 {-r * .38}V{-r}M{r * .36} {-r * .12}L{r * .95} {-r * .3}M{r * .22} {r * .3}L{r * .6} {r * .8}M{-r * .22} {r * .3}L{-r * .6} {r * .8}M{-r * .36} {-r * .12}L{-r * .95} {-r * .3}" stroke="{c2}" stroke-width="6" fill="none"/></g>')
    medal = lambda x, y, s, ribbon, disc, ink: (f'<g transform="translate({x} {y}) scale({s})"><path d="M-46 -150L-6 -30H34L-6 -150Z" fill="{ribbon}"/><path d="M46 -150L6 -30H-34L6 -150Z" fill="{PALEG}"/>'
                                                f'<circle r="78" cy="30" fill="{disc}"/><circle r="60" cy="30" fill="none" stroke="{ink}" stroke-width="6"/>'
                                                f'<path d="M0 -4L11 20L38 24L18 42L23 68L0 55L-23 68L-18 42L-38 24L-11 20Z" fill="{ink}"/></g>')
    # capa
    track = ''.join(f'<ellipse cx="540" cy="1000" rx="{300 + i * 70}" ry="{120 + i * 28}" fill="none" stroke="{GOLD}" stroke-width="4" opacity="{.9 - i * .15}"/>' for i in range(5))
    cover = page(1350, G, f'''
<svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">{track}
<circle cx="880" cy="330" r="360" fill="{G2}"/>
<g>{ball(250, 890, 120, IV, G)}</g>
<g>{medal(820, 840, 1.15, TERRA, GOLD, G)}</g>
<rect x="0" y="1130" width="1080" height="14" fill="{GOLD}"/></svg>
{bracket(56)}
<div class=abs style="left:80px;top:96px"><span class=kick style="color:{PALEG}">{K}</span></div>
<div class="abs serif" style="left:80px;top:190px;width:900px;font-size:84px;line-height:1.08;font-weight:700;color:{IV}">Governo financia <span style="color:{PALEG};font-style:italic">esporte</span> nos centros de acolhimento de migrantes</div>
{foot(IV, 56)}''')
    # 2 o que foi aprovado: documento + valor
    ill2 = sv(f'''<rect x="60" y="20" width="330" height="300" rx="22" fill="{IV}" stroke="{G}" stroke-width="6"/>
<rect x="60" y="20" width="330" height="62" rx="22" fill="{G}"/><rect x="60" y="56" width="330" height="26" fill="{G}"/>
<text x="225" y="64" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="4" fill="{IV}">BOE</text>
{''.join(f'<rect x="92" y="{114 + i * 40}" width="{240 - (i % 2) * 60}" height="14" rx="7" fill="{G}" opacity=".35"/>' for i in range(5))}
<circle cx="330" cy="268" r="34" fill="{TERRA}"/><path d="M314 268L326 280L348 254" fill="none" stroke="{IV}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="450" y="70" width="430" height="200" rx="30" fill="{TERRA}"/>
<text x="665" y="168" text-anchor="middle" font-family="Lora" font-weight="700" font-size="84" fill="{IV}">709.500 €</text>
<text x="665" y="226" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" letter-spacing="4" fill="{PALEG}">SUBVENÇÃO DIRETA</text>''')
    # 3 para quê: prédio do centro + bola + pessoas
    ill3 = sv(f'''<rect x="40" y="300" width="840" height="14" rx="7" fill="{GOLD}"/>
<path d="M90 300V130L260 50L430 130V300Z" fill="{G}"/>
{''.join(f'<rect x="{x}" y="{y}" width="42" height="58" rx="21" fill="{IV}"/>' for x in (130, 200, 270, 340) for y in (150,))}
<rect x="225" y="226" width="70" height="74" rx="35" fill="{GOLD}"/>
{human(560, 130, 1.6, TERRA)}{human(660, 150, 1.4, G)}{human(760, 130, 1.6, GOLD)}
{ball(810, 270, 36, IV, G).replace('stroke="%s"' % G, 'stroke="%s"' % G)}''')
    # 4 divisão: duas barras proporcionais
    ill4 = sv(f'''<rect x="40" y="40" width="{840 * 409.5 / 709.5:.0f}" height="110" rx="22" fill="{G}"/>
<text x="70" y="108" font-family="Lora" font-weight="700" font-size="58" fill="{PALEG}">409.500 €</text>
<text x="{40 + 840 * 409.5 / 709.5 + 20:.0f}" y="108" font-family="Inter" font-weight="800" font-size="26" letter-spacing="3" fill="{G}">AÇÕES</text>
<rect x="40" y="190" width="{840 * 300 / 709.5:.0f}" height="110" rx="22" fill="{TERRA}"/>
<text x="70" y="258" font-family="Lora" font-weight="700" font-size="58" fill="{IV}">300.000 €</text>
<text x="{40 + 840 * 300 / 709.5 + 20:.0f}" y="258" font-family="Inter" font-weight="800" font-size="26" letter-spacing="3" fill="{G}">DIVULGAÇÃO</text>
<g transform="translate(800 90)"><path d="M-40 -20L30 -60V60L-40 20Z" fill="{G}"/><rect x="-62" y="-22" width="28" height="44" rx="6" fill="{G}"/><path d="M50 -30Q76 0 50 30" fill="none" stroke="{G}" stroke-width="7" stroke-linecap="round"/></g>
''')
    # 5 prazos: linha do tempo
    pts = [(140, '15/10/2026', 'BOE'), (350, '27/10/2026', 'Conselho'), (570, '31/10/2027', 'Execução'), (790, '31/01/2028', 'Justificação')]
    ill5 = sv(f'<rect x="60" y="150" width="800" height="10" rx="5" fill="{G}"/>' + ''.join(
        f'<circle cx="{x}" cy="155" r="26" fill="{[TERRA, GOLD, G, G2][i]}" stroke="{IV}" stroke-width="6"/>'
        f'<text x="{x}" y="{100 if i % 2 == 0 else 236}" text-anchor="middle" font-family="Lora" font-weight="700" font-size="34" fill="{G}">{d}</text>'
        f'<text x="{x}" y="{136 if False else (58 if i % 2 == 0 else 276)}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="3" fill="{TERRA}">{t.upper()}</text>'
        for i, (x, d, t) in enumerate(pts)))
    S = [
        cover,
        cslide(IV, G, TERRA, K, 'O que foi aprovado', 'Real Decreto 831/2026, de 14/10, publicado no BOE em 15/10. Concede ao Comité Olímpico Español uma subvenção direta de 709.500 euros, com pagamento único.', ill2),
        cslide(G, IV, PALEG, K, 'Para que serve', 'Promover a prática esportiva nos centros da rede pública de migrações e a integração dos residentes, combatendo o racismo e a discriminação por meio do esporte.', ill3.replace(f'fill="{G}"', f'fill="{G2}"', 1)),
        cslide(SAND, G, TERRA, K, 'Como o valor se divide', 'Ações práticas: palestras em escolas, visitas aos centros, seis medalhistas olímpicos como embaixadores e atividades em cinco centros. O restante vai para divulgação.', ill4),
        cslide(TERRA, IV, PALEG, K, 'Prazos', 'Execução até 31/10/2027 e prestação de contas até 31/01/2028. Em 27/10, o Conselho de Ministros aprovou subvenção ao Comité Paralímpico Español para esporte inclusivo nos mesmos recursos.', ill5.replace(f'fill="{G}"', f'fill="{IV}"').replace(f'fill="{TERRA}"', f'fill="{G}"').replace(f'stroke="{IV}"', f'stroke="{TERRA}"'), tsize=62),
        closing(1350, 'Fontes: BOE (Real Decreto 831/2026) e La Moncloa (Conselho de Ministros de 27/10/2026). Consulta em 30/10/2026.', logo=280),
    ]
    return S


# ================================================================ CULTURA (Reel)
def reel_slide(bg, ink, accent, kick, big, ill):
    return page(1920, bg, f'''{bracket(150, 190)}
<div class=abs style="left:80px;top:170px"><div class=kick style="color:{accent}">{kick}</div><div style="margin-top:14px;width:120px;height:4px;background:{GOLD}"></div></div>
<div class="abs serif" style="left:80px;top:290px;width:900px;font-size:80px;line-height:1.1;font-weight:700;color:{ink}">{big}</div>
<div class=abs style="left:60px;top:800px;width:960px;height:760px">{ill}</div>
{foot(ink, 150)}''')


def culture():
    K = 'VOCÊ SABIA? | ESPANHA'
    V = '0 0 960 760'
    ground = lambda c: f'<rect x="40" y="690" width="880" height="26" rx="13" fill="{c}"/>'
    # flor de crisântemo
    def flower(x, y, r, petal, centre, n=14):
        return f'<g transform="translate({x} {y})">' + ''.join(f'<ellipse transform="rotate({i * 360 / n}) translate(0 {-r * .62})" rx="{r * .17}" ry="{r * .42}" fill="{petal}"/>' for i in range(n)) + f'<circle r="{r * .24}" fill="{centre}"/></g>'
    # 1 capa: velas + flores
    ill1 = sv(f'''{ground(GOLD)}
<g transform="translate(480 0)">
{flower(-250, 330, 150, TERRA, GOLD)}{flower(250, 330, 150, GOLD, TERRA)}
<rect x="-30" y="120" width="60" height="540" rx="16" fill="{IV}"/><ellipse cx="0" cy="120" rx="30" ry="9" fill="{PALEG}"/>
<path d="M0 100C-30 60 -8 30 0 -20C8 30 30 60 0 100Z" fill="{GOLD}"/><path d="M0 98C-14 70 -4 52 0 30C4 52 14 70 0 98Z" fill="{TERRA}"/></g>
<path d="M230 480L230 690M730 480L730 690" stroke="{PALEG}" stroke-width="14" stroke-linecap="round"/>
{flower(250, 560, 90, PALEG, TERRA, 12)}{flower(710, 560, 90, PALEG, TERRA, 12)}''', V)
    # 2 flores no túmulo: lápide em arco + cruz + vaso
    ill2 = sv(f'''{ground(G)}
<path d="M300 690V260C300 140 660 140 660 260V690Z" fill="{G}"/>
<path d="M480 220V380M410 280H550" stroke="{PALEG}" stroke-width="22" stroke-linecap="round"/>
<rect x="400" y="600" width="160" height="90" rx="14" fill="{TERRA}"/>
<path d="M440 600C430 520 400 500 380 470M480 600V450M520 600C530 520 560 500 580 470" stroke="{G2}" stroke-width="10" fill="none" stroke-linecap="round"/>
{flower(380, 460, 70, GOLD, TERRA, 12)}{flower(480, 430, 80, TERRA, GOLD, 14)}{flower(580, 460, 70, GOLD, TERRA, 12)}
{flower(200, 640, 50, TERRA, GOLD, 10)}{flower(760, 640, 50, GOLD, TERRA, 10)}''', V)
    # 3 hueso de santo: ossos de maçapão em bandeja
    bone = lambda x, y, rot, w: (f'<g transform="translate({x} {y}) rotate({rot})"><rect x="{-w / 2}" y="-22" width="{w}" height="44" rx="22" fill="{IV}"/>'
                                 + ''.join(f'<circle cx="{sx * w / 2}" cy="{sy * 24}" r="30" fill="{IV}"/>' for sx in (-1, 1) for sy in (-1, 1)) + f'<rect x="{-w / 2 + 30}" y="-8" width="{w - 60}" height="8" rx="4" fill="{PALEG}"/></g>')
    ill3 = sv(f'''<ellipse cx="480" cy="420" rx="430" ry="260" fill="{GOLD}"/><ellipse cx="480" cy="420" rx="370" ry="210" fill="{G}"/>
{bone(480, 340, -8, 420)}{bone(470, 430, 6, 440)}{bone(490, 520, -4, 400)}
<circle cx="240" cy="230" r="14" fill="{TERRA}"/><circle cx="740" cy="250" r="14" fill="{TERRA}"/>''', V)
    # 4 buñuelo de viento: bolinhos fritos recheados (um cortado)
    bun = lambda x, y, r: f'<g><circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}"/><path d="M{x - r * .6} {y - r * .35}Q{x - r * .2} {y - r * .8} {x + r * .3} {y - r * .65}" stroke="{PALEG}" stroke-width="12" fill="none" stroke-linecap="round"/></g>'
    ill4 = sv(f'''<ellipse cx="480" cy="560" rx="400" ry="90" fill="{G}"/><ellipse cx="480" cy="540" rx="340" ry="62" fill="{G2}"/>
{bun(300, 440, 110)}{bun(660, 450, 100)}{bun(480, 330, 120)}
<g transform="translate(480 330)"><path d="M-120 0A120 120 0 0 1 120 0Z" fill="{GOLD}"/><path d="M-100 0A100 100 0 0 1 100 0Z" fill="{PALEG}"/><path d="M-100 0H100" stroke="{IV}" stroke-width="2"/><path d="M-80 0C-60 40 -30 30 -10 60C20 30 60 40 80 0Z" fill="{IV}"/></g>
<circle cx="400" cy="200" r="10" fill="{TERRA}"/>''', V)
    # 5 castañada: cone de papel com castanhas + fumaça
    chest = lambda x, y, s: f'<g transform="translate({x} {y}) scale({s})"><path d="M-34 -8C-40 -50 40 -50 34 -8C40 30 -40 30 -34 -8Z" fill="{TERRA}"/><path d="M0 -40C-18 -24 -18 -8 0 4C18 -8 18 -24 0 -40Z" fill="{PALEG}"/></g>'
    ill5 = sv(f'''{ground(GOLD)}
<path d="M300 260H660L580 690H380Z" fill="{IV}"/><path d="M330 330H630M345 420H615M365 510H595M385 600H575" stroke="{G}" stroke-width="5" opacity=".25"/>
{chest(380, 240, 1.7)}{chest(480, 210, 1.9)}{chest(580, 240, 1.7)}{chest(430, 300, 1.5)}{chest(540, 300, 1.5)}
<path d="M430 150C410 110 450 90 430 50M530 150C510 110 550 90 530 50M630 160C610 130 640 110 625 80" stroke="{PALEG}" stroke-width="12" fill="none" stroke-linecap="round" opacity=".8"/>
<g transform="translate(180 560)">{chest(0, 0, 1.4)}{chest(70, 30, 1.2)}</g><g transform="translate(700 560)">{chest(0, 20, 1.3)}{chest(70, -10, 1.5)}</g>''', V)
    S = [
        reel_slide(G, IV, PALEG, K, 'Dia de Todos os Santos na Espanha: <span style="color:%s;font-style:italic">flores, doces e tradições</span>' % PALEG, ill1),
        reel_slide(IV, G, TERRA, K, '1º de novembro: dia de lembrar os falecidos, com flores nos túmulos', ill2),
        reel_slide(TERRA, IV, PALEG, K, 'Hueso de santo: rolinho de massa de amêndoa em forma de osso', ill3.replace(f'fill="{G}"', f'fill="{G2}"', 1)),
        reel_slide(SAND, G, TERRA, K, 'Buñuelo de viento: bolinho frito com recheio doce', ill4),
        reel_slide(G, IV, PALEG, K, 'Castañada: no norte, encontro para comer castanhas assadas', ill5),
        closing(1920, 'Fontes: RAE e Ministerio de Educación, Formación Profesional y Deportes. Consulta em 23/10/2026.', logo=400, bottom=160),
    ]
    return S


# ================================================================ IMIGRAÇÃO (Série Arraigo 1)
def imig():
    K = 'Série Arraigo · Parte 1 de 4'
    # capa: árvore com raízes
    roots = ''.join(f'<path d="M540 960C{540 + dx * .4} 1040 {540 + dx} 1080 {540 + dx * 1.3} {1130 + abs(dx) * .1}" stroke="{GOLD}" stroke-width="{10 - abs(dx) // 70}" fill="none" stroke-linecap="round"/>' for dx in (-380, -250, -120, 0, 120, 250, 380))
    leaves = ''.join(f'<circle cx="{540 + 230 * math.cos(a)}" cy="{650 + 210 * math.sin(a) * .8}" r="{44 + (i % 3) * 12}" fill="{[TERRA, GOLD, G2][i % 3]}"/>' for i, a in enumerate([k * 0.55 for k in range(12)]))
    cover = page(1350, IV, f'''<svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">
<rect x="0" y="940" width="1080" height="410" fill="{SAND}"/><rect x="0" y="938" width="1080" height="8" fill="{G}"/>
{roots}{leaves}<circle cx="540" cy="650" r="150" fill="{G}"/>
<path d="M520 960C524 860 516 780 540 640C564 780 556 860 560 960Z" fill="{G}"/>
<path d="M540 760C480 730 450 690 440 640M540 720C600 700 640 660 650 610" stroke="{G}" stroke-width="16" fill="none" stroke-linecap="round"/></svg>
{bracket(56)}
<div class=abs style="left:80px;top:96px"><span class=kick style="color:{TERRA}">Imigração · Série Arraigo</span></div>
<div class="abs serif" style="left:80px;top:160px;width:850px;font-size:78px;line-height:1.08;font-weight:700;color:{G}">Parte 1 de 4: <span style="color:{TERRA};font-style:italic">arraigo social</span></div>
<div class=abs style="left:60px;top:1030px;width:960px;height:180px;border-radius:24px;background:{G}"></div>
<div class=abs style="left:90px;top:1052px;width:900px;font-size:36px;line-height:1.38;color:{IV}">Para quem vive na Espanha sem autorização de residência e comprova vínculos ou integração.</div>
{foot(G, 50)}''')
    # 2 o que é: calendário de 2 anos
    ill2 = sv(f'''<rect x="60" y="20" width="800" height="305" rx="26" fill="{IV}" stroke="{G}" stroke-width="6"/>
<rect x="60" y="20" width="800" height="70" rx="26" fill="{G}"/><rect x="60" y="62" width="800" height="28" fill="{G}"/>
<text x="460" y="70" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" letter-spacing="6" fill="{IV}">2 ANOS SEGUIDOS</text>
{''.join(f'<rect x="{100 + c * 62}" y="{112 + r * 56}" width="48" height="40" rx="9" fill="{TERRA if (r, c) in ((1, 5), (1, 6), (1, 7)) else G}" opacity="{1 if (r, c) in ((1, 5), (1, 6), (1, 7)) else .3}"/>' for r in range(3) for c in range(12))}
<text x="460" y="304" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" fill="{TERRA}">ausências: até 90 dias no total</text>''')
    # 3 vínculo familiar: família + aliança
    ill3 = sv(f'''<rect x="40" y="300" width="840" height="14" rx="7" fill="{GOLD}"/>
{human(330, 120, 1.8, G)}{human(500, 140, 1.6, GOLD)}{human(620, 190, 1.2, TERRA)}
<g transform="translate(130 150)"><circle cx="-26" cy="0" r="40" fill="none" stroke="{GOLD}" stroke-width="14"/><circle cx="26" cy="0" r="40" fill="none" stroke="{G}" stroke-width="14"/></g>
<g transform="translate(780 150)"><path d="M0 70C-70 20 -80 -30 -40 -50C-18 -60 0 -45 0 -28C0 -45 18 -60 40 -50C80 -30 70 20 0 70Z" fill="{TERRA}"/></g>''')
    # 4 informe de integração: documento com selo + prédio
    ill4 = sv(f'''<rect x="60" y="20" width="300" height="300" rx="20" fill="{G}"/>
<path d="M60 90L210 20L360 90Z" fill="{G2}"/>
{''.join(f'<rect x="{x}" y="120" width="30" height="150" fill="{IV}"/>' for x in (95, 160, 225, 290))}<rect x="80" y="276" width="260" height="22" rx="4" fill="{IV}"/>
<rect x="480" y="30" width="330" height="280" rx="18" fill="{IV}" stroke="{G}" stroke-width="6"/>
{''.join(f'<rect x="510" y="{70 + i * 38}" width="{250 - (i % 2) * 70}" height="14" rx="7" fill="{G}" opacity=".35"/>' for i in range(4))}
<circle cx="765" cy="250" r="44" fill="{TERRA}"/><circle cx="765" cy="250" r="32" fill="none" stroke="{IV}" stroke-width="4" stroke-dasharray="6 5"/><path d="M747 250L761 264L787 236" fill="none" stroke="{IV}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<text x="510" y="290" font-family="Inter" font-weight="800" font-size="26" letter-spacing="4" fill="{TERRA}">GRATUITO</text>''')
    # 5 condições: escudo + lista
    ill5 = sv(f'''<path d="M200 20L330 66V170C330 240 280 292 200 324C120 292 70 240 70 170V66Z" fill="{G}"/>
<path d="M200 70V260M150 120H250" stroke="{IV}" stroke-width="0" />
<path d="M140 170L186 216L262 130" fill="none" stroke="{PALEG}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>
{''.join(f'<g transform="translate(450 {52 + i * 92})"><circle r="26" cy="26" cx="26" fill="{[TERRA, GOLD, IV][i]}"/><path d="M14 26L23 35L40 16" fill="none" stroke="{G}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><rect x="76" y="14" width="{[360, 330, 250][i]}" height="24" rx="12" fill="{IV}" opacity=".85"/></g>' for i in range(3))}''')
    # 6 onde pedir: oficina + monitor (sede eletrônica) + relógio 3 meses
    ill6 = sv(f'''<rect x="40" y="300" width="840" height="14" rx="7" fill="{GOLD}"/>
<path d="M60 130L200 50L340 130Z" fill="{G}"/><rect x="80" y="130" width="240" height="170" fill="{G}"/>
{''.join(f'<rect x="{x}" y="160" width="38" height="110" rx="4" fill="{IV}"/>' for x in (100, 160, 222, 282))}
<rect x="400" y="60" width="270" height="180" rx="16" fill="{IV}" stroke="{G}" stroke-width="8"/><rect x="520" y="240" width="30" height="42" fill="{G}"/><rect x="470" y="278" width="130" height="14" rx="7" fill="{G}"/>
<path d="M440 110H630M440 150H600M440 190H560" stroke="{TERRA}" stroke-width="12" stroke-linecap="round"/>
<g transform="translate(780 140)"><circle r="92" fill="{TERRA}"/><circle r="70" fill="{IV}"/><path d="M0 -44V0L32 24" stroke="{G}" stroke-width="12" fill="none" stroke-linecap="round"/><text y="134" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" fill="{TERRA}" letter-spacing="3">3 MESES</text></g>''')
    S = [
        cover,
        cslide(G, IV, PALEG, K, 'O que é', 'Autorização de residência para quem está na Espanha sem autorização de residência. Requisito: 2 anos seguidos no país, com ausências de até 90 dias no total.', ill2.replace(f'fill="{G}"', f'fill="{G2}"', 0)),
        cslide(IV, G, TERRA, K, 'Com vínculo familiar', 'Cônjuge, parceiro registrado ou familiar de 1º grau com residência na Espanha. Exige meios econômicos.', ill3),
        cslide(SAND, G, TERRA, K, 'Sem vínculo familiar', 'Informe de integração social, emitido pela Comunidade Autônoma ou pela prefeitura do seu empadronamiento. É gratuito.', ill4),
        cslide(TERRA, IV, PALEG, K, 'Condições para os dois caminhos', 'Sem antecedentes penais na Espanha e nos países onde viveu nos últimos 5 anos, não representar ameaça à ordem pública, à segurança ou à saúde pública, e pagar a taxa.', ill5.replace(f'fill="{G}"', f'fill="{G2}"', 1), tsize=56, lines=2),
        cslide(IV, G, TERRA, K, 'Onde pedir e duração', 'Oficina de Extranjería do seu domicílio, presencial ou pela sede eletrônica. A ficha oficial prevê resposta em até 3 meses. Vale 1 ano e permite trabalhar. TIE: até 1 mês após a concessão.', ill6, tsize=56),
        closing(1350, 'Amanhã, parte 2: arraigo sociolaboral<br>Fonte: Ministerio de Inclusión, Seguridad Social y Migraciones. Consulta em 28/10/2026.', logo=250, bottom=50),
    ]
    return S


async def render(S, prefix, h):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': h})
        for i, htm in enumerate(S):
            await pg.set_content(htm)
            await pg.wait_for_timeout(400)
            await pg.screenshot(path=OUT + f'{prefix}-{i + 1}.png')
        await b.close()


which = sys.argv[1:] or ['noticia', 'cultura', 'imigracao']
if 'noticia' in which:
    asyncio.run(render(news(), 'noticia', 1350))
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
