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


# ================= 2026-11-14 : ícones e cenas novos =================
def content2(kick,title,body,icon_fn,theme,bs=50):
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

# ---------- ícones NOTÍCIA (Supremo) ----------
def ic_balanca(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 24V168M60 176H140" stroke="{a}" stroke-width="10" stroke-linecap="round"/><path d="M34 62H166" stroke="{a}" stroke-width="9" stroke-linecap="round"/><circle cx="100" cy="24" r="11" fill="{a}"/><path d="M34 62L10 122H58Z M166 62L142 122H190Z" fill="none" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M8 122Q34 150 60 122Z M140 122Q166 150 192 122Z" fill="{a}"/><circle cx="100" cy="100" r="14" fill="{b}"/></svg>'
def ic_familia(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="64" cy="48" r="22" fill="{a}"/><path d="M26 140V96C26 76 102 76 102 96V140Z" fill="{a}"/><circle cx="144" cy="82" r="17" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M114 160V124C114 108 174 108 174 124V160Z" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M20 176H180" stroke="{a}" stroke-width="8" stroke-linecap="round"/></svg>'
def ic_lista(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="34" y="14" width="116" height="164" rx="10" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M56 56H128M56 84H128M56 112H100" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="142" cy="140" r="34" fill="{a}"/><text x="142" y="150" text-anchor="middle" font-family="Inter" font-weight="800" font-size="25" fill="{b}">CERA</text></svg>'
def ic_cal20(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="22" y="30" width="156" height="148" rx="16" fill="{b}" stroke="{a}" stroke-width="8"/><rect x="22" y="30" width="156" height="42" rx="14" fill="{a}"/><text x="100" y="134" text-anchor="middle" font-family="Lora" font-weight="700" font-size="66" fill="{a}">20</text><text x="100" y="164" text-anchor="middle" font-family="Inter" font-weight="800" font-size="18" letter-spacing="2" fill="{a}">DIAS ÚTEIS</text><path d="M58 18V42M142 18V42" stroke="{a}" stroke-width="9" stroke-linecap="round"/></svg>'
def ic_martelo(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><g transform="rotate(-35 100 90)"><rect x="52" y="40" width="96" height="46" rx="10" fill="{a}"/><rect x="92" y="86" width="16" height="92" rx="7" fill="{a}"/></g><ellipse cx="108" cy="172" rx="70" ry="14" fill="{a}"/><rect x="40" y="152" width="136" height="14" rx="6" fill="{b}" stroke="{a}" stroke-width="4"/></svg>'

def cover_tribunal():
    cols=''.join(f'<rect x="{x}" y="780" width="64" height="360" fill="{IV}"/><rect x="{x-12}" y="760" width="88" height="26" fill="{SAND}"/><rect x="{x-12}" y="1140" width="88" height="26" fill="{SAND}"/><path d="M{x+16} 800V1130M{x+32} 800V1130M{x+48} 800V1130" stroke="{G2}" stroke-width="3" opacity=".6"/>' for x in (190,326,462,598,734))
    return page(1350,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 50% 70%,{G2} 0,{G} 66%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Tribunal Supremo</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:70px;line-height:1.07;font-weight:700;color:{IV}">Supremo cita <span style="color:{GOLD};font-style:italic">filhos maiores de espanhóis</span> com nacionalidade pela Lei de Memória Democrática</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <path d="M130 760L540 520L950 760Z" fill="{SAND}"/><path d="M200 740L540 556L880 740Z" fill="{G}"/>
      <circle cx="540" cy="672" r="46" fill="{GOLD}"/>
      <g transform="translate(500 632) scale(.4)"><path d="M100 24V168M60 176H140" stroke="{G}" stroke-width="12" stroke-linecap="round"/><path d="M34 62H166" stroke="{G}" stroke-width="12" stroke-linecap="round"/><path d="M8 122Q34 150 60 122Z M140 122Q166 150 192 122Z" fill="{G}"/><path d="M34 62L10 122M34 62L58 122M166 62L142 122M166 62L190 122" stroke="{G}" stroke-width="8"/></g>
      <rect x="150" y="744" width="780" height="22" fill="{IV}"/>
      {cols}
      <rect x="150" y="1166" width="780" height="22" fill="{IV}"/><rect x="120" y="1188" width="840" height="22" fill="{SAND}"/><rect x="90" y="1210" width="900" height="22" fill="{GOLD}"/>
      <path d="M150 640C100 560 80 470 130 400" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="4 16" stroke-linecap="round" opacity=".7"/>
    </svg>
    {foot(IV)}''')
NOT=[cover_tribunal()]
NOT.append(content2('Notícia · A providência','Sala Terceira do Supremo','Em <b>10 de novembro de 2026</b>, a Sala Terceira do Tribunal Supremo determinou o emplazamiento (citação) no procedimento <b>1013/2026</b>.',ic_martelo,'ivory'))
NOT.append(content2('Notícia · Quem é citado','Filhos e filhas maiores de idade','De espanhóis que obtiveram a nacionalidade pela <b>Lei 20/2022</b> (Memória Democrática), inscritos no CERA e no anexo III da Instrução de 25/10/2022.',ic_familia,'terra',48))
NOT.append(content2('Notícia · Quem consta na lista','CERA e anexo III','O texto usa a inscrição no Censo Eleitoral de Residentes Ausentes (CERA) como critério. Não indica efeitos sobre o voto nem sobre a nacionalidade.',ic_lista,'green',48))
NOT.append(content2('Notícia · O prazo','Vinte dias úteis','O prazo conta a partir do dia seguinte à publicação da resolução no <b>BOE</b>. O interessado pode comparecer como parte codemandada.',ic_cal20,'ivory'))
NOT.append(content2('Notícia · Como comparecer','Advogado e procurador','Quem quiser intervir deve nomear advogado e procurador e, se achar adequado, apresentar contestação à demanda no momento processual correspondente.',ic_balanca,'terra',48))
NOT.append(closing(1350,G2,IV,GOLD,'Fonte: Ministerio de Asuntos Exteriores, providência do Tribunal Supremo de 10/11/2026 (proc. 1013/2026).<br>Consulta em 14/11/2026.'))

# ---------- ícones IMIGRAÇÃO (temporada) ----------
def ic_broto(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 184V96" stroke="{a}" stroke-width="10" stroke-linecap="round"/><path d="M100 110C100 60 60 40 24 48C26 92 58 112 100 110Z" fill="{a}"/><path d="M100 90C100 46 134 24 176 30C174 74 142 96 100 90Z" fill="{b}" stroke="{a}" stroke-width="7"/><path d="M40 184H160" stroke="{a}" stroke-width="9" stroke-linecap="round"/></svg>'
def ic_9m(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="76" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M100 36A64 64 0 1 1 39 118" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round"/><text x="100" y="118" text-anchor="middle" font-family="Lora" font-weight="700" font-size="70" fill="{a}">9</text><text x="100" y="150" text-anchor="middle" font-family="Inter" font-weight="800" font-size="19" letter-spacing="2" fill="{a}">MESES</text></svg>'
def ic_predio(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="46" width="120" height="132" fill="{a}"/><path d="M28 46L100 10L172 46Z" fill="{a}"/><rect x="58" y="70" width="26" height="26" fill="{b}"/><rect x="116" y="70" width="26" height="26" fill="{b}"/><rect x="58" y="112" width="26" height="26" fill="{b}"/><rect x="116" y="112" width="26" height="26" fill="{b}"/><rect x="86" y="140" width="28" height="38" fill="{b}"/></svg>'
def ic_casa(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M20 98L100 30L180 98" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><path d="M44 90V176H156V90L100 44Z" fill="{a}"/><rect x="84" y="118" width="32" height="58" fill="{b}"/><path d="M62 108H92M108 108H138" stroke="{b}" stroke-width="7" stroke-linecap="round"/></svg>'
def ic_laptop(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="38" y="40" width="124" height="86" rx="10" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M14 148H186L170 130H30Z" fill="{a}"/><path d="M62 70H138M62 92H110" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="142" cy="96" r="12" fill="{a}"/><path d="M137 96L141 100L148 91" stroke="{b}" stroke-width="4" fill="none" stroke-linecap="round"/></svg>'
def ic_aviao(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M20 120L88 100L58 28L82 28L128 92L170 78C186 74 192 90 176 98L130 114L96 176H72L88 118L38 134Z" fill="{a}"/><path d="M20 170H110" stroke="{a}" stroke-width="7" stroke-dasharray="4 14" stroke-linecap="round"/></svg>'

def cover_campo():
    fil=''
    for i in range(9):
        y=700+i*58; sp=0.55+i*0.12
        fil+=f'<path d="M{540-420*sp:.0f} {y+60}L540 700" stroke="{G2}" stroke-width="{5+i*2}" opacity=".9"/>'
    cestos=''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{G}"/><circle cx="{x-r*.3:.0f}" cy="{y-r*.3:.0f}" r="{r*.4:.0f}" fill="{G2}"/><circle cx="{x+r*.45:.0f}" cy="{y+r*.1:.0f}" r="{r*.22:.0f}" fill="{GOLD}"/>' for x,y,r in [(150,1010,64),(300,1070,58),(870,1000,66),(740,1090,60),(560,1130,56)])
    return page(1350,TERRA,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 50% 54%,#D9744F 0,{TERRA} 64%)"></div>
    {bracket('#F3D79A')}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:70px;line-height:1.07;font-weight:700;color:{IV}">Trabalho de <span style="color:#F3D79A;font-style:italic">temporada</span>: como funciona a autorização de residência e trabalho?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="540" cy="640" r="150" fill="#F3D79A"/>
      <path d="M0 700C220 650 400 670 540 690C700 664 880 650 1080 696V1350H0Z" fill="{GOLD}"/>
      <path d="M0 800C240 748 420 770 540 790C720 760 900 748 1080 796V1350H0Z" fill="{G2}"/>
      {''.join(f'<path d="M0 {880+i*66}C260 {850+i*66} 800 {910+i*66} 1080 {874+i*66}" fill="none" stroke="{G}" stroke-width="{10+i*3}" stroke-linecap="round"/><path d="M0 {880+i*66}C260 {850+i*66} 800 {910+i*66} 1080 {874+i*66}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="2 26" stroke-linecap="round"/>' for i in range(6))}
      {cestos}
      <g transform="translate(790 560)"><path d="M0 110V0" stroke="{G}" stroke-width="7"/><path d="M0 70C-36 66-52 40-50 14C-14 18 2 40 0 70Z" fill="{G}"/><path d="M0 50C30 46 52 26 52 0C22 4 2 24 0 50Z" fill="{G}"/></g>
    </svg>
    {foot(IV)}''')
IMG=[cover_campo()]
IMG.append(content2('Imigração · O que é','Autorização de temporada','Permite a uma pessoa estrangeira maior de 16 anos residir e trabalhar por conta alheia em atividade de temporada, por até <b>nove meses</b> em cada ano civil.',ic_9m,'green',48))
IMG.append(content2('Imigração · Quem pede','O empregador solicita','O pedido é do empregador, pessoalmente ou por representante legal. O trabalhador não pode estar nem residir na Espanha. No primeiro ano, precisa do visto específico para entrar.',ic_predio,'ivory',46))
IMG.append(content2('Imigração · O trabalhador','Requisitos do trabalhador','Sem antecedentes penais na Espanha e nos países onde viveu nos últimos cinco anos, e compromisso de regressar ao país de origem ao fim da relação laboral.',ic_aviao,'terra',48))
IMG.append(content2('Imigração · O empregador','Obrigações do empregador','Contrato fixo-descontínuo por escrito, pagamento da viagem de chegada, seguro de saúde, alojamento adequado e em dia com tributos e Seguridade Social.',ic_casa,'green',48))
IMG.append(content2('Imigração · Pedido e prazos','Como e quando pedir','Pedido telemático, com pelo menos <b>dois meses</b> de antecedência. A ficha oficial prevê um mês para resolver a autorização inicial, válida por quatro anos.',ic_laptop,'ivory',46))
IMG.append(closing(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Hoja 23 (atualizada em maio de 2025).<br>Consulta em 14/11/2026.'))

# ---------- CULTURA (Reel): Las Médulas ----------
def picos(base,cols,seed,n,x0,x1,hmin,hmax,wmin,wmax):
    rnd=random.Random(seed); s=''
    for i in range(n):
        cx=rnd.uniform(x0,x1); h=rnd.uniform(hmin,hmax); w=rnd.uniform(wmin,wmax); c=rnd.choice(cols)
        s+=f'<path d="M{cx-w/2:.0f} {base}L{cx-w*.18:.0f} {base-h:.0f}L{cx-w*.04:.0f} {base-h*1.05:.0f}L{cx+w*.2:.0f} {base-h*.96:.0f}L{cx+w/2:.0f} {base}Z" fill="{c}"/>'
    return s
def castanheiro(x,y,s,c1,c2):
    return f'<rect x="{x-6*s}" y="{y-20*s}" width="{12*s}" height="{40*s}" fill="{c2}"/><circle cx="{x}" cy="{y-40*s}" r="{34*s}" fill="{c1}"/><circle cx="{x-24*s}" cy="{y-20*s}" r="{24*s}" fill="{c1}"/><circle cx="{x+24*s}" cy="{y-22*s}" r="{24*s}" fill="{c1}"/>'
def cena_medulas_capa(w,h):
    sol=f'<circle cx="720" cy="300" r="170" fill="{GOLD}"/>'
    f1=picos(900,[SAND,IV],3,5,100,900,420,560,170,230)
    f2=picos(960,[TERRA],7,7,60,900,520,720,200,280)
    f3=picos(1010,['#8E3F26',TERRA],11,6,60,900,260,380,180,240)
    chao=f'<path d="M0 960C200 930 500 990 960 940V1180H0Z" fill="{G2}"/>'
    arv=''.join(castanheiro(x,y,s,G,TERRA) for x,y,s in [(130,1020,1.5),(300,1070,1.8),(520,1040,1.4),(760,1090,1.9),(880,1030,1.3),(40,1110,1.7)])
    return sol+f1+f2+f3+chao+arv
def cena_bierzo(w,h):
    # mapa estilizado: Ponferrada -> Las Médulas (20 km), León/Castela e Leão
    reg=f'<path d="M60 180L420 90L820 140L900 440L780 760L440 840L120 700L40 420Z" fill="{G2}" stroke="{GOLD}" stroke-width="6" stroke-linejoin="round"/>'
    estr=f'<path d="M330 560C400 520 450 470 520 400C570 350 610 330 680 300" fill="none" stroke="{IV}" stroke-width="8" stroke-dasharray="4 20" stroke-linecap="round"/>'
    pin=lambda x,y,c,t,tx: f'<circle cx="{x}" cy="{y}" r="26" fill="{c}"/><circle cx="{x}" cy="{y}" r="10" fill="{G}"/><text x="{x+tx}" y="{y-40}" text-anchor="middle" font-family="Lora" font-weight="700" font-size="48" fill="{IV}">{t}</text>'
    picos_m=picos(330,[TERRA,'#8E3F26'],2,4,640,760,60,110,90,130)
    return reg+estr+pin(330,560,GOLD,'Ponferrada',0)+picos_m+f'<circle cx="680" cy="330" r="22" fill="{TERRA}" stroke="{IV}" stroke-width="6"/><text x="660" y="190" text-anchor="middle" font-family="Lora" font-weight="700" font-size="48" fill="{IV}">Las Médulas</text>'+f'<path d="M660 205V300" stroke="{IV}" stroke-width="4" stroke-dasharray="2 8"/>'+f'<text x="500" y="720" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="6" fill="{GOLD}">BIERZO · LEÓN</text><text x="500" y="770" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" letter-spacing="4" fill="{IV}">CASTELA E LEÃO</text>'
def cena_agua(w,h):
    # dois rios -> canais -> encosta; 100 km
    mont=f'<path d="M500 760L620 330L680 270L760 330L900 760Z" fill="{TERRA}"/><path d="M680 270L720 520L760 330Z" fill="#8E3F26"/>'
    rio=lambda y,t: f'<path d="M20 {y}C140 {y-50} 260 {y+50} 380 {y}" fill="none" stroke="{IV}" stroke-width="18" stroke-linecap="round"/><text x="200" y="{y-70}" text-anchor="middle" font-family="Lora" font-weight="700" font-size="46" fill="{GOLD}">{t}</text>'
    canais=f'<path d="M380 220C470 220 520 300 640 300" fill="none" stroke="{GOLD}" stroke-width="12" stroke-dasharray="26 14" stroke-linecap="round"/><path d="M380 520C470 520 520 400 640 330" fill="none" stroke="{GOLD}" stroke-width="12" stroke-dasharray="26 14" stroke-linecap="round"/>'
    gota=lambda x,y: f'<path d="M{x} {y-34}C{x+30} {y+6} {x+26} {y+30} {x} {y+30}C{x-26} {y+30} {x-30} {y+6} {x} {y-34}Z" fill="{IV}"/>'
    return mont+rio(220,'Eria')+rio(520,'Cabreira')+canais+gota(470,300)+gota(540,420)+f'<rect x="40" y="800" width="860" height="110" rx="55" fill="{G}"/><text x="470" y="874" text-anchor="middle" font-family="Lora" font-weight="700" font-size="64" fill="{GOLD}">mais de 100 km</text>'
def cena_selo97(w,h):
    mos=f'<defs><clipPath id="cc"><circle cx="480" cy="330" r="270"/></clipPath></defs><g clip-path="url(#cc)"><rect x="210" y="60" width="540" height="540" fill="{G}"/>{picos(520,[TERRA,SAND,"#8E3F26"],5,8,230,740,180,330,130,200)}<circle cx="600" cy="200" r="60" fill="{GOLD}"/><path d="M210 520H750V600H210Z" fill="{G2}"/></g>'
    aro=f'<circle cx="480" cy="330" r="270" fill="none" stroke="{G}" stroke-width="14"/>'
    faixa=f'<rect x="150" y="610" width="660" height="150" rx="75" fill="{G}"/><text x="480" y="712" text-anchor="middle" font-family="Lora" font-weight="700" font-size="100" fill="{GOLD}">1997</text>'
    return mos+aro+faixa+f'<text x="480" y="820" text-anchor="middle" font-family="Inter" font-weight="800" font-size="30" letter-spacing="5" fill="{G}">PATRIMÔNIO MUNDIAL</text>'
def reel():
    S=[]
    S.append(rbv(f'''{Tv('<span style="color:@AC;font-style:italic">Las Médulas</span>, em León, são Patrimônio Mundial',86)}
    {cardv(60,600,960,1140,G,cena_medulas_capa(960,1140),-40)}''',1,'green'))
    S.append(rbv(f'''{Tv('Uma exploração mineira da <span style="color:@AC">Hispânia romana</span>',80)}
    {Pv('Exploração a céu aberto na comarca do Bierzo, província de León, em Castela e Leão, a cerca de 20 km de Ponferrada.',560)}
    {cardv(60,980,960,780,G,cena_bierzo(960,780),0)}''',2,'terra'))
    S.append(rbv(f'''{Tv('A água vinha <span style="color:@AC">de longe</span>',100)}
    {Pv('Um sistema de canais trazia água dos rios Eria e Cabreira, a mais de 100 km de distância.',540)}
    {cardv(60,830,960,910,G,cena_agua(960,910),0)}''',3,'ivory'))
    S.append(rbv(f'''{Tv('Patrimônio da Humanidade <span style="color:@AC">desde 1997</span>',84)}
    {Pv('É um dos 50 bens espanhóis na Lista do Patrimônio Mundial. A página oficial de turismo descreve a paisagem avermelhada.',560)}
    {cardv(60,960,960,780,SAND,cena_selo97(960,780),0)}''',4,'green'))
    S.append(closing(1920,G,IV,GOLD,'Fontes: Turespaña (spain.info), “Las Médulas”; Ministerio de Asuntos Exteriores, Patrimonio Mundial.<br>Consulta em 14/11/2026.',logo=460,serif_sz=88,top=.2))
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
