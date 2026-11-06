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
def content(n,tot,kick,title,body,icon_fn,theme,numtxt=None,bs=42):
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
      <div style="font-size:{bs}px;line-height:1.42;color:{bc};font-weight:400">{body}</div></div>
    {arc}{foot(fc,n,tot)}'''
    return page(1350,bg,inner)

def closing(h,bg,fg,acc,srcs,logo=360,serif_sz=70,pad=80,top=.12):
    inner=f'''{bracket(acc)}
    <div class=abs style="left:0;right:0;top:{int(h*top)}px;display:flex;justify-content:center"><img src="{LOGO}" width="{logo}" height="{logo}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60}px;text-align:center;font-size:{serif_sz}px;line-height:1.14;font-weight:700;color:{fg}">Aqui você fica por dentro de tudo sobre a Espanha</div>
    <div class=abs style="left:50%;margin-left:-65px;top:{int(h*top)+logo+60+serif_sz*3+50}px;width:130px;height:5px;background:{acc}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3+90}px;text-align:center;font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
    <div class=abs style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3+170}px;text-align:center;font-size:40px;color:{fg}">Siga <b>@espanhasemsegredo</b></div>
    <div class=abs style="left:{pad+20}px;right:{pad+20}px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg};opacity:.85">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>'''
    return page(h,bg,inner)


# ================= ÍCONES NOVOS (2026-11-06) =================
def ic_cal(a,b):
    g=''.join(f'<rect x="{44+c*22}" y="{84+r*20}" width="14" height="12" rx="2" fill="{a}" opacity="{1 if (r*5+c)<9 else .35}"/>' for r in range(4) for c in range(6))
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="26" y="40" width="148" height="140" rx="14" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M26 54Q26 40 40 40H160Q174 40 174 54V76H26Z" fill="{a}"/><rect x="62" y="24" width="10" height="30" rx="5" fill="{a}" stroke="{b}" stroke-width="3"/><rect x="128" y="24" width="10" height="30" rx="5" fill="{a}" stroke="{b}" stroke-width="3"/>{g}</svg>'
def ic_calplus(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="22" y="38" width="130" height="132" rx="14" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M22 52Q22 38 36 38H138Q152 38 152 52V70H22Z" fill="{a}"/><rect x="54" y="22" width="10" height="28" rx="5" fill="{a}"/><rect x="110" y="22" width="10" height="28" rx="5" fill="{a}"/><path d="M44 112H112M44 138H92" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="148" cy="144" r="38" fill="{a}"/><path d="M148 124V164M128 144H168" stroke="{b}" stroke-width="12" stroke-linecap="round"/></svg>'
def ic_balance(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 24V164M62 172H138" stroke="{a}" stroke-width="10" stroke-linecap="round"/><path d="M34 62H166" stroke="{a}" stroke-width="8" stroke-linecap="round"/><circle cx="100" cy="30" r="12" fill="{a}"/><path d="M34 62L10 114H58Z M166 62L142 114H190Z" fill="none" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><path d="M10 114Q34 142 58 114ZM142 114Q166 142 190 114Z" fill="{a}"/></svg>'
def ic_keyclock(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="70" cy="76" r="44" fill="{a}"/><circle cx="70" cy="76" r="16" fill="{b}"/><path d="M98 108L172 182M146 156L166 136M128 138L146 120" stroke="{a}" stroke-width="14" stroke-linecap="round" fill="none"/><circle cx="148" cy="52" r="34" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M148 32V54L164 64" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_exit(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M40 24H124V176H40Z" fill="{a}"/><path d="M124 40L160 56V176H124" fill="{a}" opacity=".55"/><circle cx="108" cy="102" r="7" fill="{b}"/><path d="M10 150H70M150 112H196M174 90L198 112L174 134" stroke="{b}" stroke-width="0" fill="none"/><path d="M130 100H186M166 80L190 100L166 120" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><text x="62" y="76" font-family="Inter" font-weight="800" font-size="30" fill="{b}">72h</text></svg>'

def suitcase(col,acc,fill):
    return f'<svg width="330" height="300" viewBox="0 0 330 300"><path d="M115 70V46C115 30 125 22 140 22H190C205 22 215 30 215 46V70" fill="none" stroke="{col}" stroke-width="12"/><rect x="20" y="70" width="290" height="190" rx="26" fill="{fill}" stroke="{col}" stroke-width="8"/><path d="M110 70V260M220 70V260" stroke="{col}" stroke-width="6"/><rect x="146" y="150" width="38" height="30" rx="6" fill="{acc}"/><rect x="40" y="262" width="34" height="18" rx="6" fill="{col}"/><rect x="256" y="262" width="34" height="18" rx="6" fill="{col}"/></svg>'
def bigcal():
    cells=''
    for r in range(5):
        for c in range(7):
            x=40+c*74; y=150+r*72; i=r*7+c
            op=.9 if i<19 else .25
            cells+=f'<rect x="{x}" y="{y}" width="58" height="54" rx="9" fill="{G}" opacity="{.16 if i>=19 else .9}"/>'
            if i<19: cells+=f'<path d="M{x+14} {y+28}L{x+25} {y+40}L{x+45} {y+14}" fill="none" stroke="{IV}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'<svg width="580" height="540" viewBox="0 0 580 540"><rect x="6" y="6" width="568" height="528" rx="30" fill="{IV}" stroke="{G}" stroke-width="8"/><path d="M6 40Q6 6 40 6H540Q574 6 574 40V110H6Z" fill="{TERRA}"/><rect x="120" y="-14" width="22" height="64" rx="11" fill="{G}"/><rect x="438" y="-14" width="22" height="64" rx="11" fill="{G}"/><text x="290" y="82" text-anchor="middle" font-family="Lora" font-weight="700" font-size="46" fill="{IV}" letter-spacing="4">90 DIAS / SEMESTRE</text>{cells}</svg>'

def cover_imig():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{IV} 0%,{SAND} 100%)"></div>
    <div class=abs style="left:-140px;top:700px;width:600px;height:600px;border-radius:50%;background:{GOLD};opacity:.25"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Estância</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:700px;font-size:104px;line-height:1.04;font-weight:700;color:{G}">Entrei como <span style="color:{TERRA};font-style:italic">turista</span>: o que posso pedir aqui?</div>
    <div class=abs style="left:420px;top:640px;transform:rotate(4deg)">{bigcal()}</div>
    <div class=abs style="left:70px;top:900px;transform:rotate(-7deg)">{suitcase(G,GOLD,G2)}</div>
    
    <div class=abs style="left:0;right:0;bottom:0;height:150px;background:{G}"></div>
    <div class=foot style="bottom:40px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,IV,inner)

IMIG=[cover_imig()]
T=7
IMIG.append(content(2,T,'Estância curta','Estância de curta duração','Dura <b>até 90 dias por semestre</b>, contados desde a primeira entrada na Espanha.',ic_cal,'ivory',bs=56))
IMIG.append(content(3,T,'Depois dos 90 dias','Para seguir no país','É preciso uma <b>prórroga de estância</b> ou uma <b>autorização de residência</b>.',ic_calplus,'terra',bs=56))
IMIG.append(content(4,T,'Prórroga','Só em casos excepcionais','Quem entrou sem visto só fica além de 3 meses por razões <b>humanitárias, familiares, de atenção sanitária, de interesse público</b> ou outra excepcional.',ic_balance,'green',bs=56))
IMIG.append(content(5,T,'Residência','Cada autorização, seus requisitos','Exemplo: as regras do <b>arraigo</b> exigem pelo menos <b>2 anos</b> de permanência continuada na Espanha.',ic_keyclock,'ivory',bs=56))
IMIG.append(content(6,T,'Prórroga negada','Prazo de saída','A resolução fixa o prazo para sair, de <b>no máximo 72 horas</b>. Se a estância inicial ainda não acabou, a saída é até o seu fim.',ic_exit,'terra',bs=56))
IMIG.append(closing(1350,G,IV,GOLD,'Fontes: Ministerio del Interior (Estancia de corta duración) e Ministerio de Inclusión (Hoja 28).<br>Consulta em 06/11/2026.'))

# ================= REEL CASTANHA (1080x1920) =================
import math
def nut(cx,cy,s=1,fill=TERRA,tuft=INK,hl=GOLD):
    return f'<g transform="translate({cx} {cy}) scale({s})"><path d="M-60 12C-60 -38 -26 -72 0 -72C26 -72 60 -38 60 12C60 52 30 72 0 72C-30 72 -60 52 -60 12Z" fill="{fill}"/><path d="M-56 -4C-52 -36 -30 -62 -2 -66" fill="none" stroke="{hl}" stroke-width="7" stroke-linecap="round" opacity=".8"/><path d="M-34 60Q0 78 34 60Q20 38 0 38Q-20 38 -34 60Z" fill="{SAND}"/><path d="M-10 -72Q0 -90 10 -72Z" fill="{tuft}"/></g>'
def burr(cx,cy,r,body,spike,n=28):
    s=''
    for i in range(n):
        a=2*math.pi*i/n
        x1,y1=cx+math.cos(a)*r*.82,cy+math.sin(a)*r*.82
        x2,y2=cx+math.cos(a)*r*1.18,cy+math.sin(a)*r*1.18
        s+=f'<path d="M{x1:.0f} {y1:.0f}L{x2:.0f} {y2:.0f}" stroke="{spike}" stroke-width="9" stroke-linecap="round"/>'
    return s+f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{body}"/>'
def halfburr(cx,cy,r,body,spike,n=14):
    s=''
    for i in range(n+1):
        a=math.pi*i/n
        x1,y1=cx+math.cos(a)*r*.85,cy+math.sin(a)*r*.85
        x2,y2=cx+math.cos(a)*r*1.2,cy+math.sin(a)*r*1.2
        s+=f'<path d="M{x1:.0f} {y1:.0f}L{x2:.0f} {y2:.0f}" stroke="{spike}" stroke-width="10" stroke-linecap="round"/>'
    return s+f'<path d="M{cx-r} {cy}A{r} {r} 0 0 0 {cx+r} {cy}Z" fill="{body}"/><path d="M{cx-r+20} {cy}A{r-20} {r-20} 0 0 0 {cx+r-20} {cy}Z" fill="{spike}" opacity=".35"/>'
def svgfull(inner,h=1920): return f'<svg class=abs style="left:0;top:0" width="1080" height="{h}" viewBox="0 0 1080 {h}">{inner}</svg>'

# ícones das festas (viewBox 220)
def i_fogueira(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 220 220"><path d="M40 190L180 160M40 160L180 190" stroke="{a}" stroke-width="16" stroke-linecap="round"/><path d="M110 164C60 150 70 100 96 78C96 100 112 100 112 82C130 60 118 36 112 22C160 50 170 120 138 150C150 120 128 118 128 134C128 148 110 150 110 164Z" fill="{a}"/><path d="M110 164C90 156 92 132 108 120C110 134 124 136 124 150C124 158 118 162 110 164Z" fill="{b}"/>{nut(52,128,.28,b,a,a)}{nut(176,132,.26,b,a,a)}</svg>'
def i_sidra(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 220 220"><path d="M62 24H158L148 180Q146 198 128 198H92Q74 198 72 180Z" fill="none" stroke="{a}" stroke-width="9" stroke-linejoin="round"/><path d="M68 80H152L146 178Q144 190 130 190H90Q76 190 74 178Z" fill="{b}"/><g fill="{a}" opacity=".85"><circle cx="96" cy="150" r="6"/><circle cx="118" cy="128" r="5"/><circle cx="106" cy="104" r="4"/><circle cx="130" cy="160" r="5"/></g><path d="M62 80Q110 66 158 80" fill="none" stroke="{a}" stroke-width="6" opacity=".6"/>{nut(172,176,.3,a,a,b)}</svg>'
def i_panellets(a,b):
    d=''.join(f'<circle cx="{x}" cy="{y}" r="36" fill="{b}" stroke="{a}" stroke-width="6"/>'+''.join(f'<path d="M{x+dx} {y+dy}l9 4l-9 4z" fill="{a}"/>' for dx,dy in((-16,-12),(6,-18),(-6,4),(14,2),(-20,12),(4,18))) for x,y in((78,92),(142,92),(110,142)))
    return f'<svg width="100%" height="100%" viewBox="0 0 220 220"><ellipse cx="110" cy="150" rx="100" ry="46" fill="{a}" opacity=".35"/><ellipse cx="110" cy="136" rx="100" ry="46" fill="none" stroke="{a}" stroke-width="7"/>{d}</svg>'
def i_cartucho(a,b):
    nuts=''.join(nut(x,y,.3,b,a,a) for x,y in((78,56),(110,44),(142,56),(94,82),(126,82)))
    return f'<svg width="100%" height="100%" viewBox="0 0 220 220">{nuts}<path d="M52 66L168 66L128 204Q110 214 92 204Z" fill="{a}"/><path d="M60 100L160 100M70 134L150 134" stroke="{b}" stroke-width="5" opacity=".55"/><path d="M52 66Q110 90 168 66" fill="none" stroke="{b}" stroke-width="6"/></svg>'
def i_cesta(a,b):
    nuts=''.join(nut(x,y,.3,b,a,a) for x,y in((70,84),(106,72),(142,84),(88,100),(124,100),(160,100)))
    w=''.join(f'<path d="M{x} 108V190" stroke="{b}" stroke-width="5" opacity=".6"/>' for x in range(70,160,24))
    return f'<svg width="100%" height="100%" viewBox="0 0 220 220">{nuts}<path d="M32 108H188L170 190Q166 202 152 202H68Q54 202 50 190Z" fill="{a}"/>{w}<path d="M32 108H188" stroke="{b}" stroke-width="8"/><path d="M52 108C52 40 168 40 168 108" fill="none" stroke="{a}" stroke-width="10"/></svg>'

def reel(bg,inner,n,fg=IV,acc=GOLD,pattern=True):
    pat=f'<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(135deg,rgba(201,162,74,.07) 0 2px,transparent 2px 42px)"></div>' if pattern else ''
    return page(1920,bg,f'''{pat}{bracket(acc)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{acc}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{acc}">Espanha Sem Segredo</span></div><span class=c style="color:{acc}">{n} / 5</span></div>''')

def row(top,icon,reg,name,sub,bgc,fg,acc,ic_a,ic_b,h=400):
    return f'''<div class=abs style="left:60px;right:60px;top:{top}px;height:{h}px;border-radius:28px;background:{bgc};border:3px solid {acc}"></div>
    <div class=abs style="left:90px;top:{top+(h-250)//2}px;width:250px;height:250px">{icon(ic_a,ic_b)}</div>
    <div class=abs style="left:380px;right:90px;top:{top+(h-250)//2-10}px">
      <div class=kick style="color:{acc};font-size:26px">{reg}</div>
      <div class=serif style="font-size:78px;line-height:1.05;font-weight:700;color:{fg};margin:8px 0 12px">{name}</div>
      <div style="font-size:34px;line-height:1.35;color:{fg};opacity:.92">{sub}</div></div>'''

CAS=[]
# tela 1 - capa (verde, burrinho aberto com castanhas)
cv=svgfull(f'<circle cx="840" cy="1050" r="420" fill="{GOLD}" opacity=".16"/>'
  +halfburr(540,1130,300,G2,GOLD)
  +nut(410,1060,1.9,TERRA,INK,GOLD)+nut(610,1010,2.1,TERRA,INK,GOLD)+nut(720,1100,1.6,TERRA,INK,GOLD)+nut(520,1130,1.7,TERRA,INK,GOLD)
  )
CAS.append(reel(G,f'''{cv}<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:110px;line-height:1.05;font-weight:700;color:{IV}">Em várias regiões da Espanha, a festa da <span style="color:{GOLD};font-style:italic">castanha</span> tem nome próprio</div>
<div class=abs style="left:80px;top:1590px;font-size:30px;font-weight:600;letter-spacing:.16em;color:{GOLD}">CONHEÇA OS NOMES  →</div>''',1))
# tela 2 - marfim
CAS.append(reel(IV,f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:76px;line-height:1.05;font-weight:700;color:{G}">Galícia, Astúrias <span style="color:{TERRA};font-style:italic">e Catalunha</span></div>
{row(450,i_fogueira,'GALÍCIA','Magosto','Castanhas assadas no fogo, perto do Dia de Todos os Santos',SAND,G,TERRA,TERRA,IV)}
{row(860,i_sidra,'ASTÚRIAS','Amagüestu','Castanhas e sidra doce, tradição do outono asturiano',G,IV,GOLD,GOLD,G)}
{row(1270,i_panellets,'CATALUNHA','Castañada','Castanhas e panellets, doces típicos da data',SAND,G,TERRA,TERRA,IV)}''',2,acc=TERRA,pattern=False))
# tela 3 - terracota
CAS.append(reel(TERRA,f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:84px;line-height:1.05;font-weight:700;color:{IV}">Castela e Leão, Extremadura <span style="color:#F3D79A;font-style:italic">e País Basco</span></div>
{row(580,i_cartucho,'CASTELA E LEÃO E EXTREMADURA','Calbote','O mesmo costume da castanha assada, com outro nome','#9E4930',IV,'#F3D79A','#F3D79A',TERRA,h=470)}
{row(1090,i_cesta,'PAÍS BASCO','Gaztañerre','A festa da castanha no País Basco','#9E4930',IV,'#F3D79A','#F3D79A',TERRA,h=470)}''',3,acc='#F3D79A',pattern=False))
# tela 4 - verde 2: calendário Todos os Santos -> San Martín
def tile(x,y,dia,txt):
    return f'''<div class=abs style="left:{x}px;top:{y}px;width:400px;height:520px;border-radius:26px;background:{IV};overflow:hidden;border:4px solid {GOLD}">
    <div style="height:110px;background:{TERRA};color:{IV};font-size:36px;letter-spacing:.22em;font-weight:700;display:flex;align-items:center;justify-content:center">NOVEMBRO</div>
    <div class=serif style="font-size:230px;font-weight:700;color:{G};text-align:center;line-height:1.05;margin-top:28px">{dia}</div>
    <div style="font-size:38px;font-weight:600;color:{G};text-align:center;margin-top:10px">{txt}</div></div>'''
mid=svgfull(f'<path d="M475 830Q540 760 605 830" fill="none" stroke="{GOLD}" stroke-width="6" stroke-dasharray="4 16" stroke-linecap="round"/><path d="M590 812L608 832L582 842" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'+nut(540,1220,1.0,TERRA,INK,GOLD)+nut(450,1250,.8,TERRA,INK,GOLD)+nut(630,1250,.8,TERRA,INK,GOLD))
CAS.append(reel(G2,f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:96px;line-height:1.05;font-weight:700;color:{IV}">Não há <span style="color:{GOLD};font-style:italic">data fixa</span></div>
{tile(70,560,'1','Todos os Santos')}{tile(610,560,'11','San Martín')}{mid}
<div class=abs style="left:80px;top:1390px;width:920px;font-size:44px;line-height:1.42;color:{IV};text-align:center">A festa costuma acontecer <b>entre o Dia de Todos os Santos e San Martín</b>, conforme a região.</div>''',4))
CAS.append(closing(1920,TERRA,IV,'#F3D79A','Fontes: Turismo de Asturias, Xunta de Galicia e VilaWeb.<br>Consulta em 05/11/2026.',logo=460,serif_sz=88,top=.2))

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,lst,h in(('imigracao',IMIG,1350),('cultura',CAS,1920)):
            pg=await b.new_page(viewport={'width':1080,'height':h})
            for i,htm in enumerate(lst):
                await pg.set_content(htm); await pg.wait_for_timeout(500)
                await pg.screenshot(path=OUT+f'{k}-{i+1}.png')
        await b.close()
asyncio.run(main())
