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


# ---------- CULTURA (Reel): feiras de Natal de Madrid ----------
def luzes(x0,x1,y,sag,n,seed):
    rnd=random.Random(seed); pts=[]
    d=f'M{x0} {y}Q{(x0+x1)/2} {y+sag} {x1} {y}'
    s=f'<path d="{d}" fill="none" stroke="{IV}" stroke-width="3" opacity=".6"/>'
    for i in range(n):
        t=(i+.5)/n; px=(1-t)**2*x0+2*(1-t)*t*(x0+x1)/2+t*t*x1; py=(1-t)**2*y+2*(1-t)*t*(y+sag)+t*t*y
        s+=f'<circle cx="{px:.0f}" cy="{py+10:.0f}" r="9" fill="{rnd.choice([GOLD,"#F3D79A",TERRA])}"/>'
    return s
def caseta(x,y,w,h,roof,body,lit=GOLD):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{body}"/><path d="M{x-14} {y}L{x+w/2} {y-h*.42}L{x+w+14} {y}Z" fill="{roof}"/>'
            f'<rect x="{x+w*.16}" y="{y+h*.22}" width="{w*.68}" height="{h*.4}" fill="{lit}" opacity=".9"/><path d="M{x+w*.16} {y+h*.62}H{x+w*.84}" stroke="{IV}" stroke-width="6"/>')
def estrela(cx,cy,r,col):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*.42
        pts.append(f'{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}')
    return f'<polygon points="{" ".join(pts)}" fill="{col}"/>'
def cena_feira_capa(w,h):
    rnd=random.Random(2)
    ceu=''.join(f'<circle cx="{rnd.randint(30,930)}" cy="{rnd.randint(40,420)}" r="{rnd.choice([3,4,5])}" fill="{IV}" opacity=".8"/>' for _ in range(34))
    arc=''.join(f'<path d="M{x} 760V560C{x} 480 {x+60} 450 {x+100} 450C{x+140} 450 {x+200} 480 {x+200} 560V760" fill="{TERRA}"/><path d="M{x+30} 760V574C{x+30} 520 {x+70} 496 {x+100} 496C{x+130} 496 {x+170} 520 {x+170} 574V760" fill="{G}"/>' for x in (-40,160,360,560,760,960))
    casetas=''.join(caseta(x,860,120,150,r,b) for x,r,b in [(40,TERRA,SAND),(210,GOLD,IV),(380,TERRA,SAND),(550,GOLD,IV),(720,TERRA,SAND)])
    return (ceu+estrela(480,170,90,GOLD)+f'<rect x="0" y="440" width="{w}" height="40" fill="{TERRA}"/>'+arc+f'<rect x="0" y="760" width="{w}" height="{h-760}" fill="{G2}"/>'
            +luzes(0,960,700,70,18,1)+casetas+f'<rect x="0" y="1010" width="{w}" height="{h-1010}" fill="{SAND}" opacity=".18"/>')
def cena_presepio(w,h):
    estab=f'<path d="M140 760V400L480 190L820 400V760Z" fill="{TERRA}"/><path d="M200 760V430L480 262L760 430V760Z" fill="{G}"/><path d="M110 410L480 170L850 410" fill="none" stroke="{GOLD}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
    est=estrela(480,90,70,GOLD)
    mae=f'<circle cx="330" cy="520" r="34" fill="{IV}"/><path d="M270 760V610C270 560 390 560 390 610V760Z" fill="{IV}"/><path d="M300 520C320 480 360 480 372 520" fill="none" stroke="{GOLD}" stroke-width="8"/>'
    pai=f'<circle cx="640" cy="520" r="34" fill="{SAND}"/><path d="M580 760V610C580 560 700 560 700 610V760Z" fill="{SAND}"/><rect x="718" y="470" width="12" height="290" fill="{GOLD}"/>'
    bebe=f'<path d="M430 760V716C430 690 530 690 530 716V760Z" fill="{GOLD}"/><circle cx="480" cy="690" r="22" fill="{IV}"/>'
    palha=f'<path d="M110 760H850" stroke="{GOLD}" stroke-width="12"/>'+''.join(f'<path d="M{x} 760L{x+10} 740" stroke="{GOLD}" stroke-width="5"/>' for x in range(130,850,34))
    pecas=f'<g transform="translate(60 776)"><rect width="190" height="90" rx="14" fill="{G}"/><text x="95" y="56" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="2" fill="{GOLD}">BELENES</text></g><g transform="translate(385 776)"><rect width="190" height="90" rx="14" fill="{G}"/><text x="95" y="56" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="2" fill="{GOLD}">ENFEITES</text></g><g transform="translate(710 776)"><rect width="190" height="90" rx="14" fill="{G}"/><text x="95" y="56" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="2" fill="{GOLD}">BRINQUEDOS</text></g>'
    return est+estab+mae+pai+bebe+palha+pecas
def cena_seculos(w,h):
    def old(x,y):
        return caseta(x,y,150,170,TERRA,SAND,TERRA)+f'<circle cx="{x+30}" cy="{y+190}" r="16" fill="{TERRA}"/><circle cx="{x+75}" cy="{y+196}" r="16" fill="{GOLD}"/><circle cx="{x+120}" cy="{y+190}" r="16" fill="{TERRA}"/>'
    ped=f'<text x="190" y="120" text-anchor="middle" font-family="Lora" font-weight="700" font-size="72" fill="{GOLD}">Séc. XVII</text><text x="190" y="170" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="3" fill="{IV}">PLAZA DE SANTA CRUZ</text>'
    seta=f'<path d="M370 480H560M526 450L562 480L526 510" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><text x="465" y="548" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="3" fill="{IV}">~200 ANOS</text>'
    rolo=f'<rect x="610" y="260" width="300" height="400" rx="16" fill="{IV}"/><rect x="590" y="244" width="340" height="40" rx="20" fill="{SAND}"/><rect x="590" y="636" width="340" height="40" rx="20" fill="{SAND}"/><path d="M650 340H870M650 390H870M650 440H820M650 490H870M650 540H780" stroke="{G}" stroke-width="10" stroke-linecap="round"/><circle cx="820" cy="590" r="30" fill="{TERRA}"/><text x="760" y="205" text-anchor="middle" font-family="Lora" font-weight="700" font-size="58" fill="{GOLD}">Ordenança</text>'
    return ped+old(110,300)+f'<rect x="40" y="540" width="300" height="12" fill="{GOLD}"/>'+seta+rolo
def cena_outras(w,h):
    t1=f'<rect x="40" y="40" width="880" height="360" rx="28" fill="{G}"/><text x="80" y="120" font-family="Lora" font-weight="700" font-size="56" fill="{GOLD}">Recoletos</text><text x="80" y="176" font-family="Inter" font-weight="800" font-size="28" letter-spacing="3" fill="{IV}">COLÓN – CIBELES</text><text x="80" y="244" font-family="Lora" font-weight="700" font-size="46" fill="{IV}">1 a 30 de dezembro</text><text x="80" y="300" font-family="Inter" font-size="34" fill="{IV}">Mais de 150 artesãos</text>'
    vaso=f'<path d="M740 150C700 200 700 300 750 340H830C880 300 880 200 840 150Z" fill="{TERRA}"/><rect x="750" y="126" width="80" height="28" rx="8" fill="{GOLD}"/><path d="M715 230H865" stroke="{IV}" stroke-width="7"/>'
    t2=f'<rect x="40" y="440" width="880" height="360" rx="28" fill="{TERRA}"/><text x="80" y="520" font-family="Lora" font-weight="700" font-size="56" fill="{IV}">La Navideña</text><text x="80" y="576" font-family="Inter" font-weight="800" font-size="28" letter-spacing="3" fill="#F3D79A">PLAZA DE ESPAÑA</text><text x="80" y="644" font-family="Lora" font-weight="700" font-size="46" fill="{IV}">Finais de nov. a início de jan.</text><text x="80" y="700" font-family="Inter" font-size="34" fill="{IV}">Datas por confirmar</text>'
    patins=f'<path d="M760 540L760 620C760 640 790 650 820 650H880L880 600L840 600L820 560Z" fill="{IV}"/><path d="M740 676H900" stroke="{G}" stroke-width="8" stroke-linecap="round"/>'
    return t1+vaso+t2+patins
def reel():
    S=[]
    S.append(rbv(f'''{Tv('As feiras de Natal de Madrid são <span style="color:@AC;font-style:italic">tradição</span> desta época do ano',80)}
    {cardv(60,640,960,1100,G,cena_feira_capa(960,1100),-30)}''',1,'green'))
    S.append(rbv(f'''{Tv('Plaza Mayor: <span style="color:@AC">presépios e enfeites</span>',84)}
    {Pv('O Mercado de Navidad vai do fim de novembro a 31 de dezembro, com 104 casetas. Vende figuras de presépio, decorações e brinquedos.',480)}
    {cardv(60,880,960,880,SAND,cena_presepio(960,880),10)}''',2,'terra'))
    S.append(rbv(f'''{Tv('Uma tradição de <span style="color:@AC">séculos</span>',100)}
    {Pv('No século XVII, já havia barracas na Plaza de Santa Cruz nesta época. Cerca de duzentos anos depois, uma ordenança legalizou o mercado.',540)}
    {cardv(60,960,960,780,G,cena_seculos(960,780),-20)}''',3,'ivory'))
    S.append(rbv(f'''{Tv('Outras feiras <span style="color:@AC">pela cidade</span>',100)}
    {Pv('Confirme datas e horários com os organizadores.',540)}
    {cardv(60,740,960,840,SAND,cena_outras(960,840),20)}''',4,'green'))
    S.append(closing(1920,G,IV,GOLD,'Fonte: Turismo de Madrid (esmadrid.com), Mercadillos navideños e Mercado de Navidad de la Plaza Mayor.<br>Consulta em 14/11/2026.',logo=460,serif_sz=88,top=.2))
    return S

async def render(lst,prefix,h):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h})
        for i,htm in enumerate(lst):
            await pg.set_content(htm); await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT+f'{prefix}-{i+1}.png')
        await b.close()
S=reel(); asyncio.run(render(S,'cultura',1920))
n=len(S); d=3.5; f=0.4
cmd=['ffmpeg','-y','-loglevel','error']
for i in range(n): cmd+=['-loop','1','-t',str(d),'-i',OUT+f'cultura-{i+1}.png']
flt=''.join(f'[{i}:v]format=yuv420p,fade=t=in:st=0:d={f},fade=t=out:st={d-f}:d={f}[v{i}];' for i in range(n))
flt+=''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[o]'
cmd+=['-filter_complex',flt,'-map','[o]','-r','30','-pix_fmt','yuv420p',OUT+'reel-cultura.mp4']
subprocess.run(cmd,check=True)
