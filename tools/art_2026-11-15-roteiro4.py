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
    <div class=abs style="left:50%;margin-left:-65px;top:{int(h*top)+logo+60+serif_sz*3.5+50}px;width:130px;height:5px;background:{acc}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3.5+90}px;text-align:center;font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
    <div class=abs style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3.5+170}px;text-align:center;font-size:40px;color:{fg}">Siga <b>@espanhasemsegredo</b></div>
    <div class=abs style="left:{pad+20}px;right:{pad+20}px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg};opacity:.85">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>'''
    return page(h,bg,inner)



import math, subprocess
def figura(cx,top,s,col):
    return f'<circle cx="{cx}" cy="{top+14*s}" r="{14*s}" fill="{col}"/><path d="M{cx-18*s} {top+78*s}V{top+46*s}C{cx-18*s} {top+34*s} {cx+18*s} {top+34*s} {cx+18*s} {top+46*s}V{top+78*s}Z" fill="{col}"/>'
import math, subprocess

# ============ ROTEIROS 1 e 2 (2026-11-15): ascendentes + cartão de familiar UE ============
def T(x,y,t,sz=40,col=IV,w=700,fam='Inter',anchor='middle',ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{sz}" letter-spacing="{ls}" fill="{col}">{t}</text>'
def star(cx,cy,r,col):
    pts=[]
    for k in range(10):
        rr=r if k%2==0 else r*.42; an=-math.pi/2+k*math.pi/5
        pts.append(f'{cx+rr*math.cos(an):.1f},{cy+rr*math.sin(an):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{col}"/>'
def arco_path(x,y,w,h): return f'M{x} {y+h}V{y+w/2}A{w/2} {w/2} 0 0 1 {x+w} {y+w/2}V{y+h}Z'

INK2='#24292C'
# ---- ícones carrossel 4 (modificar para trabalhar) ----
def ic_troca(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="64" y="86" width="72" height="62" rx="10" fill="{a}"/><path d="M80 86V66C80 40 120 40 120 66" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round"/><circle cx="100" cy="116" r="9" fill="{b}"/><path d="M14 150H48M34 134L50 150L34 166" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M186 50H152M166 34L150 50L166 66" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_contrato2(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M46 14H128L166 52V186H46Z" fill="{b}" stroke="{a}" stroke-width="9" stroke-linejoin="round"/><path d="M128 14V52H166" fill="none" stroke="{a}" stroke-width="9" stroke-linejoin="round"/><path d="M66 82H146M66 106H146M66 130H110" stroke="{a}" stroke-width="8" stroke-linecap="round"/><path d="M104 168C114 148 124 172 136 156C142 148 150 160 160 152" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'''
def ic_loja(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M20 70L36 22H164L180 70Z" fill="{a}"/><path d="M20 70C20 90 60 90 60 70C60 90 100 90 100 70C100 90 140 90 140 70C140 90 180 90 180 70" fill="{b}" stroke="{a}" stroke-width="7"/><rect x="32" y="92" width="136" height="88" fill="{b}" stroke="{a}" stroke-width="9"/><rect x="82" y="124" width="36" height="56" fill="{a}"/><rect x="46" y="112" width="26" height="26" fill="{a}" opacity=".55"/><rect x="128" y="112" width="26" height="26" fill="{a}" opacity=".55"/></svg>'''
def ic_sede(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="14" y="28" width="172" height="136" rx="14" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M14 62H186" stroke="{a}" stroke-width="8"/><circle cx="36" cy="45" r="5" fill="{a}"/><circle cx="54" cy="45" r="5" fill="{a}"/><rect x="38" y="84" width="84" height="14" rx="7" fill="{a}"/><rect x="38" y="112" width="60" height="14" rx="7" fill="{a}" opacity=".55"/><path d="M122 110L122 168L138 154L150 180L164 174L152 148L174 146Z" fill="{a}" stroke="{b}" stroke-width="5" stroke-linejoin="round"/></svg>'''
def ic_fita(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="78" r="58" fill="{a}"/><circle cx="100" cy="78" r="42" fill="none" stroke="{b}" stroke-width="7"/><path d="M82 78L96 92L120 62" fill="none" stroke="{b}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M62 124L48 188L80 170L100 190L100 134Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M138 124L152 188L120 170L100 190L100 134Z" fill="{a}"/></svg>'''

# ---- carrossel 4: FAIXA DIAGONAL ----
def faixa(kick,title,body,icon_fn,theme,bs=45):
    th={'ivory':(IV,G,IV,INK,G,TERRA,GOLD),'sand':(SAND,TERRA,IV,INK,TERRA,G,G),'green':(G,GOLD,INK,IV,IV,GOLD,GOLD)}[theme]
    bg,band,tcol,bcol,fcol,rule,ring=th
    if theme=='green': ca,cb,disc=G,TERRA,IV
    elif theme=='sand': ca,cb,disc=TERRA,G,IV
    else: ca,cb,disc=IV,GOLD,G
    inner=f'''<svg class=abs style="left:0;top:0" width="1080" height="1350"><path d="M0 0H1080V520L0 700Z" fill="{band}"/>
      <path d="M0 724L1080 544" stroke="{ring}" stroke-width="5" opacity="0"/></svg>
    <div class=abs style="left:80px;top:84px"><div class=kick style="color:{tcol if theme!='green' else INK};opacity:.85">{html.escape(kick)}</div></div>
    <div class="abs serif" style="left:80px;top:170px;width:700px;font-size:78px;line-height:1.06;font-weight:700;color:{tcol}">{title}</div>
    <div class=abs style="left:760px;top:460px;width:250px;height:250px;border-radius:50%;background:{disc};border:8px solid {bg};display:flex;align-items:center;justify-content:center"><div style="width:150px;height:150px">{icon_fn(ca,cb)}</div></div>
    <div class=abs style="left:80px;top:790px;width:920px"><div style="width:120px;height:6px;background:{rule};margin-bottom:26px"></div>
      <div style="font-size:{bs}px;line-height:1.38;color:{bcol}">{body}</div></div>
    {foot(fcol if theme!='green' else IV)}'''
    return page(1350,bg,inner)
def capa4():
    def box(x,c,tit,sub,icon):
        return f'''<rect x="{x}" y="800" width="440" height="330" rx="34" fill="{c[0]}"/>
        <foreignObject x="{x+140}" y="826" width="160" height="160"><div xmlns="http://www.w3.org/1999/xhtml" style="width:160px;height:160px">{icon(c[1],c[2])}</div></foreignObject>
        {T(x+220,1040,tit,40,c[1],800,'Inter')}{T(x+220,1088,sub,32,c[1],500,'Inter')}'''
    svg=f'''<svg class=abs style="left:0;top:0" width="1080" height="1350">
      <rect x="330" y="470" width="420" height="190" rx="30" fill="{IV}"/>
      <g transform="translate(402,498)"><rect x="12" y="52" width="76" height="66" rx="10" fill="{G}"/><path d="M28 52V36C28 8 72 8 72 36V52" fill="none" stroke="{G}" stroke-width="12" stroke-linecap="round"/><circle cx="50" cy="84" r="9" fill="{TERRA}"/></g>
      {T(618,584,'Sem permissão',30,G,800)}{T(618,626,'de trabalho',30,G,800)}
      <path d="M440 676C440 740 300 730 290 790" fill="none" stroke="{IV}" stroke-width="8" stroke-linecap="round" stroke-dasharray="2 18"/>
      <path d="M640 676C640 740 780 730 790 790" fill="none" stroke="{IV}" stroke-width="8" stroke-linecap="round" stroke-dasharray="2 18"/>
      <path d="M274 774L290 800L306 774" fill="none" stroke="{IV}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M774 774L790 800L806 774" fill="none" stroke="{IV}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
      {box(70,(G,IV,GOLD),'Conta alheia','contrato assinado',ic_contrato2)}
      {box(570,(IV,G,TERRA),'Conta própria','projeto empresarial',ic_loja)}
    </svg>'''
    inner=f'''{bracket(IV)}
    <div class=abs style="left:80px;top:76px"><div class=kick style="color:#F3D79A">Imigração · Trabalho</div></div>
    <div class="abs serif" style="left:80px;top:130px;width:920px;font-size:64px;line-height:1.07;font-weight:700;color:{IV}">Autorização que não permite trabalhar: dá para mudar? Precisa de <span style="color:#F3D79A;font-style:italic">oferta de emprego</span>?</div>
    {svg}{foot(IV)}'''
    return page(1350,TERRA,inner)
SL4=[capa4()]
SL4.append(faixa('O que é','O que é a modificação','A modificação troca a sua autorização por outra que permite <b>trabalhar</b>, por conta alheia ou por conta própria. As fichas tratam de quem tem <b>estadia por estudos</b> ou <b>residência sem permissão de trabalho</b>.',ic_troca,'ivory',43))
SL4.append(faixa('Conta alheia','Por conta alheia','A ficha pede <b>contrato de trabalho assinado</b> por empregador e trabalhador. O empregador também precisa comprovar <b>solvência econômica</b>.',ic_contrato2,'sand',48))
SL4.append(faixa('Conta própria','Por conta própria','Não pede contrato, mas <b>projeto empresarial</b>: é preciso demonstrar <b>investimento suficiente</b> e cumprir os requisitos para abrir e exercer a atividade.',ic_loja,'green',48))
SL4.append(faixa('Como pedir','Como pedir','A ficha prevê o <b>pedido telemático</b> pela sede eletrônica; por conta alheia, pode ser feito pela pessoa ou pelo empregador. Recomendamos esta via. Em caso de dúvida, <b>consulte um profissional</b>.',ic_sede,'ivory',43))
SL4.append(faixa('Prazo e validade','Prazo e validade','A ficha prevê <b>três meses</b> para a resolução, por conta alheia e por conta própria. A autorização concedida <b>vale um ano</b>.',ic_fita,'sand',48))
SL4.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: Ministerio de Inclusión (modificações desde estadia por estudos e desde residência sem permissão de trabalho), consulta em 15/11/2026.'))

async def render(lst,folder,prefix,h):
    os.makedirs(folder,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h})
        for i,htm in enumerate(lst):
            await pg.set_content(htm); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{folder}/{prefix}-{i+1}.png')
        await b.close()
R0=os.environ.get('ART_OUT',B+'2026-11-15')
asyncio.run(render(SL4,R0+'/roteiro-4-modificar-para-trabalhar','modificar-trabalho',1350))
