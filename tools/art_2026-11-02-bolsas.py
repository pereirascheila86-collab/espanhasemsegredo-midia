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
<g transform="translate(540 760)"><path d="M0 -150L300 -30L0 90L-300 -30Z" fill="{IV}"/><path d="M-170 40V190Q0 280 170 190V40L0 110Z" fill="{GOLD}"/><path d="M270 -14V200" stroke="{GOLD}" stroke-width="9"/><circle cx="270" cy="222" r="26" fill="{TERRA}"/></g>
<g transform="translate(170 960) rotate(-6)"><rect width="300" height="180" rx="16" fill="{IV}"/><path d="M30 50H270M30 90H270M30 130H190" stroke="{G}" stroke-width="12" stroke-linecap="round" opacity=".3"/><circle cx="240" cy="140" r="34" fill="{TERRA}"/></g>
<g transform="translate(720 1000)"><circle r="82" fill="{GOLD}"/><circle r="64" fill="none" stroke="{G}" stroke-width="5" stroke-dasharray="6 7"/>{txt(0, 22, '€', 78, G, 700, 'Lora')}</g>
</svg>
{bracket(56)}
<div class=abs style="left:80px;top:96px"><span class=kick style="color:{GOLD}">Imigração · Bolsas de estudo</span></div>
<div class="abs serif" style="left:80px;top:160px;width:880px;font-size:72px;line-height:1.08;font-weight:700;color:{IV}">Quer estudar na Espanha <span style="color:{GOLD};font-style:italic">com bolsa?</span></div>
<div class=abs style="left:80px;top:420px;width:900px;font-size:38px;line-height:1.38;color:{IV}">Veja as opções para quem está no exterior e quando as inscrições costumam abrir.</div>
{foot(IV, 50)}''')
    # 2 Carolina: 736 bolsas em barras por categoria
    def bar(y, v, lab):
        return f'{txt(30, y + 32, lab, 26, G, 800, "Inter", 0, "start")}<rect x="400" y="{y}" width="{v * 1.7}" height="44" rx="10" fill="{TERRA if v > 200 else G}"/>{txt(400 + v * 1.7 + 14, y + 33, v, 32, G, 700, "Lora", 0, "start")}'
    ill2 = sv(f'{txt(460, 36, "736 BOLSAS · 203 PROGRAMAS", 28, G, 800, "Inter", 4)}' + bar(66, 228, 'Pós-graduação') + bar(126, 120, 'Doutorado e pós-doc') + bar(186, 114, 'Renovações') + bar(246, 24, 'Mobilidade de professores') + bar(306, 250, 'Estudos institucionais'), VB)
    # 3 quem pode: pessoa com mapa-mundi simplificado e selo
    ill3 = sv(f'''<g transform="translate(60 30)"><rect width="360" height="300" rx="24" fill="{G}"/>{human(120, 40, 1.4, IV)}<rect x="200" y="70" width="120" height="150" rx="10" fill="{IV}"/><path d="M216 100H304M216 126H304M216 152H270" stroke="{G}" stroke-width="9" stroke-linecap="round" opacity=".4"/><circle cx="296" cy="200" r="22" fill="{TERRA}"/>{txt(180, 270, 'TÍTULO DE GRADUAÇÃO', 22, PALEG, 800, 'Inter', 3)}</g>
<g transform="translate(470 30)"><rect width="390" height="300" rx="24" fill="{G2}"/><circle cx="195" cy="130" r="96" fill="none" stroke="{GOLD}" stroke-width="6" opacity=".5"/><circle cx="195" cy="130" r="58" fill="none" stroke="{GOLD}" stroke-width="6" opacity=".7"/><path d="M195 70C165 70 150 92 150 114C150 144 195 190 195 190C195 190 240 144 240 114C240 92 225 70 195 70Z" fill="{TERRA}"/><circle cx="195" cy="114" r="16" fill="{IV}"/>{txt(195, 262, 'IBERO-AMÉRICA', 26, PALEG, 800, 'Inter', 4)}</g>''', VB)
    # 4 quando abre: duas linhas do tempo
    def tl(y, yr, op, c1, c2):
        return (f'<path d="M80 {y}H840" stroke="{IV}" stroke-width="8" stroke-linecap="round"/>'
                f'<g transform="translate(150 {y})"><circle r="30" fill="{GOLD}"/>{txt(0, 48 + 22, op, 24, IV, 800, "Inter", 0)}{txt(0, -46, "ABRE", 20, PALEG, 800, "Inter", 4)}</g>'
                f'<g transform="translate(480 {y})"><circle r="30" fill="{TERRA}"/>{txt(0, 70, c1, 24, IV, 800, "Inter", 0)}{txt(0, -46, "PÓS-GRAD.", 20, PALEG, 800, "Inter", 3)}</g>'
                f'<g transform="translate(780 {y})"><circle r="30" fill="{IV}"/>{txt(0, 70, c2, 24, IV, 800, "Inter", 0)}{txt(0, -46, "DOUTORADO", 20, PALEG, 800, "Inter", 3)}</g>'
                f'{txt(30, y - 56, yr, 30, GOLD, 700, "Lora", 0, "start")}')
    ill4 = sv(tl(100, '2025', '14/01', '12/03', '03/04') + tl(280, '2026', '12/01', '02/03', '09/04'), VB)
    # 5 Santander: universidade -> bolsa
    ill5 = sv(f'''<g transform="translate(60 50)"><path d="M0 100L130 20L260 100Z" fill="{GOLD}"/><rect x="16" y="100" width="228" height="16" fill="{IV}"/>{''.join(f'<rect x="{26 + i * 50}" y="122" width="26" height="110" rx="5" fill="{IV}"/>' for i in range(4))}<rect x="0" y="232" width="260" height="26" rx="6" fill="{IV}"/></g>
<path d="M350 170H500" stroke="{IV}" stroke-width="10" stroke-linecap="round"/><path d="M476 142L506 170L476 198" fill="none" stroke="{IV}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<g transform="translate(560 60)"><rect width="300" height="220" rx="22" fill="{IV}"/><circle cx="76" cy="110" r="46" fill="{TERRA}"/>{txt(76, 128, '€', 54, IV, 700, 'Lora')}{txt(206, 100, '1.500', 52, G, 700, 'Lora')}{txt(206, 144, 'exemplo USC', 22, G, 800, 'Inter', 2)}</g>
{txt(460, 340, 'a universidade publica a convocatória', 26, IV, 800, 'Inter', 2)}''', VB)
    # 6 antes de se candidatar: checklist
    def chk(y, s):
        return f'<g transform="translate(70 {y})"><rect width="56" height="56" rx="12" fill="{GOLD}"/><path d="M14 30L25 41L43 16" fill="none" stroke="{G}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>{txt(150, y + 40, s, 34, G, 800, "Inter", 0, "start")}'
    ill6 = sv(chk(20, 'Ler a convocatória completa') + chk(110, 'Conferir país e curso') + chk(200, 'Anotar prazo de cada bolsa') + chk(290, 'Usar só o site oficial'), VB)
    S = [
        cover,
        cslide(IV, G, TERRA, K, 'Fundación Carolina', 'Na convocatória 2026-2027, foram 736 bolsas em 203 programas: pós-graduação, doutorado e estadias pós-doutorais para estudantes e profissionais ibero-americanos.', ill2, tsize=62),
        cslide(SAND, G, TERRA, K, 'Quem pode pedir', 'A página oficial fala em graduados, nacionais e residentes de país latino-americano da Comunidade Ibero-americana de Nações, mais Portugal, com currículo sobressalente. Confirme na convocatória.', ill3),
        cslide(G, IV, PALEG, K, 'Quando abre', 'A última abriu em 12/01/2026, com prazo de pós-graduação em 02/03. A de 2027-2028 ainda não foi anunciada nas fontes consultadas. Acompanhe o site oficial.', ill4, tsize=62),
        cslide(TERRA, IV, PALEG, K, 'Bolsas Santander', 'Para intercâmbio, cada universidade publica a sua convocatória. Em 2026/27, a USC ofereceu 45 bolsas de 1.500 € e o cadastro foi até 15/09/2026.', ill5.replace(f'fill="{G}"', f'fill="{G2}"')),
        cslide(IV, G, TERRA, K, 'Antes de se candidatar', 'Cada programa tem requisitos e prazos próprios. Leia a convocatória do início ao fim e confirme tudo no site oficial da instituição.', ill6),
        closing(1350, 'Fontes: Fundación Carolina, Exteriores (Embaixada em Brasília) e USC. Consulta em 02/11/2026.', logo=250, bottom=50),
    ]
    return S


asyncio.run(render(imig(), 'bolsas', 1350))
