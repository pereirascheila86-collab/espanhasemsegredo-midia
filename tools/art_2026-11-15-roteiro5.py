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
# ---- ícones carrossel 5 (renovação não lucrativa) ----
def ic_titular(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="56" r="34" fill="{a}"/><path d="M30 176V138C30 104 170 104 170 138V176Z" fill="{a}"/><rect x="118" y="132" width="62" height="42" rx="8" fill="{b}" stroke="{a}" stroke-width="6"/><circle cx="136" cy="148" r="8" fill="{a}"/><path d="M150 146H170M150 160H166" stroke="{a}" stroke-width="5" stroke-linecap="round"/></svg>'''
def ic_checklist(a,b):
    rows=''.join(f'<path d="M30 {44+i*40}L40 {54+i*40}L56 {32+i*40}" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><rect x="78" y="{38+i*40}" width="96" height="14" rx="7" fill="{a}"/>' for i in range(4))
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="12" y="10" width="176" height="180" rx="18" fill="none" stroke="{a}" stroke-width="8"/>{rows}</svg>'''
def ic_mochila(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M70 40C70 14 130 14 130 40" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round"/><rect x="40" y="38" width="120" height="146" rx="34" fill="{a}"/><rect x="62" y="108" width="76" height="54" rx="14" fill="{b}"/><path d="M62 128H138" stroke="{a}" stroke-width="6"/><rect x="90" y="120" width="20" height="14" rx="4" fill="{a}"/><path d="M76 74H124" stroke="{b}" stroke-width="9" stroke-linecap="round"/></svg>'''
def ic_nuvem(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M52 150C20 150 14 108 46 100C44 62 100 48 120 82C150 70 176 100 162 128C170 140 160 150 148 150Z" fill="{a}"/><path d="M100 176V102M72 128L100 100L128 128" fill="none" stroke="{b}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_ciclo(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M44 96C44 62 70 40 100 40C122 40 140 50 152 66" fill="none" stroke="{a}" stroke-width="16" stroke-linecap="round"/><path d="M158 24L158 76L108 70Z" fill="{a}"/><path d="M156 104C156 138 130 160 100 160C78 160 60 150 48 134" fill="none" stroke="{b}" stroke-width="16" stroke-linecap="round"/><path d="M42 176L42 124L92 130Z" fill="{b}"/></svg>'''

# ---- carrossel 5: CADERNO ----
def caderno(kick,title,body,icon_fn,theme,bs=48):
    th={'ivory':(IV,SAND,TERRA,G,INK,GOLD,G),'green':(G,G2,GOLD,IV,IV,GOLD,IV),'sand':(SAND,IV,TERRA,G,INK,TERRA,G)}[theme]
    bg,ln,mg,tcol,bcol,tape,fc=th
    lines=''.join(f'<path d="M0 {y}H1080" stroke="{ln}" stroke-width="3"/>' for y in range(200,1200,54))
    holes=''.join(f'<circle cx="62" cy="{y}" r="22" fill="{G if theme!="green" else INK}" opacity=".16"/>' for y in (260,675,1090))
    if theme=='green': ca,cb,disc=G,TERRA,GOLD
    elif theme=='sand': ca,cb,disc=IV,GOLD,GOLD
    else: ca,cb,disc=G,TERRA,GOLD
    tk=INK if theme!='green' else INK
    inner=f'''<svg class=abs style="left:0;top:0" width="1080" height="1350">{lines}<path d="M160 0V1350" stroke="{mg}" stroke-width="4"/>{holes}</svg>
    <div class=abs style="left:196px;top:64px;transform:rotate(-2deg)"><div style="display:inline-block;padding:14px 30px;background:{tape};color:{INK};font-size:26px;letter-spacing:.16em;font-weight:700;text-transform:uppercase;box-shadow:0 3px 0 rgba(0,0,0,.18)">{html.escape(kick)}</div></div>
    <div class=abs style="left:790px;top:60px;width:210px;height:210px;transform:rotate(7deg);border-radius:50%;background:{disc};display:flex;align-items:center;justify-content:center;border:7px dashed {bg}"><div style="width:140px;height:140px">{icon_fn(INK,TERRA)}</div></div>
    <div class="abs serif" style="left:210px;top:178px;width:540px;font-size:68px;line-height:1.08;font-weight:700;color:{tcol}">{title}</div>
    <div class=abs style="left:210px;top:410px;width:800px"><svg width="260" height="20" viewBox="0 0 260 20" style="margin-bottom:20px"><path d="M4 12C60 2 120 18 256 6" fill="none" stroke="{mg}" stroke-width="6" stroke-linecap="round"/></svg>
      <div style="font-size:{bs}px;line-height:1.38;color:{bcol}">{body}</div></div>
    <div class=foot style="left:210px"><div class=l><img src="{LOGO}"><span class=n style="color:{fc}">Espanha Sem Segredo</span></div></div>'''
    return page(1350,bg,inner)
def capa5():
    cells=''; hi={(2,4),(2,5),(2,6),(3,0),(3,1),(3,2)}
    for r in range(5):
        for c in range(7):
            x=150+c*110; y=780+r*86
            f= GOLD if (r,c) in hi else IV
            cells+=f'<rect x="{x}" y="{y}" width="98" height="74" rx="10" fill="{f}"/>'
    cells+=f'<circle cx="{150+3*110+49}" cy="{780+3*86+37}" r="30" fill="none" stroke="{TERRA}" stroke-width="7"/>'
    rings=''.join(f'<rect x="{x}" y="470" width="22" height="72" rx="11" fill="{INK2}" stroke="{IV}" stroke-width="4"/>' for x in (260,520,780))
    svg=f'''<svg class=abs style="left:0;top:0" width="1080" height="1350">
      <rect x="120" y="500" width="840" height="612" rx="34" fill="{G2}" opacity=".35" transform="translate(14,14)"/>
      <rect x="120" y="500" width="840" height="612" rx="34" fill="{SAND}"/>
      <path d="M120 534A34 34 0 0 1 154 500H926A34 34 0 0 1 960 534V690H120Z" fill="none"/>
      <rect x="120" y="500" width="840" height="120" rx="34" fill="{G}"/><rect x="120" y="560" width="840" height="60" fill="{G}"/>
      {T(540,586,'VENCIMENTO',44,IV,800,'Inter',ls=10)}
      {cells}{rings}
    </svg>
    <div class=abs style="left:0;right:0;top:1128px;text-align:center;font-size:30px;color:{INK};letter-spacing:.08em"></div>'''
    inner=f'''{bracket(TERRA)}
    <div class=abs style="left:80px;top:80px"><div class=kick style="color:{TERRA}">Imigração · Residência</div></div>
    <div class="abs serif" style="left:80px;top:140px;width:900px;font-size:74px;line-height:1.06;font-weight:700;color:{G}">Como <span style="color:{TERRA};font-style:italic">renovar</span> a residência não lucrativa na Espanha?</div>
    {svg}{foot(G)}'''
    return page(1350,IV,inner)
SL5=[capa5()]
SL5.append(caderno('Quem pode','Quem pode renovar','Titular de <b>residência temporária não lucrativa</b> que não seja cidadão da UE, do EEE ou da Suíça. A autorização deve estar <b>vigente</b> ou a até <b>três meses de expirar</b>.',ic_titular,'ivory',49))
SL5.append(caderno('Requisitos','Requisitos','<b>Meios econômicos suficientes</b> para o sustento e a família, sem trabalhar; <b>seguro de saúde</b> mantido durante a vigência; <b>sem antecedentes penais</b>; residência efetiva de <b>mais de 183 dias</b> no ano civil.',ic_checklist,'green',46))
SL5.append(caderno('Filhos','Filhos em idade escolar','Quem tem filhos sob sua guarda em idade de <b>escolaridade obrigatória</b> deve comprovar a <b>matrícula escolar</b>.',ic_mochila,'sand',54))
SL5.append(caderno('Quando e como','Quando e como pedir','Nos <b>dois meses anteriores</b> ao vencimento, ou até <b>três meses depois</b>, sem prejuízo de eventual procedimento sancionador. Recomendamos o <b>pedido telemático</b>. Em caso de dúvida, <b>consulte um profissional</b>.',ic_nuvem,'ivory',45))
SL5.append(caderno('Duração e prazo','Duração e prazo','A renovação vale <b>dois anos</b>, salvo se for adequada a residência de longa duração. A ficha prevê <b>três meses</b> para a resolução. Depois, renova-se o cartão (TIE) em até um mês.',ic_ciclo,'green',47))
SL5.append(closing(1350,SAND,G,TERRA,'Fonte: Ministerio de Inclusión (renovação da residência temporária não lucrativa), consulta em 15/11/2026.'))

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
asyncio.run(render(SL5,R0+'/roteiro-5-renovacao-nao-lucrativa','renovacao-nao-lucrativa',1350))
