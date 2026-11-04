"""Arte de 04/11/2026: carrossel Prorroga (7 slides 1080x1350) e Reel VOCÊ SABIA? Fallas de Valência (5 telas 1080x1920 + MP4).
Uso: ART_OUT=2026-11-04 python3 tools/art_2026-11-04.py [imigracao|cultura]
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





def star(cx, cy, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts.append(f'{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{col}"/>'


def star_ring(cx, cy, R, r, col, n=12):
    return ''.join(star(cx + R * math.cos(2 * math.pi * k / n), cy + R * math.sin(2 * math.pi * k / n), r, col) for k in range(n))


def txt(x, y, s, size, col, w=800, fam='Inter', ls=0, anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{size}" letter-spacing="{ls}" fill="{col}">{s}</text>'


def rrect(x, y, w, h, r, fill, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'


def imig():
    V = '0 0 920 560'
    K = 'Imigração · Estância'
    # capa: ampulheta + linha do tempo que se estende
    hour = f'''<svg class=abs style="left:640px;top:760px" width="330" height="440" viewBox="0 0 330 440">
<rect x="20" y="10" width="290" height="36" rx="12" fill="{GOLD}"/><rect x="20" y="394" width="290" height="36" rx="12" fill="{GOLD}"/>
<path d="M50 46H280C280 150 190 190 190 220C190 250 280 290 280 394H50C50 290 140 250 140 220C140 190 50 150 50 46Z" fill="{IV}" opacity=".16" stroke="{IV}" stroke-width="6"/>
<path d="M90 70H240C230 130 180 170 165 210C150 170 100 130 90 70Z" fill="{TERRA}"/>
<path d="M120 394C130 330 150 300 165 300C180 300 200 330 210 394Z" fill="{PALEG}"/></svg>'''
    bar = ''.join(f'<rect x="{80 + i * 60}" y="1180" width="52" height="26" rx="6" fill="{GOLD if i < 6 else TERRA}"/>' for i in range(8))
    capa = page(1350, G, f'''{bracket(56)}
<div class=abs style="left:80px;top:96px"><div class=kick style="color:{PALEG}">{K}</div></div>
<div class="abs serif" style="left:70px;top:190px;font-size:196px;line-height:1;font-weight:700;color:{GOLD};letter-spacing:-4px">Prorroga</div>
<div class=abs style="left:80px;top:420px;width:300px;height:6px;background:{TERRA}"></div>
<div class="abs serif" style="left:80px;top:470px;width:600px;font-size:76px;line-height:1.1;font-weight:700;color:{IV}">O que é e quando se aplica</div>
<div class=abs style="left:80px;top:880px;width:520px;font-size:34px;line-height:1.4;color:{IV};opacity:.92">Estância de curta duração, estudos e voluntariado, segundo as fontes oficiais.</div>
{hour}
<svg class=abs style="left:0;top:0" width=1080 height=1350>{bar}<path d="M570 1193H640M620 1170L650 1193L620 1216" fill="none" stroke="{PALEG}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>
{foot(IV, 50)}''')
    # 2 o que é: barra de 180 dias com 90 destacados
    seg = ''.join(f'<rect x="{50 + i * 41}" y="250" width="36" height="86" rx="6" fill="{TERRA if i < 9 else G}" opacity="{1 if i < 9 else .28}"/>' for i in range(20))
    i2 = sv(f'''{seg}
<path d="M50 220H410" stroke="{G}" stroke-width="6" stroke-linecap="round"/><path d="M50 205V235M410 205V235" stroke="{G}" stroke-width="6"/>
{txt(230, 180, '90 dias', 56, TERRA, 800, 'Lora')}
<path d="M50 372H870" stroke="{G}" stroke-width="3" stroke-dasharray="4 10"/>{txt(460, 428, 'dentro de cada semestre (180 dias)', 34, G, 600)}
{rrect(120, 470, 680, 62, 31, G)}{txt(460, 513, 'prórroga ou autorização de residência', 26, IV, 700)}''', V)
    # 3 quem pode: passaporte aprovado + maleta cortada
    ill3 = sv(f'''
{rrect(90, 90, 270, 380, 22, G)}{rrect(106, 106, 238, 348, 14, G2)}<circle cx="225" cy="235" r="62" fill="none" stroke="{GOLD}" stroke-width="8"/>
<path d="M225 173V297M163 235H287M181 191Q225 235 181 279M269 191Q225 235 269 279" fill="none" stroke="{GOLD}" stroke-width="5"/>
{txt(225, 385, 'PASSAPORTE', 28, GOLD, 800, 'Inter', 4)}
<circle cx="345" cy="120" r="46" fill="{TERRA}"/><path d="M325 120L340 136L367 104" fill="none" stroke="{IV}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
{rrect(530, 220, 300, 220, 26, G)}<path d="M610 220V190Q610 168 632 168H728Q750 168 750 190V220" fill="none" stroke="{G}" stroke-width="18"/>
{rrect(530, 300, 300, 22, 6, GOLD)}
<circle cx="680" cy="330" r="150" fill="none" stroke="{TERRA}" stroke-width="16" opacity=".95"/><path d="M574 224L786 436" stroke="{TERRA}" stroke-width="16"/>''', V)
    # 4 com visto: página de visto + linha do tempo com limite
    ill4 = sv(f'''
{rrect(50, 60, 360, 230, 18, IV, f'stroke="{G}" stroke-width="5"')}{rrect(80, 92, 130, 100, 10, GOLD)}{rrect(230, 100, 150, 14, 7, G)}{rrect(230, 130, 110, 14, 7, G)}{rrect(230, 160, 130, 14, 7, G)}{rrect(80, 220, 300, 12, 6, G, 'opacity=".4"')}
{txt(145, 154, 'VISTO', 26, G, 800, 'Inter', 3)}
<path d="M70 450H850" stroke="{G}" stroke-width="8" stroke-linecap="round"/>
{rrect(70, 420, 270, 60, 10, G2)}{rrect(340, 420, 250, 60, 10, TERRA, 'opacity=".75"')}
<path d="M590 380V520" stroke="{TERRA}" stroke-width="8"/><path d="M590 380H690L670 400L690 420H590Z" fill="{TERRA}"/>
{txt(205, 535, 'visto: menos de 3 meses', 26, G, 700)}{txt(465, 358, 'prórroga', 28, TERRA, 800)}{txt(720, 535, 'limite: 90 de 180 dias', 26, G, 700)}''', V)
    # 5 sem visto: porta estreita com fechadura e selo
    ill5 = sv(f'''
<path d="M330 520V190Q330 70 460 70Q590 70 590 190V520Z" fill="{G}"/><path d="M360 520V200Q360 100 460 100Q560 100 560 200V520Z" fill="{G2}"/>
<circle cx="460" cy="300" r="34" fill="{GOLD}"/><path d="M460 300V362" stroke="{GOLD}" stroke-width="16" stroke-linecap="round"/><circle cx="460" cy="298" r="12" fill="{G}"/>
{rrect(250, 520, 420, 22, 11, G)}
<g transform="rotate(-12 760 190)"><circle cx="760" cy="190" r="112" fill="none" stroke="{TERRA}" stroke-width="10"/><circle cx="760" cy="190" r="92" fill="none" stroke="{TERRA}" stroke-width="3"/>{txt(760, 186, 'CASOS', 32, TERRA, 800, 'Inter', 4)}{txt(760, 224, 'EXCEPCIONAIS', 20, TERRA, 800, 'Inter', 1)}</g>
<g fill="{GOLD}"><circle cx="120" cy="140" r="14"/><circle cx="120" cy="210" r="14"/><circle cx="120" cy="280" r="14"/><circle cx="120" cy="350" r="14"/><circle cx="120" cy="420" r="14"/></g>
<g fill="{G}" opacity=".35">{rrect(150, 132, 120, 14, 7, G)}{rrect(150, 202, 100, 14, 7, G)}{rrect(150, 272, 120, 14, 7, G)}{rrect(150, 342, 90, 14, 7, G)}{rrect(150, 412, 110, 14, 7, G)}</g>''', V)
    # 6 estudos e voluntariado: janela do pedido em volta do vencimento + capelo
    ill6 = sv(f'''
<path d="M60 360H860" stroke="{IV}" stroke-width="8" stroke-linecap="round"/>
{rrect(140, 300, 330, 120, 16, GOLD, 'opacity=".95"')}{rrect(470, 300, 400, 120, 16, IV)}
<path d="M470 240V470" stroke="{IV}" stroke-width="8"/><path d="M470 240H600L578 266L600 292H470Z" fill="{IV}"/>
{txt(305, 372, '2 meses antes', 34, G, 800)}{txt(670, 372, '3 meses depois', 34, G, 800)}{txt(620, 282, 'vencimento', 30, PALEG, 700, 'Inter', 0, 'start')}
<g transform="translate(130 20)"><path d="M0 70L130 20L260 70L130 120Z" fill="{IV}"/><path d="M50 100V160Q130 200 210 160V100L130 138Z" fill="{PALEG}"/><path d="M250 74V150" stroke="{GOLD}" stroke-width="7"/><circle cx="250" cy="156" r="10" fill="{GOLD}"/></g>
{txt(305, 520, 'Estudos: até 2 prórrogas', 32, IV, 700)}{txt(670, 520, 'Voluntariado: 1 vez', 32, IV, 700)}''', V)
    kw = dict(tsize=64, lines=2)
    return [capa,
        cslide(IV, G, TERRA, 'O que é', 'Estância de curta duração', 'É de até 90 dias por semestre. Para ficar além disso, é preciso uma prórroga de estância ou uma autorização de residência.', i2, **kw),
        cslide(SAND, G, TERRA, 'Quem pode', 'Quem entrou sem fim de trabalho ou residência', 'Segue dentro do período de estância. Quem tem visto de busca de emprego fica de fora.', ill3, tsize=62, lines=2),
        cslide(G, IV, PALEG, 'Com visto', 'Visto de menos de 3 meses', 'A estância pode ser prorrogada, mas nunca passar de 90 dias em qualquer período de 180.', ill4, **kw),
        cslide(IV, G, TERRA, 'Sem visto', 'Além de 3 meses, só excepcionalmente', 'Razões humanitárias, familiares, de atenção sanitária, de interesse público ou outra excepcional. Na prática, depende exclusivamente das autoridades espanholas.', ill5, tsize=60, lines=2),
        cslide(TERRA, IV, PALEG, 'Estudos e voluntariado', 'Quando pedir a prórroga', 'De 2 meses antes a 3 meses depois do vencimento. Estudos: até 2 prórrogas. Voluntariado: uma só vez. Cada uma, no máximo 1 ano.', ill6, **kw),
        closing(1350, 'Fontes: Ministerio del Interior e Ministerio de Inclusión. Consulta em 23/10/2026.', logo=300, bottom=60)]


def culture():
    K = 'VOCÊ SABIA? | ESPANHA'
    V = '0 0 960 760'
    ground = lambda c: f'<rect x="40" y="712" width="880" height="24" rx="12" fill="{c}"/>'

    def ninot(cx, base, s, body, hat, face=IV):
        r = 54 * s
        return (f'<rect x="{cx - 34 * s}" y="{base - 120 * s}" width="{68 * s}" height="{120 * s}" rx="{22 * s}" fill="{body}"/>'
                f'<circle cx="{cx}" cy="{base - 120 * s - r + 20 * s}" r="{r}" fill="{face}"/>'
                f'<path d="M{cx - r * 1.1} {base - 120 * s - r * 1.2 + 20 * s}H{cx + r * 1.1}L{cx + r * .55} {base - 120 * s - r * 2.0 + 20 * s}H{cx - r * .55}Z" fill="{hat}"/>'
                f'<circle cx="{cx - r * .32}" cy="{base - 120 * s - r + 14 * s}" r="{6 * s}" fill="{INK}"/><circle cx="{cx + r * .32}" cy="{base - 120 * s - r + 14 * s}" r="{6 * s}" fill="{INK}"/>'
                f'<path d="M{cx - r * .3} {base - 120 * s - r * .5 + 20 * s}Q{cx} {base - 120 * s - r * .15 + 20 * s} {cx + r * .3} {base - 120 * s - r * .5 + 20 * s}" fill="none" stroke="{INK}" stroke-width="{5 * s}" stroke-linecap="round"/>')
    # 1 monumento: pedestal em degraus, ninots e bandeirolas
    flags = ''.join(f'<path d="M{60 + i * 110} 70L{115 + i * 110} 70L{88 + i * 110} 130Z" fill="{[GOLD, IV, G2][i % 3]}"/>' for i in range(8))
    ill1 = sv(f'''<path d="M40 60Q480 150 920 60" fill="none" stroke="{IV}" stroke-width="5"/>{flags}{ground(GOLD)}
{rrect(180, 620, 600, 92, 10, G)}{rrect(260, 520, 440, 100, 10, G2)}{rrect(340, 440, 280, 80, 10, GOLD)}
{ninot(250, 620, 1.0, TERRA, G)}{ninot(710, 620, 1.0, IV, GOLD)}{ninot(480, 440, 1.7, G, GOLD)}
<g fill="{PALEG}"><circle cx="150" cy="690" r="14"/><circle cx="810" cy="690" r="14"/><circle cx="120" cy="650" r="10"/><circle cx="840" cy="650" r="10"/></g>''', V)
    # 2 diploma/pergaminho com selo 2016
    ill2 = sv(f'''
{rrect(150, 120, 660, 480, 24, IV)}{rrect(180, 150, 600, 420, 14, 'none', f'stroke="{G}" stroke-width="5"')}
{rrect(150, 100, 660, 50, 25, GOLD)}{rrect(150, 570, 660, 50, 25, GOLD)}
{txt(480, 250, 'LISTA REPRESENTATIVA', 34, G, 800, 'Inter', 5)}{txt(480, 300, 'DO PATRIMÔNIO CULTURAL IMATERIAL', 24, G, 700, 'Inter', 3)}
{rrect(330, 330, 300, 6, 3, TERRA)}{txt(480, 450, '2016', 120, TERRA, 700, 'Lora')}
<g transform="translate(715 500)"><path d="M-40 60L-60 150L-20 125L10 150L20 60Z" fill="{TERRA}"/><circle cx="0" cy="0" r="78" fill="{GOLD}"/><circle cx="0" cy="0" r="60" fill="none" stroke="{G}" stroke-width="4"/>{star(0, 0, 36, G)}</g>''', V)
    # 3 calendário MARÇO + fogos e música
    bursts = ''.join(f'<path d="M{cx} {cy}L{cx + 70 * math.cos(math.radians(a)):.0f} {cy + 70 * math.sin(math.radians(a)):.0f}" stroke="{col}" stroke-width="8" stroke-linecap="round"/>' for cx, cy, col in [(160, 170, TERRA), (790, 130, G)] for a in range(0, 360, 45))
    ill3 = sv(f'''{ground(G)}{bursts}
{rrect(260, 150, 440, 520, 28, IV)}{rrect(260, 150, 440, 140, 28, TERRA)}{rrect(260, 250, 440, 40, 0, TERRA)}
{txt(480, 258, 'MARÇO', 84, IV, 800, 'Lora', 4)}
{''.join(f'<circle cx="{320 + c * 56}" cy="{350 + r * 62}" r="15" fill="{G}" opacity="{.28 if not (r == 3 and c >= 1) else 1}"/>' for r in range(4) for c in range(6))}
<circle cx="376" cy="598" r="22" fill="{GOLD}"/><circle cx="432" cy="598" r="22" fill="{GOLD}"/><circle cx="488" cy="598" r="22" fill="{GOLD}"/>
<path d="M160 640V540L230 520V620" fill="none" stroke="{G}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><circle cx="148" cy="644" r="22" fill="{G}"/><circle cx="218" cy="624" r="22" fill="{G}"/>
''', V)
    # 4 queima: chamas sobre a falla (silhueta)
    flame = lambda cx, w, h, col: f'<path d="M{cx - w} 712C{cx - w} 560 {cx - w * .4} 520 {cx} {712 - h}C{cx + w * .5} 540 {cx + w} 600 {cx + w} 712Z" fill="{col}"/>'
    ill4 = sv(f'''{ground(IV)}
{rrect(260, 600, 440, 112, 10, SAND, 'opacity=".25"')}
{flame(200, 110, 520, TERRA)}{flame(480, 180, 660, TERRA)}{flame(760, 110, 480, TERRA)}
{flame(330, 100, 400, GOLD)}{flame(620, 100, 430, GOLD)}{flame(480, 110, 440, GOLD)}{flame(480, 60, 250, PALEG)}
<g fill="{GOLD}"><circle cx="300" cy="120" r="9"/><circle cx="640" cy="90" r="7"/><circle cx="520" cy="60" r="8"/><circle cx="400" cy="180" r="6"/><circle cx="760" cy="170" r="9"/><circle cx="170" cy="210" r="7"/></g>
<g transform="translate(850 560)"><path d="M0 150V60" stroke="{IV}" stroke-width="10" stroke-linecap="round"/>{''.join(f'<ellipse cx="0" cy="40" rx="18" ry="38" fill="{IV}" transform="rotate({a} 0 60)"/>' for a in range(0, 360, 72))}<circle cx="0" cy="60" r="16" fill="{GOLD}"/></g>''', V)
    return [
        reel_slide(TERRA, IV, PALEG, K, 'As Fallas de Valência são <span style="color:%s;font-style:italic">Patrimônio Imaterial</span> da UNESCO' % PALEG, ill1),
        reel_slide(IV, G, TERRA, K, 'Em 2016, entraram na Lista do Patrimônio Cultural Imaterial da Humanidade', ill2),
        reel_slide(SAND, G, TERRA, K, 'Celebrada em março, a festa tem a falla no centro: ninots de artistas e artesãos', ill3),
        reel_slide(G, IV, PALEG, K, 'No fim, a falla é queimada: simboliza a chegada da primavera', ill4),
        closing(1920, 'Fontes: UNESCO (Lista Representativa, Valencia Fallas festivity) e The Local (2/12/2016). Consulta em 04/11/2026.', logo=400, bottom=160),
    ]


which = sys.argv[1:] or ['imigracao', 'cultura']
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
