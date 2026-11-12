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

# ---- ícones NOTÍCIA (tribunal / lei) ----
def ic_court(a,b):
    cols=''.join(f'<rect x="{x}" y="76" width="16" height="70" fill="{a}"/>' for x in (48,76,104,136))
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M24 70L100 22L176 70Z" fill="{a}"/>{cols}<rect x="30" y="146" width="140" height="14" fill="{a}"/><rect x="20" y="164" width="160" height="14" fill="{a}"/></svg>'
def ic_house_key(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M22 96L100 28L178 96V170H22Z" fill="{a}"/><rect x="82" y="116" width="36" height="54" fill="{b}"/><circle cx="148" cy="64" r="16" fill="{b}"/><path d="M148 80V104M148 94H160M148 104H158" stroke="{b}" stroke-width="7" stroke-linecap="round"/></svg>'
def ic_years(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="26" y="34" width="148" height="140" rx="14" fill="{b}" stroke="{a}" stroke-width="7"/><rect x="26" y="34" width="148" height="34" rx="12" fill="{a}"/><text x="100" y="140" text-anchor="middle" font-family="Lora" font-weight="700" font-size="52" fill="{a}">5·10·15</text><circle cx="60" cy="24" r="7" fill="{a}"/><circle cx="140" cy="24" r="7" fill="{a}"/></svg>'
def ic_scales(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 24V170M60 172H140" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M34 62H166" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M34 62L14 112H54Z M166 62L146 112H186Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M14 112C14 130 54 130 54 112M146 112C146 130 186 130 186 112" fill="{a}"/><circle cx="100" cy="22" r="9" fill="{a}"/></svg>'
def ic_hourglass(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M46 20H154M46 180H154" stroke="{a}" stroke-width="12" stroke-linecap="round"/><path d="M58 20C58 84 100 84 100 100C100 116 58 116 58 180H142C142 116 100 116 100 100C100 84 142 84 142 20Z" fill="{b}" stroke="{a}" stroke-width="7" stroke-linejoin="round"/><path d="M76 168C84 146 116 146 124 168Z" fill="{a}"/><path d="M100 100V140" stroke="{a}" stroke-width="5"/></svg>'

# ---- ícones IMIGRAÇÃO (conta própria) ----
def ic_consulate(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="36" y="74" width="128" height="96" fill="{a}"/><path d="M26 74L100 34L174 74Z" fill="{a}"/><rect x="86" y="118" width="28" height="52" fill="{b}"/><rect x="50" y="94" width="22" height="26" fill="{b}"/><rect x="128" y="94" width="22" height="26" fill="{b}"/><path d="M100 34V8" stroke="{a}" stroke-width="5"/><path d="M100 8H134V26H100Z" fill="{b}" stroke="{a}" stroke-width="3"/></svg>'
def ic_record(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="16" width="120" height="156" rx="10" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M62 52H138M62 76H138M62 100H108" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="132" cy="140" r="26" fill="{a}"/><path d="M119 140L129 151L147 128" fill="none" stroke="{b}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_shop(a,b):
    st=''.join(f'<path d="M{20+i*32} 52H{52+i*32}L{46+i*32} 88H{26+i*32}Z" fill="{a if i%2==0 else b}" stroke="{a}" stroke-width="4"/>' for i in range(5))
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M12 52L28 22H172L188 52Z" fill="{a}"/>{st}<rect x="30" y="92" width="140" height="80" fill="{a}"/><rect x="46" y="108" width="52" height="64" fill="{b}"/><rect x="112" y="108" width="42" height="34" fill="{b}"/></svg>'
def ic_invest(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><ellipse cx="100" cy="164" rx="62" ry="14" fill="{a}"/><ellipse cx="100" cy="148" rx="62" ry="14" fill="{b}" stroke="{a}" stroke-width="5"/><ellipse cx="100" cy="132" rx="62" ry="14" fill="{a}"/><path d="M100 124V70" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M100 86C100 44 62 38 44 46C44 80 70 94 100 86Z" fill="{a}"/><path d="M100 70C100 34 134 22 158 30C158 64 130 80 100 70Z" fill="{b}" stroke="{a}" stroke-width="5"/></svg>'
def ic_cal3(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="26" y="34" width="148" height="140" rx="14" fill="{b}" stroke="{a}" stroke-width="7"/><rect x="26" y="34" width="148" height="34" rx="12" fill="{a}"/><text x="100" y="134" text-anchor="middle" font-family="Lora" font-weight="700" font-size="76" fill="{a}">3</text><text x="100" y="162" text-anchor="middle" font-family="Inter" font-weight="800" font-size="20" letter-spacing="3" fill="{a}">MESES</text><circle cx="60" cy="24" r="7" fill="{a}"/><circle cx="140" cy="24" r="7" fill="{a}"/></svg>'

T=6
# ---------- NOTÍCIA (capa marfim, tribunal + balança) ----------
def tribunal_cover():
    cols=''.join(f'<rect x="{x}" y="640" width="64" height="360" fill="{G}"/><rect x="{x-10}" y="620" width="84" height="26" fill="{G2}"/><rect x="{x-10}" y="994" width="84" height="26" fill="{G2}"/>' for x in (220,326,432,538,644))
    return page(1350,IV,f'''{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Notícia · Tribunal Constitucional</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:78px;line-height:1.06;font-weight:700;color:{G}">Governo recorre ao Constitucional contra a <span style="color:{TERRA};font-style:italic">“prioridad nacional”</span> valenciana</div>
    <svg class=abs style="left:0;top:70px" width="1080" height="1350"><path d="M170 640L540 470L910 640Z" fill="{G}"/><path d="M250 628L540 500L830 628Z" fill="{GOLD}" opacity=".9"/>{cols}
    <rect x="190" y="1020" width="700" height="26" fill="{G}"/><rect x="160" y="1046" width="760" height="26" fill="{G2}"/>
    <g transform="translate(540 790)"><circle cx="0" cy="-14" r="64" fill="{IV}"/><path d="M0-66V70M-34 74H34" stroke="{G}" stroke-width="7" stroke-linecap="round"/><path d="M-56-30H56" stroke="{G}" stroke-width="7" stroke-linecap="round"/><path d="M-56-30L-76 14H-36Z M56-30L36 14H76Z" fill="{GOLD}" stroke="{G}" stroke-width="4" stroke-linejoin="round"/></g></svg>
    {foot(G)}''')
NOT=[tribunal_cover()]
NOT.append(content2('Notícia · O que foi decidido','O recurso aprovado em 10/11','O Conselho de Ministros acordou apresentar um <b>recurso de inconstitucionalidade</b> contra preceitos da Lei 5/2026 da Generalitat Valenciana, segundo a referência oficial da Moncloa.',ic_court,'green'))
NOT.append(content2('Notícia · O ponto sobre residência','Habitação e renda de inclusão','A referência cita a “prioridad nacional” no acesso à <b>habitação protegida</b> e à renta valenciana de inclusão, com períodos de residência ou empadronamiento de 5, 10 ou 15 anos.',ic_house_key,'ivory'))
NOT.append(content2('Notícia · Os fundamentos','Lei de Estrangeiros e UE','O recurso invoca a Lei Orgânica 4/2000 e a jurisprudência da UE sobre <b>residentes de longa duração</b>, segundo a referência do Conselho de Ministros.',ic_scales,'terra'))
NOT.append(content2('Notícia · O que vem agora','Quem decide é o Tribunal','Cabe ao <b>Tribunal Constitucional</b> analisar o recurso. As fontes consultadas não detalham efeitos imediatos nem prazos. Quem vive na região deve acompanhar os canais oficiais.',ic_hourglass,'green'))
NOT.append(closing(1350,G,IV,GOLD,'Fontes: La Moncloa, Referência do Conselho de Ministros de 10/11/2026; The Objective (10/11/2026).<br>Consulta em 12/11/2026.'))

# ---------- IMIGRAÇÃO (capa terracota, loja) ----------
def loja_cover():
    return page(1350,TERRA,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 30% 75%,#C96A49 0,{TERRA} 70%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:78px;line-height:1.06;font-weight:700;color:{IV}">Como funciona a autorização de residência e trabalho <span style="color:#F3D79A;font-style:italic">por conta própria</span>?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350"><rect x="170" y="760" width="740" height="420" fill="{IV}"/>
    {''.join(f'<path d="M{150+i*76} 640H{226+i*76}L{216+i*76} 760H{160+i*76}Z" fill="{G if i%2==0 else IV}" stroke="{G}" stroke-width="5"/>' for i in range(10))}
    <path d="M130 640L170 560H910L950 640Z" fill="{G}"/><rect x="160" y="1180" width="760" height="24" fill="{G2}"/>
    <rect x="230" y="830" width="260" height="350" fill="{G}"/><circle cx="460" cy="1010" r="11" fill="{GOLD}"/>
    <rect x="560" y="830" width="290" height="190" fill="{SAND}" stroke="{G}" stroke-width="8"/><path d="M560 925H850M705 830V1020" stroke="{G}" stroke-width="5"/>
    <g transform="translate(700 1110)"><rect x="-90" y="-46" width="180" height="62" rx="8" fill="{GOLD}"/><text x="0" y="-4" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="4" fill="{G}">ABERTO</text></g>
    <g transform="rotate(14 900 700)"><circle cx="900" cy="700" r="76" fill="{GOLD}"/><circle cx="900" cy="700" r="60" fill="none" stroke="{G}" stroke-width="4" stroke-dasharray="3 9"/><path d="M868 704L892 730L934 672" fill="none" stroke="{G}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/></g></svg>
    {foot(IV)}''')
IMG=[loja_cover()]
IMG.append(content2('Imigração · Para quem é','Quem pode pedir','A autorização é para pessoa estrangeira <b>não residente</b> na Espanha que quer exercer atividade por conta própria. O pedido é pessoal, no consulado espanhol correspondente.',ic_consulate,'green'))
IMG.append(content2('Imigração · Requisitos gerais','Situação e antecedentes','Não estar em situação irregular na Espanha, não ter antecedentes penais na Espanha nem onde viveu nos últimos cinco anos e não representar ameaça à ordem pública.',ic_record,'ivory'))
IMG.append(content2('Imigração · A atividade','Exigências do negócio','Cumprir os requisitos que a lei exige dos espanhóis para abrir e operar a atividade, ter a <b>qualificação profissional</b> exigível e, se for o caso, inscrição em ordem profissional.',ic_shop,'green'))
IMG.append(content2('Imigração · O investimento','Investimento e emprego','Comprovar que o <b>investimento previsto é suficiente</b> e, se for o caso, o efeito na criação de emprego. A ficha cita relatório de associações de autônomos como meio possível.',ic_invest,'terra'))
IMG.append(content2('Imigração · Prazos da ficha oficial','Prazos e validade','A ficha oficial prevê resolução em <b>três meses</b>. Depois, um mês para pedir o visto, que a missão prevê decidir em um mês. A autorização vale um ano.',ic_cal3,'ivory'))
IMG.append(closing(1350,G2,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 14 (atualizada em maio de 2025).<br>Consulta em 12/11/2026.'))

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
def herradura(cx,top,w,h,col,sw=0):
    # arco de ferradura: abertura circular que se fecha na base
    r=w/2
    return f'<path d="M{cx-r*0.78} {top+h}L{cx-r*0.78} {top+r*1.5}A{r} {r} 0 1 1 {cx+r*0.78} {top+r*1.5}L{cx+r*0.78} {top+h}Z" fill="{col}"/>'
def estrela8(cx,cy,r,col,op=1):
    pts=[]
    for i in range(16):
        rr=r if i%2==0 else r*0.58
        a=math.pi*i/8-math.pi/2
        pts.append(f'{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{col}" opacity="{op}"/>'
def torre(x,base,w,h,col,gold=False):
    cren=''.join(f'<rect x="{x+i*w/5:.1f}" y="{base-h-16}" width="{w/5-6:.1f}" height="18" fill="{col}"/>' for i in range(0,5,2))
    return f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{col}"/>{cren}<rect x="{x+w*0.4:.1f}" y="{base-h*0.7:.1f}" width="{w*0.2:.1f}" height="{h*0.2:.1f}" rx="6" fill="{G}"/>'
def cena_colina(w,h):
    stars=''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{IV}"/>' for x,y,r in [(90,70,4),(250,130,3),(470,60,4),(700,110,3),(860,70,4),(900,190,3)])
    sierra=f'<path d="M0 330L120 210L210 290L330 170L470 300L590 200L720 310L840 190L{w} 300V{h}H0Z" fill="{G}" opacity=".9"/><path d="M330 170L300 210L335 200L360 215Z M840 190L815 225L845 215L870 232Z" fill="{IV}" opacity=".85"/>'
    colina=f'<path d="M-20 {h}V560C100 470 240 440 480 430C720 440 860 470 {w+20} 560V{h}Z" fill="{TERRA}"/>'
    muro=f'<rect x="150" y="410" width="660" height="60" fill="{SAND}"/>'+''.join(f'<rect x="{150+i*44}" y="388" width="26" height="26" fill="{SAND}"/>' for i in range(15))
    torres=torre(190,415,90,160,SAND)+torre(430,415,100,220,SAND)+torre(690,415,80,150,SAND)
    arco=herradura(480,470,150,110,G)
    luna=f'<circle cx="780" cy="110" r="46" fill="{SAND}"/><circle cx="800" cy="98" r="42" fill="{G2}"/>'
    cip=''.join(f'<path d="M{x} {y}C{x-26} {y-70} {x-14} {y-150} {x} {y-190}C{x+14} {y-150} {x+26} {y-70} {x} {y}Z" fill="{G}"/>' for x,y in [(120,760),(240,830),(360,780),(600,790),(720,840),(840,770),(480,900),(180,1000),(780,1010),(480,1090)])
    terr=''.join(f'<path d="M-20 {y}C200 {y-40} 760 {y-40} {w+20} {y}" fill="none" stroke="{GOLD}" stroke-width="3" opacity=".55"/>' for y in (640,720,800,880,960,1040,1120))
    return stars+luna+sierra+colina+terr+cip+muro+torres+arco+estrela8(480,300,34,GOLD)
def cena_1238(w,h):
    # ruínas -> sede da corte
    ruinas=f'<path d="M30 600H430" stroke="{SAND}" stroke-width="8"/><rect x="60" y="520" width="70" height="80" fill="{SAND}"/><rect x="150" y="470" width="60" height="130" fill="{SAND}"/><path d="M230 600V540L260 520L290 560L320 520V600Z" fill="{SAND}"/><rect x="340" y="540" width="80" height="60" fill="{SAND}"/>'
    seta=f'<path d="M455 520H505M485 496L511 520L485 544" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    novo=f'<path d="M540 600H930" stroke="{SAND}" stroke-width="8"/>'+torre(560,600,90,140,TERRA)+torre(680,600,110,190,TERRA)+torre(820,600,90,150,TERRA)
    txt=f'<text x="480" y="250" text-anchor="middle" font-family="Lora" font-weight="700" font-size="240" fill="{GOLD}">1238</text><text x="480" y="310" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="6" fill="{IV}">AL-AHMAR · DINASTIA NAZARÍ</text>'
    lab=f'<text x="230" y="660" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" letter-spacing="4" fill="{IV}">RUÍNAS</text><text x="735" y="660" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" letter-spacing="4" fill="{IV}">SEDE DA CORTE</text>'
    return txt+ruinas+seta+novo+lab
def cena_dois_tempos(w,h):
    # arco de ferradura (nazarí) x arco de meio ponto + círculo (renascença)
    esq=herradura(250,120,300,470,TERRA)+f'<path d="M205 590V400A45 45 0 1 1 295 400V590Z" fill="{G2}"/>'+estrela8(250,92,34,GOLD)
    dir_=f'<path d="M580 590V300A140 140 0 0 1 860 300V590Z" fill="{SAND}"/><path d="M630 590V310A90 90 0 0 1 810 310V590Z" fill="{G2}"/><circle cx="720" cy="120" r="46" fill="none" stroke="{GOLD}" stroke-width="10"/><circle cx="720" cy="120" r="10" fill="{GOLD}"/>'
    lab=f'<text x="250" y="652" text-anchor="middle" font-family="Lora" font-weight="700" font-size="54" fill="{GOLD}">Séc. XIV</text><text x="250" y="690" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="3" fill="{IV}">ESPLENDOR NAZARÍ</text><text x="720" y="652" text-anchor="middle" font-family="Lora" font-weight="700" font-size="54" fill="{GOLD}">1526</text><text x="720" y="690" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="3" fill="{IV}">PALÁCIO DE CARLOS V</text>'
    return esq+dir_+lab
def cena_selo(w,h):
    return (f'<defs><path id="alh" d="M480 300m-230 0a230 230 0 1 1 460 0a230 230 0 1 1 -460 0"/></defs>'
      f'<circle cx="480" cy="300" r="270" fill="none" stroke="{TERRA}" stroke-width="8"/><circle cx="480" cy="300" r="252" fill="none" stroke="{TERRA}" stroke-width="3"/>'
      f'{estrela8(480,300,200,G)}'
      f'<text font-family="Inter" font-weight="800" font-size="30" fill="{TERRA}"><textPath href="#alh" textLength="1400" lengthAdjust="spacing">PATRIMÔNIO MUNDIAL · UNESCO · PATRIMÔNIO MUNDIAL · UNESCO ·</textPath></text>'
      f'<text x="480" y="326" text-anchor="middle" font-family="Lora" font-weight="700" font-size="112" fill="{GOLD}">1984</text>'
      f'<text x="480" y="372" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="4" fill="{IV}">INSCRIÇÃO</text>'
      f'<path d="M480 586V636" stroke="{G}" stroke-width="6"/><circle cx="480" cy="648" r="10" fill="{TERRA}"/>'
      f'<rect x="170" y="668" width="620" height="76" rx="38" fill="{G}"/><text x="480" y="718" text-anchor="middle" font-family="Lora" font-weight="700" font-size="44" fill="{GOLD}">1994 · inclui o Albaicín</text>')
def reel():
    S=[]
    S.append(rbv(f'''{Tv('A <span style="color:@AC;font-style:italic">cidade-palácio</span> de uma dinastia, em Granada',86)}
    {cardv(60,560,960,1180,G2,cena_colina(960,1180))}''',1,'green'))
    S.append(rbv(f'''{Tv('Tudo começa em <span style="color:@AC">1238</span>',92)}
    {Pv('Segundo o Patronato da Alhambra, Al-Ahmar, fundador da dinastia nazarí, viu as ruínas da colina e decidiu reconstruí-la como sede da corte.',470)}
    {cardv(60,820,960,880,G,cena_1238(960,700),90)}''',2,'ivory'))
    S.append(rbv(f'''{Tv('Esplendor no <span style="color:@AC">século XIV</span>',88)}
    {Pv('Com Yusuf I (1333–1354) e Muhammad V (1362–1391). Depois de 1492 virou Casa Real, e Carlos V decidiu o palácio renascentista em 1526.',470)}
    {cardv(60,820,960,880,G,cena_dois_tempos(960,700),90)}''',3,'terra').replace(f'background:{G};',f'background:{G};'))
    S.append(rbv(f'''{Tv('Patrimônio Mundial desde <span style="color:@AC">1984</span>',86)}
    {Pv('A UNESCO inscreveu Alhambra e Generalife em 1984. Em 1994, a inscrição foi ampliada e passou a incluir o bairro do Albaicín.',470)}
    {cardv(60,820,960,880,SAND,cena_selo(960,700),40)}''',4,'green'))
    S.append(closing(1920,G2,IV,GOLD,'Fontes: Patronato da Alhambra e Generalife (história); UNESCO (decisões 8COM 1984 e 18COM 1994).<br>Consulta em 12/11/2026.',logo=460,serif_sz=88,top=.2))
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
