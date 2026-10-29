"""Reel VOCÊ SABIA? | ESPANHA de 29/10/2026: castells (7 telas, 1080x1920) + MP4 (3,5 s por tela, fade 0,4 s).
Uso: ART_OUT=2026-10-29 python3 tools/art_2026-10-29-cultura.py
"""
import base64, asyncio, os, subprocess
from playwright.async_api import async_playwright

B = os.path.dirname(os.path.abspath(__file__)) + '/../'
OUT = os.environ.get('ART_OUT', B + 'saida/') + '/'
os.makedirs(OUT, exist_ok=True)
LOGO = 'data:image/png;base64,' + base64.b64encode(open(B + 'marca/logo-espanha-sem-segredo.png', 'rb').read()).decode()
G = '#0F3D3A'; G2 = '#1E5550'; GOLD = '#C9A24A'; TERRA = '#B8573A'; IV = '#F5F1E8'; INK = '#24292C'; SAND = '#E9DFC9'; PALEG = '#F3D79A'

CSS = '''*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;font-family:Inter,Arial,sans-serif;position:relative}
.serif{font-family:Lora,Georgia,serif}.abs{position:absolute}
.foot{position:absolute;left:80px;right:80px;bottom:150px;display:flex;align-items:center;gap:18px}
.foot img{width:68px;height:68px}.foot .n{font-family:Lora,serif;font-style:italic;font-size:30px;letter-spacing:.12em}
.kick{font-size:30px;letter-spacing:.2em;font-weight:700;text-transform:uppercase}'''
BR = f'<svg class=abs style="right:56px;top:150px" width="190" height="190" viewBox="0 0 190 190"><path d="M0 2H188V190" fill="none" stroke="{GOLD}" stroke-width="5"/></svg>'


def page(bg, inner):
    return f'<html><head><meta charset=utf8><style>{CSS} body{{background:{bg}}}</style></head><body>{BR}{inner}</body></html>'


def foot(col):
    return f'<div class=foot><img src="{LOGO}"><span class=n style="color:{col}">Espanha Sem Segredo</span></div>'


def human(cx, y, s, col, arms=None, head=None):
    """figura estilizada: cabeça, tronco e pernas; y = topo da cabeça"""
    h = head or col
    r = 15 * s
    return (f'<circle cx="{cx}" cy="{y + r}" r="{r}" fill="{h}"/>'
            f'<rect x="{cx - 20 * s}" y="{y + 2.4 * r}" width="{40 * s}" height="{58 * s}" rx="{14 * s}" fill="{col}"/>'
            f'<rect x="{cx - 20 * s}" y="{y + 2.4 * r + 44 * s}" width="{16 * s}" height="{40 * s}" rx="{6 * s}" fill="{col}"/>'
            f'<rect x="{cx + 4 * s}" y="{y + 2.4 * r + 44 * s}" width="{16 * s}" height="{40 * s}" rx="{6 * s}" fill="{col}"/>')


def tower(levels, cx, base_y, s, cols):
    """torre: levels = [n pessoas por andar de baixo para cima], andar de 1 a 3 pessoas lado a lado"""
    out = ''
    y = base_y
    for i, n in enumerate(levels):
        step = 112 * s
        y -= step
        col = cols[i % len(cols)]
        w = 46 * s
        for k in range(n):
            x = cx + (k - (n - 1) / 2) * w
            out += human(x, y, s, col, head=None)
    return out


def slide(bg, ink, accent, kick, big, ill, sub=''):
    return page(bg, f'''
<div class=abs style="left:80px;top:170px"><div class=kick style="color:{accent}">{kick}</div><div style="margin-top:14px;width:120px;height:4px;background:{GOLD}"></div></div>
<div class="abs serif" style="left:80px;top:290px;width:920px;font-size:84px;line-height:1.1;font-weight:700;color:{ink}">{big}</div>
<div class=abs style="left:60px;top:760px;width:960px;height:760px">{ill}</div>
{foot(ink)}''')


def sv(inner, vb='0 0 960 760'):
    return f'<svg width="100%" height="100%" viewBox="{vb}">{inner}</svg>'

K = 'VOCÊ SABIA? | ESPANHA'
CAT = [TERRA, G, GOLD]
ground = lambda c: f'<rect x="40" y="690" width="880" height="26" rx="13" fill="{c}"/>'

# 1 torre humana (pinya com base larga)
base = ''.join(human(120 + k * 74, 560, 1.1, GOLD if k % 2 else PALEG, head=None) for k in range(12))
ill1 = sv(ground(GOLD) + base + tower([6, 4, 3, 1], 480, 590, 1.1, [TERRA, IV, TERRA, PALEG]) )
# 2 século XVIII: pergaminho e relógio
ill2 = sv(f'''<rect x="150" y="90" width="540" height="520" rx="30" fill="#FFFFFF" stroke="{G}" stroke-width="8"/>
<rect x="150" y="90" width="540" height="76" rx="30" fill="{G}"/><rect x="150" y="130" width="540" height="36" fill="{G}"/>
<text x="420" y="145" text-anchor="middle" font-family="Lora" font-weight="700" font-size="46" fill="{IV}">Século XVIII</text>
{''.join(f'<rect x="200" y="{210 + i * 62}" width="{440 - (i % 3) * 70}" height="16" rx="8" fill="{G}" opacity=".35"/>' for i in range(6))}
{tower([3, 2, 1], 440, 600, 1.1, [TERRA, G, GOLD])}
<g transform="translate(760 560)"><circle r="130" fill="{GOLD}"/><circle r="104" fill="{IV}"/><circle r="104" fill="none" stroke="{G}" stroke-width="8"/>
<path d="M0 -70V0L50 36" fill="none" stroke="{TERRA}" stroke-width="12" stroke-linecap="round"/><circle r="12" fill="{G}"/></g>''' + ground(G2))
# 3 nove andares
ill3 = sv(ground(GOLD) + tower([4, 4, 3, 3, 2, 2, 1, 1, 1], 440, 690, .78, [TERRA, G, GOLD]) +
          ''.join(f'<g transform="translate(790 {640 - i * 66})"><rect x="-36" y="-26" width="72" height="52" rx="12" fill="{TERRA if i == 8 else G}"/><text y="12" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" fill="{IV}">{i + 1}</text></g>' for i in range(9)))
# 4 UNESCO selo 2010
ill4 = sv(f'''<g transform="translate(480 340)">
<circle r="270" fill="{GOLD}"/><circle r="236" fill="none" stroke="{G}" stroke-width="8"/><circle r="200" fill="{IV}"/>
{''.join(f'<ellipse transform="rotate({a}) translate(0 -228)" rx="16" ry="34" fill="{G2}"/>' for a in range(-70, 71, 28))}
<text y="-20" text-anchor="middle" font-family="Lora" font-weight="700" font-size="120" fill="{G}">2010</text>
<text y="50" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" letter-spacing="6" fill="{TERRA}">PATRIMÔNIO</text>
<text y="94" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" letter-spacing="6" fill="{TERRA}">IMATERIAL</text></g>
<rect x="260" y="650" width="440" height="70" rx="35" fill="{G}"/><text x="480" y="698" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" letter-spacing="8" fill="{IV}">UNESCO</text>''')
# 5 numeros
ill5 = sv(f'''<g font-family="Lora" font-weight="700" text-anchor="middle">
<rect x="40" y="60" width="430" height="300" rx="30" fill="{G}"/><text x="255" y="210" font-size="130" fill="{PALEG}">100+</text><text x="255" y="290" font-family="Inter" font-weight="800" font-size="36" letter-spacing="5" fill="{IV}">GRUPOS</text>
<rect x="490" y="60" width="430" height="300" rx="30" fill="{TERRA}"/><text x="705" y="210" font-size="120" fill="{IV}">~12 mil</text><text x="705" y="290" font-family="Inter" font-weight="800" font-size="30" letter-spacing="2" fill="{PALEG}">CASTELLS POR ANO</text></g>
{ground(GOLD)}{''.join(human(90 + k * 78, 440, 1.5, [G, TERRA, GOLD][k % 3], head=None) for k in range(11))}''')
# 6 trabalho em equipe: mãos/ ombros (pessoas de braços dados)
ill6 = sv(ground(GOLD) + ''.join(human(130 + k * 100, 330, 2.0, [IV, TERRA, GOLD, PALEG][k % 4], head=None) for k in range(8)) +
          ''.join(f'<rect x="{85 + k * 100}" y="460" width="110" height="30" rx="13" fill="{PALEG}"/>' for k in range(8)) +
          f'<g transform="translate(480 200) scale(1.3)"><path d="M0 60C-90 0 -120 -60 -60 -90C-30 -105 0 -80 0 -60C0 -80 30 -105 60 -90C120 -60 90 0 0 60Z" fill="{TERRA}"/></g>')

S = [
    slide(G, IV, PALEG, K, 'Na Catalunha, pessoas formam <span style="color:%s;font-style:italic">torres humanas</span>' % PALEG, ill1.replace(G2, GOLD)),
    slide(IV, G, TERRA, K, 'As referências mais antigas são do século XVIII', ill2),
    slide(SAND, G, TERRA, K, 'Já havia torres de até nove andares', ill3),
    slide(TERRA, IV, PALEG, K, '2010: Patrimônio Cultural Imaterial da Humanidade (UNESCO)', ill4.replace(f'fill="{G2}"', f'fill="{TERRA}"')),
    slide(IV, G, TERRA, K, 'Hoje são mais de 100 grupos e cerca de 12 mil castells por ano', ill5),
    slide(G, IV, PALEG, K, 'Trabalho em equipe, esforço e superação', ill6),
]
LS = 400
S.append(page(IV, f'''
<div class=abs style="left:0;right:0;top:330px;display:flex;justify-content:center"><img src="{LOGO}" width="{LS}" height="{LS}"></div>
<div class="abs serif" style="left:80px;right:80px;top:{330 + LS + 60}px;text-align:center;font-size:76px;line-height:1.14;font-weight:700;color:{G}">Aqui você fica por dentro de tudo sobre a Espanha</div>
<div class=abs style="left:50%;margin-left:-65px;top:{330 + LS + 60 + 76 * 3 + 40}px;width:130px;height:5px;background:{GOLD}"></div>
<div class="abs serif" style="left:80px;right:80px;top:{330 + LS + 60 + 76 * 3 + 80}px;text-align:center;font-size:58px;font-weight:700;color:{TERRA}">Espanha Sem Segredo</div>
<div class=abs style="left:80px;right:80px;top:{330 + LS + 60 + 76 * 3 + 160}px;text-align:center;font-size:42px;color:{G}">Siga <b>@espanhasemsegredo</b></div>
<div class=abs style="left:100px;right:100px;bottom:160px;text-align:center;font-size:25px;line-height:1.5;color:{G};opacity:.85">Fontes: UNESCO e Generalitat de Catalunya. Consulta em 28/10/2026.<br>Conteúdo informativo, não é assessoria jurídica.</div>'''))


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, htm in enumerate(S):
            await pg.set_content(htm)
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT + f'cultura-{i + 1}.png')
        await b.close()

asyncio.run(main())
n = len(S); d = 3.5; f = 0.4
cmd = ['ffmpeg', '-y', '-loglevel', 'error']
for i in range(n):
    cmd += ['-loop', '1', '-t', str(d), '-i', OUT + f'cultura-{i + 1}.png']
flt = ''.join(f'[{i}:v]format=yuv420p,fade=t=in:st=0:d={f},fade=t=out:st={d - f}:d={f}[v{i}];' for i in range(n))
flt += ''.join(f'[v{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0[o]'
cmd += ['-filter_complex', flt, '-map', '[o]', '-r', '30', '-pix_fmt', 'yuv420p', OUT + 'reel-cultura.mp4']
subprocess.run(cmd, check=True)
