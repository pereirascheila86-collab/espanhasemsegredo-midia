"""Artes de 01/11/2026: Reel VOCÊ SABIA? Jamón ibérico (6 telas, 1080x1920 + MP4) e carrossel Série Arraigo parte 3 (7 slides, 1080x1350).
Uso: ART_OUT=2026-11-01 python3 tools/art_2026-11-01.py [cultura|imigracao]
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





def ham_leg(cx, cy, s, body, bone, hoof):
    # perna de jamón: corpo ovalado, casco e osso
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M-40 -230C40 -250 150 -190 160 -60C170 80 90 190 20 230L-10 240L-30 210C-110 150 -170 20 -130 -110C-110 -180 -80 -220 -40 -230Z" fill="{body}"/>'
            f'<path d="M-20 -150C40 -160 100 -110 100 -40" fill="none" stroke="{bone}" stroke-width="10" stroke-linecap="round" opacity=".55"/>'
            f'<rect x="-30" y="226" width="44" height="70" rx="12" fill="{bone}"/>'
            f'<path d="M-34 296H18L10 336H-26Z" fill="{hoof}"/></g>')


def tag(cx, cy, col, txt, tc):
    return (f'<g transform="translate({cx} {cy})"><path d="M0 -90V-20" stroke="{tc}" stroke-width="5"/>'
            f'<rect x="-70" y="-20" width="140" height="64" rx="12" fill="{col}"/><circle cx="-46" cy="12" r="7" fill="{tc}" opacity=".6"/>'
            f'<text x="14" y="22" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="3" fill="{tc}">{txt}</text></g>')


def spain_map(col, ox=0, oy=0, sc=1.0):
    return (f'<g transform="translate({ox} {oy}) scale({sc})"><path d="M60 120L170 70L330 78L470 60L560 100L600 180L560 250L520 330L430 390L330 410L230 440L130 400L90 320L50 240Z" fill="{col}"/></g>')


def pin(x, y, col, ring, lbl, lc, dx=0, dy=-62):
    return (f'<circle cx="{x}" cy="{y}" r="30" fill="{ring}" opacity=".35"/><circle cx="{x}" cy="{y}" r="15" fill="{col}"/>'
            f'<text x="{x + dx}" y="{y + dy}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" fill="{lc}">{lbl}</text>')


def culture():
    K = 'VOCÊ SABIA? | ESPANHA'
    V = '0 0 960 760'
    ground = lambda c: f'<rect x="40" y="710" width="880" height="24" rx="12" fill="{c}"/>'
    # 1 capa: perna de jamón sobre tábua com faca e azeitonas
    ill1 = sv(f'''{ground(GOLD)}
<rect x="90" y="560" width="780" height="120" rx="30" fill="{TERRA}"/><rect x="90" y="650" width="780" height="40" rx="20" fill="{G2}" opacity=".6"/>
{ham_leg(430, 330, 1.0, TERRA, PALEG, G)}
<path d="M600 610L860 560" stroke="{PALEG}" stroke-width="12" stroke-linecap="round"/><path d="M600 610L690 545L720 600Z" fill="{PALEG}"/>
<ellipse cx="160" cy="640" rx="34" ry="42" fill="{G}"/><ellipse cx="148" cy="624" rx="7" ry="14" fill="{PALEG}" opacity=".6"/>
<ellipse cx="225" cy="650" rx="34" ry="42" fill="{GOLD}"/>''', V)
    # 2 Guijuelo: mapa com pino em Salamanca (oeste-centro) e flocos de frio
    snow = ''.join(f'<g transform="translate({x} {y})" stroke="{IV}" stroke-width="6" stroke-linecap="round"><path d="M0 -26V26M-23 -13L23 13M-23 13L23 -13"/></g>' for x, y in [(700, 150), (790, 260), (720, 380), (830, 120)])
    ill2 = sv(f'''{spain_map(G, 40, 60, 1.0)}{pin(200, 290, TERRA, GOLD, 'Guijuelo', G, 30, -48)}
<path d="M200 290L330 250" stroke="{GOLD}" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round"/>
<g transform="translate(700 250)"><rect x="-120" y="-120" width="240" height="240" rx="26" fill="{TERRA}"/>{snow.replace('translate(700 150)','translate(0 0)') if False else ''}
<path d="M-60 40Q0 -50 60 40" fill="none" stroke="{IV}" stroke-width="10" stroke-linecap="round"/><path d="M-70 -30H70M-70 0H40" stroke="{PALEG}" stroke-width="8" stroke-linecap="round" opacity=".7"/>
<text y="86" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" letter-spacing="3" fill="{IV}">FRIO E SECO</text></g>''', V)
    # 3 Dehesa de Extremadura: azinheiras com porcos escuros
    def tree(x, y, s):
        return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-14" y="0" width="28" height="170" rx="8" fill="{INK}"/>'
                f'<circle cx="-70" cy="-10" r="70" fill="{G2}"/><circle cx="60" cy="-30" r="80" fill="{G}"/><circle cx="-5" cy="-80" r="70" fill="{G2}"/></g>')
    def pig(x, y, s, col):
        return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="76" ry="46" fill="{col}"/><ellipse cx="82" cy="-8" rx="34" ry="30" fill="{col}"/>'
                f'<path d="M96 -36L112 -62L122 -30Z" fill="{col}"/><ellipse cx="112" cy="2" rx="12" ry="9" fill="{TERRA}"/><circle cx="92" cy="-14" r="4" fill="{IV}"/>'
                f'<rect x="-52" y="30" width="16" height="42" rx="6" fill="{col}"/><rect x="26" y="30" width="16" height="42" rx="6" fill="{col}"/></g>')
    acorns = ''.join(f'<g transform="translate({x} {y})"><ellipse rx="12" ry="16" fill="{GOLD}"/><path d="M-14 -8Q0 -24 14 -8Z" fill="{TERRA}"/></g>' for x, y in [(660, 620), (730, 640), (790, 615)])
    ill3 = sv(f'''<rect x="40" y="560" width="880" height="170" rx="30" fill="{GOLD}" opacity=".5"/>
{tree(220, 190, 1.1)}{tree(720, 220, 0.95)}{pig(380, 600, 0.9, INK)}{pig(540, 560, 0.7, INK)}{acorns}
<text x="480" y="700" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="6" fill="{TERRA}">CÁCERES · BADAJOZ</text>''', V)
    # 4 Jabugo + Los Pedroches: dois pontos no sul, duas etiquetas
    ill4 = sv(f'''{spain_map(G, 40, 20, 1.0)}
{pin(190, 400, TERRA, GOLD, 'Jabugo', IV, 0, 66)}{pin(380, 340, GOLD, TERRA, 'Pedroches', IV, 0, -44)}
<g transform="translate(720 450)"><rect x="-190" y="-100" width="380" height="200" rx="22" fill="{TERRA}"/><text y="-20" text-anchor="middle" font-family="Lora" font-weight="700" font-size="46" fill="{IV}">Los Pedroches</text><text y="30" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" letter-spacing="4" fill="{PALEG}">RECONHECIDA EM 2006</text><text y="72" text-anchor="middle" font-family="Inter" font-weight="600" font-size="22" fill="{IV}">norte de Córdoba</text></g>''', V)
    # 5 precinto preto: etiqueta preta presa a um jamón, quatro cores em fileira
    cols = [(INK, 'PRETO'), (TERRA, 'VERMELHO'), (GOLD, 'VERDE?'), (SAND, 'BRANCO')]
    ill5 = sv(f'''{ground(G)}
{ham_leg(230, 330, 0.85, TERRA, PALEG, G)}
<path d="M260 150C300 100 360 90 440 110" stroke="{INK}" stroke-width="8" fill="none"/>
<g transform="translate(620 330)"><rect x="-190" y="-170" width="380" height="340" rx="26" fill="{INK}"/><circle cx="0" cy="-70" r="56" fill="none" stroke="{GOLD}" stroke-width="8"/><circle cx="0" cy="-70" r="14" fill="{GOLD}"/>
<text y="50" text-anchor="middle" font-family="Inter" font-weight="800" font-size="44" letter-spacing="6" fill="{IV}">PRECINTO</text><text y="108" text-anchor="middle" font-family="Lora" font-weight="700" font-size="62" fill="{GOLD}">PRETO</text></g>''', V)
    ill5 = ill5.replace('fill="#C9A24A"/><text y="108"', 'fill="#C9A24A"/><text y="108"')
    S = [
        reel_slide(G, IV, PALEG, K, 'Jamón ibérico: <span style="color:%s;font-style:italic">não é tudo igual</span>' % PALEG, ill1),
        reel_slide(IV, G, TERRA, K, 'Guijuelo, em Salamanca: clima frio e seco, segundo o Spain.info', ill2),
        reel_slide(SAND, G, TERRA, K, 'Dehesa de Extremadura: porcos criados em Cáceres e Badajoz', ill3),
        reel_slide(TERRA, IV, PALEG, K, 'Jabugo, em Huelva, e Los Pedroches, no norte de Córdoba', ill4),
        reel_slide(IV, G, TERRA, K, 'Precinto preto: pela norma nacional, jamón de bellota 100% ibérico', ill5),
        closing(1920, 'Fontes: Spain.info (Turespaña) e BOE, RD 4/2014. Consulta em 23/10/2026.', logo=400, bottom=160),
    ]
    return S


def imig():
    K = 'Série Arraigo · Parte 3 de 4'
    # capa: capelo + livros empilhados + calendário
    cover = page(1350, G, f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:repeating-linear-gradient(45deg,rgba(201,162,74,.07) 0 2px,transparent 2px 40px)"></div>
<svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">
<rect x="170" y="1010" width="560" height="70" rx="12" fill="{TERRA}"/><rect x="200" y="930" width="500" height="80" rx="12" fill="{GOLD}"/><rect x="150" y="850" width="540" height="80" rx="12" fill="{IV}"/>
<path d="M190 890H650M230 970H660M200 1045H700" stroke="{G}" stroke-width="6" opacity=".4"/>
<g transform="translate(470 640)"><path d="M0 -120L260 -20L0 80L-260 -20Z" fill="{IV}"/><path d="M-150 40V150Q0 230 150 150V40L0 100Z" fill="{GOLD}"/>
<path d="M230 -4V170" stroke="{GOLD}" stroke-width="8"/><circle cx="230" cy="190" r="22" fill="{TERRA}"/></g>
<g transform="translate(820 1000)"><rect x="-130" y="-130" width="260" height="260" rx="20" fill="{IV}"/><rect x="-130" y="-130" width="260" height="70" rx="20" fill="{TERRA}"/>
<text y="40" text-anchor="middle" font-family="Lora" font-weight="700" font-size="120" fill="{G}">2</text><text y="96" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="6" fill="{G}">MESES</text></g>
</svg>
{bracket(56)}
<div class=abs style="left:80px;top:96px"><span class=kick style="color:{GOLD}">Imigração · Série Arraigo</span></div>
<div class="abs serif" style="left:80px;top:160px;width:880px;font-size:76px;line-height:1.08;font-weight:700;color:{IV}">Parte 3 de 4: <span style="color:{GOLD};font-style:italic">arraigo socioformativo</span></div>
<div class=abs style="left:80px;top:340px;width:900px;font-size:38px;line-height:1.38;color:{IV}">Para quem vive na Espanha e vai estudar.</div>
{foot(IV, 50)}''')
    # 2 para quem é: pessoa com mochila + faixa de 2 anos e 90 dias
    bar = ''.join(f'<rect x="{60 + i * 34}" y="270" width="26" height="50" rx="6" fill="{TERRA}"/>' for i in range(24))
    ill2 = sv(f'''{human(150, 20, 2.0, G)}{bar}<text x="60" y="362" font-family="Inter" font-weight="800" font-size="26" letter-spacing="3" fill="{G}">2 ANOS CONTÍNUOS</text>
<g transform="translate(560 60)"><rect width="260" height="150" rx="22" fill="{G}"/><text x="130" y="82" text-anchor="middle" font-family="Lora" font-weight="700" font-size="76" fill="{IV}">90</text><text x="130" y="122" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="3" fill="{PALEG}">DIAS NO MÁXIMO</text></g>
<text x="690" y="244" text-anchor="middle" font-family="Inter" font-weight="700" font-size="24" fill="{G}">de ausência, no total</text>''', '0 0 920 380')
    # 3 formações: quatro cartões-ícone
    def card(x, y, ic, l1, l2, col, tc):
        return f'<g transform="translate({x} {y})"><rect width="420" height="150" rx="20" fill="{col}"/>{ic}<text x="150" y="68" font-family="Inter" font-weight="800" font-size="27" fill="{tc}">{l1}</text><text x="150" y="104" font-family="Inter" font-weight="800" font-size="27" fill="{tc}">{l2}</text></g>'
    ic_book = lambda c: f'<rect x="28" y="36" width="44" height="78" rx="6" fill="{c}"/><rect x="78" y="36" width="44" height="78" rx="6" fill="{c}" opacity=".75"/>'
    ic_cert = lambda c: f'<rect x="26" y="34" width="84" height="64" rx="8" fill="{c}"/><circle cx="68" cy="108" r="16" fill="{c}"/>'
    ic_gear = lambda c: f'<circle cx="68" cy="75" r="36" fill="{c}"/><circle cx="68" cy="75" r="14" fill="{TERRA}"/>' + ''.join(f'<rect x="62" y="22" width="12" height="20" rx="4" fill="{c}" transform="rotate({a} 68 75)"/>' for a in range(0, 360, 60))
    ic_adult = lambda c: f'<circle cx="52" cy="56" r="16" fill="{c}"/><rect x="34" y="76" width="36" height="46" rx="12" fill="{c}"/><circle cx="92" cy="62" r="13" fill="{c}"/><rect x="78" y="78" width="28" height="42" rx="10" fill="{c}"/>'
    ill3 = sv(card(40, 20, ic_book(IV), 'Secundário', 'pós-obrigatório', G, IV) +
              card(500, 20, ic_cert(IV), 'Certificados', 'profissionais', G2, IV) +
              card(40, 200, ic_gear(IV), 'Ciclos de', 'grau médio', G2, IV) +
              card(500, 200, ic_adult(IV), 'Ensino de', 'adultos', G, IV), '0 0 920 370')
    # 4 informe: documento com selo + prefeitura
    ill4 = sv(f'''<g transform="translate(70 20)"><rect width="330" height="340" rx="18" fill="{IV}"/><text x="30" y="60" font-family="Inter" font-weight="800" font-size="24" letter-spacing="5" fill="{TERRA}">INFORME</text>
<path d="M30 100H300M30 140H300M30 180H230" stroke="{G}" stroke-width="12" stroke-linecap="round" opacity=".3"/><circle cx="250" cy="270" r="52" fill="{TERRA}"/><circle cx="250" cy="270" r="40" fill="none" stroke="{IV}" stroke-width="3" stroke-dasharray="5 5"/><path d="M228 270L244 286L274 252" fill="none" stroke="{IV}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>
<g transform="translate(520 40)"><path d="M0 100L160 20L320 100Z" fill="{GOLD}"/><rect x="20" y="100" width="280" height="20" fill="{G}"/>{''.join(f'<rect x="{34 + i * 62}" y="124" width="30" height="130" rx="6" fill="{IV}"/>' for i in range(5))}<rect x="0" y="254" width="320" height="30" rx="8" fill="{G}"/>
<text x="160" y="336" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="3" fill="{PALEG}">GRÁTIS · VALE 6 MESES</text></g>''', '0 0 920 370')
    # 5 prazos: linha do tempo com marcos 2 meses antes / 3 meses depois
    ill5 = sv(f'''<path d="M60 190H860" stroke="{IV}" stroke-width="10" stroke-linecap="round"/>
<g transform="translate(180 190)"><circle r="40" fill="{TERRA}"/><text y="14" text-anchor="middle" font-family="Lora" font-weight="700" font-size="40" fill="{IV}">2</text><text y="-70" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="3" fill="{PALEG}">MESES ANTES</text><text y="100" text-anchor="middle" font-family="Inter" font-weight="600" font-size="23" fill="{IV}">do prazo de matrícula:</text><text y="130" text-anchor="middle" font-family="Inter" font-weight="800" font-size="25" fill="{PALEG}">fazer o pedido</text></g>
<g transform="translate(460 190)"><rect x="-44" y="-44" width="88" height="88" rx="14" fill="{GOLD}"/><path d="M-24 0L-6 18L26 -16" fill="none" stroke="{G}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><text y="-70" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="3" fill="{PALEG}">CONCESSÃO</text></g>
<g transform="translate(740 190)"><circle r="40" fill="{GOLD}"/><text y="14" text-anchor="middle" font-family="Lora" font-weight="700" font-size="40" fill="{G}">3</text><text y="-70" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="3" fill="{PALEG}">MESES DEPOIS</text><text y="100" text-anchor="middle" font-family="Inter" font-weight="600" font-size="23" fill="{IV}">da concessão:</text><text y="130" text-anchor="middle" font-family="Inter" font-weight="800" font-size="25" fill="{PALEG}">provar a matrícula</text></g>''', '0 0 920 370')
    # 6 trabalhar: balança estudo x trabalho, 30 h
    ill6 = sv(f'''<path d="M460 80V320M380 320H540" stroke="{G}" stroke-width="12" stroke-linecap="round"/><path d="M180 130H740" stroke="{G}" stroke-width="12" stroke-linecap="round"/><circle cx="460" cy="80" r="22" fill="{GOLD}"/>
<path d="M180 130L120 230H240Z M740 130L680 230H800Z" fill="none" stroke="{G}" stroke-width="5"/>
<path d="M90 230H270Q270 290 180 290Q90 290 90 230Z" fill="{TERRA}"/><path d="M650 230H830Q830 290 740 290Q650 290 650 230Z" fill="{G}"/>
<path d="M130 190L180 165L230 190L180 213Z" fill="{G}"/><rect x="168" y="196" width="24" height="18" fill="{G}" opacity="0"/>
<rect x="700" y="170" width="80" height="56" rx="8" fill="{GOLD}"/><path d="M724 170V158H756V170" fill="none" stroke="{GOLD}" stroke-width="8"/>
<text x="740" y="344" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" fill="{TERRA}">até 30 h / semana</text>''', '0 0 920 370')
    S = [
        cover,
        cslide(IV, G, TERRA, K, 'Para quem é', 'Quem tem pelo menos 2 anos de permanência continuada na Espanha, com ausências de até 90 dias no total, e não é solicitante de proteção internacional.', ill2, tsize=62),
        cslide(SAND, G, TERRA, K, 'Formações aceitas', 'Secundário pós-obrigatório em tempo integral que dê título, certificados profissionais completos, ensino de adultos presencial ou ciclos de grau médio.', ill3),
        cslide(G, IV, PALEG, K, 'Informe de integração social', 'Emitido pela Comunidade Autônoma ou pela prefeitura do lugar onde você está empadronado. É gratuito, sai em até 1 mês e vale 6 meses.', ill4, tsize=58),
        cslide(TERRA, IV, PALEG, K, 'Prazos que importam', 'Se a matrícula tem prazo oficial, o pedido é feito nos 2 meses anteriores ao início. A prova da matrícula é entregue em até 3 meses após a concessão.', ill5.replace(f'fill="{G}"', f'fill="{G2}"')),
        cslide(IV, G, TERRA, K, 'Trabalhar enquanto estuda', 'Permitido trabalhar por conta alheia até 30 horas por semana, com pelo menos o salário mínimo ou o do convênio. Duração da autorização: 1 ano.', ill6, tsize=58),
        closing(1350, 'Próximo sábado, parte 4: arraigo familiar<br>Fonte: Ministerio de Inclusión, consulta em 28/10/2026.', logo=250, bottom=50),
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
