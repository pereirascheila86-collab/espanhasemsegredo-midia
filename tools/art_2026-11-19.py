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

# ================= 2026-11-19 =================
# ---------- NOTICIA: ultimo dia do voto por correio (29N) ----------
def ic_calendario(a,b):
    return SV(f'<rect x="24" y="36" width="152" height="140" rx="14" fill="{b}" stroke="{a}" stroke-width="8"/><rect x="24" y="36" width="152" height="40" rx="14" fill="{a}"/><path d="M62 18V50M138 18V50" stroke="{a}" stroke-width="10" stroke-linecap="round"/>{T(100,148,"19",64,a,800,"Lora")}')
def ic_censo(a,b):
    return SV(f'<path d="M44 20H128L160 52V180H44Z" fill="{b}" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><path d="M128 20V52H160" fill="none" stroke="{a}" stroke-width="8" stroke-linejoin="round"/><circle cx="102" cy="82" r="16" fill="{a}"/><path d="M72 128C72 106 84 100 102 100C120 100 132 106 132 128Z" fill="{a}"/><path d="M66 150H138" stroke="{a}" stroke-width="7" stroke-linecap="round"/>')
def ic_laptop_loja(a,b):
    return SV(f'<rect x="38" y="34" width="124" height="86" rx="10" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M18 144H182L168 124H32Z" fill="{a}"/><circle cx="100" cy="76" r="22" fill="{a}"/><path d="M90 76L98 84L112 66" fill="none" stroke="{b}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M80 160H120" stroke="{a}" stroke-width="7" stroke-linecap="round"/>')
def ic_caixa_correio(a,b):
    return SV(f'<path d="M44 176V90C44 52 70 34 100 34C130 34 156 52 156 90V176Z" fill="{a}"/><rect x="68" y="78" width="64" height="12" rx="6" fill="{b}"/><rect x="82" y="108" width="36" height="46" rx="4" fill="{b}"/><path d="M156 74H184V54H156Z" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M170 54V28" stroke="{a}" stroke-width="6"/><path d="M28 176H172" stroke="{a}" stroke-width="9" stroke-linecap="round"/>')
def ic_consulado(a,b):
    return SV(f'<circle cx="100" cy="112" r="60" fill="{b}" stroke="{a}" stroke-width="8"/><path d="M40 112H160M100 52C72 80 72 144 100 172M100 52C128 80 128 144 100 172" fill="none" stroke="{a}" stroke-width="5"/><path d="M100 14V62" stroke="{a}" stroke-width="7"/><path d="M100 14H146V40H100Z" fill="{a}"/><path d="M100 24H146M100 32H146" stroke="{b}" stroke-width="5"/>')
def cover_voto():
    urna=f'<rect x="330" y="720" width="420" height="330" rx="26" fill="{GOLD}"/><rect x="330" y="720" width="420" height="64" rx="26" fill="{TERRA}"/><rect x="430" y="742" width="220" height="22" rx="11" fill="{INK}"/><rect x="400" y="830" width="280" height="150" rx="14" fill="{G}"/>{T(540,918,"VOTO",56,GOLD,800,"Lora",ls=8)}{T(540,962,"POR CORREIO",26,IV,700,"Inter",ls=6)}'
    env=lambda x,y,r:f'<g transform="translate({x} {y}) rotate({r})"><rect width="170" height="112" rx="10" fill="{IV}"/><path d="M0 8L85 70L170 8" fill="none" stroke="{G2}" stroke-width="6"/><rect x="118" y="62" width="34" height="34" rx="5" fill="{TERRA}"/></g>'
    cal=f'<g transform="translate(110 540) rotate(-7)"><rect width="190" height="200" rx="18" fill="{IV}"/><rect width="190" height="60" rx="18" fill="{TERRA}"/><path d="M52 -12V24M138 -12V24" stroke="{IV}" stroke-width="12" stroke-linecap="round"/>{T(95,160,"19",98,G,800,"Lora")}{T(95,44,"NOV",30,IV,800,"Inter",ls=6)}</g>'
    return page(1350,G,f'''{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:74px;line-height:1.05;font-weight:700;color:{IV}">Último dia para pedir o <span style="color:{GOLD};font-style:italic">voto por correio</span> nas eleições de 29N</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="540" cy="900" r="360" fill="{G2}" opacity=".55"/>
      {cal}{env(720,520,12)}{env(760,640,-8)}{urna}
      <path d="M0 1060H1080V1350H0Z" fill="#0B2F2D"/>
    </svg>
    {foot(IV)}''')
NOT=[cover_voto()]
NOT.append(content2('Notícia · O prazo','Pedido só até hoje','O pedido do voto por correio para as eleições gerais de <b>29 de novembro de 2026</b> termina <b>hoje, 19 de novembro</b>, inclusive, segundo os Correos.',ic_calendario,'ivory',46))
NOT.append(content2('Notícia · Requisito','Inscrição no censo eleitoral','É imprescindível ter o <b>certificado de inscrição no Censo Eleitoral</b>. A documentação é enviada ao endereço indicado no pedido, que pode ser diferente do domicílio habitual.',ic_censo,'terra',44))
NOT.append(content2('Notícia · Como pedir','Online ou presencial','<b>Online</b>, em correos.es, com DNI eletrônico ou certificado digital reconhecido. <b>Presencial</b>, em uma agência dos Correos, com DNI, passaporte ou carteira de motorista original.',ic_laptop_loja,'green',44))
NOT.append(content2('Notícia · Depois do pedido','Voto até 25 de novembro','A documentação é enviada desde <b>9 de novembro</b>. O voto deve ser depositado nos Correos até <b>25 de novembro</b>.',ic_caixa_correio,'ivory',50))
NOT.append(content2('Notícia · No exterior','Eleitores no exterior (CERA)','Segundo o Ministério de Exteriores: depósito do voto no consulado de <b>21 a 26 de novembro</b>; votos enviados por correio devem chegar até <b>24 de novembro</b>.',ic_consulado,'green',44))
NOT.append(closing(1350,TERRA,IV,'#F3D79A','Fontes: Correos (06/10/2026); Ministerio de Asuntos Exteriores; Infobae/EFE (19/11/2026).<br>Consulta em 19/11/2026.'))

# ---------- IMIGRACAO: residencia independente de familiar reagrupado (Hoja 11) ----------
def ic_casa_chave(a,b):
    return SV(f'<path d="M20 98L100 30L180 98" fill="none" stroke="{a}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><path d="M40 90V170H160V90L100 40Z" fill="{a}"/><circle cx="84" cy="122" r="18" fill="{b}"/><circle cx="84" cy="122" r="7" fill="{a}"/><path d="M100 122H146M132 122V142M118 122V138" stroke="{b}" stroke-width="9" stroke-linecap="round"/>')
def ic_aneis(a,b):
    return SV(f'<circle cx="74" cy="112" r="46" fill="none" stroke="{a}" stroke-width="16"/><circle cx="126" cy="112" r="46" fill="none" stroke="{b}" stroke-width="16"/><path d="M100 76A46 46 0 0 1 100 148" fill="none" stroke="{a}" stroke-width="16"/><path d="M84 34L100 16L116 34L100 50Z" fill="{b}" stroke="{a}" stroke-width="5"/>')
def ic_bolo18(a,b):
    vel=''.join(f'<path d="M{x} 70V46" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M{x} 40C{x-8} 30 {x} 22 {x} 22C{x} 22 {x+8} 30 {x} 40Z" fill="{b}"/>' for x in (66,100,134))
    return SV(f'{vel}<rect x="36" y="70" width="128" height="40" rx="8" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="24" y="110" width="152" height="62" rx="10" fill="{a}"/>{T(100,158,"18",48,b,800,"Lora")}')
def ic_escudo(a,b):
    return SV(f'<path d="M100 18L168 42V100C168 140 138 164 100 182C62 164 32 140 32 100V42Z" fill="{a}"/><path d="M100 148C70 128 62 106 62 90C62 76 72 68 84 68C92 68 98 72 100 78C102 72 108 68 116 68C128 68 138 76 138 90C138 106 130 128 100 148Z" fill="{b}"/>')
def ic_balcao(a,b):
    return SV(f'<path d="M20 70L100 22L180 70Z" fill="{a}"/><rect x="30" y="70" width="140" height="106" fill="{b}" stroke="{a}" stroke-width="7"/><circle cx="100" cy="104" r="14" fill="{a}"/><path d="M76 138C76 120 86 116 100 116C114 116 124 120 124 138Z" fill="{a}"/><rect x="22" y="138" width="156" height="38" rx="5" fill="{a}"/><path d="M50 158H90M118 158H150" stroke="{b}" stroke-width="7" stroke-linecap="round"/>')
def ic_pessoa_doc(a,b):
    return SV(f'<circle cx="100" cy="60" r="28" fill="{a}"/><path d="M44 160C44 112 66 98 100 98C134 98 156 112 156 160Z" fill="{a}"/><rect x="118" y="116" width="52" height="64" rx="6" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M130 136H158M130 152H158" stroke="{a}" stroke-width="6" stroke-linecap="round"/>')
def cover_indep():
    casa=f'<path d="M250 740L540 500L830 740V1050H250Z" fill="{G}"/><path d="M220 752L540 482L860 752" fill="none" stroke="{TERRA}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/><path d="M470 1050V850C470 800 610 800 610 850V1050Z" fill="{GOLD}"/><rect x="310" y="800" width="100" height="110" rx="10" fill="{IV}"/><rect x="670" y="800" width="100" height="110" rx="10" fill="{IV}"/><path d="M360 800V910M310 855H410M720 800V910M670 855H770" stroke="{G}" stroke-width="5"/>'
    pessoas=figura(330,985,1.9,IV)+figura(750,985,1.9,IV)
    chave=f'<g transform="translate(560 960)"><circle cx="0" cy="0" r="26" fill="{TERRA}" stroke="{IV}" stroke-width="7"/><circle cx="0" cy="0" r="9" fill="{IV}"/><path d="M26 0H84M70 0V22M54 0V16" stroke="{IV}" stroke-width="9" stroke-linecap="round"/></g>'
    return page(1350,IV,f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{IV} 0,{SAND} 100%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Imigração · Família</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:880px;font-size:68px;line-height:1.06;font-weight:700;color:{G}">Familiar reagrupado: quando é possível pedir residência <span style="color:{TERRA};font-style:italic">independente</span>?</div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">
      <circle cx="540" cy="760" r="330" fill="{GOLD}" opacity=".18"/>
      {casa}
      <path d="M0 1050H1080V1350H0Z" fill="{G2}"/>{pessoas}{chave}
    </svg>
    {foot(IV)}''')
IMG=[cover_indep()]
IMG.append(content2('Imigração · Quem pode pedir','Titular da reagrupação','Pessoa com autorização de <b>residência temporal por reagrupação familiar</b>, sem ameaça à ordem pública, à segurança ou à saúde pública, segundo a ficha oficial.',ic_pessoa_doc,'green',44))
IMG.append(content2('Imigração · Cônjuge ou parceiro','Pelo menos 1 ano','Ao menos <b>1 ano</b> de residência por reagrupação na Espanha, mais meios econômicos próprios ou os requisitos de trabalho por conta alheia ou própria.',ic_aneis,'ivory',46))
IMG.append(content2('Imigração · Filhos','Ao chegar à maioridade','<b>5 anos</b> de residência na Espanha, ou comprovação dos requisitos de trabalho ou de meios econômicos previstos na ficha. Aos 5 anos, a Oficina verifica de ofício.',ic_bolo18,'terra',44))
IMG.append(content2('Imigração · Casos especiais','Fim do vínculo, violência, viuvez','Separação ou divórcio: vínculo de <b>3 anos</b> e 1 ano de convivência na Espanha. Violência ou viuvez: sem período mínimo. Pedido em até <b>6 meses</b> do evento.',ic_escudo,'green',42))
IMG.append(content2('Imigração · Como pedir','Presencial, na Oficina','Pessoalmente, na <b>Oficina de Extranjería</b> da sua província, com passaporte ou cartão válido e as provas do caso. A ficha oficial prevê resposta em até <b>3 meses</b>.',ic_balcao,'ivory',46))
IMG.append(closing(1350,TERRA,IV,'#F3D79A','Fonte: Ministerio de Inclusión, Hoja 11 (atualizada em maio de 2025).<br>Consulta em 19/11/2026.'))

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
