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

# ===================== NOTICIA: cita automatica da TIE =====================
def noticia_cover():
    card=f'<div class=abs style="left:90px;top:640px;width:560px;height:360px;transform:rotate(-8deg)">{ic_card(G,GOLD)}</div>'
    cal=f'<div class=abs style="left:560px;top:560px;width:380px;height:380px;border-radius:50%;background:{TERRA}"></div><div class=abs style="left:610px;top:610px;width:280px;height:280px"><svg width="100%" height="100%" viewBox="0 0 200 200"><rect x="22" y="36" width="156" height="142" rx="16" fill="{IV}"/><path d="M22 52A16 16 0 0 1 38 36H162A16 16 0 0 1 178 52V76H22Z" fill="{G}"/><path d="M62 18V52M138 18V52" stroke="{G}" stroke-width="10" stroke-linecap="round"/><path d="M110 88L78 134H102L92 168L126 118H104Z" fill="{TERRA}"/></svg></div>'
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{IV} 0%,{SAND} 100%)"></div>
    <div class=abs style="left:-120px;top:420px;width:620px;height:620px;border-radius:50%;background:{GOLD};opacity:.3"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{TERRA}">Notícia · Imigração</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:100px;line-height:1.05;font-weight:700;color:{G}">Polícia testa <span style="color:{TERRA};font-style:italic">cita automática</span> para a TIE</div>
    {card}{cal}
    <div class=abs style="left:80px;top:1060px;width:900px;font-size:34px;line-height:1.35;color:{INK}">Piloto de agendamento da coleta de impressões digitais, a partir de outubro de 2026.</div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,IV,inner)

NOT=[noticia_cover(),
 content2('N','Notícia · O que é','O que é o piloto','Atribuição automática de cita para a coleta de impressões digitais e a emissão da TIE. Segundo aviso da Oficina de Extranjería de Málaga, o sistema começou em outubro de 2026.',ic_card,'ivory'),
 content2('N','Notícia · Como funciona','Como funciona','Com a resolução favorável, o sistema solicita a cita. A Polícia Nacional atribui o horário na delegacia mais próxima da residência e avisa por SMS e/ou e-mail.',ic_sms,'green'),
 content2('N','Notícia · Alcance','Ainda é um piloto','No início, só parte dos processos e algumas províncias participam. O agendamento tradicional segue disponível. Confira o aviso da sua Oficina de Extranjería.',ic_pin,'sand'),
 content2('N','Notícia · Exceções','O que fica de fora','Autorizações concedidas sob condição, como a entrada na Espanha ou a alta na Seguridade Social, ficam fora. Nesses casos, a cita é pedida do modo tradicional, depois de cumprida a condição.',ic_hourglass,'terra'),
 content2('N','Notícia · Se algo falhar','Cancelou ou faltou?','Se cancelar a cita, o sistema pode reagendar quando houver vaga. Se faltar sem cancelar, é preciso pedir nova cita pela sede eletrônica.',ic_refresh,'ivory'),
 closing2(1350,G,IV,GOLD,'Fontes: Oficina de Extranjería de Málaga (aviso) e ARC Legal.<br>Consulta em 26/10/2026.')]

# ===================== IMIGRACAO: voluntariado =====================
def imig_cover():
    hands=f'<div class=abs style="left:290px;top:700px;width:460px;height:460px"><svg width="100%" height="100%" viewBox="0 0 200 200"><circle cx="100" cy="100" r="92" fill="{G2}"/><circle cx="100" cy="100" r="92" fill="none" stroke="{GOLD}" stroke-width="2.5" stroke-dasharray="3 7"/></svg></div><div class=abs style="left:350px;top:760px;width:340px;height:340px">{ic_vol(GOLD,G)}</div>'
    ring=f'<div class=abs style="left:70px;top:900px;width:230px;height:250px;border-radius:50%;background:{TERRA};color:{IV};display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(-8deg);border:4px solid {GOLD}"><div class=serif style="font-size:84px;font-weight:700;line-height:1">90+</div><div style="font-size:26px;letter-spacing:.18em;font-weight:700">DIAS</div></div>'
    ring2=f'<div class=abs style="left:790px;top:740px;width:220px;height:220px;border-radius:50%;background:{IV};color:{G};display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(7deg)"><div class=serif style="font-size:84px;font-weight:700;line-height:1">1</div><div style="font-size:26px;letter-spacing:.18em;font-weight:700">ANO MÁX.</div></div>'
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:radial-gradient(circle at 20% 90%,{G2} 0,{G} 62%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Imigração · Estância</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:900px;font-size:82px;line-height:1.06;font-weight:700;color:{IV}">Voluntariado na Espanha: como funciona a <span style="color:{GOLD};font-style:italic">autorização</span> de estância?</div>
    {hands}{ring}{ring2}
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{INK}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,G,inner)

IMG=[imig_cover(),
 content2('I','Imigração · Para quem é','Para quem é','Quem vai fazer voluntariado em programa de interesse geral, sem fins lucrativos, por mais de 90 dias. A estância dura o mesmo que o voluntariado, no máximo 1 ano.',ic_vol,'ivory'),
 content2('I','Imigração · Convênio','O convênio','É preciso ter sido admitido em um serviço de voluntariado, com convênio assinado com a entidade do programa, que deve estar legalmente constituída e inscrita em registro competente.',ic_agree,'terra'),
 content2('I','Imigração · Atividade','Sem remuneração','A atividade não é remunerada. Só pode haver reembolso de gastos e dinheiro de bolso. O convênio descreve funções, horas, alojamento e manutenção.',ic_nomoney,'ivory'),
 content2('I','Imigração · Outras condições','Outras condições','Seguro de saúde com seguradora autorizada na Espanha, meios econômicos para a estância e o regresso, e pagamento da taxa. Acima de 6 meses, maiores de idade apresentam antecedentes criminais.',ic_health,'green'),
 content2('I','Imigração · Onde pedir','Onde pedir','Pessoalmente, na Missão Diplomática ou Consulado da Espanha da sua área de residência. A ficha oficial prevê resposta em 1 mês. Acima de 6 meses, é preciso pedir a TIE na polícia.',ic_passport,'sand'),
 closing2(1350,IV,G,TERRA,'Fonte: Ministerio de Inclusión, Seguridad Social y Migraciones.<br>Consulta em 23/10/2026.')]

# ===================== CULTURA: pan con tomate (Reel 1080x1920) =====================
def tomato(cx,cy,r,half=False,rot=0,leaf=G2):
    s=f'<g transform="translate({cx} {cy}) rotate({rot})">'
    s+=f'<circle r="{r}" fill="{TERRA}"/><circle r="{r*.84}" fill="{TERRA}" stroke="#F3D79A" stroke-width="3" opacity=".95"/>'
    if half:
        for k in range(5):
            s+=f'<g transform="rotate({k*72})"><path d="M0 {-r*.1} C{r*.22} {-r*.25} {r*.22} {-r*.58} 0 {-r*.68} C{-r*.22} {-r*.58} {-r*.22} {-r*.25} 0 {-r*.1}Z" fill="{SAND}" opacity=".9"/><circle cx="0" cy="{-r*.42}" r="{r*.05}" fill="{GOLD}"/></g>'
        s+=f'<circle r="{r*.1}" fill="{SAND}"/>'
    else:
        s+=f'<ellipse cx="{-r*.35}" cy="{-r*.4}" rx="{r*.18}" ry="{r*.1}" fill="{IV}" opacity=".45" transform="rotate(-35 {-r*.35} {-r*.4})"/>'
        for k in range(5):
            s+=f'<path transform="rotate({k*72})" d="M0 0 C{r*.1} {-r*.2} {r*.2} {-r*.3} {r*.05} {-r*.42} C0 {-r*.3} 0 {-r*.15} 0 0Z" fill="{leaf}"/>'
    return s+'</g>'

def bread_slice(x,y,w,rub=True,drizzle=True,hl=GOLD):
    # viewBox 600x560
    p='M90 210C40 130 120 40 225 52C265 20 345 20 385 52C490 40 565 130 515 210C545 238 535 270 512 280V470C512 505 490 526 458 526H142C110 526 88 505 88 470V280C65 270 55 238 90 210Z'
    q='M118 218C84 160 146 82 230 92C268 66 342 66 380 92C464 82 526 160 484 218C506 238 500 258 484 262V462C484 482 472 494 452 494H148C128 494 116 482 116 462V262C100 258 94 238 118 218Z'
    s=f'<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{w}" height="{w*560/600}" viewBox="0 0 600 560"><path d="{p}" fill="{hl}"/><path d="{q}" fill="{SAND}"/>'
    if rub:
        s+=f'<g opacity=".85" fill="{TERRA}"><ellipse cx="230" cy="190" rx="86" ry="46" transform="rotate(-12 230 190)"/><ellipse cx="380" cy="270" rx="100" ry="52" transform="rotate(10 380 270)"/><ellipse cx="240" cy="350" rx="90" ry="46" transform="rotate(-6 240 350)"/><ellipse cx="390" cy="410" rx="78" ry="36"/></g>'
        s+=''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="7" ry="4" fill="{GOLD}" transform="rotate({r} {cx} {cy})"/>' for cx,cy,r in [(200,180,20),(260,205,-30),(360,255,15),(420,285,-20),(220,345,40),(280,360,-10),(380,400,25),(410,425,5)])
    if drizzle:
        s+=f'<path d="M130 300C190 270 220 330 280 296C340 262 380 330 450 296" fill="none" stroke="#F3D79A" stroke-width="14" stroke-linecap="round" opacity=".9"/>'
    return s+'</svg>'

def oil_bottle(x,y,h):
    w=h*.38
    return f'<svg class=abs style="left:{x}px;top:{y}px" width="{w}" height="{h}" viewBox="0 0 76 200"><path d="M28 4H48V30C48 44 70 56 70 82V184C70 192 64 196 56 196H20C12 196 6 192 6 184V82C6 56 28 44 28 30Z" fill="{G2}" stroke="{GOLD}" stroke-width="3"/><rect x="12" y="104" width="52" height="60" rx="6" fill="{IV}"/><circle cx="38" cy="126" r="9" fill="{GOLD}"/><path d="M20 148H56" stroke="{G}" stroke-width="4" stroke-linecap="round"/><rect x="28" y="0" width="20" height="10" rx="3" fill="{GOLD}"/></svg>'

def reel_scene(n,bg,kick_col,inner,fgfoot):
    return page(1920,bg,f'''{bracket(kick_col)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{kick_col}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{fgfoot}">Espanha Sem Segredo</span></div></div>''')

# tela 1: terracota
t1=f'''<div class=abs style="left:-200px;top:1000px;width:900px;height:900px;border-radius:50%;background:#C9684A;opacity:.55"></div>
<div class="abs serif" style="left:80px;top:240px;width:920px;font-size:112px;line-height:1.05;font-weight:700;color:{IV}">Pan con tomate tem <span style="color:#F3D79A;font-style:italic">outro nome</span> na Catalunha</div>
{bread_slice(180,820,720)}
<svg class=abs style="left:0;top:0" width="1080" height="1920">{tomato(180,1480,120,half=True,rot=20)}{tomato(900,1440,100,half=False)}</svg>
{oil_bottle(860,880,330)}'''
# tela 2: marfim
t2=f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(0deg,rgba(15,61,58,.04) 0 2px,transparent 2px 46px)"></div>
<div class=abs style="left:80px;top:260px;font-size:34px;letter-spacing:.2em;font-weight:700;color:{TERRA}">NA CATALUNHA, ASSIM SE CHAMA</div>
<div class="abs serif" style="left:60px;top:340px;width:960px;font-size:176px;line-height:1.0;font-weight:700;font-style:italic;color:{G}">pa amb<br>tomàquet</div>
<div class=abs style="left:80px;top:760px;width:140px;height:6px;background:{GOLD}"></div>
<svg class=abs style="left:0;top:0" width="1080" height="1920">{tomato(540,1180,250,half=True,rot=10)}<g transform="translate(790 1420) rotate(-24)"><rect x="0" y="0" width="300" height="46" rx="10" fill="{G}"/><rect x="-170" y="8" width="190" height="30" rx="14" fill="{GOLD}"/><path d="M300 0L420 46H300Z" fill="{G2}"/></g></svg>
<div class=abs style="left:80px;top:1650px;width:920px;font-size:40px;line-height:1.4;color:{INK}">Segundo a Generalitat de Catalunya.</div>'''
# tela 3: verde
vine=f'''<svg class=abs style="left:90px;top:0" width="1080" height="1920"><path d="M820 1760C760 1500 560 1400 600 1180C630 1020 780 980 760 820" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/>
{''.join(f'<path transform="translate({x} {y}) rotate({r})" d="M0 0C60 -70 150 -60 190 0C130 50 50 50 0 0Z" fill="{G2}" stroke="{GOLD}" stroke-width="3"/>' for x,y,r in [(600,1180,-150),(640,1330,-20),(760,1000,-170),(700,1560,-150),(770,880,-40)])}
{tomato(480,1360,92)}{tomato(840,1180,84,rot=30)}{tomato(520,1010,70,rot=-40)}{tomato(900,1560,76,rot=15)}</svg>'''
t3=f'''<div class="abs serif" style="left:80px;top:250px;font-size:210px;line-height:1.0;font-weight:700;color:#F3D79A">Século<br>XIX</div>
<div class=abs style="left:80px;top:700px;width:400px;font-size:44px;line-height:1.42;color:{IV}">Primeiras referências do prato. Segundo o escritor Nèstor Luján, surgiu no campo, com muito tomate, para amolecer o pão duro.</div>
{vine}
<svg class=abs style="left:80px;top:1260px;opacity:.95" width="300" height="220" viewBox="0 0 300 220"><path d="M20 160C20 100 90 70 160 70C230 70 290 110 280 160C270 200 200 210 150 205C90 200 20 200 20 160Z" fill="{SAND}"/><path d="M40 150C80 130 130 160 170 140C210 120 240 140 266 150" stroke="{GOLD}" stroke-width="5" fill="none" opacity=".8"/><path d="M60 118C90 100 130 96 170 98" stroke="{G}" stroke-width="4" fill="none" opacity=".4"/></svg>'''
# tela 4: areia - bifurcacao de versoes
t4=f'''<div class="abs serif" style="left:80px;top:250px;width:920px;font-size:128px;line-height:1.04;font-weight:700;color:{G}">Qual é a <span style="color:{TERRA};font-style:italic">origem</span> do prato?</div>
<svg class=abs style="left:0;top:0" width="1080" height="1920"><rect x="520" y="1000" width="40" height="640" rx="10" fill="{G}"/><circle cx="540" cy="990" r="18" fill="{GOLD}"/>
<path d="M200 1090H610L680 1140L610 1190H200Z" fill="{G}"/><text x="240" y="1156" font-family="Inter" font-weight="800" font-size="42" fill="{IV}" letter-spacing="3">VERSÃO LUJÁN</text>
<path d="M920 1300H430L360 1350L430 1400H920Z" fill="{TERRA}"/><text x="450" y="1364" font-family="Inter" font-weight="800" font-size="38" fill="{IV}" letter-spacing="3">OUTRAS VERSÕES</text>
<text x="900" y="880" text-anchor="middle" font-family="Lora" font-weight="700" font-size="360" fill="{GOLD}" opacity=".85">?</text>
<ellipse cx="540" cy="1650" rx="260" ry="30" fill="{G}" opacity=".18"/></svg>
<div class=abs style="left:80px;top:700px;width:760px;font-size:46px;line-height:1.42;color:{INK}">Há mais de uma versão. Esta é a que a fonte oficial registra, atribuída a Luján.</div>'''

REEL=[reel_scene(1,TERRA,'#F3D79A',t1,IV),reel_scene(2,IV,TERRA,t2,G),reel_scene(3,G,GOLD,t3,GOLD),reel_scene(4,SAND,TERRA,t4,G),
 closing2(1920,G,IV,GOLD,'Fonte: Generalitat de Catalunya (Patrimoni Gencat).<br>Consulta em 23/10/2026.',cta='Com ou sem azeite? Comente.',logo=460,serif_sz=88,top=.17)]
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
