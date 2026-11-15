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
# ---- ícones carrossel 7 (homologação ensino médio) ----
def ic_capelo(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 28L188 70L100 112L12 70Z" fill="{a}"/><path d="M48 96V132C48 150 152 150 152 132V96L100 120Z" fill="{b}" stroke="{a}" stroke-width="7" stroke-linejoin="round"/><path d="M178 76V138" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="178" cy="148" r="11" fill="{b}" stroke="{a}" stroke-width="6"/></svg>'''
def ic_opcoes(a,b):
    bx=lambda x,y,f: f'<rect x="{x}" y="{y}" width="72" height="72" rx="12" fill="{f}" stroke="{a}" stroke-width="8"/>'
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200">{bx(14,14,b)}{bx(114,14,b)}{bx(14,114,b)}{bx(114,114,a)}<path d="M132 150L146 164L170 134" fill="none" stroke="{b}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M32 50H68M132 50H168M32 150H68" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'''
def ic_forms(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="30" y="12" width="140" height="176" rx="14" fill="{b}" stroke="{a}" stroke-width="9"/><circle cx="62" cy="56" r="10" fill="{a}"/><rect x="84" y="48" width="64" height="14" rx="7" fill="{a}"/><circle cx="62" cy="100" r="10" fill="{a}"/><rect x="84" y="92" width="64" height="14" rx="7" fill="{a}"/><circle cx="62" cy="144" r="10" fill="{a}"/><rect x="84" y="136" width="46" height="14" rx="7" fill="{a}"/></svg>'''
def ic_volante(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M14 52H186V84C170 84 170 116 186 116V148H14V116C30 116 30 84 14 84Z" fill="{b}" stroke="{a}" stroke-width="9" stroke-linejoin="round"/><path d="M130 52V148" stroke="{a}" stroke-width="6" stroke-dasharray="3 10"/><path d="M40 84H100M40 116H84" stroke="{a}" stroke-width="8" stroke-linecap="round"/><path d="M146 100L156 112L172 90" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_tela(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="14" y="26" width="172" height="116" rx="14" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M70 176H130M100 142V176" stroke="{a}" stroke-width="9" stroke-linecap="round"/><circle cx="100" cy="84" r="30" fill="{a}"/><path d="M86 84L96 94L116 70" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'''

# ---- carrossel 7: CERTIFICADO (moldura ornamental, tudo centralizado) ----
def cert(kick,title,body,icon_fn,theme,bs=46):
    th={'ivory':(IV,G,GOLD,G,INK,TERRA),'green':(G,IV,GOLD,GOLD,IV,GOLD),'sand':(SAND,G,TERRA,G,INK,TERRA)}[theme]
    bg,tcol,fr,kc,bcol,rule=th
    if theme=='green': ca,cb=GOLD,G
    elif theme=='sand': ca,cb=G,SAND
    else: ca,cb=G,IV
    corners=''
    for (x,y,sx,sy) in [(70,70,1,1),(1010,70,-1,1),(70,1280,1,-1),(1010,1280,-1,-1)]:
        corners+=f'<g transform="translate({x},{y}) scale({sx},{sy})"><path d="M0 0H90M0 0V90" stroke="{fr}" stroke-width="7"/><circle cx="26" cy="26" r="9" fill="{fr}"/></g>'
    svg=f'''<svg class=abs style="left:0;top:0" width="1080" height="1350"><rect x="40" y="40" width="1000" height="1270" rx="6" fill="none" stroke="{fr}" stroke-width="5"/><rect x="58" y="58" width="964" height="1234" rx="4" fill="none" stroke="{fr}" stroke-width="2"/>{corners}
      <path d="M440 585H640" stroke="{rule}" stroke-width="5"/><circle cx="540" cy="585" r="9" fill="{rule}"/></svg>'''
    inner=f'''{svg}
    <div class=abs style="left:0;right:0;top:110px;text-align:center"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div>
    <div class=abs style="left:410px;top:170px;width:260px;height:260px;border-radius:50%;border:6px solid {fr};display:flex;align-items:center;justify-content:center"><div style="width:160px;height:160px">{icon_fn(ca,cb)}</div></div>
    <div class="abs serif" style="left:110px;right:110px;top:440px;text-align:center;font-size:66px;line-height:1.08;font-weight:700;color:{tcol};display:none">{title}</div>
    <div class="abs serif" style="left:110px;right:110px;top:300px;text-align:center;font-size:1px;color:transparent">.</div>
    <div class="abs serif" style="left:110px;right:110px;top:530px;text-align:center;font-size:0"></div>
    <div class="abs serif" style="left:110px;right:110px;top:450px;text-align:center;font-size:68px;line-height:1.06;font-weight:700;color:{tcol}">{title}</div>
    <div class=abs style="left:130px;right:130px;top:640px;text-align:center;font-size:{bs}px;line-height:1.4;color:{bcol}">{body}</div>
    <div class=foot style="justify-content:center;left:80px;right:80px"><div class=l><img src="{LOGO}"><span class=n style="color:{tcol}">Espanha Sem Segredo</span></div></div>'''
    return page(1350,bg,inner)
def capa7():
    scroll=f'''<g transform="rotate(-3 540 840)">
      <rect x="150" y="650" width="780" height="420" rx="14" fill="{IV}" stroke="{GOLD}" stroke-width="5"/>
      <rect x="168" y="668" width="744" height="384" rx="8" fill="none" stroke="{GOLD}" stroke-width="2"/>
      <rect x="120" y="640" width="60" height="440" rx="30" fill="{SAND}" stroke="{GOLD}" stroke-width="4"/><rect x="900" y="640" width="60" height="440" rx="30" fill="{SAND}" stroke="{GOLD}" stroke-width="4"/>
      <path d="M300 730H780" stroke="{G}" stroke-width="10" stroke-linecap="round"/>
      <path d="M360 790H720M330 840H750M360 890H640" stroke="{G2}" stroke-width="7" stroke-linecap="round" opacity=".6"/>
      <path d="M330 980C360 950 380 1000 410 970C440 940 460 1000 500 962" fill="none" stroke="{G}" stroke-width="6" stroke-linecap="round"/>
      <g transform="translate(740,940)"><path d="M-26 20L-44 86L-8 70L0 96L8 70L44 86L26 20Z" fill="{TERRA}"/><circle r="52" fill="{TERRA}" stroke="{GOLD}" stroke-width="6"/>{star(0,0,26,GOLD)}</g>
    </g>'''
    cap=f'''<g transform="translate(540,520)"><path d="M0 -70L170 0L0 70L-170 0Z" fill="{G}"/><path d="M-100 34V104C-100 140 100 140 100 104V34L0 78Z" fill="{G2}" stroke="{G}" stroke-width="6"/><path d="M150 12V112" stroke="{TERRA}" stroke-width="7" stroke-linecap="round"/><circle cx="150" cy="124" r="14" fill="{TERRA}"/></g>'''
    return page(1350,SAND,f'''{bracket(TERRA)}
    <div class=abs style="left:80px;top:80px"><div class=kick style="color:{TERRA}">Imigração · Estudos</div></div>
    <div class="abs serif" style="left:80px;top:140px;width:900px;font-size:72px;line-height:1.06;font-weight:700;color:{G}">Estudou o <span style="color:{TERRA};font-style:italic">ensino médio</span> fora da Espanha? Veja como pedir a homologação.</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">{cap}{scroll}</svg>{foot(G)}''')
SL7=[capa7()]
SL7.append(cert('O que se pede','O que se pede','No formulário, a pessoa escolhe <b>uma opção</b>: título de <b>Graduado em ESO</b>; <b>ESO e Bachillerato</b>; convalidação de estudos equivalentes ao <b>1º de Bachillerato</b>; ou título de <b>Bachiller</b>.',ic_opcoes,'ivory',48))
SL7.append(cert('Dados do pedido','Dados do pedido','O formulário pede o <b>país do sistema educativo</b> (o último, se forem vários), a identificação, o endereço e o e-mail.',ic_forms,'green',54))
SL7.append(cert('Volante condicional','Volante condicional','O formulário prevê um <b>volante de inscrição condicional</b>, opcional, entregue no <b>centro de ensino</b>.',ic_volante,'sand',56))
SL7.append(cert('Como pedir','Como pedir','O pedido é feito pela <b>sede eletrônica</b> do Ministerio de Educación. Recomendamos esta via. Em caso de dúvida, <b>consulte um profissional</b>.',ic_tela,'ivory',52))
SL7.append(closing(1350,G2,IV,GOLD,'Fonte: Ministerio de Educación, FP y Deportes (formulário de homologação ESO e Bachillerato), consulta em 15/11/2026.'))

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
asyncio.run(render(SL7,R0+'/roteiro-7-homologacao-ensino-medio','homologacao-ensino-medio',1350))
