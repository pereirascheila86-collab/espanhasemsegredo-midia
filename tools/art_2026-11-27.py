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

# ============ NOTICIA: como votar 29N ============
def ico(g,x,y,s): return svg('0 0 200 200',g,s,s,f'left:{x}px;top:{y}px')
def urn(x,y,s=1.0):
    g=f'<ellipse cx="450" cy="590" rx="400" ry="30" fill="{INK}" opacity=".35"/>'
    g+=f'<g transform="rotate(-11 380 150)"><rect x="300" y="20" width="170" height="260" rx="6" fill="{IV}" stroke="{G}" stroke-width="5"/><path d="M300 20L385 92L470 20" fill="none" stroke="{G}" stroke-width="5"/></g>'
    g+=f'<g transform="rotate(10 560 150)"><rect x="480" y="40" width="170" height="260" rx="6" fill="{SAND}" stroke="{G}" stroke-width="5"/><path d="M480 40L565 112L650 40" fill="none" stroke="{G}" stroke-width="5"/></g>'
    g+=f'<path d="M180 240H720L760 580H140Z" fill="{IV}" fill-opacity=".16" stroke="{IV}" stroke-width="8" stroke-linejoin="round"/>'
    g+=f'<rect x="150" y="206" width="600" height="52" rx="14" fill="{GOLD}"/><rect x="290" y="224" width="320" height="15" rx="7" fill="{INK}"/>'
    for px,py,r,c in [(260,520,-14,IV),(390,540,8,SAND),(520,515,-5,IV),(610,545,17,SAND),(430,490,24,IV)]:
        g+=f'<rect x="{px}" y="{py-34}" width="120" height="68" rx="5" fill="{c}" opacity=".92" transform="rotate({r} {px+60} {py})"/>'
    g+=f'<path d="M215 290L190 540" stroke="{IV}" stroke-width="14" stroke-linecap="round" opacity=".35"/>'
    return svg('0 0 900 630',g,int(900*s),int(630*s),f'left:{x}px;top:{y}px')
def a_clock():
    g=f'<circle cx="460" cy="260" r="235" fill="{IV}" stroke="{GOLD}" stroke-width="20"/>'
    for i in range(12):
        a=math.radians(i*30); g+=f'<path d="M{460+190*math.sin(a):.0f} {260-190*math.cos(a):.0f}L{460+210*math.sin(a):.0f} {260-210*math.cos(a):.0f}" stroke="{G}" stroke-width="9" stroke-linecap="round"/>'
    g+=f'<path d="M460 260H330M460 260L545 335" stroke="{G}" stroke-width="18" stroke-linecap="round"/><circle cx="460" cy="260" r="20" fill="{TERRA}"/>'
    g+=T(90,285,'9h',84,GOLD,'Lora')+T(835,285,'20h',84,GOLD,'Lora')
    return g
def a_ids():
    g=f'<g transform="rotate(-9 250 270)"><rect x="60" y="130" width="400" height="260" rx="26" fill="{G}"/>'+f'<rect x="92" y="190" width="120" height="150" rx="12" fill="{SAND}"/><circle cx="152" cy="240" r="30" fill="{TERRA}"/><path d="M106 340C106 266 198 266 198 340Z" fill="{TERRA}"/><path d="M244 220H420M244 262H390M244 304H420" stroke="{IV}" stroke-width="14" stroke-linecap="round"/>'+T(110,172,'DNI',34,GOLD,'Inter',800,6)+'</g>'
    g+=f'<rect x="505" y="80" width="260" height="350" rx="20" fill="{TERRA}"/><circle cx="635" cy="230" r="70" fill="none" stroke="{GOLD}" stroke-width="8"/><path d="M565 230H705M635 160C590 200 590 260 635 300C680 260 680 200 635 160" fill="none" stroke="{GOLD}" stroke-width="6"/>'+T(635,370,'PASSAPORTE',28,IV,'Inter',700,3)
    g+=f'<circle cx="780" cy="420" r="72" fill="{GOLD}"/><path d="M745 422L772 448L818 394" fill="none" stroke="{G}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
    return g
def a_school():
    g=f'<path d="M70 480H850" stroke="{SAND}" stroke-width="10" stroke-linecap="round"/><path d="M140 475V250L370 130L600 250V475Z" fill="{SAND}"/><path d="M110 268L370 120L630 268" fill="none" stroke="{GOLD}" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/><path d="M320 475V370Q320 320 370 320T420 370V475Z" fill="{G}"/>'
    for px in (180,490):
        g+=f'<rect x="{px}" y="300" width="70" height="80" rx="8" fill="{TERRA}"/>'
    g+=f'<circle cx="370" cy="230" r="34" fill="{IV}" stroke="{G}" stroke-width="8"/>'
    g+=f'<path d="M735 460C660 360 635 320 635 260C635 200 680 160 735 160S835 200 835 260C835 320 810 360 735 460Z" fill="{TERRA}" stroke="{IV}" stroke-width="10"/><circle cx="735" cy="258" r="36" fill="{IV}"/>'
    return g
def a_mail():
    g=f'<path d="M150 460V190Q150 60 300 60T450 190V460Z" fill="{G2}"/><rect x="210" y="170" width="180" height="26" rx="13" fill="{INK}"/><rect x="262" y="460" width="76" height="40" fill="{G}"/><path d="M110 500H500" stroke="{G}" stroke-width="12" stroke-linecap="round"/>'+T(300,300,'CORREOS',40,GOLD,'Inter',800,3)
    g+=f'<path d="M545 270H625" stroke="{GOLD}" stroke-width="14" stroke-linecap="round"/><circle cx="730" cy="270" r="130" fill="{IV}" stroke="{TERRA}" stroke-width="22"/><path d="M638 362L822 178" stroke="{TERRA}" stroke-width="22"/>'
    g+=f'<circle cx="730" cy="225" r="30" fill="{G}"/><path d="M675 345C675 250 785 250 785 345Z" fill="{G}"/><path d="M638 362L822 178" stroke="{TERRA}" stroke-width="22"/>'
    return g
def a_leave():
    g=f'<rect x="80" y="170" width="420" height="290" rx="34" fill="{IV}"/><path d="M195 170V120Q195 90 228 90H352Q385 90 385 120V170" fill="none" stroke="{IV}" stroke-width="26"/><path d="M80 290H500" stroke="{G}" stroke-width="12"/><rect x="250" y="255" width="80" height="70" rx="14" fill="{GOLD}"/>'
    g+=f'<circle cx="665" cy="285" r="170" fill="{G}" stroke="{GOLD}" stroke-width="16"/><path d="M665 285V115A170 170 0 0 1 825 342Z" fill="{GOLD}" opacity=".3"/>'+T(665,320,'4h',120,IV,'Lora')+T(665,385,'ATÉ',30,GOLD,'Inter',800,6)
    return g
def nslide(bg,fg,acc,panel,k,art,tt,tx,tsz=76):
    inner=f"""{bracket(acc)}{kick(k,acc)}
    {at(80,180,'',920,f'height:520px;border-radius:30px;background:{panel}')}
    {svg('0 0 920 540',art,920,540,'left:80px;top:170px')}
    {title(tt,fg,750,tsz)}{rule(886,acc)}{body(tx,fg,930,45)}{foot(fg)}"""
    return page(1350,bg,inner)
def n_cover():
    inner=f"""{bracket(GOLD)}{kick('Notícia · Espanha',GOLD)}
    {title(f'Eleições neste domingo, 29/11: <span style="color:{GOLD};font-style:italic">como votar</span> na Espanha',IV,170,94)}
    {urn(171,600,.82)}
    {at(80,1135,f'<div style="display:inline-block;background:{GOLD};color:{G};font-size:32px;font-weight:700;letter-spacing:.1em;padding:14px 30px;border-radius:10px">HORÁRIO E DOCUMENTOS · DESLIZE →</div>')}
    {foot(IV)}"""
    return page(1350,G,inner)
NOT=[n_cover(),
 nslide(IV,G,TERRA,G,'Horário',a_clock(),'Das 9h às 20h','Quem às 20h já estiver no local, ou na fila de entrada, ainda pode votar para o Congresso e o Senado.',84),
 nslide(G,IV,GOLD,IV,'Documento',a_ids(),'Leve o original com foto','<b>DNI, passaporte ou carteira de motorista</b>, mesmo vencidos. Não valem fotocópias nem o protocolo do DNI em andamento.',70),
 nslide(TERRA,IV,SAND,G,'Local de votação',a_school(),'Onde votar','A <b>tarjeta censal</b> indica colégio e mesa; ela não é obrigatória para votar. O INE também oferece consulta.',84),
 nslide(IV,G,TERRA,SAND,'Voto por correio',a_mail(),'Pediu pelo correio?','Com o pedido de voto por correio aceito, <b>não é possível</b> votar presencialmente na mesa no domingo.',76),
 nslide(G,IV,GOLD,TERRA,'Trabalho',a_leave(),'Vai trabalhar no domingo?','Há licença remunerada de <b>até quatro horas</b> para votar. O tempo depende da jornada; se reduzida, é proporcional.',64),
 closing(1350,IV,G,TERRA,'Fontes: La Moncloa (24/11/2026), Telemadrid (11/11/2026) e Estrella Digital (27/11/2026).<br>Consulta em 27/11/2026.')]

# ============ IMIGRAÇÃO: vítimas (arco lateral) ============
def doorway(x,y):
    g=f'<path d="M0 640H920" stroke="{G}" stroke-width="10"/>'
    g+=f'<path d="M250 640V260C250 40 670 40 670 260V640Z" fill="{G}"/><path d="M300 640V272C300 105 620 105 620 272V640Z" fill="{GOLD}"/>'
    g+=f'<path d="M300 640V272C300 190 340 150 392 138V600Z" fill="{G2}"/><circle cx="368" cy="410" r="14" fill="{GOLD}"/>'
    g+=f'<path d="M300 640H620L840 760H110Z" fill="{SAND}"/>'
    for i in range(9):
        a=math.radians(-60+i*15)
        g+=f'<path d="M{505+95*math.sin(a):.0f} {360-95*math.cos(a):.0f}L{505+140*math.sin(a):.0f} {360-140*math.cos(a):.0f}" stroke="{IV}" stroke-width="9" stroke-linecap="round" opacity=".85"/>'
    g+=f'<circle cx="505" cy="360" r="62" fill="{IV}"/>'
    for sx,m in [(140,1),(780,-1)]:
        g+=f'<g transform="translate({sx} 640) scale({m} 1)"><path d="M0 0V-240" stroke="{G2}" stroke-width="12" stroke-linecap="round"/>'+''.join(f'<path d="M0 {yy}C-90 {yy-10} -90 {yy-80} -80 {yy-85}C-20 {yy-75} 0 {yy-40} 0 {yy}Z" fill="{TERRA}"/><path d="M0 {yy-34}C80 {yy-40} 82 {yy-105} 72 {yy-112}C20 {yy-100} 0 {yy-70} 0 {yy-34}Z" fill="{G2}"/>' for yy in (-40,-140))+'</g>'
    return svg('0 0 920 760',g,920,760,f'left:{x}px;top:{y}px')
def i_cover():
    inner=f"""{bracket(GOLD)}{kick('Imigração · Proteção',TERRA)}
    {title(f'Vítimas estrangeiras de <span style="color:{TERRA};font-style:italic">violência ou tráfico</span>: o que a norma prevê',G,170,86)}
    {doorway(80,440)}
    {foot(G)}{at(780,1250,f'<span class=kick style="color:{TERRA};font-size:26px">Deslize →</span>',240)}"""
    return page(1350,IV,inner)
def e_shield(a,b): return f'<path d="M100 10L176 38V98C176 146 142 176 100 192C58 176 24 146 24 98V38Z" fill="{a}"/><circle cx="100" cy="78" r="24" fill="{b}"/><path d="M58 148C58 98 142 98 142 148C128 160 115 168 100 174C85 168 72 160 58 148Z" fill="{b}"/>'
def e_children(a,b): return f'<path d="M14 92C14 20 186 20 186 92Z" fill="{a}"/><path d="M100 28V16" stroke="{a}" stroke-width="10" stroke-linecap="round"/><circle cx="70" cy="122" r="19" fill="{b}"/><path d="M40 186C40 134 100 134 100 186Z" fill="{b}"/><circle cx="136" cy="134" r="15" fill="{a}"/><path d="M112 186C112 146 160 146 160 186Z" fill="{a}"/>'
def e_chain(a,b): return f'<g fill="none" stroke-width="18" stroke-linecap="round"><path d="M82 118L58 142C42 158 18 134 34 118L66 86C78 74 92 76 100 86" stroke="{a}"/><path d="M118 82L142 58C158 42 182 66 166 82L134 114C122 126 108 124 100 114" stroke="{a}"/><path d="M62 44L74 66M36 68L60 78M138 156L126 134M164 132L140 122" stroke="{b}" stroke-width="11"/></g>'
def e_witness(a,b): return f'<path d="M20 28H138Q154 28 154 44V104Q154 120 138 120H78L40 150V120H20Q8 120 8 104V44Q8 28 20 28Z" fill="{a}"/><path d="M36 60H126M36 88H100" stroke="{b}" stroke-width="12" stroke-linecap="round"/><circle cx="140" cy="130" r="40" fill="{b}" stroke="{a}" stroke-width="10"/><path d="M168 160L192 188" stroke="{a}" stroke-width="18" stroke-linecap="round"/>'
def e_phone(a,b): return f'<path d="M52 20L84 24L98 68L76 84C88 112 108 132 136 144L154 122L192 138L190 170C186 184 172 190 158 188C84 178 22 118 14 44C13 30 22 22 36 20Z" fill="{a}"/><path d="M118 26C150 30 172 52 176 84M116 56C132 60 142 70 146 86" fill="none" stroke="{b}" stroke-width="13" stroke-linecap="round"/>'
def islide(side,bg,fg,acc,k,icon,ia,ib,tt,tx,tsz=76,extra=''):
    inner=f"""{at(0,0,'',250,f'height:1350px;background:{side}')}
    {ico(icon(ia,ib),35,150,180)}
    {at(125,370,'',6,f'height:780px;background:{acc};opacity:.7')}
    {bracket(acc)}{at(320,110,f'<span class=kick style="color:{acc}">{k}</span>',640)}
    {at(320,390,f'<div class=serif style="font-size:{tsz}px;line-height:1.1;font-weight:700;color:{fg}">{tt}</div><div style="width:130px;height:5px;background:{acc};margin:40px 0 44px"></div><div style="font-size:52px;line-height:1.48;color:{fg}">{tx}</div>{extra}',680)}
    <div class=foot style="left:320px"><div class=l><img src="{LOGO}"><span class=n style="color:{fg}">Espanha Sem Segredo</span></div></div>"""
    return page(1350,bg,inner)
help_=f'<div style="display:flex;gap:22px;margin-top:56px"><div style="flex:1;border:4px solid {GOLD};border-radius:20px;text-align:center;padding:22px 0"><div class=serif style="font-size:110px;font-weight:700;color:{GOLD}">016</div></div><div style="flex:1;border:4px solid {GOLD};border-radius:20px;text-align:center;padding:22px 0"><div class=serif style="font-size:110px;font-weight:700;color:{GOLD}">112</div></div></div>'
IMG=[i_cover(),
 islide(G,IV,G,TERRA,'Violência de gênero',e_shield,IV,TERRA,'Com ou sem situação regular','Mulheres estrangeiras vítimas na Espanha podem pedir residência e trabalho por <b>circunstâncias excepcionais</b>. A autorização definitiva dura cinco anos.'),
 islide(TERRA,G,IV,GOLD,'Violência sexual',e_children,IV,G,'Também meninas e meninos','A ficha abrange mulheres, meninas e meninos estrangeiros vítimas, <b>independentemente da situação administrativa</b>. Há proteção específica para menores.'),
 islide(GOLD,IV,G,TERRA,'Tráfico de pessoas',e_chain,G,IV,'Tempo para se recuperar e refletir','A norma prevê período de <b>pelo menos 90 dias</b>, com estada autorizada e suspensão do procedimento sancionador.',72),
 islide(G2,IV,G,TERRA,'Colaboração',e_witness,IV,GOLD,'Quem colabora contra redes','Vítimas, prejudicados ou testemunhas de tráfico ilícito de mão de obra ou exploração sexual. As autoridades decidem sobre a <b>isenção da sanção</b>.'),
 islide(TERRA,G,IV,GOLD,'Ajuda',e_phone,IV,G,'Precisa de apoio?','<b>016</b>: violência contra a mulher; gratuito, confidencial, 24 horas, 53 idiomas por telefone. Emergência: <b>112</b>.',82,help_),
 closing(1350,G,IV,GOLD,'Fontes: Ministerio de Inclusión, Hojas 35, 35 bis, 37 e 38 (maio/2025);<br>Ministerio de Igualdad, serviço 016. Consulta em 27/11/2026.')]

# ============ REEL: Tribunal das Águas ============
def gothic(y):
    g=f'<rect x="60" y="0" width="760" height="800" fill="{SAND}"/>'
    for k,(c,o) in enumerate([(G,0),(TERRA,48),(G2,96),(GOLD,144),(INK,180)]):
        l=130+o*0.9; r=750-o*0.9; top=40+o
        g+=f'<path d="M{l} 800V{top+340}C{l} {top+160} {l+150} {top+40} 440 {top}C{r-150} {top+40} {r} {top+160} {r} {top+340}V800Z" fill="{c}"/>'
    g+=f'<circle cx="440" cy="370" r="50" fill="none" stroke="{GOLD}" stroke-width="9"/>'+''.join(f'<path d="M440 370L{440+48*math.cos(math.radians(a)):.0f} {370+48*math.sin(math.radians(a)):.0f}" stroke="{GOLD}" stroke-width="6"/>' for a in range(0,360,45))
    for i in range(8):
        cx=100+i*97; cy=705+(-1)**0*abs(i-3.5)*18
        g+=f'<circle cx="{cx}" cy="{cy-66}" r="26" fill="{IV}" stroke="{INK}" stroke-width="5"/><path d="M{cx-36} {cy+40}C{cx-36} {cy-50} {cx+36} {cy-50} {cx+36} {cy+40}Z" fill="{IV}" stroke="{INK}" stroke-width="5"/><path d="M{cx-40} {cy+40}H{cx+40}M{cx-30} {cy+40}V{cy+86}M{cx+30} {cy+40}V{cy+86}" stroke="{TERRA}" stroke-width="10" stroke-linecap="round"/>'
    return svg('0 0 880 830',g,880,830,f'left:100px;top:{y}px')
def thursday(y):
    g=f'<rect x="60" y="60" width="500" height="480" rx="34" fill="{IV}"/><path d="M60 190V94Q60 60 94 60H526Q560 60 560 94V190Z" fill="{G}"/>'+''.join(f'<rect x="{px}" y="20" width="28" height="90" rx="14" fill="{GOLD}"/>' for px in (160,432))
    g+=T(310,160,'TODA SEMANA',38,IV,'Inter',800,5)+T(310,350,'quinta',130,TERRA,'Lora')+T(310,465,'12h',92,G,'Lora')
    g+=f'<path d="M610 560V260C610 190 700 120 725 105C750 120 840 190 840 260V560Z" fill="{G}"/><path d="M652 560V285C652 235 705 190 725 178C745 190 798 235 798 285V560Z" fill="{GOLD}"/><path d="M725 180V560" stroke="{G}" stroke-width="8"/><path d="M30 565H860" stroke="{SAND}" stroke-width="14" stroke-linecap="round"/>'
    return svg('0 0 880 600',g,880,600,f'left:100px;top:{y}px')
def canals(y):
    g=f'<rect x="0" y="0" width="880" height="640" rx="40" fill="{SAND}"/>'
    for i in range(4):
        for j in range(5):
            c=[G2,TERRA,GOLD][(i+j)%3]
            g+=f'<rect x="{26+j*169}" y="{26+i*150}" width="150" height="132" rx="14" fill="{c}" opacity=".42"/>'
    main='M440 640C440 560 390 520 440 450'
    g+=f'<path d="{main}" fill="none" stroke="{G}" stroke-width="40" stroke-linecap="round"/>'
    for ex,ey in [(40,470),(60,320),(130,150),(300,30),(560,40),(740,140),(840,300),(830,480)]:
        g+=f'<path d="M440 450C440 {ey+90} {(ex+440)//2} {ey+60} {ex} {ey}" fill="none" stroke="{G}" stroke-width="17" stroke-linecap="round"/><circle cx="{ex}" cy="{ey}" r="19" fill="{IV}" stroke="{G}" stroke-width="8"/>'
    g+=f'<circle cx="440" cy="450" r="62" fill="{IV}" stroke="{G}" stroke-width="12"/>'+T(440,475,'8',72,TERRA,'Lora')
    return svg('0 0 880 640',g,880,640,f'left:100px;top:{y}px')
def voices(y):
    g=f'<path d="M40 40H520Q560 40 560 80V260Q560 300 520 300H250L150 380V300H80Q40 300 40 260V80Q40 40 80 40Z" fill="{IV}"/>'+T(300,205,'em valenciano',58,G,'Lora')
    g+=f'<path d="M420 360H800Q840 360 840 400V500Q840 540 800 540H760V610L680 540H420Q380 540 380 500V400Q380 360 420 360Z" fill="{GOLD}"/>'+''.join(f'<circle cx="{x}" cy="450" r="22" fill="{G}"/>' for x in (530,610,690))
    g+=f'<circle cx="720" cy="160" r="130" fill="{TERRA}" stroke="{IV}" stroke-width="10"/>'+T(720,155,'UNESCO',40,IV,'Inter',800,3)+T(720,225,'2009',66,IV,'Lora')
    return svg('0 0 880 630',g,880,630,f'left:100px;top:{y}px')
def reel(bg,acc,fg,inner):
    return page(1920,bg,f"""{bracket(acc)}{at(80,110,f'<span class=kick style="color:{acc}">VOCÊ SABIA? | ESPANHA</span>')}{inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{fg}">Espanha Sem Segredo</span></div></div>""")
RR=[
 reel(IV,TERRA,G,title(f'Em Valência, um tribunal se reúne à <span style="color:{TERRA};font-style:italic">porta da catedral</span>',G,240,100)+gothic(780)),
 reel(TERRA,SAND,IV,title(f'O Tribunal das <span style="color:{SAND};font-style:italic">Águas</span>',IV,240,104)+body('Reúne-se às quintas, ao meio-dia, na <b>Porta dos Apóstolos</b>. Se a quinta for feriado, a sessão passa para quarta.',IV,560,50)+thursday(1030)),
 reel(G,GOLD,IV,title(f'Quem <span style="color:{GOLD};font-style:italic">julga</span>',IV,240,108)+body('<b>Oito agricultores</b>, representantes dos canais de irrigação que levam água do rio Turia à horta. São eleitos democraticamente a cada dois anos.',IV,460,50)+canals(980)),
 reel(G2,GOLD,IV,title(f'Só com a <span style="color:{GOLD};font-style:italic">palavra</span>',IV,240,104)+body('Julgamento oral, em valenciano, sem advogados nem documentos; a decisão não admite recurso. Em <b>2009</b>, os tribunais de irrigantes de Valência e Múrcia entraram na UNESCO como patrimônio imaterial.',IV,440,48)+voices(1060)),
 closing(1920,IV,G,TERRA,'Fontes: UNESCO; Visit València; Tribunal de las Aguas<br>(tribunaldelasaguas.org). Consulta em 27/11/2026.',logo=460,serif_sz=88,top=.17)]

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
