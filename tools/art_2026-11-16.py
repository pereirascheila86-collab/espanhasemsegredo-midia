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

# ================= 2026-11-16 : ícones e cenas novos =================
def T(x,y,t,sz=40,col=IV,w=700,fam='Inter',anchor='middle',ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{sz}" letter-spacing="{ls}" fill="{col}">{t}</text>'
def SV(inner): return f'<svg width="100%" height="100%" viewBox="0 0 200 200">{inner}</svg>'

# ---------- NOTÍCIA: Canárias ----------
def ic_recorde(a,b):  # termômetro/medidor com marca
    return SV(f'<path d="M24 160A84 84 0 0 1 176 160" fill="none" stroke="{a}" stroke-width="16" stroke-linecap="round"/><path d="M24 160A84 84 0 0 1 150 84" fill="none" stroke="{b}" stroke-width="16" stroke-linecap="round"/><path d="M100 150L150 84" stroke="{a}" stroke-width="9" stroke-linecap="round"/><circle cx="100" cy="150" r="14" fill="{a}"/><path d="M168 66L180 50M182 90L198 84" stroke="{b}" stroke-width="6" stroke-linecap="round"/>')
def ic_barco(a,b):
    return SV(f'<path d="M20 120H180L156 160H44Z" fill="{a}"/><path d="M60 120V84H140V120" fill="{b}" stroke="{a}" stroke-width="7"/><circle cx="82" cy="102" r="7" fill="{a}"/><circle cx="104" cy="102" r="7" fill="{a}"/><circle cx="126" cy="102" r="7" fill="{a}"/><path d="M96 84V50H112" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round"/><path d="M10 176C40 164 60 188 90 176S150 164 190 176" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round"/>')
def ic_leitos(a,b):
    return SV(f'<rect x="14" y="110" width="172" height="20" rx="6" fill="{a}"/><rect x="14" y="130" width="12" height="40" fill="{a}"/><rect x="174" y="130" width="12" height="40" fill="{a}"/><rect x="22" y="76" width="52" height="34" rx="12" fill="{b}" stroke="{a}" stroke-width="7"/><rect x="82" y="86" width="96" height="24" rx="8" fill="{b}" stroke="{a}" stroke-width="7"/><circle cx="148" cy="36" r="22" fill="{a}"/><path d="M148 26V46M138 36H158" stroke="{b}" stroke-width="7" stroke-linecap="round"/>')
def ic_edificio(a,b):
    return SV(f'<path d="M20 176H180" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M100 22L176 70H24Z" fill="{a}"/><rect x="40" y="76" width="22" height="84" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="89" y="76" width="22" height="84" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="138" y="76" width="22" height="84" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="26" y="160" width="148" height="14" fill="{a}"/><circle cx="100" cy="48" r="9" fill="{b}"/>')
def ic_calendario(a,b):
    return SV(f'<rect x="22" y="34" width="156" height="142" rx="14" fill="{b}" stroke="{a}" stroke-width="8"/><rect x="22" y="34" width="156" height="38" rx="12" fill="{a}"/><path d="M60 20V46M140 20V46" stroke="{a}" stroke-width="9" stroke-linecap="round"/>{T(100,134,"NOV",54,a,800,"Lora")}{T(100,162,"2026",24,a,800,"Inter",ls=3)}')

def cover_canarias():
    # mapa-simples do arquipélago, ondas e cayuco com pessoas; dados em faixa
    ilhas=''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" stroke="{G}" stroke-width="3"/>' for x,y,rx,ry,c in [(190,640,70,38,SAND),(430,700,60,34,SAND),(650,610,86,46,SAND),(840,690,64,36,SAND),(960,610,40,24,SAND)])
    ilhas+=f'<ellipse cx="190" cy="640" rx="70" ry="38" fill="{GOLD}" stroke="{G}" stroke-width="3"/>'  # El Hierro destaque (ilha oeste)
    ondas=''.join(f'<path d="M0 {880+i*52}C150 {850+i*52} 330 {910+i*52} 540 {880+i*52}S900 {850+i*52} 1080 {880+i*52}" fill="none" stroke="{IV}" stroke-width="{3+i}" opacity="{.55-i*.1:.2f}"/>' for i in range(5))
    cay=f'<g transform="translate(330 770)"><path d="M0 70H420L380 130H40Z" fill="{TERRA}"/>'+''.join(f'<circle cx="{40+i*34}" cy="38" r="12" fill="{IV}"/><rect x="{30+i*34}" y="50" width="22" height="22" rx="8" fill="{IV}"/>' for i in range(11))+f'</g>'
    return page(1350,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{G} 0,{G2} 100%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Canárias</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:68px;line-height:1.07;font-weight:700;color:{IV}">Canárias registra <span style="color:{GOLD};font-style:italic">recorde diário</span> de chegadas de migrantes</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <rect x="0" y="560" width="1080" height="790" fill="{G2}" opacity=".0"/>
      {ilhas}{T(190,708,"El Hierro",30,GOLD,800)}
      <path d="M190 640L230 790" stroke="{GOLD}" stroke-width="4" stroke-dasharray="3 12" stroke-linecap="round"/>
      {ondas}{cay}
      <rect x="70" y="1050" width="940" height="110" rx="55" fill="{IV}"/>{T(540,1120,"Sábado, 14 de novembro de 2026",40,G,800,"Lora")}
    </svg>
    {foot(IV)}''')
NOT=[cover_canarias()]
NOT.append(content2('Notícia · Sábado, 14/11','O novo recorde','Entre <b>1.488</b> e <b>1.580</b> pessoas chegaram às Canárias em um só dia, conforme o veículo (dados provisórios). O recorde anterior era de <b>1.461</b>, em 7/11/2020.',ic_recorde,'green',46))
NOT.append(content2('Notícia · Fim de semana','Mais de 2.500 pessoas','No domingo (15/11), seis cayucos com <b>1.049</b> ocupantes chegaram a El Hierro, segundo a Infobae. Salvamento Marítimo e Guardia Civil atuam no resgate.',ic_barco,'terra',46))
NOT.append(content2('Notícia · El Hierro','Acolhida sobrecarregada','O centro de atenção temporária tem <b>500 vagas</b> e a ilha abrigava mais de <b>1.600</b> migrantes. O Cabildo declarou emergência social.',ic_leitos,'ivory',48))
NOT.append(content2('Notícia · Governo','O que o Governo anunciou','O ministro Ángel Víctor Torres visitou a ilha, anunciou uma terceira guardamar e uma reunião interministerial na terça-feira. Clavijo pede <b>15,18 milhões de euros</b>.',ic_edificio,'green',44))
NOT.append(content2('Notícia · Novembro','O mês até agora','Até o texto da Infobae, <b>10.495</b> pessoas chegaram às Canárias em novembro, em 108 embarcações (dado provisório do governo regional). Os números podem mudar.',ic_calendario,'terra',46))
NOT.append(closing(1350,G2,IV,GOLD,'Fontes: Euronews (15/11/2026); Infobae (15/11/2026); Diario de Avisos (08/11/2026).<br>Consulta em 16/11/2026.'))

# ---------- IMIGRAÇÃO: prestações transnacionais ----------
def ic_deslocamento(a,b):
    return SV(f'<rect x="10" y="100" width="64" height="76" rx="8" fill="{a}"/><rect x="126" y="60" width="64" height="116" rx="8" fill="{a}"/><path d="M26 118H58M26 138H58M142 80H174M142 100H174M142 120H174M142 140H174" stroke="{b}" stroke-width="6" stroke-linecap="round"/><path d="M82 70C104 30 120 30 122 56" fill="none" stroke="{b}" stroke-width="7" stroke-dasharray="2 11" stroke-linecap="round"/><path d="M114 44L124 62L140 46Z" fill="{b}"/><path d="M6 182H194" stroke="{a}" stroke-width="8" stroke-linecap="round"/>')
def ic_revogado(a,b):
    return SV(f'<rect x="40" y="14" width="120" height="164" rx="10" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M62 52H138M62 76H138M62 100H112" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M30 150L170 40" stroke="{a}" stroke-width="12" stroke-linecap="round"/><circle cx="148" cy="150" r="26" fill="{a}"/><path d="M137 139L159 161M159 139L137 161" stroke="{b}" stroke-width="7" stroke-linecap="round"/>')
def ic_grupo(a,b):
    return SV(f'<circle cx="100" cy="100" r="30" fill="{a}"/><circle cx="34" cy="48" r="20" fill="{b}" stroke="{a}" stroke-width="7"/><circle cx="166" cy="48" r="20" fill="{b}" stroke="{a}" stroke-width="7"/><circle cx="34" cy="160" r="20" fill="{b}" stroke="{a}" stroke-width="7"/><circle cx="166" cy="160" r="20" fill="{b}" stroke="{a}" stroke-width="7"/><path d="M50 60L78 84M150 60L122 84M50 148L78 118M150 148L122 118" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M90 100H110M100 90V110" stroke="{b}" stroke-width="7" stroke-linecap="round"/>')
def ic_lupa(a,b):
    return SV(f'<rect x="24" y="22" width="108" height="140" rx="10" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M46 56H110M46 80H110M46 104H84" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="130" cy="124" r="34" fill="{b}" stroke="{a}" stroke-width="12"/><path d="M155 150L188 184" stroke="{a}" stroke-width="14" stroke-linecap="round"/>')
def ic_aviso(a,b):
    return SV(f'<path d="M100 20L184 168H16Z" fill="{a}"/><path d="M100 70V120" stroke="{b}" stroke-width="13" stroke-linecap="round"/><circle cx="100" cy="146" r="9" fill="{b}"/>')

def cover_tps():
    # cena nova: dois prédios (origem e Espanha) ligados por seta, carimbo REVOGADA
    ond=''
    prediosL=''.join(f'<rect x="{110+i*70}" y="{740-h}" width="56" height="{h}" fill="{IV}" opacity=".9"/>' for i,h in enumerate([150,220,180]))
    prediosR=''.join(f'<rect x="{690+i*70}" y="{740-h}" width="56" height="{h}" fill="{GOLD}"/>' for i,h in enumerate([200,140,260]))
    jan=''.join(f'<rect x="{696+i*70}" y="{740-h+24+j*44}" width="12" height="16" fill="{G}"/><rect x="{722+i*70}" y="{740-h+24+j*44}" width="12" height="16" fill="{G}"/>' for i,h in enumerate([200,140,260]) for j in range(int((h-30)//44)))
    return page(1350,IV,f'''{bracket(G2)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:66px;line-height:1.07;font-weight:700;color:{G}">Prestação transnacional de serviços: <span style="color:{TERRA};font-style:italic">o que mudou</span>?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <rect x="60" y="500" width="960" height="380" rx="26" fill="{G}"/>
      <path d="M60 740H1020" stroke="{GOLD}" stroke-width="5"/>
      {prediosL}{prediosR}{jan}
      <path d="M470 600C540 540 600 540 660 600" fill="none" stroke="{IV}" stroke-width="6" stroke-dasharray="3 14" stroke-linecap="round"/><path d="M646 574L668 606L632 612Z" fill="{IV}"/>
      {T(250,800,'Empresa fora da UE',30,IV,700)}{T(800,800,'Centro de trabalho na Espanha',26,GOLD,700)}{T(800,836,'',20)}
      <g transform="rotate(-9 540 1030)"><rect x="250" y="940" width="580" height="170" rx="18" fill="none" stroke="{TERRA}" stroke-width="10"/><rect x="266" y="956" width="548" height="138" rx="10" fill="none" stroke="{TERRA}" stroke-width="3"/>{T(540,1058,'REVOGADA',86,TERRA,800,'Lora',ls=6)}</g>
    </svg>
    {foot(G)}''')
IMG=[cover_tps()]
IMG.append(content2('Imigração · O que era','Deslocamento temporário','Um trabalhador estrangeiro se desloca a um centro de trabalho na Espanha, vinculado a uma empresa estabelecida fora da UE e do EEE.',ic_deslocamento,'ivory',48))
IMG.append(content2('Imigração · O que mudou','Autorização revogada','Segundo a ficha oficial do Ministério de Inclusão, a autorização específica de prestações transnacionais de serviços está revogada.',ic_revogado,'terra',48))
IMG.append(content2('Imigração · Regime atual','Traslado intraempresarial','A ficha informa que o caso é tratado como traslado intraempresarial, quando cumpridos os requisitos da Lei 14/2013.',ic_grupo,'green',48))
IMG.append(content2('Imigração · Onde conferir','Requisitos e documentos','Os requisitos de cada situação constam nas páginas do Ministério de Inclusão e da Unidade de Grandes Empresas. Confira a versão vigente antes de qualquer pedido.',ic_lupa,'ivory',46))
IMG.append(content2('Imigração · Atenção','Textos antigos circulam','Guias e consulados ainda citam o regime anterior. Cada caso é diferente: confirme a norma vigente na data do pedido.',ic_aviso,'terra',48))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, página Prestaciones transnacionales de servicios; RD 1155/2024 (BOE).<br>Consulta em 16/11/2026.'))

# ---------- CULTURA: Mezquita de Córdoba ----------
def arco_ferradura(cx,y,w,h,col,fill='none',sw=0):
    r=w/2
    return f'<path d="M{cx-r*.78} {y+h} L{cx-r*.78} {y+r*.9} A{r} {r} 0 1 1 {cx+r*.78} {y+r*.9} L{cx+r*.78} {y+h}" fill="{fill}" stroke="{col}" stroke-width="{sw}"/>'
def cena_arcos(w,h):
    bg=f'<rect width="{w}" height="{h}" fill="{G}"/>'
    s=''
    # arcos de dupla ordem com aduelas alternadas (vermelho/marfim)
    for k,(ww,y0,col) in enumerate([(820,70,G2),(660,150,TERRA),(500,230,G2),(340,310,TERRA)]):
        cx=w/2
        s+=arco_ferradura(cx,y0,ww,h-y0-90,IV,col,10)
        # aduelas
        for i in range(9):
            ang=math.pi*(0.08+i*0.105)
            r=ww/2
            x1=cx+math.cos(ang)*r*.98; y1=y0+r*.9-math.sin(ang)*r*.98
            x2=cx+math.cos(ang)*(r*.78); y2=y0+r*.9-math.sin(ang)*(r*.78)
            s+=f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{IV if i%2 else GOLD}" stroke-width="12"/>'
    chao=f'<rect y="{h-90}" width="{w}" height="90" fill="{SAND}"/><path d="M0 {h-90}H{w}" stroke="{GOLD}" stroke-width="6"/>'
    return bg+s+chao
def cena_mapa(w,h):
    fundo=f'<rect width="{w}" height="{h}" fill="{G}"/>'
    # planta: recinto + extensão: retângulo central, 80,28 ha como moldura
    planta=f'<g transform="translate(0 22) scale(1 .72)"><rect x="130" y="90" width="700" height="440" rx="18" fill="{G2}" stroke="{GOLD}" stroke-width="6" stroke-dasharray="4 14"/><rect x="330" y="200" width="300" height="220" fill="{TERRA}"/><rect x="470" y="260" width="64" height="100" fill="{IV}"/><path d="M330 310H630" stroke="{IV}" stroke-width="3" opacity=".6"/></g>'
    ruas=f'<g transform="translate(0 22) scale(1 .72)"><path d="M130 160C300 130 420 190 640 140S780 170 830 150M130 460C320 500 520 430 830 480" fill="none" stroke="{SAND}" stroke-width="5" opacity=".5"/></g>'
    rio=''
    txt=T(480,60,'Centro histórico: 80,28 ha',40,GOLD,800,'Lora')+T(480,520,'1984',130,IV,700,'Lora')+T(480,570,'INSCRIÇÃO',28,GOLD,800,'Inter',ls=6)+T(480,640,'extensão em 1994',38,SAND,700)
    return fundo+planta+ruas+rio+txt
def cena_mesquitas(w,h):
    fundo=f'<rect width="{w}" height="{h}" fill="{SAND}"/>'
    s=''
    xs=[(120,330),(300,290),(480,350),(660,300),(840,340)]
    for x,top in xs:
        s+=f'<rect x="{x-40}" y="{top}" width="80" height="{620-top}" fill="{G}"/><path d="M{x-48} {top}C{x-48} {top-50} {x+48} {top-50} {x+48} {top}Z" fill="{TERRA}"/><rect x="{x-5}" y="{top-80}" width="10" height="40" fill="{G}"/><circle cx="{x}" cy="{top-90}" r="9" fill="{GOLD}"/><rect x="{x-12}" y="{top+30}" width="24" height="46" rx="12" fill="{SAND}"/>'
    s+=f'<rect x="0" y="620" width="{w}" height="{h-620}" fill="{G}"/><path d="M0 620H{w}" stroke="{GOLD}" stroke-width="6"/>'
    s+=T(480,690,'cerca de 300 mesquitas',52,IV,700,'Lora')
    return fundo+s+T(480,100,'Córdoba, a partir do século VIII',40,G,800,'Lora')
def cena_catedral(w,h):
    fundo=f'<rect width="{w}" height="{h}" fill="{TERRA}"/>'
    # mesquita (arcos) à esquerda -> nave gótica/cruz no centro do bloco
    bloco=f'<g transform="translate(0 -50)"><rect x="90" y="330" width="780" height="260" fill="{SAND}"/><path d="M90 330H870" stroke="{GOLD}" stroke-width="6"/>'
    arcos=''.join(arco_ferradura(130+i*60,380,60,210,G,'none',7) for i in range(12))
    nave=f'<rect x="380" y="230" width="200" height="360" fill="{G}"/><path d="M380 230L480 150L580 230Z" fill="{G2}"/><path d="M480 80V190M444 118H516" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/><path d="M420 590V420C420 380 540 380 540 420V590Z" fill="{IV}" opacity=".9"/></g>'
    torre=f'<g transform="translate(40 70)"><rect width="70" height="210" fill="{G}"/><rect x="-8" y="-24" width="86" height="28" fill="{GOLD}"/></g>'
    txt=T(480,630,'Séc. XIII · Fernando III',50,IV,800,'Lora')+T(480,680,'a Grande Mesquita vira catedral',34,IV,600)
    return fundo+bloco+arcos+nave+txt
def reel():
    S=[]
    S.append(rbv(f'''{Tv('A <span style="color:@AC;font-style:italic">Mezquita</span> de Córdoba e o centro histórico: Patrimônio Mundial',78)}
    {cardv(60,700,960,1040,G,cena_arcos(960,1040),0)}''',1,'ivory'))
    S.append(rbv(f'''{Tv('Inscrito pela <span style="color:@AC">UNESCO</span>',96)}
    {Pv('O Centro Histórico de Córdoba foi inscrito em 1984, com extensão em 1994. A zona central tem 80,28 hectares, e a UNESCO cita os critérios (i), (ii), (iii) e (iv).',500)}
    {cardv(60,1010,960,730,G,cena_mapa(960,730),0)}''',2,'green'))
    S.append(rbv(f'''{Tv('Uma cidade de <span style="color:@AC">mesquitas</span>',96)}
    {Pv('Segundo a UNESCO, a partir do século VIII, após a conquista moura, Córdoba teve seu período de maior prosperidade, com cerca de 300 mesquitas, palácios e edifícios públicos.',480)}
    {cardv(60,1030,960,710,SAND,cena_mesquitas(960,710),0)}''',3,'terra'))
    S.append(rbv(f'''{Tv('De mesquita a <span style="color:@AC">catedral</span>',96)}
    {Pv('No século XIII, sob Fernando III, a Grande Mesquita foi convertida em catedral. Foram erguidos o Alcázar de los Reyes Cristianos e a Torre de la Calahorra.',480)}
    {cardv(60,1030,960,710,TERRA,cena_catedral(960,710),0)}''',4,'ivory'))
    S.append(closing(1920,G,IV,GOLD,'Fonte: UNESCO, Centro Histórico de Córdoba (whc.unesco.org/es/list/313).<br>Consulta em 16/11/2026.',logo=460,serif_sz=88,top=.2))
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
