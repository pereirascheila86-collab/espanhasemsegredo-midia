"""Carrossel de imigração de 03/11/2026: CCSE (7 slides, 1080x1350).
Estilo do dia: capa verde-petróleo com letras gigantes douradas, miolo areia com cartão-etiqueta lateral.
Uso: ART_OUT=2026-11-03 python3 tools/art_2026-11-03.py
"""
import base64, asyncio, os, html
from playwright.async_api import async_playwright

B = os.path.dirname(os.path.abspath(__file__)) + '/../'
OUT = os.environ.get('ART_OUT', B + 'saida/') + '/'
os.makedirs(OUT, exist_ok=True)
LOGO = 'data:image/png;base64,' + base64.b64encode(open(B + 'marca/logo-espanha-sem-segredo.png', 'rb').read()).decode()
G = '#0F3D3A'; G2 = '#1E5550'; GOLD = '#C9A24A'; TERRA = '#B8573A'; IV = '#F5F1E8'; INK = '#24292C'; SAND = '#E9DFC9'

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

def grid_bg(col, op):
    lines = ''.join(f'<path d="M{x} 0V1350" stroke="{col}" stroke-opacity="{op}" stroke-width="2"/>' for x in range(0, 1081, 120))
    lines += ''.join(f'<path d="M0 {y}H1080" stroke="{col}" stroke-opacity="{op}" stroke-width="2"/>' for y in range(0, 1351, 120))
    return f'<svg class=abs style="left:0;top:0" width=1080 height=1350>{lines}</svg>'

# ---- capa
CAPA = page(G, f'''
{grid_bg(IV, .07)}
<div class=abs style="left:80px;top:96px"><div class=kick style="color:{GOLD}">Imigração · Nacionalidade</div></div>
<div class="abs serif" style="left:60px;top:190px;font-size:330px;line-height:1;font-weight:700;color:{GOLD};letter-spacing:-6px">CCSE</div>
<div class=abs style="left:80px;top:560px;width:920px;height:6px;background:{TERRA}"></div>
<div class="abs serif" style="left:80px;top:610px;width:900px;font-size:84px;line-height:1.08;font-weight:700;color:{IV}">O que você precisa saber antes de se inscrever</div>
<div class=abs style="left:80px;top:1000px;display:flex;gap:16px">
 <span style="padding:14px 28px;border-radius:40px;border:3px solid {GOLD};color:{GOLD};font-size:28px;font-weight:700;letter-spacing:.08em">INSTITUTO CERVANTES</span>
 <span style="padding:14px 28px;border-radius:40px;background:{TERRA};color:{IV};font-size:28px;font-weight:700;letter-spacing:.08em">DESLIZE →</span></div>
{foot(IV)}''')

# ---- miolo: cartão-etiqueta lateral (nº grande à esquerda, texto à direita)
def inner(n, kick, title, body, icon, accent=TERRA, bg=SAND, extra=''):
    return page(bg, f'''
{grid_bg(G, .05)}
<div class=abs style="left:0;top:0;width:300px;height:1350px;background:{G}"></div>
<div class="abs serif" style="left:34px;top:70px;font-size:230px;line-height:1;font-weight:700;color:{GOLD}">{n}</div>
<div class=abs style="left:30px;top:340px;width:240px;height:620px">{icon}</div>
<div class=abs style="left:360px;top:96px;width:640px"><div class=kick style="color:{accent}">{html.escape(kick)}</div></div>
<div class="abs serif" style="left:360px;top:150px;width:660px;font-size:86px;line-height:1.05;font-weight:700;color:{G}">{title}</div>
<div class=abs style="left:360px;top:560px;width:80px;height:8px;background:{accent}"></div>
<div class=abs style="left:360px;top:610px;width:650px;font-size:43px;line-height:1.38;color:{INK}">{body}</div>
{extra}
<div class=foot style="left:360px"><div class=l><img src="{LOGO}"><span class=n style="color:{G}">Espanha Sem Segredo</span></div></div>''')

def ico(s): return f'<svg width=240 height=620 viewBox="0 0 240 620">{s}</svg>'

i2 = ico(f'''<rect x="30" y="40" width="180" height="230" rx="16" fill="{IV}"/><rect x="30" y="40" width="180" height="50" rx="16" fill="{TERRA}"/>
<rect x="30" y="68" width="180" height="22" fill="{TERRA}"/>
<rect x="55" y="120" width="130" height="12" rx="6" fill="{G}" opacity=".5"/><rect x="55" y="150" width="100" height="12" rx="6" fill="{G}" opacity=".5"/><rect x="55" y="180" width="120" height="12" rx="6" fill="{G}" opacity=".5"/>
<circle cx="120" cy="238" r="20" fill="{GOLD}"/>''')
i3 = ico(f'''<circle cx="120" cy="110" r="52" fill="{IV}"/><path d="M30 270C30 190 70 164 120 164C170 164 210 190 210 270Z" fill="{IV}"/>
<rect x="64" y="300" width="112" height="86" rx="10" fill="{GOLD}"/><rect x="82" y="322" width="76" height="9" rx="4" fill="{G}"/><rect x="82" y="342" width="56" height="9" rx="4" fill="{G}"/>''')
i4 = ico(f'''<rect x="40" y="40" width="160" height="210" rx="14" fill="{IV}"/><rect x="62" y="70" width="116" height="10" rx="5" fill="{G}" opacity=".5"/><rect x="62" y="96" width="90" height="10" rx="5" fill="{G}" opacity=".5"/>
<circle cx="120" cy="190" r="34" fill="{GOLD}"/><path d="M104 190L116 203L138 178" fill="none" stroke="{G}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M120 290V380M88 350L120 384L152 350" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="50" y="410" width="140" height="100" rx="14" fill="{TERRA}"/><path d="M60 424L120 468L180 424" fill="none" stroke="{IV}" stroke-width="7" stroke-linejoin="round"/>''')
i6 = ico(f'''<path d="M120 70C95 50 55 44 30 56V240C55 228 95 234 120 254C145 234 185 228 210 240V56C185 44 145 50 120 70Z" fill="{IV}"/>
<path d="M120 70V254" stroke="{G}" stroke-width="5"/>
<rect x="68" y="330" width="104" height="190" rx="18" fill="{GOLD}"/><rect x="82" y="352" width="76" height="120" rx="6" fill="{G}"/><circle cx="120" cy="496" r="9" fill="{G}"/>''')

# ---- slide 5: calendário
def datebox(day, mon, label, hl=False):
    bgc = TERRA if hl else IV; fg = IV if hl else G
    return f'''<div style="display:flex;align-items:center;gap:26px;margin-bottom:26px">
<div style="width:150px;height:150px;border-radius:20px;background:{bgc};color:{fg};display:flex;flex-direction:column;align-items:center;justify-content:center;border:4px solid {G}">
<div class=serif style="font-size:78px;font-weight:700;line-height:1">{day}</div><div style="font-size:26px;font-weight:800;letter-spacing:.14em">{mon}</div></div>
<div style="font-size:38px;line-height:1.25;color:{INK};width:430px;font-weight:600">{label}</div></div>'''
S5 = page(SAND, f'''
{grid_bg(G, .05)}
<div class=abs style="left:0;top:0;width:300px;height:1350px;background:{G}"></div>
<div class="abs serif" style="left:34px;top:70px;font-size:230px;line-height:1;font-weight:700;color:{GOLD}">5</div>
<div class=abs style="left:30px;top:340px;width:240px;height:620px">{ico(f'<rect x="30" y="60" width="180" height="200" rx="16" fill="{IV}"/><rect x="30" y="60" width="180" height="48" rx="16" fill="{TERRA}"/><rect x="30" y="86" width="180" height="22" fill="{TERRA}"/>' + ''.join(f'<circle cx="{66+c*36}" cy="{140+r*36}" r="9" fill="{G}" opacity=".5"/>' for r in range(3) for c in range(4)) + f'<circle cx="138" cy="212" r="14" fill="{GOLD}"/>')}</div>
<div class=abs style="left:360px;top:96px"><div class=kick style="color:{TERRA}">Próximas datas</div></div>
<div class="abs serif" style="left:360px;top:150px;width:660px;font-size:86px;line-height:1.05;font-weight:700;color:{G}">Fique de olho no calendário</div>
<div class=abs style="left:360px;top:470px;width:660px">
{datebox('5','NOV','Último dia de inscrição para a prova de novembro')}
{datebox('23','NOV','Abre a inscrição para as provas de 2027')}
{datebox('26','NOV','Prova oficial do CCSE',True)}</div>
<div class=abs style="left:360px;top:1160px;width:640px;font-size:25px;color:{G2};font-weight:600">Datas de 2026, segundo o Instituto Cervantes.</div>
<div class=foot style="left:360px"><div class=l><img src="{LOGO}"><span class=n style="color:{G}">Espanha Sem Segredo</span></div></div>''')

# ---- fechamento
FIM = page(TERRA, f'''
{grid_bg(IV, .08)}
<div class=abs style="left:360px;top:120px;width:360px;height:360px;border-radius:50%;background:{IV}"></div>
<img class=abs style="left:370px;top:130px;width:340px;height:340px" src="{LOGO}">
<div class="abs serif" style="left:80px;top:560px;width:920px;text-align:center;font-size:82px;line-height:1.1;font-weight:700;color:{IV}">Aqui você fica por dentro de tudo sobre a Espanha</div>
<div class=abs style="left:80px;top:900px;width:920px;text-align:center;font-size:40px;color:{IV};font-weight:600;letter-spacing:.04em">Salve este post e siga @espanhasemsegredo</div>
<div class=abs style="left:120px;top:1100px;width:840px;text-align:center;font-size:25px;line-height:1.5;color:{IV};opacity:.92">Fonte: Instituto Cervantes e Ministerio de Justicia. Consulta em 23/10/2026.<br>Conteúdo informativo, não é assessoria jurídica.</div>''')

SL = [CAPA,
 inner('2', 'O que é', 'A prova do conhecimento da Espanha', 'O CCSE é a prova de conhecimentos <b>constitucionais e socioculturais</b> da Espanha, aplicada pelo <b>Instituto Cervantes</b>.', i2),
 inner('3', 'Quem apresenta', 'Aparece na lista de documentos', 'Na página de nacionalidade do <b>Ministerio de Justicia</b>, o diploma CCSE consta entre os documentos de <b>maiores de idade</b>.', i3, G2),
 inner('4', 'Como comprovar', 'Com o diploma do Cervantes', 'Você comprova com o <b>diploma do Instituto Cervantes</b>. No formulário do pedido, pode <b>autorizar a consulta</b> ao Ministerio de Justicia.', i4),
 S5,
 inner('6', 'Para estudar', 'Material gratuito e oficial', 'O Cervantes oferece o <b>manual de preparação CCSE 2026</b> e o aplicativo gratuito <b>CCSE Nacionalidad Española</b>. Perguntas, tempo e nota: veja no site do Instituto.', i6, G2),
 FIM]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for i, h in enumerate(SL, 1):
            await pg.set_content(h); await pg.wait_for_timeout(250)
            await pg.screenshot(path=f'{OUT}imigracao-{i}.png')
        await b.close()
asyncio.run(main())
