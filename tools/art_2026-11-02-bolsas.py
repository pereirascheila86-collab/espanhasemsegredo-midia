"""Arte de 02/11/2026: carrossel Bolsas de estudo para estrangeiros (7 slides, 1080x1350). Uso: ART_OUT=2026-11-02 python3 tools/art_2026-11-02-bolsas.py"""
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


def imig():
    K = 'Imigração · Bolsas de estudo'
    VB = '0 0 920 370'
    cover = page(1350, G, f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:repeating-linear-gradient(45deg,rgba(201,162,74,.07) 0 2px,transparent 2px 40px)"></div>
<svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">
<g transform="translate(540 790)"><path d="M0 -150L300 -30L0 90L-300 -30Z" fill="{IV}"/><path d="M-170 40V190Q0 280 170 190V40L0 110Z" fill="{GOLD}"/><path d="M270 -14V200" stroke="{GOLD}" stroke-width="9"/><circle cx="270" cy="222" r="26" fill="{TERRA}"/></g>
<g transform="translate(170 1000) rotate(-6)"><rect width="300" height="170" rx="16" fill="{IV}"/><path d="M30 50H270M30 90H270M30 130H190" stroke="{G}" stroke-width="12" stroke-linecap="round" opacity=".3"/><circle cx="240" cy="130" r="34" fill="{TERRA}"/></g>
<g transform="translate(760 1030)"><circle r="82" fill="{GOLD}"/><circle r="64" fill="none" stroke="{G}" stroke-width="5" stroke-dasharray="6 7"/>{txt(0, 22, '€', 78, G, 700, 'Lora')}</g>
</svg>
{bracket(56)}
<div class=abs style="left:80px;top:96px"><span class=kick style="color:{GOLD}">Imigração · Bolsas de estudo</span></div>
<div class="abs serif" style="left:80px;top:160px;width:880px;font-size:68px;line-height:1.08;font-weight:700;color:{IV}">Bolsas para estudar na Espanha: <span style="color:{GOLD};font-style:italic">o que abre e quando</span></div>
<div class=abs style="left:80px;top:470px;width:900px;font-size:36px;line-height:1.38;color:{IV}">Fundación Carolina e Becas García Lorca (Andaluzia, com Sevilha). Veja a situação de cada uma hoje.</div>
{foot(IV, 50)}''')
    # 2 situação: dois cartões de status
    def pill(x, y, w, col, tc, t1, t2):
        return f'<g transform="translate({x} {y})"><rect width="{w}" height="130" rx="22" fill="{col}"/>{txt(w / 2, 52, t1, 26, tc, 800, "Inter", 3)}{txt(w / 2, 100, t2, 40, tc, 700, "Lora")}</g>'
    ill2 = sv(pill(40, 30, 400, G, PALEG, 'CURSO 2026-2027', 'Encerrada') + pill(480, 30, 400, TERRA, IV, 'CURSO 2027-2028', 'Ainda não abriu') +
              f'<path d="M240 190V235M680 190V235" stroke="{G}" stroke-width="6" stroke-linecap="round"/>' +
              f'<rect x="40" y="235" width="840" height="100" rx="22" fill="{G2}"/>{txt(460, 296, "Hora de se preparar", 44, IV, 700, "Lora")}', VB)
    # 3 Carolina: três calendários
    def cal(x, dt, lab, col):
        d, m = dt
        return f'<g transform="translate({x} 40)"><rect width="250" height="240" rx="20" fill="{IV}"/><rect width="250" height="64" rx="20" fill="{col}"/><rect y="40" width="250" height="24" fill="{col}"/>{txt(125, 46, m, 28, IV if col != GOLD else G, 800, "Inter", 6)}{txt(125, 160, d, 96, G, 700, "Lora")}{txt(125, 214, lab, 22, TERRA, 800, "Inter", 2)}</g>'
    ill3 = sv(cal(30, ('12', 'JAN 2026'), 'ABERTURA', TERRA) + cal(335, ('02', 'MAR 2026'), 'PÓS-GRAD.', G) + cal(640, ('09', 'ABR 2026'), 'DOUTORADO', G2) + txt(460, 340, 'prazos da última convocatória', 24, G, 800, 'Inter', 3), VB)
    # 4 como se candidatar: tela com passos
    def step(y, t, done=False):
        return f'<rect x="60" y="{y}" width="40" height="40" rx="10" fill="{GOLD}"/><path d="M69 {y + 21}L78 {y + 30}L92 {y + 10}" fill="none" stroke="{G}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>{txt(120, y + 30, t, 28, G, 800, "Inter", 0, "start")}'
    ill4 = sv(f'<rect x="30" y="10" width="640" height="350" rx="22" fill="{IV}"/><rect x="30" y="10" width="640" height="52" rx="22" fill="{G}"/><circle cx="62" cy="36" r="8" fill="{GOLD}"/><circle cx="90" cy="36" r="8" fill="{TERRA}"/>' + step(92, 'Cadastro online') + step(150, 'Nota média equivalente') + step(208, 'Até 5 programas') + step(266, 'Sem envio de documentos') +
              f'<g transform="translate(700 150)"><rect width="190" height="80" rx="40" fill="{TERRA}"/>{txt(95, 52, "Recibido", 30, IV, 800, "Inter", 0)}</g>', VB)
    # 5 García Lorca: universidade + 56
    ill5 = sv(f'''<g transform="translate(50 40)"><path d="M0 100L140 20L280 100Z" fill="{GOLD}"/><rect x="16" y="100" width="248" height="16" fill="{IV}"/>{''.join(f'<rect x="{28 + i * 54}" y="122" width="28" height="120" rx="5" fill="{IV}"/>' for i in range(4))}<rect x="0" y="242" width="280" height="28" rx="6" fill="{IV}"/></g>
<g transform="translate(450 60)"><circle cx="110" cy="110" r="110" fill="{IV}"/>{txt(110, 138, '56', 100, G, 700, 'Lora')}{txt(110, 178, 'BOLSAS', 24, TERRA, 800, 'Inter', 5)}</g>
<g transform="translate(720 90)"><rect width="170" height="200" rx="18" fill="{G}"/>{txt(85, 70, 'MATRÍCULA', 19, PALEG, 800, 'Inter', 1)}{txt(85, 120, '+', 50, IV, 700, 'Lora')}{txt(85, 160, 'ALOJAMENTO', 19, PALEG, 800, 'Inter', 0)}</g>
{txt(460, 362, 'universidades públicas da Andaluzia', 26, IV, 800, 'Inter', 2)}''', VB)
    # 6 García Lorca prazo e pedido: faixa de datas + documentos
    ill6 = sv(f'''<g transform="translate(40 40)"><rect width="400" height="200" rx="22" fill="{G}"/>{txt(200, 52, 'EM 2026', 24, PALEG, 800, 'Inter', 6)}{txt(200, 124, '25/03 a 08/04', 52, IV, 700, 'Lora')}{txt(200, 168, 'pela plataforma da AUIP', 22, PALEG, 800, 'Inter', 2)}</g>
<g transform="translate(480 40)">{''.join(f'<g transform="translate({i * 140} {(i % 2) * 20})"><rect width="120" height="150" rx="12" fill="{IV}"/><path d="M18 40H102M18 66H102M18 92H70" stroke="{G}" stroke-width="8" stroke-linecap="round" opacity=".35"/><circle cx="90" cy="124" r="14" fill="{TERRA}"/></g>' for i in range(3))}</g>
{txt(660, 250, 'histórico · diploma · cartas', 24, IV, 800, 'Inter', 2)}
<g transform="translate(40 270)"><rect width="840" height="70" rx="18" fill="{TERRA}"/>{txt(420, 46, 'Média de 7,5 a 10 na escala de 1 a 10', 30, IV, 800, 'Inter', 0)}</g>''', VB)
    S = [
        cover,
        cslide(IV, G, TERRA, K, 'Situação hoje', 'Os pedidos de 2026-2027 já encerraram. As convocatórias de 2027-2028 ainda não foram publicadas nas fontes oficiais consultadas. É o momento de se preparar.', ill2, tsize=62),
        cslide(SAND, G, TERRA, K, 'Fundación Carolina: ainda não abriu', 'A convocatória é anual e costuma abrir no início de janeiro. A última abriu em 12/01/2026, com prazo de pós-graduação até 02/03 e de doutorado até 09/04.', ill3, tsize=56, lines=2),
        cslide(G, IV, PALEG, K, 'Carolina: como se candidatar', 'O pedido é online, sem envio de documentos. Faça o cadastro, informe a nota média equivalente e escolha até 5 programas. Depois, confira se o status é Recibido.', ill4.replace(f'fill="{G}"', f'fill="{G2}"', 1), tsize=58),
        cslide(TERRA, IV, PALEG, K, 'García Lorca: ainda não abriu', 'Em 2026-2027, foram 56 bolsas de mestrado nas universidades públicas da Andaluzia, incluindo Sevilha. Cobrem matrícula e, nas aulas presenciais, alojamento e alimentação.', ill5.replace(f'fill="{G}"', f'fill="{G2}"'), tsize=58),
        cslide(IV, G, TERRA, K, 'García Lorca: prazo e pedido', 'Em 2026, o prazo foi de 25/03 a 08/04. É preciso morar fora da Espanha, ter média de 7,5 a 10 e carta de referência. A de 2027-2028 ainda não saiu.', ill6, tsize=58),
        closing(1350, 'Fontes: Fundación Carolina, AUIP e Universidad de Sevilla. Consulta em 02/11/2026.', logo=250, bottom=50),
    ]
    return S


asyncio.run(render(imig(), 'bolsas', 1350))
