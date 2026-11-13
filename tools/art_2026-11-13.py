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
    <div class=abs style="left:50%;margin-left:-65px;top:{int(h*top)+logo+60+serif_sz*3.5+50}px;width:130px;height:5px;background:{acc}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3.5+90}px;text-align:center;font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
    <div class=abs style="left:{pad}px;right:{pad}px;top:{int(h*top)+logo+60+serif_sz*3.5+170}px;text-align:center;font-size:40px;color:{fg}">Siga <b>@espanhasemsegredo</b></div>
    <div class=abs style="left:{pad+20}px;right:{pad+20}px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg};opacity:.85">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>'''
    return page(h,bg,inner)



import math, subprocess
def figura(cx,top,s,col):
    return f'<circle cx="{cx}" cy="{top+14*s}" r="{14*s}" fill="{col}"/><path d="M{cx-18*s} {top+78*s}V{top+46*s}C{cx-18*s} {top+34*s} {cx+18*s} {top+34*s} {cx+18*s} {top+46*s}V{top+78*s}Z" fill="{col}"/>'
import math, subprocess
# ================= 2026-11-12 : ícones e cenas novos =================
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

# ---------- CULTURA (Reel 1080x1920): Alhambra ----------
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
def cardv(x,y,w,h,bg,svg,dy=0): return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;background:{bg}"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><g transform="translate(0,{dy})">{svg}</g></svg></div>'

# ================= 2026-11-13 : ícones e cenas novos =================
import random
def mosaico(x0,y0,w,h,cols,seed=1,cell=46):
    rnd=random.Random(seed); s=''
    for gx in range(int(w//cell)+1):
        for gy in range(int(h//cell)+1):
            px=x0+gx*cell+rnd.uniform(-5,5); py=y0+gy*cell+rnd.uniform(-5,5)
            pts=[(px,py),(px+cell*rnd.uniform(.8,1.1),py+rnd.uniform(-6,6)),(px+cell*rnd.uniform(.8,1.1),py+cell*rnd.uniform(.8,1.1)),(px+rnd.uniform(-6,6),py+cell*rnd.uniform(.8,1.1))]
            s+=f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" fill="{rnd.choice(cols)}" stroke="{G}" stroke-width="2"/>'
    return s

# ---- ícones NOTÍCIA (BOE / retorno) ----
def ic_boe(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M46 14H128L160 46V186H46Z" fill="{a}"/><path d="M128 14V46H160" fill="{b}"/><path d="M64 78H142M64 100H142M64 122H112" stroke="{b}" stroke-width="8" stroke-linecap="round"/><circle cx="128" cy="152" r="20" fill="{b}"/><circle cx="128" cy="152" r="11" fill="none" stroke="{a}" stroke-width="4"/><text x="64" y="58" font-family="Lora" font-weight="700" font-size="26" fill="{b}">BOE</text></svg>'
def ic_cal29(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="22" y="30" width="156" height="148" rx="16" fill="{b}" stroke="{a}" stroke-width="8"/><rect x="22" y="30" width="156" height="42" rx="14" fill="{a}"/><text x="100" y="140" text-anchor="middle" font-family="Lora" font-weight="700" font-size="70" fill="{a}">29</text><text x="100" y="166" text-anchor="middle" font-family="Inter" font-weight="800" font-size="20" letter-spacing="4" fill="{a}">NOV</text><path d="M58 18V42M142 18V42" stroke="{a}" stroke-width="9" stroke-linecap="round"/></svg>'
def ic_return(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M104 96L158 48L190 76V156H104Z" fill="{a}"/><rect x="132" y="112" width="28" height="44" fill="{b}"/><path d="M14 150C20 84 70 46 120 44" fill="none" stroke="{a}" stroke-width="8" stroke-dasharray="3 14" stroke-linecap="round"/><path d="M120 24L148 44L120 66Z" fill="{b}" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><circle cx="24" cy="160" r="14" fill="{a}"/><circle cx="24" cy="160" r="5" fill="{b}"/></svg>'
def ic_cert(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="18" y="36" width="164" height="116" rx="8" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M42 70H158M42 92H158M42 114H112" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="142" cy="132" r="24" fill="{a}"/><path d="M130 150L124 186L142 174L160 186L154 150Z" fill="{a}"/><circle cx="142" cy="132" r="12" fill="{b}"/></svg>'
def ic_helphand(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="52" r="34" fill="{b}" stroke="{a}" stroke-width="8"/><text x="100" y="64" text-anchor="middle" font-family="Lora" font-weight="700" font-size="44" fill="{a}">€</text><path d="M16 130L56 116L108 124L146 108C160 102 172 116 160 126L112 154H62L16 160Z" fill="{a}"/><path d="M62 154L112 154" stroke="{b}" stroke-width="5"/></svg>'

# ---- ícones IMIGRAÇÃO (exceção à autorização de trabalho) ----
def ic_90(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="104" r="76" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M100 104L100 50M100 104L140 126" stroke="{a}" stroke-width="9" stroke-linecap="round"/><circle cx="100" cy="104" r="9" fill="{a}"/><rect x="50" y="8" width="100" height="30" rx="15" fill="{a}"/><text x="100" y="30" text-anchor="middle" font-family="Inter" font-weight="800" font-size="19" fill="{b}">90 dias</text></svg>'
def ic_flask(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M78 20H122M86 20V76L36 156C28 172 38 184 54 184H146C162 184 172 172 164 156L114 76V20" fill="{b}" stroke="{a}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/><path d="M58 138H142L160 160C164 170 158 176 148 176H52C42 176 36 170 40 160Z" fill="{a}"/><circle cx="96" cy="112" r="7" fill="{a}"/><circle cx="114" cy="94" r="5" fill="{a}"/></svg>'
def ic_press(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="22" y="34" width="156" height="132" rx="12" fill="{b}" stroke="{a}" stroke-width="8"/><rect x="40" y="52" width="58" height="42" fill="{a}"/><path d="M112 56H160M112 76H160M112 96H144M40 114H160M40 134H160M40 152H120" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'
def ic_passcheck(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="12" width="120" height="164" rx="14" fill="{a}"/><circle cx="100" cy="72" r="28" fill="none" stroke="{b}" stroke-width="6"/><path d="M72 72H128M100 44V100M82 52C92 72 92 72 82 92M118 52C108 72 108 72 118 92" stroke="{b}" stroke-width="3" fill="none"/><path d="M62 126H138M62 146H112" stroke="{b}" stroke-width="7" stroke-linecap="round"/><circle cx="148" cy="152" r="28" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M134 152L144 163L164 138" fill="none" stroke="{a}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_span(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M24 128H176" stroke="{a}" stroke-width="10" stroke-linecap="round"/><circle cx="36" cy="128" r="14" fill="{a}"/><circle cx="100" cy="128" r="14" fill="{b}" stroke="{a}" stroke-width="7"/><circle cx="164" cy="128" r="14" fill="{a}"/><text x="36" y="86" text-anchor="middle" font-family="Lora" font-weight="700" font-size="40" fill="{a}">15d</text><text x="100" y="62" text-anchor="middle" font-family="Lora" font-weight="700" font-size="40" fill="{a}">2m</text><text x="164" y="86" text-anchor="middle" font-family="Lora" font-weight="700" font-size="40" fill="{a}">1a</text><path d="M36 156V168M100 156V168M164 156V168" stroke="{a}" stroke-width="6" stroke-linecap="round"/></svg>'

T=5
# ---------- NOTÍCIA (capa verde, página do BOE + caminho de volta) ----------
def boe_cover():
    linhas=''.join(f'<rect x="{150}" y="{300+i*42}" width="{[380,330,380,260,380,350,300][i%7]}" height="12" rx="6" fill="{G}" opacity=".55"/>' for i in range(8))
    return page(1350,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 70% 78%,{G2} 0,{G} 62%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · BOE de 9/11</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:76px;line-height:1.07;font-weight:700;color:{IV}">BOE publica o regulamento do <span style="color:{GOLD};font-style:italic">Estatuto da cidadania espanhola</span> no exterior</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <g transform="rotate(-5 380 880)"><rect x="140" y="570" width="500" height="640" rx="14" fill="{IV}"/><rect x="140" y="570" width="500" height="92" rx="14" fill="{SAND}"/>
      <text x="176" y="634" font-family="Lora" font-weight="700" font-size="60" fill="{G}">BOE</text><text x="400" y="634" font-family="Inter" font-weight="700" font-size="24" letter-spacing="3" fill="{TERRA}">9 NOV 2026</text>
      <g transform="translate(0,400)">{linhas}</g>
      <circle cx="540" cy="1100" r="58" fill="{GOLD}"/><circle cx="540" cy="1100" r="44" fill="none" stroke="{G}" stroke-width="4" stroke-dasharray="3 8"/><path d="M516 1102L534 1120L568 1074" fill="none" stroke="{G}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></g>
      <path d="M600 640C700 540 820 520 900 600" fill="none" stroke="{GOLD}" stroke-width="7" stroke-dasharray="4 20" stroke-linecap="round"/>
      <path d="M884 570L934 612L876 632Z" fill="{GOLD}"/>
      <path d="M760 1000L890 880L1020 1000V1196H760Z" fill="{TERRA}"/><rect x="860" y="1070" width="58" height="126" fill="{IV}"/><circle cx="906" cy="1136" r="6" fill="{G}"/><rect x="800" y="1030" width="44" height="44" fill="{IV}"/>
      <rect x="690" y="1196" width="400" height="14" fill="{GOLD}"/>
    </svg>
    {foot(IV)}''')
NOT=[boe_cover()]
NOT.append(content2('Notícia · O que foi publicado','O Real Decreto 954/2026','Publicado no BOE de <b>9 de novembro</b>, o decreto aprova o regulamento da Lei 40/2006, do Estatuto da cidadania espanhola no exterior.',ic_boe,'ivory',54))
NOT.append(content2('Notícia · Quando vale','Entrada em vigor','A norma entra em vigor <b>20 dias após a publicação</b>, em 29 de novembro de 2026. O direito à assistência sanitária de certos grupos começa um ano depois da publicação.',ic_cal29,'terra',54))
NOT.append(content2('Notícia · Retorno','Quem é pessoa retornada','É quem tem nacionalidade espanhola de origem, viveu fora e volta para residir de forma definitiva. O regulamento exige <b>12 meses</b> de inscrição consular antes da baixa.',ic_return,'green',54))
NOT.append(content2('Notícia · O certificado','Documentos e prazo','O artigo 9 prevê DNI ou passaporte, certidão de nascimento, baixa consular e empadronamiento histórico. A Dirección General tem até <b>três meses</b> para reconhecer a condição.',ic_cert,'ivory',54))
NOT.append(content2('Notícia · Ajuda ao retorno','Subvenção prevista','O texto prevê uma ajuda a espanhóis de origem em vulnerabilidade econômica, por real decreto. <b>Valores e requisitos</b> ainda não constam do BOE.',ic_helphand,'green',54))
NOT.append(closing(1350,G2,IV,GOLD,'Fonte: BOE, Real Decreto 954/2026 (BOE-A-2026-23384, de 9/11/2026).<br>Consulta em 13/11/2026.'))

# ---------- IMIGRAÇÃO (capa marfim, porta em arco + ícones em órbita) ----------
def porta_cover():
    def orb(cx,cy,fn,bg,fg,ib):
        return f'<circle cx="{cx}" cy="{cy}" r="82" fill="{bg}"/><g transform="translate({cx-52} {cy-52})"><svg width="104" height="104" viewBox="0 0 200 200">{fn(fg,ib)[fn(fg,ib).index(">")+1:-6]}</svg></g>'
    return page(1350,IV,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 50% 78%,{SAND} 0,{IV} 70%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:76px;line-height:1.07;font-weight:700;color:{G}">Residência com <span style="color:{TERRA};font-style:italic">exceção</span> da autorização de trabalho: quem pode pedir?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <path d="M300 1190V800C300 640 400 560 540 560C680 560 780 640 780 800V1190Z" fill="{G}"/>
      <path d="M345 1190V810C345 676 430 606 540 606C650 606 735 676 735 810V1190Z" fill="{GOLD}"/>
      <path d="M345 1190V830C345 690 420 626 480 618L480 1190Z" fill="{G2}"/>
      <path d="M480 618C560 618 735 676 735 810V1190H480Z" fill="{IV}" opacity=".92"/>
      <circle cx="540" cy="760" r="22" fill="{GOLD}"/><path d="M540 782V850" stroke="{G}" stroke-width="10"/>
      <rect x="230" y="1190" width="620" height="24" fill="{G2}"/><rect x="200" y="1214" width="680" height="22" fill="{G}"/>
      {orb(160,640,ic_flask,TERRA,IV,TERRA)}
      {orb(920,640,ic_press,G2,IV,G2)}
      {orb(130,960,ic_cert,GOLD,G,GOLD)}
      {orb(950,960,ic_passcheck,TERRA,IV,TERRA)}
    </svg>
    {foot(G)}''')
IMG=[porta_cover()]
IMG.append(content2('Imigração · O que é','Exceção à autorização de trabalho','Reconhece a exceção para atividade com duração prevista <b>superior a 90 dias</b>. Quem não reside na Espanha e fica até 90 dias deve pedir um visto de curta duração.',ic_90,'terra',52))
IMG.append(content2('Imigração · Ensino e pesquisa','Pesquisa, ensino e cultura','Técnicos, pesquisadores e cientistas convidados ou contratados por entidades públicas ou universidades; professores de universidade espanhola; e pessoal de instituições culturais.',ic_flask,'green',52))
IMG.append(content2('Imigração · Outros casos','Outros casos da ficha','Correspondentes de meios estrangeiros acreditados, ministros de culto, dirigentes de sindicatos e organizações empresariais e prestação transnacional de serviços, entre outros.',ic_press,'ivory',52))
IMG.append(content2('Imigração · Requisitos e pedido','Requisitos e onde pedir','Não ser cidadão da UE, não estar em situação irregular, não ter antecedentes penais e pagar a taxa. O pedido é pessoal: no consulado ou, na Espanha, na Oficina de Extranjería.',ic_passcheck,'green',52))
IMG.append(content2('Imigração · Prazos da ficha oficial','Prazos e validade','A ficha oficial prevê resolução em <b>15 dias</b> no consulado e em <b>dois meses</b> na Espanha. A autorização inicial vale pela duração da atividade, até um ano.',ic_span,'terra',52))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 16 (atualizada em maio de 2025).<br>Consulta em 13/11/2026.'))

# ---------- CULTURA (Reel 1080x1920): obras de Gaudí ----------
def espiral(cx,base,h,w,col,rib):
    # pináculo estriado com topo arredondado e esfera
    top=base-h
    return (f'<path d="M{cx-w/2} {base}L{cx-w/2*0.8} {top+60}C{cx-w/2*0.8} {top+10} {cx+w/2*0.8} {top+10} {cx+w/2*0.8} {top+60}L{cx+w/2} {base}Z" fill="{col}"/>'
            +''.join(f'<path d="M{cx+i*w/6:.1f} {base}L{cx+i*w/6*0.8:.1f} {top+70}" stroke="{rib}" stroke-width="3"/>' for i in (-2,-1,0,1,2))
            +f'<circle cx="{cx}" cy="{top-8}" r="{w*0.16:.1f}" fill="{GOLD}"/><path d="M{cx} {top-8+w*0.16:.1f}V{top+20}" stroke="{col}" stroke-width="5"/>')
def cena_gaudi_capa(w,h):
    sol=f'<circle cx="480" cy="360" r="250" fill="{GOLD}"/>'+''.join(f'<path d="M480 360L{480+330*math.cos(a):.1f} {360+330*math.sin(a):.1f}" stroke="{GOLD}" stroke-width="4" opacity=".5"/>' for a in [i*math.pi/14 for i in range(28)])
    torres=''.join(espiral(cx,860,hh,ww,col,rib) for cx,hh,ww,col,rib in [(210,520,120,TERRA,G),(360,640,140,SAND,TERRA),(540,720,150,IV,TERRA),(720,620,140,SAND,TERRA),(860,500,120,TERRA,G)])
    arcos=''.join(f'<path d="M{x} 1180V1010C{x} 930 {x+54} 890 {x+100} 890C{x+146} 890 {x+200} 930 {x+200} 1010V1180" fill="none" stroke="{GOLD}" stroke-width="14" stroke-linecap="round"/>' for x in (-10,190,390,590,790))
    base=f'<rect x="0" y="860" width="{w}" height="{h-860}" fill="{G2}"/>'
    mos=f'<g clip-path="url(#cm)">{mosaico(0,1020,w,h-1020,[TERRA,GOLD,SAND,IV,G],seed=4,cell=52)}</g><defs><clipPath id="cm"><rect x="0" y="1020" width="{w}" height="{h-1020}"/></clipPath></defs>'
    return sol+torres+base+arcos+mos
def cena_catenaria(w,h):
    # 1984 -> 2005: 3 -> 7 arcos catenários
    def arco(cx,top,base,wd,col):
        return f'<path d="M{cx-wd/2} {base}C{cx-wd/2} {top+40} {cx-wd/4} {top} {cx} {top}C{cx+wd/4} {top} {cx+wd/2} {top+40} {cx+wd/2} {base}" fill="none" stroke="{col}" stroke-width="18" stroke-linecap="round"/>'
    esq=''.join(arco(x,300+(i%2)*30,590,118,TERRA) for i,x in enumerate((110,235,360)))
    dir_=''.join(arco(x,300+(i%2)*30,590,76,TERRA) for i,x in enumerate((540,616,692,768,844,920,996)) if x<950)
    return (f'<text x="235" y="190" text-anchor="middle" font-family="Lora" font-weight="700" font-size="150" fill="{GOLD}">1984</text><text x="235" y="240" text-anchor="middle" font-family="Inter" font-weight="800" font-size="28" letter-spacing="5" fill="{IV}">TRÊS OBRAS</text>'
            +f'<text x="740" y="190" text-anchor="middle" font-family="Lora" font-weight="700" font-size="150" fill="{GOLD}">2005</text><text x="740" y="240" text-anchor="middle" font-family="Inter" font-weight="800" font-size="28" letter-spacing="5" fill="{IV}">SETE OBRAS</text>'
            +esq+dir_+f'<path d="M440 460H500M480 436L506 460L480 484" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
            +f'<path d="M40 590H920" stroke="{IV}" stroke-width="6"/>')
def tile(x,y,s,n,glyph,bg,fg):
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="26" fill="{bg}"/><g transform="translate({x} {y})">{glyph}</g>'
            f'<circle cx="{x+36}" cy="{y+36}" r="26" fill="{fg}"/><text x="{x+36}" y="{y+47}" text-anchor="middle" font-family="Lora" font-weight="700" font-size="34" fill="{bg}">{n}</text>')
def cena_sete(w,h):
    s=210; g={}
    c1=TERRA; c2=G; c3=SAND
    g[1]=f'<path d="M30 150Q60 100 100 140T170 120V170H30Z" fill="{c1}"/><path d="M30 178H180" stroke="{c1}" stroke-width="6"/><circle cx="60" cy="130" r="8" fill="{GOLD}"/><circle cx="120" cy="130" r="8" fill="{IV}"/>'
    g[2]=f'<path d="M50 190V110C50 60 150 60 150 110V190" fill="none" stroke="{c1}" stroke-width="14"/><path d="M80 190V120C80 96 120 96 120 120V190Z" fill="{c1}"/>'
    g[3]=f'<path d="M20 70Q60 50 105 70T190 70V180Q150 200 105 180T20 180Z" fill="{c1}"/><path d="M20 112Q60 94 105 112T190 112M20 146Q60 128 105 146T190 146" fill="none" stroke="{c3}" stroke-width="5"/>'
    g[4]=''.join(f'<rect x="{34+i*38}" y="{58+j*38}" width="34" height="34" fill="{c1 if (i+j)%2==0 else GOLD}"/>' for i in range(4) for j in range(4))
    g[5]=f'<path d="M30 70H180V190H30Z" fill="{c1}"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="17" fill="{c3}"/>' for x,y in [(66,100),(105,100),(144,100),(86,150),(124,150)])
    g[6]=espiral(105,190,150,64,c1,c3)
    g[7]=f'<path d="M30 190L70 100M180 190L140 100M105 190V90" stroke="{c1}" stroke-width="16" stroke-linecap="round"/><path d="M40 90C70 50 140 50 170 90" fill="none" stroke="{c1}" stroke-width="12" stroke-linecap="round"/>'
    pos=[(30,110),(255,110),(480,110),(705,110),(140,390),(375,390),(610,390)]
    out=''.join(tile(x,y,s,i+1,g[i+1],G,GOLD) for i,(x,y) in enumerate(pos))
    return out
def cena_selo2(w,h):
    mos=f'<defs><clipPath id="cc"><circle cx="480" cy="300" r="250"/></clipPath></defs><g clip-path="url(#cc)">{mosaico(230,50,500,500,[TERRA,GOLD,G,G2,SAND,IV],seed=9,cell=44)}</g>'
    aro=f'<circle cx="480" cy="300" r="250" fill="none" stroke="{G}" stroke-width="12"/><circle cx="480" cy="300" r="146" fill="{G}"/>'
    txt=f'<text x="480" y="318" text-anchor="middle" font-family="Lora" font-weight="700" font-size="54" fill="{GOLD}">UNESCO</text><text x="480" y="360" text-anchor="middle" font-family="Inter" font-weight="800" font-size="17" letter-spacing="2" fill="{IV}">PATRIMÔNIO MUNDIAL</text>'
    crit=''.join(f'<rect x="{x}" y="592" width="150" height="86" rx="43" fill="{G}"/><text x="{x+75}" y="650" text-anchor="middle" font-family="Lora" font-weight="700" font-size="48" fill="{GOLD}">{t}</text>' for x,t in [(150,'(i)'),(330,'(ii)'),(510,'(iv)')])
    return mos+aro+txt+crit+f'<text x="480" y="724" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="4" fill="{G}">CRITÉRIOS</text>'
def reel():
    S=[]
    S.append(rbv(f'''{Tv('Sete obras de <span style="color:@AC;font-style:italic">Gaudí</span> são Patrimônio Mundial',86)}
    {cardv(60,560,960,1180,G,cena_gaudi_capa(960,1180))}''',1,'terra'))
    S.append(rbv(f'''{Tv('De <span style="color:@AC">1984</span> a 2005',100)}
    {Pv('Em 1984, a UNESCO inscreveu o Parque Güell, o Palácio Güell e a Casa Milà. Em 2005, o conjunto foi ampliado e passou a integrar “Obras de Antoni Gaudí”.',420)}
    {cardv(60,860,960,840,G,cena_catenaria(960,840),40)}''',2,'green'))
    S.append(rbv(f'''{Tv('Sete obras em <span style="color:@AC">Barcelona e arredores</span>',80)}
    {Pv('Parque Güell, Palácio Güell, Casa Milà, Casa Vicens, Casa Batlló, a Fachada da Natividade e a Cripta da Sagrada Família e a Cripta da Colônia Güell.',500)}
    {cardv(60,960,960,780,SAND,cena_sete(960,780),20)}''',3,'ivory'))
    S.append(rbv(f'''{Tv('Por que a UNESCO as <span style="color:@AC">destaca</span>',86)}
    {Pv('Segundo a UNESCO, são uma contribuição criativa excepcional à arquitetura e à técnica construtiva entre os séculos XIX e XX, ligada ao Modernismo catalão.',470)}
    {cardv(60,900,960,820,SAND,cena_selo2(960,820),50)}''',4,'terra'))
    S.append(closing(1920,G,IV,GOLD,'Fonte: UNESCO, Centro do Patrimônio Mundial, “Works of Antoni Gaudí” (ref. 320).<br>Consulta em 13/11/2026.',logo=460,serif_sz=88,top=.2))
    return S

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
S=reel(); asyncio.run(render(S,'cultura',1920))
n=len(S); d=3.5; f=0.4
cmd=['ffmpeg','-y','-loglevel','error']
for i in range(n): cmd+=['-loop','1','-t',str(d),'-i',OUT+f'cultura-{i+1}.png']
flt=''.join(f'[{i}:v]format=yuv420p,fade=t=in:st=0:d={f},fade=t=out:st={d-f}:d={f}[v{i}];' for i in range(n))
flt+=''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[o]'
cmd+=['-filter_complex',flt,'-map','[o]','-r','30','-pix_fmt','yuv420p',OUT+'reel-cultura.mp4']
subprocess.run(cmd,check=True)
