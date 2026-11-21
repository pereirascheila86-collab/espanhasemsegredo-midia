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

# ================= 2026-11-21 =================
# ---------- NOTICIA: SMI 2027 ----------
def ic_ata(a,b):
    return SV(f'<path d="M48 18H128L160 50V182H48Z" fill="{b}" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><path d="M128 18V50H160" fill="none" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><path d="M68 78H132M68 98H132M68 118H108" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="128" cy="152" r="22" fill="{a}"/><path d="M118 152L126 160L140 144" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_barras_alta(a,b):
    return SV(f'<rect x="26" y="130" width="34" height="46" rx="4" fill="{a}"/><rect x="74" y="100" width="34" height="76" rx="4" fill="{a}"/><rect x="122" y="66" width="34" height="110" rx="4" fill="{a}"/><path d="M28 90L84 52L112 70L170 22" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M146 20H172V46" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_sol_dia(a,b):
    r=''.join(f'<path d="M100 100L{100+84*math.cos(math.radians(t)):.1f} {100+84*math.sin(math.radians(t)):.1f}" stroke="{a}" stroke-width="8" stroke-linecap="round"/>' for t in range(0,360,45))
    return SV(f'{r}<circle cx="100" cy="100" r="48" fill="{b}" stroke="{a}" stroke-width="8"/>{T(100,116,"€",52,a,800,"Lora")}')
def ic_grupo(a,b):
    return SV(f'{figura(60,40,1.5,b)}{figura(140,40,1.5,b)}{figura(100,26,2.0,a)}<path d="M24 176H176" stroke="{a}" stroke-width="9" stroke-linecap="round"/>')
def ic_casa_euro(a,b):
    return SV(f'<path d="M22 96L100 28L178 96" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><path d="M42 90V176H158V90L100 40Z" fill="{b}" stroke="{a}" stroke-width="7"/><circle cx="100" cy="122" r="28" fill="{a}"/>{T(100,134,"€",36,b,800,"Lora")}')
def cover_smi():
    barras=''.join(f'<rect x="{x}" y="{1050-h}" width="110" height="{h}" rx="8" fill="{IV}" opacity="{o}"/>' for x,h,o in ((170,160,.35),(310,260,.5),(450,370,.7),(590,480,.9),(730,610,1)))
    moeda=lambda cx,cy,r,t:f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD}"/><circle cx="{cx}" cy="{cy}" r="{r-16}" fill="none" stroke="{TERRA}" stroke-width="5"/>{T(cx,cy+r*.32,"€",int(r*1.0),TERRA,800,"Lora")}'
    seta=f'<path d="M170 800L420 640L560 560L800 360" fill="none" stroke="{GOLD}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 30"/>'
    return page(1350,TERRA,f'''{bracket('#F3D79A')}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:72px;line-height:1.05;font-weight:700;color:{IV}">Governo aprova salário mínimo de <span style="color:#F3D79A;font-style:italic">1.286 euros</span> para 2027</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="540" cy="820" r="340" fill="{G}" opacity=".35"/>
      {barras}{seta}{moeda(820,330+110,120,'')}{moeda(300,640,70,'')}
      <path d="M0 1050H1080V1350H0Z" fill="{G}"/>
      {T(540,1150,"1.286 € · 14 pagas · a partir de 1/1/2027",34,GOLD,700,"Inter",ls=2)}
    </svg>
    {foot(IV)}''')
NOT=[cover_smi()]
NOT.append(content2('Notícia · O que foi aprovado','Consejo de Ministros, 17/11','O Governo aprovou o <b>salário mínimo interprofissional de 2027</b>: <b>1.286 euros brutos por mês</b>, em <b>14 pagas</b>, segundo o Ministerio de Trabajo e a EFE.',ic_ata,'ivory',44))
NOT.append(content2('Notícia · Quanto muda','Alta de 5,3%','O novo valor vale <b>a partir de 1º de janeiro de 2027</b> e equivale a <b>18.004 euros brutos por ano</b>, segundo as duas fontes consultadas.',ic_barras_alta,'green',46))
NOT.append(content2('Notícia · Valor diário','42,87 € por dia','O comunicado do Ministerio de Trabajo indica <b>42,87 euros brutos por dia</b>. Para contratos de duração determinada: <b>60,88 euros</b> por jornada.',ic_sol_dia,'terra',46))
NOT.append(content2('Notícia · Quem é alcançado','Cerca de 2,7 milhões','Segundo a EFE, a medida alcança cerca de <b>2,7 milhões de trabalhadores</b>, <b>13,6%</b> dos assalariados.',ic_grupo,'ivory',50))
NOT.append(content2('Notícia · Trabalho doméstico','10,06 € por hora','Para empregadas do lar, o comunicado indica <b>10,06 euros brutos por hora</b>. Valores brutos: antes de impostos e contribuições.',ic_casa_euro,'green',46))
NOT.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: Ministerio de Trabajo y Economía Social (17/11/2026); RTVC/EFE (17/11/2026).<br>Consulta em 21/11/2026.'))

# ---------- IMIGRACAO: renovacao residencia e trabalho por conta alheia (Hoja 13) ----------
def ic_ampulheta(a,b):
    return SV(f'<path d="M50 20H150M50 180H150" stroke="{a}" stroke-width="12" stroke-linecap="round"/><path d="M58 24C58 84 96 90 96 100C96 110 58 116 58 176H142C142 116 104 110 104 100C104 90 142 84 142 24Z" fill="{b}" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><path d="M80 164H120L100 134Z" fill="{a}"/><path d="M92 52H108" stroke="{a}" stroke-width="7" stroke-linecap="round"/>')
def ic_ponte_validade(a,b):
    return SV(f'<rect x="14" y="62" width="64" height="76" rx="8" fill="{a}"/><rect x="122" y="62" width="64" height="76" rx="8" fill="{a}"/><path d="M78 100H122" stroke="{a}" stroke-width="12" stroke-dasharray="4 14" stroke-linecap="round"/><path d="M104 84L124 100L104 116" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><circle cx="46" cy="100" r="14" fill="{b}"/><circle cx="154" cy="100" r="14" fill="{b}"/>')
def ic_maleta_check(a,b):
    return SV(f'<rect x="26" y="66" width="148" height="106" rx="14" fill="{a}"/><path d="M72 66V50C72 40 80 34 90 34H110C120 34 128 40 128 50V66" fill="none" stroke="{a}" stroke-width="10"/><path d="M26 112H174" stroke="{b}" stroke-width="6"/><circle cx="100" cy="124" r="22" fill="{b}"/><path d="M90 124L98 132L112 114" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_tela_balcao(a,b):
    return SV(f'<rect x="20" y="30" width="104" height="72" rx="8" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M8 120H136L126 104H18Z" fill="{a}"/><path d="M60 52L72 64L96 40" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M128 100L176 100V176H128Z" fill="{a}"/><circle cx="152" cy="126" r="11" fill="{b}"/><path d="M136 160C136 146 142 142 152 142C162 142 168 146 168 160Z" fill="{b}"/>')
def ic_cartao_tie(a,b):
    return SV(f'<rect x="16" y="46" width="168" height="110" rx="14" fill="{a}"/><circle cx="62" cy="92" r="19" fill="{b}"/><path d="M34 138C34 118 46 112 62 112C78 112 90 118 90 138Z" fill="{b}"/><path d="M110 82H164M110 102H164M110 122H146" stroke="{b}" stroke-width="7" stroke-linecap="round"/><path d="M148 42A26 26 0 0 1 184 66" fill="none" stroke="{b}" stroke-width="6" stroke-linecap="round"/>')
def cover_renov():
    cartao=f'<g transform="translate(250 560) rotate(-6)"><rect width="580" height="360" rx="30" fill="{IV}"/><rect width="580" height="76" rx="30" fill="{GOLD}"/><rect y="46" width="580" height="30" fill="{GOLD}"/>{T(40,52,"RESIDENCIA Y TRABAJO",24,G,800,"Inter",anchor="start",ls=3)}<circle cx="150" cy="210" r="52" fill="{G2}"/><path d="M82 330C82 270 112 262 150 262C188 262 218 270 218 330Z" fill="{G2}"/><path d="M290 190H520M290 230H520M290 270H460" stroke="{G}" stroke-width="12" stroke-linecap="round"/></g>'
    seta=f'<path d="M820 520A190 190 0 1 1 560 400" fill="none" stroke="{TERRA}" stroke-width="30" stroke-linecap="round"/><path d="M520 360L592 396L540 452Z" fill="{TERRA}"/>'
    cal=f'<g transform="translate(110 940)"><rect width="230" height="190" rx="18" fill="{IV}"/><rect width="230" height="52" rx="18" fill="{TERRA}"/>{T(115,38,"4 ANOS",30,IV,800,"Inter",ls=4)}{T(115,148,"+4",98,G,800,"Lora")}</g>'
    return page(1350,G,f'''{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:66px;line-height:1.06;font-weight:700;color:{IV}">Como renovar a residência e o trabalho <span style="color:{GOLD};font-style:italic">por conta alheia</span>?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="540" cy="740" r="330" fill="{G2}" opacity=".6"/>
      {seta}{cartao}{cal}
      <path d="M0 1180H1080V1350H0Z" fill="#0B2F2D"/>
    </svg>
    {foot(IV)}''')
IMG=[cover_renov()]
IMG.append(content2('Imigração · Quando pedir','Nos 2 meses antes do vencimento','A ficha oficial prevê o pedido <b>nos 2 meses anteriores</b> ao vencimento. Também admite até <b>3 meses depois</b>, com possível procedimento sancionador.',ic_ampulheta,'ivory',44))
IMG.append(content2('Imigração · Durante a tramitação','Validade prorrogada','Segundo a ficha, apresentar o pedido <b>dentro do prazo</b> prorroga a validade da autorização anterior <b>até a resolução</b> do procedimento.',ic_ponte_validade,'terra',46))
IMG.append(content2('Imigração · O que se comprova','Continuidade do trabalho','Continuar a relação de trabalho ou outra hipótese da ficha, como prestação de desemprego. Exige ainda <b>não ter antecedentes penais na Espanha</b> e pagar a taxa.',ic_maleta_check,'green',42))
IMG.append(content2('Imigração · Como pedir','Presencial ou telemático','Na <b>Oficina de Extranjería</b> da província ou por via telemática, na sede eletrônica. Documentos estrangeiros pedem tradutor jurado e apostila ou legalização.',ic_tela_balcao,'ivory',42))
IMG.append(content2('Imigração · Depois do pedido','Resposta e validade','A ficha oficial prevê resposta em até <b>3 meses</b>. A renovação é de <b>4 anos</b>, salvo residência de longa duração. A TIE é pedida em <b>1 mês</b> após a notificação.',ic_cartao_tie,'green',42))
IMG.append(closing(1350,TERRA,IV,'#F3D79A','Fonte: Ministerio de Inclusión, Hoja 13 (atualizada em maio de 2025).<br>Consulta em 21/11/2026.'))

async def render(lst,prefix,h):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':h})
        for i,htm in enumerate(lst):
            await pg.set_content(htm); await pg.wait_for_timeout(500)
            await pg.screenshot(path=OUT+f'{prefix}-{i+1}.png')
        await b.close()
asyncio.run(render(NOT,'noticia',1350))
asyncio.run(render(IMG,'imigracao',1350))
