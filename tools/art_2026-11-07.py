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
def ic_check(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="30" width="120" height="150" rx="12" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="72" y="16" width="56" height="30" rx="10" fill="{a}"/><g stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M60 82L68 90L82 74M60 114L68 122L82 106M60 146L68 154L82 138"/><path d="M96 82H142M96 114H142M96 146H130"/></g></svg>'''

# ================= ÍCONES NOVOS (07/11) =================
def ic_micro(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="168" width="120" height="14" rx="5" fill="{a}"/><path d="M70 168C70 140 90 124 112 124" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round"/><g transform="rotate(-28 110 80)"><rect x="92" y="22" width="36" height="104" rx="8" fill="{a}"/><rect x="98" y="126" width="24" height="22" rx="4" fill="{b}" stroke="{a}" stroke-width="5"/><rect x="86" y="14" width="48" height="16" rx="6" fill="{a}"/></g><circle cx="150" cy="60" r="7" fill="{b}"/><circle cx="168" cy="92" r="5" fill="{b}"/></svg>'''
def ic_atom(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><g fill="none" stroke="{a}" stroke-width="7"><ellipse cx="100" cy="100" rx="78" ry="30"/><ellipse cx="100" cy="100" rx="78" ry="30" transform="rotate(60 100 100)"/><ellipse cx="100" cy="100" rx="78" ry="30" transform="rotate(-60 100 100)"/></g><circle cx="100" cy="100" r="16" fill="{a}"/><circle cx="100" cy="100" r="6" fill="{b}"/></svg>'''
def ic_contract(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="38" y="22" width="110" height="150" rx="10" fill="{b}" stroke="{a}" stroke-width="6"/><g stroke="{a}" stroke-width="6" stroke-linecap="round"><path d="M58 56H128M58 80H128M58 104H100"/></g><path d="M96 158L150 104L170 124L116 178L92 182Z" fill="{a}"/><path d="M146 108L166 128" stroke="{b}" stroke-width="5"/></svg>'''
def ic_laptop(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="40" width="120" height="86" rx="10" fill="{a}"/><rect x="50" y="50" width="100" height="66" rx="4" fill="{b}"/><path d="M20 140H180L168 160H32Z" fill="{a}"/><path d="M66 100L84 80L98 94L130 62" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><circle cx="130" cy="62" r="6" fill="{a}"/></svg>'''
def ic_family(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="64" cy="58" r="22" fill="{a}"/><circle cx="136" cy="58" r="22" fill="{a}"/><circle cx="100" cy="112" r="16" fill="{a}"/><path d="M22 168C22 126 40 96 64 96C88 96 106 126 106 168Z" fill="{a}"/><path d="M94 168C94 126 112 96 136 96C160 96 178 126 178 168Z" fill="{a}" opacity=".85"/><path d="M80 176C80 148 90 134 100 134C110 134 120 148 120 176Z" fill="{b}" stroke="{a}" stroke-width="5"/></svg>'''
def ic_seal(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 14L116 30L138 24L148 44L170 48L168 70L186 84L174 102L186 120L168 132L170 154L148 156L138 176L116 170L100 186L84 170L62 176L52 156L30 154L32 132L14 120L26 102L14 84L32 70L30 48L52 44L62 24L84 30Z" fill="{a}"/><circle cx="100" cy="100" r="46" fill="none" stroke="{b}" stroke-width="6"/><path d="M78 102L94 118L124 84" fill="none" stroke="{b}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_scale(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 24V170M60 176H140" stroke="{a}" stroke-width="10" stroke-linecap="round"/><path d="M34 62H166" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M34 62L12 118H56Z M166 62L144 118H188Z" fill="none" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M12 118C12 138 56 138 56 118Z M144 118C144 138 188 138 188 118Z" fill="{a}"/><circle cx="100" cy="34" r="12" fill="{a}"/><circle cx="100" cy="34" r="5" fill="{b}"/></svg>'''
def ic_calendar(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="28" y="40" width="144" height="132" rx="14" fill="{b}" stroke="{a}" stroke-width="7"/><path d="M28 80H172V54Q172 40 158 40H42Q28 40 28 54Z" fill="{a}"/><path d="M64 22V54M136 22V54" stroke="{a}" stroke-width="10" stroke-linecap="round"/><g fill="{a}"><circle cx="64" cy="106" r="8"/><circle cx="100" cy="106" r="8"/><circle cx="136" cy="106" r="8"/><circle cx="64" cy="140" r="8"/><circle cx="100" cy="140" r="8"/></g></svg>'''

# ================= NOTÍCIA: cartas de naturaleza =================
def decree(col,fill,acc,w=560,h=620):
    return f'''<svg width="{w}" height="{h}" viewBox="0 0 560 620"><rect x="70" y="20" width="420" height="520" rx="14" fill="{fill}" stroke="{col}" stroke-width="6"/>
    <rect x="96" y="46" width="368" height="468" rx="8" fill="none" stroke="{acc}" stroke-width="3" stroke-dasharray="3 10"/>
    <path d="M280 78L292 108L324 112L300 134L308 166L280 150L252 166L260 134L236 112L268 108Z" fill="{acc}"/>
    <g stroke="{col}" stroke-width="7" stroke-linecap="round"><path d="M130 220H430M130 256H430M130 292H430M130 328H360"/></g>
    <path d="M130 400C160 370 180 430 210 396S250 380 270 404" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round"/>
    <circle cx="400" cy="440" r="56" fill="{acc}"/><circle cx="400" cy="440" r="42" fill="none" stroke="{fill}" stroke-width="4"/><path d="M378 442L394 458L424 422" fill="none" stroke="{fill}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M370 492L360 556L400 536L440 556L430 492Z" fill="{acc}"/></svg>'''
def not_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(160deg,{TERRA} 0%,#9A4529 100%)"></div>
    <div class=abs style="left:-140px;top:640px;width:620px;height:620px;border-radius:50%;background:{GOLD};opacity:.22"></div>
    {bracket(IV)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:96px;line-height:1.05;font-weight:700;color:{IV}">BOE publica <span style="color:#F3D79A;font-style:italic">cartas de naturaleza</span> concedidas pelo Governo</div>
    <div class=abs style="left:250px;top:640px">{decree(G,IV,GOLD)}</div>
    <div class=abs style="left:60px;top:900px;width:360px;transform:rotate(-5deg);background:{G};color:{IV};padding:22px 28px;border-radius:14px;border:3px solid {GOLD}">
      <div style="font-size:20px;letter-spacing:.2em;font-weight:700;color:{GOLD}">BOE Nº 277 · 06/11/2026</div>
      <div class=serif style="font-size:40px;font-weight:700;line-height:1.1;margin-top:6px">Concessões individuais</div></div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,TERRA,inner)
T=6
NOT=[not_cover(),
 content(2,T,'Notícia · O que saiu','O que foi publicado','O BOE de <b>6 de novembro de 2026</b> publicou reais decretos que concedem a nacionalidade espanhola por carta de naturaleza, entre eles o Real Decreto 969/2026, de 4 de novembro.',ic_seal,'ivory'),
 content(3,T,'Notícia · Como é concedida','Concessão por decreto','A carta de naturaleza é concedida por real decreto. O texto publicado cita <b>"circunstâncias excepcionais"</b> e remete ao Código Civil quanto a requisitos, condições e prazos.',ic_scale,'green'),
 content(4,T,'Notícia · Não é a via comum','Não é a via comum','São concessões individuais, e não uma mudança de regra. A via geral segue sendo a <b>residência legal e contínua</b>: 10 anos como regra geral, com prazos menores em casos previstos.',ic_doc,'ivory'),
 content(5,T,'Notícia · O que fazer','Se você busca a nacionalidade','Confira a via que corresponde ao seu caso na fonte oficial: <b>Ministerio de Justicia</b> e administracion.gob.es. Cada caso depende de documentos e requisitos próprios.',ic_check,'terra'),
 closing(1350,G,IV,GOLD,'Fontes: BOE nº 277, de 06/11/2026 (RD 969/2026); EFE/Infobae (06/11/2026); administracion.gob.es.<br>Consulta em 07/11/2026.')]

# ================= IMIGRAÇÃO: Hoja 68 investigadores =================
def lab_cover():
    # frascos + átomo em fundo verde
    flask=lambda x,y,s,c: f'<g transform="translate({x} {y}) scale({s})"><path d="M-30 -120H30V-60L90 60C102 84 88 110 62 110H-62C-88 110 -102 84 -90 60L-30 -60Z" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linejoin="round"/><path d="M-72 40H72L90 66C100 88 88 106 62 106H-62C-88 106 -100 88 -90 66Z" fill="{c}"/><path d="M-40 -120H40" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/></g>'
    svg=f'<svg class=abs style="left:0;top:640px" width="1080" height="560" viewBox="0 0 1080 560"><g fill="none" stroke="{GOLD}" stroke-width="4" opacity=".55"><ellipse cx="800" cy="200" rx="190" ry="68"/><ellipse cx="800" cy="200" rx="190" ry="68" transform="rotate(60 800 200)"/><ellipse cx="800" cy="200" rx="190" ry="68" transform="rotate(-60 800 200)"/></g><circle cx="800" cy="200" r="26" fill="{GOLD}"/>{flask(220,300,1.35,TERRA)}{flask(520,360,1.0,GOLD)}<path d="M80 430H1000" stroke="{GOLD}" stroke-width="5"/></svg>'
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 85% 40%,{G2} 0,{G} 62%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Pesquisa</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:920px;font-size:100px;line-height:1.04;font-weight:700;color:{IV}">Pesquisador estrangeiro na Espanha: <span style="color:{GOLD};font-style:italic">residência e trabalho</span></div>
    {svg}
    <div class=abs style="left:80px;top:1130px;font-size:30px;font-weight:600;letter-spacing:.14em;color:{GOLD}">DESLIZE  →</div>
    {foot(GOLD)}'''
    return page(1350,G,inner)
T=7
IMG=[lab_cover(),
 content(2,T,'Imigração · Para quem é','Para quem é','Pessoal de pesquisa, técnicos de entidades de P&D&I, professores contratados por universidades e doutorandos matriculados. Há duas modalidades: <b>pesquisa UE</b> e <b>pesquisa nacional</b>.',ic_micro,'ivory'),
 content(3,T,'Imigração · Requisitos','Requisitos gerais','Maior de 18 anos, sem situação irregular na Espanha, <b>sem antecedentes penais</b>, com seguro de saúde, recursos econômicos suficientes e taxa paga.',ic_check,'terra'),
 content(4,T,'Imigração · Convênio ou contrato','Convênio de acolhimento','Deve indicar o <b>objeto da pesquisa</b>, o compromisso das duas partes e as datas de início e fim. A entidade precisa estar em dia com tributos e Seguridade Social.',ic_contract,'green'),
 content(5,T,'Imigração · Como pedir','Como pedir','Em geral, pela <b>entidade anfitriã</b>, por via eletrônica na UGE-CE, com o modelo MI-T. Doutorando sem contrato pode pedir pessoalmente. Documentos estrangeiros: tradução juramentada e apostila.',ic_laptop,'ivory'),
 content(6,T,'Imigração · Validade e família','Validade e família','A ficha oficial prevê <b>3 anos</b> de validade inicial e resolução em até 20 dias úteis. Cônjuge, filhos e ascendentes dependentes podem pedir autorização vinculada.',ic_family,'terra'),
 closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 68 (atualizada em agosto de 2026).<br>Consulta em 07/11/2026.')]

# ================= CULTURA: Patios de Córdoba (Reel 1080x1920) =================
POT='#B8573A'
def pot(x,y,s=1,flower=GOLD,leaf='#2E7D5B'):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-34 0H34L26 56H-26Z" fill="{POT}"/><rect x="-38" y="-8" width="76" height="14" rx="4" fill="#9A4529"/><path d="M0 -8C-30 -40 -50 -30 -56 -60M0 -8C30 -44 52 -34 58 -66M0 -8V-70" fill="none" stroke="{leaf}" stroke-width="6" stroke-linecap="round"/><g fill="{flower}"><circle cx="-56" cy="-66" r="13"/><circle cx="58" cy="-72" r="13"/><circle cx="0" cy="-78" r="15"/><circle cx="-26" cy="-46" r="10"/><circle cx="28" cy="-48" r="10"/></g><g fill="{G}"><circle cx="-56" cy="-66" r="4"/><circle cx="58" cy="-72" r="4"/><circle cx="0" cy="-78" r="5"/></g></g>'
def arc_door(x,y,w,h,col,fill=None):
    f=fill or 'none'
    return f'<path d="M{x} {y+h}V{y+w/2}C{x} {y-w*.2} {x+w} {y-w*.2} {x+w} {y+w/2}V{y+h}Z" fill="{f}" stroke="{col}" stroke-width="6"/>'
def well(x,y,s=1):
    return f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="110" ry="34" fill="{SAND}" stroke="{G}" stroke-width="5"/><path d="M-110 0V60C-110 92 110 92 110 60V0" fill="{IV}" stroke="{G}" stroke-width="5"/><ellipse cx="0" cy="0" rx="82" ry="22" fill="{G2}"/><path d="M-90 -2V-150M90 -2V-150M-100 -150H100" stroke="{G}" stroke-width="9" stroke-linecap="round"/><path d="M0 -150V-60" stroke="{G}" stroke-width="4"/><rect x="-14" y="-62" width="28" height="22" rx="5" fill="{TERRA}"/></g>'
def tile_band(y,col1,col2,h=70):
    s=''
    for i in range(0,1080,70):
        s+=f'<rect x="{i}" y="{y}" width="70" height="{h}" fill="{col1 if (i//70)%2==0 else col2}"/><path d="M{i+35} {y+10}L{i+60} {y+h/2}L{i+35} {y+h-10}L{i+10} {y+h/2}Z" fill="none" stroke="{GOLD}" stroke-width="3"/>'
    return f'<svg class=abs style="left:0;top:{y}px" width="1080" height="{h}" viewBox="0 {y} 1080 {h}">{s}</svg>'
def patio_scene(variant):
    # cena do pátio: fachada caiada, arcos, vasos em parede, poço
    if variant==1:
        wall=f'<rect x="0" y="820" width="1080" height="640" fill="{IV}"/>'
        arcs=''.join(arc_door(90+i*300,980,220,360,G,SAND) for i in range(3))
        pots=''.join(pot(200+i*300,860+ (i%2)*20,.9,GOLD if i%2==0 else TERRA) for i in range(3))
        return f'<svg class=abs style="left:0;top:130px" width="1080" height="1920" viewBox="0 0 1080 1920">{wall}<rect x="0" y="1340" width="1080" height="200" fill="{SAND}"/>{arcs}{pots}<path d="M0 1340H1080" stroke="{G}" stroke-width="6"/></svg>'
    if variant==2:
        # parede com vasos azuis/ terracota em fileira (vista frontal de parede de pátio)
        wall=f'<rect x="60" y="760" width="960" height="720" rx="16" fill="{IV}"/>'
        rows=''
        for r in range(3):
            for c in range(4):
                rows+=pot(180+c*240,900+r*190,.62,GOLD if (r+c)%2==0 else IV,'#2E7D5B' if (r+c)%3 else '#1E5550')
            rows+=f'<path d="M100 {960+r*190}H980" stroke="{G}" stroke-width="7" opacity=".5"/>'
        return f'<svg class=abs style="left:0;top:130px" width="1080" height="1920" viewBox="0 0 1080 1920">{wall}{rows}</svg>'
    if variant==3:
        return f'<svg class=abs style="left:0;top:130px" width="1080" height="1920" viewBox="0 0 1080 1920"><rect x="0" y="860" width="1080" height="720" fill="{IV}"/><rect x="0" y="1500" width="1080" height="80" fill="{SAND}"/>{arc_door(380,900,320,520,G,G2)}{well(180,1420,.9)}{pot(870,1450,1.0,GOLD)}{pot(560,1480,.8,TERRA)}<path d="M0 1500H1080" stroke="{G}" stroke-width="6"/></svg>'
def reel_base(inner,n,bg=None):
    return page(1920,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:radial-gradient(circle at 20% 10%,{G2} 0,{G} 62%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{GOLD}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">{n} / 5</span></div>''')
def reel():
    S=[]
    # 1 capa: pátio com arcos e vasos
    S.append(reel_base(f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:100px;line-height:1.05;font-weight:700;color:{IV}">Em Córdoba, a festa dos <span style="color:{GOLD};font-style:italic">pátios</span> é Patrimônio da UNESCO</div>
    {patio_scene(1)}
    <div class="abs" style="left:80px;top:720px;width:920px;font-size:46px;line-height:1.4;color:{IV}">Uma tradição de casas de pátio do casco antigo.</div>''',1))
    # 2 o que é (parede de vasos)
    S.append(reel_base(f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:88px;line-height:1.06;font-weight:700;color:{IV}">O que <span style="color:{GOLD}">é</span> a festa</div>
    <div class=abs style="left:80px;top:430px;width:920px;font-size:46px;line-height:1.4;color:{IV}">Uma festa centrada nas casas de patio do bairro antigo. Os vizinhos enfeitam os pátios com plantas.</div>
    {patio_scene(2)}''',2))
    # 3 quando e como é (poço, concurso)
    S.append(reel_base(f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:88px;line-height:1.06;font-weight:700;color:{IV}">Quando e <span style="color:{GOLD}">como</span></div>
    <div class=abs style="left:80px;top:430px;width:920px;font-size:46px;line-height:1.4;color:{IV}">No início de maio, durante doze dias. Há concurso com prêmios e música popular, como o flamenco, nos pátios maiores.</div>
    {patio_scene(3)}''',3))
    # 4 UNESCO 2012
    S.append(reel_base(f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:88px;line-height:1.06;font-weight:700;color:{IV}">Reconhecida em <span style="color:{GOLD}">2012</span></div>
    <div class=abs style="left:80px;top:430px;width:920px;font-size:46px;line-height:1.4;color:{IV}">Inscrita na Lista Representativa do Patrimônio Cultural Imaterial da Humanidade da UNESCO. Valoriza o pátio como espaço de convivência.</div>
    <div class=abs style="left:290px;top:1000px">{badge(ic_seal(G,GOLD),GOLD,G,500)}</div>
    {tile_band(1620,G2,TERRA,80)}''',4))
    S.append(closing(1920,TERRA,IV,'#F3D79A','Fonte: UNESCO, Patrimônio Cultural Imaterial (La fiesta de los patios de Córdoba).<br>Consulta em 07/11/2026.',logo=460,serif_sz=88,top=.2))
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
