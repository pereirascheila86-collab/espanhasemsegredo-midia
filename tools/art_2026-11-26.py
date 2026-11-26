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

import math

def svg(vb,inner,w,h,style=''):
    return f'<svg class=abs style="{style}" width="{w}" height="{h}" viewBox="{vb}">{inner}</svg>'
def at(x,y,h,w=920,extra=''):
    return f'<div class=abs style="left:{x}px;top:{y}px;width:{w}px;{extra}">{h}</div>'
def kick(t,c): return at(80,96,f'<span class=kick style="color:{c}">{t}</span>')

def closing(h,bg,fg,acc,srcs,logo=360,serif_sz=70,top=.12):
    y=int(h*top)
    inner=f"""{bracket(acc)}
    <div class=abs style="left:0;right:0;top:{y}px;display:flex;justify-content:center"><img src="{LOGO}" width="{logo}" height="{logo}"></div>
    <div class=abs style="left:80px;right:80px;top:{y+logo+60}px;text-align:center">
      <div class=serif style="font-size:{serif_sz}px;line-height:1.14;font-weight:700;color:{fg}">Aqui você fica por dentro de tudo sobre a Espanha</div>
      <div style="width:130px;height:5px;background:{acc};margin:44px auto 40px"></div>
      <div class=serif style="font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
      <div style="font-size:40px;color:{fg};margin-top:26px">Siga <b>@espanhasemsegredo</b></div></div>
    <div class=abs style="left:90px;right:90px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg}">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>"""
    return page(h,bg,inner)

# ============ NOTÍCIA: licenças ============
def calpage(x,y,s=1.0):
    g=f'<rect x="10" y="50" width="340" height="350" rx="28" fill="{IV}" stroke="{G}" stroke-width="10"/><path d="M10 150V78Q10 50 38 50H322Q350 50 350 78V150Z" fill="{TERRA}" stroke="{G}" stroke-width="10"/>'
    g+=''.join(f'<rect x="{px}" y="14" width="24" height="76" rx="12" fill="{GOLD}" stroke="{G}" stroke-width="6"/>' for px in (80,256))
    g+=f'<text x="180" y="128" text-anchor="middle" font-family="Inter" font-weight="800" font-size="46" letter-spacing="8" fill="{IV}">NOV</text><text x="180" y="338" text-anchor="middle" font-family="Lora" font-weight="700" font-size="180" fill="{G}">26</text>'
    return svg('0 0 360 410',g,int(360*s),int(410*s),f'left:{x}px;top:{y}px')
def mobile(x,y):
    g=f'<path d="M260 0V70" stroke="{G}" stroke-width="6"/><path d="M40 130Q260 20 480 130" fill="none" stroke="{G}" stroke-width="10" stroke-linecap="round"/>'
    for px,py,l in [(40,130,120),(150,90,230),(260,74,130),(370,90,250),(480,130,110)]:
        g+=f'<path d="M{px} {py}V{py+l}" stroke="{G}" stroke-width="4"/>'
    def star(cx,cy,c): return f'<path d="M{cx} {cy-38}L{cx+11} {cy-11}L{cx+40} {cy-10}L{cx+17} {cy+9}L{cx+25} {cy+38}L{cx} {cy+21}L{cx-25} {cy+38}L{cx-17} {cy+9}L{cx-40} {cy-10}L{cx-11} {cy-11}Z" fill="{c}"/>'
    g+=star(40,286,GOLD)+star(480,276,TERRA)
    g+=f'<path d="M165 330a42 42 0 1 0 30 74a52 52 0 0 1-30-74Z" fill="{G2}"/>'
    g+=f'<circle cx="260" cy="238" r="38" fill="{TERRA}"/>'
    g+=f'<path d="M370 380C320 345 316 316 336 303C351 294 365 301 370 314C375 301 389 294 404 303C424 316 420 345 370 380Z" fill="{GOLD}"/>'
    return svg('0 0 530 430',g,530,430,f'left:{x}px;top:{y}px')
def n_cover():
    inner=f"""{at(0,820,'',1080,f'height:530px;background:{SAND}')}{bracket(GOLD)}{kick('Notícia · Espanha',TERRA)}
    {at(80,170,f'<div class=serif style="font-size:104px;line-height:1.05;font-weight:700;color:{G}">Licenças por <span style="color:{TERRA};font-style:italic">nascimento</span> e <span style="color:{TERRA};font-style:italic">luto</span> mudam na Espanha</div>')}
    {mobile(500,645)}{calpage(80,690,.98)}
    {at(80,1128,f'<div style="display:inline-block;background:{G};color:{IV};font-size:32px;font-weight:700;letter-spacing:.1em;padding:16px 30px;border-radius:10px">EM VIGOR EM 26/11/2026 · DESLIZE →</div>')}
    {foot(G)}"""
    return page(1350,IV,inner)

# icons
def ico(g,x,y,s): return svg('0 0 200 200',g,s,s,f'left:{x}px;top:{y}px')
def i_cradle(a,b): return f'<path d="M30 92H170C170 140 140 156 100 156S30 140 30 92Z" fill="{a}"/><path d="M100 92C100 46 130 32 170 40V92Z" fill="{b}" stroke="{a}" stroke-width="7" stroke-linejoin="round"/><path d="M20 168Q100 200 180 168" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round"/><circle cx="70" cy="78" r="20" fill="{b}" stroke="{a}" stroke-width="6"/>'
def i_hourcal(a,b): return f'<rect x="26" y="36" width="148" height="140" rx="16" fill="none" stroke="{a}" stroke-width="11"/><path d="M26 76H174M62 20V52M138 20V52" stroke="{a}" stroke-width="11" stroke-linecap="round"/><circle cx="100" cy="126" r="32" fill="{b}"/><path d="M100 108V126L114 136" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round"/>'
def i_ribbon(a,b): return f'<path d="M100 20C66 20 62 52 80 80L140 180L166 160L112 78C130 50 134 20 100 20ZM100 40C112 40 108 52 100 62C92 52 88 40 100 40Z" fill="{a}" fill-rule="evenodd"/><path d="M88 94L34 160L60 180L108 120Z" fill="{b}"/>'
def i_family(a,b): return f'<circle cx="62" cy="54" r="24" fill="{a}"/><circle cx="144" cy="62" r="20" fill="{b}"/><path d="M22 174V130C22 78 102 78 102 130V174Z" fill="{a}"/><path d="M110 174V130C110 88 178 88 178 130V174Z" fill="{b}"/><circle cx="106" cy="126" r="14" fill="{a}" stroke="{b}" stroke-width="5"/><path d="M86 174C86 138 126 138 126 174Z" fill="{a}" stroke="{b}" stroke-width="5"/>'
def i_hands(a,b): return f'<path d="M100 112C58 84 50 54 68 40C82 30 96 38 100 52C104 38 118 30 132 40C150 54 142 84 100 112Z" fill="{b}"/><path d="M18 112C30 108 40 116 52 130L84 138C100 142 96 160 80 156L58 150M18 164C46 166 60 186 100 180L180 138C190 126 178 114 162 120L116 142" fill="none" stroke="{a}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>'

def nslide(bg,fg,tc,acc,kc,k,hero,unit,title,body,icon,ic_a,ic_b):
    inner=f"""{bracket(acc)}{kick(k,kc)}
    {at(80,170,f'<div class=serif style="font-size:340px;line-height:1;font-weight:700;color:{acc};letter-spacing:-.04em">{hero}</div><div style="font-size:40px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:{fg}">{unit}</div>',640)}
    {ico(icon(ic_a,ic_b),690,300,310)}
    {at(80,700,f'<div class=serif style="font-size:72px;line-height:1.1;font-weight:700;color:{fg}">{title}</div><div style="width:130px;height:5px;background:{acc};margin:32px 0 34px"></div><div style="font-size:45px;line-height:1.45;color:{tc}">{body}</div>')}
    {foot(fg)}"""
    return page(1350,bg,inner)
NOT=[n_cover(),
 nslide(G,IV,IV,GOLD,GOLD,'Nascimento e cuidado','20','semanas','Por cada progenitor','É uma a mais. Intransferíveis. Famílias monoparentais: de 32 para <b>34 semanas</b>.',i_cradle,IV,GOLD),
 nslide(IV,G,INK,TERRA,TERRA,'Atenção ao calendário','1º','de março de 2027','Semana extra: depois','Vale para fatos a partir de <b>26/11/2026</b>, mas a semana adicional só poderá ser pedida a partir de março, segundo a EFE.',i_hourcal,G,GOLD),
 nslide(TERRA,IV,IV,SAND,SAND,'Falecimento','10','dias úteis','Licença por luto','Cônjuge, parceiro(a) de fato ou parente consanguíneo de 1º grau. Uso nas <b>quatro semanas</b> após o falecimento.',i_ribbon,IV,G),
 nslide(IV,G,INK,GOLD,TERRA,'Outros familiares','3','dias úteis','Segundo grau','Antes eram 2. Com deslocamento, somam-se <b>mais 2 dias</b>. A imprensa inclui os afins de 1º grau, como sogros.',i_family,G,TERRA),
 nslide(G,IV,IV,GOLD,GOLD,'Cuidados paliativos','+','novo direito','Adaptar ou reduzir a jornada','Para cuidar de cônjuge, parceiro(a) ou parente consanguíneo até 2º grau. O decreto-lei ainda depende de <b>validação no Congresso</b>.',i_hands,IV,GOLD),
 closing(1350,TERRA,IV,SAND,'Fontes: La Moncloa (24/11/2026); elDiario.es e Infobae/EFE (25/11/2026).<br>Consulta em 26/11/2026.')]

# ============ IMIGRAÇÃO: razões humanitárias ============
def umbrella(x,y,w=920):
    g=f'<path d="M40 300C60 80 250 20 460 20S860 80 880 300C830 252 760 252 705 300C650 252 580 252 530 300C505 272 415 272 390 300C340 252 270 252 215 300C160 252 90 252 40 300Z" fill="{GOLD}"/>'
    g+=f'<path d="M460 20C330 80 300 200 305 270M460 20C590 80 620 200 615 270" fill="none" stroke="{G}" stroke-width="7"/><path d="M460 270V560Q460 610 420 610T380 570" fill="none" stroke="{IV}" stroke-width="18" stroke-linecap="round"/>'
    for cx,cy,r,c in [(290,410,46,IV),(610,420,42,SAND),(550,486,28,IV)]:
        bw=r*1.7
        g+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}"/><path d="M{cx-bw} 620C{cx-bw} {cy+r-6} {cx+bw} {cy+r-6} {cx+bw} 620Z" fill="{c}"/>'
    for px,py in [(30,360),(110,420),(60,520),(160,560),(860,370),(790,450),(880,500),(770,570),(20,160),(900,150),(130,60),(790,50)]:
        g+=f'<path d="M{px} {py}l-16 44" stroke="{SAND}" stroke-width="8" stroke-linecap="round" opacity=".7"/>'
    return svg('0 0 920 620',g,w,int(w*620/920),f'left:{x}px;top:{y}px')
def i_cover():
    inner=f"""{at(0,1170,'',1080,f'height:180px;background:{G}')}{bracket(GOLD)}{kick('Imigração · Hoja 32 (tema)',SAND)}
    {at(80,170,f'<div class=serif style="font-size:96px;line-height:1.06;font-weight:700;color:{IV}">Residência por <span style="color:{SAND};font-style:italic">razões humanitárias</span>: quem a norma prevê</div>')}
    {umbrella(100,580,880)}
    <div class=foot style="bottom:52px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>"""
    inner=inner.replace(' (tema)','').replace(' · Hoja 32',' · Residência')
    return page(1350,TERRA,inner)
def i_scale(a,b): return f'<path d="M100 28V166M60 172H140M40 52H160" stroke="{a}" stroke-width="11" stroke-linecap="round"/><path d="M40 56L14 112H66ZM160 56L134 112H186Z" fill="none" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M12 112Q40 142 68 112ZM132 112Q160 142 188 112Z" fill="{b}"/><circle cx="100" cy="36" r="14" fill="{b}"/>'
def i_permit(a,b): return f'<path d="M100 14L170 40V96C170 140 140 170 100 186C60 170 30 140 30 96V40Z" fill="none" stroke="{a}" stroke-width="11" stroke-linejoin="round"/><circle cx="100" cy="78" r="22" fill="{b}"/><path d="M62 144C62 100 138 100 138 144Z" fill="{b}"/>'
def i_pulse(a,b): return f'<path d="M100 176C40 134 18 100 18 70C18 44 38 26 62 26C80 26 93 36 100 50C107 36 120 26 138 26C162 26 182 44 182 70C182 100 160 134 100 176Z" fill="{b}"/><path d="M10 100H62L78 70L98 138L118 82L130 100H190" fill="none" stroke="{a}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
def i_return(a,b): return f'<circle cx="100" cy="100" r="76" fill="none" stroke="{a}" stroke-width="11"/><path d="M66 106H138M66 106L92 80M66 106L92 132" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><path d="M46 46L154 154" stroke="{b}" stroke-width="16" stroke-linecap="round"/>'
def i_work(a,b): return f'<rect x="22" y="62" width="156" height="112" rx="16" fill="{a}"/><path d="M70 62V44Q70 30 84 30H116Q130 30 130 44V62" fill="none" stroke="{a}" stroke-width="12"/><path d="M22 108H178" stroke="{b}" stroke-width="9"/><rect x="82" y="92" width="36" height="34" rx="7" fill="{b}"/>'
def waveband(c):
    return svg('0 0 1080 90',f'<path d="M0 50Q90 0 180 50T360 50T540 50T720 50T900 50T1080 50" fill="none" stroke="{c}" stroke-width="5"/><path d="M0 76Q90 26 180 76T360 76T540 76T720 76T900 76T1080 76" fill="none" stroke="{c}" stroke-width="3" opacity=".5"/>',1080,90,'left:0;top:1120px')
def islide(bg,fg,tc,acc,k,title,body,icon,disc,ia,ib):
    inner=f"""{bracket(acc)}{kick(k,acc)}
    {at(80,190,f'<div style="width:350px;height:350px;border-radius:175px 175px 24px 24px;background:{disc}"></div>',350)}
    {ico(icon(ia,ib),135,260,240)}
    {at(80,610,f'<div class=serif style="font-size:74px;line-height:1.1;font-weight:700;color:{fg}">{title}</div><div style="width:130px;height:5px;background:{acc};margin:30px 0 32px"></div><div style="font-size:44px;line-height:1.43;color:{tc}">{body}</div>')}
    {waveband(acc)}{foot(fg)}"""
    return page(1350,bg,inner)
IMG=[i_cover(),
 islide(IV,G,INK,TERRA,'O que é','Autorização excepcional','Residência temporária para quem está na Espanha em um dos casos do <b>art. 128</b> do Regulamento de Estrangeiros.',i_permit,G,IV,GOLD),
 islide(G,IV,IV,GOLD,'Proteção e vítimas','Dois dos casos','Permanência autorizada pelo Interior (asilo ou proteção temporária) e vítimas de <b>certos delitos</b>, discriminatórios ou de violência familiar, com sentença firme.',i_scale,GOLD,G,IV),
 islide(IV,G,INK,TERRA,'Saúde','Doença grave surgida na Espanha','Tratamento especializado inacessível no país de origem e <b>grave risco</b> se faltar. Exige relatório clínico da autoridade sanitária.',i_pulse,TERRA,IV,G),
 islide(TERRA,IV,IV,SAND,'Retorno','Perigo ao voltar','Quem comprovar que ir ao país de origem pedir o visto traz <b>perigo</b> para si ou a família e cumprir os demais requisitos.',i_return,SAND,G,TERRA),
 islide(G,IV,IV,GOLD,'Pedido e vigência','Sem visto, por um ano','Pedido em regra pessoal. Permite trabalhar, respeitada a idade mínima. Na doença grave, há prorrogação <b>conforme o tratamento</b>.',i_work,IV,G,GOLD),
 closing(1350,G,IV,GOLD,'Fonte: BOE, Real Decreto 1155/2024, arts. 124 e 128 a 132<br>(texto original, 20/11/2024). Consulta em 26/11/2026.')]

# ============ REEL: silbo gomero ============
def sound(cx,cy,c,d=1,n=4):
    return ''.join(f'<path d="M{cx+d*(30+i*42)} {cy-30-i*24}Q{cx+d*(66+i*52)} {cy} {cx+d*(30+i*42)} {cy+30+i*24}" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" opacity="{1-i*.2}"/>' for i in range(n))
def whistler(x,y,c,d=1):
    return f'<g transform="translate({x} {y}) scale({d} 1)"><circle cx="0" cy="0" r="34" fill="{c}"/><path d="M-52 150C-52 22 52 22 52 150Z" fill="{c}"/><path d="M40 92L52 36L24 8" fill="none" stroke="{c}" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/></g>'
def ravines(y,back,mid,front):
    g=f'<path d="M0 300L150 120L260 240L430 40L560 230L700 110L850 260L1080 90V760H0Z" fill="{back}"/>'
    g+=f'<path d="M0 360L210 290L330 460L470 640L610 480L720 330L1080 300V760H0Z" fill="{mid}"/>'
    g+=f'<path d="M0 560L180 540L300 640L500 720L760 600L900 560L1080 580V760H0Z" fill="{front}"/>'
    g+=whistler(130,386,GOLD,1)+sound(185,386,GOLD,1)+whistler(950,328,IV,-1)+sound(895,328,IV,-1,3)
    return svg('0 0 1080 760',g,1080,760,f'left:0;top:{y}px')
def island(y):
    g=f'<circle cx="440" cy="330" r="320" fill="{SAND}"/><path d="M440 80C560 90 690 170 700 300C710 430 580 590 430 580C290 570 170 470 180 320C190 180 310 70 440 80Z" fill="{G2}"/>'
    for ang in range(0,360,40):
        ex=440+220*math.cos(math.radians(ang)); ey=330+215*math.sin(math.radians(ang))
        g+=f'<path d="M440 320Q{(440+ex)/2+30} {(320+ey)/2-24} {ex:.0f} {ey:.0f}" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linecap="round"/>'
    g+=f'<circle cx="440" cy="320" r="34" fill="{TERRA}" stroke="{IV}" stroke-width="8"/>'
    return svg('0 0 880 660',g,880,660,f'left:100px;top:{y}px')
def notes(y):
    g=''
    for i,v in enumerate('AEIOU'):
        cx=100+i*170
        g+=f'<circle cx="{cx}" cy="90" r="70" fill="none" stroke="{GOLD}" stroke-width="6"/><text x="{cx}" y="116" text-anchor="middle" font-family="Lora" font-weight="700" font-size="76" fill="{IV}">{v}</text>'
    g+=f'<path d="M30 330C150 220 250 220 340 310S520 420 640 300S790 220 850 250" fill="none" stroke="{IV}" stroke-width="16" stroke-linecap="round"/><path d="M30 470C170 540 260 390 400 420S620 540 850 410" fill="none" stroke="{GOLD}" stroke-width="16" stroke-linecap="round"/>'
    return svg('0 0 880 560',g,880,560,f'left:100px;top:{y}px')
def school(y):
    g=f'<rect x="40" y="40" width="800" height="440" rx="24" fill="{G}" stroke="{GOLD}" stroke-width="18"/><path d="M110 520H770" stroke="{TERRA}" stroke-width="22" stroke-linecap="round"/>'
    g+=whistler(230,230,IV,1)+sound(290,230,GOLD,1)
    g+=f'<text x="660" y="250" text-anchor="middle" font-family="Lora" font-weight="700" font-size="104" fill="{IV}">1999</text><text x="660" y="316" text-anchor="middle" font-family="Inter" font-weight="700" font-size="34" letter-spacing="4" fill="{GOLD}">NAS ESCOLAS</text>'
    return svg('0 0 880 560',g,880,560,f'left:100px;top:{y}px')
def reel(bg,acc,fg,inner):
    return page(1920,bg,f"""{bracket(acc)}{at(80,110,f'<span class=kick style="color:{acc}">VOCÊ SABIA? | ESPANHA</span>')}{inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{fg}">Espanha Sem Segredo</span></div></div>""")
def head(t,c,sz=100): return at(80,240,f'<div class=serif style="font-size:{sz}px;line-height:1.08;font-weight:700;color:{c}">{t}</div>')
def txt(t,c,y): return at(80,y,f'<div style="font-size:50px;line-height:1.42;color:{c}">{t}</div>')
RR=[
 reel(G,GOLD,IV,head(f'Na Espanha há uma ilha onde se conversa <span style="color:{GOLD};font-style:italic">assobiando</span>',IV,106)+ravines(880,G2,TERRA,INK)+at(0,1640,'',1080,f'height:280px;background:{INK}')+f'<div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{IV}">Espanha Sem Segredo</span></div></div>'),
 reel(IV,TERRA,G,head(f'La Gomera, nas <span style="color:{TERRA};font-style:italic">Canárias</span>',G)+txt('É a ilha do <b>silbo gomero</b>, uma linguagem assobiada que reproduz a língua espanhola.',INK,560)+island(940)),
 reel(G,GOLD,IV,head(f'Assobios no lugar das <span style="color:{GOLD};font-style:italic">letras</span>',IV)+txt('<b>Dois</b> assobios diferentes substituem as cinco vogais do espanhol. Outros <b>quatro</b>, as consoantes.',IV,560)+notes(1030)),
 reel(TERRA,SAND,IV,head(f'Patrimônio <span style="color:{SAND};font-style:italic">vivo</span>',IV)+txt('Ensinado nas escolas desde 1999. Em <b>2009</b>, entrou na Lista Representativa do Patrimônio Cultural Imaterial da UNESCO.',IV,540)+school(1010)),
 closing(1920,IV,G,TERRA,'Fonte: UNESCO, El silbo gomero.<br>Consulta em 26/11/2026.',logo=460,serif_sz=88,top=.17)]

async def main():
    sets={'noticia':(NOT,1350),'imigracao':(IMG,1350),'cultura':(RR,1920)}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,(lst,h) in sets.items():
            pg=await b.new_page(viewport={'width':1080,'height':h})
            for i,htm in enumerate(lst):
                await pg.set_content(htm); await pg.wait_for_timeout(500)
                await pg.screenshot(path=OUT+f'{k}-{i+1}.png')
        await b.close()
asyncio.run(main())
