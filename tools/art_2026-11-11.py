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



import math, subprocess
def figura(cx,top,s,col):
    return f'<circle cx="{cx}" cy="{top+14*s}" r="{14*s}" fill="{col}"/><path d="M{cx-18*s} {top+78*s}V{top+46*s}C{cx-18*s} {top+34*s} {cx+18*s} {top+34*s} {cx+18*s} {top+46*s}V{top+78*s}Z" fill="{col}"/>'
# ================= 2026-11-11 : ícones e cenas novos =================
def ic_decree(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="16" width="120" height="150" rx="10" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M62 54H138M62 78H138M62 102H110" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="130" cy="146" r="30" fill="{a}"/><path d="M116 146L127 157L146 134" fill="none" stroke="{b}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_euro_beds(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="76" r="56" fill="{a}"/><text x="100" y="96" text-anchor="middle" font-family="Lora" font-weight="700" font-size="64" fill="{b}">€</text><path d="M20 176V146H180V176M20 160H180M34 146V126H88V146" fill="none" stroke="{a}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/></svg>'
def ic_boat(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 22V104M100 30L156 98H100" fill="{a}" stroke="{a}" stroke-width="4" stroke-linejoin="round"/><path d="M100 40L56 98H100Z" fill="{b}" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><path d="M26 112H174L150 154H50Z" fill="{a}"/><path d="M10 176C34 160 52 190 76 174C100 158 120 190 146 174C166 162 180 172 190 178" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'
def ic_kids(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200">{figura(52,60,1.3,a)}{figura(100,84,1.0,a)}<path d="M120 150H182M166 132L184 150L166 168" fill="none" stroke="{a}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M20 176H110" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'
def ic_island(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M16 150C40 90 70 70 100 74C132 70 160 96 186 150Z" fill="{a}"/><path d="M10 164C36 150 54 178 80 164C106 150 124 178 150 164C168 154 182 162 192 168" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="150" cy="40" r="22" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M100 74V40M100 44C112 36 124 38 130 46M100 44C88 36 76 38 70 46" fill="none" stroke="{b}" stroke-width="6" stroke-linecap="round"/></svg>'
def ic_building(a,b):
    wins=''.join(f'<rect x="{x}" y="{y}" width="16" height="16" rx="2" fill="{b}"/>' for x in (58,92,126) for y in (50,84,118))
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="26" width="120" height="150" rx="6" fill="{a}"/>{wins}<rect x="86" y="146" width="28" height="30" fill="{b}"/><path d="M20 176H180" stroke="{a}" stroke-width="7" stroke-linecap="round"/></svg>'
def ic_catalog(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="30" y="20" width="110" height="148" rx="10" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M52 56H118M52 82H118M52 108H96" stroke="{a}" stroke-width="7" stroke-linecap="round"/><circle cx="132" cy="124" r="32" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M156 148L184 178" stroke="{a}" stroke-width="12" stroke-linecap="round"/></svg>'
def ic_shield(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 16L172 42V100C172 144 140 172 100 188C60 172 28 144 28 100V42Z" fill="{a}"/><path d="M68 100L92 126L134 76" fill="none" stroke="{b}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def ic_contract(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="34" y="14" width="116" height="156" rx="10" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M56 48H128M56 72H128M56 96H100" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M56 140C70 118 80 156 96 134S112 130 124 138" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round"/><path d="M150 100L186 64L198 76L162 112L146 116Z" fill="{a}"/></svg>'
def ic_clock3(a,b):
    return f'<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="80" fill="{b}" stroke="{a}" stroke-width="9"/><path d="M100 50V100L136 120" fill="none" stroke="{a}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ---------- NOTÍCIA ----------
def boia_cover():
    stripes=''.join(f'<path d="M{540+r1*math.cos(a):.1f} {820+r1*math.sin(a):.1f}A{r1} {r1} 0 0 1 {540+r1*math.cos(a+0.7):.1f} {820+r1*math.sin(a+0.7):.1f}L{540+r2*math.cos(a+0.7):.1f} {820+r2*math.sin(a+0.7):.1f}A{r2} {r2} 0 0 0 {540+r2*math.cos(a):.1f} {820+r2*math.sin(a):.1f}Z" fill="{G}"/>' for a in [k*math.pi/2+0.4 for k in range(4)] for r1,r2 in [(230,120)])
    waves=''.join(f'<path d="M0 {y}C90 {y-30} 180 {y+30} 270 {y}S450 {y-30} 540 {y}S720 {y+30} 810 {y}S990 {y-30} 1080 {y}" fill="none" stroke="{GOLD}" stroke-width="4" opacity="{op}"/>' for y,op in [(1080,.9),(1112,.6),(1144,.35)])
    return page(1350,TERRA,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 50% 62%,#C96A49 0,{TERRA} 70%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Notícia · Canárias</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:880px;font-size:84px;line-height:1.05;font-weight:700;color:{IV}">Governo declara <span style="color:#F3D79A;font-style:italic">Emergência Migratória</span> em Canarias</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350"><circle cx="540" cy="820" r="230" fill="{IV}"/>{stripes}<circle cx="540" cy="820" r="120" fill="{TERRA}"/><circle cx="540" cy="820" r="230" fill="none" stroke="{G}" stroke-width="8"/><circle cx="540" cy="820" r="120" fill="none" stroke="{G}" stroke-width="8"/>{waves}
    <text x="540" y="1240" text-anchor="middle" font-family="Inter" font-weight="700" font-size="1" fill="{TERRA}"> </text></svg>
    <div class=abs style="left:80px;top:1170px;font-size:30px;font-weight:600;letter-spacing:.14em;color:#F3D79A;display:none">DESLIZE  →</div>
    {foot(IV)}''')
T=7
NOT=[boia_cover()]
NOT.append(content(2,T,'Notícia · O acordo','A Emergência Migratória','Em 10 de novembro, a Comissão Interministerial de Imigração, presidida por <b>Ángel Víctor Torres</b>, acordou declarar a Emergência Migratória em Canarias e ampliar os recursos.',ic_decree,'ivory'))
NOT.append(content(3,T,'Notícia · Vagas e traslados','15,18 milhões de euros','Valor <b>adicional</b> para habilitar mais vagas em centros estatais e para traslados entre ilhas e para a Península, segundo a nota da Moncloa.',ic_euro_beds,'green'))
NOT.append(content(4,T,'Notícia · Resgate e saúde','Cruz Roja e Salvamento','Mais <b>1 milhão de euros</b> para a Cruz Roja. A guardamar Calíope se incorpora, e Canarias terá três das cinco guardamares operativas do país.',ic_boat,'terra'))
NOT.append(content(5,T,'Notícia · Menores','Menores não acompanhados','Haverá reforço na Delegación del Gobierno en Canarias para tramitar expedientes de <b>reubicação</b> de menores migrantes não acompanhados.',ic_kids,'ivory'))
NOT.append(content(6,T,'Notícia · El Hierro','Apoio a El Hierro','Hacienda estudará medidas para os gastos extraordinários da ilha. Exteriores e Interior destacam a cooperação com os países de origem.',ic_island,'green'))
NOT.append(closing(1350,G,IV,GOLD,'Fonte: La Moncloa, nota de imprensa de 10/11/2026 (Política Territorial e Memória Democrática).<br>Consulta em 11/11/2026.'))

# ---------- IMIGRAÇÃO ----------
def contrato_cover():
    lines=''.join(f'<path d="M290 {y}H690" stroke="{G2}" stroke-width="8" stroke-linecap="round"/>' for y in (640,690,740,790))
    return page(1350,G,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 70% 70%,{G2} 0,{G} 70%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Trabalho</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:880px;font-size:80px;line-height:1.06;font-weight:700;color:{IV}">Como funciona a autorização de residência e trabalho <span style="color:{GOLD};font-style:italic">por conta alheia</span>?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350"><g transform="rotate(-6 480 860)"><rect x="230" y="560" width="520" height="620" rx="18" fill="{IV}"/><rect x="230" y="560" width="520" height="90" rx="18" fill="{SAND}"/>
    <text x="490" y="620" text-anchor="middle" font-family="Lora" font-weight="700" font-size="40" fill="{G}">CONTRATO</text>{lines.replace('640','700').replace('690','750').replace('740','800').replace('790','850')}
    <path d="M290 1060C340 990 380 1120 440 1040S540 1030 600 1060" fill="none" stroke="{TERRA}" stroke-width="7" stroke-linecap="round"/><path d="M290 1100H640" stroke="{G2}" stroke-width="3"/></g>
    <circle cx="790" cy="1040" r="92" fill="{GOLD}"/><circle cx="790" cy="1040" r="74" fill="none" stroke="{G}" stroke-width="4" stroke-dasharray="3 9"/><path d="M752 1042L782 1074L836 1006" fill="none" stroke="{G}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>
    <g transform="rotate(30 880 640)"><rect x="850" y="470" width="34" height="260" rx="8" fill="{TERRA}"/><path d="M850 730L867 790L884 730Z" fill="{SAND}"/></g>
    <rect x="780" y="860" width="170" height="124" rx="16" fill="{TERRA}"/><path d="M820 860V838C820 822 910 822 910 838V860" fill="none" stroke="{TERRA}" stroke-width="12"/><rect x="770" y="904" width="190" height="14" fill="{GOLD}"/></svg>
    {foot(GOLD)}''')
IMG=[contrato_cover()]
IMG.append(content(2,T,'Imigração · Quem pede','Quem pede e para quê','Quem pede é o <b>empregador</b>, pela via eletrônica (Mercurio), para contratar estrangeiro maior de 16 anos. A autorização é de residência e trabalho por mais de 90 dias e menos de 5 anos.',ic_building,'ivory'))
IMG.append(content(3,T,'Imigração · Situação nacional de emprego','Situação nacional de emprego','A contratação é possível se a ocupação está no <b>Catálogo de Ocupações de Difícil Cobertura</b> ou se o empregador comprova que não consegue preencher a vaga, com oferta no portal Empléate.',ic_catalog,'green'))
IMG.append(content(4,T,'Imigração · Trabalhador','Requisitos do trabalhador','Não estar em situação irregular na Espanha, não ter antecedentes criminais na Espanha nem onde viveu nos últimos cinco anos e ter a <b>formação</b> e a habilitação profissional exigidas.',ic_shield,'terra'))
IMG.append(content(5,T,'Imigração · Empregador','Requisitos do empregador','Contrato assinado que garanta atividade contínua, inscrição na Seguridade Social, obrigações tributárias em dia e <b>meios econômicos</b> suficientes para o contrato.',ic_contract,'ivory'))
IMG.append(content(6,T,'Imigração · Prazos','Prazos da ficha oficial','A ficha oficial prevê resolução em <b>três meses</b>. Depois, o trabalhador tem um mês para pedir o visto no consulado, que prevê decidir em um mês.',ic_clock3,'green'))
IMG.append(closing(1350,TERRA,IV,'#F3D79A','Fonte: Ministerio de Inclusión, Hoja 12 (atualizada em maio de 2025).<br>Consulta em 11/11/2026.'))

# ---------- CULTURA (Reel 1080x1920) ----------
def rbv(inner,n,theme='green'):
    if theme=='ivory': bg,fg,acc,k=IV,G,TERRA,TERRA
    elif theme=='terra': bg,fg,acc,k=TERRA,IV,'#F3D79A','#F3D79A'
    else: bg,fg,acc,k=G,IV,GOLD,GOLD
    return page(1920,bg,f'''{bracket(acc)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{k}">Você sabia? | Espanha</span></div>
    {inner.replace('@FG',fg).replace('@AC',acc)}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{acc}">Espanha Sem Segredo</span></div><span class=c style="color:{acc}">{n} / 5</span></div>''')
def Tv(t,sz=88): return f'<div class="abs serif" style="left:80px;top:220px;width:920px;font-size:{sz}px;line-height:1.06;font-weight:700;color:@FG">{t}</div>'
def Pv(t,top=520): return f'<div class=abs style="left:80px;top:{top}px;width:920px;font-size:44px;line-height:1.4;color:@FG;opacity:.95">{t}</div>'
def cardv(x,y,w,h,bg,svg): return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;background:{bg}"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg></div>'
def farol(cx,base,h,w,col1,col2):
    # torre em tres corpos, ultimo de restauracao
    return (f'<rect x="{cx-w/2}" y="{base-h*0.62}" width="{w}" height="{h*0.62}" fill="{col1}"/>'
            f'<rect x="{cx-w*0.40}" y="{base-h*0.86}" width="{w*0.8}" height="{h*0.24}" fill="{col1}"/>'
            f'<rect x="{cx-w*0.30}" y="{base-h}" width="{w*0.6}" height="{h*0.14}" fill="{col2}"/>'
            f'<rect x="{cx-w*0.38}" y="{base-h-14}" width="{w*0.76}" height="16" fill="{col2}"/>'
            f'<path d="M{cx-w*0.22} {base-h-14}V{base-h-60}H{cx+w*0.22}V{base-h-14}" fill="{GOLD}"/><path d="M{cx-w*0.3} {base-h-60}L{cx} {base-h-100}L{cx+w*0.3} {base-h-60}Z" fill="{col2}"/>')
def cena_noite(w,h):
    stars=''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{IV}"/>' for x,y,r in [(90,80,4),(210,140,3),(420,60,4),(660,110,3),(850,70,4),(900,200,3),(120,260,3)])
    beam=f'<path d="M{w/2+40} 250L{w} 120V330Z" fill="{GOLD}" opacity=".35"/><path d="M{w/2-40} 250L0 120V330Z" fill="{GOLD}" opacity=".35"/>'
    sea=''.join(f'<path d="M0 {y}C120 {y-26} 240 {y+26} 360 {y}S600 {y-26} 720 {y}S{w-40} {y+26} {w} {y}V{h}H0Z" fill="{c}"/>' for y,c in [(h-210,G2),(h-140,G),(h-70,'#0B2E2C')])
    rock=f'<path d="M{w/2-220} {h-200}C{w/2-190} {h-300} {w/2+190} {h-300} {w/2+220} {h-200}Z" fill="{SAND}" opacity=".95"/>'
    return f'<circle cx="780" cy="120" r="54" fill="{SAND}"/>'+stars+beam+rock+farol(w/2,h-250,420,110,IV,SAND)+sea
def cena_arco(w,h):
    # arco romano e colunas sobre o mar
    cols=''.join(f'<rect x="{x}" y="260" width="64" height="360" fill="{IV}"/><rect x="{x-14}" y="240" width="92" height="30" fill="{SAND}"/><rect x="{x-14}" y="610" width="92" height="30" fill="{SAND}"/>' for x in (200,696))
    arc=f'<path d="M232 270C232 90 728 90 728 270" fill="none" stroke="{IV}" stroke-width="56"/><path d="M232 270C232 130 728 130 728 270" fill="none" stroke="{GOLD}" stroke-width="6"/>'
    txt=f'<text x="480" y="440" text-anchor="middle" font-family="Lora" font-weight="700" font-size="92" fill="{GOLD}">I d.C.</text><text x="480" y="500" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" letter-spacing="3" fill="{IV}">FARUM BRIGANTIUM</text>'
    sea=f'<path d="M0 680C120 654 240 706 360 680S600 654 720 680S900 706 960 680V{h}H0Z" fill="{G2}"/><path d="M0 730C120 704 240 756 360 730S600 704 720 730S900 756 960 730V{h}H0Z" fill="{G}"/>'
    return cols+arc+txt+sea
def cena_medida(w,h):
    base=h-80; H=600; x=170
    t1=H*0.62
    return (f'<rect x="{x}" y="{base-H}" width="220" height="{H*0.5:.0f}" fill="{TERRA}"/>'
            f'<rect x="{x}" y="{base-H*0.5:.0f}" width="220" height="{H*0.5:.0f}" fill="{GOLD}"/>'
            f'<rect x="{x-40}" y="{base}" width="300" height="40" fill="{SAND}"/>'
            f'<path d="M{x+280} {base-H}H{x+330}V{base}H{x+280}" fill="none" stroke="{IV}" stroke-width="5"/>'
            f'<text x="{x+350}" y="{base-H*0.74:.0f}" font-family="Lora" font-weight="700" font-size="76" fill="{TERRA}">21 m</text><text x="{x+350}" y="{base-H*0.74+40:.0f}" font-family="Inter" font-weight="700" font-size="26" letter-spacing="3" fill="{IV}">SÉC. XVIII</text>'
            f'<text x="{x+350}" y="{base-H*0.25:.0f}" font-family="Lora" font-weight="700" font-size="76" fill="{GOLD}">34 m</text><text x="{x+350}" y="{base-H*0.25+40:.0f}" font-family="Inter" font-weight="700" font-size="26" letter-spacing="2" fill="{IV}">ALVENARIA ROMANA</text>'
            f'<rect x="60" y="{base}" width="160" height="40" fill="{G}"/><text x="140" y="{base+30}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="22" fill="{IV}">ROCHA 57 m</text>')
def cena_selo2(w,h):
    return (f'<defs><path id="cs2" d="M480 330m-250 0a250 250 0 1 1 500 0a250 250 0 1 1 -500 0"/></defs>'
      f'<circle cx="480" cy="330" r="290" fill="none" stroke="{TERRA}" stroke-width="8"/><circle cx="480" cy="330" r="270" fill="none" stroke="{TERRA}" stroke-width="3"/><circle cx="480" cy="330" r="190" fill="{G}"/>'
      f'<text font-family="Inter" font-weight="800" font-size="32" fill="{TERRA}"><textPath href="#cs2" textLength="1540" lengthAdjust="spacing">PATRIMÔNIO MUNDIAL · UNESCO · PATRIMÔNIO MUNDIAL · UNESCO ·</textPath></text>'
      f'<text x="480" y="352" text-anchor="middle" font-family="Lora" font-weight="700" font-size="120" fill="{GOLD}">2009</text><text x="480" y="410" text-anchor="middle" font-family="Inter" font-weight="800" font-size="28" letter-spacing="6" fill="{IV}">A CORUÑA</text>'
      +f'<text x="480" y="715" text-anchor="middle" font-family="Lora" font-weight="700" font-size="56" fill="{G}">Torre de Hércules</text>')
def reel():
    S=[]
    S.append(rbv(f'''{Tv('O farol romano que <span style="color:@AC;font-style:italic">ainda guia navios</span>, em A Coruña')}
    {cardv(60,780,960,860,G2,cena_noite(960,860))}''',1,'green'))
    S.append(rbv(f'''{Tv('Construído no <span style="color:@AC">século I</span>',92)}
    {Pv('Segundo a UNESCO, os romanos o construíram como Farum Brigantium, no fim do século I d.C., na entrada do porto de A Coruña.',480)}
    {cardv(60,900,960,760,G2,cena_arco(960,760))}''',2,'ivory').replace(f'background:{G2}',f'background:{G}'))
    S.append(rbv(f'''{Tv('55 metros sobre uma <span style="color:@AC">rocha de 57</span>',84)}
    {Pv('34 metros são de alvenaria romana e 21 vêm da restauração do século XVIII, dirigida pelo arquiteto Eustaquio Giannini.',500)}
    {cardv(60,900,960,760,G,cena_medida(960,760))}''',3,'green'))
    S.append(rbv(f'''{Tv('Patrimônio Mundial desde <span style="color:@AC">2009</span>',88)}
    {Pv('Para a UNESCO, é o único farol romano totalmente preservado que ainda é usado para sinalização marítima.',500)}
    {cardv(60,900,960,760,SAND,cena_selo2(960,760))}''',4,'terra'))
    S.append(closing(1920,G2,IV,GOLD,'Fontes: UNESCO (Tower of Hercules, ficha 1312; notícia de 27/06/2009) e Turismo de Galicia.<br>Consulta em 11/11/2026.',logo=460,serif_sz=88,top=.2))
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
