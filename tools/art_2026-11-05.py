"""Arte de 05/11/2026: noticia (Estatuto da cidadania no exterior), imigracao (Atividades formativas, Hoja 2), Reel VOCE SABIA? Alhambra.
Uso: ART_OUT=2026-11-05 python3 tools/art_2026-11-05.py [noticia|imigracao|cultura]"""
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
    import re, math as _m
    plain = re.sub('<[^>]+>', '', body)
    bl = _m.ceil(len(plain) / 46)
    fy = int(170 + lines * tsize * 1.1 + 28); by = fy + 32; it = by + bl * 48 + 30; ih = 1215 - it
    return page(1350, bg, f'''{bracket(56)}
<div class=abs style="left:80px;top:96px"><div class=kick style="color:{accent}">{kick}</div></div>
<div class="abs serif" style="left:80px;top:170px;width:880px;font-size:{tsize}px;line-height:1.1;font-weight:700;color:{ink}">{title}</div>
<div class=abs style="left:80px;top:{fy}px;width:130px;height:5px;background:{GOLD}"></div>
<div class=abs style="left:80px;top:{by}px;width:900px;font-size:35px;line-height:1.38;color:{ink}">{body}</div>
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


# ---------- helpers de ícones novos (05/11) ----------
def house(x, y, s, col, roof=None, door=IV):
    roof = roof or col
    return (f'<path d="M{x - 60 * s} {y}L{x} {y - 55 * s}L{x + 60 * s} {y}Z" fill="{roof}"/>'
            f'<rect x="{x - 48 * s}" y="{y}" width="{96 * s}" height="{70 * s}" fill="{col}"/>'
            f'<rect x="{x - 12 * s}" y="{y + 28 * s}" width="{24 * s}" height="{42 * s}" rx="{4 * s}" fill="{door}"/>')


def arch(cx, top, w, h, col, inner=None):
    """arco de ferradura (mourisco): w largura, h altura total"""
    r = w / 2
    d = (f'M{cx - r * .72} {top + h}L{cx - r * .72} {top + r * 1.15}'
         f'C{cx - r * 1.12} {top + r * .95} {cx - r * 1.0} {top - r * .05} {cx} {top}'
         f'C{cx + r * 1.0} {top - r * .05} {cx + r * 1.12} {top + r * .95} {cx + r * .72} {top + r * 1.15}'
         f'L{cx + r * .72} {top + h}Z')
    return f'<path d="{d}" fill="{col}"/>'


def crenel(x, y, w, n, h, col):
    cw = w / (2 * n - 1)
    return ''.join(f'<rect x="{x + 2 * i * cw:.1f}" y="{y - h}" width="{cw:.1f}" height="{h}" fill="{col}"/>' for i in range(n))


def tower(x, base, w, h, col, win=None):
    win = win or IV
    return (f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" fill="{col}"/>' + crenel(x, base - h, w, 3, 22, col) +
            arch(x + w / 2, base - h + 40, 34, 56, win))


def cypress(x, base, h, col):
    return f'<path d="M{x} {base}C{x - 34} {base - h * .5} {x - 18} {base - h * .85} {x} {base - h}C{x + 18} {base - h * .85} {x + 34} {base - h * .5} {x} {base}Z" fill="{col}"/>'


def person_icon(cx, y, s, col):
    return human(cx, y, s, col)


def noticia():
    K = 'Notícia · Espanha'
    V = '0 0 920 560'
    # capa: globo com seta de retorno para a casa
    mer = ''.join(f'<ellipse cx="210" cy="210" rx="{rx}" ry="190" fill="none" stroke="{IV}" stroke-width="3" opacity=".55"/>' for rx in (70, 140))
    par = ''.join(f'<path d="M{20} {y}H{400}" stroke="{IV}" stroke-width="3" opacity=".45"/>' for y in (110, 210, 310))
    globe = f'''<svg class=abs style="left:520px;top:720px" width="470" height="470" viewBox="0 0 470 470">
<g transform="translate(25 20)"><circle cx="210" cy="210" r="190" fill="{G2}" stroke="{IV}" stroke-width="6"/>{mer}{par}
<path d="M120 150Q170 110 220 140Q240 190 190 215Q150 250 120 215Z" fill="{PALEG}" opacity=".95"/><path d="M260 240Q300 220 330 260Q320 310 280 320Q250 290 260 240Z" fill="{PALEG}" opacity=".95"/>
<circle cx="168" cy="178" r="13" fill="{TERRA}"/></g>
<path d="M60 430C150 470 330 470 410 400" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/><path d="M382 388L414 398L402 428" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
    hs = f'<svg class=abs style="left:80px;top:1000px" width="300" height="220" viewBox="0 0 300 220">{house(120, 80, 1.6, TERRA, GOLD, IV)}<rect x="0" y="206" width="260" height="10" rx="5" fill="{GOLD}"/></svg>'
    capa = page(1350, G, f'''{bracket(56)}
<div class=abs style="left:80px;top:96px"><div class=kick style="color:{PALEG}">{K}</div></div>
<div class="abs serif" style="left:80px;top:180px;width:920px;font-size:80px;line-height:1.1;font-weight:700;color:{IV}">Governo aprova o regulamento do <span style="color:{GOLD}">Estatuto da cidadania espanhola</span> no exterior</div>
<div class=abs style="left:80px;top:700px;width:300px;height:6px;background:{TERRA}"></div>
<div class=abs style="left:80px;top:740px;width:560px;font-size:34px;line-height:1.4;color:{IV};opacity:.92">Conselho de Ministros, 3 de novembro de 2026</div>
{globe}{hs}{foot(IV, 50)}''')
    # 2 o que foi aprovado: decreto com selo e cinco etiquetas
    chips = ''
    labels = ['Participação', 'Prestações', 'Saúde', 'Subvenções', 'Retorno']
    for i, t in enumerate(labels):
        col = [G, TERRA, G2, G, TERRA][i]
        chips += rrect(460, 60 + i * 96, 400, 74, 37, col) + txt(660, 108 + i * 96, t, 32, IV, 700)
    i2 = sv(f'''{rrect(40, 40, 330, 470, 20, SAND)}{rrect(40, 40, 330, 70, 20, G)}{rrect(40, 90, 330, 20, 0, G)}
{txt(205, 86, 'REAL DECRETO', 28, IV, 800, 'Inter', 4)}
{''.join(rrect(70, 140 + k * 36, 270 - (k % 3) * 40, 12, 6, G, 'opacity=".35"') for k in range(7))}
<circle cx="290" cy="440" r="48" fill="{GOLD}"/><circle cx="290" cy="440" r="34" fill="none" stroke="{G}" stroke-width="4"/>{star(290, 440, 22, G)}
<path d="M385 280H440" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/><path d="M420 258L444 280L420 302" fill="none" stroke="{GOLD}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
{chips}''', V)
    # 3 quem: quatro cartões
    def card(x, label, sub, icon):
        return rrect(x, 70, 190, 400, 20, G) + icon + txt(x + 95, 400, label, 25, GOLD, 800, 'Lora') + txt(x + 95, 436, sub, 20, IV, 600)
    elder = f'{human(105, 150, 1.55, IV)}<path d="M168 262V340" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/><path d="M168 262Q190 250 196 272" fill="none" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/>'
    wheel = f'{human(325, 130, 1.3, IV)}<circle cx="325" cy="296" r="34" fill="none" stroke="{GOLD}" stroke-width="9"/><circle cx="325" cy="296" r="6" fill="{GOLD}"/>'
    ret = f'{human(525, 150, 1.5, IV)}{rrect(560, 280, 52, 42, 8, GOLD)}<path d="M574 280V268H598V280" fill="none" stroke="{GOLD}" stroke-width="6"/>'
    shield = f'<path d="M735 120L805 142V220Q805 290 735 322Q665 290 665 220V142Z" fill="{IV}"/><path d="M735 170V280M690 215H780" stroke="{TERRA}" stroke-width="14" stroke-linecap="round"/>'
    i3 = sv(card(10, '65+', 'maiores de 65', elder) + card(228, 'Incapacidade', 'absoluta', wheel) + card(446, 'Retornadas', 'ao país', ret) + card(664, 'Vítimas', 'de violência', shield), V)
    # 4 retorno: casa, certificado e balcão
    cert = f'''{rrect(520, 70, 340, 240, 18, IV)}{rrect(542, 92, 296, 196, 10, 'none', f'stroke="{G}" stroke-width="4"')}
{txt(690, 150, 'CERTIFICADO', 28, G, 800, 'Inter', 4)}{txt(690, 196, 'pessoa espanhola', 30, TERRA, 700, 'Lora')}{txt(690, 236, 'retornada', 30, TERRA, 700, 'Lora')}
<path d="M780 300L770 380L800 360L830 380L820 300Z" fill="{TERRA}"/><circle cx="800" cy="296" r="38" fill="{GOLD}"/>{star(800, 296, 20, G)}'''
    desk = f'''{rrect(40, 420, 400, 26, 8, GOLD)}{rrect(70, 446, 22, 56, 6, GOLD)}{rrect(388, 446, 22, 56, 6, GOLD)}{human(190, 250, 1.3, IV)}{rrect(310, 360, 90, 60, 8, SAND)}{rrect(325, 375, 60, 8, 4, G)}{rrect(325, 392, 40, 8, 4, G)}
{txt(240, 540, 'Oficina Española del Retorno', 26, IV, 700)}'''
    i4 = sv(cert + desk + f'<path d="M450 200H500" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/><path d="M480 178L504 200L480 222" fill="none" stroke="{GOLD}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>', V)
    # 5 43 -> 51
    dots43 = ''.join(f'<circle cx="{70 + (i % 11) * 24}" cy="{410 + (i // 11) * 24}" r="9" fill="{IV}" opacity=".75"/>' for i in range(43))
    dots51 = ''.join(f'<circle cx="{500 + (i % 13) * 24}" cy="{410 + (i // 13) * 24}" r="9" fill="{GOLD if i >= 43 else IV}"/>' for i in range(51))
    i5 = sv(f'''{txt(190, 300, '43', 190, IV, 700, 'Lora')}{txt(690, 300, '51', 190, GOLD, 700, 'Lora')}
<path d="M340 230H440" stroke="{IV}" stroke-width="10" stroke-linecap="round"/><path d="M412 198L448 230L412 262" fill="none" stroke="{IV}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
{dots43}{dots51}{txt(190, 380, 'membros eleitos hoje', 26, PALEG, 700)}{txt(690, 380, 'membros eleitos no novo texto', 26, PALEG, 700)}''', V)
    # 6 jornal oficial + lupa
    lines = ''.join(rrect(110, 160 + k * 40, 280 - (k % 2) * 40, 14, 7, G, 'opacity=".4"') for k in range(7))
    i6 = sv(f'''{rrect(80, 40, 560, 480, 14, SAND)}{rrect(80, 40, 560, 80, 14, G)}{rrect(80, 100, 560, 20, 0, G)}{txt(360, 96, 'BOLETÍN OFICIAL DEL ESTADO', 30, IV, 800, 'Inter', 3)}
{lines}{rrect(420, 160, 190, 160, 10, G2, 'opacity=".9"')}{rrect(440, 340, 150, 14, 7, G, 'opacity=".4"')}{rrect(440, 372, 120, 14, 7, G, 'opacity=".4"')}
<circle cx="660" cy="360" r="92" fill="{IV}" fill-opacity=".25" stroke="{TERRA}" stroke-width="16"/><path d="M728 428L840 520" stroke="{TERRA}" stroke-width="26" stroke-linecap="round"/>''', V)
    kw = dict(tsize=60, lines=2)
    return [capa,
        cslide(IV, G, TERRA, 'O que foi aprovado', 'Um único regulamento para a Lei 40/2006', 'Em 3 de novembro, o Conselho de Ministros aprovou o Real Decreto que reúne participação institucional, prestações econômicas, assistência sanitária, subvenções e retorno.', i2, **kw),
        cslide(SAND, G, TERRA, 'Quem é o foco', 'Cidadãos espanhóis no exterior', 'Atenção especial a maiores de 65 anos, pessoas com incapacidade absoluta, pessoas retornadas e vítimas de violência contra as mulheres no exterior, com seus descendentes.', i3, **kw),
        cslide(G, IV, PALEG, 'Retorno', 'Certificado de pessoa espanhola retornada', 'O texto define a condição de pessoa retornada e cria o certificado, que dá acesso às políticas de retorno. A Oficina Española del Retorno orienta e acompanha.', i4, **kw),
        cslide(TERRA, IV, PALEG, 'Participação', 'Conselho Geral com mais membros', 'O Conselho Geral da Cidadania Espanhola no Exterior passa de 43 para 51 membros eleitos. O texto atualiza composição, funcionamento e procedimentos eleitorais.', i5, **kw),
        cslide(IV, G, TERRA, 'Para quem não é espanhol', 'Não é mudança de residência', 'O regulamento trata de cidadãos espanhóis. A nota oficial não o apresenta como mudança nas regras de residência de estrangeiros. O texto completo sai no BOE.', i6, **kw),
        closing(1350, 'Fonte: La Moncloa, Referência do Conselho de Ministros de 3/11/2026. Consulta em 05/11/2026.', logo=300, bottom=60)]


def imig():
    K = 'Imigração · Estância'
    V = '0 0 920 560'
    # capa: livro aberto com balão de conversa
    book = f'''<svg class=abs style="left:90px;top:880px" width="900" height="330" viewBox="0 0 900 330">
<path d="M30 300C30 120 150 70 330 100V300C220 270 120 280 30 300Z" fill="{IV}"/><path d="M630 100C810 70 930 120 930 300C840 280 740 270 630 300Z" transform="translate(-60 0)" fill="{IV}"/>
<path d="M330 100Q450 60 570 100V300Q450 270 330 300Z" fill="{SAND}"/>
{''.join(f'<path d="M70 {150 + k * 30}H290" stroke="{G2}" stroke-width="7" stroke-linecap="round" opacity=".5"/>' for k in range(4))}
{''.join(f'<path d="M610 {150 + k * 30}H830" stroke="{G2}" stroke-width="7" stroke-linecap="round" opacity=".5"/>' for k in range(4))}
<path d="M450 60V290" stroke="{TERRA}" stroke-width="6"/></svg>
<svg class=abs style="left:640px;top:690px" width="330" height="200" viewBox="0 0 330 200"><path d="M30 20H300Q320 20 320 40V130Q320 150 300 150H120L60 190V150H30Q10 150 10 130V40Q10 20 30 20Z" fill="{GOLD}"/>{txt(165, 105, 'Hola', 70, G, 700, 'Lora')}</svg>'''
    capa = page(1350, G2, f'''{bracket(56)}
<div class=abs style="left:80px;top:96px"><div class=kick style="color:{PALEG}">{K}</div></div>
<div class="abs serif" style="left:70px;top:190px;font-size:128px;line-height:1.02;font-weight:700;color:{GOLD};letter-spacing:-3px">Atividades<br>formativas</div>
<div class=abs style="left:80px;top:470px;width:300px;height:6px;background:{TERRA}"></div>
<div class="abs serif" style="left:80px;top:510px;width:780px;font-size:56px;line-height:1.12;font-weight:700;color:{IV}">Como funciona a estância de longa duração</div>
<div class=abs style="left:80px;top:690px;width:520px;font-size:32px;line-height:1.4;color:{IV};opacity:.92">O que a ficha oficial prevê para quem vai estudar idiomas ou se capacitar na Espanha.</div>
{book}{foot(IV, 50)}''')
    # 2 cinco modalidades
    def tile(x, col, label, icon):
        return rrect(x, 120, 164, 300, 22, col) + icon + txt(x + 82, 392, label, 21, IV, 700)
    ic1 = f'<path d="M{20 + 25} 165H{20 + 125}Q{20 + 145} 165 {20 + 145} 185V235Q{20 + 145} 255 {20 + 125} 255H{20 + 70}L{20 + 40} 285V255H{20 + 25}Q{20 + 5} 255 {20 + 5} 235V185Q{20 + 5} 165 {20 + 25} 165Z" fill="{GOLD}"/>'
    def sh(x): return x
    ic1 = f'<path d="M45 170H145Q165 170 165 190V240Q165 260 145 260H90L60 290V260H45Q25 260 25 240V190Q25 170 45 170Z" fill="{GOLD}"/>' + txt(95, 232, 'A', 50, G, 800, 'Lora')
    ic2 = f'<path d="M{200 + 20} 180H{200 + 82}V270H{200 + 20}Z" fill="{IV}"/><path d="M{200 + 82} 180H{200 + 144}V270H{200 + 82}Z" fill="{SAND}"/>' + txt(282, 238, 'ñ', 60, TERRA, 700, 'Lora')
    ic3 = f'<circle cx="446" cy="225" r="62" fill="{IV}"/><path d="M446 187V263M408 225H484" stroke="{TERRA}" stroke-width="20" stroke-linecap="round"/>'
    ic4 = f'<rect x="590" y="170" width="116" height="110" rx="10" fill="{IV}"/><path d="M606 200H690M606 225H675M606 250H660" stroke="{G}" stroke-width="8" stroke-linecap="round" opacity=".5"/><circle cx="690" cy="272" r="22" fill="{GOLD}"/><path d="M679 296L673 322L690 312L707 322L701 296Z" fill="{TERRA}"/>'
    ic5 = f'<path d="M790 200L850 200L870 225L850 250H790Z" fill="{IV}"/><path d="M820 250V290" stroke="{IV}" stroke-width="12" stroke-linecap="round"/><circle cx="820" cy="295" r="16" fill="{GOLD}"/>' + f'<path d="M806 188H834" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/>'
    i2 = sv(tile(10, G, 'Conversação', '') + ic1 + tile(190, TERRA, 'Idiomas', '') + ic2 + tile(370, G2, 'Sanitária', '') + ic3 + tile(550, G, 'Técnica', '') + ic4 + tile(730, TERRA, 'Profissional', '') + ic5, V)
    # 3 quem: cartão 18+, anel de estrelas UE cortado
    i3 = sv(f'''{rrect(40, 90, 400, 250, 22, IV)}{rrect(70, 130, 110, 130, 12, GOLD)}{human(125, 145, 1.1, G)}{rrect(210, 140, 190, 20, 10, G, 'opacity=".6"')}{rrect(210, 180, 150, 20, 10, G, 'opacity=".6"')}
{txt(310, 300, '18+', 70, TERRA, 800, 'Lora')}
<circle cx="150" cy="400" r="30" fill="{GOLD}"/><path d="M135 400L146 412L168 388" fill="none" stroke="{G}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>{txt(200, 412, 'admitido na atividade', 28, IV, 700, 'Inter', 0, 'start')}
<g transform="translate(570 40)">{star_ring(180, 220, 130, 22, GOLD, 12)}<circle cx="180" cy="220" r="170" fill="none" stroke="{TERRA}" stroke-width="16"/><path d="M60 100L300 340" stroke="{TERRA}" stroke-width="16"/></g>
{txt(750, 500, 'UE · EEE · Suíça', 30, IV, 700)}''', V)
    # 4 requisitos
    def rq(x, y, icon, big, sub):
        return rrect(x, y, 420, 230, 20, G) + icon + txt(x + 285, y + 100, big, 44, GOLD, 800, 'Lora') + txt(x + 285, y + 150, sub, 22, IV, 700)
    coin = lambda x, y: ''.join(f'<ellipse cx="{x}" cy="{y - k * 22}" rx="48" ry="16" fill="{GOLD}" stroke="{G}" stroke-width="4"/>' for k in range(4, -1, -1))
    i4 = sv(rq(20, 10, coin(110, 160), '100%', 'do IPREM por mês') +
            rq(480, 10, f'<path d="M570 60L630 78V140Q630 190 570 214Q510 190 510 140V78Z" fill="{IV}"/><path d="M570 100V175M532 138H608" stroke="{TERRA}" stroke-width="12" stroke-linecap="round"/>', 'Seguro', 'de saúde na Espanha') +
            rq(20, 270, f'{rrect(52, 296, 110, 150, 10, IV)}<path d="M68 330H146M68 358H146M68 386H120" stroke="{G}" stroke-width="7" stroke-linecap="round" opacity=".5"/>', '6+ meses', 'antecedentes penais') +
            rq(480, 270, f'{rrect(52 + 460, 296, 110, 150, 10, IV)}<path d="M{52 + 460} 446l18 -16 18 16 18 -16 18 16 18 -16 18 16V446Z" fill="{IV}"/><path d="M{528} 332H{606}M{528} 360H{606}" stroke="{G}" stroke-width="7" stroke-linecap="round" opacity=".5"/>', 'Matrícula', 'paga', ), V)
    # 5 onde e quando
    cons = f'''{rrect(30, 460, 300, 24, 8, GOLD)}<path d="M30 200L180 120L330 200Z" fill="{IV}"/>{''.join(rrect(60 + k * 66, 210, 38, 240, 8, IV) for k in range(4))}{rrect(30, 450, 300, 14, 4, IV)}'''
    ofi = f'''{rrect(560, 150, 330, 310, 10, IV)}{''.join(rrect(590 + (k % 3) * 94, 180 + (k // 3) * 90, 60, 60, 8, G, 'opacity=".55"') for k in range(6))}{rrect(700, 380, 60, 80, 6, TERRA)}{rrect(560, 450, 330, 24, 8, GOLD)}'''
    cal = f'''{rrect(380, 150, 140, 150, 16, SAND)}{rrect(380, 150, 140, 46, 16, G)}{rrect(380, 180, 140, 16, 0, G)}{txt(450, 262, '2', 80, TERRA, 800, 'Lora')}{txt(450, 288, 'meses', 24, G, 700)}'''
    i5 = sv(cons + ofi + cal + txt(180, 535, 'Consulado', 28, IV, 800) + txt(725, 535, 'Oficina de Extranjería', 28, IV, 800) + f'<path d="M335 330H375M525 330H555" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>' + txt(450, 335, 'antes', 24, PALEG, 700), V)
    # 6 duração
    i6 = sv(f'''<path d="M60 250H860" stroke="{G}" stroke-width="6" stroke-linecap="round" opacity=".25"/>
{rrect(60, 200, 520, 100, 18, G)}{rrect(580, 200, 70, 100, 12, TERRA)}
{txt(320, 262, 'a formação', 40, IV, 700)}{txt(615, 262, '+15', 30, IV, 800)}{txt(615, 330, 'dias', 24, TERRA, 800)}
<path d="M60 150H580" stroke="{G}" stroke-width="6" stroke-linecap="round"/><path d="M60 130V170M580 130V170" stroke="{G}" stroke-width="6"/>{txt(320, 115, 'no máximo 1 ano', 36, TERRA, 800, 'Lora')}
<circle cx="760" cy="395" r="92" fill="none" stroke="{GOLD}" stroke-width="14"/><path d="M700 362A66 66 0 0 1 806 346" fill="none" stroke="{GOLD}" stroke-width="14" stroke-linecap="round"/><path d="M806 316V352H772" fill="none" stroke="{GOLD}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
{txt(760, 412, '1x', 56, G, 800, 'Lora')}{txt(760, 520, 'prórroga', 30, G, 700)}
{rrect(60, 400, 560, 66, 33, 'none', f'stroke="{G}" stroke-width="4" stroke-dasharray="4 10"')}{txt(340, 443, 'trabalho: a ficha não trata do tema', 27, G, 700)}''', V)
    kw = dict(tsize=60, lines=2)
    return [capa,
        cslide(IV, G, TERRA, 'O que permite', 'Estadia de mais de 90 dias', 'Para ser auxiliar de conversação, estudar espanhol ou língua cooficial de forma presencial, fazer preparatório de formação sanitária especializada, certificação técnica ou certificado profissional.', i2, **kw),
        cslide(G, IV, PALEG, 'Quem pode pedir', 'Maiores de 18 anos admitidos', 'Não vale para cidadãos da UE, do EEE ou da Suíça. Quem pede estando na Espanha precisa de situação de residência válida.', i3, **kw),
        cslide(SAND, G, TERRA, 'Requisitos', 'O que a ficha exige', 'Meios econômicos, seguro de saúde de seguradora autorizada na Espanha, matrícula paga e, se a estadia passar de 6 meses, ausência de antecedentes penais.', i4, **kw),
        cslide(TERRA, IV, PALEG, 'Onde e quando', 'Pelo menos 2 meses antes', 'Do exterior, no consulado. Na Espanha, na Oficina de Extranjería ou pela sede Mercurio. A ficha prevê resposta em até 1 mês (consulado) ou 2 meses (Espanha).', i5, **kw),
        cslide(IV, G, TERRA, 'Duração', 'Tanto quanto a formação', 'Dura o mesmo que a formação, no máximo 1 ano, com 15 dias extras. A prórroga só pode ser pedida uma vez.', i6, **kw),
        closing(1350, 'Fonte: Ministerio de Inclusión, Hoja 2 (atualizada em setembro de 2025). Consulta em 05/11/2026.', logo=300, bottom=60)]


def culture():
    K = 'VOCÊ SABIA? | ESPANHA'
    V = '0 0 960 760'
    ground = lambda c: f'<rect x="40" y="712" width="880" height="24" rx="12" fill="{c}"/>'
    # 1 silhueta da Alhambra sobre a serra
    ill1 = sv(f'''<circle cx="780" cy="130" r="64" fill="{PALEG}"/><circle cx="806" cy="116" r="56" fill="{G}"/>
<path d="M0 470L130 330L210 410L330 270L450 400L560 300L700 430L820 340L960 470V712H0Z" fill="{G2}"/><path d="M330 270L360 305L335 300L318 330Z" fill="{IV}" opacity=".85"/><path d="M560 300L585 332L562 326L545 352Z" fill="{IV}" opacity=".85"/>
{rrect(140, 540, 680, 172, 4, GOLD)}{crenel(140, 540, 680, 17, 26, GOLD)}
{tower(90, 712, 120, 290, GOLD)}{tower(750, 712, 120, 330, GOLD)}{tower(420, 712, 120, 250, GOLD, G)}
{arch(480, 560, 120, 152, G)}{arch(300, 610, 70, 102, G2)}{arch(660, 610, 70, 102, G2)}
{cypress(250, 712, 200, G)}{cypress(720, 712, 240, G)}{ground(IV)}''', V)
    # 2 arco com 1984 e azulejos estrelados
    tiles = ''
    for r in range(3):
        for c in range(9):
            cx, cy = 140 + c * 85, 585 + r * 0
    st8 = lambda cx, cy, s, col: f'<polygon points="{" ".join(f"{cx + (s if k % 2 == 0 else s * .62) * math.cos(math.pi / 8 * k - math.pi / 2):.1f},{cy + (s if k % 2 == 0 else s * .62) * math.sin(math.pi / 8 * k - math.pi / 2):.1f}" for k in range(16))}" fill="{col}"/>'
    band = ''.join(st8(100 + c * 95, 650, 38, [TERRA, GOLD][c % 2]) for c in range(9))
    ill2 = sv(f'''{arch(480, 40, 600, 600, G)}{arch(480, 100, 470, 540, IV)}
{txt(480, 360, '1984', 190, TERRA, 700, 'Lora')}{rrect(300, 395, 360, 6, 3, GOLD)}{txt(480, 445, 'inscrição na lista', 30, G, 700)}{txt(480, 485, 'Alhambra e Generalife', 22, G, 600)}
{rrect(40, 610, 880, 100, 8, G)}{band}''', V)
    # 3 encosta do Albayzín: casas brancas em degraus + "+"
    hs = ''
    cols = [IV, SAND, IV, SAND]
    for row in range(3):
        for k in range(7):
            x = 70 + k * 120 + (row % 2) * 55
            y = 450 + row * 88
            hs += f'<rect x="{x}" y="{y}" width="92" height="74" fill="{cols[(k + row) % 4]}"/><rect x="{x + 34}" y="{y + 26}" width="24" height="34" rx="12" fill="{G}"/><path d="M{x} {y}H{x + 92}" stroke="{TERRA}" stroke-width="10"/>'
    ill3 = sv(f'''<path d="M0 712V420Q480 290 960 420V712Z" fill="{G}"/>{hs}
<circle cx="700" cy="150" r="90" fill="{GOLD}"/><path d="M700 104V196M654 150H746" stroke="{G}" stroke-width="22" stroke-linecap="round"/>
{txt(480, 330, 'Albayzín', 64, G, 700, 'Lora')}{txt(220, 190, '1994', 120, TERRA, 700, 'Lora')}{ground(GOLD)}''', V)
    # 4 três peças em um só bem: castelo, jardim, casas, ligados por anel
    castle = f'{rrect(50, 400, 250, 200, 6, GOLD)}{crenel(50, 400, 250, 7, 24, GOLD)}{tower(40, 600, 70, 240, GOLD)}{arch(175, 470, 70, 130, G)}'
    garden = f'{cypress(480, 600, 250, IV)}{cypress(420, 600, 170, SAND)}{cypress(540, 600, 170, SAND)}<ellipse cx="480" cy="560" rx="100" ry="26" fill="{GOLD}"/><path d="M480 560V470" stroke="{IV}" stroke-width="8" stroke-linecap="round"/><path d="M480 470Q450 480 440 520M480 470Q510 480 520 520" fill="none" stroke="{IV}" stroke-width="6" stroke-linecap="round"/>'
    casas = ''.join(f'<rect x="{680 + k * 88}" y="{500 + (k % 2) * -50}" width="76" height="{100 + (k % 2) * 50}" fill="{IV}"/><rect x="{706 + k * 88}" y="{530 + (k % 2) * -50}" width="22" height="30" rx="11" fill="{G}"/>' for k in range(3))
    ill4 = sv(f'''<circle cx="480" cy="420" r="320" fill="none" stroke="{GOLD}" stroke-width="10" stroke-dasharray="2 22" stroke-linecap="round"/>
{castle}{garden}{casas}{rrect(40, 600, 880, 14, 7, GOLD)}
{txt(175, 665, 'Alhambra', 34, IV, 700)}{txt(480, 665, 'Generalife', 34, IV, 700)}{txt(790, 665, 'Albayzín', 34, IV, 700)}
{txt(480, 120, 'Granada', 84, PALEG, 700, 'Lora')}''', V)
    return [
        reel_slide(G, IV, PALEG, K, 'A <span style="color:%s;font-style:italic">Alhambra</span>, em Granada, é Patrimônio Mundial da UNESCO' % GOLD, ill1),
        reel_slide(IV, G, TERRA, K, 'Foi inscrita na lista em 1984, junto com o Generalife', ill2),
        reel_slide(SAND, G, TERRA, K, 'Em 1994, o bem foi ampliado e passou a incluir o bairro do Albayzín', ill3),
        reel_slide(TERRA, IV, PALEG, K, 'Hoje o bem se chama Alhambra, Generalife e Albayzín, Granada', ill4),
        closing(1920, 'Fonte: UNESCO, Centro do Patrimônio Mundial (Lista do Patrimônio Mundial, nº 314). Consulta em 05/11/2026.', logo=400, bottom=160),
    ]


which = sys.argv[1:] or ['noticia', 'imigracao', 'cultura']
if 'noticia' in which:
    asyncio.run(render(noticia(), 'noticia', 1350))
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
