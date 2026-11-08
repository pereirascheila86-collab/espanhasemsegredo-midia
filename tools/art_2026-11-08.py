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


def ic_doc(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M50 20H125L160 55V175H50Z" fill="{b}" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><path d="M125 20V55H160" fill="none" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><g stroke="{a}" stroke-width="6" stroke-linecap="round"><path d="M70 85H140M70 105H140M70 125H112"/></g><circle cx="142" cy="150" r="26" fill="{a}"/><path d="M130 170L124 196L142 186L160 196L154 170Z" fill="{a}"/><path d="M130 150L139 159L155 141" fill="none" stroke="{b}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
# ================= ÍCONES NOVOS (2026-11-08) =================
def ic_return(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M36 104A64 64 0 0 1 150 62" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round"/><path d="M168 40L172 86L128 76Z" fill="{a}"/><path d="M164 96A64 64 0 0 1 50 138" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round"/><path d="M32 160L28 114L72 124Z" fill="{a}"/><path d="M100 70L138 102H62Z" fill="{a}"/><rect x="70" y="100" width="60" height="42" fill="{a}"/><rect x="92" y="114" width="16" height="28" rx="8" fill="{b}"/></svg>'''
def ic_idcard(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="16" y="46" width="168" height="112" rx="14" fill="{a}"/><circle cx="64" cy="94" r="20" fill="{b}"/><path d="M30 144C30 122 46 114 64 114C82 114 98 122 98 144Z" fill="{b}"/><g stroke="{b}" stroke-width="7" stroke-linecap="round"><path d="M114 80H166M114 100H166M114 120H146"/></g><rect x="146" y="132" width="24" height="16" rx="4" fill="{b}" opacity=".0"/></svg>'''
def ic_embassy(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 50L172 92H28Z" fill="{a}"/><g fill="{a}"><rect x="40" y="100" width="18" height="62"/><rect x="76" y="100" width="18" height="62"/><rect x="106" y="100" width="18" height="62"/><rect x="142" y="100" width="18" height="62"/></g><rect x="26" y="166" width="148" height="14" rx="3" fill="{a}"/><path d="M100 50V12" stroke="{a}" stroke-width="6" stroke-linecap="round"/><path d="M100 14H140L128 26L140 38H100Z" fill="{b}"/></svg>'''
def ic_clock(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="78" fill="{a}"/><circle cx="100" cy="100" r="62" fill="{b}"/><g stroke="{a}" stroke-width="6" stroke-linecap="round"><path d="M100 48V54M100 146V152M48 100H54M146 100H152"/></g><path d="M100 100V62M100 100L128 116" stroke="{a}" stroke-width="9" stroke-linecap="round"/><circle cx="100" cy="100" r="8" fill="{a}"/></svg>'''
def ic_cal3(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="26" y="40" width="148" height="140" rx="16" fill="{a}"/><rect x="26" y="40" width="148" height="38" rx="16" fill="{b}"/><rect x="26" y="62" width="148" height="16" fill="{b}"/><g stroke="{a}" stroke-width="10" stroke-linecap="round"><path d="M64 22V50M136 22V50"/></g><text x="100" y="158" text-anchor="middle" font-family="Lora" font-weight="700" font-size="82" fill="{b}">3</text></svg>'''
def ic_clip(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="38" y="30" width="124" height="152" rx="12" fill="{a}"/><rect x="70" y="16" width="60" height="32" rx="10" fill="{b}"/><g stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M60 84L70 94L88 72M60 124L70 134L88 112"/><path d="M104 84H146M104 124H146"/></g><path d="M60 158H140" stroke="{b}" stroke-width="7" stroke-linecap="round" opacity=".6"/></svg>'''
def ic_lifebuoy(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><defs><clipPath id="rg"><path fill-rule="evenodd" d="M100 20A80 80 0 1 1 99.9 20ZM100 66A34 34 0 1 0 100.1 66Z"/></clipPath></defs><g clip-path="url(#rg)"><circle cx="100" cy="100" r="82" fill="{a}"/><circle cx="100" cy="100" r="57" fill="none" stroke="{b}" stroke-width="48" stroke-dasharray="30 59.5" stroke-dashoffset="-15"/></g></svg>'''
def ic_bag(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M76 34L88 56H112L124 34Q100 24 76 34Z" fill="{a}"/><path d="M88 56C40 84 26 124 34 150C42 178 158 178 166 150C174 124 160 84 112 56Z" fill="{a}"/><path d="M82 66H118" stroke="{b}" stroke-width="7" stroke-linecap="round"/><path d="M122 104C112 94 86 94 82 110C78 128 120 126 116 146C112 162 88 162 78 150M100 88V168" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round"/></svg>'''
def ic_report(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M46 20H126L160 54V180H46Z" fill="{a}"/><path d="M126 20V54H160" fill="none" stroke="{b}" stroke-width="6" stroke-linejoin="round"/><g fill="{b}"><rect x="66" y="118" width="16" height="40"/><rect x="92" y="96" width="16" height="62"/><rect x="118" y="130" width="16" height="28"/></g><g stroke="{b}" stroke-width="6" stroke-linecap="round"><path d="M66 74H122M66 92H100"/></g></svg>'''
def ic_brief(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M72 62V48C72 40 78 34 86 34H114C122 34 128 40 128 48V62" fill="none" stroke="{a}" stroke-width="10"/><rect x="22" y="62" width="156" height="104" rx="14" fill="{a}"/><path d="M22 108H178" stroke="{b}" stroke-width="6"/><rect x="88" y="98" width="24" height="22" rx="5" fill="{b}"/></svg>'''
def ic_stone(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><g fill="{a}"><rect x="20" y="30" width="76" height="44" rx="5"/><rect x="104" y="30" width="76" height="44" rx="5"/><rect x="62" y="82" width="76" height="44" rx="5"/><rect x="20" y="134" width="76" height="44" rx="5"/><rect x="104" y="134" width="76" height="44" rx="5"/><rect x="-10" y="82" width="64" height="44" rx="5"/><rect x="146" y="82" width="64" height="44" rx="5"/></g></svg>'''

# ================= IMIGRAÇÃO: Hoja 17 (retorno voluntário) =================
def maleta(x,y,s=1):
    return f'''<svg class=abs style="left:{x}px;top:{y}px" width="{int(560*s)}" height="{int(520*s)}" viewBox="0 0 560 520">
    <path d="M200 130V90C200 66 216 50 240 50H320C344 50 360 66 360 90V130" fill="none" stroke="{G}" stroke-width="22" stroke-linecap="round"/>
    <rect x="40" y="120" width="480" height="340" rx="40" fill="{TERRA}"/>
    <rect x="40" y="120" width="480" height="340" rx="40" fill="none" stroke="{G}" stroke-width="8"/>
    <rect x="130" y="120" width="40" height="340" fill="{GOLD}"/><rect x="390" y="120" width="40" height="340" fill="{GOLD}"/>
    <rect x="236" y="262" width="88" height="62" rx="12" fill="{G}"/><rect x="256" y="280" width="48" height="26" rx="6" fill="{GOLD}"/>
    <circle cx="96" cy="492" r="18" fill="{G}"/><circle cx="464" cy="492" r="18" fill="{G}"/>
    <g transform="rotate(-12 470 190)"><rect x="440" y="150" width="96" height="70" rx="10" fill="{IV}" stroke="{G}" stroke-width="5"/><circle cx="488" cy="185" r="18" fill="none" stroke="{TERRA}" stroke-width="5"/><path d="M478 186L486 194L500 176" fill="none" stroke="{TERRA}" stroke-width="5" stroke-linecap="round"/></g>
    </svg>'''
def img_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:{SAND}"></div>
    <div class=abs style="left:-160px;top:760px;width:700px;height:700px;border-radius:50%;background:{G};opacity:.95"></div>
    <div class=abs style="left:620px;top:690px;width:640px;height:640px;border-radius:50%;background:{GOLD};opacity:.35"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Retorno</span></div>
    <div class="abs serif" style="left:80px;top:165px;width:900px;font-size:92px;line-height:1.06;font-weight:700;color:{G}">Retornou <span style="color:{TERRA};font-style:italic">voluntariamente</span> ao seu país? Veja o que diz a ficha oficial</div>
    <svg class=abs style="left:60px;top:560px;overflow:visible" width="960" height="260" viewBox="0 0 960 260"><path d="M900 200Q480 -20 70 200" fill="none" stroke="{G}" stroke-width="6" stroke-dasharray="4 20" stroke-linecap="round"/><path d="M52 210L94 176L100 226Z" fill="{G}"/><circle cx="900" cy="200" r="16" fill="{TERRA}"/></svg>
    {maleta(260,740,0.95)}
    <div class=abs style="left:80px;top:1130px;font-size:30px;font-weight:600;letter-spacing:.14em;color:{IV}">DESLIZE  →</div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div></div>'''
    return page(1350,SAND,inner)
IMG=[img_cover()]; T=7
IMG.append(content(2,T,'Retorno · Para quem é','Para quem é','Quem foi titular de residência temporal, com ou sem trabalho, e voltou ao país de origem, com ou sem programa de retorno voluntário. Não vale para cidadãos da UE, do EEE ou da Suíça.',ic_return,'green'))
IMG.append(content(3,T,'Retorno · Tempo','Compromisso de não regresso','É preciso ter <b>terminado o prazo</b> do compromisso de não regresso à Espanha. Quem voltou sem programa deve esperar <b>três anos</b> desde o retorno.',ic_cal3,'ivory'))
IMG.append(content(4,T,'Retorno · Requisitos','Requisitos principais','Não estar em situação irregular na Espanha, <b>sem antecedentes criminais</b> na Espanha e nos países onde viveu nos últimos cinco anos, e cumprir os requisitos da autorização pedida.',ic_clip,'terra'))
IMG.append(content(5,T,'Retorno · Onde pedir','Onde e como pedir','<b>Pessoalmente</b>, no consulado espanhol do país de origem, com a TIE em vigor. Quem não aderiu a programa de retorno também renuncia, por escrito, à autorização anterior.',ic_embassy,'green'))
IMG.append(content(6,T,'Retorno · Prazo','Prazo e vantagens','Tramitação preferente. A ficha oficial prevê resolução em até <b>45 dias</b>. O tempo de residência anterior ao retorno conta para a residência de longa duração.',ic_clock,'ivory'))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 17 (atualizada em maio de 2025).<br>Consulta em 08/11/2026.'))

# ================= NOTÍCIA: Ceuta, emergência =================
def ondas(col,y0,n=6,op=.5):
    s=''
    for i in range(n):
        y=y0+i*46
        s+=f'<path d="M-20 {y}Q 80 {y-26} 180 {y}T 380 {y}T 580 {y}T 780 {y}T 980 {y}T 1180 {y}" fill="none" stroke="{col}" stroke-width="4" opacity="{op-i*0.06:.2f}"/>'
    return f'<svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">{s}</svg>'
def estreito():
    return f'''<svg class=abs style="left:70px;top:590px" width="940" height="560" viewBox="0 0 940 560">
    <path d="M0 0H940V100C860 130 770 90 690 140C610 190 530 160 450 206C380 246 300 240 200 278L0 300Z" fill="{G2}" stroke="{GOLD}" stroke-width="4"/>
    <text x="40" y="150" font-family="Lora" font-size="46" font-weight="700" fill="{IV}">Espanha</text>
    <path d="M940 560H260C290 500 430 480 500 440C560 405 640 410 700 372C770 330 870 345 940 316Z" fill="{TERRA}" stroke="{GOLD}" stroke-width="4"/>
    <path d="M500 440C550 416 600 398 650 392L668 414L606 446Z" fill="{GOLD}" opacity=".9"/>
    <circle cx="650" cy="392" r="30" fill="none" stroke="{IV}" stroke-width="5"/><circle cx="650" cy="392" r="12" fill="{IV}"/>
    <text x="700" y="474" font-family="Lora" font-size="46" font-weight="700" fill="{IV}">Ceuta</text>
    </svg>'''
def not_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{G} 0%,{G2} 100%)"></div>
    {ondas(GOLD,560,8,.5)}
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:165px;width:900px;font-size:96px;line-height:1.05;font-weight:700;color:{IV}">Governo amplia a <span style="color:{GOLD};font-style:italic">emergência</span> para atender migrantes em Ceuta</div>
    {estreito()}
    <div class=abs style="left:70px;top:1010px;width:auto;white-space:nowrap;transform:rotate(-3deg);background:{TERRA};color:{IV};padding:14px 26px;border-radius:14px;border:3px solid {GOLD}">
      <div style="font-size:20px;letter-spacing:.2em;font-weight:700;color:#F3D79A">CONSELHO DE MINISTROS</div>
      <div class=serif style="font-size:40px;font-weight:700;line-height:1.1;margin-top:4px">3 de novembro de 2026</div></div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,G,inner)
NOT=[not_cover()]; T=7
NOT.append(content(2,T,'Notícia · O que foi','O que o Governo aprovou','O Conselho de Ministros tomou razão da <b>ampliação da declaração de emergência</b> para serviços, obras e fornecimentos essenciais às necessidades básicas de migrantes chegados a Ceuta.',ic_lifebuoy,'ivory'))
NOT.append(content(3,T,'Notícia · Valor','Valor da ampliação','O valor informado na referência oficial é de <b>26.153.526,61 euros</b>. A área responsável é o Ministério de Inclusão, Seguridade Social e Migrações.',ic_bag,'terra'))
NOT.append(content(4,T,'Notícia · Informe','Informe sobre a situação','A mesma referência inclui um informe da Política Territorial e Memória Democrática, atualizado sobre a situação em Ceuta, <b>a 2 de novembro de 2026</b>.',ic_report,'ivory'))
NOT.append(content(5,T,'Notícia · Emprego','Plano de emprego','No mesmo Conselho, aprovou-se um suplemento de <b>25 milhões de euros</b> para planos de contratação de desempregados em Ceuta e Melilla, a cargo do SEPE.',ic_brief,'green'))
NOT.append(content(6,T,'Notícia · Em resumo','O que a referência não detalha','O documento oficial lido não informa o número de pessoas atendidas nem prazos. Os itens tratam de gestão e financiamento.',ic_doc,'terra'))
NOT.append(closing(1350,IV,G,TERRA,'Fonte: La Moncloa, Referencia do Conselho de Ministros de 03/11/2026.<br>Consulta em 08/11/2026.'))

# ================= CULTURA: Aqueduto de Segóvia (Reel 1080x1920) =================
def aqueduto(x,y,w,h,col,bg,tiers=2,lab=None):
    # duas arcadas sobrepostas; arcos inferiores maiores, superiores menores
    s=f'<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
    h2=h*0.42; h1=h-h2
    nb=6; pw=w/nb
    s+=f'<rect x="0" y="{h2}" width="{w}" height="{h1}" fill="{col}"/>'
    for i in range(nb):
        ax=i*pw+pw*.18; aw=pw*.64
        s+=f'<path d="M{ax:.1f} {h} V{h2+h1*.42:.1f} C{ax:.1f} {h2+h1*.02:.1f} {ax+aw:.1f} {h2+h1*.02:.1f} {ax+aw:.1f} {h2+h1*.42:.1f} V{h} Z" fill="{bg}"/>'
    nu=12; uw=w/nu
    s+=f'<rect x="0" y="0" width="{w}" height="{h2+4}" fill="{col}"/>'
    for i in range(nu):
        ax=i*uw+uw*.2; aw=uw*.6
        s+=f'<path d="M{ax:.1f} {h2} V{h2*.45:.1f} C{ax:.1f} {h2*.12:.1f} {ax+aw:.1f} {h2*.12:.1f} {ax+aw:.1f} {h2*.45:.1f} V{h2} Z" fill="{bg}"/>'
    s+=f'<rect x="-10" y="{h-14}" width="{w+20}" height="14" fill="{col}"/>'
    s+='</svg>'
    return s
def sol(x,y,r,col):
    return f'<svg class=abs style="left:{x-r}px;top:{y-r}px" width="{2*r}" height="{2*r}"><circle cx="{r}" cy="{r}" r="{r}" fill="{col}"/></svg>'
def card(x,y,w,h,bg=SAND,inner=''):
    return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:26px;background:{bg};overflow:hidden">{inner}</div>'
def rb(inner,n):
    return page(1920,IV,f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:linear-gradient(180deg,{IV} 0%,{SAND} 100%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{TERRA}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{G}">Espanha Sem Segredo</span></div><span class=c style="color:{G}">{n} / 5</span></div>''')
def T_(t,sz=92): return f'<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:{sz}px;line-height:1.06;font-weight:700;color:{G}">{t}</div>'
def P_(t,top=520): return f'<div class=abs style="left:80px;top:{top}px;width:920px;font-size:46px;line-height:1.4;color:{INK}">{t}</div>'
def reel():
    S=[]
    S.append(rb(f'''{T_('O aqueduto de <span style="color:%s;font-style:italic">Segóvia</span> faz parte de um Patrimônio Mundial da UNESCO'%TERRA,96)}
    {card(60,820,960,740,G,sol(780,230,110,GOLD)+aqueduto(40,300,880,400,IV,G)+'<div class=abs style="left:0;right:0;bottom:0;height:40px;background:%s"></div>'%TERRA)}
    {P_('Um monumento romano de pé.',1640)}''',1))
    S.append(rb(f'''{T_('Quão <span style="color:%s">alto</span> é?'%TERRA)}
    {P_('Segundo a UNESCO, chega a 28,5 metros acima do solo, no ponto mais baixo do vale.',470)}
    {card(60,830,960,780,TERRA,aqueduto(110,160,700,440,IV,TERRA)+'<svg class=abs style="left:800px;top:150px" width="120" height="460" viewBox="0 0 120 460"><path d="M60 14V446" stroke="%s" stroke-width="5"/><path d="M36 40L60 12L84 40M36 420L60 448L84 420" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round"/></svg>'%(GOLD,GOLD)+'<div class="abs serif" style="left:0;right:0;bottom:46px;text-align:center;font-size:84px;font-weight:700;color:%s">28,5 m</div>'%GOLD)}''',2))
    # 3 pilares: grade 16 x 8 = 128
    grid=''.join(f'<rect x="{i*52+22}" y="{j*62+22}" width="26" height="46" rx="4" fill="{IV}"/><path d="M{i*52+22} {j*62+24}A13 13 0 0 1 {i*52+48} {j*62+24}Z" fill="{IV}"/>' for i in range(16) for j in range(8))
    S.append(rb(f'''{T_('Duas arcadas, <span style="color:%s">128</span> pilares'%TERRA,88)}
    {P_('Duas arcadas sobrepostas sustentadas por 128 pilares, em um percurso de 813 metros, com quatro trechos retos.',560)}
    {card(60,980,960,620,G,'<svg class=abs style="left:44px;top:60px" width="880" height="520" viewBox="0 0 880 520">'+grid+'</svg>')}''',3))
    S.append(rb(f'''{T_('Uma obra de <span style="color:%s">alvenaria</span>'%TERRA)}
    {P_('A UNESCO descreve o aqueduto como uma enorme construção em alvenaria, parte da Cidade Velha de Segóvia e seu Aqueduto.',470)}
    {card(60,900,960,700,G,'<div class=abs style="left:130px;top:70px;width:700px;height:560px">'+badge(ic_stone(G,GOLD),GOLD,G,520)+'</div>')}''',4))
    S.append(closing(1920,G,IV,GOLD,'Fonte: UNESCO, Centro do Patrimônio Mundial (Old Town of Segovia and its Aqueduct).<br>Consulta em 08/11/2026.',logo=460,serif_sz=88,top=.2))
    return S

async def render(lst,prefix,h):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h})
        for i,htm in enumerate(lst):
            await pg.set_content(htm); await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT+f'{prefix}-{i+1}.png')
        await b.close()
import subprocess
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
