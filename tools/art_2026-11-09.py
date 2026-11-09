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
# ================= ÍCONES NOVOS (2026-11-09) =================
def ic_cap(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 40L184 84L100 128L16 84Z" fill="{a}"/><path d="M52 108V146C52 160 76 172 100 172C124 172 148 160 148 146V108L100 134Z" fill="{a}"/><path d="M172 92V142" stroke="{b}" stroke-width="7" stroke-linecap="round"/><circle cx="172" cy="148" r="9" fill="{b}"/></svg>'''
def ic_hourglass(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="46" y="20" width="108" height="14" rx="6" fill="{a}"/><rect x="46" y="166" width="108" height="14" rx="6" fill="{a}"/><path d="M58 34H142C142 76 114 90 114 100C114 110 142 124 142 166H58C58 124 86 110 86 100C86 90 58 76 58 34Z" fill="none" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><path d="M72 46H128C124 70 108 82 100 90C92 82 76 70 72 46Z" fill="{b}"/><path d="M78 160C82 140 94 128 100 120C106 128 118 140 122 160Z" fill="{b}"/></svg>'''
def ic_coins(a,b):
    s=''
    for i,y in enumerate((142,114,86)):
        s+=f'<ellipse cx="100" cy="{y+14}" rx="64" ry="22" fill="{a}"/><rect x="36" y="{y-6}" width="128" height="20" fill="{a}"/><ellipse cx="100" cy="{y-6}" rx="64" ry="22" fill="{a}" stroke="{b}" stroke-width="5"/>'
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200">{s}<text x="100" y="80" text-anchor="middle" font-family="Lora" font-weight="700" font-size="30" fill="{b}">€</text></svg>'''
def ic_screen(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="20" y="36" width="160" height="108" rx="12" fill="{a}"/><rect x="32" y="48" width="136" height="84" rx="5" fill="{b}"/><rect x="82" y="144" width="36" height="16" fill="{a}"/><rect x="60" y="160" width="80" height="10" rx="5" fill="{a}"/><g stroke="{a}" stroke-width="7" stroke-linecap="round"><path d="M50 70H116M50 88H150M50 106H96"/></g><circle cx="146" cy="108" r="12" fill="{a}"/><path d="M140 108L145 113L153 102" fill="none" stroke="{b}" stroke-width="4" stroke-linecap="round"/></svg>'''
def ic_signpost(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="92" y="20" width="16" height="164" rx="4" fill="{a}"/><path d="M100 36H152L172 56L152 76H100Z" fill="{a}"/><path d="M100 94H48L28 114L48 134H100Z" fill="{a}"/><g stroke="{b}" stroke-width="6" stroke-linecap="round"><path d="M112 56H146M86 114H52"/></g></svg>'''
def ic_boat(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M20 110H180C170 144 150 160 126 160H74C50 160 30 144 20 110Z" fill="{a}"/><path d="M56 110V84H144V110" fill="{a}"/><rect x="82" y="58" width="36" height="26" rx="4" fill="{a}"/><g fill="{b}"><circle cx="64" cy="132" r="8"/><circle cx="100" cy="132" r="8"/><circle cx="136" cy="132" r="8"/></g><path d="M10 172Q35 158 60 172T110 172T160 172T200 168" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round"/></svg>'''
def ic_cross(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="26" y="52" width="148" height="116" rx="12" fill="{a}"/><path d="M100 14L176 52H24Z" fill="{a}"/><rect x="84" y="76" width="32" height="76" rx="4" fill="{b}"/><rect x="62" y="98" width="76" height="32" rx="4" fill="{b}"/></svg>'''
def ic_ferry(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M14 112H186L166 156H34Z" fill="{a}"/><rect x="40" y="76" width="120" height="36" rx="6" fill="{a}"/><rect x="74" y="50" width="52" height="26" rx="5" fill="{a}"/><g fill="{b}"><rect x="52" y="88" width="18" height="14" rx="3"/><rect x="82" y="88" width="18" height="14" rx="3"/><rect x="112" y="88" width="18" height="14" rx="3"/><rect x="86" y="58" width="28" height="12" rx="3"/></g><path d="M8 172Q36 158 64 172T120 172T176 172" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round"/></svg>'''
def ic_info(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="76" fill="{a}"/><circle cx="100" cy="64" r="10" fill="{b}"/><rect x="90" y="86" width="20" height="62" rx="8" fill="{b}"/></svg>'''
def ic_pin(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 18C66 18 42 44 42 76C42 118 100 182 100 182C100 182 158 118 158 76C158 44 134 18 100 18Z" fill="{a}"/><circle cx="100" cy="76" r="24" fill="{b}"/></svg>'''

# ================= IMIGRAÇÃO: Hoja 20 =================
def birete(x,y,s=1):
    return f'''<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{int(620*s)}" height="{int(520*s)}" viewBox="0 0 620 520">
    <path d="M310 40L590 170L310 300L30 170Z" fill="{G}"/>
    <path d="M150 238V340C150 392 226 430 310 430C394 430 470 392 470 340V238L310 316Z" fill="{G2}"/>
    <path d="M30 170L310 300L590 170" fill="none" stroke="{GOLD}" stroke-width="6" stroke-linejoin="round"/>
    <path d="M540 196V350" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/>
    <path d="M540 350L516 420M540 350L540 424M540 350L564 420" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/>
    <circle cx="540" cy="350" r="16" fill="{GOLD}"/>
    </svg>'''
def estrada(col,acc):
    return f'''<svg class=abs style="left:0;top:700px" width="1080" height="560" viewBox="0 0 1080 560">
    <path d="M-20 520C200 520 260 330 470 330C690 330 700 150 1100 140" fill="none" stroke="{col}" stroke-width="86" stroke-linecap="round" opacity=".9"/>
    <path d="M-20 520C200 520 260 330 470 330C690 330 700 150 1100 140" fill="none" stroke="{acc}" stroke-width="5" stroke-dasharray="26 26"/>
    </svg>'''
def img_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:{TERRA}"></div>
    <div class=abs style="left:560px;top:580px;width:700px;height:700px;border-radius:50%;background:{GOLD};opacity:.45"></div>
    {estrada(G,IV)}
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Imigração · Pós-estudos</span></div>
    <div class="abs serif" style="left:80px;top:165px;width:900px;font-size:86px;line-height:1.07;font-weight:700;color:{IV}">Terminou os estudos na Espanha? Veja a autorização para <span style="color:{GOLD};font-style:italic">buscar emprego</span> ou iniciar um negócio</div>
    {birete(40,640,.78)}
    <div class=abs style="right:80px;top:1190px;font-size:30px;font-weight:600;letter-spacing:.14em;color:{IV}">DESLIZE  →</div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div></div>'''
    return page(1350,TERRA,inner)
IMG=[img_cover()]; T=7
IMG.append(content(2,T,'Hoja 20 · Para quem é','Para quem é','Quem tinha estância de longa duração por estudos e concluiu curso em instituição de ensino superior autorizada, com nível mínimo equivalente a grau universitário. Não vale para cidadãos da UE.',ic_cap,'green'))
IMG.append(content(3,T,'Hoja 20 · Validade','24 meses, sem trabalhar','A autorização vale <b>24 meses</b>, sem prorrogação, para buscar emprego ligado aos estudos ou iniciar um projeto empresarial. Neste período, o titular <b>não está autorizado a trabalhar</b>.',ic_hourglass,'ivory'))
IMG.append(content(4,T,'Hoja 20 · Requisitos','Requisitos principais','Seguro de saúde, meios econômicos de <b>100% do IPREM mensal</b> (50% se o alojamento estiver pago antecipadamente), sem antecedentes criminais e taxa paga.',ic_coins,'terra'))
IMG.append(content(5,T,'Hoja 20 · Como pedir','Quando e como pedir','Pedido <b>eletrônico</b>, dirigido à Delegação ou Subdelegação do Governo da província. Apresentar até 60 dias antes de a autorização de estudos vencer; fora do prazo, até 90 dias depois, sem prejuízo de sanções.',ic_screen,'green'))
IMG.append(content(6,T,'Hoja 20 · Depois','Depois do pedido','A ficha oficial prevê resolução em até <b>20 dias</b>. Quem encontrar trabalho relacionado aos estudos, ou abrir um negócio, deve pedir a autorização correspondente.',ic_signpost,'ivory'))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 20 (atualizada em setembro de 2025).<br>Consulta em 09/11/2026.'))

# ================= NOTÍCIA: Canárias =================
def ilhas(col,acc):
    return f'''<svg class=abs style="left:0;top:760px" width="1080" height="420" viewBox="0 0 1080 420">
    <path d="M60 300C90 240 130 232 170 250C200 262 230 258 250 290C220 320 150 330 60 300Z" fill="{col}"/>
    <path d="M420 270C450 200 520 190 570 214C610 232 640 250 650 290C590 330 480 330 420 270Z" fill="{col}"/>
    <path d="M820 290C840 244 890 236 930 250C970 264 990 280 1000 300C940 330 860 330 820 290Z" fill="{col}"/>
    <path d="M520 214L548 168L574 218Z" fill="{acc}"/>
    </svg>'''
def cayuco(x,y,s=1):
    return f'''<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{int(520*s)}" height="{int(240*s)}" viewBox="0 0 520 240">
    <path d="M10 120C120 150 400 150 510 100L470 180C400 214 120 214 50 180Z" fill="{TERRA}" stroke="{IV}" stroke-width="5"/>
    <path d="M10 120L510 100" stroke="{GOLD}" stroke-width="8"/>
    <g fill="{IV}"><circle cx="120" cy="92" r="16"/><circle cx="180" cy="86" r="16"/><circle cx="240" cy="82" r="16"/><circle cx="300" cy="80" r="16"/><circle cx="360" cy="76" r="16"/><circle cx="420" cy="74" r="16"/>
    <path d="M100 128C100 106 140 106 140 128Z"/><path d="M160 126C160 102 200 102 200 126Z"/><path d="M220 124C220 100 260 100 260 124Z"/><path d="M280 122C280 98 320 98 320 122Z"/><path d="M340 120C340 96 380 96 380 120Z"/><path d="M400 118C400 94 440 94 440 118Z"/></g>
    </svg>'''
def not_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{G2} 0%,{G} 100%)"></div>
    <div class=abs style="left:700px;top:560px;width:280px;height:280px;border-radius:50%;background:{GOLD};opacity:.85"></div>
    {ilhas(G2,GOLD)}
    <div class=abs style="left:0;right:0;top:960px;height:390px;background:{G}"></div>
    {ondas(GOLD,960,6,.55)}
    {cayuco(250,860,1.1)}
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Canárias</span></div>
    <div class="abs serif" style="left:80px;top:165px;width:900px;font-size:90px;line-height:1.05;font-weight:700;color:{IV}">Chegadas de <span style="color:{GOLD};font-style:italic">cayucos</span> às Canárias aumentam no início de novembro</div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,G,inner)
def ondas(col,y0,n=6,op=.5):
    s=''
    for i in range(n):
        y=y0+i*46
        s+=f'<path d="M-20 {y}Q 80 {y-26} 180 {y}T 380 {y}T 580 {y}T 780 {y}T 980 {y}T 1180 {y}" fill="none" stroke="{col}" stroke-width="4" opacity="{max(op-i*0.06,.1):.2f}"/>'
    return f'<svg class=abs style="left:0;top:0" width="1080" height="1350" viewBox="0 0 1080 1350">{s}</svg>'
NOT=[not_cover()]; T=7
NOT.append(content(2,T,'Notícia · 4 de novembro','557 pessoas em seis cayucos','Segundo o Euronews, em 4 de novembro chegaram a <b>El Hierro 557 pessoas</b> em seis cayucos, saídos do Senegal. O resgate é atribuído ao Salvamento Marítimo.',ic_boat,'ivory'))
NOT.append(content(3,T,'Notícia · 6 de novembro','Mais de 1.021 em uma noite','A RTVC informa que, desde as 21h de 5 de novembro, o Salvamento Marítimo desembarcou <b>mais de 1.021 pessoas</b> em El Hierro, Gran Canaria e Lanzarote.',ic_pin,'green'))
NOT.append(content(4,T,'Notícia · Números','Balanços ainda variam','A RTVC fala em cerca de <b>3.200 pessoas</b> nos cinco primeiros dias de novembro. A EFE cita cerca de <b>6.000</b> na primeira semana. Os períodos contados são diferentes.',ic_info,'terra'))
NOT.append(content(5,T,'Notícia · Atendimento','Pressão sobre o atendimento','A RTVC relata o gerente do hospital de El Hierro descrevendo as urgências como saturadas. Em 4 de novembro, a Delegação do Governo transferiu 500 pessoas de ferry para Tenerife.',ic_cross,'ivory'))
NOT.append(content(6,T,'Notícia · Em resumo','O que ainda falta','Os números vêm da imprensa e podem mudar. Não consultamos um balanço oficial consolidado do Ministério do Interior sobre o período.',ic_ferry,'green'))
NOT.append(closing(1350,IV,G,TERRA,'Fontes: RTVC (06/11/2026), Euronews (04/11/2026) e EFE via Infobae (09/11/2026).<br>Consulta em 09/11/2026.'))

# ================= CULTURA: Almudena (Reel 1080x1920) =================
def sol(x,y,r,col):
    return f'<svg class=abs style="left:{x-r}px;top:{y-r}px" width="{2*r}" height="{2*r}"><circle cx="{r}" cy="{r}" r="{r}" fill="{col}"/></svg>'
def card(x,y,w,h,bg=SAND,inner=''):
    return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:26px;background:{bg};overflow:hidden">{inner}</div>'
def catedral(x,y,w,col,win):
    # fachada neoclássica com cúpula central e duas torres sinos
    return f'''<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{w}" height="{int(w*.8)}" viewBox="0 0 800 640">
    <rect x="80" y="330" width="640" height="300" fill="{col}"/>
    <rect x="40" y="610" width="720" height="30" fill="{col}"/>
    <path d="M120 330V210H220V330Z" fill="{col}"/><path d="M110 210L170 150L230 210Z" fill="{col}"/>
    <path d="M580 330V210H680V330Z" fill="{col}"/><path d="M570 210L630 150L690 210Z" fill="{col}"/>
    <rect x="300" y="270" width="200" height="70" fill="{col}"/>
    <path d="M310 270C310 140 490 140 490 270Z" fill="{col}"/>
    <path d="M388 160V120M400 100V120" stroke="{col}" stroke-width="10"/><rect x="390" y="70" width="20" height="60" fill="{col}"/><rect x="372" y="88" width="56" height="16" fill="{col}"/>
    <g fill="{win}"><path d="M150 400V470C150 490 190 490 190 470V400C190 380 150 380 150 400Z"/><path d="M270 400V470C270 490 310 490 310 470V400C310 380 270 380 270 400Z"/><path d="M490 400V470C490 490 530 490 530 470V400C530 380 490 380 490 400Z"/><path d="M610 400V470C610 490 650 490 650 470V400C650 380 610 380 610 400Z"/>
    <path d="M360 640V500C360 440 440 440 440 500V640Z"/><path d="M150 250V290C150 304 190 304 190 290V250C190 236 150 236 150 250Z"/><path d="M610 250V290C610 304 650 304 650 290V250C650 236 610 236 610 250Z"/></g>
    </svg>'''
def muralha(x,y,w,h,col,line,niche):
    s=f'<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{col}"/>'
    rh=70
    for r in range(int(h/rh)+1):
        off=0 if r%2==0 else 90
        s+=f'<path d="M0 {r*rh}H{w}" stroke="{line}" stroke-width="5"/>'
        for c in range(-1,int(w/180)+2):
            s+=f'<path d="M{c*180+off} {r*rh}V{(r+1)*rh}" stroke="{line}" stroke-width="5"/>'
    # ameias
    for c in range(0,int(w/140)+1):
        s+=f'<rect x="{c*140+10}" y="-60" width="90" height="62" fill="{col}"/>'
    cx=w/2
    s+=f'<path d="M{cx-120} {h} V{h*.45} C{cx-120} {h*.12} {cx+120} {h*.12} {cx+120} {h*.45} V{h} Z" fill="{niche}"/>'
    s+=f'<circle cx="{cx}" cy="{h*.52}" r="64" fill="{GOLD}"/><path d="M{cx-26} {h*.52+60} V{h*.52-10} Q{cx} {h*.52-60} {cx+26} {h*.52-10} V{h*.52+60}Z" fill="{niche}"/>'
    s+='</svg>'
    return s
def corona(x,y,r,col1,col2,sug):
    amd=''
    import math
    for i in range(14):
        a=i*2*math.pi/14
        cx=r+(r*.74)*math.cos(a); cy=r+(r*.74)*math.sin(a)
        amd+=f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="26" ry="14" transform="rotate({a*180/math.pi+90:.1f} {cx:.1f} {cy:.1f})" fill="{col2}" stroke="{sug}" stroke-width="3"/>'
    for i in range(14):
        a=(i+.5)*2*math.pi/14
        cx=r+(r*.74)*math.cos(a); cy=r+(r*.74)*math.sin(a)
        amd+=f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="12" fill="{GOLD}"/>'
    return f'''<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{2*r}" height="{2*r}" viewBox="0 0 {2*r} {2*r}"><circle cx="{r}" cy="{r}" r="{r}" fill="{col1}"/><circle cx="{r}" cy="{r}" r="{r*.42}" fill="{SAND}"/><circle cx="{r}" cy="{r}" r="{r*.42}" fill="none" stroke="{sug}" stroke-width="6"/>{amd}</svg>'''
def selo(x,y,r):
    return f'''<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{2*r}" height="{2*r}" viewBox="0 0 200 200"><circle cx="100" cy="100" r="96" fill="{TERRA}" stroke="{GOLD}" stroke-width="6"/><circle cx="100" cy="100" r="78" fill="none" stroke="{IV}" stroke-width="3" stroke-dasharray="3 7"/><path d="M60 126L66 90L84 108L100 78L116 108L134 90L140 126Z" fill="{GOLD}"/><rect x="60" y="130" width="80" height="10" rx="4" fill="{GOLD}"/><text x="100" y="172" text-anchor="middle" font-family="Lora" font-weight="700" font-size="28" fill="{IV}">1908</text></svg>'''
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
    S.append(rb(f'''{T_('Hoje é dia da Virgem da <span style="color:%s;font-style:italic">Almudena</span>, padroeira de Madri'%TERRA,92)}
    {card(60,820,960,760,TERRA,sol(780,190,100,GOLD)+catedral(80,150,800,IV,TERRA)+'<div class=abs style="left:0;right:0;bottom:0;height:46px;background:%s"></div>'%G)}''',1))
    S.append(rb(f'''{T_('Uma <span style="color:%s">lenda</span> de 1085'%TERRA)}
    {P_('Segundo a lenda, a imagem foi encontrada por Afonso VI, em 1085, num recanto da muralha árabe, depois de séculos oculta.',460)}
    {card(60,940,960,660,G,muralha(0,120,960,540,G2,G,G))}''',2))
    S.append(rb(f'''{T_('Padroeira <span style="color:%s">oficial</span> desde 1908'%TERRA)}
    {P_('Em 1908, o papa Pio X concedeu à Virgem da Almudena o título de padroeira oficial de Madri.',460)}
    {card(60,860,960,740,G,selo(260,110,260))}''',3))
    S.append(rb(f'''{T_('A <span style="color:%s">corona</span> da Almudena'%TERRA)}
    {P_('Doce criado em 1978 como homenagem à padroeira. No dia 9, às 12h30, é repartida na Plaza Mayor: cerca de 1.000 porções gratuitas, até acabar.',460)}
    {card(60,980,960,620,G,corona(230,70,240,TERRA,IV,GOLD))}''',4))
    S.append(closing(1920,G,IV,GOLD,'Fonte: Ayuntamiento de Madrid (diario.madrid.es), Fiesta de la Almudena 2026.<br>Consulta em 09/11/2026.',logo=460,serif_sz=88,top=.2))
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
