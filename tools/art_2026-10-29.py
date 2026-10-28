"""Carrossel de imigração de 29/10/2026: tradução juramentada (7 slides, 1080x1350).
Layout novo: capa com selo circular em terracota e cenas em moldura deslocada (nada de bloco verde com borda ondulada).
Uso: ART_OUT=2026-10-29 python3 tools/art_2026-10-29.py
"""
import base64, asyncio, os, html
from playwright.async_api import async_playwright

B = os.path.dirname(os.path.abspath(__file__)) + '/../'
OUT = os.environ.get('ART_OUT', B + 'saida/') + '/'
os.makedirs(OUT, exist_ok=True)
LOGO = 'data:image/png;base64,' + base64.b64encode(open(B + 'marca/logo-espanha-sem-segredo.png', 'rb').read()).decode()
G = '#0F3D3A'; G2 = '#1E5550'; GOLD = '#C9A24A'; TERRA = '#B8573A'; IV = '#F5F1E8'; INK = '#24292C'; SAND = '#E9DFC9'; PALEG = '#F3D79A'

CSS = '''
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;font-family:Inter,Arial,sans-serif;position:relative}
.serif{font-family:Lora,Georgia,serif}
.abs{position:absolute}
.foot{position:absolute;left:80px;right:80px;bottom:56px;display:flex;align-items:center;justify-content:space-between}
.foot .l{display:flex;align-items:center;gap:18px}
.foot img{width:68px;height:68px}
.foot .n{font-family:Lora,serif;font-style:italic;font-size:30px;letter-spacing:.12em}
.foot .c{font-size:26px;letter-spacing:.16em;font-weight:700}
.kick{font-size:28px;letter-spacing:.2em;font-weight:700;text-transform:uppercase}
'''


def page(bg, inner):
    return f'<html><head><meta charset=utf8><style>{CSS} body{{background:{bg}}}</style></head><body>{inner}</body></html>'


def foot(col, right=''):
    c = f'<span class=c style="color:{col}">{right}</span>' if right else ''
    return (f'<div class=foot><div class=l><img src="{LOGO}"><span class=n style="color:{col}">'
            f'Espanha Sem Segredo</span></div>{c}</div>')


# ---------------------------------------------------------------- cena (slides 2 a 6)
def scene(bg, ink, accent, kick, title, body, illus, frame_bg, tag=None, right='DESLIZE →'):
    tagh = (f'<div style="display:inline-block;margin-top:26px;padding:12px 26px;border-radius:40px;'
            f'background:{accent};color:{bg};font-size:27px;font-weight:700;letter-spacing:.08em">{tag}</div>') if tag else ''
    inner = f'''
    <div class=abs style="left:80px;top:92px"><div class=kick style="color:{accent}">{html.escape(kick)}</div></div>
    <div class="abs serif" style="left:80px;top:150px;width:900px;font-size:78px;line-height:1.06;font-weight:700;color:{ink}">{title}</div>
    <div class=abs style="left:112px;top:452px;width:888px;height:430px;border-radius:34px;border:4px solid {accent}"></div>
    <div class=abs style="left:80px;top:420px;width:888px;height:430px;border-radius:34px;background:{frame_bg};overflow:hidden">{illus}</div>
    <div class=abs style="left:80px;top:930px;width:7px;height:250px;background:{accent};border-radius:4px"></div>
    <div class=abs style="left:116px;top:924px;width:860px;font-size:42px;line-height:1.38;color:{ink}">{body}{tagh}</div>
    {foot(ink, right)}'''
    return page(bg, inner)


def svgbox(inner, vb='0 0 888 430'):
    return f'<svg width="100%" height="100%" viewBox="{vb}">{inner}</svg>'


def doc(x, y, w, h, fill, line, stripe=None, rot=0, fold=True):
    s = (f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})">'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{line}" stroke-width="5"/>')
    if stripe:
        s += f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="14" fill="{stripe}"/><rect x="{x}" y="{y + 30}" width="{w}" height="16" fill="{stripe}"/>'
    for i in range(4):
        s += f'<rect x="{x + 26}" y="{y + 84 + i * 30}" width="{w - 52 - (i % 2) * 40}" height="10" rx="5" fill="{line}" opacity=".55"/>'
    s += '</g>'
    return s


# 2: quando é exigida
ill2 = svgbox(f'''
{doc(60, 70, 240, 290, '#FFFFFF', G, TERRA, -6)}
<g transform="translate(180 230)"><circle r="46" fill="{G}"/><circle r="46" fill="none" stroke="{GOLD}" stroke-width="4" transform="scale(1.18)"/>
<path d="M-46 0H46M0 -46C-24 -22 -24 22 0 46C24 22 24 -22 0 -46M-40 -20H40M-40 20H40" fill="none" stroke="{IV}" stroke-width="4"/></g>
<g stroke="{TERRA}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M350 215H520M480 175L525 215L480 255"/></g>
{doc(590, 70, 240, 290, '#FFFFFF', G, G2, 5)}
<g transform="translate(712 232)"><circle r="50" fill="{GOLD}"/><text y="18" text-anchor="middle" font-family="Lora" font-weight="700" font-size="54" fill="{G}">ES</text></g>
<g transform="translate(790 340)"><circle r="30" fill="{TERRA}"/><path d="M-13 0L-3 11L15 -10" fill="none" stroke="{IV}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>
''')

# 3: língua cooficial
ill3 = svgbox(f'''
<path d="M70 70H520A34 34 0 0 1 554 104V210A34 34 0 0 1 520 244H230L150 310V244H70A34 34 0 0 1 36 210V104A34 34 0 0 1 70 70Z" fill="{G}"/>
<text x="295" y="178" text-anchor="middle" font-family="Lora" font-weight="700" font-size="62" fill="{IV}">Castelhano</text>
<path d="M368 190H818A34 34 0 0 1 852 224V330A34 34 0 0 1 818 364H738V420L658 364H368A34 34 0 0 1 334 330V224A34 34 0 0 1 368 190Z" fill="{TERRA}" stroke="{PALEG}" stroke-width="5"/>
<text x="593" y="298" text-anchor="middle" font-family="Lora" font-weight="700" font-size="50" fill="{IV}">língua cooficial</text>
<g transform="translate(822 96)"><path d="M0 -44C-26 -44 -42 -24 -42 -2C-42 28 0 66 0 66C0 66 42 28 42 -2C42 -24 26 -44 0 -44Z" fill="{GOLD}"/><circle cy="-6" r="14" fill="{G}"/></g>
''')

# 4: quem traduz
def person(cx, cy, a, b):
    return (f'<circle cx="{cx}" cy="{cy - 38}" r="34" fill="{a}"/><path d="M{cx - 62} {cy + 62}C{cx - 62} {cy + 12} {cx - 34} {cy + 2} {cx} {cy + 2}'
            f'C{cx + 34} {cy + 2} {cx + 62} {cy + 12} {cx + 62} {cy + 62}Z" fill="{a}"/>'
            f'<circle cx="{cx + 44}" cy="{cy + 40}" r="26" fill="{b}" stroke="{a}" stroke-width="5"/>'
            f'<path d="M{cx + 33} {cy + 40}L{cx + 41} {cy + 49}L{cx + 56} {cy + 31}" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')


ill4 = svgbox(f'''
<rect x="40" y="46" width="390" height="338" rx="26" fill="{IV}" stroke="{G}" stroke-width="5"/>
{person(135, 160, G, GOLD)}
<text x="235" y="150" font-family="Inter" font-weight="800" font-size="34" fill="{G}">Intérprete</text>
<text x="235" y="192" font-family="Inter" font-weight="800" font-size="34" fill="{G}">Jurado</text>
<text x="70" y="266" font-family="Inter" font-size="28" fill="{INK}">autorizado pelo</text>
<text x="70" y="306" font-family="Inter" font-size="28" font-weight="700" fill="{TERRA}">Ministerio de</text>
<text x="70" y="344" font-family="Inter" font-size="28" font-weight="700" fill="{TERRA}">Asuntos Exteriores</text>
<rect x="458" y="46" width="390" height="338" rx="26" fill="{IV}" stroke="{TERRA}" stroke-width="5" stroke-dasharray="14 10"/>
{person(553, 160, TERRA, GOLD)}
<text x="653" y="150" font-family="Inter" font-weight="800" font-size="34" fill="{TERRA}">Língua</text>
<text x="653" y="192" font-family="Inter" font-weight="800" font-size="34" fill="{TERRA}">cooficial</text>
<text x="488" y="266" font-family="Inter" font-size="28" fill="{INK}">intérprete autorizado</text>
<text x="488" y="306" font-family="Inter" font-size="28" font-weight="700" fill="{TERRA}">pela própria</text>
<text x="488" y="344" font-family="Inter" font-size="28" font-weight="700" fill="{TERRA}">comunidade</text>
''')

# 5: onde achar
rows = ''
for i, (lbl, w) in enumerate([('ES', 330), ('EN', 260), ('PT', 300), ('FR', 220)]):
    y = 100 + i * 66
    rows += (f'<rect x="130" y="{y}" width="{w + 30}" height="14" rx="7" fill="{G}" opacity=".5"/>'
             f'<rect x="{160 + w + 30}" y="{y - 14}" width="62" height="40" rx="20" fill="{TERRA}"/>'
             f'<text x="{191 + w + 30}" y="{y + 14}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" fill="{IV}">{lbl}</text>')
ill5 = svgbox(f'''
<rect x="90" y="40" width="590" height="350" rx="22" fill="#FFFFFF" stroke="{G}" stroke-width="5"/>
<rect x="90" y="40" width="590" height="46" rx="22" fill="{G}"/><rect x="90" y="64" width="590" height="22" fill="{G}"/>
<text x="385" y="73" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="4" fill="{IV}">LISTA OFICIAL</text>
<g transform="translate(0 38)">{rows}</g>
<g transform="translate(760 250)"><circle r="70" fill="{GOLD}" opacity=".22"/><circle r="52" fill="none" stroke="{G}" stroke-width="14"/><path d="M38 38L88 88" stroke="{G}" stroke-width="18" stroke-linecap="round"/></g>
''')

# 6: recomendação (selo + check)
ill6 = svgbox(f'''
<g transform="translate(396 215)">
<circle r="178" fill="none" stroke="{GOLD}" stroke-width="5"/>
<circle r="150" fill="{GOLD}"/><circle r="128" fill="none" stroke="{G}" stroke-width="4"/>
<path d="M-62 4L-20 48L66 -48" fill="none" stroke="{G}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<g font-family="Inter" font-weight="700" font-size="22" letter-spacing="2" fill="{IV}" opacity=".9"><text x="848" y="72" text-anchor="end">RECOMENDAÇÃO DO</text><text x="848" y="106" text-anchor="end">ESPANHA SEM SEGREDO</text></g>
<g font-family="Inter" font-weight="800" font-size="30" letter-spacing="5" fill="{PALEG}"><text x="40" y="70">LISTA</text><text x="40" y="112">OFICIAL</text>
<text x="848" y="338" text-anchor="end">TRADUTOR</text><text x="848" y="380" text-anchor="end">JURADO</text></g>
''')

CAPA = page(TERRA, f'''
<div class=abs style="left:80px;top:92px"><div class=kick style="color:{PALEG}">Imigração · Documentos</div></div>
<svg class=abs style="right:-120px;top:120px" width="700" height="700" viewBox="0 0 760 760">
<defs><path id=ring d="M380 380 m-290 0 a290 290 0 1 1 580 0 a290 290 0 1 1 -580 0"/></defs>
<g transform="rotate(-16 380 380)">
<circle cx="380" cy="380" r="352" fill="none" stroke="{IV}" stroke-width="7"/>
<circle cx="380" cy="380" r="226" fill="none" stroke="{IV}" stroke-width="4"/>
<text font-family="Inter" font-weight="800" font-size="46" fill="{IV}"><textPath href="#ring" textLength="1790" lengthAdjust="spacing">TRADUÇÃO JURAMENTADA ✦ TRADUCCIÓN JURADA ✦ </textPath></text>
<g transform="translate(380 380)">
<path d="M-92 -120H46L110 -56V124H-92Z" fill="{IV}"/><path d="M46 -120V-56H110" fill="none" stroke="{TERRA}" stroke-width="7"/>
<g stroke="{TERRA}" stroke-width="9" stroke-linecap="round"><path d="M-60 -34H66M-60 -4H66M-60 26H20"/></g>
<circle cx="52" cy="86" r="48" fill="{G}"/><circle cx="52" cy="86" r="36" fill="none" stroke="{GOLD}" stroke-width="4"/>
<path d="M30 86L46 102L76 68" fill="none" stroke="{IV}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
</g></g></svg>
<div class="abs serif" style="left:80px;top:820px;width:920px;font-size:78px;line-height:1.08;font-weight:700;color:{IV}">Tradução juramentada: <span style="color:{PALEG};font-style:italic">quando é exigida</span> e como obter na Espanha</div>
{foot(IV, 'DESLIZE →')}''')

S2 = scene(IV, G, TERRA, 'Imigração · Documentos', 'Quando a tradução é exigida',
           'Os trâmites de extranjería podem pedir documentos emitidos por autoridades estrangeiras. Eles devem estar traduzidos ao castelhano.',
           ill2, SAND)
S3 = scene(G, IV, GOLD, 'Imigração · Documentos', 'E se houver língua cooficial?',
           'Se o órgão fica numa comunidade com língua cooficial, a tradução para essa língua também vale.',
           ill3, IV)
S4 = scene(SAND, G, TERRA, 'Imigração · Documentos', 'Quem pode traduzir',
           'Um Intérprete Jurado autorizado pelo Ministerio de Asuntos Exteriores. Para a língua cooficial, um intérprete autorizado pela própria comunidade.',
           ill4, SAND)
S5 = scene(IV, G, TERRA, 'Imigração · Documentos', 'Onde achar um tradutor',
           'O Ministério publica uma lista oficial de tradutores-intérpretes jurados, com os idiomas de cada um. Ele não faz a tradução nem intermedeia a contratação.',
           ill5, SAND)
S6 = scene(G, IV, GOLD, 'Imigração · Documentos', 'Nossa recomendação',
           'Na Espanha, o recomendável é sempre traduzir com um tradutor-intérprete jurado que conste na lista oficial do Ministerio de Asuntos Exteriores.',
           ill6, G2)

LOGO_SZ = 360
S7 = page(IV, f'''
<svg class=abs style="right:56px;top:56px" width="230" height="230" viewBox="0 0 230 230"><path d="M0 2H228V230" fill="none" stroke="{TERRA}" stroke-width="3"/></svg>
<div class=abs style="left:0;right:0;top:130px;display:flex;justify-content:center"><img src="{LOGO}" width="{LOGO_SZ}" height="{LOGO_SZ}"></div>
<div class="abs serif" style="left:80px;right:80px;top:{130 + LOGO_SZ + 60}px;text-align:center;font-size:70px;line-height:1.14;font-weight:700;color:{G}">Aqui você fica por dentro de tudo sobre a Espanha</div>
<div class=abs style="left:50%;margin-left:-65px;top:{130 + LOGO_SZ + 60 + 70 * 3 + 40}px;width:130px;height:5px;background:{TERRA}"></div>
<div class="abs serif" style="left:80px;right:80px;top:{130 + LOGO_SZ + 60 + 70 * 3 + 80}px;text-align:center;font-size:56px;font-weight:700;color:{TERRA}">Espanha Sem Segredo</div>
<div class=abs style="left:80px;right:80px;top:{130 + LOGO_SZ + 60 + 70 * 3 + 160}px;text-align:center;font-size:40px;color:{G}">Siga <b>@espanhasemsegredo</b></div>
<div class=abs style="left:100px;right:100px;bottom:60px;text-align:center;font-size:25px;line-height:1.5;color:{G};opacity:.85">Fonte: Ministerio de Inclusión e Ministerio de Asuntos Exteriores. Consulta em 23/10/2026.<br>Conteúdo informativo, não é assessoria jurídica.</div>''')

SLIDES = [CAPA, S2, S3, S4, S5, S6, S7]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, htm in enumerate(SLIDES):
            await pg.set_content(htm)
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT + f'imigracao-{i + 1}.png')
        await b.close()

asyncio.run(main())
