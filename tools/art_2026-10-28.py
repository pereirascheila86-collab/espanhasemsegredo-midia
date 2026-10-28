import base64, asyncio, os, html, sys, math
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

# ---------- icons (viewBox 200) ----------
def ic_doc(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M50 20H125L160 55V175H50Z" fill="{b}" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><path d="M125 20V55H160" fill="none" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><g stroke="{a}" stroke-width="6" stroke-linecap="round"><path d="M70 85H140M70 105H140M70 125H112"/></g><circle cx="142" cy="150" r="26" fill="{a}"/><path d="M130 170L124 196L142 186L160 196L154 170Z" fill="{a}"/><path d="M130 150L139 159L155 141" fill="none" stroke="{b}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
def ic_heart(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 172C45 130 24 98 24 68C24 42 44 26 66 26C82 26 94 35 100 48C106 35 118 26 134 26C156 26 176 42 176 68C176 98 155 130 100 172Z" fill="{a}"/><path d="M100 70V118M76 94H124" stroke="{b}" stroke-width="12" stroke-linecap="round"/></svg>'''
def ic_workstudy(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M20 62L82 40L100 100L38 122Z" fill="{a}"/><path d="M82 40L144 62L126 122L100 100Z" fill="{b}" stroke="{a}" stroke-width="5" stroke-linejoin="round"/><rect x="92" y="108" width="88" height="62" rx="8" fill="{a}"/><path d="M120 108V98C120 92 124 88 130 88H142C148 88 152 92 152 98V108" fill="none" stroke="{a}" stroke-width="6"/><path d="M92 136H180" stroke="{b}" stroke-width="5"/><rect x="128" y="130" width="16" height="14" rx="3" fill="{b}"/></svg>'''
def ic_check(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="40" y="30" width="120" height="150" rx="12" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="72" y="16" width="56" height="30" rx="10" fill="{a}"/><g stroke="{a}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M60 82L68 90L82 74M60 114L68 122L82 106M60 146L68 154L82 138"/><path d="M96 82H142M96 114H142M96 146H130"/></g></svg>'''
def ic_cap(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 28L184 66L100 104L16 66Z" fill="{a}"/><path d="M50 90V128C50 144 150 144 150 128V90L100 114Z" fill="{a}" opacity=".85"/><path d="M176 72V124" stroke="{a}" stroke-width="6" stroke-linecap="round"/><circle cx="176" cy="130" r="9" fill="{b}" stroke="{a}" stroke-width="4"/><rect x="62" y="146" width="76" height="40" rx="8" fill="{b}" stroke="{a}" stroke-width="5"/><text x="100" y="175" text-anchor="middle" font-family="Inter" font-weight="800" font-size="26" fill="{a}">IA</text></svg>'''
def ic_person(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="64" r="34" fill="{a}"/><path d="M36 182C36 138 62 114 100 114C138 114 164 138 164 182Z" fill="{a}"/><rect x="124" y="116" width="46" height="62" rx="12" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M134 140H160" stroke="{a}" stroke-width="5" stroke-linecap="round"/></svg>'''
def ic_consulate(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 22L180 70H20Z" fill="{a}"/><g fill="{a}"><rect x="34" y="82" width="20" height="78"/><rect x="72" y="82" width="20" height="78"/><rect x="108" y="82" width="20" height="78"/><rect x="146" y="82" width="20" height="78"/></g><rect x="22" y="164" width="156" height="14" rx="3" fill="{a}"/><circle cx="100" cy="52" r="9" fill="{b}"/></svg>'''
def ic_shield(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 18L168 42V98C168 140 138 168 100 184C62 168 32 140 32 98V42Z" fill="{a}"/><path d="M100 64V132M66 98H134" stroke="{b}" stroke-width="16" stroke-linecap="round"/></svg>'''
def ic_house(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 24L184 94H16Z" fill="{a}"/><rect x="34" y="92" width="132" height="86" fill="{a}"/><rect x="82" y="120" width="36" height="58" rx="18" fill="{b}"/><rect x="48" y="108" width="24" height="24" rx="4" fill="{b}"/><rect x="128" y="108" width="24" height="24" rx="4" fill="{b}"/></svg>'''
def ic_alert(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><path d="M100 22L184 168H16Z" fill="{a}" stroke="{a}" stroke-width="10" stroke-linejoin="round"/><path d="M100 70V122" stroke="{b}" stroke-width="14" stroke-linecap="round"/><circle cx="100" cy="146" r="9" fill="{b}"/></svg>'''
def ic_coin(a,b):
    return f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="74" fill="{a}"/><circle cx="100" cy="100" r="56" fill="none" stroke="{b}" stroke-width="5"/><path d="M118 74C110 66 88 66 84 80C80 96 116 96 114 114C112 130 88 132 80 124M100 58V142" fill="none" stroke="{b}" stroke-width="9" stroke-linecap="round"/></svg>'''

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


# =====================================================================
# 26/10/2026 - noticia (cita automatica TIE), imigracao (voluntariado), cultura (pan con tomate)
# Sem numeracao nos slides. Icones e cenas novos, especificos do assunto.
# =====================================================================
def foot2(col, label=''):
    c=f'<span class=c style="color:{col}">{label}</span>' if label else ''
    return f'<div class=foot><div class=l><img src="{LOGO}"><span class=n style="color:{col}">Espanha Sem Segredo</span></div>{c}</div>'

def svg(inner, vb=200): return f'<svg width="100%" height="100%" viewBox="0 0 {vb} {vb}">{inner}</svg>'

# ---- icones noticia ----
def ic_card(a,b):
    return svg(f'<rect x="14" y="46" width="172" height="112" rx="14" fill="{a}"/><rect x="32" y="70" width="36" height="28" rx="6" fill="{b}"/><path d="M32 84H68M50 70V98" stroke="{a}" stroke-width="3"/><circle cx="142" cy="90" r="19" fill="{b}"/><path d="M110 140C110 118 174 118 174 140Z" fill="{b}"/><path d="M32 122H92M32 138H76" stroke="{b}" stroke-width="7" stroke-linecap="round"/>')
def ic_sms(a,b):
    return svg(f'<rect x="56" y="14" width="88" height="172" rx="20" fill="{b}" stroke="{a}" stroke-width="7"/><path d="M80 24H120" stroke="{a}" stroke-width="6" stroke-linecap="round"/><path d="M72 62H128A10 10 0 0 1 138 72V104A10 10 0 0 1 128 114H100L84 130V114H72A10 10 0 0 1 62 104V72A10 10 0 0 1 72 62Z" fill="{a}"/><circle cx="82" cy="88" r="6" fill="{b}"/><circle cx="100" cy="88" r="6" fill="{b}"/><circle cx="118" cy="88" r="6" fill="{b}"/><rect x="72" y="146" width="56" height="16" rx="8" fill="{a}" opacity=".35"/>')
def ic_pin(a,b):
    return svg(f'<path d="M100 18C68 18 46 42 46 72C46 110 100 164 100 164C100 164 154 110 154 72C154 42 132 18 100 18Z" fill="{a}"/><circle cx="100" cy="72" r="21" fill="{b}"/><ellipse cx="100" cy="178" rx="62" ry="11" fill="none" stroke="{a}" stroke-width="5"/><ellipse cx="100" cy="178" rx="30" ry="5" fill="{a}" opacity=".5"/>')
def ic_hourglass(a,b):
    return svg(f'<path d="M52 20H148M52 180H148" stroke="{a}" stroke-width="12" stroke-linecap="round"/><path d="M62 20C62 78 100 88 100 100C100 112 62 122 62 180M138 20C138 78 100 88 100 100C100 112 138 122 138 180" fill="none" stroke="{a}" stroke-width="9"/><path d="M72 40H128C124 66 100 80 100 80C100 80 76 66 72 40Z" fill="{a}"/><path d="M76 166C80 140 120 140 124 166Z" fill="{a}"/><path d="M100 92V140" stroke="{a}" stroke-width="4" stroke-dasharray="4 6"/>')
def ic_refresh(a,b):
    return svg(f'<g fill="none" stroke="{a}" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"><path d="M40 104A60 60 0 0 1 148 64"/><path d="M152 28V70H110"/><path d="M160 96A60 60 0 0 1 52 136"/><path d="M48 172V130H90"/></g><circle cx="100" cy="100" r="14" fill="{a}"/><path d="M100 92V101L106 106" stroke="{b}" stroke-width="4" fill="none" stroke-linecap="round"/>')
# ---- icones imigracao ----
def ic_vol(a,b):
    return svg(f'<path d="M26 104C26 152 58 180 100 180C142 180 174 152 174 104" fill="none" stroke="{a}" stroke-width="15" stroke-linecap="round"/><path d="M14 104H40M160 104H186" stroke="{a}" stroke-width="15" stroke-linecap="round"/><g transform="translate(48 8) scale(.52)"><path d="M100 172C45 130 24 98 24 68C24 42 44 26 66 26C82 26 94 35 100 48C106 35 118 26 134 26C156 26 176 42 176 68C176 98 155 130 100 172Z" fill="{a}"/></g><circle cx="100" cy="64" r="7" fill="{b}"/>')
def ic_agree(a,b):
    return svg(f'<path d="M40 16H128L164 52V184H40Z" fill="{b}" stroke="{a}" stroke-width="7" stroke-linejoin="round"/><path d="M128 16V52H164" fill="none" stroke="{a}" stroke-width="7" stroke-linejoin="round"/><path d="M60 78H118M60 98H140" stroke="{a}" stroke-width="7" stroke-linecap="round"/><path d="M58 150C66 128 74 166 86 142C92 130 100 154 116 138" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round"/><circle cx="142" cy="150" r="22" fill="{a}"/><path d="M142 138L146 147L156 148L149 154L151 164L142 159L133 164L135 154L128 148L138 147Z" fill="{b}"/>')
def ic_nomoney(a,b):
    return svg(f'<circle cx="100" cy="100" r="74" fill="{a}"/><circle cx="100" cy="100" r="58" fill="none" stroke="{b}" stroke-width="4"/><text x="100" y="132" text-anchor="middle" font-family="Lora" font-weight="700" font-size="96" fill="{b}">€</text><path d="M38 162L162 38" stroke="{b}" stroke-width="26" stroke-linecap="round"/><path d="M38 162L162 38" stroke="{a}" stroke-width="12" stroke-linecap="round"/>')
def ic_health(a,b):
    return svg(f'<circle cx="92" cy="92" r="72" fill="{a}"/><path d="M92 50V134M50 92H134" stroke="{b}" stroke-width="26" stroke-linecap="round"/><circle cx="150" cy="150" r="38" fill="{b}" stroke="{a}" stroke-width="7"/><text x="150" y="166" text-anchor="middle" font-family="Lora" font-weight="700" font-size="46" fill="{a}">€</text>')
def ic_passport(a,b):
    return svg(f'<rect x="46" y="14" width="108" height="172" rx="12" fill="{a}"/><rect x="58" y="26" width="84" height="148" rx="6" fill="none" stroke="{b}" stroke-width="3" opacity=".7"/><circle cx="100" cy="82" r="30" fill="none" stroke="{b}" stroke-width="5"/><ellipse cx="100" cy="82" rx="12" ry="30" fill="none" stroke="{b}" stroke-width="4"/><path d="M70 82H130M76 64H124M76 100H124" stroke="{b}" stroke-width="3"/><path d="M72 134H128M82 150H118" stroke="{b}" stroke-width="6" stroke-linecap="round"/><circle cx="150" cy="150" r="26" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M138 150L147 159L163 141" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')

def content2(variant,kick,title,body,icon_fn,theme):
    th={'ivory':(IV,G,INK,G2,GOLD),'green':(G,IV,IV,GOLD,GOLD),'terra':(TERRA,IV,IV,IV,'#F3D79A'),'sand':(SAND,G,INK,TERRA,TERRA)}[theme]
    bg,hc,bc,kc,accent=th
    if theme=='ivory': ia,ib,pbg=IV,GOLD,G
    elif theme=='green': ia,ib,pbg=G,TERRA,GOLD
    elif theme=='terra': ia,ib,pbg=TERRA,G,IV
    else: ia,ib,pbg=SAND,GOLD,G
    if variant=='N':
        ico=f'<div class=abs style="right:80px;top:170px;width:280px;height:280px;border-radius:36px;background:{pbg};padding:42px;transform:rotate(4deg)">{icon_fn(ia,ib)}</div><div class=abs style="right:96px;top:186px;width:280px;height:280px;border-radius:36px;border:3px solid {accent};transform:rotate(4deg)"></div>'
        head=f'<div class=abs style="left:80px;top:96px"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div><div class="abs serif" style="left:80px;top:196px;width:560px;font-size:76px;line-height:1.08;font-weight:700;color:{hc}">{title}</div>'
        bodyx=f'<div class=abs style="left:80px;top:590px;width:920px"><div style="width:130px;height:5px;background:{accent};margin-bottom:40px"></div><div style="font-size:52px;line-height:1.42;color:{bc}">{body}</div></div>'
        deco=f'<div class=abs style="left:0;top:0;bottom:0;width:22px;background:{accent}"></div>'
    else:
        ico=f'<div class=abs style="left:80px;top:190px">{badge(icon_fn(ia,ib),pbg,ia,250)}</div>'
        head=f'<div class=abs style="left:80px;top:96px"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div><div class="abs serif" style="left:380px;top:222px;width:620px;font-size:72px;line-height:1.08;font-weight:700;color:{hc}">{title}</div>'
        bodyx=f'<div class=abs style="left:80px;top:520px;width:920px"><div style="width:100%;height:3px;background:{accent};opacity:.6;margin-bottom:40px"></div><div style="font-size:52px;line-height:1.42;color:{bc}">{body}</div></div>'
        deco=f'<svg class=abs style="left:0;bottom:130px;opacity:.28" width="1080" height="40" viewBox="0 0 1080 40"><path d="M0 20Q135 -10 270 20T540 20T810 20T1080 20" fill="none" stroke="{accent}" stroke-width="3" stroke-dasharray="3 14" stroke-linecap="round"/></svg>'
    return page(1350,bg,f'{deco}{bracket(accent)}{head}{ico}{bodyx}{foot2(hc)}')

def closing2(h,bg,fg,acc,srcs,cta='',logo=360,serif_sz=70,top=.12):
    pad=80
    y1=int(h*top); y2=y1+logo+60; y3=y2+serif_sz*3+50
    inner=f'''{bracket(acc)}
    <div class=abs style="left:0;right:0;top:{y1}px;display:flex;justify-content:center"><img src="{LOGO}" width="{logo}" height="{logo}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{y2}px;text-align:center;font-size:{serif_sz}px;line-height:1.14;font-weight:700;color:{fg}">Aqui você fica por dentro de tudo sobre a Espanha</div>
    <div class=abs style="left:50%;margin-left:-65px;top:{y3}px;width:130px;height:5px;background:{acc}"></div>
    <div class="abs serif" style="left:{pad}px;right:{pad}px;top:{y3+40}px;text-align:center;font-size:56px;font-weight:700;color:{acc}">Espanha Sem Segredo</div>
    <div class=abs style="left:{pad}px;right:{pad}px;top:{y3+120}px;text-align:center;font-size:40px;color:{fg}">Siga <b>@espanhasemsegredo</b></div>
    {f'<div class=abs style="left:{pad}px;right:{pad}px;top:{y3+190}px;text-align:center;font-size:36px;color:{acc};font-weight:700">{cta}</div>' if cta else ''}
    <div class=abs style="left:{pad+20}px;right:{pad+20}px;bottom:70px;text-align:center;font-size:25px;line-height:1.5;color:{fg};opacity:.88">{srcs}<br>Conteúdo informativo, não é assessoria jurídica.</div>'''
    return page(h,bg,inner)

THA={'gI':(G,IV,GOLD,IV,INK,GOLD,GOLD,G,IV),
     'tI':(TERRA,IV,'#F3D79A',IV,INK,GOLD,G,IV,GOLD),
     'iG':(IV,G,TERRA,G,IV,GOLD,TERRA,IV,G),
     'sG':(SAND,G,TERRA,G,IV,GOLD,GOLD,G,IV)}
def contentA(kick,title,body,icon_fn,theme,tw=600):
    tb,tf,kc,bb,bf,acc,cbg,ia,ib=THA[theme]
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:640px;background:{tb}"></div>
    <div class=abs style="left:0;top:640px;width:1080px;height:710px;background:{bb}"></div>
    <svg class=abs style="left:0;top:610px" width="1080" height="60" viewBox="0 0 1080 60" preserveAspectRatio="none"><path d="M0 0H1080V30Q1020 60 960 30T840 30T720 30T600 30T480 30T360 30T240 30T120 30T0 30Z" fill="{tb}"/></svg>
    {bracket(acc)}
    <div class=abs style="left:80px;top:96px"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div>
    <div class="abs serif" style="left:80px;top:180px;width:{tw}px;font-size:84px;line-height:1.08;font-weight:700;color:{tf}">{title}</div>
    <div class=abs style="left:84px;top:520px;width:130px;height:5px;background:{acc}"></div>
    <div class=abs style="left:700px;top:440px;width:300px;height:300px;border-radius:50%;background:{cbg};box-shadow:0 0 0 10px {bb}"><div style="width:100%;height:100%;padding:62px">{icon_fn(ia,ib)}</div></div>
    <div class=abs style="left:80px;top:770px;width:920px;font-size:{48 if len(body)<150 else 43}px;line-height:1.4;color:{bf}">{body}</div>
    {foot2(bf if bb!=IV else G)}'''
    return page(1350,tb,inner)

# ---------- layout B (imigracao): janela em arco centralizada, titulo e texto centralizados ----------
THB={'ivory':(IV,G,INK,TERRA,GOLD,G,IV,GOLD),
     'sand':(SAND,G,INK,TERRA,TERRA,G,SAND,GOLD),
     'green':(G,IV,IV,GOLD,GOLD,GOLD,G,IV),
     'terra':(TERRA,IV,IV,'#F3D79A',IV,IV,TERRA,G)}
def contentB(kick,title,body,icon_fn,theme,ts=70):
    bg,hc,bc,kc,acc,abg,ia,ib=THB[theme]
    inner=f'''{bracket(acc)}
    <div class=abs style="left:0;right:0;top:78px;text-align:center"><div class=kick style="color:{kc}">{html.escape(kick)}</div></div>
    <svg class=abs style="left:330px;top:160px" width="420" height="440" viewBox="0 0 420 440"><path d="M10 440V190C10 80 100 10 210 10C320 10 410 80 410 190V440Z" fill="{abg}"/><path d="M34 440V192C34 96 112 34 210 34C308 34 386 96 386 192V440" fill="none" stroke="{acc}" stroke-width="3" opacity=".7"/></svg>
    <div class=abs style="left:390px;top:240px;width:300px;height:300px">{icon_fn(ia,ib)}</div>
    <div class="abs serif" style="left:80px;right:80px;top:660px;text-align:center;font-size:{ts}px;line-height:1.08;font-weight:700;color:{hc}">{title}</div>
    <div class=abs style="left:50%;margin-left:-65px;top:{660+ts+40}px;width:130px;height:5px;background:{acc}"></div>
    <div class=abs style="left:90px;right:90px;top:{660+ts+90}px;text-align:center;font-size:48px;line-height:1.42;color:{bc}">{body}</div>
    {foot2(hc)}'''
    return page(1350,bg,inner)


# =====================================================================
# 28/10/2026 - noticia (zonas gravemente afetadas), imigracao (renovacao 13), cultura (mercados de Madri)
# Icones e cenas novos. Sem numeracao nos slides.
# =====================================================================
def ic_govdome(a,b):
    return svg(f'<path d="M60 84C60 52 80 34 100 34C120 34 140 52 140 84Z" fill="{a}"/><rect x="96" y="14" width="8" height="22" fill="{a}"/><path d="M104 14H128V28H104Z" fill="{b}"/><rect x="40" y="88" width="120" height="12" fill="{a}"/><g fill="{a}"><rect x="48" y="104" width="16" height="54"/><rect x="78" y="104" width="16" height="54"/><rect x="106" y="104" width="16" height="54"/><rect x="136" y="104" width="16" height="54"/></g><rect x="34" y="162" width="132" height="14" rx="3" fill="{a}"/><circle cx="152" cy="150" r="30" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M138 150L148 160L167 140" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_ninepins(a,b):
    pins=''
    for r in range(3):
        for c in range(3):
            x=44+c*56; y=52+r*52
            pins+=f'<path d="M{x} {y+30}C{x-14} {y+8} {x-12} {y-14} {x} {y-14}C{x+12} {y-14} {x+14} {y+8} {x} {y+30}Z" fill="{a if (r+c)%2==0 else b}"/><circle cx="{x}" cy="{y-2}" r="5" fill="{b if (r+c)%2==0 else a}"/>'
    return svg(f'<rect x="12" y="20" width="176" height="164" rx="22" fill="none" stroke="{a}" stroke-width="5" stroke-dasharray="3 11" stroke-linecap="round"/>{pins}')
def ic_stormfire(a,b):
    return svg(f'<path d="M52 98C30 98 20 82 24 68C28 52 46 48 56 54C60 34 80 26 98 34C112 22 142 28 146 54C166 54 178 70 172 86C168 96 158 98 148 98Z" fill="{a}"/><g stroke="{b}" stroke-width="7" stroke-linecap="round"><path d="M56 112L48 138M84 112L76 138M112 112L104 138"/></g><path d="M146 186C122 186 110 168 118 148C122 160 130 160 132 150C130 134 142 124 146 112C152 128 172 134 172 160C172 176 162 186 146 186Z" fill="{b}" stroke="{a}" stroke-width="4"/>')
def ic_housecoin(a,b):
    return svg(f'<path d="M20 100L100 28L180 100V174H20Z" fill="{a}"/><rect x="78" y="124" width="44" height="50" rx="6" fill="{b}"/><circle cx="100" cy="86" r="30" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M108 76C102 70 90 72 90 82C90 94 110 90 110 100C110 108 98 110 92 104M100 66V112" fill="none" stroke="{a}" stroke-width="6" stroke-linecap="round"/>')
def ic_claim(a,b):
    return svg(f'<path d="M36 26H128L156 54V174H36Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><path d="M128 26V54H156" fill="none" stroke="{a}" stroke-width="6" stroke-linejoin="round"/><g stroke="{a}" stroke-width="7" stroke-linecap="round"><path d="M58 80H120M58 104H120M58 128H92"/></g><path d="M118 176L168 126L184 142L134 192L112 196Z" fill="{a}"/><path d="M168 126L176 118C180 114 186 114 190 118C194 122 194 128 190 132L184 142Z" fill="{b}" stroke="{a}" stroke-width="4"/>')

# ---------- NOTICIA ----------
def rain(x0,y0,w,h,col,n=14):
    s=''
    for i in range(n):
        x=x0+(i*w/n)+((i*37)%23); y=y0+((i*53)%h)
        s+=f'<path d="M{x:.0f} {y:.0f}l-14 40" stroke="{col}" stroke-width="5" stroke-linecap="round" opacity=".75"/>'
    return f'<svg class=abs style="left:0;top:0" width="1080" height="1350">{s}</svg>'
def noticia_cover():
    cloud=f'<svg class=abs style="left:560px;top:80px" width="440" height="260" viewBox="0 0 440 260"><path d="M110 200C50 200 22 160 36 124C48 92 92 82 116 98C124 44 180 12 232 34C262 8 332 22 344 84C400 84 430 130 410 168C398 192 372 200 346 200Z" fill="{IV}" opacity=".95"/></svg>'
    dots=''.join(f'<circle cx="{110+i*107}" cy="1118" r="34" fill="none" stroke="{GOLD}" stroke-width="5"/><circle cx="{110+i*107}" cy="1118" r="14" fill="{GOLD}"/>' for i in range(9))
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:{TERRA}"></div>
    <div class=abs style="left:-300px;top:700px;width:1680px;height:1680px;border-radius:50%;background:{G}"></div>
    {rain(520,330,500,300,IV)}{cloud}{bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:560px;font-size:74px;line-height:1.06;font-weight:700;color:{IV}">Governo declara <span style="color:#F3D79A;font-style:italic">zona gravemente afetada</span></div>
    <div class="abs serif" style="left:60px;top:560px;font-size:430px;font-weight:700;line-height:1;color:{IV};letter-spacing:-.04em">45</div>
    <div class=abs style="left:560px;top:700px;width:440px;font-size:38px;line-height:1.35;color:{IV}">episódios adversos em <b>nove comunidades autônomas</b></div>
    <svg class=abs style="left:0;top:0" width="1080" height="1350">{dots}</svg>
    <div class=abs style="left:80px;right:80px;top:1180px;text-align:center;font-size:30px;letter-spacing:.12em;font-weight:700;color:{GOLD}">CONSELHO DE MINISTROS · 27/10/2026</div>
    <div class=abs style="left:0;right:0;bottom:0;height:130px;background:{INK}"></div>
    <div class=foot style="bottom:30px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,TERRA,inner)
NOT0=[noticia_cover(),
 content2('N','Notícia · O acordo','O que foi decidido','O Conselho de Ministros declarou "zona afetada gravemente por uma emergência de proteção civil" os territórios atingidos por emergências até 20 de outubro de 2026.',ic_govdome,'ivory'),
 content2('N','Notícia · Onde','Nove comunidades','Andaluzia, Castela e Leão, Castela-Mancha, Catalunha, Comunidade Valenciana, Extremadura, Galiza, Ilhas Baleares e Região de Múrcia.',ic_ninepins,'green'),
 content2('N','Notícia · O que houve','Incêndios e chuvas','Os episódios incluem incêndios florestais, chuvas intensas e inundações. A DANA Adam, desde 17 de outubro, deixou sete mortos, segundo o balanço provisório.',ic_stormfire,'terra'),
 content2('N','Notícia · As ajudas','Ajudas previstas','Há ajudas para danos pessoais e em moradias, estabelecimentos e despesas de entes locais. O IRPF não incide sobre ajudas por danos pessoais.',ic_housecoin,'sand'),
 content2('N','Notícia · Quem pede','Quem pode solicitar','Segundo o Governo, pessoas ou entidades que comprovem os danos podem pedir as ajudas à Secretaria-Geral de Proteção Civil e Emergências.',ic_claim,'ivory'),
 closing2(1350,G2,IV,GOLD,'Fontes: La Moncloa, referência do Conselho de Ministros de 27/10/2026.<br>Consulta em 28/10/2026.')]

NOT=[x.replace('font-size:52px;line-height:1.42','font-size:56px;line-height:1.4') for x in NOT0]
# ---------- IMIGRACAO ----------
def ic_renewcal(a,b):
    return svg(f'<rect x="26" y="44" width="148" height="132" rx="16" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="26" y="44" width="148" height="34" rx="16" fill="{a}"/><g stroke="{a}" stroke-width="8" stroke-linecap="round"><path d="M60 26V56M140 26V56"/></g><path d="M70 126A32 32 0 0 1 128 108" fill="none" stroke="{a}" stroke-width="9" stroke-linecap="round"/><path d="M130 88L132 112L108 110" fill="none" stroke="{a}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M130 130A32 32 0 0 1 72 148" fill="none" stroke="{a}" stroke-width="9" stroke-linecap="round" opacity=".55"/>')
def ic_lateclock(a,b):
    return svg(f'<circle cx="100" cy="104" r="72" fill="{a}"/><circle cx="100" cy="104" r="58" fill="{b}"/><path d="M100 62V106L130 126" fill="none" stroke="{a}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="M158 24L186 52M42 24L14 52" stroke="{a}" stroke-width="10" stroke-linecap="round"/><circle cx="160" cy="160" r="26" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M160 146V162M160 172V174" stroke="{a}" stroke-width="8" stroke-linecap="round"/>')
def ic_reqlist(a,b):
    return svg(f'<path d="M100 14L170 38V92C170 134 140 162 100 178C60 162 30 134 30 92V38Z" fill="{a}"/><g stroke="{b}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none"><path d="M64 70L74 80L92 60M64 112L74 122L92 102"/></g><g stroke="{b}" stroke-width="8" stroke-linecap="round"><path d="M110 72H140M110 114H140"/></g>')
def ic_folderstamp(a,b):
    return svg(f'<path d="M20 52C20 42 26 36 36 36H78L94 56H164C174 56 180 62 180 72V160C180 170 174 176 164 176H36C26 176 20 170 20 160Z" fill="{a}"/><rect x="44" y="76" width="96" height="78" rx="6" fill="{b}" transform="rotate(-5 92 115)"/><g stroke="{a}" stroke-width="6" stroke-linecap="round"><path d="M58 100H116M58 120H116M58 140H92" transform="rotate(-5 92 115)"/></g><circle cx="148" cy="144" r="26" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M136 144L145 153L161 135" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_officemail(a,b):
    return svg(f'<path d="M20 90L100 28L180 90Z" fill="{a}"/><rect x="34" y="90" width="132" height="84" fill="{a}"/><rect x="52" y="108" width="34" height="30" rx="4" fill="{b}"/><rect x="114" y="108" width="34" height="30" rx="4" fill="{b}"/><rect x="86" y="138" width="28" height="36" fill="{b}"/><rect x="104" y="14" width="56" height="40" rx="6" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M106 18L132 38L158 18" fill="none" stroke="{a}" stroke-width="5" stroke-linejoin="round"/>')
def ic_sedelaptop(a,b):
    return svg(f'<rect x="38" y="40" width="124" height="86" rx="10" fill="{a}"/><rect x="48" y="50" width="104" height="66" rx="4" fill="{b}"/><path d="M18 140H182L170 160H30Z" fill="{a}"/><path d="M70 98L90 78L104 92L132 64" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="150" cy="148" r="26" fill="{b}" stroke="{a}" stroke-width="5"/><path d="M138 148L147 157L163 139" fill="none" stroke="{a}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
def imig_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:{IV}"></div>
    <div class=abs style="left:0;top:0;width:1080px;height:560px;background:{G}"></div>
    <svg class=abs style="left:0;top:530px" width="1080" height="60" viewBox="0 0 1080 60" preserveAspectRatio="none"><path d="M0 0H1080V30Q1020 60 960 30T840 30T720 30T600 30T480 30T360 30T240 30T120 30T0 30Z" fill="{G}"/></svg>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Renovações</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:760px;font-size:68px;line-height:1.06;font-weight:700;color:{IV}">Como renovar a residência temporal e trabalho por conta alheia?</div>
    <div class=abs style="left:90px;top:660px;width:430px;height:430px;transform:rotate(-5deg)">{ic_renewcal(G,SAND)}</div>
    <div class="abs serif" style="left:560px;top:640px;font-size:230px;font-weight:700;line-height:1;color:{TERRA}">2</div>
    <div class=abs style="left:560px;top:880px;width:420px;font-size:44px;line-height:1.25;font-weight:700;color:{G}">meses antes do vencimento</div>
    <div class=abs style="left:560px;top:1000px;width:420px;font-size:32px;line-height:1.35;color:{INK}">é quando a ficha oficial prevê o pedido</div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{TERRA}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{IV}">Espanha Sem Segredo</span></div><span class=c style="color:{IV}">DESLIZE  →</span></div>'''
    return page(1350,IV,inner)
IMG0=[imig_cover(),
 contentA('Imigração · Prazo','Quando pedir','O pedido pode ser feito nos 2 meses anteriores ao vencimento. Se for feito no prazo, a validade da autorização atual se prorroga até o fim do procedimento.',ic_renewcal,'iG'),
 contentA('Imigração · Fora do prazo','Pedido fora do prazo','É possível pedir até 3 meses depois do vencimento, mas isso pode levar a um procedimento sancionador.',ic_lateclock,'tI',tw=620),
 contentA('Imigração · Requisitos','Requisitos','Sem antecedentes penais na Espanha, taxa paga e comprovação de uma das situações previstas na ficha, como a continuidade da relação de trabalho.',ic_reqlist,'gI'),
 contentA('Imigração · Como pedir','Como pedir','Recomendamos fazer o pedido de forma telemática, pela sede eletrônica Mercurio. A ficha oficial também prevê o pedido presencial na Oficina de Extranjería.',ic_sedelaptop,'sG',tw=620),
 contentA('Imigração · Depois','Depois do pedido','A ficha oficial prevê resposta em até 3 meses. A renovação vale 4 anos e, aprovada, a TIE deve ser pedida em 1 mês.',ic_officemail,'iG',tw=620),
 closing2(1350,TERRA,IV,'#F3D79A','Fonte: Ministerio de Inclusión, Ficha 13 (maio de 2025).<br>Consulta em 27/10/2026.',cta='Qual é a sua dúvida sobre renovação?')]

IMG=[x.replace('font-size:43px;line-height:1.4','font-size:49px;line-height:1.4').replace('font-size:48px;line-height:1.4','font-size:52px;line-height:1.4') for x in IMG0]
# ---------- CULTURA: mercados de Madri (Reel 1080x1920) ----------
def reel_scene(bg,kick_col,inner,fgfoot):
    return page(1920,bg,f'''{bracket(kick_col)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{kick_col}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{fgfoot}">Espanha Sem Segredo</span></div></div>''')
def awning(x,y,w,n,c1,c2,h=150):
    s='';sw=w/n
    for i in range(n):
        s+=f'<path d="M{x+i*sw:.1f} {y}h{sw:.1f}v{h-40}a{sw/2:.1f} 40 0 0 1 -{sw:.1f} 0Z" fill="{c1 if i%2==0 else c2}"/>'
    return s
def produce(cx,cy,r,cols):
    s=''
    for i,c in enumerate(cols):
        s+=f'<circle cx="{cx+(i%4)*r*2-r*3+ (r if (i//4)%2 else 0)}" cy="{cy-(i//4)*r*1.7}" r="{r}" fill="{c}"/>'
    return s
# tela 1
stall=f'''<svg class=abs style="left:0;top:0" width="1080" height="1920">
{awning(100,820,880,8,TERRA,IV,170)}
<rect x="100" y="800" width="880" height="26" fill="{G}"/>
<rect x="130" y="990" width="12" height="560" fill="{G}"/><rect x="938" y="990" width="12" height="560" fill="{G}"/>
<rect x="100" y="1250" width="880" height="26" rx="6" fill="{G}"/>
<rect x="130" y="1276" width="820" height="260" fill="{SAND}"/>
<g>{produce(540,1236,52,[TERRA,GOLD,TERRA,GOLD,GOLD,TERRA,GOLD,TERRA,TERRA,GOLD,TERRA,GOLD])}</g>
<rect x="190" y="1160" width="200" height="90" rx="10" fill="{G2}"/><g stroke="{GOLD}" stroke-width="5"><path d="M210 1180H370M210 1205H370M210 1230H370"/></g>
<g transform="translate(820 1090)"><path d="M0 0H110L95 90H15Z" fill="none" stroke="{G}" stroke-width="8"/><path d="M-20 -10H130" stroke="{G}" stroke-width="8" stroke-linecap="round"/><path d="M55 -10V-60" stroke="{G}" stroke-width="8"/><circle cx="55" cy="-72" r="14" fill="{GOLD}"/></g>
<rect x="150" y="900" width="760" height="64" rx="10" fill="{G}"/><text x="530" y="945" text-anchor="middle" font-family="Lora" font-weight="700" font-style="italic" font-size="38" fill="{GOLD}">Mercado Municipal</text>
</svg>'''
c1=f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(0deg,rgba(15,61,58,.05) 0 3px,transparent 3px 60px)"></div>
<div class="abs serif" style="left:80px;top:240px;width:920px;font-size:112px;line-height:1.05;font-weight:700;color:{G}">Mercados municipais de <span style="color:{TERRA};font-style:italic">Madri</span>: você sabe o que são?</div>
<div class=abs style="left:0;top:130px">{stall}</div>'''
# tela 2: 45 e 21 distritos
def dgrid():
    s=''
    for i in range(21):
        r,c=divmod(i,7); x=130+c*120; y=1290+r*140
        s+=f'<path d="M{x} {y+90}V{y+36}C{x} {y} {x+80} {y} {x+80} {y+36}V{y+90}Z" fill="{G2}" stroke="{GOLD}" stroke-width="4"/><circle cx="{x+40}" cy="{y+54}" r="9" fill="{GOLD}"/>'
    return f'<svg class=abs style="left:0;top:0" width="1080" height="1920">{s}</svg>'
c2=f'''<div class=abs style="left:80px;top:250px;font-size:44px;letter-spacing:.14em;font-weight:700;color:{GOLD}">SEGUNDO A PREFEITURA</div>
<div class="abs serif" style="left:60px;top:300px;font-size:560px;line-height:1;font-weight:700;color:{IV};letter-spacing:-.05em">45</div>
<div class="abs serif" style="left:80px;top:900px;width:920px;font-size:80px;line-height:1.1;font-weight:700;color:#F3D79A">mercados municipais</div>
<div class=abs style="left:80px;top:1060px;width:920px;font-size:50px;line-height:1.35;color:{IV}">espalhados por <b>21 distritos</b> de Madri</div>
<div class=abs style="left:84px;top:1190px;width:130px;height:5px;background:{GOLD}"></div>
<div class=abs style="left:0;top:10px">{dgrid()}</div>'''
# tela 3: 2.331 e barras
def bars():
    return f'''<svg class=abs style="left:0;top:0" width="1080" height="1920">
<rect x="80" y="1020" width="920" height="120" rx="24" fill="{G}"/><rect x="80" y="1020" width="{920*1173/2331:.0f}" height="120" rx="24" fill="{TERRA}"/>
<text x="110" y="1096" font-family="Inter" font-weight="800" font-size="56" fill="{IV}">1.173</text>
<rect x="80" y="1290" width="920" height="120" rx="24" fill="{G}"/><rect x="80" y="1290" width="{920*323/2331:.0f}" height="120" rx="24" fill="{TERRA}"/>
<text x="110" y="1366" font-family="Inter" font-weight="800" font-size="56" fill="{IV}">323</text>
<g transform="translate(900 1080)"><path d="M-40 0H40L30 40H-30Z" fill="{IV}"/><path d="M-30 0C-30 -30 30 -30 30 0" fill="none" stroke="{IV}" stroke-width="7"/></g>
<g transform="translate(900 1350)" stroke="{IV}" stroke-width="8" stroke-linecap="round" fill="none"><path d="M-22 -34V30M-34 -34V-8C-34 0 -22 0 -22 -8V-34M-10 -34V-8C-10 0 -22 0 -22 -8M20 -34C34 -20 34 4 20 8V30"/></g>
</svg>
<div class=abs style="left:80px;top:1160px;width:920px;white-space:nowrap;font-size:42px;color:{INK}">pequenos comércios de alimentos</div>
<div class=abs style="left:80px;top:1430px;width:920px;white-space:nowrap;font-size:42px;color:{INK}">hotelaria e restauração</div>'''
c3=f'''<div class=abs style="left:80px;top:250px;font-size:44px;letter-spacing:.14em;font-weight:700;color:{TERRA}">NESSES MERCADOS</div>
<div class="abs serif" style="left:60px;top:330px;font-size:300px;line-height:1;font-weight:700;color:{G};letter-spacing:-.03em">2.331</div>
<div class="abs serif" style="left:80px;top:690px;width:920px;font-size:92px;line-height:1.08;font-weight:700;color:{G}">locais de <span style="color:{TERRA};font-style:italic">venda</span></div>
<div class=abs style="left:84px;top:900px;width:140px;height:6px;background:{GOLD}"></div>
<div class=abs style="left:0;top:200px">{bars()}</div>'''
# tela 4: definicao RAE
def trade():
    return f'''<svg class=abs style="left:0;top:0" width="1080" height="1920">
<rect x="130" y="760" width="820" height="520" rx="26" fill="{IV}"/><rect x="130" y="760" width="820" height="520" rx="26" fill="none" stroke="{GOLD}" stroke-width="6" transform="translate(12 12)"/>
<text x="190" y="880" font-family="Lora" font-style="italic" font-weight="700" font-size="104" fill="{TERRA}">mercado</text>
<path d="M190 918H890" stroke="{G}" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>
<text x="190" y="1010" font-family="Inter" font-size="40" fill="{INK}">Lugar público destinado a</text>
<g font-family="Inter" font-weight="800" font-size="46" fill="{G}"><text x="190" y="1110">vender</text><text x="190" y="1180">comprar</text><text x="190" y="1250">ou trocar</text></g>
<g transform="translate(700 1130)" fill="none" stroke="{TERRA}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"><path d="M-110 -40H90M60 -80L100 -40L60 0"/><path d="M110 40H-90M-60 0L-100 40L-60 80"/></g>
</svg>'''
c4=f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:100px;line-height:1.06;font-weight:700;color:{IV}">O que é um <span style="color:#F3D79A;font-style:italic">mercado?</span></div>
<div class=abs style="left:0;top:140px">{trade()}</div>
<div class=abs style="left:80px;top:1560px;width:920px;font-size:46px;line-height:1.4;color:{IV}">Definição geral da RAE: bens e serviços, em lugar público.</div>'''
REEL=[reel_scene(IV,TERRA,c1,G),reel_scene(G,GOLD,c2,GOLD),reel_scene(SAND,TERRA,c3,G),reel_scene(TERRA,'#F3D79A',c4,IV),
 closing2(1920,IV,G,TERRA,'Fontes: RAE; Ayuntamiento de Madrid (09/2024).<br>Consulta em 23/10/2026.',cta='Qual mercado quer conhecer? Comente o nome dele.',logo=460,serif_sz=88,top=.17)]
REEL[4]=REEL[4].replace('Conteúdo informativo, não é assessoria jurídica.','Conteúdo informativo.')

async def main():
    sets={'noticia':(NOT,1350),'imigracao':(IMG,1350),'cultura':(REEL,1920)}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for k,(lst,h) in sets.items():
            pg=await b.new_page(viewport={'width':1080,'height':h})
            for i,htm in enumerate(lst):
                await pg.set_content(htm); await pg.wait_for_timeout(500)
                await pg.screenshot(path=OUT+f'{k}-{i+1}.png')
        await b.close()
asyncio.run(main())
