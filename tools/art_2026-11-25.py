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
    <div class=abs style="left:50%;margin-left:-65px;top:{int(h*top)+logo+60+int(serif_sz*3.5)+40}px;width:130px;height:5px;background:{acc}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+int(serif_sz*3.5)+80}px;text-align:center;font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
    <div class=abs style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+int(serif_sz*3.5)+160}px;text-align:center;font-size:40px;color:{fg}">Siga <b>@espanhasemsegredo</b></div>
    <div class=abs style="left:{pad+20}px;right:{pad+20}px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg};opacity:.85">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>'''
    return page(h,bg,inner)

import math
# ---------- IMIGRAÇÃO: mobilidade de alunos ----------
def ic_exch(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M20 90H60L60 62H140V90H180L100 24Z" fill="{a}" opacity="0"/><path d="M30 80H170M30 80L58 54M30 80L58 106" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><path d="M170 130H30M170 130L142 104M170 130L142 156" fill="none" stroke="{b}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_cap(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 38L186 78L100 118L14 78Z" fill="{a}"/><path d="M50 104V142C50 160 150 160 150 142V104L100 128Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M178 84V138" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="178" cy="146" r="8" fill="{a}"/></svg>'''
def ic_docs(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="52" y="28" width="104" height="140" rx="10" fill="{b}" stroke="{a}" stroke-width="6" transform="rotate(8 100 100)"/><rect x="40" y="24" width="104" height="140" rx="10" fill="{a}"/><path d="M60 62H124M60 86H124M60 110H100" stroke="{b}" stroke-width="8" stroke-linecap="round"/><circle cx="124" cy="140" r="16" fill="{b}"/><path d="M116 140L122 146L133 133" fill="none" stroke="{a}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_pinmap(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M30 60L76 44L124 60L170 44V148L124 164L76 148L30 164Z" fill="{a}" opacity=".85"/><path d="M76 44V148M124 60V164" stroke="{b}" stroke-width="4"/><path d="M100 22C80 22 66 38 66 56C66 82 100 112 100 112C100 112 134 82 134 56C134 38 120 22 100 22Z" fill="{b}" stroke="{a}" stroke-width="6"/><circle cx="100" cy="56" r="12" fill="{a}"/></svg>'''
def ic_magn(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="86" cy="86" r="52" fill="{b}" stroke="{a}" stroke-width="12"/><path d="M126 126L176 176" stroke="{a}" stroke-width="18" stroke-linecap="round"/><path d="M62 74H110M62 94H110M62 114H92" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'''

def imig_cover():
    pil=''.join(f'<rect x="{x}" y="150" width="26" height="150" fill="{IV}"/>' for x in (92,150,208,266))
    uni=f'<svg width="400" height="330" viewBox="0 0 400 330"><path d="M40 150L200 40L360 150Z" fill="{IV}"/><g transform="translate(14,0)">{pil}</g><rect x="50" y="300" width="300" height="20" fill="{IV}"/><circle cx="200" cy="112" r="16" fill="{G2}"/></svg>'
    globe=f'''<svg width="460" height="460" viewBox="0 0 460 460"><circle cx="230" cy="230" r="190" fill="none" stroke="{GOLD}" stroke-width="8"/><ellipse cx="230" cy="230" rx="84" ry="190" fill="none" stroke="{GOLD}" stroke-width="5"/><path d="M40 230H420M70 140H390M70 320H390" stroke="{GOLD}" stroke-width="5"/><path d="M60 400C160 300 300 300 400 400" fill="none" stroke="{TERRA}" stroke-width="14" stroke-linecap="round"/><path d="M400 400L360 396M400 400L394 360" stroke="{TERRA}" stroke-width="14" stroke-linecap="round"/></svg>'''
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:{IV}"></div>
    <div class=abs style="left:0;top:760px;width:1080px;height:590px;background:{G}"></div>
    <div class=abs style="left:640px;top:520px;opacity:.95">{globe}</div>
    <div class=abs style="left:90px;top:790px">{uni}</div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Estudos</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:880px;font-size:104px;line-height:1.04;font-weight:700;color:{G}">Mobilidade de <span style="color:{TERRA};font-style:italic">alunos</span>: o que a ficha oficial trata</div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,IV,inner)
IMG=[imig_cover()]; T=7
IMG.append(content(2,T,'Imigração · Para quem','Estudante em mobilidade','A ficha oficial do Ministério de Inclusión trata de <b>estudantes estrangeiros em programas de mobilidade</b>. Confira nela quem se enquadra no seu caso.',ic_cap,'terra'))
IMG.append(content(3,T,'Imigração · Natureza','Estância, não residência','Quem estuda tem uma <b>estância por estudos</b>, que não se confunde com autorização de residência. Duração e condições: veja a ficha oficial.',ic_exch,'green'))
IMG.append(content(4,T,'Imigração · Documentos','Lista só na ficha','Em geral, pedem-se comprovantes da instituição, de meios econômicos e de seguro de saúde. A <b>lista exata</b> está na ficha oficial vigente.',ic_docs,'ivory'))
IMG.append(content(5,T,'Imigração · Onde conferir','Fonte e instituição','Consulte a ficha do Ministério e a <b>instituição de acolhida</b>. Cada programa pode ter exigências próprias.',ic_pinmap,'terra'))
IMG.append(content(6,T,'Imigração · Atenção','Confira antes de viajar','Prazos de resposta: <b>a ficha oficial prevê</b> o que consta nela, sem garantia de resultado. Cada caso é um caso.',ic_magn,'ivory'))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, página Movilidad de alumnos.<br>Consulta indicada em 25/11/2026 (a conferir).'))

# ---------- REEL: Toledo ----------
def reel_page(bg,acc,fg,inner,n):
    return page(1920,bg,f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:{bg}"></div>
    <div class=abs style="left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(0deg,{acc}12 0 2px,transparent 2px 48px)"></div>
    {bracket(acc)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{acc}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{fg}">Espanha Sem Segredo</span></div><span class=c style="color:{acc}">{n} / 5</span></div>''')
def hill(col,acc,x,y):
    bl=''.join(f'<rect x="{bx}" y="{by}" width="{bw}" height="{600-by}" fill="{col}"/>' for bx,by,bw in [(120,380,70),(200,330,60),(270,400,80),(360,300,90),(460,370,60),(530,340,80),(620,410,70),(700,360,60)])
    return f'''<svg class=abs style="left:{x}px;top:{y}px" width="880" height="640" viewBox="0 0 880 640"><circle cx="720" cy="90" r="64" fill="{acc}"/><path d="M0 600C100 420 240 300 440 300C640 300 780 420 880 600Z" fill="{col}" opacity=".35"/>{bl}<rect x="372" y="240" width="66" height="62" fill="{col}"/><path d="M372 240L405 190L438 240Z" fill="{col}"/><path d="M0 560H880V640H0Z" fill="{acc}" opacity=".8"/><path d="M0 590C120 570 200 610 330 590S560 570 700 590 820 600 880 590" fill="none" stroke="{col}" stroke-width="6"/></svg>'''
def three(col,acc,x,y):
    cross=f'<g transform="translate(0,0)"><rect x="104" y="30" width="40" height="190" fill="{col}"/><rect x="50" y="86" width="148" height="40" fill="{col}"/></g>'
    cres=f'<g transform="translate(300,0)"><circle cx="124" cy="124" r="86" fill="{col}"/><circle cx="154" cy="110" r="74" fill="{acc}"/><path d="M170 80L178 104L204 104L184 120L192 146L170 130L148 146L156 120L136 104L162 104Z" fill="{col}"/></g>'
    star=f'<g transform="translate(600,0)"><path d="M124 30L206 172H42Z M124 214L42 72H206Z" fill="none" stroke="{col}" stroke-width="14" stroke-linejoin="round"/></g>'
    return f'<svg class=abs style="left:{x}px;top:{y}px" width="880" height="250" viewBox="0 0 880 250">{cross}{cres}{star}</svg>'
def river(col,acc,x,y):
    return f'''<svg class=abs style="left:{x}px;top:{y}px" width="880" height="620" viewBox="0 0 880 620"><circle cx="440" cy="300" r="250" fill="{acc}" opacity=".25"/><path d="M60 560C60 140 440 40 560 200C680 360 360 400 360 300C360 200 560 220 560 300" fill="none" stroke="{col}" stroke-width="34" stroke-linecap="round" opacity=".9"/><path d="M60 560C60 140 440 40 560 200" fill="none" stroke="{acc}" stroke-width="8" stroke-dasharray="6 20" stroke-linecap="round"/></svg>'''
def archway(col,acc,x,y):
    return f'''<svg class=abs style="left:{x}px;top:{y}px" width="880" height="620" viewBox="0 0 880 620"><path d="M120 620V300C120 90 760 90 760 300V620" fill="none" stroke="{col}" stroke-width="44"/><path d="M230 620V320C230 200 650 200 650 320V620" fill="none" stroke="{acc}" stroke-width="18"/><path d="M440 150V90M410 120H470" stroke="{acc}" stroke-width="12" stroke-linecap="round"/></svg>'''
RR=[]
RR.append(reel_page(TERRA,IV,IV,f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:106px;line-height:1.06;font-weight:700;color:{IV}">Uma cidade sobre uma <span style="color:#F3D79A;font-style:italic">colina</span> na Espanha central</div>{hill(IV,'#F3D79A',100,860)}
<div class=abs style="left:80px;top:1580px;width:920px;font-size:44px;color:{IV}">Você conhece Toledo?</div>''',1))
RR.append(reel_page(IV,GOLD,G,f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:100px;line-height:1.06;font-weight:700;color:{G}">Cidade <span style="color:{TERRA};font-style:italic">histórica</span> da UNESCO</div>
<div class=abs style="left:80px;top:560px;width:920px;font-size:50px;line-height:1.42;color:{INK}">Em <b>1986</b>, a UNESCO inscreveu a Cidade Histórica de Toledo na lista do Patrimônio Mundial.</div>{archway(G,GOLD,100,1050)}''',2))
RR.append(reel_page(G,GOLD,IV,f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:100px;line-height:1.06;font-weight:700;color:{IV}">Cidade das <span style="color:{GOLD};font-style:italic">três culturas</span></div>
<div class=abs style="left:80px;top:560px;width:920px;font-size:50px;line-height:1.42;color:{IV}">Ao longo dos séculos, conviveram ali comunidades <b>cristã</b>, <b>muçulmana</b> e <b>judaica</b>.</div>{three(IV,G,100,1200)}''',3))
RR.append(reel_page(IV,TERRA,G,f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:100px;line-height:1.06;font-weight:700;color:{G}">Cercada pelo <span style="color:{TERRA};font-style:italic">rio Tajo</span></div>
<div class=abs style="left:80px;top:560px;width:920px;font-size:50px;line-height:1.42;color:{INK}">O rio contorna a cidade antiga em uma grande curva, o que ajuda a explicar sua posição defensiva.</div>{river(G,TERRA,100,1020)}''',4))
RR.append(closing(1920,GOLD,G,G,'Fonte: UNESCO, Historic City of Toledo (a conferir).<br>Consulta indicada em 25/11/2026.',logo=460,serif_sz=88,top=.2))

async def main(only=None):
    sets={'cultura':RR,'imigracao':IMG}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,lst in sets.items():
            if only and k not in only: continue
            h=1920 if k=='cultura' else 1350
            pg=await b.new_page(viewport={'width':1080,'height':h})
            for i,htm in enumerate(lst):
                await pg.set_content(htm); await pg.wait_for_timeout(500)
                await pg.screenshot(path=OUT+f'{k}-{i+1}.png')
        await b.close()
asyncio.run(main(sys.argv[1:] or None))
