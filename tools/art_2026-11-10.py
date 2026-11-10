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



# ================= 2026-11-10 : ícones e cenas novos =================
def ic_phone(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="62" y="16" width="76" height="168" rx="16" fill="{a}"/><rect x="72" y="36" width="56" height="112" rx="4" fill="{b}"/><circle cx="100" cy="166" r="7" fill="{b}"/><path d="M84 70H116M84 92H116M84 114H104" stroke="{a}" stroke-width="6" stroke-linecap="round"/><path d="M150 52C164 62 164 92 150 102M164 40C186 58 186 96 164 114" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round"/></svg>'
def ic_table(a,b):
    s=''.join(f'<circle cx="{100+78*__import__("math").cos(i*1.0472):.1f}" cy="{100+78*__import__("math").sin(i*1.0472):.1f}" r="16" fill="{a}"/>' for i in range(6))
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200">{s}<circle cx="100" cy="100" r="50" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M100 76L106 94H125L110 105L116 123L100 112L84 123L90 105L75 94H94Z" fill="{a}"/></svg>'
def ic_plane(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 14C108 14 112 24 112 36V72L184 118V138L112 114V150L134 168V182L100 172L66 182V168L88 150V114L16 138V118L88 72V36C88 24 92 14 100 14Z" fill="{a}"/><circle cx="100" cy="46" r="8" fill="{b}"/></svg>'
def ic_eight(a,b):
    rows=''.join(f'<circle cx="62" cy="{50+i*30}" r="9" fill="{a}"/><path d="M82 {50+i*30}H146" stroke="{a}" stroke-width="7" stroke-linecap="round"/>' for i in range(5))
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="34" y="20" width="132" height="160" rx="12" fill="{b}" stroke="{a}" stroke-width="6"/>{rows}<text x="146" y="176" text-anchor="end" font-family="Lora" font-weight="700" font-size="30" fill="{a}">8</text></svg>'
def ic_balance(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 24V168M60 172H140" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M34 60H166" stroke="{a}" stroke-width="8" stroke-linecap="round"/><circle cx="100" cy="24" r="10" fill="{a}"/><path d="M34 60L14 112H54Z M166 60L146 112H186Z" fill="{b}" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><path d="M14 112C14 134 54 134 54 112M146 112C146 134 186 134 186 112" fill="{a}"/></svg>'
def ic_resid(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="30" y="42" width="140" height="130" rx="14" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="30" y="42" width="140" height="36" rx="14" fill="{a}"/><path d="M62 24V54M138 24V54" stroke="{a}" stroke-width="9" stroke-linecap="round"/><text x="100" y="140" text-anchor="middle" font-family="Lora" font-weight="700" font-size="44" fill="{a}">1 ano</text></svg>'
def figura(cx,top,s,col):
    return f'<circle cx="{cx}" cy="{top+14*s}" r="{14*s}" fill="{col}"/><path d="M{cx-18*s} {top+78*s}V{top+46*s}C{cx-18*s} {top+34*s} {cx+18*s} {top+34*s} {cx+18*s} {top+46*s}V{top+78*s}Z" fill="{col}"/>'
def ic_family(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><g>{figura(58,40,1.6,a)}{figura(142,40,1.6,a)}{figura(100,92,1.2,b)}</g><path d="M30 178H170" stroke="{a}" stroke-width="7" stroke-linecap="round"/><rect x="82" y="92" width="36" height="86" rx="10" fill="{b}" opacity="0"/></svg>'
def ic_pct(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="82" fill="{a}"/><text x="100" y="116" text-anchor="middle" font-family="Lora" font-weight="700" font-size="52" fill="{b}">150%</text><text x="100" y="146" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" letter-spacing="3" fill="{b}">IPREM</text></svg>'
def ic_reporthome(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 18L176 84H24Z" fill="{a}"/><rect x="40" y="84" width="120" height="96" fill="{a}"/><rect x="112" y="108" width="62" height="78" rx="8" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M124 130H162M124 148H162M124 166H148" stroke="{a}" stroke-width="5" stroke-linecap="round"/><rect x="64" y="110" width="30" height="30" rx="4" fill="{b}"/></svg>'
def ic_mercurio(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="20" y="36" width="160" height="104" rx="12" fill="{a}"/><rect x="32" y="48" width="136" height="80" rx="4" fill="{b}"/><path d="M80 164H120M100 140V164" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M100 62C86 62 78 72 78 84C78 98 100 116 100 116C100 116 122 98 122 84C122 72 114 62 100 62Z" fill="{a}"/><circle cx="100" cy="84" r="7" fill="{b}"/></svg>'

# ---------- NOTÍCIA ----------
import math
def mesa_cover():
    seats=''.join(f'<circle cx="{540+280*math.cos(i*math.pi/3+0.52):.1f}" cy="{900+280*math.sin(i*math.pi/3+0.52):.1f}" r="46" fill="{G2}" stroke="{GOLD}" stroke-width="5"/>' for i in range(6))
    isl=''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{GOLD}"/>' for x,y,rx,ry in [(120,580,34,20),(190,610,26,16),(250,578,22,14),(300,620,16,10),(166,660,14,9)])
    return page(1350,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 50% 66%,{G2} 0,{G} 70%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Canárias</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:880px;font-size:84px;line-height:1.05;font-weight:700;color:{IV}">Comissão de Imigração se reúne <span style="color:{GOLD};font-style:italic">hoje</span> por causa das Canárias</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">{isl}<path d="M320 600C420 600 440 680 480 760" fill="none" stroke="{GOLD}" stroke-width="4" stroke-dasharray="3 14" stroke-linecap="round"/>
    {seats}<circle cx="540" cy="900" r="200" fill="{IV}"/><circle cx="540" cy="900" r="182" fill="none" stroke="{GOLD}" stroke-width="4"/>
    <text x="540" y="896" text-anchor="middle" font-family="Lora" font-weight="700" font-size="54" fill="{G}">La Moncloa</text>
    <text x="540" y="944" text-anchor="middle" font-family="Inter" font-weight="700" font-size="26" letter-spacing="6" fill="{TERRA}">10 DE NOVEMBRO</text></svg>
    <div class=abs style="left:80px;top:1150px;font-size:30px;font-weight:600;letter-spacing:.14em;color:{GOLD}">DESLIZE  →</div>
    <div class=abs style="left:0;right:0;bottom:0;height:140px;background:{G2};opacity:0"></div>
    {foot(GOLD)}''')

NOT=[mesa_cover()]; T=7
NOT.append(content(2,T,'Notícia · A convocatória','Reunião pedida por Sánchez','Em 7 de novembro, após falar com o presidente canário, Fernando Clavijo, Pedro Sánchez se comprometeu a convocar os ministérios e a reforçar os recursos sanitários em <b>El Hierro</b>.',ic_phone,'ivory'))
NOT.append(content(3,T,'Notícia · Quem participa','Seis ministérios na mesa','A Comissão é presidida por <b>Ángel Víctor Torres</b>. Clavijo e o presidente do Cabildo de El Hierro, Alpidio Armas, participam de forma extraordinária. A reunião é antes do Conselho de Ministros.',ic_table,'green'))
NOT.append(content(4,T,'Notícia · Transferências','Voos à Península','Em 7 de novembro, dois Airbus A330 do Ejército del Aire levaram mais de <b>300 pessoas</b> de El Hierro a Torrejón de Ardoz, segundo o Euronews. Novos voos não estão descartados.',ic_plane,'terra'))
NOT.append(content(5,T,'Notícia · O que pedem as Canárias','Pacto com oito pontos','O Pacto Canario por la Migración pede plano extraordinário de contingência, coordenação permanente e gestão diplomática no Senegal. Sem respostas concretas, as ilhas falam em recorrer à Justiça.',ic_eight,'ivory'))
NOT.append(content(6,T,'Notícia · As posições','Governo e PP divergem','Torres defende as transferências para o arquipélago não virar uma “cárcel de inmigrantes”. Feijóo, do PP, diz que as ilhas precisam de “algo más” do que uma reunião.',ic_balance,'green'))
NOT.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: Diario de Avisos (07/11/2026) e Euronews (09/11/2026).<br>Consulta em 10/11/2026.'))

# ---------- IMIGRAÇÃO ----------
def familia_cover():
    fam=figura(250,640,3.4,IV)+figura(400,640,3.4,IV)+figura(325,730,2.5,GOLD)
    casa=f'<path d="M110 700L325 520L540 700Z" fill="{G}"/><rect x="140" y="690" width="370" height="330" fill="{G}"/><path d="M110 1020H540" stroke="{GOLD}" stroke-width="6"/>'
    return page(1350,IV,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{IV} 0%,{SAND} 100%)"></div>
    <div class=abs style="left:520px;top:600px;width:620px;height:620px;border-radius:50%;background:{TERRA}"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Família</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:880px;font-size:88px;line-height:1.05;font-weight:700;color:{G}">Quer trazer a família para a Espanha? Veja a <span style="color:{TERRA};font-style:italic">reagrupação</span> familiar</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350"><g transform="translate(0,80)">{casa}{fam}<rect x="290" y="900" width="70" height="120" rx="35" fill="{TERRA}"/></g>
      <circle cx="840" cy="860" r="110" fill="{G2}"/><ellipse cx="840" cy="860" rx="44" ry="110" fill="none" stroke="{GOLD}" stroke-width="4"/><path d="M730 860H950M752 800H928M752 920H928" stroke="{GOLD}" stroke-width="4"/><path d="M840 750V970" stroke="{GOLD}" stroke-width="4"/>
      <path d="M560 760C620 700 700 700 740 780" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="3 14" stroke-linecap="round"/></svg>
    <div class=abs style="left:80px;top:1190px;font-size:30px;font-weight:600;letter-spacing:.14em;color:{G}">DESLIZE  →</div>
    {foot(G)}''')
IMG=[familia_cover()]
IMG.append(content(2,T,'Imigração · Quem reagrupa','Quem pode reagrupar','Estrangeiro residente na Espanha <b>há pelo menos um ano</b>, com autorização para outro ano, no mínimo. A ficha prevê exceções para titulares de residência de longa duração.',ic_resid,'ivory'))
IMG.append(content(3,T,'Imigração · Quem é reagrupado','Quem pode ser reagrupado','Cônjuge ou parceiro maior de 18 anos (apenas um), filhos menores de 18 e ascendentes de primeiro grau a cargo, com mais de 65 anos, conforme as condições da ficha.',ic_family,'terra'))
IMG.append(content(4,T,'Imigração · Meios econômicos','Meios econômicos','Para dois membros, a ficha exige <b>150% do IPREM</b> mensal. Cada membro adicional soma 50%. Com menores, há regras próprias de cálculo.',ic_pct,'green'))
IMG.append(content(5,T,'Imigração · Moradia','Moradia adequada','Comprova-se com relatório da Comunidade Autônoma do local de residência, válido por até seis meses. Se não vier em um mês, admitem-se outros meios de prova, com o comprovante do pedido.',ic_reporthome,'ivory'))
IMG.append(content(6,T,'Imigração · Pedido e prazos','Pedido e prazos','O reagrupante pede na Oficina de Extranjería da província ou pela sede eletrônica Mercurio. A ficha oficial prevê resolução em dois meses. Depois, o familiar tem dois meses para pedir o visto.',ic_mercurio,'terra'))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 8 (atualizada em maio de 2025).<br>Consulta em 10/11/2026.'))

# ---------- CULTURA (Reel 1080x1920, fundo verde) ----------
def rbv(inner,n):
    return page(1920,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:radial-gradient(circle at 20% 90%,{G2} 0,{G} 65%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{GOLD}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">{n} / 5</span></div>''')
def Tv(t,sz=88): return f'<div class="abs serif" style="left:80px;top:220px;width:920px;font-size:{sz}px;line-height:1.06;font-weight:700;color:{IV}">{t}</div>'
def Pv(t,top=520): return f'<div class=abs style="left:80px;top:{top}px;width:920px;font-size:44px;line-height:1.4;color:{IV};opacity:.95">{t}</div>'
def cardv(x,y,w,h,bg,svg): return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;background:{bg}"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg></div>'
def cena_montanhas(w,h):
    arv=''.join(f'<path d="M{x} {y}l22 -60l22 60z" fill="{G}"/>' for x,y in [(60,640),(110,660),(760,650),(820,630),(870,664)])
    return (f'<circle cx="760" cy="150" r="80" fill="{GOLD}"/>'
      f'<path d="M0 420L180 220L300 330L470 140L650 360L780 270L960 420V{h}H0Z" fill="{G2}"/>'
      f'<path d="M0 520C200 420 360 470 520 440C700 410 820 470 960 430V{h}H0Z" fill="{G}"/>'
      f'<rect x="380" y="470" width="180" height="150" fill="{IV}"/><path d="M360 470L470 400L580 470Z" fill="{TERRA}"/><rect x="560" y="400" width="52" height="220" fill="{IV}"/><path d="M552 400L586 350L620 400Z" fill="{TERRA}"/><path d="M440 620V540C440 515 500 515 500 540V620Z" fill="{G}"/><circle cx="586" cy="440" r="10" fill="{G}"/>'
      +arv+f'<rect x="0" y="{h-50}" width="{w}" height="50" fill="{G}"/>')
def cena_selo(w,h):
    return (f'<defs><path id="cs" d="M480 340m-250 0a250 250 0 1 1 500 0a250 250 0 1 1 -500 0"/></defs>'
      f'<circle cx="480" cy="340" r="290" fill="none" stroke="{GOLD}" stroke-width="8"/><circle cx="480" cy="340" r="270" fill="none" stroke="{GOLD}" stroke-width="3"/><circle cx="480" cy="340" r="180" fill="{TERRA}"/>'
      f'<text font-family="Inter" font-weight="800" font-size="36" letter-spacing="10" fill="{GOLD}"><textPath href="#cs">FIESTA · DE · INTERÉS · TURÍSTICO · FIESTA · DE · INTERÉS ·</textPath></text>'
      f'<path d="M480 240C440 240 414 270 414 306C414 356 480 420 480 420C480 420 546 356 546 306C546 270 520 240 480 240Z" fill="{IV}"/><circle cx="480" cy="304" r="22" fill="{TERRA}"/>'
      f'<text x="480" y="715" text-anchor="middle" font-family="Lora" font-weight="700" font-size="64" fill="{IV}">Moreda · Aller</text>')
def cena_gaita(w,h):
    pipes=''.join(f'<rect x="{x}" y="{y}" width="26" height="{hh}" rx="10" fill="{GOLD}"/><rect x="{x-6}" y="{y+hh*0.35:.0f}" width="38" height="14" rx="5" fill="{IV}"/>' for x,y,hh in [(540,60,330),(600,40,360),(660,90,300)])
    ribs=''.join(f'<path d="M{200+i*50} 330Q{240+i*50} 440 {200+i*50} 560" fill="none" stroke="{IV}" stroke-width="3" opacity=".55"/>' for i in range(6))
    return (pipes+f'<ellipse cx="400" cy="450" rx="210" ry="140" fill="{TERRA}" transform="rotate(-14 400 450)"/>'+ribs+
      f'<path d="M240 520L90 640" stroke="{GOLD}" stroke-width="30" stroke-linecap="round"/><path d="M90 640L52 676" stroke="{IV}" stroke-width="16" stroke-linecap="round"/>'
      f'<path d="M520 520L760 640" stroke="{GOLD}" stroke-width="26" stroke-linecap="round"/><path d="M760 640L860 700" stroke="{IV}" stroke-width="22" stroke-linecap="round"/>'
      +''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="{G}"/>' for x,y in [(640,600),(690,622),(730,640)])
      +f'<path d="M740 150C760 110 820 110 840 150" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/><path d="M714 120C750 60 830 60 866 120" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>')
def cena_pao(w,h):
    cuts=''.join(f'<path d="M{480+r*math.cos(a):.0f} {400+r*math.sin(a):.0f}L{480+(r+70)*math.cos(a):.0f} {400+(r+70)*math.sin(a):.0f}" stroke="{TERRA}" stroke-width="14" stroke-linecap="round" transform="rotate(0)"/>' for a in [x*math.pi/3 for x in range(6)] for r in [60])
    return (f'<ellipse cx="480" cy="440" rx="250" ry="200" fill="{GOLD}"/><ellipse cx="480" cy="400" rx="250" ry="200" fill="{GOLD}" stroke="{TERRA}" stroke-width="8"/>'+cuts+f'<circle cx="480" cy="400" r="46" fill="{TERRA}"/>'
      f'<path d="M230 560C330 640 630 640 730 560" fill="none" stroke="{IV}" stroke-width="26" stroke-linecap="round"/>')
def cena_fabada(w,h):
    feij=''.join(f'<ellipse cx="{x}" cy="{y}" rx="26" ry="16" fill="{IV}" transform="rotate({r} {x} {y})"/>' for x,y,r in [(360,350,20),(430,336,-15),(500,344,30),(570,338,-25),(630,352,10),(400,372,-20),(470,376,15),(540,374,-10),(600,372,25)])
    vap=''.join(f'<path d="M{x} 270c-22 -34 22 -52 0 -90" fill="none" stroke="{IV}" stroke-width="6" stroke-linecap="round" opacity=".6"/>' for x in (420,500,580))
    casa=''.join(f'<path d="M{x} {y}a70 70 0 0 1 140 0Z" fill="{SAND}"/><path d="M{x+10} {y-8}a60 60 0 0 1 120 0" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="2 10" stroke-linecap="round"/>' for x,y in [(560,690),(760,690)])
    return (vap+f'<ellipse cx="500" cy="360" rx="190" ry="40" fill="{INK}"/><path d="M310 360C310 560 380 620 500 620C620 620 690 560 690 360Z" fill="{TERRA}"/><ellipse cx="500" cy="352" rx="176" ry="30" fill="{GOLD}"/>'+feij
      +f'<path d="M300 400C240 400 240 480 310 480M700 400C760 400 760 480 690 480" fill="none" stroke="{TERRA}" stroke-width="18" stroke-linecap="round"/>'+casa
      +f'')
def reel():
    S=[]
    S.append(rbv(f'''{Tv('Amanhã é dia de <span style="color:%s;font-style:italic">San Martín</span> em Moreda, nas Astúrias'%GOLD)}
    {cardv(60,780,960,860,SAND,cena_montanhas(960,860))}''',1))
    S.append(rbv(f'''{Tv('Uma festa de <span style="color:%s">interesse turístico</span>'%GOLD,84)}
    {Pv('Em Moreda, no concelho de Aller, a Sociedade Humanitarios de San Martín organiza a festa em 11 de novembro.',500)}
    {cardv(60,900,960,760,G2,cena_selo(960,760))}''',2))
    S.append(rbv(f'''{Tv('Missa com <span style="color:%s">gaitas</span> e leilão do pão'%GOLD,84)}
    {Pv('A missa de São Martinho é cantada, com gaitas asturianas. O pão de escanda abençoado é leiloado: a puya del ramu.',500)}
    {cardv(60,900,960,760,G2,'<g transform="translate(-10,90) scale(.74)">'+cena_gaita(960,760)+'</g><g transform="translate(560,150) scale(.5)">'+cena_pao(960,760)+'</g>')}''',3))
    S.append(rbv(f'''{Tv('Desfile e <span style="color:%s">almoço</span> típico'%GOLD)}
    {Pv('Carros alegóricos, bandas de gaitas, grupos de dança e as xandas, com trajes tradicionais. No almoço: fabada, casadiellas e panchón.',480)}
    {cardv(60,900,960,760,G2,'<g transform="translate(0,30)">'+cena_fabada(960,760)+'</g>')}''',4))
    S.append(closing(1920,TERRA,IV,'#F3D79A','Fonte: Turespaña, spain.info (Fiesta de San Martín o de los Humanitarios).<br>Consulta em 10/11/2026.',logo=460,serif_sz=88,top=.2))
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
