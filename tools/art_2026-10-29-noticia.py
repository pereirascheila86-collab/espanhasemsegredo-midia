"""Carrossel de notícia de 29/10/2026: bolsas de estudo 2027-2028 (6 slides, 1080x1350).
Uso: ART_OUT=2026-10-29 python3 tools/art_2026-10-29-noticia.py
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
BRACKET = f'<svg class=abs style="right:56px;top:56px" width="190" height="190" viewBox="0 0 190 190"><path d="M0 2H188V190" fill="none" stroke="{GOLD}" stroke-width="5"/></svg>'


def page(bg, inner):
    return f'<html><head><meta charset=utf8><style>{CSS} body{{background:{bg}}}</style></head><body>{BRACKET}{inner}</body></html>'


def foot(col, right=''):
    c = f'<span class=c style="color:{col}">{right}</span>' if right else ''
    return (f'<div class=foot><div class=l><img src="{LOGO}"><span class=n style="color:{col}">'
            f'Espanha Sem Segredo</span></div>{c}</div>')


def svgbox(inner, vb='0 0 920 430'):
    return f'<svg width="100%" height="100%" viewBox="{vb}">{inner}</svg>'


def scene(bg, ink, accent, kick, title, body, illus, frame_bg, right='DESLIZE →'):
    inner = f'''
    <div class=abs style="left:80px;top:92px"><div class=kick style="color:{accent}">{html.escape(kick)}</div>
      <div style="margin-top:14px;width:120px;height:4px;background:{GOLD}"></div></div>
    <div class="abs serif" style="left:80px;top:178px;width:800px;font-size:74px;line-height:1.08;font-weight:700;color:{ink}">{title}</div>
    <div class=abs style="left:80px;top:462px;width:920px;height:410px;border-radius:30px;background:{frame_bg};overflow:hidden;border:4px solid {accent}">{illus}</div>
    <div class=abs style="left:80px;top:930px;width:920px;font-size:41px;line-height:1.38;color:{ink}">{body}</div>
    {foot(ink, right)}'''
    return page(bg, inner)


# capa: capelo + moedas + pergaminho do decreto
CAPA = page(G, f'''
<div class=abs style="left:80px;top:92px"><div class=kick style="color:{PALEG}">Notícia · Estudos</div>
<div style="margin-top:14px;width:120px;height:4px;background:{GOLD}"></div></div>
<svg class=abs style="left:60px;top:250px" width="960" height="560" viewBox="0 0 960 560">
<ellipse cx="480" cy="505" rx="400" ry="34" fill="{G2}"/>
<g transform="translate(480 250)">
<path d="M-250 -10L0 -130L250 -10L0 110Z" fill="{IV}"/>
<path d="M-250 -10L0 110V150L-250 30Z" fill="{SAND}"/><path d="M250 -10L0 110V150L250 30Z" fill="{PALEG}"/>
<path d="M-150 60V170C-150 215 -60 245 0 245C60 245 150 215 150 170V60L0 130Z" fill="{TERRA}"/>
<path d="M0 -10L238 -4V170" fill="none" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/>
<rect x="222" y="170" width="32" height="70" rx="8" fill="{GOLD}"/>
</g>
<g transform="translate(150 430)"><circle r="62" fill="{GOLD}"/><circle r="48" fill="none" stroke="{G}" stroke-width="5"/>
<text y="22" text-anchor="middle" font-family="Lora" font-weight="700" font-size="64" fill="{G}">€</text></g>
<g transform="translate(810 440)"><circle r="52" fill="{GOLD}"/><circle r="40" fill="none" stroke="{G}" stroke-width="5"/>
<text y="19" text-anchor="middle" font-family="Lora" font-weight="700" font-size="54" fill="{G}">€</text></g>
<g transform="translate(220 90)" fill="{GOLD}"><path d="M0 -26L8 -8L26 0L8 8L0 26L-8 8L-26 0L-8 -8Z"/></g>
<g transform="translate(760 70) scale(.7)" fill="{PALEG}"><path d="M0 -26L8 -8L26 0L8 8L0 26L-8 8L-26 0L-8 -8Z"/></g>
</svg>
<div class="abs serif" style="left:80px;top:850px;width:880px;font-size:76px;line-height:1.08;font-weight:700;color:{IV}">Bolsas de estudo 2027-2028: <span style="color:{PALEG};font-style:italic">o primeiro passo</span> do Governo</div>
{foot(IV, 'DESLIZE →')}''')

# 2: Conselho de Ministros, 27 out
ill2 = svgbox(f'''
<g transform="translate(60 40)">
<rect width="300" height="340" rx="22" fill="{IV}" stroke="{G}" stroke-width="6"/>
<rect width="300" height="86" rx="22" fill="{TERRA}"/><rect y="50" width="300" height="36" fill="{TERRA}"/>
<text x="150" y="60" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" letter-spacing="6" fill="{IV}">OUTUBRO</text>
<text x="150" y="226" text-anchor="middle" font-family="Lora" font-weight="700" font-size="140" fill="{G}">27</text>
<text x="150" y="292" text-anchor="middle" font-family="Inter" font-weight="700" font-size="30" letter-spacing="4" fill="{TERRA}">2026</text>
</g>
<g transform="translate(470 70)">
<path d="M0 120L190 20L380 120Z" fill="{G}"/><rect x="20" y="120" width="340" height="22" fill="{GOLD}"/>
<g fill="{IV}"><rect x="42" y="150" width="46" height="130" rx="6"/><rect x="132" y="150" width="46" height="130" rx="6"/><rect x="202" y="150" width="46" height="130" rx="6"/><rect x="292" y="150" width="46" height="130" rx="6"/></g>
<rect x="10" y="280" width="360" height="26" rx="6" fill="{GOLD}"/><rect x="-10" y="306" width="400" height="26" rx="6" fill="{G}"/>
<circle cx="190" cy="76" r="24" fill="{GOLD}"/>
</g>
<g transform="translate(715 350) rotate(-10)"><rect x="-96" y="-34" width="192" height="68" rx="12" fill="none" stroke="{TERRA}" stroke-width="7"/>
<text y="14" text-anchor="middle" font-family="Inter" font-weight="800" font-size="38" letter-spacing="4" fill="{TERRA}">URGENTE</text></g>
''')

# 3: limites e valores (sliders)
def slider(y, label, knob, col):
    return (f'<text x="60" y="{y - 46}" font-family="Inter" font-weight="800" font-size="30" letter-spacing="2" fill="{G}">{label}</text>'
            f'<rect x="60" y="{y}" width="800" height="18" rx="9" fill="{G}" opacity=".18"/>'
            f'<rect x="60" y="{y}" width="{knob - 60}" height="18" rx="9" fill="{col}"/>'
            f'<circle cx="{knob}" cy="{y + 9}" r="30" fill="{IV}" stroke="{col}" stroke-width="8"/>'
            f'<text x="{knob}" y="{y + 20}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="{col}">?</text>')


ill3 = svgbox(slider(130, 'LIMITE DE RENDA FAMILIAR', 520, TERRA) + slider(250, 'LIMITE DE PATRIMÔNIO', 360, G2) + slider(370, 'VALOR DAS BOLSAS E AJUDAS', 680, GOLD))

# 4: documento sem os números
ill4 = svgbox(f'''
<g transform="translate(70 36)">
<path d="M0 0H330L400 70V360H0Z" fill="#FFFFFF" stroke="{G}" stroke-width="6" stroke-linejoin="round"/>
<path d="M330 0V70H400" fill="none" stroke="{G}" stroke-width="6"/>
<rect x="36" y="46" width="190" height="16" rx="8" fill="{G}"/>
<rect x="36" y="98" width="320" height="12" rx="6" fill="{G}" opacity=".35"/><rect x="36" y="130" width="280" height="12" rx="6" fill="{G}" opacity=".35"/>
<rect x="36" y="178" width="320" height="64" rx="12" fill="none" stroke="{TERRA}" stroke-width="5" stroke-dasharray="14 10"/>
<text x="196" y="222" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="3" fill="{TERRA}">€ ? ? ?</text>
<rect x="36" y="268" width="320" height="64" rx="12" fill="none" stroke="{TERRA}" stroke-width="5" stroke-dasharray="14 10"/>
<text x="196" y="312" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="3" fill="{TERRA}">€ ? ? ?</text>
</g>
<g transform="translate(560 214)">
<circle r="150" fill="{GOLD}" opacity=".25"/>
<path d="M-70 -20L-14 38L84 -62" fill="none" stroke="{G}" stroke-width="0"/>
<rect x="-110" y="-70" width="220" height="140" rx="16" fill="{G}"/>
<text y="14" text-anchor="middle" font-family="Lora" font-weight="700" font-size="52" fill="{IV}">BOE</text>
<text y="50" text-anchor="middle" font-family="Inter" font-weight="700" font-size="20" letter-spacing="4" fill="{PALEG}">AINDA NÃO</text>
</g>
''', '0 0 920 430')

# 5: acompanhar: lupa sobre duas fontes
ill5 = svgbox(f'''
<g transform="translate(60 60)"><rect width="380" height="130" rx="20" fill="{G}"/>
<text x="190" y="62" text-anchor="middle" font-family="Lora" font-weight="700" font-size="48" fill="{IV}">BOE</text>
<text x="190" y="98" text-anchor="middle" font-family="Inter" font-weight="700" font-size="20" letter-spacing="3" fill="{PALEG}">TEXTO FINAL</text></g>
<g transform="translate(60 230)"><rect width="380" height="130" rx="20" fill="{TERRA}"/>
<text x="190" y="56" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" fill="{IV}">Ministerio de Educación,</text>
<text x="190" y="92" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" fill="{IV}">FP y Deportes</text></g>
<g stroke="{GOLD}" stroke-width="10" stroke-linecap="round" fill="none"><path d="M470 125H560M470 295H560M560 125V295M560 210H610"/></g>
<g transform="translate(750 210)"><circle r="90" fill="{IV}" stroke="{G}" stroke-width="14"/><circle r="60" fill="none" stroke="{GOLD}" stroke-width="5"/>
<path d="M64 64L130 130" stroke="{G}" stroke-width="24" stroke-linecap="round"/>
<path d="M-26 -8L-6 14L30 -26" fill="none" stroke="{TERRA}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>
''')

S2 = scene(IV, G, TERRA, 'Notícia · Estudos', 'O que aconteceu', 'Em 27 de outubro de 2026, o Conselho de Ministros autorizou a tramitação urgente do projeto de Real Decreto sobre bolsas e ajudas ao estudo do curso 2027-2028.', ill2, SAND)
S3 = scene(TERRA, IV, PALEG, 'Notícia · Estudos', 'O que o decreto define', 'Os limites de renda e de patrimônio familiar e os valores das bolsas e ajudas. O projeto também modifica em parte o Real Decreto 1721/2007.', ill3, IV)
S4 = scene(SAND, G, TERRA, 'Notícia · Estudos', 'O que ainda não se sabe', 'A página oficial do Conselho não traz os limites nem os valores. Autorizar a tramitação urgente não é aprovar o decreto.', ill4, IV)
S5 = scene(IV, G, TERRA, 'Notícia · Estudos', 'Como acompanhar', 'Aguarde o texto final no BOE e consulte o Ministerio de Educación, FP y Deportes. Quem pode pedir só se confirma no texto final e na convocatória.', ill5, SAND)

LS = 360
S6 = page(IV, f'''
<div class=abs style="left:0;right:0;top:130px;display:flex;justify-content:center"><img src="{LOGO}" width="{LS}" height="{LS}"></div>
<div class="abs serif" style="left:80px;right:80px;top:{130 + LS + 60}px;text-align:center;font-size:70px;line-height:1.14;font-weight:700;color:{G}">Aqui você fica por dentro de tudo sobre a Espanha</div>
<div class=abs style="left:50%;margin-left:-65px;top:{130 + LS + 60 + 70 * 3 + 40}px;width:130px;height:5px;background:{GOLD}"></div>
<div class="abs serif" style="left:80px;right:80px;top:{130 + LS + 60 + 70 * 3 + 80}px;text-align:center;font-size:56px;font-weight:700;color:{TERRA}">Espanha Sem Segredo</div>
<div class=abs style="left:80px;right:80px;top:{130 + LS + 60 + 70 * 3 + 160}px;text-align:center;font-size:40px;color:{G}">Siga <b>@espanhasemsegredo</b></div>
<div class=abs style="left:100px;right:100px;bottom:60px;text-align:center;font-size:25px;line-height:1.5;color:{G};opacity:.85">Fonte: La Moncloa, Referencia do Consejo de Ministros de 27/10/2026. Consulta em 29/10/2026.<br>Conteúdo informativo, não é assessoria jurídica.</div>''')

SLIDES = [CAPA, S2, S3, S4, S5, S6]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, htm in enumerate(SLIDES):
            await pg.set_content(htm)
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT + f'noticia-{i + 1}.png')
        await b.close()

asyncio.run(main())
