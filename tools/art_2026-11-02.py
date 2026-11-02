"""Artes de 02/11/2026: Reel VOCÊ SABIA? Lotería de Navidad (5 telas, 1080x1920 + MP4) e carrossel Série Arraigo parte 4 (7 slides, 1080x1350).
Uso: ART_OUT=2026-11-02 python3 tools/art_2026-11-02.py [cultura|imigracao]
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
    # 1 capa: bombo de sorteio com bolas e um décimo
    balls = ''.join(f'<circle cx="{x}" cy="{y}" r="22" fill="{c}"/>' for x, y, c in [(330, 250, GOLD), (400, 300, TERRA), (470, 230, IV), (540, 310, GOLD), (610, 260, TERRA), (420, 380, IV), (520, 390, GOLD)])
    ill1 = sv(f'''{ground(GOLD)}
<circle cx="470" cy="320" r="190" fill="{G2}"/><circle cx="470" cy="320" r="190" fill="none" stroke="{GOLD}" stroke-width="10"/>{balls}
<path d="M470 510V640M340 700L400 600H540L600 700Z" stroke="{GOLD}" stroke-width="12" fill="{TERRA}" stroke-linejoin="round"/>
<path d="M660 320H760" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/><circle cx="780" cy="320" r="26" fill="{TERRA}"/>
<g transform="translate(760 560) rotate(-8)"><rect x="-90" y="-60" width="180" height="120" rx="12" fill="{IV}"/><rect x="-90" y="-60" width="180" height="30" rx="12" fill="{TERRA}"/>{txt(0, 30, '20 €', 44, G, 800, 'Lora')}</g>''', V)
    # 2 calendário 22 + abeto
    ill2 = sv(f'''{ground(G)}
<g transform="translate(300 80)"><rect width="420" height="560" rx="30" fill="{IV}"/><rect width="420" height="130" rx="30" fill="{TERRA}"/><rect y="90" width="420" height="40" fill="{TERRA}"/>
{txt(210, 90, 'DEZEMBRO', 46, IV, 800, 'Inter', 8)}{txt(210, 360, '22', 230, G, 700, 'Lora')}{txt(210, 470, '2026', 56, TERRA, 800, 'Inter', 10)}
<circle cx="90" cy="0" r="14" fill="{GOLD}"/><circle cx="330" cy="0" r="14" fill="{GOLD}"/></g>
<g transform="translate(130 700)"><path d="M0 -330L-90 -170H-40L-120 -40H-60L-140 90H140L60 -40H120L40 -170H90Z" fill="{G2}"/><rect x="-18" y="90" width="36" height="40" fill="{TERRA}"/>{star(0, -340, 36, GOLD)}</g>''', V)
    # 3 décimo dividido em 10 partes
    parts = ''.join(f'<rect x="{80 + i * 80}" y="250" width="72" height="260" rx="8" fill="{TERRA if i == 3 else G2}"/>' for i in range(10))
    ill3 = sv(f'''{ground(GOLD)}{parts}
<path d="M80 200H880" stroke="{G}" stroke-width="6"/><path d="M80 186V214M880 186V214" stroke="{G}" stroke-width="6"/>
{txt(480, 160, 'UM NÚMERO = 10 DÉCIMOS', 36, G, 800, 'Inter', 4)}
<g transform="translate(400 560)"><path d="M0 -30V-60" stroke="{G}" stroke-width="5"/><rect x="-110" y="0" width="220" height="110" rx="20" fill="{G}"/>{txt(0, 78, '20 €', 62, PALEG, 700, 'Lora')}</g>''', V)
    # 4 moedas empilhadas + faixa 400.000
    def stack(x, n):
        return ''.join(f'<ellipse cx="{x}" cy="{650 - i * 34}" rx="90" ry="26" fill="{GOLD if i % 2 == 0 else PALEG}"/>' for i in range(n))
    ill4 = sv(f'''{ground(IV)}{stack(210, 7)}{stack(430, 11)}{stack(650, 5)}{stack(790, 3)}
<g transform="translate(480 200)"><rect x="-330" y="-100" width="660" height="200" rx="26" fill="{INK}"/>{txt(0, 20, '400.000 €', 112, GOLD, 700, 'Lora')}{txt(0, 72, 'POR DÉCIMO · 4 MILHÕES POR SÉRIE', 26, IV, 800, 'Inter', 3)}</g>''', V)
    S = [
        reel_slide(G, IV, PALEG, K, 'Na Espanha, o Natal tem um sorteio: <span style="color:%s;font-style:italic">o Gordo</span>' % PALEG, ill1),
        reel_slide(IV, G, TERRA, K, 'O Sorteo de Navidad de 2026 será em 22 de dezembro', ill2),
        reel_slide(SAND, G, TERRA, K, 'O bilhete é dividido em décimos. Cada um custa 20 €, segundo a imprensa', ill3),
        reel_slide(TERRA, IV, PALEG, K, 'O Gordo paga 400.000 € por décimo, segundo a imprensa', ill4.replace(f'fill="{IV}"/>', f'fill="{PALEG}"/>', 1)),
        closing(1920, 'Fontes: Demócrata (8/7/2026) e Zaragozala (9/7/2026). Consulta em 02/11/2026.', logo=400, bottom=160),
    ]
    return S


def imig():
    K = 'Série Arraigo · Parte 4 de 4'
    VB = '0 0 920 370'
    # capa: família sob anel de estrelas, casa
    cover = page(1350, G, f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:repeating-linear-gradient(135deg,rgba(201,162,74,.07) 0 2px,transparent 2px 44px)"></div>
<svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">
{star_ring(540, 860, 250, 24, GOLD)}
<path d="M300 1010L540 800L780 1010Z" fill="{TERRA}"/><rect x="340" y="1010" width="400" height="170" rx="10" fill="{IV}"/><rect x="500" y="1070" width="80" height="110" rx="10" fill="{G}"/>
{human(430, 810, 1.6, GOLD)}{human(650, 900, 1.0, PALEG)}
<path d="M240 1180H840" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>
</svg>
{bracket(56)}
<div class=abs style="left:80px;top:96px"><span class=kick style="color:{GOLD}">Imigração · Série Arraigo</span></div>
<div class="abs serif" style="left:80px;top:160px;width:880px;font-size:76px;line-height:1.08;font-weight:700;color:{IV}">Parte 4 de 4: <span style="color:{GOLD};font-style:italic">arraigo familiar</span></div>
<div class=abs style="left:80px;top:340px;width:900px;font-size:38px;line-height:1.38;color:{IV}">Para pai, mãe ou tutor de menor europeu e para quem apoia uma pessoa com deficiência europeia.</div>
{foot(IV, 50)}''')
    # 2 sem permanência mínima: calendário de 2 anos riscado + casa com check
    ill2 = sv(f'''<g transform="translate(60 40)"><rect width="320" height="260" rx="22" fill="{G}"/><rect width="320" height="70" rx="22" fill="{TERRA}"/>{txt(160, 50, 'ANOS', 30, IV, 800, 'Inter', 8)}{txt(160, 190, '2', 140, PALEG, 700, 'Lora')}
<path d="M-20 270L340 -10" stroke="{TERRA}" stroke-width="22" stroke-linecap="round"/></g>
{txt(220, 340, 'Outros arraigos', 26, G, 800, 'Inter', 3)}
<g transform="translate(520 18)"><path d="M0 120L160 0L320 120Z" fill="{GOLD}"/><rect x="30" y="120" width="260" height="170" rx="10" fill="{G}"/><rect x="130" y="190" width="60" height="100" rx="8" fill="{IV}"/>
<circle cx="260" cy="260" r="48" fill="{TERRA}"/><path d="M238 260L254 276L284 242" fill="none" stroke="{IV}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>
{txt(680, 360, 'Arraigo familiar', 26, G, 800, 'Inter', 3)}''', VB)
    # 3 quem pode: adulto+criança e apoio, com selo de estrelas
    ill3 = sv(f'''<g transform="translate(60 20)"><rect width="390" height="300" rx="24" fill="{G}"/>{human(130, 40, 1.4, IV)}{human(260, 100, 0.9, PALEG)}{txt(195, 276, 'PAI · MÃE · TUTOR', 25, PALEG, 800, 'Inter', 3)}</g>
<g transform="translate(480 20)"><rect width="390" height="300" rx="24" fill="{G2}"/>{human(120, 40, 1.4, IV)}
<path d="M190 150C220 128 250 128 280 150" fill="none" stroke="{PALEG}" stroke-width="16" stroke-linecap="round"/>
<path d="M290 80C290 60 320 54 330 78C340 54 370 60 370 80C370 104 330 126 330 126C330 126 290 104 290 80Z" fill="{TERRA}"/>{txt(195, 276, 'APOIO A PESSOA COM DEFICIÊNCIA', 20, PALEG, 800, 'Inter', 1)}</g>
{txt(460, 362, 'nacionalidade UE · EEE · Suíça', 24, G, 800, 'Inter', 2)}''', VB)
    # 4 guarda e convivência: casa, documento com selo
    ill4 = sv(f'''<g transform="translate(70 30)"><path d="M0 120L170 0L340 120Z" fill="{TERRA}"/><rect x="30" y="120" width="280" height="190" rx="10" fill="{IV}"/>{human(120, 160, 1.3, G)}{human(220, 215, 0.85, GOLD)}</g>
<g transform="translate(520 40)"><rect width="330" height="290" rx="18" fill="{IV}"/>{txt(30, 62, 'GUARDA', 26, TERRA, 800, 'Inter', 6, 'start')}<path d="M30 110H300M30 150H300M30 190H220" stroke="{G}" stroke-width="12" stroke-linecap="round" opacity=".3"/>
<circle cx="250" cy="236" r="46" fill="{TERRA}"/><circle cx="250" cy="236" r="35" fill="none" stroke="{IV}" stroke-width="3" stroke-dasharray="5 5"/><path d="M230 236L245 251L272 220" fill="none" stroke="{IV}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></g>''', VB)
    # 5 apoio: balança da capacidade jurídica + duas pessoas lado a lado
    ill5 = sv(f'''{human(130, 60, 1.9, IV)}{human(300, 110, 1.5, PALEG)}
<path d="M205 220C240 200 262 206 276 230" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/>
<g transform="translate(640 40)"><path d="M0 40V260M-90 260H90" stroke="{IV}" stroke-width="12" stroke-linecap="round"/><path d="M-170 70H170" stroke="{IV}" stroke-width="12" stroke-linecap="round"/><circle cx="0" cy="40" r="20" fill="{GOLD}"/>
<path d="M-170 70L-220 160H-120Z M170 70L120 160H220Z" fill="none" stroke="{IV}" stroke-width="5"/><path d="M-240 160H-100Q-100 215 -170 215Q-240 215 -240 160Z" fill="{G}"/><path d="M100 160H240Q240 215 170 215Q100 215 100 160Z" fill="{G}"/></g>
{txt(640, 350, 'capacidade jurídica', 28, IV, 800, 'Inter', 3)}''', VB)
    # 6 resposta: três meses até o envelope
    mon = ''.join(f'<g transform="translate({60 + i * 190} 90)"><rect width="170" height="170" rx="20" fill="{G if i < 2 else G2}"/>{txt(85, 100, str(i + 1), 96, PALEG, 700, "Lora")}{txt(85, 146, "MÊS", 24, IV, 800, "Inter", 6)}</g>' for i in range(3))
    ill6 = sv(f'''{mon}<path d="M610 175H680" stroke="{G}" stroke-width="10" stroke-linecap="round"/><path d="M660 150L690 175L660 200" fill="none" stroke="{G}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate(710 90)"><rect width="170" height="130" rx="14" fill="{TERRA}"/><path d="M0 14L85 80L170 14" fill="none" stroke="{IV}" stroke-width="8"/></g>
{txt(460, 330, 'o que a ficha oficial prevê', 28, G, 800, 'Inter', 3)}''', VB)
    S = [
        cover,
        cslide(IV, G, TERRA, K, 'Diferença importante', 'A ficha oficial não exige permanência mínima, diferente dos outros arraigos. É preciso comprovar residência na Espanha ao pedir. Quem pede não pode ser cidadão da UE, do EEE ou da Suíça.', ill2, tsize=62),
        cslide(SAND, G, TERRA, K, 'Quem pode pedir', 'Pai, mãe ou tutor de menor com nacionalidade de outro Estado da UE, do EEE ou da Suíça. Também quem dá apoio a uma pessoa com deficiência com essa nacionalidade.', ill3),
        cslide(G, IV, PALEG, K, 'Pai, mãe ou tutor', 'É preciso ter a guarda do menor e conviver com ele, ou estar em dia com as obrigações de pai ou mãe.', ill4),
        cslide(TERRA, IV, PALEG, K, 'Quem dá apoio', 'É preciso ser familiar da pessoa, tê-la a cargo e conviver com ela, para apoiá-la no exercício da capacidade jurídica.', ill5),
        cslide(IV, G, TERRA, K, 'Prazo de resposta', 'A ficha oficial prevê decisão em até 3 meses, contados da entrada do pedido no registro do órgão competente. Vale sempre a norma vigente na data do pedido.', ill6, tsize=62),
        closing(1350, 'Série Arraigo: social, sociolaboral, socioformativo e familiar<br>Fonte: Ministerio de Inclusión, consulta em 29/10/2026.', logo=250, bottom=50),
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
