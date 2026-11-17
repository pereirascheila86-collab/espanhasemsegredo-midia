import base64, asyncio, os, html, sys, subprocess
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
# ================= 2026-11-12 : ícones e cenas novos =================
def content2(kick,title,body,icon_fn,theme,bs=48):
    th={'ivory':(IV,G,INK,G2,GOLD),'green':(G,IV,IV,GOLD,GOLD),'terra':(TERRA,IV,IV,'#F3D79A','#F3D79A')}[theme]
    bg,hc,bc,kc,accent=th
    if theme=='ivory': ia,ib,badge_bg=IV,GOLD,G
    elif theme=='green': ia,ib,badge_bg=G,GOLD,GOLD
    else: ia,ib,badge_bg=TERRA,IV,IV
    ico=badge(icon_fn(ia,ib),badge_bg,ia,250)
    inner=f'''{bracket(accent)}
    <div class=abs style="left:80px;top:96px"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div>
    <div class=abs style="left:80px;top:170px">{ico}</div>
    <div class=abs style="left:80px;top:450px;width:920px">
      <div class=serif style="font-size:72px;line-height:1.08;font-weight:700;color:{hc}">{title}</div>
      <div style="width:130px;height:5px;background:{accent};margin:28px 0 30px"></div>
      <div style="font-size:{bs}px;line-height:1.38;color:{bc};font-weight:400">{body}</div></div>
    {arches(accent,op=.35)}{foot(hc)}'''
    return page(1350,bg,inner)

# ---------- CULTURA (Reel 1080x1920): Alhambra ----------
def rbv(inner,n,theme='green'):
    if theme=='ivory': bg,fg,acc,k=IV,G,TERRA,TERRA
    elif theme=='terra': bg,fg,acc,k=TERRA,IV,'#F3D79A','#F3D79A'
    else: bg,fg,acc,k=G,IV,GOLD,GOLD
    return page(1920,bg,f'''{bracket(acc)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{k}">Você sabia? | Espanha</span></div>
    {inner.replace('@FG',fg).replace('@AC',acc)}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{acc}">Espanha Sem Segredo</span></div><span class=c style="color:{acc}">{n} / 5</span></div>''')
def Tv(t,sz=84): return f'<div class="abs serif" style="left:80px;top:220px;width:920px;font-size:{sz}px;line-height:1.06;font-weight:700;color:@FG">{t}</div>'
def Pv(t,top=500): return f'<div class=abs style="left:80px;top:{top}px;width:920px;font-size:44px;line-height:1.4;color:@FG;opacity:.95">{t}</div>'
def cardv(x,y,w,h,bg,svg,dy=0): return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;background:{bg}"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><g transform="translate(0,{dy})">{svg}</g></svg></div>'

# ================= 2026-11-13 : ícones e cenas novos =================
import random
def mosaico(x0,y0,w,h,cols,seed=1,cell=46):
    rnd=random.Random(seed); s=''
    for gx in range(int(w//cell)+1):
        for gy in range(int(h//cell)+1):
            px=x0+gx*cell+rnd.uniform(-5,5); py=y0+gy*cell+rnd.uniform(-5,5)
            pts=[(px,py),(px+cell*rnd.uniform(.8,1.1),py+rnd.uniform(-6,6)),(px+cell*rnd.uniform(.8,1.1),py+cell*rnd.uniform(.8,1.1)),(px+rnd.uniform(-6,6),py+cell*rnd.uniform(.8,1.1))]
            s+=f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" fill="{rnd.choice(cols)}" stroke="{G}" stroke-width="2"/>'
    return s


# ================= 2026-11-14 : ícones e cenas novos =================
def content2(kick,title,body,icon_fn,theme,bs=50):
    th={'ivory':(IV,G,INK,G2,GOLD),'green':(G,IV,IV,GOLD,GOLD),'terra':(TERRA,IV,IV,'#F3D79A','#F3D79A')}[theme]
    bg,hc,bc,kc,accent=th
    if theme=='ivory': ia,ib,badge_bg=IV,GOLD,G
    elif theme=='green': ia,ib,badge_bg=G,GOLD,GOLD
    else: ia,ib,badge_bg=TERRA,IV,IV
    ico=badge(icon_fn(ia,ib),badge_bg,ia,250)
    inner=f'''{bracket(accent)}
    <div class=abs style="left:80px;top:96px"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div>
    <div class=abs style="left:80px;top:170px">{ico}</div>
    <div class=abs style="left:80px;top:450px;width:920px">
      <div class=serif style="font-size:72px;line-height:1.08;font-weight:700;color:{hc}">{title}</div>
      <div style="width:130px;height:5px;background:{accent};margin:28px 0 30px"></div>
      <div style="font-size:{bs}px;line-height:1.38;color:{bc};font-weight:400">{body}</div></div>
    {arches(accent,op=.35)}{foot(hc)}'''
    return page(1350,bg,inner)

def rbv(inner,n,theme='green'):
    if theme=='ivory': bg,fg,acc,k=IV,G,TERRA,TERRA
    elif theme=='terra': bg,fg,acc,k=TERRA,IV,'#F3D79A','#F3D79A'
    else: bg,fg,acc,k=G,IV,GOLD,GOLD
    return page(1920,bg,f'''{bracket(acc)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{k}">Você sabia? | Espanha</span></div>
    {inner.replace('@FG',fg).replace('@AC',acc)}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{acc}">Espanha Sem Segredo</span></div><span class=c style="color:{acc}">{n} / 5</span></div>''')
def Tv(t,sz=84): return f'<div class="abs serif" style="left:80px;top:220px;width:920px;font-size:{sz}px;line-height:1.06;font-weight:700;color:@FG">{t}</div>'
def Pv(t,top=500): return f'<div class=abs style="left:80px;top:{top}px;width:920px;font-size:44px;line-height:1.4;color:@FG;opacity:.95">{t}</div>'
def cardv(x,y,w,h,bg,svg,dy=0): return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;background:{bg}"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><g transform="translate(0,{dy})">{svg}</g></svg></div>'

# ================= 2026-11-16 : ícones e cenas novos =================
def T(x,y,t,sz=40,col=IV,w=700,fam='Inter',anchor='middle',ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{sz}" letter-spacing="{ls}" fill="{col}">{t}</text>'
def SV(inner): return f'<svg width="100%" height="100%" viewBox="0 0 200 200">{inner}</svg>'


# ---------- NOTÍCIA: ucranianos na Espanha (dados Inclusión, 30/06/2026) ----------
def ic_donut(a,b):
    return SV(f'<circle cx="100" cy="100" r="66" fill="none" stroke="{b}" stroke-width="30"/><path d="M100 34A66 66 0 1 1 52 146" fill="none" stroke="{a}" stroke-width="30" stroke-linecap="butt"/><circle cx="100" cy="100" r="30" fill="{a}" opacity=".15"/>{T(100,112,"76%",34,a,800,"Lora")}')
def ic_escudo_pessoa(a,b):
    return SV(f'<path d="M100 14L170 40V100C170 142 140 170 100 188C60 170 30 142 30 100V40Z" fill="{a}"/><circle cx="100" cy="78" r="20" fill="{b}"/><path d="M62 144C62 114 78 102 100 102C122 102 138 114 138 144Z" fill="{b}"/>')
def ic_relogio(a,b):
    return SV(f'<circle cx="100" cy="104" r="72" fill="{b}" stroke="{a}" stroke-width="10"/><path d="M100 60V106L132 126" fill="none" stroke="{a}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/><path d="M70 22H130" stroke="{a}" stroke-width="10" stroke-linecap="round"/><path d="M100 22V32" stroke="{a}" stroke-width="10"/>')
def ic_barras(a,b):
    return SV(f'<path d="M16 176H184" stroke="{a}" stroke-width="9" stroke-linecap="round"/><rect x="30" y="100" width="34" height="76" rx="5" fill="{a}"/><rect x="82" y="60" width="34" height="116" rx="5" fill="{b}" stroke="{a}" stroke-width="7"/><rect x="134" y="24" width="34" height="152" rx="5" fill="{a}"/>')
def ic_revisar(a,b):
    return SV(f'<rect x="30" y="20" width="124" height="158" rx="12" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M54 62H130M54 92H130M54 122H96" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M110 150A34 34 0 1 1 150 168" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round"/><path d="M150 140L152 172L122 166Z" fill="{a}"/>')

def cover_ucra():
    # painel de donut grande com 353 mil, sobre marfim; faixa terracota
    import math
    def arc(cx,cy,r,p0,p1):
        a0=-math.pi/2+2*math.pi*p0; a1=-math.pi/2+2*math.pi*p1
        x0,y0=cx+r*math.cos(a0),cy+r*math.sin(a0); x1,y1=cx+r*math.cos(a1),cy+r*math.sin(a1)
        return f'M{x0:.1f} {y0:.1f}A{r} {r} 0 {1 if p1-p0>.5 else 0} 1 {x1:.1f} {y1:.1f}'
    cx,cy,r=540,810,230
    return page(1350,IV,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{IV} 0,{SAND} 100%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:76px;line-height:1.06;font-weight:700;color:{G}">Ucranianos na Espanha: <span style="color:{TERRA};font-style:italic">353 mil</span> com residência em vigor</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{G}" stroke-width="78" opacity=".12"/>
      <path d="{arc(cx,cy,r,0,.76)}" fill="none" stroke="{TERRA}" stroke-width="78"/>
      <path d="{arc(cx,cy,r,.76,.96)}" fill="none" stroke="{GOLD}" stroke-width="78"/>
      <path d="{arc(cx,cy,r,.96,1)}" fill="none" stroke="{G2}" stroke-width="78"/>
      {T(cx,cy-6,'353.009',84,G,800,'Lora')}{T(cx,cy+48,'pessoas',34,G2,600,'Inter',ls=3)}
      <rect x="60" y="1100" width="340" height="62" rx="31" fill="{TERRA}"/>{T(230,1141,'76% proteção temporal',23,IV,700)}
      <rect x="415" y="1100" width="300" height="62" rx="31" fill="{GOLD}"/>{T(565,1141,'20% longa duração',23,G,700)}
      <rect x="730" y="1100" width="290" height="62" rx="31" fill="{G}"/>{T(875,1141,'Dados: 30/06/2026',23,IV,700)}
    </svg>
    {foot(G)}''')
NOT=[cover_ucra()]
NOT.append(content2('Notícia · Os números','Residência em vigor','<b>353.009</b> pessoas de nacionalidade ucraniana tinham documentação de residência em vigor em 30/06/2026, <b>8,2%</b> a mais do que um ano antes (25.675 pessoas).',ic_barras,'green',46))
NOT.append(content2('Notícia · Motivo','Proteção temporal','<b>262.782</b> pessoas têm proteção temporal, <b>76%</b> do total. Residência de longa duração: <b>67.724</b> pessoas, ou 20%.',ic_donut,'ivory',50))
NOT.append(content2('Notícia · Validade','Até 4 de março de 2027','A última data de validade da proteção temporal é <b>4/3/2027</b>. As autorizações são concedidas por um ano e prorrogadas anualmente desde março de 2022.',ic_relogio,'terra',46))
NOT.append(content2('Notícia · Trabalho','Afiliação à Seguridad Social','Com proteção temporal (maiores de 16 anos): <b>41.564</b> de 208.855 afiliados, 20%. Outros motivos: <b>41.350</b> de 82.821, ou 50%.',ic_escudo_pessoa,'green',48))
NOT.append(content2('Notícia · Atenção','Dados de junho de 2026','Os números são de 30/06/2026 e podem ser revisados em publicações posteriores. Confira sempre a fonte oficial.',ic_revisar,'ivory',50))
NOT.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: Ministerio de Inclusión, nota de prensa de 3/8/2026; Observatorio Permanente de la Inmigración.<br>Consulta em 17/11/2026.'))

# ---------- IMIGRAÇÃO: trabalhador transfronteiriço por conta alheia (Hoja 40) ----------
def ic_fronteira(a,b):
    return SV(f'<path d="M100 14V186" stroke="{a}" stroke-width="8" stroke-dasharray="3 14" stroke-linecap="round"/><circle cx="52" cy="62" r="20" fill="{a}"/><path d="M20 140C20 106 34 92 52 92C70 92 84 106 84 140Z" fill="{a}"/><rect x="118" y="106" width="64" height="62" rx="8" fill="{b}" stroke="{a}" stroke-width="7"/><path d="M130 106V92C130 84 136 80 142 80H158C164 80 170 84 170 92V106" fill="none" stroke="{a}" stroke-width="7"/><path d="M84 96L112 96M104 84L116 96L104 108" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_empresa(a,b):
    return SV(f'<rect x="22" y="70" width="156" height="108" rx="6" fill="{a}"/><path d="M22 70L56 24H144L178 70Z" fill="{b}" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><rect x="84" y="118" width="32" height="60" fill="{b}"/><rect x="38" y="92" width="30" height="24" fill="{b}"/><rect x="132" y="92" width="30" height="24" fill="{b}"/>')
def ic_contrato(a,b):
    return SV(f'<rect x="34" y="14" width="124" height="166" rx="10" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M58 52H134M58 76H134M58 100H110" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M58 150C70 126 80 160 92 140S110 150 118 140" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round"/><path d="M130 166L180 116L192 128L142 178L124 182Z" fill="{a}"/>')
def ic_verificado(a,b):
    return SV(f'<circle cx="100" cy="100" r="76" fill="{a}"/><path d="M62 104L90 132L142 74" fill="none" stroke="{b}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_prazo(a,b):
    return SV(f'<rect x="20" y="36" width="160" height="30" rx="8" fill="{a}"/><rect x="20" y="66" width="160" height="108" rx="10" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M62 24V48M138 24V48" stroke="{b}" stroke-width="9" stroke-linecap="round"/><path d="M48 106H152M48 140H152" stroke="{a}" stroke-width="6" stroke-dasharray="2 12" stroke-linecap="round"/><circle cx="82" cy="120" r="11" fill="{a}"/><rect x="108" y="104" width="44" height="32" rx="6" fill="{a}"/>')

def cover_front():
    # posto de fronteira: cancela listrada, guarita, montanhas e silhueta cruzando; cenário terracota
    cancela=''.join(f'<rect x="{260+i*60}" y="738" width="30" height="26" fill="{IV if i%2==0 else G}" transform="rotate(-4 540 750)"/>' for i in range(8))
    return page(1350,TERRA,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{TERRA} 0,#9C4529 100%)"></div>
    {bracket('#F3D79A')}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:920px;font-size:72px;line-height:1.06;font-weight:700;color:{IV}">Trabalhador <span style="color:#F3D79A;font-style:italic">transfronteiriço</span>: como funciona a autorização por conta alheia?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <path d="M0 700L180 520L300 620L470 470L640 640L800 540L1080 720V860H0Z" fill="{G}" opacity=".85"/>
      <path d="M0 780L260 650L420 740L700 620L1080 780V900H0Z" fill="{G2}"/>
      <rect x="0" y="860" width="1080" height="250" fill="{SAND}"/>
      <path d="M0 960H1080" stroke="{GOLD}" stroke-width="5" stroke-dasharray="26 18"/>
      <rect x="226" y="690" width="22" height="200" fill="{INK}"/><rect x="226" y="690" width="22" height="200" fill="{IV}" opacity=".2"/>
      <g transform="translate(0 0)">{cancela}</g>
      <rect x="800" y="700" width="150" height="160" fill="{IV}"/><path d="M786 700L875 640L964 700Z" fill="{G}"/><rect x="835" y="740" width="80" height="54" fill="{G2}"/><rect x="860" y="808" width="30" height="52" fill="{G}"/>
      <circle cx="560" cy="808" r="20" fill="{G}"/><path d="M530 880C530 846 544 830 560 830C576 830 590 846 590 880Z" fill="{G}"/>
      <path d="M610 842H700M684 828L700 842L684 856" fill="none" stroke="{TERRA}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
      {T(540,1070,'Residir do outro lado, trabalhar na Espanha',34,G,800,'Lora')}
    </svg>
    {foot(IV)}''')
IMG=[cover_front()]
IMG.append(content2('Imigração · Quem é','Trabalhador transfronteiriço','Quem <b>reside em província ou demarcação limítrofe</b> com a Espanha e trabalha por conta alheia aqui. Não vale para cidadãos da UE, do EEE ou da Suíça.',ic_fronteira,'ivory',46))
IMG.append(content2('Imigração · Quem pede','O pedido é do empregador','Pessoa física apresenta pessoalmente; pessoa jurídica, por seu representante legal. É preciso <b>contrato assinado</b> por ambas as partes.',ic_contrato,'green',48))
IMG.append(content2('Imigração · O trabalhador','Requisitos da pessoa','Sem antecedentes penais na Espanha e nos países onde residiu nos últimos <b>5 anos</b>. Capacitação da profissão, quando exigida. A situação nacional de emprego deve permitir a contratação.',ic_verificado,'terra',44))
IMG.append(content2('Imigração · O empregador','Requisitos da empresa','Inscrita na <b>Seguridad Social</b>, em dia com as obrigações tributárias e previdenciárias e com meios econômicos, materiais ou pessoais suficientes.',ic_empresa,'ivory',48))
IMG.append(content2('Imigração · Duração e pedido','Prazos e onde pedir','A duração coincide com a do contrato (de <b>3 meses a 1 ano</b>), para a ocupação indicada. Pedido na Oficina de Extranjería ou pelo Mercurio. A ficha oficial prevê resolução em 3 meses.',ic_prazo,'green',44))
IMG.append(closing(1350,G2,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 40 (atualizada em maio de 2025). Conteúdo orientativo.<br>Consulta em 17/11/2026.'))

async def render(lst,prefix,h):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h})
        for i,htm in enumerate(lst):
            await pg.set_content(htm); await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT+f'{prefix}-{i+1}.png')
        await b.close()
asyncio.run(render(NOT,'noticia',1350))
asyncio.run(render(IMG,'imigracao',1350))
