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

# =====================================================================
# 27/10/2026 - noticia (eleicoes gerais 29/11), imigracao (praticas), cultura (flamenco, Reel)
# Sem numeracao nos slides. Icones e cenas novos, especificos do assunto.
# =====================================================================
def foot2(col, label=''):
    c=f'<span class=c style="color:{col}">{label}</span>' if label else ''
    return f'<div class=foot><div class=l><img src="{LOGO}"><span class=n style="color:{col}">Espanha Sem Segredo</span></div>{c}</div>'
def svg(inner, vb=200): return f'<svg width="100%" height="100%" viewBox="0 0 {vb} {vb}">{inner}</svg>'
import math

# ---------- icones noticia (eleicoes) ----------
def ic_decree(a,b):
    return svg(f'<rect x="40" y="26" width="120" height="148" rx="8" fill="{b}" stroke="{a}" stroke-width="6"/><rect x="28" y="18" width="144" height="22" rx="11" fill="{a}"/><rect x="28" y="160" width="144" height="22" rx="11" fill="{a}"/><path d="M62 70H138M62 88H138M62 106H108" stroke="{a}" stroke-width="6" stroke-linecap="round"/><circle cx="132" cy="134" r="20" fill="{a}"/><path d="M132 122L136 131L146 132L139 139L141 148L132 143L123 148L125 139L118 132L128 131Z" fill="{b}"/>')
def ic_cal29(a,b):
    return svg(f'<rect x="22" y="34" width="156" height="148" rx="16" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M22 50A16 16 0 0 1 38 34H162A16 16 0 0 1 178 50V74H22Z" fill="{a}"/><path d="M64 16V48M136 16V48" stroke="{a}" stroke-width="10" stroke-linecap="round"/><text x="100" y="150" text-anchor="middle" font-family="Lora" font-weight="700" font-size="76" fill="{a}">29</text><text x="100" y="64" text-anchor="middle" font-family="Inter" font-weight="800" font-size="20" letter-spacing="4" fill="{b}">NOV</text>')
def ic_urna(a,b):
    return svg(f'<rect x="30" y="92" width="140" height="92" rx="10" fill="{a}"/><rect x="62" y="104" width="76" height="12" rx="6" fill="{b}"/><path d="M58 28H142V92H58Z" fill="{b}" stroke="{a}" stroke-width="6" stroke-linejoin="round" transform="rotate(-5 100 60)"/><path d="M76 52H124M76 68H124" stroke="{a}" stroke-width="6" stroke-linecap="round" transform="rotate(-5 100 60)"/><path d="M84 40L92 48L108 30" stroke="{a}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="rotate(-5 100 60)" opacity="0"/><path d="M100 150L84 134H116Z" fill="{b}"/>')
def ic_worldenv(a,b):
    return svg(f'<circle cx="92" cy="92" r="70" fill="{a}"/><g fill="none" stroke="{b}" stroke-width="4"><ellipse cx="92" cy="92" rx="30" ry="70"/><path d="M22 92H162M32 56H152M32 128H152"/></g><rect x="86" y="120" width="98" height="64" rx="10" fill="{b}" stroke="{a}" stroke-width="7"/><path d="M92 128L135 160L178 128" fill="none" stroke="{a}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>')
def ic_mail(a,b):
    return svg(f'<rect x="20" y="52" width="150" height="104" rx="12" fill="{a}"/><path d="M26 62L95 118L164 62" fill="none" stroke="{b}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/><rect x="128" y="26" width="52" height="62" rx="6" fill="{b}" stroke="{a}" stroke-width="6" transform="rotate(8 154 57)"/><circle cx="154" cy="50" r="12" fill="{a}" transform="rotate(8 154 57)"/><path d="M138 74H170" stroke="{a}" stroke-width="5" stroke-linecap="round" transform="rotate(8 154 57)"/><path d="M30 176C54 164 70 188 94 176S130 168 158 178" fill="none" stroke="{a}" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 9"/>')

# ---------- layout A (noticia): bloco superior com titulo, circulo no encontro, bloco inferior com texto ----------
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

# ===================== NOTICIA: eleicoes gerais 29/11 =====================
def hemicycle(cx,cy):
    s=''
    cols=[GOLD,IV,TERRA,'#F3D79A',SAND]
    for ri,r in enumerate([250,312,374,436]):
        n=int(math.pi*r/36)
        for k in range(n):
            ang=math.pi+math.pi*(k+.5)/n
            x=cx+r*math.cos(ang); y=cy+r*math.sin(ang)
            sec=int((k+.5)/n*5)
            s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{cols[sec]}"/>'
    return f'<svg class=abs style="left:0;top:0" width="1080" height="1350">{s}</svg>'
def noticia_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:linear-gradient(180deg,{G} 0%,{G2} 100%)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:{GOLD}">Notícia · Espanha</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:800px;font-size:98px;line-height:1.05;font-weight:700;color:{IV}">A Espanha vai às urnas em <span style="color:{GOLD};font-style:italic">29 de novembro</span></div>
    {hemicycle(540,1010)}
    <div class="abs serif" style="left:0;right:0;top:830px;text-align:center;font-size:150px;font-weight:700;line-height:1;color:{IV}">29</div>
    <div class=abs style="left:0;right:0;top:985px;text-align:center;font-size:34px;letter-spacing:.3em;font-weight:700;color:{GOLD}">NOV · 2026</div>
    <div class=abs style="left:80px;right:80px;top:1060px;text-align:center;font-size:32px;line-height:1.35;color:{IV}">Eleições gerais para o Congresso dos Deputados e o Senado</div>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{INK}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,G,inner)

NOT=[noticia_cover(),
 contentA('Notícia · O decreto','O que foi decidido','O Real Decreto 806/2026, de 5 de outubro, dissolve o Congresso dos Deputados e o Senado e convoca eleições. Foi publicado no BOE em 6 de outubro.',ic_decree,'gI'),
 contentA('Notícia · A data','Dia 29 de novembro','As eleições gerais são em 29 de novembro de 2026. O período eleitoral vai de 6 de outubro a 29 de novembro, segundo o INE.',ic_cal29,'tI'),
 contentA('Notícia · Quem vota','Quem pode votar','Segundo a Junta Eleitoral Central, votam espanhóis maiores de idade inscritos no censo eleitoral. Para estrangeiros residentes, a Junta cita o voto em eleições municipais e europeias.',ic_urna,'iG',tw=620),
 contentA('Notícia · No exterior','Espanhóis no exterior','Quem está inscrito no CERA recebe a documentação e devolve o voto aos consulados entre 4 e 24 de novembro. A urna no consulado funciona de 21 a 26 de novembro (calendário do INE).',ic_worldenv,'sG',tw=620),
 contentA('Notícia · Voto por correio','Voto por correio','Na Espanha, o pedido vai de 6 de outubro a 19 de novembro. Para espanhóis temporariamente no exterior, o pedido vai só até 31 de outubro.',ic_mail,'tI',tw=600),
 closing2(1350,SAND,G,TERRA,'Fontes: INE (calendário eleitoral); Junta Eleitoral Central; Ministerio de Asuntos Exteriores (RD 806/2026).<br>Consulta em 27/10/2026.')]

# ===================== IMIGRACAO: praticas =====================
def ic_diploma(a,b):
    return svg(f'<path d="M100 22L184 60L100 98L16 60Z" fill="{a}"/><path d="M48 82V116C48 134 152 134 152 116V82L100 106Z" fill="{a}" opacity=".85"/><path d="M174 66V112" stroke="{a}" stroke-width="6" stroke-linecap="round"/><rect x="40" y="132" width="120" height="50" rx="8" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M58 150H142M58 164H112" stroke="{a}" stroke-width="5" stroke-linecap="round"/><circle cx="144" cy="164" r="12" fill="{a}"/>')
def ic_timeline(a,b):
    return svg(f'<rect x="20" y="30" width="160" height="140" rx="14" fill="{b}" stroke="{a}" stroke-width="6"/><path d="M20 62H180" stroke="{a}" stroke-width="6"/><g fill="{a}"><rect x="38" y="82" width="72" height="16" rx="8"/><rect x="62" y="108" width="100" height="16" rx="8"/><rect x="38" y="134" width="56" height="16" rx="8"/></g><path d="M62 18V42M138 18V42" stroke="{a}" stroke-width="8" stroke-linecap="round"/>')
def ic_building(a,b):
    return svg(f'<rect x="38" y="48" width="92" height="132" rx="6" fill="{a}"/><g fill="{b}"><rect x="52" y="64" width="22" height="20" rx="3"/><rect x="94" y="64" width="22" height="20" rx="3"/><rect x="52" y="98" width="22" height="20" rx="3"/><rect x="94" y="98" width="22" height="20" rx="3"/><rect x="72" y="140" width="24" height="40" rx="3"/></g><path d="M130 100H176V180H130Z" fill="{a}" opacity=".8"/><path d="M84 48V20L120 32L84 44" fill="{a}" stroke="{a}" stroke-width="4" stroke-linejoin="round"/><path d="M150 124H168M150 144H168" stroke="{b}" stroke-width="5" stroke-linecap="round"/>')
def ic_laptop(a,b):
    return svg(f'<rect x="38" y="36" width="124" height="88" rx="10" fill="{b}" stroke="{a}" stroke-width="7"/><path d="M14 148H186L172 164H28Z" fill="{a}"/><path d="M62 70H104M62 90H138" stroke="{a}" stroke-width="6" stroke-linecap="round"/><circle cx="140" cy="70" r="12" fill="{a}"/><path d="M134 70L139 75L148 65" stroke="{b}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
def ic_finger(a,b):
    arcs=''.join(f'<path d="M{100-r} {150-r*.2} A{r} {r*1.15} 0 0 1 {100+r} {150-r*.2}" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round" stroke-dasharray="{60 if r%2 else 200} 8"/>' for r in (18,34,50,66))
    return svg(f'<circle cx="100" cy="100" r="88" fill="{a}" opacity=".18"/><g transform="translate(0 -14)">{arcs}</g><path d="M100 150V92" stroke="{a}" stroke-width="8" stroke-linecap="round"/><path d="M152 150A52 52 0 0 1 100 178" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round"/><path d="M146 138L154 154L168 142" fill="none" stroke="{a}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')

def imig_cover():
    inner=f'''<div class=abs style="left:0;top:0;width:1080px;height:1350px;background:{TERRA}"></div>
    <div class=abs style="left:-260px;top:560px;width:1600px;height:1600px;border-radius:50%;background:{IV}"></div>
    <div class=abs style="left:-260px;top:560px;width:1600px;height:1600px;border-radius:50%;border:4px solid {GOLD};transform:scale(.97)"></div>
    {bracket(GOLD)}
    <div class=abs style="left:80px;top:100px"><span class=kick style="color:#F3D79A">Imigração · Prácticas</span></div>
    <div class="abs serif" style="left:80px;top:170px;width:880px;font-size:96px;line-height:1.05;font-weight:700;color:{IV}">Práticas (<i>prácticas</i>) na Espanha: quem pode e <span style="color:#F3D79A;font-style:italic">como?</span></div>
    <div class=abs style="left:90px;top:740px;width:380px;height:380px;transform:rotate(-7deg)">{ic_diploma(G,SAND)}</div>
    <div class=abs style="left:610px;top:750px;width:340px;height:340px;transform:rotate(6deg)">{svg(f'<rect x="20" y="62" width="160" height="112" rx="14" fill="{G}"/><path d="M70 62V46C70 38 76 32 84 32H116C124 32 130 38 130 46V62" fill="none" stroke="{G}" stroke-width="9"/><path d="M20 112H180" stroke="{GOLD}" stroke-width="5"/><rect x="88" y="102" width="24" height="22" rx="5" fill="{GOLD}"/>')}</div>
    <svg class=abs style="left:430px;top:860px" width="220" height="80" viewBox="0 0 220 80"><path d="M10 40H190M156 12L192 40L156 68" fill="none" stroke="{TERRA}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div class=abs style="left:0;right:0;bottom:0;height:170px;background:{G}"></div>
    <div class=foot style="bottom:50px"><div class=l><img src="{LOGO}"><span class=n style="color:{GOLD}">Espanha Sem Segredo</span></div><span class=c style="color:{GOLD}">DESLIZE  →</span></div>'''
    return page(1350,TERRA,inner)

IMG=[imig_cover(),
 contentB('Imigração · Para quem é','Para quem é','Estudantes estrangeiros que obtiveram título de ensino superior nos 2 anos anteriores ao pedido, ou que cursam estudos que levem a um.',ic_diploma,'ivory'),
 contentB('Imigração · Duração','Quanto dura','Com convênio de acolhimento, a mesma duração do convênio, no máximo 12 meses. Com contrato de trabalho em práticas, a prevista no contrato.',ic_timeline,'green'),
 contentB('Imigração · Condições','Condições das práticas','Devem ser na mesma área acadêmica e no mesmo nível do título, dentro de convênio de práticas ou contrato em práticas, em entidade pública ou privada.',ic_building,'sand',ts=64),
 contentB('Imigração · Quem pede','Quem faz o pedido','A entidade de acolhimento pede, exclusivamente por via telemática, na sede eletrônica Mercurio. A ficha oficial prevê resposta em até 30 dias.',ic_laptop,'terra'),
 contentB('Imigração · Depois','Depois da autorização','A TIE deve ser pedida na polícia em até 1 mês. Com convênio, a prorrogação é possível uma só vez, e o total não passa de 2 anos.',ic_finger,'ivory',ts=66),
 closing2(1350,G,IV,GOLD,'Fonte: Ministerio de Inclusión, Seguridad Social y Migraciones (Hoja 21).<br>Consulta em 23/10/2026.')]

# ===================== CULTURA: flamenco (Reel 1080x1920) =====================
def guitar(x,y,s,rot):
    # viewBox 300x760: corpo + braco
    return f'''<svg class=abs style="left:{x}px;top:{y}px;overflow:visible" width="{300*s}" height="{760*s}" viewBox="0 0 300 760"><g transform="rotate({rot} 150 380)">
    <rect x="132" y="20" width="36" height="330" rx="6" fill="{INK}"/>
    <path d="M124 -40H176L180 40H120Z" fill="{G}" stroke="{GOLD}" stroke-width="4"/>
    <g fill="{GOLD}"><circle cx="112" cy="-6" r="7"/><circle cx="112" cy="18" r="7"/><circle cx="188" cy="-6" r="7"/><circle cx="188" cy="18" r="7"/></g>
    <g stroke="{GOLD}" stroke-width="2" opacity=".8"><path d="M132 60H168M132 100H168M132 140H168M132 180H168M132 220H168M132 260H168M132 300H168"/></g>
    <path d="M150 330C80 330 60 380 90 420C40 450 20 530 50 600C80 690 220 690 250 600C280 530 260 450 210 420C240 380 220 330 150 330Z" fill="{TERRA}" stroke="{G}" stroke-width="6"/>
    <path d="M150 346C96 346 82 384 106 416C64 446 48 520 72 584C98 664 202 664 228 584C252 520 236 446 194 416C218 384 204 346 150 346Z" fill="none" stroke="{GOLD}" stroke-width="3" opacity=".8"/>
    <circle cx="150" cy="470" r="44" fill="{G}"/><circle cx="150" cy="470" r="54" fill="none" stroke="{GOLD}" stroke-width="6"/><circle cx="150" cy="470" r="62" fill="none" stroke="{IV}" stroke-width="3" stroke-dasharray="6 6"/>
    <rect x="106" y="610" width="88" height="16" rx="5" fill="{INK}"/>
    <g stroke="{IV}" stroke-width="1.6" opacity=".9"><path d="M140 40V612M146 40V612M154 40V612M160 40V612"/></g></g></svg>'''
def burst(cx,cy,r1,r2,n,col,w=8):
    s=''
    for k in range(n):
        a=2*math.pi*k/n
        s+=f'<path d="M{cx+r1*math.cos(a):.1f} {cy+r1*math.sin(a):.1f}L{cx+r2*math.cos(a):.1f} {cy+r2*math.sin(a):.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
    return s
def horseshoe(cx,top,w,h,col,sw=10,fill='none'):
    r=w/2
    return f'<path d="M{cx-r*.86} {top+h} V{top+r*1.25} A{r} {r} 0 1 1 {cx+r*.86} {top+r*1.25} V{top+h}" fill="{fill}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'

def reel_scene(bg,kick_col,inner,fgfoot,kcol=None):
    return page(1920,bg,f'''{bracket(kick_col)}
    <div class=abs style="left:80px;top:110px"><span class=kick style="color:{kick_col}">Você sabia? | Espanha</span></div>
    {inner}
    <div class=foot style="bottom:90px"><div class=l><img src="{LOGO}"><span class=n style="color:{fgfoot}">Espanha Sem Segredo</span></div></div>''')

# tela 1: marfim, violao grande
c1=f'''<div class=abs style="left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(90deg,rgba(15,61,58,.05) 0 3px,transparent 3px 54px)"></div>
<div class="abs serif" style="left:80px;top:240px;width:920px;font-size:128px;line-height:1.04;font-weight:700;color:{G}">Flamenco é <span style="color:{TERRA};font-style:italic">Patrimônio</span> da Humanidade</div>
<div class=abs style="left:84px;top:760px;font-size:44px;letter-spacing:.06em;font-weight:600;color:{INK}">segundo a UNESCO</div>
<div class=abs style="left:84px;top:830px;width:140px;height:6px;background:{GOLD}"></div>
<svg class=abs style="left:0;top:0" width="1080" height="1920"><circle cx="560" cy="1290" r="360" fill="{SAND}"/><g>{burst(560,1290,400,450,28,GOLD,6)}</g></svg>
{guitar(300,700,1.45,18)}'''
# tela 2: verde, 2010 dentro de arco de ferradura
c2=f'''<svg class=abs style="left:0;top:0" width="1080" height="1920">{horseshoe(540,320,780,1000,GOLD,12,G2)}{horseshoe(540,380,660,940,GOLD,3)}</svg>
<div class="abs serif" style="left:0;right:0;top:600px;text-align:center;font-size:280px;line-height:1;font-weight:700;color:#F3D79A;letter-spacing:-.02em">2010</div>
<div class=abs style="left:0;right:0;top:940px;text-align:center;font-size:30px;letter-spacing:.14em;font-weight:700;color:{GOLD}">INSCRIÇÃO NA UNESCO</div>
<div class=abs style="left:130px;right:130px;top:1380px;text-align:center;font-size:48px;line-height:1.4;color:{IV}">Ano em que o flamenco entrou na lista do Patrimônio Cultural Imaterial.</div>'''
# tela 3: areia, venn canto/danca/musica + coracao Andaluzia
def venn():
    cs=[(370,800,'CANTO',TERRA),(710,800,'DANÇA',G),(540,1090,'MÚSICA',GOLD)]
    s=''
    for x,y,t,c in cs: s+=f'<circle cx="{x}" cy="{y}" r="250" fill="{c}" opacity=".72"/>'
    for x,y,t,c in cs:
        dx=-80 if x<500 else (80 if x>600 else 0); dy=-60 if y<1000 else 110
        s+=f'<text x="{x+dx}" y="{y+dy}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="40" letter-spacing="4" fill="{IV if c!=GOLD else INK}">{t}</text>'
    s+=f'<text x="540" y="960" text-anchor="middle" font-family="Lora" font-style="italic" font-weight="700" font-size="46" fill="{IV}">flamenco</text>'
    return f'<svg class=abs style="left:0;top:0" width="1080" height="1920">{s}</svg>'
c3=f'''<div class="abs serif" style="left:80px;top:230px;width:920px;font-size:92px;line-height:1.06;font-weight:700;color:{G}">Canto, dança e música em uma só <span style="color:{TERRA};font-style:italic">arte</span></div>
{venn()}
<svg class=abs style="left:80px;top:1480px" width="160" height="150" viewBox="0 0 200 200"><path d="M100 172C45 130 24 98 24 68C24 42 44 26 66 26C82 26 94 35 100 48C106 35 118 26 134 26C156 26 176 42 176 68C176 98 155 130 100 172Z" fill="{TERRA}"/></svg>
<div class=abs style="left:270px;top:1480px;width:700px;font-size:46px;line-height:1.4;color:{INK}">Segundo a UNESCO, a <b>Andaluzia</b> é o coração do flamenco.</div>'''
# tela 4: terracota, palmas
def palmas():
    return f'''<svg class=abs style="left:0;top:0" width="1080" height="1920">
    <g stroke="{GOLD}" fill="none">{burst(540,1130,190,300,20,GOLD,9)}</g>
    <g transform="translate(540 1130)"><g transform="rotate(-28)"><rect x="-290" y="-70" width="270" height="140" rx="70" fill="{SAND}"/><g stroke="{TERRA}" stroke-width="5" stroke-linecap="round"><path d="M-130 -40L-60 -40M-140 -10L-50 -10M-130 20L-60 20"/></g></g>
    <g transform="rotate(28)"><rect x="20" y="-70" width="270" height="140" rx="70" fill="{IV}"/><g stroke="{TERRA}" stroke-width="5" stroke-linecap="round"><path d="M60 -40L130 -40M50 -10L140 -10M60 20L130 20"/></g></g></g>
    <g fill="{GOLD}"><circle cx="300" cy="840" r="14"/><circle cx="780" cy="840" r="14"/><circle cx="540" cy="780" r="18"/></g></svg>'''
c4=f'''<div class=abs style="left:80px;top:250px;font-size:44px;letter-spacing:.14em;font-weight:700;color:#F3D79A">QUEM AJUDOU A DESENVOLVER?</div>
<div class="abs serif" style="left:80px;top:340px;width:920px;font-size:150px;line-height:1.0;font-weight:700;font-style:italic;color:{IV}">Comunidade gitana</div>
{palmas()}
<div class=abs style="left:80px;top:1500px;width:920px;font-size:46px;line-height:1.4;color:{IV}">Segundo a UNESCO, teve papel importante no flamenco.</div>'''
REEL=[reel_scene(IV,TERRA,c1,G),reel_scene(G,GOLD,c2,GOLD),reel_scene(SAND,TERRA,c3,G),reel_scene(TERRA,'#F3D79A',c4,IV),
 closing2(1920,G,IV,GOLD,'Fonte: UNESCO, Patrimônio Cultural Imaterial (Flamenco, 2010).<br>Consulta em 23/10/2026.',cta='Já viu flamenco ao vivo? Comente SIM ou NÃO.',logo=460,serif_sz=88,top=.17)]
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
