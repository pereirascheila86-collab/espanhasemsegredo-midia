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

# ================= 2026-11-16 : ícones e cenas novos =================
def T(x,y,t,sz=40,col=IV,w=700,fam='Inter',anchor='middle',ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-weight="{w}" font-size="{sz}" letter-spacing="{ls}" fill="{col}">{t}</text>'
def SV(inner): return f'<svg width="100%" height="100%" viewBox="0 0 200 200">{inner}</svg>'



# ================= 2026-11-18 =================
# ---------- NOTICIA: 5 milhoes para El Hierro ----------
def ic_cruz_saude(a,b):
    return SV(f'<rect x="24" y="52" width="152" height="118" rx="14" fill="{a}"/><path d="M70 52V38C70 30 76 26 84 26H116C124 26 130 30 130 38V52" fill="none" stroke="{a}" stroke-width="9"/><path d="M100 78V144M68 111H132" stroke="{b}" stroke-width="20" stroke-linecap="round"/>')
def ic_cabildo(a,b):
    cols=''.join(f'<rect x="{40+i*30}" y="86" width="16" height="72" fill="{a}"/>' for i in range(5))
    return SV(f'<path d="M16 84L100 24L184 84Z" fill="{a}"/><circle cx="100" cy="62" r="9" fill="{b}"/>{cols}<rect x="22" y="160" width="156" height="16" rx="3" fill="{a}"/><path d="M100 24V8" stroke="{a}" stroke-width="6"/><path d="M100 8H128V22H100Z" fill="{b}" stroke="{a}" stroke-width="4"/>')
def ic_decreto(a,b):
    return SV(f'<path d="M40 24H160C170 24 170 40 160 40V160C160 174 148 178 138 176H56C46 176 40 168 40 158Z" fill="{b}" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><path d="M62 62H138M62 86H138M62 110H108" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="130" cy="144" r="22" fill="{a}"/><path d="M120 144L128 152L142 134" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_hemiciclo(a,b):
    s=''
    for r,n in ((38,5),(62,8),(86,11)):
        for i in range(n):
            ang=math.pi-math.pi*i/(n-1)
            s+=f'<circle cx="{100+r*math.cos(ang):.1f}" cy="{150-r*math.sin(ang):.1f}" r="8" fill="{a if r!=62 else b}" stroke="{a}" stroke-width="3"/>'
    return SV(s+f'<path d="M24 170H176" stroke="{a}" stroke-width="9" stroke-linecap="round"/>')
def ic_moedas(a,b):
    return SV(f'<ellipse cx="100" cy="150" rx="66" ry="20" fill="{a}"/><ellipse cx="100" cy="124" rx="66" ry="20" fill="{b}" stroke="{a}" stroke-width="7"/><ellipse cx="100" cy="98" rx="66" ry="20" fill="{a}"/><ellipse cx="100" cy="72" rx="66" ry="20" fill="{b}" stroke="{a}" stroke-width="7"/>{T(100,84,"€",34,a,800,"Lora")}')

def cover_hierro():
    ondas=''.join(f'<path d="M0 {y}C120 {y-26} 240 {y+26} 360 {y}S600 {y-26} 720 {y}S960 {y+26} 1080 {y}V1350H0Z" fill="{c}" opacity="{o}"/>' for y,c,o in ((860,G2,.8),(930,G2,.9),(1010,'#0B2F2D',1)))
    return page(1350,G,f'''{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:880px;font-size:78px;line-height:1.05;font-weight:700;color:{IV}">Governo aprova <span style="color:{GOLD};font-style:italic">5 milhões</span> de euros para El Hierro</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="830" cy="640" r="70" fill="{GOLD}" opacity=".9"/>
      {ondas}
      <path d="M270 880C300 800 330 760 400 748C440 700 520 690 580 720C640 722 700 760 740 820C760 850 770 870 780 890C640 906 420 906 270 880Z" fill="{TERRA}"/>
      <path d="M330 820C400 790 480 800 560 786" stroke="{IV}" stroke-width="5" fill="none" opacity=".4"/>
      <g transform="translate(150 960)"><path d="M0 0H130L110 34H20Z" fill="{IV}"/><path d="M65 0V-70L112 0" fill="{GOLD}"/><path d="M65 -70V0" stroke="{IV}" stroke-width="4"/></g>
      {T(830,660,"5 M€",46,G,800,"Lora")}
      {T(540,1120,"El Hierro, Canárias",32,IV,700,"Lora",ls=3)}
    </svg>
    {foot(IV)}''')
NOT=[cover_hierro()]
NOT.append(content2('Notícia · O que foi aprovado','Real decreto-ley urgente','Segundo a imprensa, o Consejo de Ministros de <b>17/11/2026</b> aprovou duas subvenções diretas extraordinárias, num total de <b>5 milhões de euros</b>, por causa das chegadas de migrantes a El Hierro.',ic_decreto,'ivory',44))
NOT.append(content2('Notícia · Saúde','3 milhões para as Canárias','Destinados aos <b>gastos sanitários extraordinários</b> do Serviço Canario de la Salud: pessoal, urgências, transferências e material.',ic_cruz_saude,'terra',50))
NOT.append(content2('Notícia · El Hierro','2 milhões para o Cabildo','Subvenção ao <b>Cabildo Insular de El Hierro</b> para gastos sociais e econômicos extraordinários da ilha.',ic_cabildo,'green',50))
NOT.append(content2('Notícia · Contexto','Soma-se à emergência migratória','A verba vem depois da <b>Emergência Migratória</b> declarada na semana anterior, com 15,18 milhões, segundo a EFE.',ic_moedas,'ivory',48))
NOT.append(content2('Notícia · Próximo passo','Convalidação no Congresso','Como todo real decreto-ley, precisa ser <b>convalidado pelo Congresso</b> em até 30 dias. O texto oficial ainda deve ser conferido no BOE.',ic_hemiciclo,'green',46))
NOT.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: Demócrata (18/11/2026); Infobae/EFE (17/11/2026); Moncloa.com (17/11/2026).<br>Consulta em 18/11/2026.'))

# ---------- IMIGRACAO: setor audiovisual ----------
def ic_claquete(a,b):
    return SV(f'<rect x="22" y="76" width="156" height="104" rx="8" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M22 76L14 40L170 22L178 58Z" fill="{a}"/><path d="M52 34L68 62M88 28L104 56M124 24L140 52" stroke="{b}" stroke-width="9"/><path d="M22 110H178" stroke="{a}" stroke-width="6"/><path d="M60 140H140" stroke="{a}" stroke-width="7" stroke-linecap="round"/>')
def ic_camera(a,b):
    return SV(f'<rect x="20" y="62" width="112" height="86" rx="12" fill="{a}"/><path d="M132 90L184 60V150L132 120Z" fill="{a}"/><circle cx="76" cy="105" r="26" fill="{b}"/><circle cx="76" cy="105" r="11" fill="{a}"/><circle cx="38" cy="40" r="20" fill="{a}"/><circle cx="92" cy="36" r="20" fill="{a}"/>')
def ic_visto_sel(a,b):
    return SV(f'<rect x="26" y="26" width="148" height="148" rx="14" fill="{b}" stroke="{a}" stroke-width="8"/><circle cx="100" cy="92" r="38" fill="none" stroke="{a}" stroke-width="7"/><path d="M62 92H138M100 54C84 72 84 112 100 130M100 54C116 72 116 112 100 130" fill="none" stroke="{a}" stroke-width="5"/><path d="M52 150H148" stroke="{a}" stroke-width="7" stroke-linecap="round"/>')
def ic_empresa_ok(a,b):
    return SV(f'<rect x="24" y="52" width="100" height="126" rx="6" fill="{a}"/><rect x="42" y="72" width="22" height="20" fill="{b}"/><rect x="84" y="72" width="22" height="20" fill="{b}"/><rect x="42" y="108" width="22" height="20" fill="{b}"/><rect x="84" y="108" width="22" height="20" fill="{b}"/><rect x="62" y="146" width="24" height="32" fill="{b}"/><circle cx="144" cy="66" r="38" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M126 66L140 80L164 52" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_familia(a,b):
    return SV(f'<circle cx="64" cy="48" r="18" fill="{a}"/><path d="M30 120C30 82 44 72 64 72C84 72 98 82 98 120Z" fill="{a}"/><circle cx="136" cy="48" r="18" fill="{a}"/><path d="M102 120C102 82 116 72 136 72C156 72 170 82 170 120Z" fill="{a}"/><circle cx="100" cy="112" r="13" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M76 164C76 140 86 132 100 132C114 132 124 140 124 164Z" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M22 176H178" stroke="{a}" stroke-width="7" stroke-linecap="round"/>')

def cover_audio():
    holes=''.join(f'<rect x="{x}" y="{y}" width="26" height="20" rx="4" fill="{IV}" opacity=".25"/>' for y in (806,1056) for x in range(70,1030,70))
    frames=''.join(f'<rect x="{70+i*190}" y="836" width="170" height="210" rx="6" fill="{c}"/>' for i,c in enumerate((G2,GOLD,TERRA,G2,GOLD)))
    return page(1350,IV,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{IV} 0,{SAND} 100%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:68px;line-height:1.06;font-weight:700;color:{G}">Profissional do <span style="color:{TERRA};font-style:italic">audiovisual</span> estrangeiro: como funciona a entrada e a permanência?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <rect x="0" y="790" width="1080" height="290" fill="{INK}"/>{holes}{frames}
      <g transform="translate(110 500) rotate(-6)"><rect x="0" y="70" width="320" height="200" rx="10" fill="{G}"/><path d="M0 70L-14 20L300 -10L320 50Z" fill="{TERRA}"/><path d="M50 8L76 62M118 2L144 56M186 -4L212 50M254 -10L280 44" stroke="{IV}" stroke-width="16"/><path d="M0 130H320" stroke="{GOLD}" stroke-width="5"/>{T(160,208,"CENA 1 · TOMADA 1",24,IV,700,"Inter",ls=4)}</g>
      <g transform="translate(600 480)"><circle cx="90" cy="60" r="56" fill="{G}"/><circle cx="270" cy="60" r="56" fill="{G}"/><rect x="40" y="86" width="290" height="190" rx="18" fill="{G2}"/><circle cx="170" cy="182" r="62" fill="{INK}"/><circle cx="170" cy="182" r="38" fill="{G}"/><circle cx="170" cy="182" r="14" fill="{GOLD}"/><rect x="290" y="130" width="24" height="24" rx="12" fill="{TERRA}"/></g>
      {T(540,1180,"Estância, visto ou residência: depende do tempo",32,G,800,"Lora")}
    </svg>
    {foot(G)}''')
IMG=[cover_audio()]
IMG.append(content2('Imigração · Quem é','Setor audiovisual','Artistas, técnicos e profissionais estrangeiros em <b>atuações ao vivo</b> ou gravações para difusão em meios de massa. O guia oficial prevê regras também para familiares.',ic_camera,'green',46))
IMG.append(content2('Imigração · Até 90 dias','Estância curta','Estância de até <b>90 dias em 180</b>: não exige autorização de residência e trabalho. Pode exigir visto, conforme o país. NIE e Seguridad Social, quando não coberta por convênio.',ic_claquete,'ivory',44))
IMG.append(content2('Imigração · 90 a 180 dias','Visto de estância audiovisual','Título suficiente para permanecer e trabalhar nesse período, com entradas e saídas múltiplas. Pedido no <b>consulado</b>; o guia prevê decisão em até 10 dias úteis.',ic_visto_sel,'terra',44))
IMG.append(content2('Imigração · Mais de 180 dias','Autorização de residência','Pedida pela <b>empresa espanhola</b>, por via eletrônica, na sede eletrônica do Ministério. Se o profissional estiver fora da Espanha, pede depois o visto no consulado.',ic_empresa_ok,'ivory',44))
IMG.append(content2('Imigração · Atenção','Prorrogação e familiares','Prorrogação excepcional da estância: pedido à UGE, <b>30 dias antes</b>. Familiares só trabalham se tiverem autorização de residência própria.',ic_familia,'green',46))
IMG.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: Spain Audiovisual Hub (Gobierno de España), guia de 27/11/2023; Orden PCM/1238/2021 (modelo MI-T, Ministerio de Inclusión).<br>Consulta em 18/11/2026.'))

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
