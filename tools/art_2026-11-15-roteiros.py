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

# ---- ícones carrossel 1 (ascendentes) ----
def ic_geracoes(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="42" cy="58" r="16" fill="{a}"/><path d="M22 150V96C22 78 62 78 62 96V150Z" fill="{a}"/><path d="M70 150V176" stroke="{b}" stroke-width="6" stroke-linecap="round"/><path d="M62 112H76V176" fill="none" stroke="{b}" stroke-width="6" stroke-linecap="round"/><circle cx="108" cy="42" r="19" fill="{a}"/><path d="M84 150V92C84 70 132 70 132 92V150Z" fill="{a}"/><circle cx="162" cy="92" r="14" fill="{b}"/><path d="M146 150V112C146 98 178 98 178 112V150Z" fill="{b}"/><path d="M14 168H186" stroke="{a}" stroke-width="8" stroke-linecap="round"/></svg>'''
def ic_casa_apoio(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M24 98L100 30L176 98V172H24Z" fill="{b}" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><path d="M100 148C60 120 66 90 84 90C94 90 100 98 100 98C100 98 106 90 116 90C134 90 140 120 100 148Z" fill="{a}"/><path d="M12 108L100 24L188 108" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_humano(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 72C64 46 70 12 90 12C98 12 100 22 100 22C100 22 102 12 110 12C130 12 136 46 100 72Z" fill="{b}" stroke="{a}" stroke-width="6" transform="translate(0,6)"/><path d="M14 126L52 112C66 108 80 112 92 120L124 120C136 120 138 138 124 140L90 142" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M90 142L128 138L168 112C178 106 188 116 180 126L128 176L66 178L14 160" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_casa_escudo(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M10 96L76 36L142 96V164H10Z" fill="{b}" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><rect x="58" y="116" width="36" height="48" fill="{a}"/><path d="M146 66L186 80V116C186 146 166 164 146 176C126 164 106 146 106 116V80Z" fill="{a}"/><path d="M128 120L142 134L166 104" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_laptop(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="38" y="34" width="124" height="94" rx="10" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M12 150H188L170 128H30Z" fill="{a}"/><circle cx="100" cy="82" r="26" fill="{a}"/><path d="M87 82L96 92L114 70" fill="none" stroke="{b}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M82 168H118" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'''
def ic_calendario(a,b):
    cells=''.join(f'<rect x="{34+i*34}" y="{92+j*30}" width="22" height="18" rx="3" fill="{a}"/>' for j in range(3) for i in range(4))
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="18" y="36" width="164" height="144" rx="14" fill="{b}" stroke="{a}" stroke-width="8"/><rect x="18" y="36" width="164" height="38" rx="12" fill="{a}"/><path d="M58 18V50M142 18V50" stroke="{b}" stroke-width="9" stroke-linecap="round"/>{cells}</svg>'''

# ---- ícones carrossel 2 (cartão de familiar UE) ----
def ic_aneis(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="72" cy="100" r="46" fill="none" stroke="{a}" stroke-width="14"/><circle cx="128" cy="100" r="46" fill="none" stroke="{b}" stroke-width="14"/><path d="M100 62A46 46 0 0 1 100 138A46 46 0 0 1 100 62Z" fill="{a}" opacity=".0"/><path d="M100 64A46 46 0 0 0 100 136" fill="none" stroke="{a}" stroke-width="14"/></svg>'''
def ic_vinculos(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="36" r="20" fill="{a}"/><circle cx="36" cy="132" r="20" fill="{a}"/><circle cx="164" cy="132" r="20" fill="{a}"/><path d="M100 60V104M100 104L48 118M100 104L152 118" stroke="{b}" stroke-width="8" stroke-linecap="round" fill="none"/><circle cx="100" cy="104" r="14" fill="{b}"/><path d="M20 176H180" stroke="{a}" stroke-width="8" stroke-linecap="round"/></svg>'''
def ic_trabalho(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="16" y="64" width="168" height="108" rx="14" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M70 64V46C70 38 76 34 84 34H116C124 34 130 38 130 46V64" fill="none" stroke="{a}" stroke-width="8"/><path d="M16 112H184" stroke="{a}" stroke-width="7"/><rect x="88" y="100" width="24" height="26" rx="5" fill="{a}"/></svg>'''
def ic_balcao(a,b):
    cols=''.join(f'<rect x="{44+i*34}" y="76" width="18" height="72" fill="{a}"/>' for i in range(4))
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 14L184 62H16Z" fill="{a}"/>{cols}<rect x="26" y="152" width="148" height="14" rx="3" fill="{a}"/><rect x="14" y="172" width="172" height="14" rx="3" fill="{b}" stroke="{a}" stroke-width="5"/><circle cx="100" cy="42" r="8" fill="{b}"/></svg>'''
def ic_cartao(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="14" y="40" width="172" height="120" rx="16" fill="{b}" stroke="{a}" stroke-width="8"/><rect x="32" y="64" width="34" height="26" rx="5" fill="{a}"/><circle cx="148" cy="76" r="20" fill="none" stroke="{a}" stroke-width="5"/><g fill="{a}">{''.join(f'<circle cx="{148+20*math.cos(k*math.pi/3):.1f}" cy="{76+20*math.sin(k*math.pi/3):.1f}" r="3.6"/>' for k in range(6))}</g><path d="M32 118H110M32 138H88" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'''

# ---- cenas ----
def pessoa(cx,base,s,col,tipo='adulto',bengala=None):
    if tipo=='crianca': h=60*s; r=13*s; bw=22*s
    elif tipo=='idoso': h=96*s; r=16*s; bw=32*s
    else: h=112*s; r=18*s; bw=36*s
    top=base-h
    out=f'<circle cx="{cx}" cy="{top+r}" r="{r}" fill="{col}"/><path d="M{cx-bw} {base}V{top+2*r+10*s}C{cx-bw} {top+r+6*s} {cx+bw} {top+r+6*s} {cx+bw} {top+2*r+10*s}V{base}Z" fill="{col}"/>'
    if bengala: out+=f'<path d="M{cx+bw+8*s} {base}V{top+2*r+34*s}Q{cx+bw+8*s} {top+2*r+20*s} {cx+bw+22*s} {top+2*r+20*s}" fill="none" stroke="{bengala}" stroke-width="{6*s}" stroke-linecap="round"/>'
    return out
def cena_familia(w,h,fg,ac,bg):
    base=h-46
    s=f'<circle cx="{w*.5}" cy="{h*.34}" r="{w*.2}" fill="{ac}" opacity=".9"/>'
    s+=f'<path d="M0 {base}H{w}V{h}H0Z" fill="{fg}" opacity=".18"/>'
    s+=pessoa(w*.2,base,2.3,fg,'idoso',ac)
    s+=pessoa(w*.34,base,2.2,fg,'idoso')
    s+=pessoa(w*.58,base,2.9,fg,'adulto')
    s+=pessoa(w*.76,base,2.5,fg,'crianca')
    return s

# ---- carrossel 1: ARCO ----
def arco(kick,title,body,icon_fn,theme,bs=46):
    th={'sand':(SAND,G,INK,G,TERRA,GOLD,IV),'green':(G,IV,IV,SAND,GOLD,GOLD,G),'terra':(TERRA,IV,IV,'#F3D79A','#F3D79A',IV,TERRA)}[theme]
    bg,hc,bc,archfill,acc,ring,ia=th
    # cores do ícone: dentro do arco
    if theme=='sand': ca,cb=IV,GOLD
    elif theme=='green': ca,cb=G,TERRA
    else: ca,cb=TERRA,G
    arch_w,arch_h,ax,ay=420,430,330,150
    inner=f'''{bracket(acc)}
    <div class=abs style="left:80px;right:300px;top:78px"><div class=kick style="color:{acc if theme!='sand' else TERRA}">{html.escape(kick)}</div></div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <path d="{arco_path(ax-26,ay-26,arch_w+52,arch_h+26)}" fill="none" stroke="{ring}" stroke-width="4"/>
      <path d="{arco_path(ax,ay,arch_w,arch_h)}" fill="{archfill}"/></svg>
    <div class=abs style="left:{ax+60}px;top:{ay+60}px;width:{arch_w-120}px;height:{arch_w-120}px">{icon_fn(ca,cb)}</div>
    <div class=abs style="left:80px;top:640px;width:920px">
      <div class=serif style="font-size:68px;line-height:1.08;font-weight:700;color:{hc}">{title}</div>
      <div style="width:130px;height:5px;background:{acc};margin:26px 0 28px"></div>
      <div style="font-size:{bs}px;line-height:1.38;color:{bc}">{body}</div></div>
    {foot(hc)}'''
    return page(1350,bg,inner)
def capa1():
    w,h,x,y=760,620,160,150
    inner=f'''{bracket(GOLD)}
    <div class=abs style="left:80px;top:70px"><div class=kick style="color:{GOLD}">Imigração · Residência</div></div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <path d="{arco_path(x-30,y-30,w+60,h+30)}" fill="none" stroke="{GOLD}" stroke-width="4"/>
      <path d="{arco_path(x,y,w,h)}" fill="{SAND}"/>
      <g transform="translate({x},{y})">{cena_familia(w,h,G,TERRA,SAND)}</g></svg>
    <div class="abs serif" style="left:80px;top:850px;width:920px;font-size:70px;line-height:1.08;font-weight:700;color:{IV}">Pai ou mãe de <span style="color:{GOLD};font-style:italic">espanhol</span> pode pedir residência na Espanha?</div>
    <div class=abs style="left:80px;top:1140px;font-size:34px;color:{SAND}">Deslize e veja o que a ficha oficial prevê</div>
    {foot(IV)}'''
    return page(1350,G,inner)

SL1=[capa1()]
SL1.append(arco('Quem entra','Os ascendentes','Os <b>ascendentes diretos de primeiro grau</b> de uma pessoa com nacionalidade espanhola, ou do cônjuge ou parceiro dela, nos casos que a ficha oficial prevê.',ic_geracoes,'sand'))
SL1.append(arco('Em que casos','Dois casos previstos','A ficha prevê dois casos: quando se comprova que <b>vivem a cargo</b> do familiar e <b>não têm apoio familiar</b> no país de origem, ou quando há <b>razões humanitárias</b>.',ic_humano,'green',46))
SL1.append(arco('Condições','Convivência e antecedentes','A ficha pede <b>convivência</b> com o familiar e <b>ausência de antecedentes penais</b> na Espanha e nos países onde a pessoa viveu nos últimos cinco anos.',ic_casa_escudo,'terra',46))
SL1.append(arco('Como pedir','Pela via telemática','A ficha prevê a <b>apresentação telemática</b>, pela sede eletrônica. Recomendamos fazer assim. Se tiver dúvida sobre o seu caso, <b>consulte um profissional</b>.',ic_laptop,'sand',46))
SL1.append(arco('Prazos e validade','Prazo e validade','A ficha prevê <b>dois meses</b> para a resolução. A autorização vale <b>cinco anos</b>, ou o período de residência previsto do familiar espanhol, se menor.',ic_calendario,'green',46))
SL1.append(closing(1350,SAND,G,TERRA,'Fonte: Ministerio de Inclusión (residência temporária de familiares de pessoas com nacionalidade espanhola), consulta em 15/11/2026.'))

# ---- carrossel 2: TRILHA ----
def trilha(idx,tot,kick,title,body,icon_fn,theme,bs=46):
    th={'green':(G,IV,IV,GOLD,GOLD),'ivory':(IV,G,INK,TERRA,TERRA),'terra':(TERRA,IV,IV,'#F3D79A','#F3D79A')}[theme]
    bg,hc,bc,kc,acc=th
    if theme=='green': ca,cb,bb=G,TERRA,GOLD
    elif theme=='ivory': ca,cb,bb=IV,GOLD,G
    else: ca,cb,bb=TERRA,G,IV
    ys=[190+i*200 for i in range(tot)]
    sp=f'<path d="M110 120V1240" stroke="{acc}" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round"/>'
    for i,y in enumerate(ys):
        if i<idx: sp+=f'<circle cx="110" cy="{y}" r="16" fill="{acc}"/>'
        elif i==idx: sp+=f'<circle cx="110" cy="{y}" r="30" fill="{bg}" stroke="{acc}" stroke-width="6"/><circle cx="110" cy="{y}" r="16" fill="{acc}"/>'
        else: sp+=f'<circle cx="110" cy="{y}" r="13" fill="none" stroke="{acc}" stroke-width="4"/>'
    inner=f'''{bracket(acc)}
    <svg class=abs style="left:0;top:0" width="1080" height="1350">{sp}</svg>
    <div class=abs style="left:210px;top:86px"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div>
    <div class=abs style="left:210px;top:150px;width:210px;height:210px">{badge(icon_fn(ca,cb),bb,ca,210)}</div>
    <div class=abs style="left:210px;top:400px;width:790px">
      <div class=serif style="font-size:68px;line-height:1.08;font-weight:700;color:{hc}">{title}</div>
      <div style="width:110px;height:5px;background:{acc};margin:24px 0 28px"></div>
      <div style="font-size:{bs}px;line-height:1.4;color:{bc}">{body}</div></div>
    {foot(hc)}'''
    return page(1350,bg,inner)
def capa2():
    stars=''.join(star(250+80*math.cos(k*math.pi/6-math.pi/2),420+80*math.sin(k*math.pi/6-math.pi/2),13,GOLD) for k in range(12))
    card=f'''<g transform="rotate(5 540 840)"><rect x="110" y="610" width="860" height="520" rx="34" fill="{SAND}" stroke="{G}" stroke-width="3"/></g>
    <g transform="rotate(-4 540 840)"><rect x="110" y="590" width="860" height="520" rx="34" fill="{G}"/>
      <rect x="150" y="630" width="780" height="440" rx="22" fill="none" stroke="{GOLD}" stroke-width="3"/>
      <g transform="translate(0,420)">{stars}</g>
      <circle cx="260" cy="840" r="52" fill="{G2}" stroke="{GOLD}" stroke-width="3"/>
      <rect x="170" y="1010" width="170" height="14" rx="7" fill="{GOLD}" opacity=".0"/>
      <rect x="430" y="700" width="440" height="22" rx="11" fill="{IV}" opacity=".9"/>
      <rect x="430" y="756" width="330" height="22" rx="11" fill="{IV}" opacity=".55"/>
      <rect x="430" y="812" width="390" height="22" rx="11" fill="{IV}" opacity=".55"/>
      <rect x="430" y="900" width="86" height="64" rx="12" fill="{GOLD}"/><path d="M430 932H516M473 900V964" stroke="{G}" stroke-width="3"/>
      <circle cx="280" cy="1000" r="0" fill="none"/>
      <path d="M180 996C200 960 232 960 252 996" fill="none" stroke="none"/>
    </g>'''
    inner=f'''{bracket(G2)}
    <div class=abs style="left:80px;top:90px"><div class=kick style="color:{TERRA}">Imigração · Residência</div></div>
    <div class="abs serif" style="left:80px;top:160px;width:920px;font-size:76px;line-height:1.06;font-weight:700;color:{G}">Familiar de <span style="color:{TERRA};font-style:italic">cidadão da UE</span>: como pedir o cartão de residência?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">{card}</svg>
    {foot(G)}'''
    return page(1350,IV,inner)
TOT=5
SL2=[capa2()]
SL2.append(trilha(0,TOT,'Quem é familiar','Quem é familiar','Familiar de cidadão <b>espanhol ou de outro país da UE</b>, do EEE ou da Suíça que não tenha essa nacionalidade e vá acompanhá-lo ou reunir-se com ele na Espanha por mais de três meses.',ic_aneis,'green',41))
SL2.append(trilha(1,TOT,'Quais vínculos','Quais vínculos','Cônjuge, parceiro registrado, descendentes e ascendentes, outros familiares <b>a cargo ou que convivam</b> com o cidadão, e parceiro de fato com <b>vínculo duradouro comprovado</b>.',ic_vinculos,'ivory',44))
SL2.append(trilha(2,TOT,'Condições do cidadão da UE','Condições do cidadão da UE','Trabalhar por conta alheia ou própria na Espanha, ou ter <b>recursos suficientes e seguro de saúde</b>. Estudante também pode, com seguro e recursos.',ic_trabalho,'terra',45))
SL2.append(trilha(3,TOT,'Onde e quando','Onde e quando','Pedido <b>presencial</b> na Oficina de Extranjería da província ou na Comisaría de Polícia, <b>em até três meses</b> desde a entrada na Espanha.',ic_balcao,'green',46))
SL2.append(trilha(4,TOT,'Prazo e validade','Prazo e validade','A ficha prevê <b>emissão em até três meses</b> após o pedido. O cartão vale <b>cinco anos</b>, ou o período previsto de residência do cidadão da UE, se menor.',ic_cartao,'ivory',45))
SL2.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión (cartão de residência de familiar de cidadão da UE), consulta em 15/11/2026.'))

async def render(lst,folder,prefix,h):
    os.makedirs(folder,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h})
        for i,htm in enumerate(lst):
            await pg.set_content(htm); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{folder}/{prefix}-{i+1}.png')
        await b.close()
R=os.environ.get('ART_OUT',B+'2026-11-15')
asyncio.run(render(SL1,R+'/roteiro-1-ascendentes','ascendentes',1350))
asyncio.run(render(SL2,R+'/roteiro-2-cartao-ue','cartao-ue',1350))
