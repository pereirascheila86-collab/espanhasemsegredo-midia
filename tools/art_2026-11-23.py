import base64, asyncio, os, html, sys, subprocess
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
import math
def T(x,y,t,sz=40,col=IV,w=700,fam='Inter',anchor='middle',ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{sz}" letter-spacing="{ls}" fill="{col}">{t}</text>'
def SV(inner): return f'<svg width="100%" height="100%" viewBox="0 0 200 200">{inner}</svg>'
def figura(cx,top,s,col):
    return f'<circle cx="{cx}" cy="{top+14*s}" r="{14*s}" fill="{col}"/><path d="M{cx-18*s} {top+78*s}V{top+46*s}C{cx-18*s} {top+34*s} {cx+18*s} {top+34*s} {cx+18*s} {top+46*s}V{top+78*s}Z" fill="{col}"/>'
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


# ================= 2026-11-23 =================
which=sys.argv[1:] or ['noticia','imigracao','cultura']

# ---------- NOTICIA: eleições gerais 29/11 (voto por correio / CERA) ----------
def ic_urna(a,b):
    return SV(f'<rect x="30" y="88" width="140" height="86" rx="10" fill="{a}"/><rect x="62" y="80" width="76" height="12" rx="4" fill="{b}"/><path d="M78 24H122V70H78Z" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M88 44H112M88 56H106" stroke="{a}" stroke-width="5" stroke-linecap="round"/><rect x="62" y="116" width="76" height="30" rx="6" fill="{b}"/>')
def ic_sobre(a,b):
    return SV(f'<rect x="22" y="48" width="156" height="112" rx="12" fill="{a}"/><path d="M22 58L100 118L178 58" fill="none" stroke="{b}" stroke-width="9" stroke-linejoin="round"/>{T(100,150,"25/11",34,b,800,"Inter")}')
def ic_consulado(a,b):
    return SV(f'<path d="M20 170H180M30 170V92H170V170" fill="{a}" stroke="{a}" stroke-width="5"/><path d="M20 92L100 40L180 92Z" fill="{a}"/>'+''.join(f'<rect x="{x}" y="108" width="20" height="62" fill="{b}"/>' for x in (50,90,130))+f'<path d="M100 40V14" stroke="{a}" stroke-width="6"/><path d="M100 14H136V30H100Z" fill="{b}"/>')
def ic_lupa_data(a,b):
    return SV(f'<rect x="24" y="36" width="116" height="124" rx="12" fill="{a}"/><rect x="24" y="36" width="116" height="32" rx="12" fill="{b}"/><path d="M60 24V48M104 24V48" stroke="{a}" stroke-width="9" stroke-linecap="round"/>{T(82,134,"29",56,b,800,"Lora")}<circle cx="144" cy="132" r="26" fill="none" stroke="{b}" stroke-width="9"/><path d="M162 152L186 178" stroke="{b}" stroke-width="12" stroke-linecap="round"/>')
def cover_29n():
    urna=(f'<rect x="300" y="760" width="480" height="300" rx="34" fill="{G}"/><rect x="360" y="730" width="360" height="44" rx="14" fill="{IV}"/>'
          f'<rect x="460" y="740" width="160" height="14" rx="7" fill="{G}"/>'
          f'<g transform="rotate(-8 540 600)"><rect x="440" y="540" width="200" height="250" rx="12" fill="{IV}"/><path d="M475 600H605M475 640H605M475 680H560" stroke="{TERRA}" stroke-width="12" stroke-linecap="round"/></g>'
          f'<rect x="372" y="860" width="336" height="130" rx="14" fill="none" stroke="{GOLD}" stroke-width="8"/>'
          f'{T(540,955,"29 · 11",84,GOLD,800,"Lora")}')
    sobres=''.join(f'<g transform="translate({x} {y}) rotate({r})"><rect width="150" height="104" rx="10" fill="{IV}" opacity=".92"/><path d="M0 8L75 58L150 8" fill="none" stroke="{TERRA}" stroke-width="8"/></g>' for x,y,r in ((90,610,-14),(860,560,12),(820,880,-8)))
    return page(1350,TERRA,f'''{bracket('#F3D79A')}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Notícia · Eleições</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:68px;line-height:1.06;font-weight:700;color:{IV}">Eleições gerais na Espanha: o que vale até <span style="color:#F3D79A;font-style:italic">domingo, 29/11</span></div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350"><circle cx="540" cy="860" r="330" fill="#A24B30"/>{sobres}{urna}<path d="M0 1110H1080V1350H0Z" fill="{G}"/></svg>
    {foot(IV)}''')
NOT=[cover_29n()]
NOT.append(content2('Notícia · A votação','Domingo, 29 de novembro','As eleições gerais para as <b>Cortes Generales</b> estão marcadas para o <b>domingo, 29 de novembro de 2026</b>, segundo o Ministerio de Asuntos Exteriores.',ic_lupa_data,'ivory',44))
NOT.append(content2('Notícia · Voto por correio','Depósito nos Correos','Quem pediu o voto por correio deve depositá-lo nos <b>Correos até 25 de novembro</b>, segundo a nota dos Correos.',ic_sobre,'green',46))
NOT.append(content2('Notícia · Para quem vota no exterior','Consulado (CERA)','Para quem vota do exterior, Exteriores informa o depósito no consulado de <b>21 a 26 de novembro</b>. Votos enviados por correio devem chegar até 24/11.',ic_consulado,'terra',44))
NOT.append(content2('Notícia · Confira antes de agir','Datas oficiais','Prazos e regras podem ser atualizados. Confirme sempre em <b>exteriores.gob.es</b> e nos canais oficiais antes de votar.',ic_urna,'ivory',46))
NOT.append(closing(1350,G,IV,GOLD,'Fontes: Ministerio de Asuntos Exteriores (Elecciones a Cortes Generales 2026); Correos.<br>Consulta em 19/11/2026; a reconferir em 23/11/2026.'))

# ---------- IMIGRACAO: Hoja 67, renovação de profissional altamente qualificado ----------
def ic_diploma(a,b):
    return SV(f'<rect x="26" y="48" width="148" height="104" rx="10" fill="{a}"/><path d="M48 80H152M48 100H152M48 120H110" stroke="{b}" stroke-width="8" stroke-linecap="round"/><circle cx="146" cy="138" r="24" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M138 158L134 184L146 174L158 184L154 158" fill="{b}" stroke="{a}" stroke-width="4" stroke-linejoin="round"/>')
def ic_60_90(a,b):
    return SV(f'<rect x="22" y="36" width="156" height="132" rx="14" fill="{a}"/><rect x="22" y="36" width="156" height="36" rx="14" fill="{b}"/><path d="M62 22V50M138 22V50" stroke="{a}" stroke-width="10" stroke-linecap="round"/>{T(100,128,"60 | 90",46,b,800,"Lora")}{T(100,158,"dias",28,b,700)}')
def ic_telemat(a,b):
    return SV(f'<rect x="20" y="34" width="160" height="104" rx="12" fill="{a}"/><rect x="32" y="46" width="136" height="80" rx="4" fill="{b}"/><path d="M70 160H130M100 138V160" stroke="{a}" stroke-width="10" stroke-linecap="round"/><path d="M60 94L88 110L140 66" fill="none" stroke="{a}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_20dias(a,b):
    return SV(f'<circle cx="84" cy="100" r="62" fill="{a}"/><circle cx="84" cy="100" r="50" fill="{b}"/><path d="M84 66V102L110 118" fill="none" stroke="{a}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><rect x="118" y="118" width="64" height="44" rx="8" fill="{b}" stroke="{a}" stroke-width="6"/><circle cx="138" cy="136" r="7" fill="{a}"/><path d="M130 152H170" stroke="{a}" stroke-width="5" stroke-linecap="round"/>')
def ic_atencao(a,b):
    return SV(f'<path d="M100 26L176 160H24Z" fill="{a}" stroke="{a}" stroke-width="10" stroke-linejoin="round"/><path d="M100 70V114" stroke="{b}" stroke-width="13" stroke-linecap="round"/><circle cx="100" cy="138" r="8" fill="{b}"/>')
def cover_hoja67():
    estrelas=''.join(f'<path d="M{540+300*math.cos(math.radians(a)):.1f} {800+300*math.sin(math.radians(a)):.1f}l9 20 22 3-16 15 4 22-19-11-19 11 4-22-16-15 22-3z" transform="translate(-14 -22)" fill="{GOLD}"/>' for a in range(-90,270,30))
    cartao=(f'<rect x="200" y="620" width="680" height="400" rx="34" fill="{IV}"/><rect x="200" y="620" width="680" height="84" rx="34" fill="{GOLD}"/><rect x="200" y="660" width="680" height="44" fill="{GOLD}"/>'
            f'<rect x="250" y="750" width="190" height="220" rx="16" fill="{G2}"/>{figura(345,785,2.7,IV)}'
            f'<path d="M490 770H830M490 830H830M490 890H760M490 950H700" stroke="{G}" stroke-width="14" stroke-linecap="round" opacity=".85"/>')
    return page(1350,G,f'''{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:66px;line-height:1.06;font-weight:700;color:{IV}">Profissional altamente qualificado: como <span style="color:{GOLD};font-style:italic">renovar</span> a autorização?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350"><circle cx="540" cy="820" r="330" fill="{G2}" opacity=".75"/>{estrelas}{cartao}<path d="M0 1100H1080V1350H0Z" fill="#0B2F2D"/></svg>
    {foot(IV)}''')
IMG=[cover_hoja67()]
IMG.append(content2('Imigração · Quem pede','Empresa ou profissional','A renovação pode ser pedida pela <b>empresa ou pelo profissional estrangeiro</b>, pessoalmente ou por meio de representante legitimado, conforme a ficha oficial.',ic_diploma,'ivory',44))
IMG.append(content2('Imigração · Quando pedir','60 dias antes, 90 depois','O pedido é feito nos <b>60 dias naturais anteriores</b> ao vencimento. A ficha prevê também os <b>90 dias posteriores</b>, sem prejuízo de possível processo sancionador.',ic_60_90,'green',42))
IMG.append(content2('Imigração · Como pedir','Pela via telemática','A ficha oficial indica a apresentação <b>telemática</b>, pela sede eletrônica da UGE-CE. Pedido em prazo prorroga a validade da autorização anterior até a resolução.',ic_telemat,'terra',42))
IMG.append(content2('Imigração · Depois do pedido','Resposta e cartão','A ficha oficial prevê resolução em <b>20 dias</b>. Renovada, a TIE deve ser pedida em <b>1 mês</b>, em comissaria de Polícia. São previsões, não garantias.',ic_20dias,'ivory',42))
IMG.append(content2('Imigração · Atenção','Cada caso é diferente','A ficha é <b>orientativa</b>, foi atualizada em maio de 2025 e vale a norma vigente na data do pedido. Confira a sua situação antes de agir.',ic_atencao,'green',44))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 67.<br>Consulta em 23/11/2026.'))

# ---------- CULTURA (Reel 1080x1920): Constituição de 1978 ----------
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
def cardv(x,y,w,h,bg,svg): return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;background:{bg}"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg></div>'
def sc_livro():
    # livro aberto com páginas, ao lado urna; fundo areia
    pag=''.join(f'<path d="M{150} {200+i*70}H{410}M{510} {200+i*70}H{770}" stroke="{G2}" stroke-width="9" stroke-linecap="round" opacity=".7"/>' for i in range(6))
    return (f'<path d="M80 130Q290 90 460 150V700Q290 650 80 700Z" fill="{IV}" stroke="{G}" stroke-width="8"/><path d="M840 130Q630 90 460 150V700Q630 650 840 700Z" fill="{IV}" stroke="{G}" stroke-width="8"/>'
            f'{pag}<path d="M460 150V700" stroke="{GOLD}" stroke-width="10"/>'
            f'<rect x="300" y="740" width="320" height="60" rx="10" fill="{GOLD}"/>{T(460,785,"6 · 12 · 1978",40,G,800,"Lora")}')
def sc_etapas():
    nomes=['Comissão Constituinte','Pleno do Congresso','Senado','Comissão Mista']
    s=''
    for i,nm in enumerate(nomes):
        y=60+i*150
        s+=f'<rect x="{60+i*40}" y="{y}" width="{700-i*40}" height="110" rx="16" fill="{[IV,GOLD,IV,GOLD][i]}"/>'+T(60+i*40+(700-i*40)/2,y+68,nm,40,G,700,'Inter')
    return s+f'<path d="M810 80V640" stroke="{IV}" stroke-width="8" stroke-dasharray="4 18" stroke-linecap="round"/><path d="M810 680l-22-34h44z" fill="{IV}"/>'
def sc_voto():
    cedulas=''.join(f'<g transform="translate({x} {y}) rotate({r})"><rect width="170" height="210" rx="12" fill="{IV}"/><path d="M26 56H144M26 96H144" stroke="{G}" stroke-width="9" stroke-linecap="round"/><path d="M30 150L58 178L120 124" fill="none" stroke="{TERRA}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></g>' for x,y,r in ((90,50,-9),(330,20,4),(570,60,10),(210,270,6),(470,265,-6)))
    return cedulas+f'<rect x="120" y="520" width="620" height="84" rx="16" fill="{GOLD}"/>'+T(430,578,'abrumadora mayoría',44,G,800,'Lora')
def sc_linha():
    return (f'<rect x="60" y="360" width="700" height="12" rx="6" fill="{G}"/>'
            f'<circle cx="150" cy="366" r="30" fill="{GOLD}"/><circle cx="410" cy="366" r="30" fill="{TERRA}"/><circle cx="670" cy="366" r="30" fill="{G2}"/>'
            +T(150,290,'1976',56,G,800,'Lora')+T(410,290,'1977',56,G,800,'Lora')+T(670,290,'1978',56,G,800,'Lora')
            +T(150,470,'15/12',38,G,700)+T(410,470,'15/06',38,G,700)+T(670,470,'6/12',38,G,700)
            +f'<rect x="40" y="540" width="740" height="8" rx="4" fill="{GOLD}"/>')
CUL=[
 rbv(Tv('6 de dezembro de 1978: a Espanha aprovou a Constituição em referendo',74)+cardv(80,760,920,840,SAND,sc_livro().replace('820','820'))+f'<div class=abs style="left:80px;top:1640px;width:920px;font-size:40px;font-weight:700;color:@AC;letter-spacing:.04em">Constituição Espanhola</div>',1,'ivory'),
 rbv(Tv('O texto passou por várias etapas',90)+Pv('Foi discutido na Comissão Constituinte e no Pleno do Congresso, nos mesmos órgãos do Senado e numa Comissão Mista.',500)+cardv(80,1000,920,640,G2,sc_etapas()),2,'green'),
 rbv(Tv('Aprovada por esmagadora maioria',86)+Pv('Segundo o Congreso, o texto foi aprovado por <b>abrumadora mayoría</b> no referendo de 6 de dezembro de 1978.',500)+cardv(80,1000,920,640,TERRA if False else G,sc_voto()),3,'terra'),
 rbv(Tv('Antes, dois marcos',92)+Pv('A Lei para a Reforma Política foi a referendo em 15 de dezembro de 1976. As eleições para as Cortes constituintes foram em 15 de junho de 1977.',500)+cardv(80,1020,920,620,SAND,sc_linha()),4,'ivory'),
 closing(1920,G,IV,GOLD,'Fonte: Congreso de los Diputados (La Constitución de 1978).<br>Consulta em 23/11/2026.',logo=460,serif_sz=82,top=.10),
]

async def render(lst,prefix,h):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h})
        for i,htm in enumerate(lst):
            await pg.set_content(htm); await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT+f'{prefix}-{i+1}.png')
        await b.close()
if 'noticia' in which: asyncio.run(render(NOT,'noticia',1350))
if 'imigracao' in which: asyncio.run(render(IMG,'imigracao',1350))
if 'cultura' in which:
    asyncio.run(render(CUL,'cultura',1920))
    n=len(CUL); d=3.5; f=0.4
    cmd=['ffmpeg','-y','-loglevel','error']
    for i in range(n): cmd+=['-loop','1','-t',str(d),'-i',OUT+f'cultura-{i+1}.png']
    flt=''.join(f'[{i}:v]format=yuv420p,fade=t=in:st=0:d={f},fade=t=out:st={d-f}:d={f}[v{i}];' for i in range(n))
    flt+=''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[o]'
    cmd+=['-filter_complex',flt,'-map','[o]','-r','30','-pix_fmt','yuv420p',OUT+'reel-cultura.mp4']
    subprocess.run(cmd,check=True)
