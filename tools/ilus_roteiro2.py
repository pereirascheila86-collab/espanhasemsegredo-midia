import asyncio,os
from playwright.async_api import async_playwright
OUT=os.environ.get("ART_OUT","2026-11-15/roteiro-2-ilustracoes")
G="#183A34";T="#B76E3C";GO="#D9B866";IV="#FAF5EA";SA="#EFE6D2";GR="#1F1F1F"
def star(cx,cy,r,f):
    import math
    p=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.4
        p.append(f"{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{f}"/>'
def person(x,y,s,body,head=GO):
    return f'<g transform="translate({x},{y}) scale({s})"><circle cx="0" cy="-70" r="22" fill="{head}"/><path d="M-34 40 Q-34 -40 0 -40 Q34 -40 34 40 Z" fill="{body}"/></g>'
# 1 capa: cartão + círculo de estrelas
def capa():
    s=f'<rect x="150" y="40" width="460" height="260" rx="26" fill="{IV}"/><rect x="150" y="40" width="460" height="64" rx="26" fill="{T}"/><rect x="150" y="80" width="460" height="24" fill="{T}"/>'
    s+=f'<circle cx="250" cy="195" r="46" fill="{GO}"/><path d="M190 280 Q190 232 250 232 Q310 232 310 280Z" fill="{G}"/>'
    for i,w in enumerate([210,170,130]): s+=f'<rect x="360" y="{150+i*38}" width="{w}" height="14" rx="7" fill="{G}" opacity="{0.9-0.2*i}"/>'
    import math
    cx,cy=740,170
    s+=f'<circle cx="{cx}" cy="{cy}" r="120" fill="#0F2A25"/>'
    for i in range(12):
        a=i*math.pi/6; s+=star(cx+84*math.cos(a),cy+84*math.sin(a),13,GO)
    s+=f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{GO}" stroke-width="5"/>'
    return s
def familiar():
    s=f'<path d="M20 270 H860" stroke="{G}" stroke-width="6" stroke-linecap="round"/>'
    s+=person(250,230,1.2,G)+person(340,240,0.9,T)+person(430,252,0.6,GO,T)
    s+=f'<path d="M520 270 V120 Q520 100 540 100 H800 Q820 100 820 120 V270Z" fill="{T}"/><rect x="560" y="140" width="80" height="70" rx="8" fill="{SA}"/><rect x="680" y="140" width="80" height="70" rx="8" fill="{SA}"/>'
    s+=star(670,60,22,GO)
    return s
def vinculos():
    s=f'<circle cx="370" cy="150" r="84" fill="none" stroke="{GO}" stroke-width="16"/><circle cx="510" cy="150" r="84" fill="none" stroke="{T}" stroke-width="16"/>'
    s+=f'<path d="M440 70 a84 84 0 0 1 0 160" fill="none" stroke="{IV}" stroke-width="0"/>'
    for x,y,c in [(150,70,IV),(150,230,GO),(730,70,GO),(730,230,IV)]: s+=f'<circle cx="{x}" cy="{y}" r="34" fill="{c}"/>'
    s+=f'<path d="M184 82 L290 130 M184 218 L290 170 M696 82 L590 130 M696 218 L590 170" stroke="{GO}" stroke-width="5" stroke-dasharray="4 12" stroke-linecap="round"/>'
    return s
def condicoes():
    s=f'<rect x="120" y="110" width="240" height="170" rx="22" fill="{T}"/><path d="M200 110 V86 Q200 70 216 70 H264 Q280 70 280 86 V110" fill="none" stroke="{G}" stroke-width="14"/><rect x="120" y="180" width="240" height="14" fill="{G}"/><rect x="226" y="168" width="28" height="38" rx="6" fill="{GO}"/>'
    s+=f'<path d="M520 60 L640 100 V190 Q640 250 520 292 Q400 250 400 190 V100 Z" fill="{G}"/><rect x="508" y="130" width="24" height="90" rx="4" fill="{IV}"/><rect x="475" y="163" width="90" height="24" rx="4" fill="{IV}"/>'
    s+=f'<rect x="700" y="90" width="170" height="190" rx="14" fill="{GO}"/><rect x="725" y="125" width="120" height="12" rx="6" fill="{G}"/><rect x="725" y="160" width="120" height="12" rx="6" fill="{G}"/><rect x="725" y="195" width="80" height="12" rx="6" fill="{G}"/>'
    return s
def onde():
    s=f'<rect x="80" y="270" width="720" height="10" rx="5" fill="{G}"/><path d="M160 270 V130 H640 V270Z" fill="{T}"/><path d="M130 130 L400 50 L670 130Z" fill="{G}"/>'
    for x in [200,300,500,560]: s+=f'<rect x="{x}" y="160" width="46" height="110" rx="6" fill="{SA}"/>'
    s+=f'<rect x="370" y="190" width="60" height="80" rx="6" fill="{G}"/>{star(400,100,16,GO)}'
    s+=f'<g transform="translate(700,40)"><rect width="150" height="150" rx="16" fill="{IV}"/><rect width="150" height="40" rx="16" fill="{GO}"/><rect y="24" width="150" height="16" fill="{GO}"/><text x="75" y="106" font-size="64" font-weight="700" font-family="Arial" fill="{G}" text-anchor="middle">3</text></g>'
    return s
def prazo():
    s=f'<rect x="100" y="80" width="330" height="200" rx="22" fill="{GO}"/><rect x="100" y="120" width="330" height="34" fill="{G}"/><circle cx="190" cy="212" r="30" fill="{T}"/><rect x="250" y="190" width="140" height="12" rx="6" fill="{G}"/><rect x="250" y="220" width="100" height="12" rx="6" fill="{G}"/>'
    s+=f'<path d="M560 60 H700 M560 280 H700 M575 60 Q575 150 630 170 Q575 190 575 280 M685 60 Q685 150 630 170 Q685 190 685 280" fill="none" stroke="{IV}" stroke-width="12" stroke-linecap="round"/><path d="M590 255 Q630 200 670 255Z" fill="{GO}"/>'
    s+=f'<g transform="translate(780,70)"><rect width="110" height="110" rx="14" fill="{T}"/><rect width="110" height="30" rx="14" fill="{IV}"/><text x="55" y="86" font-size="44" font-weight="700" font-family="Arial" fill="{IV}" text-anchor="middle">5</text></g><text x="835" y="235" font-size="30" font-weight="700" font-family="Arial" fill="{GO}" text-anchor="middle">anos</text>'
    return s
items={"capa":(capa,880,340),"familiar":(familiar,880,300),"vinculos":(vinculos,880,300),"condicoes":(condicoes,880,300),"onde":(onde,880,300),"prazo":(prazo,920,300)}
async def main():
    os.makedirs(OUT,exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); 
        for n,(f,w,h) in items.items():
            pg=await b.new_page(viewport={"width":w,"height":h},device_scale_factor=2)
            await pg.set_content(f'<html><body style="margin:0;background:transparent"><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{f()}</svg></body></html>')
            await pg.screenshot(path=f"{OUT}/ilustracao-{n}.png",omit_background=True)
        await b.close()
asyncio.run(main())
