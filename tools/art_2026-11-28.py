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

import math

def svg(vb,inner,w,h,style=''):
    return f'<svg class=abs style="{style}" width="{w}" height="{h}" viewBox="{vb}">{inner}</svg>'
def at(x,y,h,w=920,extra=''):
    return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;{extra}">{h}</div>'
def kick(t,c): return at(80,96,f'<span class=kick style="color:{c}">{t}</span>')

def closing(h,bg,fg,acc,srcs,logo=360,serif_sz=70,top=.12):
    y=int(h*top)
    inner=f"""{bracket(acc)}
    <div class=abs style="left:0;right:0;top:{y}px;display:flex;justify-content:center"><img src="{LOGO}" width="{logo}" height="{logo}"></div>
    <div class=abs style="left:80px;right:80px;top:{y+logo+60}px;text-align:center">
      <div class=serif style="font-size:{serif_sz}px;line-height:1.14;font-weight:700;color:{fg}">Aqui você fica por dentro de tudo sobre a Espanha</div>
      <div style="width:130px;height:5px;background:{acc};margin:44px auto 40px"></div>
      <div class=serif style="font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
      <div style="font-size:40px;color:{fg};margin-top:26px">Siga <b>@espanhasemsegredo</b></div></div>
    <div class=abs style="left:90px;right:90px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg}">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>"""
    return page(h,bg,inner)


def T(x,y,t,fs,c,fam='Inter',w=700,ls=0,anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{fs}" letter-spacing="{ls}" fill="{c}">{t}</text>'
def title(t,c,y=170,sz=96,w=920): return at(80,y,f'<div class=serif style="font-size:{sz}px;line-height:1.08;font-weight:700;color:{c}">{t}</div>',w)
def body(t,c,y,sz=44,w=920,x=80): return at(x,y,f'<div style="font-size:{sz}px;line-height:1.42;color:{c}">{t}</div>',w)
def rule(y,c,x=80): return at(x,y,'',130,f'height:5px;background:{c}')

# ============ NOTICIA: pensões 2027 (moedas em escada, bloco inferior) ============
def coins(x,base,n,w=150,top=GOLD,edge=INK):
    g=''
    for i in range(n):
        y=base-i*34
        g+=f'<path d="M{x} {y-30}V{y}C{x} {y+34} {x+w} {y+34} {x+w} {y}V{y-30}Z" fill="{top}" stroke="{edge}" stroke-width="5"/><ellipse cx="{x+w/2}" cy="{y-30}" rx="{w/2}" ry="24" fill="{SAND}" stroke="{edge}" stroke-width="5"/>'
    return g
def p_stair():
    g=f'<path d="M20 520H900" stroke="{G}" stroke-width="10" stroke-linecap="round"/>'
    for i,n in enumerate([3,5,7,9]): g+=coins(70+i*205,488,n)
    g+=f'<path d="M80 300C300 260 520 180 790 62" fill="none" stroke="{TERRA}" stroke-width="18" stroke-linecap="round"/><path d="M720 56L802 56L778 132" fill="none" stroke="{TERRA}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
    return g
def p_pct():
    g=f'<circle cx="460" cy="250" r="225" fill="{IV}" stroke="{GOLD}" stroke-width="22"/>'+T(460,292,'+3,5%',130,G,'Lora')+T(460,362,'PROVISÓRIO',36,TERRA,'Inter',800,7)
    g+=coins(40,470,5,130)+coins(750,470,7,130)
    return g
def p_people():
    g=''
    for r,(yy,cnt,off) in enumerate([(150,7,0),(290,6,60),(430,7,0)]):
        for i in range(cnt):
            x=100+off+i*120; c=[G,TERRA,G2,GOLD][(i+r)%4]
            g+=f'<circle cx="{x}" cy="{yy-52}" r="30" fill="{c}"/><path d="M{x-46} {yy+56}C{x-46} {yy-34} {x+46} {yy-34} {x+46} {yy+56}Z" fill="{c}"/>'
    return g
def p_envelope():
    g=''
    for x,lbl,val,sub in [(40,'APOSENTADORIA MÉDIA','774,5 €','cerca de, por ano'),(480,'PENSÃO MÉDIA','676 €','por ano')]:
        g+=f'<rect x="{x}" y="70" width="400" height="400" rx="30" fill="{IV}" stroke="{GOLD}" stroke-width="10"/><rect x="{x}" y="70" width="400" height="92" rx="30" fill="{G}"/>'+T(x+200,130,lbl,27,IV,'Inter',800,2)+T(x+200,300,'+'+val,76,TERRA,'Lora')+T(x+200,370,sub,34,G)+f'<path d="M{x+80} 420H{x+320}" stroke="{SAND}" stroke-width="14" stroke-linecap="round"/>'
    return g
def p_floor():
    g=''
    for x,hh,c,lbl,v in [(60,250,G,'mínimas e não contributivas','8,8% a 14,2%'),(500,330,G2,'Ingresso Mínimo Vital','14,1%')]:
        g+=f'<rect x="{x}" y="{480-hh}" width="360" height="{hh}" rx="20" fill="{c}"/>'+T(x+180,480-hh+120,v,58 if len(v)>6 else 90,GOLD,'Lora')+T(x+180,515,lbl,26,G,'Inter',700)
        g+=f'<path d="M{x+180} {440-hh}V{370-hh if hh<300 else 70}M{x+150} {400-hh if hh<300 else 100}L{x+180} {370-hh if hh<300 else 70}L{x+210} {400-hh if hh<300 else 100}" fill="none" stroke="{TERRA}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>'
    return g
def p_decree():
    g=f'<g transform="rotate(-4 280 260)"><rect x="110" y="40" width="350" height="440" rx="18" fill="{IV}" stroke="{G}" stroke-width="8"/>'+T(285,125,'REAL',44,G,'Lora')+T(285,178,'DECRETO-LEI',38,G,'Lora')+''.join(f'<path d="M160 {y}H410" stroke="{SAND}" stroke-width="16" stroke-linecap="round"/>' for y in (240,290,340))+f'<path d="M180 425H390" stroke="{TERRA}" stroke-width="6" stroke-dasharray="16 14"/></g>'
    g+=f'<rect x="520" y="130" width="340" height="310" rx="28" fill="{SAND}"/><rect x="520" y="130" width="340" height="90" rx="28" fill="{TERRA}"/>'+T(690,190,'DEZEMBRO',36,IV,'Inter',800,5)+T(690,370,'15',150,G,'Lora')+T(690,420,'IPC definitivo',30,G)
    return g
def pslide(bg,fg,acc,panel,k,art,tt,tx,tsz=80):
    inner=f"""{at(0,780,'',1080,f'height:570px;background:{panel}')}{bracket(acc)}{kick(k,acc)}
    {title(tt,fg,180,tsz,800)}
    {svg('0 0 920 540',art,920,540,'left:80px;top:300px') if False else ''}
    {svg('0 0 920 540',art,920,540,'left:80px;top:330px')}"""
    return inner
def pensao(bg,fg,acc,k,art,artpanel,tt,tx,tsz=78):
    inner=f"""{bracket(acc)}{kick(k,acc)}{title(tt,fg,180,tsz,820)}{rule(385,acc)}{body(tx,fg,435,45)}
    {at(60,760,'',960,f'height:450px;border-radius:34px;background:{artpanel}')}{svg('0 0 920 540',art,740,434,'left:170px;top:772px')}{foot(fg)}"""
    return page(1350,bg,inner)
def p_cover():
    inner=f"""{at(0,640,'',1080,f'height:710px;background:{TERRA}')}{bracket(TERRA)}{kick('Notícia · Espanha',TERRA)}
    {title(f'Pensões na Espanha em 2027: <span style="color:{TERRA};font-style:italic">quanto devem subir</span>',G,175,92)}
    {at(80,660,'',920,f'height:490px;border-radius:30px;background:{IV}')}{svg('0 0 920 540',p_stair(),880,517,'left:100px;top:630px')}
    {foot(IV)}{at(780,1185,f'<span class=kick style="color:{IV};font-size:26px">Deslize →</span>',240)}"""
    return page(1350,IV,inner)
NOT=[p_cover(),
 pensao(G,IV,GOLD,'Contributivas',p_pct(),G2,'Alta provisória de 3,5%','Usa o dado adiantado do IPC de novembro. A confirmação virá em <b>15 de dezembro</b>, com o índice definitivo.'),
 pensao(IV,G,TERRA,'Alcance',p_people(),SAND,'Quem entra na conta','Mais de <b>10,6 milhões</b> de pensões contributivas, recebidas por quase 9,6 milhões de pessoas. O percentual vale também para 722.400 pensionistas de Clases Pasivas.',74),
 pensao(TERRA,IV,SAND,'Em euros',p_envelope(),G2,'Quanto representa','Na aposentadoria média, cerca de <b>774,5 €</b> a mais por ano. Na pensão média do sistema, <b>676 €</b> a mais por ano.'),
 pensao(IV,G,TERRA,'Reforço',p_floor(),SAND,'Altas maiores','Pensões mínimas e não contributivas: de <b>8,8% a 14,2%</b>, conforme a modalidade. Ingresso Mínimo Vital: <b>14,1%</b>.'),
 pensao(G,IV,GOLD,'Próximos passos',p_decree(),G2,'Ainda falta aprovar','Segundo La Moncloa, o Governo aprovará um <b>real decreto-lei</b> para garantir o aumento em janeiro.'),
 closing(1350,IV,G,TERRA,'Fonte: La Moncloa, Inclusión, Seguridad Social y Migraciones (27/11/2026).<br>Consulta em 28/11/2026.')]

# ============ IMIGRAÇÃO: retorno voluntário (bilhete de embarque) ============
def plane(x,y,s,c,r=0): return f'<g transform="translate({x} {y}) rotate({r}) scale({s})"><path d="M95 0C95 -9 80 -12 62 -12H22L-22 -78H-44L-24 -12H-62L-80 -34H-94L-84 0L-94 34H-80L-62 12H-24L-44 78H-22L22 12H62C80 12 95 9 95 0Z" fill="{c}"/></g>'
def r_globe():
    g=f'<circle cx="400" cy="240" r="200" fill="{G2}"/><g fill="none" stroke="{SAND}" stroke-width="5" opacity=".8"><ellipse cx="400" cy="240" rx="90" ry="200"/><path d="M200 240H600M230 140H570M230 340H570M400 40V440"/></g>'
    g+=f'<path d="M505 150C640 20 790 80 770 240C752 400 520 480 250 390" fill="none" stroke="{TERRA}" stroke-width="12" stroke-dasharray="26 20" stroke-linecap="round"/>'+plane(235,383,1.0,TERRA,200)
    g+=f'<circle cx="505" cy="150" r="22" fill="{GOLD}" stroke="{IV}" stroke-width="7"/>'
    return g
def r_passport():
    g=''
    for x,c,r in [(180,G,-8),(420,TERRA,7)]:
        g+=f'<g transform="rotate({r} {x+120} 240)"><rect x="{x}" y="80" width="240" height="330" rx="20" fill="{c}"/><circle cx="{x+120}" cy="215" r="62" fill="none" stroke="{GOLD}" stroke-width="8"/><ellipse cx="{x+120}" cy="215" rx="26" ry="62" fill="none" stroke="{GOLD}" stroke-width="5"/><path d="M{x+58} 215H{x+182}M{x+60} 340H{x+180}" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/></g>'
    g+=f'<circle cx="720" cy="380" r="68" fill="{GOLD}"/>'+T(720,402,'não UE',32,G,'Inter',800)
    return g
def r_two():
    g=f'<path d="M230 90C175 20 80 80 130 150L230 235L330 150C380 80 285 20 230 90Z" fill="{TERRA}"/><path d="M60 330C90 290 160 300 215 345L290 345Q320 365 290 390H215M60 410C150 450 250 460 400 355Q405 325 365 332L290 365" fill="none" stroke="{G}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>'
    g+=f'<path d="M460 40V440" stroke="{GOLD}" stroke-width="6" stroke-dasharray="14 18"/>'
    g+=f'<path d="M540 250L580 150H800L840 250Z" fill="{G}"/>'+''.join(f'<path d="M{x} 150L{x-12 if x<690 else x+12} 250" stroke="{GOLD}" stroke-width="14"/>' for x in (630,690,750))
    g+=f'<rect x="570" y="250" width="240" height="180" fill="{IV}" stroke="{G}" stroke-width="10"/><rect x="610" y="310" width="66" height="120" fill="{TERRA}"/><rect x="710" y="300" width="70" height="60" fill="{GOLD}"/>'
    return g
def r_case():
    g=f'<path d="M345 140V90Q345 60 375 60H545Q575 60 575 90V140" fill="none" stroke="{G}" stroke-width="26"/><rect x="200" y="135" width="520" height="310" rx="40" fill="{TERRA}"/><path d="M300 135V445M620 135V445" stroke="{G}" stroke-width="26"/><g transform="rotate(-10 460 290)"><rect x="350" y="235" width="220" height="110" rx="12" fill="{IV}"/>'+plane(460,290,.55,G)+'</g>'
    g+=f'<circle cx="270" cy="460" r="22" fill="{G}"/><circle cx="650" cy="460" r="22" fill="{G}"/><circle cx="780" cy="130" r="64" fill="{GOLD}"/>'+T(780,155,'€',72,G,'Lora')
    return g
def r_three():
    g=f'<rect x="110" y="40" width="420" height="420" rx="30" fill="{IV}" stroke="{G}" stroke-width="10"/><path d="M110 150H530" stroke="{G}" stroke-width="10"/>'+T(320,118,'COMPROMISSO',34,TERRA,'Inter',800,3)+T(320,330,'3',200,G,'Lora')+T(320,420,'anos',52,G,'Lora')
    g+=f'<g transform="rotate(38 700 270)"><rect x="668" y="80" width="64" height="300" rx="12" fill="{TERRA}"/><path d="M668 380L700 455L732 380Z" fill="{SAND}"/><path d="M686 425L700 455L714 425Z" fill="{INK}"/><rect x="668" y="110" width="64" height="26" fill="{GOLD}"/></g>'
    return g
def r_desk():
    g=f'<path d="M60 440H860" stroke="{G}" stroke-width="12" stroke-linecap="round"/>'
    for x,c in [(250,G),(660,TERRA)]:
        g+=f'<circle cx="{x}" cy="200" r="66" fill="{c}"/><path d="M{x-120} 440C{x-120} 250 {x+120} 250 {x+120} 440Z" fill="{c}"/>'
    g+=f'<circle cx="455" cy="140" r="86" fill="{GOLD}"/>'+T(455,182,'i',120,G,'Lora')+f'<rect x="380" y="350" width="150" height="90" rx="10" fill="{IV}" stroke="{G}" stroke-width="8"/>'
    return g
def ticket(bg,fg,acc,paper,k,art,tt,tx,tsz=64):
    inner=f"""{bracket(acc)}{kick(k,acc)}
    {at(80,190,'',920,f'height:980px;border-radius:36px;background:{paper}')}
    {svg('0 0 920 500',art,860,468,'left:110px;top:215px')}
    {at(80,700,'',920,f'border-top:5px dashed {TERRA}')}
    {at(50,670,'',62,f'height:62px;border-radius:50%;background:{bg}')}{at(968,670,'',62,f'height:62px;border-radius:50%;background:{bg}')}
    {at(140,750,f'<div class=serif style="font-size:{tsz}px;line-height:1.12;font-weight:700;color:{G}">{tt}</div><div style="width:120px;height:5px;background:{GOLD};margin:28px 0 30px"></div><div style="font-size:43px;line-height:1.42;color:{INK}">{tx}</div>',800)}
    {foot(fg)}"""
    return page(1350,bg,inner)
def r_cover():
    inner=f"""{bracket(GOLD)}{kick('Imigração',GOLD)}
    {title(f'Retorno voluntário: como funcionam os <span style="color:{GOLD};font-style:italic">programas</span> na Espanha',IV,180,90)}
    {at(80,620,'',920,f'height:510px;border-radius:36px;background:{IV}')}{svg('0 0 920 500',r_globe(),880,478,'left:100px;top:630px')}
    {foot(IV)}{at(780,1175,f'<span class=kick style="color:{GOLD};font-size:26px">Deslize →</span>',240)}"""
    return page(1350,TERRA,inner)
IMG=[r_cover(),
 ticket(G,IV,GOLD,IV,'Para quem',r_passport(),'Nacionais de fora da UE','Podem optar pelo retorno ao país de origem se cumprirem os requisitos de cada <b>convocatória anual</b> de subvenções.'),
 ticket(IV,G,TERRA,SAND,'Modalidades',r_two(),'Assistido ou produtivo','<b>Assistido, com reintegração:</b> especial vulnerabilidade comprovada. <b>Produtivo:</b> para iniciar um projeto empresarial ligado ao retorno.'),
 ticket(TERRA,IV,SAND,IV,'Apoios · 2026',r_case(),'O que a convocatória prevê','Orientação, apoio psicológico, passagem de volta e auxílios de viagem e instalação. No produtivo, também apoio ao projeto.',60),
 ticket(G2,IV,GOLD,SAND,'Atenção',r_three(),'Há compromissos','Renúncia aos documentos que ligam à Espanha e, por <b>3 anos</b>, não voltar para trabalhar nem com residência não lucrativa.',64),
 ticket(IV,G,TERRA,SAND,'Onde se informar',r_desk(),'Procure uma entidade','ONGs e organismos especializados executam os projetos. Há também um projeto com a OIM. Informe-se antes de decidir.'),
 closing(1350,G,IV,GOLD,'Fontes: Ministerio de Inclusión, Seguridad Social y Migraciones:<br>retorno voluntário e subvenções 2026.<br> Consulta em 28/11/2026.')]

# ============ REEL: Canto da Sibila (noite em Maiorca) ============
def star(x,y,r,c=GOLD): return f'<path d="M{x} {y-r}Q{x+r*.18} {y-r*.18} {x+r} {y}Q{x+r*.18} {y+r*.18} {x} {y+r}Q{x-r*.18} {y+r*.18} {x-r} {y}Q{x-r*.18} {y-r*.18} {x} {y-r}Z" fill="{c}"/>'
def sky(): return ''.join(star(x,y,r) for x,y,r in [(90,60,20),(250,150,11),(760,70,26),(640,180,10),(830,230,14),(60,260,12),(450,40,14)])
def candle(x,y): return f'<rect x="{x-14}" y="{y}" width="28" height="200" rx="8" fill="{IV}"/><path d="M{x} {y-66}C{x+30} {y-30} {x+22} {y-4} {x} {y-4}S{x-30} {y-30} {x} {y-66}Z" fill="{GOLD}"/>'
def singer(cx,top):
    t=top
    g=f'<path d="M{cx-190} {t+800}L{cx-95} {t+260}Q{cx} {t+215} {cx+95} {t+260}L{cx+190} {t+800}Z" fill="{IV}"/>'
    g+=f'<path d="M{cx-95} {t+260}L{cx-240} {t+780}L{cx-150} {t+790}L{cx-70} {t+370}ZM{cx+95} {t+260}L{cx+240} {t+780}L{cx+150} {t+790}L{cx+70} {t+370}Z" fill="{TERRA}"/>'
    g+=f'<path d="M{cx-175} {t+740}H{cx+175}" stroke="{GOLD}" stroke-width="18"/><path d="M{cx-62} {t+256}Q{cx} {t+318} {cx+62} {t+256}" fill="none" stroke="{GOLD}" stroke-width="16"/>'
    g+=f'<circle cx="{cx}" cy="{t+160}" r="82" fill="{SAND}"/><path d="M{cx-88} {t+135}C{cx-85} {t+40} {cx+85} {t+40} {cx+88} {t+135}Z" fill="{TERRA}" stroke="{GOLD}" stroke-width="8"/>'
    # espada erguida diante do rosto
    g+=f'<path d="M{cx-10} {t+330}V{t+30}L{cx} {t-5}L{cx+10} {t+30}V{t+330}Z" fill="{SAND}" stroke="{INK}" stroke-width="5"/><path d="M{cx-64} {t+338}H{cx+64}" stroke="{GOLD}" stroke-width="20" stroke-linecap="round"/><path d="M{cx} {t+340}V{t+415}" stroke="{INK}" stroke-width="20" stroke-linecap="round"/><circle cx="{cx}" cy="{t+385}" r="34" fill="{SAND}" stroke="{INK}" stroke-width="4"/>'
    return g
def reel(bg,acc,fg,inner):
    return page(1920,bg,f"""{bracket(acc)}{at(80,110,f'<span class=kick style="color:{acc}">VOCÊ SABIA? | ESPANHA</span>')}{inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{fg}">Espanha Sem Segredo</span></div></div>""")
def s_cover(y):
    g=sky()+singer(440,90)+candle(110,640)+candle(770,640)+f'<path d="M30 892H850" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
    return svg('0 0 880 920',g,880,920,f'left:100px;top:{y}px')
def s_church(y):
    g=sky()
    g+=f'<path d="M150 760V430L440 270L730 430V760Z" fill="{SAND}"/><path d="M120 446L440 260L760 446" fill="none" stroke="{GOLD}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>'
    g+=f'<rect x="640" y="200" width="150" height="560" fill="{IV}"/><path d="M625 206L715 90L805 206Z" fill="{TERRA}"/><path d="M715 94V40M692 62H738" stroke="{GOLD}" stroke-width="10"/><path d="M680 330V270Q715 225 750 270V330Z" fill="{G}"/>'
    g+=f'<circle cx="440" cy="450" r="58" fill="{G}" stroke="{GOLD}" stroke-width="10"/>'+''.join(f'<path d="M440 450L{440+52*math.cos(math.radians(a)):.0f} {450+52*math.sin(math.radians(a)):.0f}" stroke="{GOLD}" stroke-width="6"/>' for a in range(0,360,60))
    g+=f'<path d="M370 760V630Q440 540 510 630V760Z" fill="{GOLD}"/><path d="M370 760L290 800H590L510 760Z" fill="{GOLD}" opacity=".4"/><path d="M40 760H840" stroke="{IV}" stroke-width="10" stroke-linecap="round"/>'
    return svg('0 0 880 820',g,880,820,f'left:100px;top:{y}px')
def s_trio(y):
    def acol(x):
        return f'<path d="M{x-90} 640L{x-45} 330Q{x} 305 {x+45} 330L{x+90} 640Z" fill="{SAND}"/><circle cx="{x}" cy="262" r="52" fill="{IV}"/><path d="M{x-45} 335Q{x} 385 {x+45} 335" fill="none" stroke="{TERRA}" stroke-width="14"/>'+candle(x+(70 if x<440 else -70),300)
    g=acol(150)+acol(730)+f'<g transform="translate(176 106) scale(.6)">{singer(440,40)}</g>'+f'<path d="M30 645H850" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>'
    return svg('0 0 880 670',g,880,670,f'left:100px;top:{y}px')
def s_organ(y):
    g=''
    for i,h in enumerate([210,260,310,360,420,360,310,260,210]):
        x=105+i*76
        g+=f'<rect x="{x}" y="{460-h}" width="54" height="{h}" rx="22" fill="{SAND}" stroke="{GOLD}" stroke-width="6"/><path d="M{x+10} 415H{x+44}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
    g+=f'<rect x="70" y="455" width="740" height="90" rx="16" fill="{TERRA}"/>'+''.join(f'<rect x="{110+i*40}" y="480" width="24" height="40" rx="4" fill="{IV}"/>' for i in range(17))
    g+=f'<rect x="210" y="590" width="460" height="130" rx="24" fill="{IV}"/>'+T(440,648,'UNESCO',40,G,'Inter',800,6)+T(440,702,'2010',56,TERRA,'Lora')
    return svg('0 0 880 740',g,880,740,f'left:100px;top:{y}px')
RR=[
 reel(G,GOLD,IV,title(f'Em Maiorca, a noite de Natal tem um canto com <span style="color:{GOLD};font-style:italic">espada</span>',IV,240,98)+s_cover(750)),
 reel(G2,GOLD,IV,title(f'O Canto da <span style="color:{GOLD};font-style:italic">Sibila</span>',IV,240,108)+body('Na noite de <b>24 de dezembro</b>, é interpretado nas matinas, em igrejas de toda a ilha de Maiorca.',IV,500,52)+s_church(850)),
 reel(TERRA,SAND,IV,title(f'Quem <span style="color:{SAND};font-style:italic">canta</span>',IV,240,108)+body('Um menino ou uma menina, junto a dois ou mais coroinhas com velas. Costuma vestir túnica, muitas vezes com capa, e um gorro da mesma cor.',IV,460,50)+at(80,960,'',920,f'height:720px;border-radius:40px;background:{G}')+s_trio(985)),
 reel(G,GOLD,IV,title(f'Voz, órgão e <span style="color:{GOLD};font-style:italic">espada</span>',IV,240,100)+body('Canta-se a capela, com órgão entre os versos; ao final, a espada desenha uma cruz no ar. Em <b>2010</b>, o canto entrou na lista da UNESCO de patrimônio imaterial.',IV,470,50)+s_organ(960)),
 closing(1920,IV,G,TERRA,'Fonte: UNESCO, Patrimônio Cultural Imaterial,<br>“Chant of the Sybil on Majorca” e decisão 5.COM 6.38.<br>Consulta em 28/11/2026.',logo=460,serif_sz=88,top=.17)]

async def main():
    sets={'noticia':(NOT,1350),'imigracao':(IMG,1350),'cultura':(RR,1920)}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,(lst,h) in sets.items():
            pg=await b.new_page(viewport={'width':1080,'height':h})
            for i,htm in enumerate(lst):
                await pg.set_content(htm); await pg.wait_for_timeout(500)
                await pg.screenshot(path=OUT+f'{k}-{i+1}.png')
        await b.close()
asyncio.run(main())
