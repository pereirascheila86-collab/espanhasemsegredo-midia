"""Arte de 03/11/2026: Reel VOCÊ SABIA? Caminho de Santiago (5 telas, 1080x1920 + MP4).
Uso: ART_OUT=2026-11-03 python3 tools/art_2026-11-03-cultura.py
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


def culture():
    K = 'VOCÊ SABIA? | ESPANHA'
    V = '0 0 960 760'
    ground = lambda c: f'<rect x="40" y="712" width="880" height="24" rx="12" fill="{c}"/>'
    # 1 capa: vieira (concha) com raios, cajado e cabaça
    rays = ''.join(f'<path d="M480 560L{480 + 330 * math.cos(math.radians(a)):.0f} {560 - 330 * math.sin(math.radians(a)):.0f}" stroke="{GOLD}" stroke-width="14" stroke-linecap="round"/>' for a in range(25, 160, 15))
    lines = ''.join(f'<path d="M480 600L{480 + 300 * math.cos(math.radians(a)):.0f} {590 - 330 * math.sin(math.radians(a)):.0f}" stroke="{IV}" stroke-width="6" opacity=".55"/>' for a in range(30, 155, 20))
    ill1 = sv(f'''{ground(GOLD)}{rays}
<path d="M200 560Q200 240 480 220Q760 240 760 560Q480 640 200 560Z" fill="{TERRA}"/>{lines}
<path d="M200 560Q480 650 760 560L720 640Q480 700 240 640Z" fill="{PALEG}"/>
<rect x="436" y="640" width="88" height="70" rx="14" fill="{G2}"/>
<path d="M850 120V700" stroke="{IV}" stroke-width="16" stroke-linecap="round"/><circle cx="850" cy="150" r="36" fill="{IV}"/><ellipse cx="850" cy="240" rx="42" ry="56" fill="{GOLD}"/>''', V)
    # 2 selo europeu: anel de estrelas com seta de caminho
    ill2 = sv(f'''
<circle cx="480" cy="320" r="290" fill="{G}"/>{star_ring(480, 320, 225, 28, GOLD)}
<path d="M360 470Q420 380 480 400T600 250" fill="none" stroke="{IV}" stroke-width="14" stroke-linecap="round" stroke-dasharray="2 30"/>
<path d="M560 230L620 240L600 300" fill="none" stroke="{TERRA}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
{txt(480, 720, '1987', 120, TERRA, 700, 'Lora')}''', V)
    # 3 Pireneus -> catedral: caminho
    ill3 = sv(f'''{ground(G)}
<path d="M40 420L180 200L260 320L340 190L470 420Z" fill="{G2}"/><path d="M180 200L210 250L150 250Z M340 190L370 240L310 240Z" fill="{IV}"/>
<path d="M120 700C300 620 140 560 340 520S560 470 560 430" fill="none" stroke="{GOLD}" stroke-width="22" stroke-linecap="round"/>
<g transform="translate(700 180)"><rect x="-150" y="260" width="300" height="270" fill="{G}"/><rect x="-150" y="130" width="70" height="160" fill="{G}"/><rect x="80" y="130" width="70" height="160" fill="{G}"/>
<path d="M-150 130L-115 40L-80 130Z M80 130L115 40L150 130Z" fill="{TERRA}"/><path d="M-60 530V380Q0 310 60 380V530Z" fill="{IV}"/><path d="M0 330V250M-20 285H20" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/></g>
{txt(260, 120, 'PIRENEUS', 28, G, 800, 'Inter', 6)}{txt(700, 130, 'GALÍCIA', 28, G, 800, 'Inter', 6)}''', V)
    # 4 costa norte: ondas, linha de costa e marcos
    waves = ''.join(f'<path d="M40 {590 + i * 46}Q140 {560 + i * 46} 240 {590 + i * 46}T440 {590 + i * 46}T640 {590 + i * 46}T840 {590 + i * 46}" fill="none" stroke="{IV}" stroke-width="8" stroke-linecap="round" opacity="{0.9 - i * .2}"/>' for i in range(3))
    ill4 = sv(f'''{waves}
<path d="M60 420C200 300 330 400 480 330S720 240 900 300" fill="none" stroke="{PALEG}" stroke-width="22" stroke-linecap="round"/>
<circle cx="150" cy="365" r="22" fill="{G}"/><circle cx="330" cy="372" r="22" fill="{G}"/><circle cx="520" cy="326" r="22" fill="{G}"/><circle cx="720" cy="270" r="22" fill="{G}"/>
{txt(480, 150, 'CAMINHOS DO NORTE', 44, IV, 800, 'Inter', 6)}''', V)
    return [
        reel_slide(G, IV, PALEG, K, 'O Caminho de Santiago é <span style="color:%s;font-style:italic">Patrimônio Mundial</span> da UNESCO' % PALEG, ill1),
        reel_slide(IV, G, TERRA, K, 'Em 1987, foi o primeiro Itinerário Cultural Europeu', ill2),
        reel_slide(SAND, G, TERRA, K, 'Em 1993, a UNESCO inscreveu o Caminho Francês, dos Pireneus à Galícia', ill3),
        reel_slide(TERRA, IV, PALEG, K, 'Em 2015, o reconhecimento foi ampliado aos Caminhos do Norte', ill4),
        closing(1920, 'Fontes: Ayuntamiento de Pamplona (8/11/2023) e Santiagoways. Consulta em 03/11/2026.', logo=400, bottom=160),
    ]


which = sys.argv[1:] or ['cultura']
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
