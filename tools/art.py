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

# ---------- icons (viewBox 200) ----------
def ic_doc(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M50 20H125L160 55V175H50Z" fill="{b}" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><path d="M125 20V55H160" fill="none" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><g stroke="{a}" stroke-width="6" stroke-linecap="round"><path d="M70 85H140M70 105H140M70 125H112"/></g><circle cx="142" cy="150" r="26" fill="{a}"/><path d="M130 170L124 196L142 186L160 196L154 170Z" fill="{a}"/><path d="M130 150L139 159L155 141" fill="none" stroke="{b}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_heart(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 172C45 130 24 98 24 68C24 42 44 26 66 26C82 26 94 35 100 48C106 35 118 26 134 26C156 26 176 42 176 68C176 98 155 130 100 172Z" fill="{a}"/><path d="M100 70V118M76 94H124" stroke="{b}" stroke-width="12" stroke-linecap="round"/></svg>'''
def ic_workstudy(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M20 62L82 40L100 100L38 122Z" fill="{a}"/><path d="M82 40L144 62L126 122L100 100Z" fill="{b}" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><rect x="92" y="108" width="88" height="62" rx="8" fill="{a}"/><path d="M120 108V98C120 92 124 88 130 88H142C148 88 152 92 152 98V108" fill="none" stroke="{a}" stroke-width="6"/><path d="M92 136H180" stroke="{b}" stroke-width="5"/><rect x="128" y="130" width="16" height="14" rx="3" fill="{b}"/></svg>'''
def ic_check(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="30" width="120" height="150" rx="12" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="72" y="16" width="56" height="30" rx="10" fill="{a}"/><g stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M60 82L68 90L82 74M60 114L68 122L82 106M60 146L68 154L82 138"/><path d="M96 82H142M96 114H142M96 146H130"/></g></svg>'''
def ic_cap(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 28L184 66L100 104L16 66Z" fill="{a}"/><path d="M50 90V128C50 144 150 144 150 128V90L100 114Z" fill="{a}" opacity=".85"/><path d="M176 72V124" stroke="{a}" stroke-width="6" stroke-linecap="round"/><circle cx="176" cy="130" r="9" fill="{b}" stroke="{a}" stroke-width="4"/><rect x="62" y="146" width="76" height="40" rx="8" fill="{b}" stroke="{a}" stroke-width="5"/><text x="100" y="175" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" fill="{a}">IA</text></svg>'''
def ic_person(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="64" r="34" fill="{a}"/><path d="M36 182C36 138 62 114 100 114C138 114 164 138 164 182Z" fill="{a}"/><rect x="124" y="116" width="46" height="62" rx="12" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M134 140H160" stroke="{a}" stroke-width="5" stroke-linecap="round"/></svg>'''
def ic_consulate(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 22L180 70H20Z" fill="{a}"/><g fill="{a}"><rect x="34" y="82" width="20" height="78"/><rect x="72" y="82" width="20" height="78"/><rect x="108" y="82" width="20" height="78"/><rect x="146" y="82" width="20" height="78"/></g><rect x="22" y="164" width="156" height="14" rx="3" fill="{a}"/><circle cx="100" cy="52" r="9" fill="{b}"/></svg>'''
def ic_shield(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 18L168 42V98C168 140 138 168 100 184C62 168 32 140 32 98V42Z" fill="{a}"/><path d="M100 64V132M66 98H134" stroke="{b}" stroke-width="16" stroke-linecap="round"/></svg>'''
def ic_house(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 24L184 94H16Z" fill="{a}"/><rect x="34" y="92" width="132" height="86" fill="{a}"/><rect x="82" y="120" width="36" height="58" rx="18" fill="{b}"/><rect x="48" y="108" width="24" height="24" rx="4" fill="{b}"/><rect x="128" y="108" width="24" height="24" rx="4" fill="{b}"/></svg>'''
def ic_alert(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 22L184 168H16Z" fill="{a}" stroke="{a}" stroke-width="10" stroke-linejoin="round"/><path d="M100 70V122" stroke="{b}" stroke-width="14" stroke-linecap="round"/><circle cx="100" cy="146" r="9" fill="{b}"/></svg>'''
def ic_coin(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="74" fill="{a}"/><circle cx="100" cy="100" r="56" fill="none" stroke="{b}" stroke-width="5"/><path d="M118 74C110 66 88 66 84 80C80 96 116 96 114 114C112 130 88 132 80 124M100 58V142" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round"/></svg>'''

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

# ---------- NOTÍCIA ----------
def facade(col,fill,acc):
    # stylised university facade (plateresque): central tower with pediment, arcades, rosettes
    s=f'<g stroke="{col}" stroke-width="3" fill="{fill}">'
    s+='<rect x="40" y="330" width="720" height="150"/>'
    s+='<rect x="250" y="190" width="300" height="290"/>'
    s+='<path d="M230 190L400 90L570 190Z"/>'
    s+='<path d="M400 40V90" stroke-width="5"/><path d="M400 40L440 52L400 66Z" fill="%s" stroke="none"/>'%acc
    s+='</g>'
    for i in range(6):
        x=70+i*110 if i<3 else 70+i*110+0
    for x in [70,170,270+0,0]:
        pass
    # side arcades
    for x in [64,148,232,566,650,734-0]:
        s+=f'<path d="M{x} 480V400C{x} 370 {x+56} 370 {x+56} 400V480Z" fill="{col}"/>'
    # central big arch door + windows
    s+=f'<path d="M340 480V380C340 330 460 330 460 380V480Z" fill="{col}"/>'
    s+=f'<circle cx="400" cy="244" r="38" fill="none" stroke="{acc}" stroke-width="5"/><circle cx="400" cy="244" r="20" fill="{acc}"/>'
    for x in [282,498]:
        s+=f'<path d="M{x} 330V290C{x} 268 {x+36} 268 {x+36} 290V330Z" fill="{col}"/>'
    s+=f'<path d="M20 480H780" stroke="{col}" stroke-width="8"/>'
    return f'<svg width="800" height="500" viewBox="0 0 800 500">{s}</svg>'

def noticia_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{IV} 0%,{SAND} 100%)"></div>
    <div class=abs style="left:-90px;top:-120px;width:560px;height:560px;border-radius:50%;background:{GOLD};opacity:.28"></div>
    <div class=abs style="left:560px;top:330px;width:540px;height:540px;border-radius:50%;background:{TERRA};opacity:.9"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Notícia · Espanha</span></div>
    <div class=abs serif style="left:80px;top:170px;width:900px;font-size:108px;line-height:1.04;font-weight:700;color:{G}">Governo aprova o novo <span style="color:{TERRA};font-style:italic">Estatuto</span> do Estudantado</div>
    <div class=abs style="left:140px;top:660px">{facade(G,IV,GOLD)}</div>
    <div class=abs style="left:640px;top:620px;width:340px;transform:rotate(-6deg);background:{G};color:{IV};padding:22px 28px;border-radius:14px;border:3px solid {GOLD}">
      <div style="font-size:20px;letter-spacing:.2em;font-weight:700;color:{GOLD}">REAL DECRETO 855/2026</div>
      <div class=serif style="font-size:44px;font-weight:700;line-height:1.1;margin-top:6px">Em vigor desde 23/10</div></div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,IV,inner)

def closing(h,bg,fg,acc,srcs,logo=360,serif_sz=70,pad=80,top=.12):
    inner=f'''{bracket(acc)}
    <div class=abs style="left:0;right:0;top:{int(h*top)}px;display:flex;justify-content:center"><img src="{LOGO}" width="{logo}" height="{logo}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60}px;text-align:center;font-size:{serif_sz}px;line-height:1.14;font-weight:700;color:{fg}">Aqui você fica por dentro de tudo sobre a Espanha</div>
    <div class=abs style="left:50%;margin-left:-65px;top:{int(h*top)+logo+60+serif_sz*3+50}px;width:130px;height:5px;background:{acc}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3+90}px;text-align:center;font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
    <div class=abs style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3+170}px;text-align:center;font-size:40px;color:{fg}">Siga <b>@espanhasemsegredo</b></div>
    <div class=abs style="left:{pad+20}px;right:{pad+20}px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg};opacity:.85">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>'''
    return page(h,bg,inner)

NOT=[noticia_cover()]
T=7
NOT.append(content(2,T,'Notícia · O que é','O novo estatuto','Substitui o estatuto de 2010 (RD 1791/2010) e vale para universidades <b>públicas e privadas</b>. Real Decreto 855/2026, em vigor desde 23/10/2026.',ic_doc,'ivory'))
NOT.append(content(3,T,'Notícia · Saúde mental','Saúde mental e proteção','Atendimento psicológico e de saúde mental <b>gratuito e acessível</b> (art. 6) e protocolos contra assédio e ciberassédio (art. 10).',ic_heart,'green'))
NOT.append(content(4,T,'Notícia · Rotina','Estudar e trabalhar','Direito de <b>compaginar estudos e trabalho</b>, de cursar a tempo parcial e de suspender os estudos, conforme a regra de cada universidade. Mais acessibilidade para estudantes com deficiência.',ic_workstudy,'terra'))
NOT.append(content(5,T,'Notícia · Avaliação','Avaliação mais clara','Acesso aos planos docentes <b>antes da matrícula</b>. Os critérios de avaliação não mudam depois da matrícula, salvo com motivação e acordo.',ic_check,'ivory'))
NOT.append(content(6,T,'Notícia · Bolsas e IA','Bolsas, mobilidade e IA','Bolsas estatais valem em <b>todo o território nacional</b>, com direito a programas de mobilidade. E há o dever de evitar fraudes, em especial o uso inapropriado de IA generativa.',ic_cap,'green'))
NOT.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: BOE (22/10/2026) e Ministerio de Ciencia, Innovación y Universidades.<br>Consulta em 24/10/2026.'))

# ---------- INTERCÂMBIO ----------
def stamp(col,txt1,txt2,size=520,rot=-12):
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 400 400" style="transform:rotate({rot}deg)"><defs><path id="c1" d="M200 200m-150 0a150 150 0 1 1 300 0a150 150 0 1 1 -300 0"/></defs>
    <circle cx="200" cy="200" r="188" fill="none" stroke="{col}" stroke-width="7"/><circle cx="200" cy="200" r="170" fill="none" stroke="{col}" stroke-width="2.5"/><circle cx="200" cy="200" r="104" fill="none" stroke="{col}" stroke-width="2.5"/>
    <text font-family="Inter" font-weight="800" font-size="30" letter-spacing="9" fill="{col}"><textPath href="#c1" startOffset="0">{txt1}</textPath></text>
    <text x="200" y="196" text-anchor="middle" font-family="Lora" font-weight="700" font-size="62" fill="{col}">ESPAÑA</text>
    <text x="200" y="246" text-anchor="middle" font-family="Inter" font-weight="700" font-size="26" letter-spacing="6" fill="{col}">{txt2}</text>
    <path d="M150 268H250" stroke="{col}" stroke-width="4"/></svg>'''
def inter_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:{G}"></div>
    <div class=abs style="left:0;top:0;width:1080px;height:1350px;background:repeating-linear-gradient(135deg,rgba(201,162,74,.07) 0 2px,transparent 2px 38px)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Estudos</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:920px;font-size:112px;line-height:1.03;font-weight:700;color:{IV}">Intercâmbio <span style="color:{GOLD};font-style:italic">escolar</span> na Espanha</div>
    <div class=abs style="left:470px;top:700px;opacity:.95">{stamp(GOLD,'AUTORIZAÇÃO · DE · ESTÂNCIA · POR · MOBILIDADE ·','ALUNOS',600,-10)}</div>
    <div class=abs style="left:80px;top:700px;width:400px;font-size:38px;line-height:1.4;color:{IV}">Qual autorização é necessária para estudar o <b>ensino secundário</b> na Espanha por mais de 90 dias?</div>
    <div class=abs style="left:80px;top:1130px;font-size:30px;font-weight:600;letter-spacing:.14em;color:{GOLD}">DESLIZE  →</div>
    <svg class=abs style="left:0;bottom:150px;opacity:0" width="1080" height="150" viewBox="0 0 1080 150"><path d="M0 150Q540 40 1080 150" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="4 14" stroke-linecap="round"/></svg>
    {foot(GOLD)}'''
    return page(1350,G,inner)
INT=[inter_cover()]
T=7
INT.append(content(2,T,'Imigração · Para quem é','Para quem é','Aluno estrangeiro de <b>ensino secundário</b> em programa de mobilidade, com estadia superior a 90 dias e limite de 1 ano. Não vale para cidadãos da UE, do EEE ou da Suíça.',ic_person,'ivory'))
INT.append(content(3,T,'Imigração · Onde pedir','Onde pedir','<b>Pessoalmente</b>, na Missão Diplomática ou Consulado da Espanha da área de residência. Se for menor, é preciso autorização dos pais ou tutores. A taxa é paga no pedido.',ic_consulate,'terra'))
INT.append(content(4,T,'Imigração · Condições','Condições exigidas','Admissão em centro de ensino e programa de mobilidade, <b>seguro de saúde</b> com entidade autorizada na Espanha, e custos assumidos pela organização ou pelo centro.',ic_shield,'ivory'))
INT.append(content(5,T,'Imigração · Alojamento','Alojamento e documentos','Família selecionada pela organização, internato ou residência do programa. <b>Passaporte em vigor</b>, com validade mínima de um ano. Documentos estrangeiros: tradução juramentada e legalização ou apostila.',ic_house,'green'))
INT.append(content(6,T,'Imigração · Atenção','Atenção acima de 6 meses','O maior de idade apresenta <b>antecedentes criminais</b> e pede a TIE na polícia em até 1 mês da entrada. A ficha oficial prevê resposta do consulado em até 1 mês.',ic_alert,'terra'))
INT.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión (ficha atualizada em novembro de 2025).<br>Consulta em 24/10/2026.'))

# ---------- REEL cafés (1080x1920) ----------
def glass(x,y,w,h,layers,label,sub,foam=False,cup=False,col=IV):
    # layers: list of (fraction, color) bottom->top inside the vessel
    iw=w; ih=h
    clip=f'<clipPath id="k{x}{y}"><path d="M0 0H{iw}L{iw*.9} {ih-30}Q{iw*.9} {ih} {iw*.7} {ih}H{iw*.3}Q{iw*.1} {ih} {iw*.1} {ih-30}Z"/></clipPath>' if not cup else f'<clipPath id="k{x}{y}"><path d="M0 0H{iw}V{ih*.55}Q{iw} {ih} {iw*.5} {ih}Q0 {ih} 0 {ih*.55}Z"/></clipPath>'
    cy=0; rects=''
    for frac,c in layers:
        hh=ih*frac; cy+=hh
        rects=f'<rect x="-5" y="{ih-cy:.1f}" width="{iw+10}" height="{hh+1:.1f}" fill="{c}"/>'+rects
    fm=''
    if foam: fm=f'<path d="M-5 {ih-cy+10:.1f}q{iw*.12:.1f} -26 {iw*.25:.1f} 0t{iw*.25:.1f} 0t{iw*.25:.1f} 0t{iw*.25:.1f} 0V{ih-cy-30:.1f}H-5Z" fill="#F7EEDD"/>'
    shape=(f'<path d="M0 0H{iw}L{iw*.9} {ih-30}Q{iw*.9} {ih} {iw*.7} {ih}H{iw*.3}Q{iw*.1} {ih} {iw*.1} {ih-30}Z" fill="none" stroke="{col}" stroke-width="5" stroke-linejoin="round"/>' if not cup else
           f'<path d="M0 0H{iw}V{ih*.55}Q{iw} {ih} {iw*.5} {ih}Q0 {ih} 0 {ih*.55}Z" fill="none" stroke="{col}" stroke-width="5"/><path d="M{iw} {ih*.14}H{iw+34}Q{iw+74} {ih*.14} {iw+74} {ih*.34}Q{iw+74} {ih*.54} {iw+30} {ih*.58}" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/><path d="M{-30} {ih+14}H{iw+30}" stroke="{col}" stroke-width="7" stroke-linecap="round"/>')
    pad=90
    svg=f'<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{iw}" height="{ih+30}" viewBox="0 0 {iw} {ih+30}"><defs>{clip}</defs><g clip-path="url(#k{x}{y})">{rects}{fm}</g>{shape}</svg>'
    # steam
    st=''.join(f'<path d="M{x+iw*f:.0f} {y-26}c-16 -26 16 -40 0 -68" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" opacity=".5"/>' for f in (.3,.55,.8))
    lab=f'<div class=abs style="left:{x-60}px;width:{iw+(120 if not cup else 160)}px;top:{y+ih+70}px;text-align:center"><div class=serif style="font-size:50px;font-weight:700;color:{GOLD}">{label}</div><div style="font-size:30px;line-height:1.3;color:{col};opacity:.92;margin-top:6px">{sub}</div></div>'
    return f'<svg class=abs style="left:0;top:0;overflow:visible" width="1080" height="1920">{st}</svg>'+svg+lab

CAF='#4B2A1A'; MILK='#F1E3C8'; WATER='#C79A62'; COND='#F8F0DC'; ESP='#2E1810'; FOAM='#F7EEDD'
def reel_base(inner,n):
    return page(1920,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:radial-gradient(circle at 80% 8%,{G2} 0,{G} 60%)"></div>
    <div class=abs style="left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(135deg,rgba(201,162,74,.06) 0 2px,transparent 2px 42px)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{GOLD}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">{n} / 5</span></div>''')

R=[]
# tela 1
R.append(reel_base(f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:108px;line-height:1.05;font-weight:700;color:{IV}">Qual a diferença entre <span style="color:{GOLD};font-style:italic">cortado</span>, café con leche e outros?</div>
{glass(90,1010,150,260,[(1,ESP)],'','',col=IV)}
{glass(300,930,170,340,[(.75,WATER),(.25,CAF)],'','',col=IV)}
{glass(530,890,190,380,[(.5,CAF),(.5,MILK)],'','',col=IV,cup=False)}
{glass(780,950,180,320,[(.25,COND),(.5,ESP),(.25,FOAM)],'','',col=IV)}
<div class=abs style="left:80px;top:1480px;width:920px;font-size:46px;line-height:1.45;color:{IV}">Segundo o dicionário da Real Academia Española, cada nome diz o que vai na xícara.</div>''',1))
R.append(reel_base(f'''<div class="abs serif" style="left:80px;top:230px;font-size:96px;line-height:1.05;font-weight:700;color:{IV}">Café solo<br><span style="color:{GOLD}">e cortado</span></div>
{glass(140,640,320,700,[(1,ESP)],'Café solo','Só água e café moído, sem leite',col=IV)}
{glass(620,640,320,700,[(.2,MILK),(.8,ESP)],'Café cortado','Café com muito pouco leite',col=IV)}
<div class=abs style="left:80px;top:1640px;font-size:28px;color:{IV};opacity:.8">Definições: RAE, Diccionario de la lengua española</div>''',2))
R.append(reel_base(f'''<div class="abs serif" style="left:80px;top:230px;font-size:96px;line-height:1.05;font-weight:700;color:{IV}">Café con leche<br><span style="color:{GOLD}">e americano</span></div>
{glass(90,640,350,640,[(.5,CAF),(.5,MILK)],'Café con leche','Café com leite. O nome descreve a mistura',col=IV,cup=True)}
{glass(620,640,320,700,[(.8,WATER),(.2,ESP)],'Café americano','Preparado com mais água que o habitual',col=IV)}''',3))
R.append(reel_base(f'''<div class="abs serif" style="left:80px;top:230px;font-size:96px;line-height:1.05;font-weight:700;color:{IV}">Capuchino<br><span style="color:{GOLD}">e bombón</span></div>
{glass(110,640,350,640,[(.45,CAF),(.2,MILK),(.35,FOAM)],'Café capuchino','Café coberto com espuma de leite ou nata',col=IV,cup=True,foam=True)}
{glass(620,640,320,700,[(.35,COND),(.65,ESP)],'Café bombón','Café com leite condensado, muito conhecido na Espanha',col=IV)}''',4))
R.append(closing(1920,TERRA,IV,'#F3D79A','Fonte: RAE (Diccionario de la lengua española).<br>Consulta em 24/10/2026.',logo=460,serif_sz=88,top=.2))

async def main(only=None):
    sets={'noticia':NOT,'intercambio':INT,'cafe':R}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,lst in sets.items():
            if only and k not in only: continue
            h=1920 if k=='cafe' else 1350
            pg=await b.new_page(viewport={'width':1080,'height':h})
            for i,htm in enumerate(lst):
                await pg.set_content(htm); await pg.wait_for_timeout(500)
                await pg.screenshot(path=OUT+f'{k}-{i+1}.png')
        await b.close()
asyncio.run(main(sys.argv[1:] or None))
