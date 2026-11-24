import base64, asyncio, os, html, sys
from playwright.async_api import async_playwright
B=os.path.dirname(os.path.abspath(__file__))+'/../'
OUT=os.environ.get('ART_OUT',B+'saida/')+'/'; os.makedirs(OUT,exist_ok=True)
LOGO='data:image/png;base64,'+base64.b64encode(open(B+'marca/logo-espanha-sem-segredo.png','rb').read()).decode()
G='#0F3D3A'; G2='#1E5550'; GOLD='#C9A24A'; TERRA='#B8573A'; IV='#F5F1E8'; INK='#24292C'; SAND='#E9DFC9'

CSS=f'''
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;overflow:hidden;font-family:Inter,Arial,sans-serif;position:relative}}
.serif{{font-family:Lora,Georgia,serif}}
.abs{{position:absolute}}
.foot{{position:absolute;left:80px;right:80px;bottom:56px;display:flex;align-items:center;justify-content:space-between}}
.foot .l{{display:flex;align-items:center;gap:18px}}
.foot img{{width:68px;height:68px}}
.foot .n{{font-family:Lora,serif;font-style:italic;font-size:30px;letter-spacing:.12em}}
.foot .c{{font-size:26px;letter-spacing:.16em;font-weight:600}}
.kick{{font-size:28px;letter-spacing:.2em;font-weight:700;text-transform:uppercase}}
'''

def bracket(col):
    return f'<svg class=abs style="right:56px;top:56px" width="230" height="230" viewBox="0 0 230 230"><path d="M0 2H228V230" fill="none" stroke="{col}" stroke-width="3"/></svg>'

def arches(col, w=1080, n=9, op=1):
    aw=w/n; s=''
    for i in range(n):
        x=i*aw
        s+=f'<path d="M{x+aw*.12:.1f} 150 V70 C{x+aw*.12:.1f} 25 {x+aw*.88:.1f} 25 {x+aw*.88:.1f} 70 V150 Z" fill="none" stroke="{col}" stroke-width="3"/>'
    return f'<svg class=abs style="left:0;bottom:146px;opacity:{op}" width="{w}" height="96" viewBox="0 0 {w} 150" preserveAspectRatio="none">{s}</svg>'

def foot(col, n=None, tot=None):
    c=f'<span class=c style="color:{col}">{n} / {tot}</span>' if n else ''
    return f'<div class=foot><div class=l><img src="{LOGO}"><span class=n style="color:{col}">Espanha Sem Segredo</span></div>{c}</div>'

def page(h,bg,inner):
    return f'<html><head><meta charset=utf8><style>{CSS} body{{height:{h}px;background:{bg}}}</style></head><body>{inner}</body></html>'

def badge(inner,col_bg,col_fg,size=300,rot=0):
    return f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{col_bg};color:{col_fg};display:flex;align-items:center;justify-content:center;transform:rotate({rot}deg)"><div style="width:{int(size*.62)}px;height:{int(size*.62)}px">{inner}</div></div>'

# ---------- content slide, shared by 2 carousels ----------
def content(n,tot,kick,title,body,icon_fn,theme,numtxt=None):
    th={'ivory':(IV,G,INK,G2,GOLD,TERRA),'green':(G,IV,IV,GOLD,GOLD,GOLD),'terra':(TERRA,IV,IV,IV,'#E8C77A','#F5F1E8')}[theme]
    bg,hc,bc,kc,accent,ibg=th
    # icon colours
    if theme=='ivory': ia,ib,badge_bg=IV,G,G
    elif theme=='green': ia,ib,badge_bg=G,GOLD,GOLD
    else: ia,ib,badge_bg=TERRA,IV,IV
    if theme=='ivory': ia,ib=IV,GOLD
    ico=badge(icon_fn(ia,ib),badge_bg,ia,260)
    big=f'<div class=abs serif style="right:40px;top:120px;font-size:460px;font-weight:700;line-height:1;color:{accent};opacity:.12;letter-spacing:-.04em">{n:02d}</div>'
    arc=arches(accent,op=.35)
    fc=hc
    inner=f'''{big}{bracket(accent)}
    <div class=abs style="left:80px;top:96px"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div>
    <div class=abs style="left:80px;top:190px">{ico}</div>
    <div class=abs style="left:80px;top:500px;width:920px">
      <div class=serif style="font-size:76px;line-height:1.08;font-weight:700;color:{hc}">{title}</div>
      <div style="width:130px;height:5px;background:{accent};margin:34px 0 36px"></div>
      <div style="font-size:42px;line-height:1.42;color:{bc};font-weight:400">{body}</div></div>
    {arc}{foot(fc,n,tot)}'''
    return page(1350,bg,inner)

def closing(h,bg,fg,acc,srcs,logo=360,serif_sz=70,pad=80,top=.12):
    inner=f'''{bracket(acc)}
    <div class=abs style="left:0;right:0;top:{int(h*top)}px;display:flex;justify-content:center"><img src="{LOGO}" width="{logo}" height="{logo}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60}px;text-align:center;font-size:{serif_sz}px;line-height:1.14;font-weight:700;color:{fg}">Aqui você fica por dentro de tudo sobre a Espanha</div>
    <div class=abs style="left:50%;margin-left:-65px;top:{int(h*top)+logo+60+int(serif_sz*3.5)+40}px;width:130px;height:5px;background:{acc}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+int(serif_sz*3.5)+80}px;text-align:center;font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
    <div class=abs style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+int(serif_sz*3.5)+160}px;text-align:center;font-size:40px;color:{fg}">Siga <b>@espanhasemsegredo</b></div>
    <div class=abs style="left:{pad+20}px;right:{pad+20}px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg};opacity:.85">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>'''
    return page(h,bg,inner)


# =================== 24/11/2026 ===================
# ---- ícones novos: Hoja 63 ----
def ic_permcard(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="14" y="48" width="172" height="110" rx="14" fill="{a}"/><circle cx="62" cy="92" r="20" fill="{b}"/><path d="M30 142C30 120 44 112 62 112C80 112 94 120 94 142Z" fill="{b}"/><path d="M112 82H168M112 104H168" stroke="{b}" stroke-width="7" stroke-linecap="round"/><path d="M120 134C120 122 134 122 142 134C150 146 164 146 164 134C164 122 150 122 142 134C134 146 120 146 120 134Z" fill="none" stroke="{b}" stroke-width="6"/></svg>'''
def ic_family(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="66" cy="54" r="22" fill="{a}"/><circle cx="134" cy="54" r="22" fill="{a}"/><path d="M26 130C26 98 44 86 66 86C88 86 106 98 106 130Z" fill="{a}"/><path d="M94 130C94 98 112 86 134 86C156 86 174 98 174 130Z" fill="{a}" opacity=".8"/><circle cx="100" cy="120" r="16" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M80 182C80 160 88 148 100 148C112 148 120 160 120 182Z" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M66 78V150M134 78V150" stroke="{b}" stroke-width="0"/></svg>'''
def ic_cal5(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="24" y="34" width="152" height="140" rx="14" fill="{b}" stroke="{a}" stroke-width="7"/><rect x="24" y="34" width="152" height="40" rx="14" fill="{a}"/><path d="M62 18V46M138 18V46" stroke="{a}" stroke-width="9" stroke-linecap="round"/><text x="100" y="146" text-anchor="middle" font-family="Lora" font-weight="700" font-size="76" fill="{a}">5</text><text x="100" y="168" text-anchor="middle" font-family="Inter" font-weight="700" font-size="18" letter-spacing="3" fill="{a}">ANOS</text></svg>'''
def ic_ex19(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M46 18H120L158 56V182H46Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M120 18V56H158" fill="none" stroke="{a}" stroke-width="6"/><text x="102" y="102" text-anchor="middle" font-family="Inter" font-weight="800" font-size="34" fill="{a}">EX-19</text><path d="M66 124H138M66 142H138M66 160H110" stroke="{a}" stroke-width="6" stroke-linecap="round"/><circle cx="150" cy="150" r="24" fill="none" stroke="{a}" stroke-width="5"/><path d="M138 150L147 159L163 141" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_counter(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="20" y="118" width="160" height="62" rx="8" fill="{a}"/><rect x="34" y="40" width="132" height="64" rx="10" fill="{b}" stroke="{a}" stroke-width="6"/><circle cx="100" cy="72" r="18" fill="{a}"/><path d="M100 72V60M100 72L110 78" stroke="{b}" stroke-width="5" stroke-linecap="round"/><path d="M40 138H160" stroke="{b}" stroke-width="5"/><rect x="82" y="146" width="36" height="12" rx="3" fill="{b}"/></svg>'''
def ic_tenyears(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="76" fill="none" stroke="{a}" stroke-width="10"/><path d="M100 24A76 76 0 0 1 176 100" fill="none" stroke="{b}" stroke-width="10"/><path d="M168 74L180 102L152 98Z" fill="{b}"/><text x="100" y="116" text-anchor="middle" font-family="Lora" font-weight="700" font-size="58" fill="{a}">10</text><text x="100" y="140" text-anchor="middle" font-family="Inter" font-weight="700" font-size="17" letter-spacing="3" fill="{a}">ANOS</text></svg>'''

def imig_cover():
    stars=''.join(f'<circle cx="{300+210*__import__("math").cos(i*3.14159/6):.1f}" cy="{300+210*__import__("math").sin(i*3.14159/6):.1f}" r="15" fill="{GOLD}"/>' for i in range(12))
    card=f'''<svg width="760" height="600" viewBox="0 0 760 600"><g transform="rotate(-7 380 300)"><rect x="40" y="70" width="680" height="440" rx="34" fill="{TERRA}" stroke="{GOLD}" stroke-width="6"/><rect x="70" y="100" width="620" height="380" rx="20" fill="none" stroke="{IV}" stroke-width="2" opacity=".5"/>
    <circle cx="190" cy="250" r="64" fill="{IV}"/><path d="M92 420C92 340 140 318 190 318C240 318 288 340 288 420Z" fill="{IV}"/>
    <path d="M340 190H650M340 240H650M340 290H560" stroke="{IV}" stroke-width="14" stroke-linecap="round" opacity=".9"/>
    <path d="M400 392C400 356 446 356 478 392C510 428 556 428 556 392C556 356 510 356 478 392C446 428 400 428 400 392Z" fill="none" stroke="{GOLD}" stroke-width="14" stroke-linejoin="round"/>
    <text x="600" y="420" font-family="Lora" font-weight="700" font-size="64" fill="{GOLD}">10</text></g></svg>'''
    ring=f'<svg class=abs style="left:560px;top:690px;opacity:.28" width="600" height="600" viewBox="0 0 600 600">{stars}</svg>'
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:{G}"></div>
    <div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 20% 90%,{G2} 0,{G} 62%)"></div>
    {ring}{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Família de cidadão da UE</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:100px;line-height:1.04;font-weight:700;color:{IV}">Cartão de residência <span style="color:{GOLD};font-style:italic">permanente</span> de familiar de cidadão da UE</div>
    <div class=abs style="left:130px;top:640px">{card}</div>
    <div class=abs style="left:80px;top:1190px;font-size:30px;font-weight:600;letter-spacing:.14em;color:{GOLD}">DESLIZE  →</div>
    {foot(GOLD)}'''
    return page(1350,G,inner)

IMG=[imig_cover()]
T=7
IMG.append(content(2,T,'Imigração · Quem pode','Quem pode pedir','Familiar de cidadão espanhol ou da UE, do EEE ou da Suíça, <b>sem essa nacionalidade</b>: cônjuge, pareja registrada, descendentes e ascendentes, nas condições da ficha oficial.',ic_family,'ivory'))
IMG.append(content(3,T,'Imigração · Requisito','Cinco anos','Em regra, <b>cinco anos</b> de residência legal e contínua na Espanha, mantido o vínculo familiar. Há situações específicas, como viuvez ou divórcio, com condições próprias.',ic_cal5,'terra'))
IMG.append(content(4,T,'Imigração · Formulário','Formulário e documentos','Formulário <b>EX-19</b> (EX-24 se não houve livre circulação), passaporte válido, foto e documentos do vínculo familiar. Traduções por tradutor juramentado.',ic_ex19,'green'))
IMG.append(content(5,T,'Imigração · Onde pedir','Onde apresentar','Na <b>Oficina de Extranjería</b> da província ou na Comisaría, ou pela via telemática da sede eletrônica. O pedido é pessoal ou por representação.',ic_counter,'ivory'))
IMG.append(content(6,T,'Imigração · Cartão','Validade do cartão','A ficha oficial indica validade de <b>dez anos</b>, com renovação automática, e prevê a expedição do cartão em até <b>três meses</b> após o pedido.',ic_tenyears,'terra'))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 63 (atualizada em maio de 2025).<br>Consulta em 24/11/2026.'))

# ---- NOTÍCIA: Canárias / Comissão Interministerial ----
def ic_roundtable(a,b):
    ch=''.join(f'<circle cx="{100+78*__import__("math").cos(i*6.2832/7):.1f}" cy="{100+78*__import__("math").sin(i*6.2832/7):.1f}" r="14" fill="{a}"/>' for i in range(7))
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200">{ch}<circle cx="100" cy="100" r="52" fill="{a}"/><circle cx="100" cy="100" r="36" fill="none" stroke="{b}" stroke-width="4"/><path d="M100 78V122M78 100H122" stroke="{b}" stroke-width="4" stroke-linecap="round" opacity=".0"/></svg>'
def ic_islands(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M24 78C34 64 52 66 58 78C62 90 44 98 30 94C22 90 20 84 24 78Z" fill="{a}"/><path d="M70 96C82 84 100 90 100 102C98 114 78 116 70 108Z" fill="{a}"/><path d="M112 66C130 54 160 62 164 82C166 100 136 110 118 98C108 90 106 74 112 66Z" fill="{a}"/><path d="M40 138C70 122 100 154 130 138C150 128 164 134 176 140" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M26 164C56 148 86 180 116 164C140 152 160 160 176 166" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" opacity=".7"/></svg>'''
def ic_boat(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M22 112H178L152 154H48Z" fill="{a}"/><path d="M100 112V40L146 112Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M100 112V30" stroke="{a}" stroke-width="6"/><path d="M14 170C44 154 70 184 100 168C130 152 156 182 186 166" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'''
def ic_hourglass(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M50 24H150M50 176H150" stroke="{a}" stroke-width="12" stroke-linecap="round"/><path d="M60 24C60 80 100 90 100 100C100 110 60 120 60 176H140C140 120 100 110 100 100C100 90 140 80 140 24Z" fill="{b}" stroke="{a}" stroke-width="7" stroke-linejoin="round"/><path d="M76 160C86 140 114 140 124 160Z" fill="{a}"/><path d="M100 100V138" stroke="{a}" stroke-width="5"/></svg>'''

def noticia_cover():
    waves=''.join(f'<path d="M-20 {y}C120 {y-40} 240 {y+40} 380 {y}S640 {y-40} 780 {y}S1040 {y+40} 1100 {y}" fill="none" stroke="{col}" stroke-width="4" opacity="{op}"/>' for y,col,op in [(1010,G2,.5),(1070,G2,.4),(1130,G2,.3)])
    isl=f'''<g fill="{G}"><path d="M120 560C140 520 200 520 214 560C224 590 170 616 140 606C118 598 112 580 120 560Z"/><path d="M262 600C290 570 340 580 346 612C350 640 296 656 270 642C256 634 254 616 262 600Z"/><path d="M430 520C470 480 560 500 574 560C584 610 500 650 450 626C420 610 416 560 430 520Z"/><path d="M634 590C664 566 712 580 716 612C718 640 664 654 640 640C626 630 624 606 634 590Z"/><path d="M770 540C796 512 850 524 858 560C864 590 810 612 780 598C762 588 760 560 770 540Z"/></g>'''
    table=f'''<svg class=abs style="left:300px;top:790px" width="480" height="330" viewBox="0 0 480 330"><ellipse cx="240" cy="190" rx="200" ry="92" fill="{TERRA}" stroke="{G}" stroke-width="5"/><ellipse cx="240" cy="178" rx="200" ry="92" fill="{GOLD}" stroke="{G}" stroke-width="5"/><ellipse cx="240" cy="178" rx="150" ry="62" fill="none" stroke="{G}" stroke-width="3" opacity=".6"/>{''.join(f'<circle cx="{240+232*__import__("math").cos(i*6.2832/7):.0f}" cy="{178+118*__import__("math").sin(i*6.2832/7):.0f}" r="20" fill="{G}"/>' for i in range(7))}</svg>'''
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{IV} 0%,{SAND} 100%)"></div>
    <div class=abs style="left:700px;top:120px;width:260px;height:260px;border-radius:50%;background:{GOLD};opacity:.55"></div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350"><g transform="translate(0,150)">{isl}</g>{waves}</svg>
    {table}{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:820px;font-size:92px;line-height:1.05;font-weight:700;color:{G}">Governo e <span style="color:{TERRA};font-style:italic">Canárias</span> se reúnem hoje</div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,IV,inner)
NOT=[noticia_cover()]
T=6
NOT.append(content(2,T,'Notícia · A reunião','Hoje, na Moncloa','Segundo a agenda da EFE, a <b>Comissão Interministerial de Imigração</b> reúne-se na manhã de 24/11, em Madri, com o presidente de Canarias, Fernando Clavijo.',ic_roundtable,'green'))
NOT.append(content(3,T,'Notícia · A pauta','O que será analisado','A EFE informa que o encontro serve para <b>analisar a situação nas ilhas</b>, em meio à crise migratória nas Canárias.',ic_islands,'ivory'))
NOT.append(content(4,T,'Notícia · Os números','Chegadas em novembro','Segundo a EFE, só em novembro chegaram às Canárias cerca de <b>130 cayucos</b>, com quase <b>13.000 pessoas</b>. Dado da agência, de 23/11.',ic_boat,'terra'))
NOT.append(content(5,T,'Notícia · O que falta','Resultado ainda não divulgado','Até a preparação deste conteúdo, <b>não havia comunicado oficial</b> sobre as decisões da reunião. Qualquer medida depende de anúncio do Governo.',ic_hourglass,'ivory'))
NOT.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: EFE, temas do dia (23/11/2026); Palácio da Moncloa.<br>Consulta em 24/11/2026.'))

# ---- REEL cultura: Mérida ----
def reel_page(bg,acc,fg,inner,n):
    return page(1920,bg,f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:{bg}"></div>
    <div class=abs style="left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(135deg,{acc}14 0 2px,transparent 2px 42px)"></div>
    {bracket(acc)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{acc}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{fg}">Espanha Sem Segredo</span></div><span class=c style="color:{acc}">{n} / 5</span></div>''')
def aqueduct(col,acc,x,y,w):
    s=''
    for i in range(7):
        px=i*(w/7)
        s+=f'<path d="M{px+8:.0f} 400V300C{px+8:.0f} 240 {px+w/7-8:.0f} 240 {px+w/7-8:.0f} 300V400Z" fill="{col}"/>'
    for i in range(7):
        px=i*(w/7)
        s+=f'<path d="M{px+22:.0f} 240V170C{px+22:.0f} 120 {px+w/7-22:.0f} 120 {px+w/7-22:.0f} 170V240Z" fill="{acc}" opacity=".9"/>'
    return f'<svg class=abs style="left:{x}px;top:{y}px" width="{w}" height="420" viewBox="0 0 {w} 420"><rect x="0" y="236" width="{w}" height="14" fill="{col}"/><rect x="0" y="110" width="{w}" height="12" fill="{acc}"/>{s}<rect x="0" y="400" width="{w}" height="14" fill="{col}"/></svg>'
def theatre(col,acc,x,y):
    rows=''.join(f'<path d="M{80+i*34} {330-i*0}A{340-i*34} {250-i*28} 0 0 1 {800-i*34-80+80} 330" fill="none" stroke="{col}" stroke-width="12" opacity="{1-i*.08:.2f}"/>' for i in range(0))
    arcs=''.join(f'<path d="M{40+i*38} 330A{360-i*38} {300-i*32} 0 0 1 {760-i*38} 330" fill="none" stroke="{col}" stroke-width="13"/>' for i in range(7))
    cols=''.join(f'<rect x="{150+i*100}" y="352" width="30" height="130" fill="{acc}"/><rect x="{140+i*100}" y="342" width="50" height="14" fill="{acc}"/>' for i in range(6))
    return f'<svg class=abs style="left:{x}px;top:{y}px" width="800" height="520" viewBox="0 0 800 520">{arcs}<rect x="40" y="340" width="720" height="10" fill="{col}"/>{cols}<rect x="100" y="482" width="600" height="14" fill="{acc}"/></svg>'
def bridge(col,acc,x,y):
    ar=''.join(f'<path d="M{20+i*84} 260V220C{20+i*84} 168 {88+i*84} 168 {88+i*84} 220V260Z" fill="{col}"/>' for i in range(11))
    wv=''.join(f'<path d="M-10 {y2}C80 {y2-16} 160 {y2+16} 250 {y2}S420 {y2-16} 510 {y2}S680 {y2+16} 770 {y2}S940 {y2-16} 1030 {y2}" fill="none" stroke="{acc}" stroke-width="5" opacity=".7"/>' for y2 in (300,340))
    return f'<svg class=abs style="left:{x}px;top:{y}px" width="1000" height="380" viewBox="0 0 1000 380"><rect x="0" y="140" width="960" height="26" fill="{col}"/><rect x="0" y="160" width="960" height="100" fill="{col}" opacity=".0"/>{ar}<rect x="0" y="252" width="960" height="10" fill="{col}"/>{wv}</svg>'
def ruin(col,acc,x,y):
    return f'''<svg class=abs style="left:{x}px;top:{y}px" width="700" height="760" viewBox="0 0 700 760"><circle cx="520" cy="130" r="90" fill="{acc}" opacity=".9"/><path d="M60 700V300C60 140 340 140 340 300V700" fill="none" stroke="{col}" stroke-width="30"/><path d="M110 700V310C110 200 290 200 290 310V700" fill="none" stroke="{col}" stroke-width="12" opacity=".6"/><rect x="380" y="330" width="52" height="370" fill="{col}"/><rect x="368" y="314" width="76" height="22" fill="{col}"/><rect x="368" y="696" width="76" height="22" fill="{col}"/><rect x="520" y="440" width="52" height="260" fill="{col}"/><rect x="508" y="424" width="76" height="22" fill="{col}"/><path d="M20 718H680" stroke="{col}" stroke-width="12"/></svg>'''
RR=[]
RR.append(reel_page(G,GOLD,IV,f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:104px;line-height:1.06;font-weight:700;color:{IV}">Uma cidade <span style="color:{GOLD};font-style:italic">romana</span> ainda de pé na Extremadura</div>{ruin(IV,GOLD,190,780)}
<div class=abs style="left:80px;top:1600px;width:920px;font-size:44px;line-height:1.4;color:{IV}">Você conhece Mérida?</div>''',1))
RR.append(reel_page(IV,TERRA,G,f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:100px;line-height:1.06;font-weight:700;color:{G}">Emerita <span style="color:{TERRA};font-style:italic">Augusta</span></div>
<div class=abs style="left:80px;top:540px;width:920px;font-size:50px;line-height:1.42;color:{INK}">O nome romano de Mérida. A cidade foi fundada em <b>25 a.C.</b>, no tempo do imperador Augusto.</div>{aqueduct(G,TERRA,40,1040,1000)}''',2))
RR.append(reel_page(TERRA,IV,IV,f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:100px;line-height:1.06;font-weight:700;color:{IV}">Teatro, <span style="color:#F3D79A;font-style:italic">circo</span> e ponte</div>
<div class=abs style="left:80px;top:540px;width:920px;font-size:50px;line-height:1.42;color:{IV}">O conjunto arqueológico reúne monumentos romanos, como o <b>teatro</b>, o <b>anfiteatro</b>, o <b>circo</b> e a <b>ponte</b> sobre o rio Guadiana.</div>{theatre(IV,'#F3D79A',140,1090)}''',3))
RR.append(reel_page(G,GOLD,IV,f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:100px;line-height:1.06;font-weight:700;color:{IV}">Patrimônio <span style="color:{GOLD};font-style:italic">Mundial</span></div>
<div class=abs style="left:80px;top:540px;width:920px;font-size:50px;line-height:1.42;color:{IV}">Em <b>1993</b>, a UNESCO inscreveu o Conjunto Arqueológico de Mérida na lista do Patrimônio Mundial.</div>{bridge(IV,GOLD,40,1100)}''',4))
RR.append(closing(1920,TERRA,IV,'#F3D79A','Fontes: UNESCO (lista do Patrimônio Mundial, nº 664).<br>Consulta em 24/11/2026.',logo=460,serif_sz=88,top=.2))

async def main(only=None):
    sets={'noticia':NOT,'cultura':RR,'imigracao':IMG}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,lst in sets.items():
            if only and k not in only: continue
            h=1920 if k=='cultura' else 1350
            pg=await b.new_page(viewport={'width':1080,'height':h})
            for i,htm in enumerate(lst):
                await pg.set_content(htm); await pg.wait_for_timeout(500)
                await pg.screenshot(path=OUT+f'{k}-{i+1}.png')
        await b.close()
asyncio.run(main(sys.argv[1:] or None))
