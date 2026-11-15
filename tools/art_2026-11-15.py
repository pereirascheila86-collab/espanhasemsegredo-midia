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

# ================= 2026-11-15 : ícones e cenas novos =================
def T(x,y,t,sz=40,col=IV,w=700,fam='Inter',anchor='middle',ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{sz}" letter-spacing="{ls}" fill="{col}">{t}</text>'

# ---------- ícones NOTÍCIA (afiliação) ----------
def ic_total(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="52" r="26" fill="{a}"/><path d="M52 128V96C52 72 148 72 148 96V128Z" fill="{a}"/><circle cx="44" cy="82" r="16" fill="{b}"/><circle cx="156" cy="82" r="16" fill="{b}"/><path d="M12 134V114C12 98 66 98 70 112" fill="{b}"/><path d="M188 134V114C188 98 134 98 130 112" fill="{b}"/><path d="M24 168H176" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M62 150L100 138L138 150" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'
def ic_barras(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="22" y="112" width="30" height="64" rx="5" fill="{a}"/><rect x="62" y="86" width="30" height="90" rx="5" fill="{a}"/><rect x="102" y="60" width="30" height="116" rx="5" fill="{a}"/><rect x="142" y="26" width="30" height="150" rx="5" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M14 184H186" stroke="{a}" stroke-width="8" stroke-linecap="round"/><path d="M30 92L80 62L120 40L158 14" fill="none" stroke="{b}" stroke-width="5" stroke-dasharray="3 10" stroke-linecap="round"/></svg>'
def ic_alta(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="14" y="42" width="172" height="116" rx="14" fill="{b}" stroke="{a}" stroke-width="8"/><circle cx="62" cy="88" r="20" fill="{a}"/><path d="M30 138C30 112 94 112 94 138Z" fill="{a}"/><path d="M112 78H168M112 100H156" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="150" cy="134" r="22" fill="{a}"/><path d="M139 134L147 143L162 124" stroke="{b}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_pizza(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="80" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M100 100V20A80 80 0 1 1 28 134Z" fill="{a}"/><path d="M100 100L28 134A80 80 0 0 1 60 36Z" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M100 100L60 36A80 80 0 0 1 100 20Z" fill="{a}" opacity=".55"/><circle cx="100" cy="100" r="14" fill="{b}"/></svg>'
def ic_pins(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M62 28C32 28 18 52 18 74C18 104 62 150 62 150C62 150 106 104 106 74C106 52 92 28 62 28Z" fill="{a}"/><circle cx="62" cy="74" r="16" fill="{b}"/><path d="M142 52C116 52 104 72 104 90C104 116 142 156 142 156C142 156 180 116 180 90C180 72 168 52 142 52Z" fill="{b}" stroke="{a}" stroke-width="8"/><circle cx="142" cy="90" r="13" fill="{a}"/><path d="M20 182H180" stroke="{a}" stroke-width="8" stroke-linecap="round"/></svg>'

def cover_afiliacao():
    base=700
    barras=''
    vals=[150,190,235,285,345,410,490]
    for i,v in enumerate(vals):
        x=110+i*120
        col=GOLD if i==len(vals)-1 else G2
        barras+=f'<rect x="{x}" y="{1010-v}" width="86" height="{v}" rx="6" fill="{col}"/>'
        # figuras no topo
        barras+=f'<circle cx="{x+43}" cy="{1010-v-26}" r="20" fill="{col}"/><path d="M{x+8} {1010-v}C{x+8} {1010-v-26} {x+78} {1010-v-26} {x+78} {1010-v}Z" fill="{col}"/>'
    return page(1350,IV,f'''{bracket(G2)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Notícia · Seguridade Social</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:68px;line-height:1.07;font-weight:700;color:{G}">Afiliação de estrangeiros chega a <span style="color:{TERRA};font-style:italic">3,7 milhões</span> em outubro</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <rect x="70" y="520" width="940" height="560" rx="26" fill="{SAND}"/>
      <path d="M90 700H990M90 800H990M90 900H990" stroke="{IV}" stroke-width="3"/>
      {barras}
      <path d="M90 1010H990" stroke="{G}" stroke-width="6" stroke-linecap="round"/>
      <rect x="120" y="548" width="270" height="86" rx="43" fill="{G}"/>{T(255,606,'16,4% do total',36,IV,800,'Inter')}
    </svg>
    {foot(G)}''')
NOT=[cover_afiliacao()]
NOT.append(content2('Notícia · Panorama','Total de afiliados','Média de <b>22.624.165</b> afiliados em outubro, o nível mais alto da série: <b>186.612</b> a mais do que em setembro e <b>784.573</b> a mais em um ano.',ic_total,'green',46))
NOT.append(content2('Notícia · Estrangeiros','Afiliados estrangeiros','<b>3.699.878</b> estrangeiros afiliados, <b>16,4%</b> do total: <b>63.899</b> a mais que em setembro e <b>598.378</b> a mais em um ano.',ic_barras,'terra',48))
NOT.append(content2('Notícia · Regularização','Processo extraordinário','No fim de outubro, <b>490.586</b> estrangeiros estavam em alta na Seguridade Social ligados ao processo extraordinário de regularização.',ic_alta,'ivory',48))
NOT.append(content2('Notícia · Desde abril','Quem já esteve em alta','<b>557.410</b> pessoas estiveram em alta ao menos um dia. Dessas, <b>75,2%</b> no Regime Geral e <b>5,9%</b> no regime de autônomos.',ic_pizza,'green',48))
NOT.append(content2('Notícia · Perfil e território','Nacionalidades e regiões','Entre os <b>490.586</b> em alta no fim de outubro, <b>27,6%</b> são colombianos e <b>15,7%</b> venezuelanos. Catalunha e Madri concentram a maior parte.',ic_pins,'terra',46))
NOT.append(closing(1350,G2,IV,GOLD,'Fonte: Seguridad Social (dados de outubro de 2026, publicados em 04/11/2026).<br>Consulta em 15/11/2026.'))

# ---------- ícones IMIGRAÇÃO (contratações em origem) ----------
def ic_contrato(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="14" width="120" height="164" rx="10" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M62 52H138M62 76H138M62 100H112" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M62 146C74 122 86 150 98 130C106 118 114 140 128 128" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round"/><circle cx="148" cy="152" r="26" fill="{a}"/><path d="M136 152L145 161L161 142" stroke="{b}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_orden(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="22" y="34" width="156" height="142" rx="14" fill="{b}" stroke="{a}" stroke-width="8"/><rect x="22" y="34" width="156" height="40" rx="12" fill="{a}"/><path d="M60 20V46M140 20V46" stroke="{a}" stroke-width="9" stroke-linecap="round"/>{T(100,134,'2026',50,a,800,'Lora')}{T(100,162,'ORDEN ANUAL',17,a,800,'Inter',ls=2)}</svg>'
def ic_passaporte(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="44" y="12" width="112" height="170" rx="12" fill="{a}"/><circle cx="100" cy="76" r="30" fill="none" stroke="{b}" stroke-width="6"/><path d="M70 76H130M100 46C86 62 86 90 100 106M100 46C114 62 114 90 100 106" stroke="{b}" stroke-width="4" fill="none"/><path d="M66 140H134" stroke="{b}" stroke-width="7" stroke-linecap="round"/><circle cx="150" cy="150" r="30" fill="{b}" stroke="{a}" stroke-width="7"/><path d="M137 150L147 160L165 138" stroke="{a}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_oferta(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="24" y="64" width="152" height="108" rx="14" fill="{a}"/><path d="M72 64V46C72 36 78 30 88 30H112C122 30 128 36 128 46V64" fill="none" stroke="{a}" stroke-width="10"/><path d="M24 112H176" stroke="{b}" stroke-width="7"/><rect x="86" y="100" width="28" height="26" rx="5" fill="{b}"/><path d="M100 14V0" stroke="{a}" stroke-width="1"/></svg>'
def ic_relogio(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="78" fill="{b}" stroke="{a}" stroke-width="10"/><path d="M100 44V100L138 122" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><circle cx="100" cy="100" r="9" fill="{a}"/><path d="M100 22V34M100 166V178M22 100H34M166 100H178" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'

def cover_origem():
    # arco do voo: do mar ao campo, contrato ao centro (cena nova)
    ondas=''.join(f'<path d="M0 {1020+i*46}C180 {990+i*46} 360 {1050+i*46} 540 {1020+i*46}S900 {990+i*46} 1080 {1020+i*46}" fill="none" stroke="{GOLD}" stroke-width="{4+i}" opacity="{.9-i*.15:.2f}"/>' for i in range(5))
    pts=''.join(f'<circle cx="{x}" cy="{y}" r="9" fill="{GOLD}"/>' for x,y in [(160,830),(260,730),(380,660),(520,630),(660,650),(790,720),(880,820)])
    return page(1350,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 50% 56%,{G2} 0,{G} 68%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:68px;line-height:1.07;font-weight:700;color:{IV}">Contratações em <span style="color:{GOLD};font-style:italic">origem</span>: como funciona a gestão coletiva?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      {pts}
      <path d="M160 830C260 640 800 560 880 820" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="3 18" stroke-linecap="round"/>
      <g transform="translate(60 800)"><circle cx="100" cy="20" r="26" fill="{IV}"/><path d="M50 130V80C50 50 150 50 150 80V130Z" fill="{IV}"/><rect x="30" y="130" width="140" height="14" rx="6" fill="{GOLD}"/></g>
      <g transform="translate(760 800)"><circle cx="100" cy="20" r="26" fill="{TERRA}"/><path d="M50 130V80C50 50 150 50 150 80V130Z" fill="{TERRA}"/><rect x="30" y="130" width="140" height="14" rx="6" fill="{GOLD}"/></g>
      <g transform="translate(405 580)"><rect x="0" y="0" width="270" height="330" rx="20" fill="{IV}"/><path d="M40 70H230M40 112H230M40 154H180" stroke="{G}" stroke-width="12" stroke-linecap="round"/><path d="M50 250C80 200 105 270 135 230C155 205 175 255 205 232" fill="none" stroke="{TERRA}" stroke-width="9" stroke-linecap="round"/><circle cx="215" cy="285" r="36" fill="{GOLD}"/><path d="M198 285L211 298L234 270" stroke="{G}" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      {ondas}
    </svg>
    {foot(IV)}''')
IMG=[cover_origem()]
IMG.append(content2('Imigração · O que é','Gestão coletiva','Procedimento que concede várias autorizações de residência e trabalho, ou de temporada, de uma vez, a trabalhadores que não estão na Espanha, a partir de ofertas de empregadores.',ic_contrato,'ivory',46))
IMG.append(content2('Imigração · Orden anual','Uma Orden por ano','O Ministério pode aprovar uma Orden por ano com as ocupações e, se for o caso, o número de postos. A de 2026 é a Orden ISM/1547/2025, com garantia de alojamento na migração circular.',ic_orden,'terra',44))
IMG.append(content2('Imigração · O trabalhador','Requisitos do trabalhador','Não estar nem residir na Espanha; não ser cidadão da UE, do EEE ou da Suíça; sem antecedentes penais nos últimos cinco anos. Em postos de temporada, compromisso de regressar.',ic_passaporte,'green',44))
IMG.append(content2('Imigração · O empregador','Ofertas do empregador','Apresenta ofertas genéricas, por si ou por representante, com contratos assinados e salário líquido previsto. Deve estar inscrito na Seguridade Social e em dia com as obrigações tributárias.',ic_oferta,'ivory',44))
IMG.append(content2('Imigração · Visto e prazos','O que a ficha prevê','Pedir o visto em até <b>dois meses</b> após a concessão e emiti-lo em até <b>cinco dias úteis</b>. Alta na Seguridade Social: até três dias da entrada (temporada) ou três meses (estáveis).',ic_relogio,'terra',44))
IMG.append(closing(1350,G,IV,GOLD,'Fontes: Ministerio de Inclusión, Hoja 24 (atualizada em maio de 2025); Moncloa, nota de 30/12/2025 (Orden GECCO 2026).<br>Consulta em 15/11/2026.'))

# ---------- CULTURA (Reel): Cueva de Altamira ----------
def bisonte(x,y,s,col,flip=False,det=None):
    det=det or col
    if flip: g=f'<g transform="translate({x+200*s} {y}) scale({-s} {s})">'
    else: g=f'<g transform="translate({x} {y}) scale({s} {s})">'
    g+=f'<path d="M40 62C46 24 90 6 118 30C140 44 170 40 186 56C200 70 196 90 190 98L184 126L172 126L168 100L136 102L130 126L118 126L114 100L84 98L76 126L62 126L60 96C48 92 40 80 40 62Z" fill="{col}"/>'
    g+=f'<path d="M44 60C20 52 6 66 8 88C10 104 26 112 40 102L52 90Z" fill="{col}"/><path d="M16 100L8 124L30 108Z" fill="{col}"/><path d="M22 58C14 42 24 32 38 40" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/><path d="M192 70C206 84 204 104 198 116" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>'
    g+=f'<path d="M70 40C84 62 86 80 82 96M104 36C112 60 112 80 108 98" stroke="{det}" stroke-width="3" fill="none" opacity=".4"/></g>'
    return g
def cena_teto(w,h):
    fundo=f'<rect width="{w}" height="{h}" fill="{TERRA}"/><path d="M0 0H{w}V{h*.2:.0f}C{w*.7:.0f} {h*.3:.0f} {w*.3:.0f} {h*.12:.0f} 0 {h*.24:.0f}Z" fill="#8E3F26"/>'
    mancha=f'<ellipse cx="{w*.5:.0f}" cy="{h*.52:.0f}" rx="{w*.46:.0f}" ry="{h*.38:.0f}" fill="#D9744F" opacity=".55"/>'
    bis=bisonte(60,190,2.0,'#4A1F14')+bisonte(480,470,2.0,G,True)+bisonte(70,740,1.8,'#4A1F14')+bisonte(540,880,1.3,GOLD,True)
    rach=f'<path d="M0 {h-60}C200 {h-110} 400 {h-30} 620 {h-90}S900 {h-60} {w} {h-100}V{h}H0Z" fill="#8E3F26"/>'
    return fundo+mancha+bis+rach
def cena_secao(w,h):
    rocha=f'<rect width="{w}" height="{h}" fill="{G}"/><path d="M0 0H{w}V90C700 130 600 60 420 100C260 130 120 70 0 110Z" fill="{G2}"/><path d="M0 {h}V{h-120}C140 {h-150} 300 {h-90} 480 {h-130}S800 {h-100} {w} {h-140}V{h}Z" fill="{G2}"/>'
    cav=f'<path d="M60 380C60 300 150 280 240 300C320 230 420 250 500 300C600 280 690 270 780 320C890 340 900 430 800 470C690 520 600 470 500 500C380 540 300 480 220 510C120 520 60 470 60 380Z" fill="{SAND}"/>'
    divs=f'<path d="M290 300V480M590 290V500" stroke="{TERRA}" stroke-width="5" stroke-dasharray="4 12"/>'
    lab=T(175,400,'Vestíbulo',34,G,800)+T(440,410,'Galeria',34,G,800)+T(700,400,'Sala lateral',32,G,800)
    esc=f'<path d="M60 600H900" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/><path d="M60 584V616M900 584V616" stroke="{GOLD}" stroke-width="8"/>'+T(480,690,'cerca de 270 metros',46,GOLD,700,'Lora')
    bis=bisonte(380,325,.34,TERRA)
    return rocha+f'<g transform="translate(-48 -150) scale(1.1)">{cav}{divs}{lab}{bis}</g>'+esc
def cena_costa(w,h):
    mar=f'<rect width="{w}" height="{h}" fill="{G}"/><path d="M0 330C160 300 320 360 480 330S800 300 {w} 340V{h}H0Z" fill="{G2}"/>'
    linha=f'<path d="M40 330C200 300 360 360 520 330S820 300 920 330" fill="none" stroke="{SAND}" stroke-width="4" stroke-dasharray="3 12"/>'
    dots=''
    xs=[70+i*(820/17) for i in range(18)]
    for i,x in enumerate(xs):
        y=330+14*math.sin(i*.9)
        c=GOLD if i==5 else IV
        r=26 if i==5 else 14
        dots+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>'
    lab=T(180,262,'Astúrias',34,IV,800)+T(480,262,'Cantábria',34,GOLD,800)+T(780,262,'País Basco',34,IV,800)
    lamp=f'<g transform="translate(330 470)"><path d="M0 70H120L110 130H10Z" fill="{GOLD}"/><path d="M20 70C20 30 100 30 100 70" fill="none" stroke="{GOLD}" stroke-width="10"/><circle cx="60" cy="100" r="16" fill="{G}"/><path d="M60 -10C34 20 40 34 60 36C80 34 86 20 60 -10Z" fill="{TERRA}"/></g>'
    ano=T(640,590,'1879',130,GOLD,700,'Lora')+T(640,650,'DESCOBERTA',30,IV,800,'Inter',ls=5)
    lab2=T(480,735,'18 cavernas · Costa Cantábrica',38,SAND,700)
    return mar+linha+dots+lab+lamp+ano+lab2
def cena_replica(w,h):
    fundo=f'<rect width="{w}" height="{h}" fill="{SAND}"/>'
    # esquerda: cueva original com cadeado
    esq=f'<path d="M50 560V360C50 220 150 170 240 170C330 170 430 220 430 360V560Z" fill="{G}"/><path d="M110 560V380C110 290 170 250 240 250C310 250 370 290 370 380V560Z" fill="{TERRA}"/>{bisonte(150,380,.5,"#4A1F14")}'
    cad=f'<rect x="190" y="610" width="100" height="78" rx="12" fill="{G}"/><path d="M208 610V582C208 540 272 540 272 582V610" fill="none" stroke="{G}" stroke-width="13"/><circle cx="240" cy="648" r="10" fill="{GOLD}"/>'
    # seta
    seta=f'<path d="M455 400H500" stroke="{TERRA}" stroke-width="12" stroke-linecap="round"/><path d="M490 376L526 400L490 424Z" fill="{TERRA}"/>'
    # direita: museu com réplica
    dir_=f'<rect x="540" y="330" width="370" height="230" fill="{G2}"/><path d="M520 330L725 220L930 330Z" fill="{G}"/><rect x="600" y="400" width="250" height="160" rx="125" fill="{TERRA}"/>{bisonte(650,440,.42,"#4A1F14")}<rect x="520" y="560" width="410" height="22" fill="{G}"/>'
    lab=T(240,780,'Cueva original',38,G,800)+T(240,824,'visita muito restrita',30,G,500)+T(725,690,'Neocueva',44,TERRA,800,'Lora')+T(725,736,'réplica no Museu de Altamira',30,G,500)
    return fundo+f'<g transform="translate(0 -90)">{esq}{cad}{seta}{dir_}{lab}</g>'
def reel():
    S=[]
    S.append(rbv(f'''{Tv('A <span style="color:@AC;font-style:italic">Cueva de Altamira</span>, em Cantábria, é Patrimônio Mundial',84)}
    {cardv(60,640,960,1100,TERRA,cena_teto(960,1100),0)}''',1,'ivory'))
    S.append(rbv(f'''{Tv('Arte rupestre em <span style="color:@AC">Santillana del Mar</span>',78)}
    {Pv('Cavidade com vestíbulo, galeria e sala lateral. As figuras, em ocre vermelho contornado em preto, representam bisontes, cervos, javalis e cavalos.',500)}
    {cardv(60,1010,960,730,G,cena_secao(960,730),0)}''',2,'green'))
    S.append(rbv(f'''{Tv('A primeira <span style="color:@AC">identificada</span>',100)}
    {Pv('Descoberta em 1879, foi a primeira caverna em que a arte paleolítica foi identificada, segundo a UNESCO. O conjunto cantábrico reúne 18 cavernas.',480)}
    {cardv(60,960,960,780,G,cena_costa(960,780),0)}''',3,'terra'))
    S.append(rbv(f'''{Tv('Uma <span style="color:@AC">réplica</span> para proteger',86)}
    {Pv('A visita à cueva original é muito restrita para proteger as pinturas. No Museu de Altamira, a Neocueva reproduz a estrutura e os murais.',500)}
    {cardv(60,980,960,760,SAND,cena_replica(960,760),0)}''',4,'ivory'))
    S.append(closing(1920,TERRA,IV,'#F3D79A','Fontes: UNESCO, Patrimônio Mundial (Altamira); Turespaña (spain.info), Cuevas de Altamira e Museo de Altamira.<br>Consulta em 15/11/2026.',logo=460,serif_sz=88,top=.2))
    return S
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
S=reel(); asyncio.run(render(S,'cultura',1920))
n=len(S); d=3.5; f=0.4
cmd=['ffmpeg','-y','-loglevel','error']
for i in range(n): cmd+=['-loop','1','-t',str(d),'-i',OUT+f'cultura-{i+1}.png']
flt=''.join(f'[{i}:v]format=yuv420p,fade=t=in:st=0:d={f},fade=t=out:st={d-f}:d={f}[v{i}];' for i in range(n))
flt+=''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[o]'
cmd+=['-filter_complex',flt,'-map','[o]','-r','30','-pix_fmt','yuv420p',OUT+'reel-cultura.mp4']
subprocess.run(cmd,check=True)
