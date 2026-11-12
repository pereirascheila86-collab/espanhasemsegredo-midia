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
    <div class=abs style="left:50%;margin-left:-65px;top:{int(h*top)+logo+60+serif_sz*3+50}px;width:130px;height:5px;background:{acc}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3+90}px;text-align:center;font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
    <div class=abs style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3+170}px;text-align:center;font-size:40px;color:{fg}">Siga <b>@espanhasemsegredo</b></div>
    <div class=abs style="left:{pad+20}px;right:{pad+20}px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg};opacity:.85">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>'''
    return page(h,bg,inner)



import math, subprocess
def figura(cx,top,s,col):
    return f'<circle cx="{cx}" cy="{top+14*s}" r="{14*s}" fill="{col}"/><path d="M{cx-18*s} {top+78*s}V{top+46*s}C{cx-18*s} {top+34*s} {cx+18*s} {top+34*s} {cx+18*s} {top+46*s}V{top+78*s}Z" fill="{col}"/>'
import math, subprocess
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


def ic_urna(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="30" y="80" width="140" height="92" rx="10" fill="{a}"/><rect x="72" y="92" width="56" height="10" rx="5" fill="{b}"/><g transform="rotate(-8 100 50)"><rect x="66" y="16" width="68" height="84" rx="6" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M80 40H120M80 58H120" stroke="{a}" stroke-width="6" stroke-linecap="round"/></g><path d="M80 140L96 156L124 124" fill="none" stroke="{b}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_casa_escudo(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 14L172 40V102C172 146 140 174 100 190C60 174 28 146 28 102V40Z" fill="{a}"/><path d="M62 108L100 74L138 108V142H62Z" fill="{b}"/><rect x="90" y="116" width="20" height="26" fill="{a}"/></svg>'
def ic_chaves_cal(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="22" y="40" width="130" height="128" rx="12" fill="{b}" stroke="{a}" stroke-width="7"/><rect x="22" y="40" width="130" height="30" rx="10" fill="{a}"/><text x="87" y="136" text-anchor="middle" font-family="Lora" font-weight="700" font-size="38" fill="{a}">2028</text><circle cx="150" cy="150" r="26" fill="{a}"/><circle cx="150" cy="150" r="9" fill="{b}"/><path d="M168 168L190 190M180 180L190 170" stroke="{a}" stroke-width="8" stroke-linecap="round"/></svg>'
def ic_tucasa(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M20 96L100 26L180 96V170H20Z" fill="{a}"/><circle cx="100" cy="116" r="38" fill="{b}"/><text x="100" y="130" text-anchor="middle" font-family="Lora" font-weight="700" font-size="40" fill="{a}">0%</text></svg>'
def ic_rasgado(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M40 16H128L112 62L134 96H40Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M62 112H160V184H48L72 148Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M58 40H100M58 62H90M80 130H140M80 152H130" stroke="{a}" stroke-width="6" stroke-linecap="round"/><path d="M146 28L176 58M176 28L146 58" stroke="{a}" stroke-width="9" stroke-linecap="round"/></svg>'
def predio_cover():
    janelas=''.join(f'<rect x="{x}" y="{y}" width="46" height="62" rx="6" fill="{GOLD if (i*3+j)%4==1 else G}"/>' for i,x in enumerate((250,330,410,490)) for j,y in enumerate((500,600,700,800,900)))
    return page(1350,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 75% 70%,{G2} 0,{G} 70%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Habitação</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:80px;line-height:1.06;font-weight:700;color:{IV}">Congresso convalida o <span style="color:{GOLD};font-style:italic">decreto de habitação</span></div>
    <svg class=abs style="left:0;top:110px" width="1080" height="1350"><rect x="210" y="450" width="380" height="640" fill="{IV}"/><rect x="190" y="430" width="420" height="30" fill="{SAND}"/>{janelas}
    <rect x="640" y="640" width="250" height="450" fill="{SAND}"/><rect x="620" y="620" width="290" height="26" fill="{IV}"/>
    {''.join(f'<rect x="{x}" y="{y}" width="40" height="54" rx="5" fill="{G}"/>' for x in (670,740,810) for y in (680,770,860,950))}
    <rect x="150" y="1090" width="780" height="24" fill="{G2}"/>
    <g transform="rotate(12 840 440)"><rect x="740" y="330" width="200" height="240" rx="14" fill="{IV}"/><path d="M772 380H908M772 420H908M772 460H860" stroke="{G}" stroke-width="10" stroke-linecap="round"/><circle cx="880" cy="530" r="30" fill="{TERRA}"/><path d="M866 530L876 541L896 516" fill="none" stroke="{IV}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></g>
    <g transform="translate(250 1180)"><circle r="0"/></g></svg>
    {foot(GOLD)}''')
T=7
HAB=[predio_cover()]
HAB.append(content2('Notícia · A votação','35 votos a 34','Em 12/11, a Diputación Permanente do Congresso convalidou o decreto de medidas de habitação e derrubou o decreto sobre renovação de aluguéis, segundo a Europa Press.',ic_urna,'ivory'))
HAB.append(content2('Notícia · Despejos','Despejos até 2030','Segundo a nota da Moncloa, o decreto prevê suspender despejos de pessoas <b>vulneráveis sem alternativa habitacional</b> até 31/12/2030, nas condições da norma.',ic_casa_escudo,'green'))
HAB.append(content2('Notícia · Aluguel','Prorrogação até 2 anos','Contratos vigentes até 31/12/2028 podem ser prorrogados por <b>até dois anos</b>, em períodos anuais, se o inquilino estiver em dia nos últimos oito meses.',ic_chaves_cal,'terra'))
HAB.append(content2('Notícia · Primeira moradia','Programa Tu Casa','Empréstimo sem juros nem comissões do ICO: o menor valor entre <b>20% do imóvel e 50.000 euros</b>. Segundo o Infobae, ainda não está disponível.',ic_tucasa,'ivory'))
HAB.append(content2('Notícia · O que caiu','Decreto derrubado','Foi derrubado o decreto que previa renovação automática por mais cinco anos e <b>indenização de um ano de aluguel</b> ao inquilino.',ic_rasgado,'green'))
HAB.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: La Moncloa (nota de 08/10/2026); Infobae/Europa Press (12/11/2026).<br>Consulta em 12/11/2026.'))
async def render(lst,prefix,h):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h})
        for i,htm in enumerate(lst):
            await pg.set_content(htm); await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT+f'{prefix}-{i+1}.png')
        await b.close()
asyncio.run(render(HAB,'habitacao',1350))
