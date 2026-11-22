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


# ================= 2026-11-22 =================
import subprocess
which=sys.argv[1:] or ['noticia','imigracao','cultura']

# ---------- NOTICIA: regularização extraordinária, balanço oficial ----------
def ic_pilha(a,b):
    return SV(''.join(f'<rect x="{34+i*5}" y="{150-i*26}" width="120" height="20" rx="4" fill="{a if i%2==0 else b}" stroke="{a}" stroke-width="3"/>' for i in range(5))+f'<path d="M64 36H136" stroke="{b}" stroke-width="7" stroke-linecap="round"/>')
def ic_cal_jul(a,b):
    return SV(f'<rect x="26" y="38" width="148" height="138" rx="14" fill="{a}"/><rect x="26" y="38" width="148" height="42" rx="14" fill="{b}"/><path d="M62 24V52M138 24V52" stroke="{a}" stroke-width="10" stroke-linecap="round"/>{T(100,152,"2/7",58,b,800,"Lora")}')
def ic_pedido_vs_autor(a,b):
    return SV(f'<rect x="14" y="52" width="64" height="96" rx="8" fill="{a}"/><path d="M28 80H64M28 100H64M28 120H52" stroke="{b}" stroke-width="7" stroke-linecap="round"/><rect x="122" y="52" width="64" height="96" rx="8" fill="none" stroke="{a}" stroke-width="7" stroke-dasharray="10 10"/>{T(100,116,"≠",56,a,800,"Inter")}<path d="M138 100L150 112L172 84" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" opacity=".0"/>')
def ic_lupa_predio(a,b):
    return SV(f'<path d="M22 150H128M32 150V84L75 54L118 84V150" fill="{a}" stroke="{a}" stroke-width="6"/><path d="M62 150V112H88V150" fill="{b}"/><circle cx="130" cy="78" r="38" fill="{b}" stroke="{a}" stroke-width="10"/><path d="M158 106L188 138" stroke="{a}" stroke-width="14" stroke-linecap="round"/>')
def cover_reg():
    folhas=''.join(f'<g transform="translate({130+i*150} {1030-i*45}) rotate({-6+i*3})"><rect width="130" height="{150+i*35}" y="{-(150+i*35)}" rx="10" fill="{IV}" opacity="{.55+i*.09:.2f}"/><path d="M22 {-(115+i*35)}H108M22 {-(85+i*35)}H108M22 {-(55+i*35)}H84" stroke="{G2}" stroke-width="8" stroke-linecap="round"/></g>' for i in range(6))
    return page(1350,G,f'''{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Imigração</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:70px;line-height:1.06;font-weight:700;color:{IV}">Regularização extraordinária: <span style="color:{GOLD};font-style:italic">1.174.978</span> solicitações recebidas</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="800" cy="700" r="230" fill="{G2}" opacity=".7"/>
      {folhas}
      <path d="M0 1060H1080V1350H0Z" fill="#0B2F2D"/>
      {T(540,1130,"Balanço oficial do prazo de apresentação",34,GOLD,700,"Inter",ls=2)}
    </svg>
    {foot(IV)}''')
NOT=[cover_reg()]
NOT.append(content2('Notícia · O que o Governo informou','Prazo encerrado','Segundo nota do <b>Ministerio de Inclusión</b>, o prazo de apresentação das solicitações da regularização extraordinária terminou com <b>1.174.978 solicitações recebidas</b>.',ic_pilha,'ivory',44))
NOT.append(content2('Notícia · Quando foi divulgado','Balanço de julho','A nota oficial com esse balanço é de <b>2 de julho de 2026</b>. O número reflete o fechamento do prazo de apresentação.',ic_cal_jul,'terra',46))
NOT.append(content2('Notícia · Como ler o número','Pedido não é autorização','O balanço informa <b>solicitações recebidas</b>. Ele não informa quantas foram resolvidas nem como cada processo terminou.',ic_pedido_vs_autor,'green',46))
NOT.append(content2('Notícia · Para acompanhar','Fontes oficiais','Para saber o andamento, consulte as páginas do <b>Ministerio de Inclusión</b> e do Governo sobre o processo de regularização.',ic_lupa_predio,'ivory',46))
NOT.append(closing(1350,G,IV,GOLD,'Fontes: Ministerio de Inclusión e La Moncloa, nota de 02/07/2026.<br>Consulta em 22/11/2026.'))

# ---------- IMIGRACAO: Hoja 10 renovação por reagrupação familiar (roteiro) ----------
def ic_familia_casa(a,b):
    return SV(f'<path d="M20 98L100 30L180 98" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><path d="M38 92V176H162V92L100 42Z" fill="{b}" stroke="{a}" stroke-width="7"/>{figura(72,104,.95,a)}{figura(128,104,.95,a)}{figura(100,122,.75,a)}')
def ic_calend_relogio(a,b):
    return SV(f'<rect x="20" y="34" width="120" height="124" rx="12" fill="{a}"/><rect x="20" y="34" width="120" height="34" rx="12" fill="{b}"/><path d="M52 22V46M108 22V46" stroke="{a}" stroke-width="9" stroke-linecap="round"/><circle cx="140" cy="138" r="44" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M140 112V140L158 152" fill="none" stroke="{a}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_elo(a,b):
    return SV(f'<circle cx="52" cy="84" r="24" fill="{a}"/><path d="M14 150C14 120 30 114 52 114C74 114 90 120 90 150Z" fill="{a}"/><circle cx="148" cy="84" r="24" fill="{a}"/><path d="M110 150C110 120 126 114 148 114C170 114 186 120 186 150Z" fill="{a}"/><path d="M82 86H118" stroke="{b}" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 14"/><circle cx="100" cy="86" r="11" fill="{b}"/>')
def ic_pasta_lupa(a,b):
    return SV(f'<path d="M20 60H76L90 78H170V164H20Z" fill="{a}"/><rect x="34" y="92" width="100" height="62" rx="6" fill="{b}"/><path d="M48 112H112M48 130H96" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="142" cy="130" r="24" fill="none" stroke="{b}" stroke-width="9"/><path d="M160 148L184 174" stroke="{b}" stroke-width="12" stroke-linecap="round"/>')
def ic_escudo_ok(a,b):
    return SV(f'<path d="M100 22L160 44V100C160 138 134 164 100 180C66 164 40 138 40 100V44Z" fill="{a}"/><path d="M100 36L148 52V100C148 130 128 152 100 166C72 152 52 130 52 100V52Z" fill="{b}"/><path d="M76 100L94 118L126 80" fill="none" stroke="{a}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
def cover_hoja10():
    casa=f'<path d="M190 640L540 330L890 640" fill="none" stroke="{TERRA}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/><path d="M250 610V990H830V610L540 380Z" fill="{G}"/>'
    fam=f'{figura(430,640,3.0,IV)}{figura(650,640,3.0,IV)}{figura(540,720,2.3,GOLD)}'
    anel=f'<g transform="translate(540 800)"><path d="M-310 0A310 310 0 1 1 -120 286" fill="none" stroke="{GOLD}" stroke-width="22" stroke-linecap="round" stroke-dasharray="4 34"/></g><path d="M-0 0" />'
    return page(1350,IV,f'''{bracket(TERRA)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Família</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:68px;line-height:1.06;font-weight:700;color:{G}">Como renovar a residência por <span style="color:{TERRA};font-style:italic">reagrupação familiar</span>?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="540" cy="840" r="330" fill="{SAND}"/>
      {anel}{casa}{fam}
      <path d="M0 1090H1080V1350H0Z" fill="{G}"/>
    </svg>
    {foot(IV)}''')
IMG=[cover_hoja10()]
IMG.append(content2('Imigração · Quem pede','O familiar reagrupado','A renovação trata de quem tem <b>autorização de residência temporal por reagrupação familiar</b> e precisa manter a situação regular quando ela se aproxima do vencimento.',ic_familia_casa,'green',44))
IMG.append(content2('Imigração · Quando pedir','Atenção ao prazo','A ficha oficial define o <b>momento do pedido</b> em relação ao vencimento. Confira a data da sua autorização e o prazo previsto na ficha.',ic_calend_relogio,'ivory',46))
IMG.append(content2('Imigração · O vínculo','Família e requisitos','A ficha trata do <b>vínculo familiar</b> com a pessoa que reagrupou e dos requisitos que devem continuar sendo cumpridos. Cada caso é diferente.',ic_elo,'terra',46))
IMG.append(content2('Imigração · Documentação','Reúna os documentos','Antes de pedir, separe os documentos listados na ficha oficial para a sua situação e <b>confira se há exigência de tradução</b> ou legalização.',ic_pasta_lupa,'ivory',46))
IMG.append(content2('Imigração · Depois do pedido','Resposta e prazos','A ficha oficial prevê prazos de resposta e de emissão da TIE. Consulte-os na ficha, pois são <b>previsões</b> e não garantias.',ic_escudo_ok,'green',46))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 10.<br>Consulta em 22/11/2026.'))

# ---------- CULTURA (Reel 1080x1920): Las Médulas ----------
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
RED='#9C4A32'; RED2='#7E3826'
def picos(base,cols=(TERRA,RED,RED2),w=920):
    return (f'<polygon points="0,{base} 120,{base-300} 230,{base-120} 360,{base-420} 500,{base-160} 640,{base-360} 780,{base-140} 920,{base-260} 920,{base} " fill="{cols[1]}"/>'
            f'<polygon points="0,{base} 60,{base-170} 190,{base-60} 300,{base-250} 430,{base-40} 560,{base-210} 700,{base-50} 830,{base-200} 920,{base-90} 920,{base}" fill="{cols[0]}"/>'
            f'<polygon points="0,{base} 920,{base} 920,{base-40} 0,{base-40}" fill="{cols[2]}"/>')
def sc_hook():
    return (f'<circle cx="680" cy="190" r="90" fill="{GOLD}" opacity=".9"/>'+picos(840)+
            f'<circle cx="360" cy="540" r="34" fill="{GOLD}"/><circle cx="360" cy="540" r="20" fill="none" stroke="{RED2}" stroke-width="5"/>'
            +''.join(f'<path d="M{x} 790c10-20 24-20 34 0" fill="none" stroke="{IV}" stroke-width="5" opacity=".5"/>' for x in (80,330,600)))
def sc_veios():
    veios=''.join(f'<path d="M{x} 760C{x+60} 600 {x-40} 480 {x+80} 330" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/>' for x in (180,380,560,740))
    tun=''.join(f'<rect x="{x}" y="{y}" width="46" height="70" rx="23" fill="{G}"/>' for x,y in ((250,620),(470,540),(650,640),(110,500)))
    return f'<polygon points="0,840 0,560 200,260 380,380 560,120 760,330 920,230 920,840" fill="{TERRA}"/>{veios}{tun}<rect y="800" width="920" height="40" fill="{RED2}"/>'
def sc_agua():
    canal=f'<path d="M0 120L560 300" stroke="{IV}" stroke-width="34" stroke-linecap="round"/><path d="M0 120L560 300" stroke="#E9DFC9" stroke-width="16" stroke-linecap="round"/>'
    gotas=''.join(f'<path d="M{x} {y}c-16 26-24 38-24 52a24 24 0 0 0 48 0c0-14-8-26-24-52z" fill="#E9DFC9" stroke="{IV}" stroke-width="4"/>' for x,y in ((590,340),(630,470),(570,560)))
    monte=f'<polygon points="480,860 480,420 600,420 600,520 720,520 720,640 840,640 840,760 920,760 920,860" fill="{RED}"/><polygon points="620,860 620,560 720,560 720,660 820,660 820,780 920,780 920,860" fill="{RED2}"/>'
    return monte+canal+gotas+f'<path d="M80 440L180 540L90 560Z" fill="{IV}" opacity=".0"/>'
def sc_selo():
    lou=''.join(f'<ellipse cx="{460+s*dx}" cy="{y}" rx="26" ry="54" transform="rotate({s*r} {460+s*dx} {y})" fill="{GOLD}"/>' for s in (-1,1) for dx,y,r in ((250,500,-20),(268,420,-34),(262,340,-48),(228,262,-62)))
    return (f'<circle cx="460" cy="430" r="300" fill="{G2}"/>{lou}<circle cx="460" cy="430" r="210" fill="{IV}"/>'
            f'<text x="460" y="470" text-anchor="middle" font-family="Lora" font-weight="700" font-size="140" fill="{G}">1997</text>'
            f'<polygon points="260,360 330,300 400,340 460,270 520,330 600,300 660,360" fill="none" stroke="{TERRA}" stroke-width="10" stroke-linejoin="round"/>'
            f'<rect x="150" y="780" width="620" height="8" rx="4" fill="{GOLD}"/>')
CUL=[
 rbv(Tv('Uma montanha escavada pelos romanos virou Patrimônio Mundial',82)+cardv(80,760,920,840,G2,sc_hook())+f'<div class=abs style="left:80px;top:1640px;width:920px;font-size:40px;font-weight:700;color:@AC;letter-spacing:.04em">Las Médulas, em León</div>',1,'green'),
 rbv(Tv('Uma das grandes minas de ouro do Império Romano',78)+Pv('Em Las Médulas, na província de León, os romanos exploraram ouro em escala enorme.',560)+cardv(80,980,920,640,SAND,sc_veios()),2,'ivory'),
 rbv(Tv('A água fazia o trabalho',90)+Pv('Canais traziam água das montanhas. Ela derrubava a rocha e carregava o material, para separar o ouro.',500)+cardv(80,1000,920,620,TERRA if False else RED2,sc_agua()),3,'terra'),
 rbv(Tv('Patrimônio Mundial desde 1997',90)+Pv('A UNESCO reconheceu a paisagem de Las Médulas como Patrimônio Mundial em 1997.',500)+cardv(80,900,920,720,G2,sc_selo()),4,'green'),
 closing(1920,G,IV,GOLD,'Fontes: UNESCO (Las Médulas, ficha 803); Turespaña (spain.info).<br>Consulta em 22/11/2026.',logo=460,serif_sz=82,top=.10),
]
# a tela 5 precisa do contador? closing não mostra.

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
