"""Gera demonstrações GIF originais, distintas por exercício.

Ilustrações esquemáticas educativas: não constituem prescrição nem ensinam
sozinhas técnica biomecânica. Antes de comercializar, revisar com profissional.
"""
from pathlib import Path
from math import cos, sin, pi
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "gifs"
OUTPUT.mkdir(parents=True, exist_ok=True)
W, H = 360, 240
NAMES = [
    "Agachamento", "Flexão na parede", "Ponte de glúteos", "Marcha no lugar",
    "Prancha adaptada", "Elevação de panturrilha", "Remada com elástico",
    "Passada adaptada", "Polichinelo sem salto", "Mobilidade de ombros",
    "Abdominal curto", "Elevação lateral de perna", "Esteira",
    "Bicicleta ergométrica", "Leg press", "Cadeira extensora",
    "Cadeira flexora", "Puxada frontal", "Remada baixa",
    "Supino em máquina", "Rosca alternada", "Tríceps na polia",
    "Desenvolvimento na máquina", "Panturrilha na máquina"
]
GROUPS = [
    "PERNAS","PEITO","GLÚTEOS","CARDIO","ABDÔMEN","PERNAS",
    "COSTAS","PERNAS","CARDIO","MOBILIDADE","ABDÔMEN","GLÚTEOS",
    "CARDIO","CARDIO","PERNAS","PERNAS","PERNAS","COSTAS",
    "COSTAS","PEITO","BRAÇOS","BRAÇOS","OMBROS","PERNAS"
]

def p(x, y):
    return round(x), round(y)

def segment(draw, one, two, width, color, shadow=True):
    if shadow:
        draw.line([p(one[0]+2,one[1]+3), p(two[0]+2,two[1]+3)],
                  fill="#071827", width=width+5, joint="curve")
    draw.line([p(*one), p(*two)], fill=color, width=width, joint="curve")

def j_default():
    return {
        "head":(180,49),"shoulder":(180,87),"hip":(180,149),
        "el":(152,112),"hl":(137,146),"er":(208,112),"hr":(223,146),
        "kl":(157,186),"fl":(149,214),"kr":(203,186),"fr":(211,214)
    }

def pose(index, a, theta):
    j = j_default()
    # Posição real das articulações em dois extremos de cada repetição,
    # com amplitude suave: a sobe de 0 a 1 e volta a 0.
    if index == 1:  # agachamento: flexão simultânea quadril/joelhos
        j.update(head=(180,49+21*a), shoulder=(180,87+22*a),
                 hip=(180,145+27*a), kl=(148-10*a,185+6*a),
                 kr=(212+10*a,185+6*a), hl=(152,125-7*a),
                 hr=(208,125-7*a))
    elif index == 2:  # flexão na parede: vista lateral
        j.update(head=(225+22*a,66),shoulder=(230+20*a,100),
                 hip=(175+12*a,155),el=(271-7*a,112),
                 hl=(309,105),er=(272-7*a,120),hr=(309,117),
                 kl=(139,187),kr=(148,188),fl=(112,213),fr=(126,213))
    elif index == 3:  # ponte: corpo deitado, eleva quadril
        j.update(head=(85,173),shoulder=(117,183),hip=(207,178-54*a),
                 el=(119,201),hl=(164,205),er=(115,198),hr=(147,208),
                 kl=(250,145),kr=(257,153),fl=(303,215),fr=(312,215))
    elif index == 4:  # marcha alternando joelhos
        lift = sin(theta)
        j.update(kl=(155,184-32*max(lift,0)),fl=(153,214-57*max(lift,0)),
                 kr=(205,184-32*max(-lift,0)),fr=(207,214-57*max(-lift,0)),
                 hl=(137,144+19*lift),hr=(223,144-19*lift))
    elif index == 5:  # prancha de joelhos apoiados
        j.update(head=(266,119+2*a),shoulder=(239,143+2*a),hip=(162,142+2*a),
                 el=(260,177),hl=(284,211),er=(253,176),hr=(272,211),
                 kl=(108,193),kr=(114,197),fl=(89,213),fr=(95,213))
    elif index == 6:  # panturrilhas: ascensão vertical
        for key,(x,y) in list(j.items()):
            j[key]=(x,y-17*a if key not in ("fl","fr") else y-12*a)
    elif index == 7:  # remada com elástico sentada
        j.update(head=(160,76),shoulder=(161,108),hip=(163,170),
                 el=(202-33*a,136),hl=(257-66*a,138),
                 er=(205-33*a,147),hr=(259-66*a,148),
                 kl=(224,176),kr=(226,180),fl=(298,213),fr=(303,215))
    elif index == 8:  # passada em vista lateral
        j.update(head=(180,49+17*a),shoulder=(180,88+17*a),
                 hip=(180,149+18*a),kl=(233,174+10*a),
                 fl=(258,213),kr=(130,177+21*a),fr=(106,213))
    elif index == 9:  # polichinelo sem salto: passo lateral e braços
        j.update(el=(143-19*a,111-23*a),hl=(131-44*a,147-74*a),
                 er=(217+19*a,111-23*a),hr=(229+44*a,147-74*a),
                 kl=(155-13*a,186),fl=(150-37*a,214),
                 kr=(205+13*a,186),fr=(210+37*a,214))
    elif index == 10:  # mobilidade ombros
        j.update(el=(147-18*a,111-34*a),hl=(131-31*a,146-96*a),
                 er=(213+18*a,111-34*a),hr=(229+31*a,146-96*a))
    elif index == 11:  # abdominal curto no colchonete
        j.update(head=(105+35*a,181-52*a),
                 shoulder=(128+39*a,183-38*a),hip=(209,183),
                 el=(147+32*a,187-25*a),hl=(173+28*a,184-25*a),
                 er=(149+32*a,198-25*a),hr=(173+28*a,200-25*a),
                 kl=(256,152),kr=(257,158),fl=(306,211),fr=(314,212))
    elif index == 12:  # abdução lateral da perna
        j.update(kr=(211+32*a,188-9*a),fr=(217+68*a,213-25*a),
                 hl=(138,129),hr=(222,129))
    elif index == 13:  # esteira: caminhar em vista lateral
        wave=sin(theta)
        j.update(head=(183,52),shoulder=(182,89),hip=(179,149),
                 el=(161-12*wave,111),hl=(152-17*wave,143),
                 er=(203+11*wave,111),hr=(213+19*wave,143),
                 kl=(165-22*wave,182),fl=(158-38*wave,210),
                 kr=(200+22*wave,182),fr=(212+38*wave,210))
    elif index == 14:  # bicicleta estacionária
        j.update(head=(142,69),shoulder=(157,104),hip=(185,159),
                 el=(200,113),hl=(235,121),er=(199,120),hr=(238,128),
                 kl=(212+25*cos(theta),178+16*sin(theta)),
                 fl=(229+20*cos(theta),195+15*sin(theta)),
                 kr=(212-25*cos(theta),178-16*sin(theta)),
                 fr=(229-20*cos(theta),195-15*sin(theta)))
    elif index == 15:  # leg press reclinado
        j.update(head=(82,105),shoulder=(116,135),hip=(167,184),
                 el=(131,170),hl=(146,189),er=(135,158),hr=(160,178),
                 kl=(234-21*a,171+7*a),fl=(305,126),
                 kr=(237-21*a,178+7*a),fr=(312,138))
    elif index == 16:  # extensão de joelhos sentado
        j.update(head=(146,72),shoulder=(147,109),hip=(159,170),
                 el=(127,137),hl=(125,169),er=(177,138),hr=(190,164),
                 kl=(225,176),kr=(226,180),
                 fl=(229+57*a,215-56*a),fr=(234+57*a,215-53*a))
    elif index == 17:  # flexora, vista lateral em equipamento
        j.update(head=(92,118),shoulder=(124,144),hip=(197,146),
                 el=(154,175),hl=(177,208),er=(161,173),hr=(178,201),
                 kl=(261,157),kr=(261,163),
                 fl=(312-40*a,205-63*a),fr=(316-40*a,209-61*a))
    elif index == 18:  # puxada frontal com barra
        j.update(head=(180,72),shoulder=(180,107),hip=(181,170),
                 el=(133+15*a,80+32*a),hl=(110+33*a,52+69*a),
                 er=(227-15*a,80+32*a),hr=(250-33*a,52+69*a),
                 kl=(159,188),kr=(203,188),fl=(149,211),fr=(211,211))
    elif index == 19:  # remada baixa sentada
        j.update(head=(134,76),shoulder=(137,111),hip=(153,169),
                 el=(204-38*a,126),hl=(258-65*a,143),
                 er=(207-38*a,141),hr=(261-65*a,152),
                 kl=(216,181),kr=(222,184),fl=(293,210),fr=(306,210))
    elif index == 20:  # chest press na máquina
        j.update(head=(150,68),shoulder=(154,107),hip=(159,172),
                 el=(210+10*a,126),hl=(238+60*a,134),
                 er=(210+10*a,139),hr=(238+60*a,147),
                 kl=(174,191),kr=(190,193),fl=(174,215),fr=(215,215))
    elif index == 21:  # rosca alternada com halteres
        j.update(el=(149,119),hl=(130+13*a,165-67*a),
                 er=(209,119),hr=(231-13*a,165-67*(1-a)))
    elif index == 22:  # tríceps na polia, extensão
        j.update(el=(154,117),hl=(167,129+55*a),
                 er=(207,117),hr=(193,129+55*a))
    elif index == 23:  # desenvolvimento na máquina
        j.update(head=(180,58),shoulder=(180,99),hip=(180,168),
                 el=(138,127-34*a),hl=(125,143-88*a),
                 er=(222,127-34*a),hr=(235,143-88*a),
                 kl=(158,189),kr=(205,189),fl=(148,215),fr=(213,215))
    elif index == 24:  # panturrilha em máquina
        for key,(x,y) in list(j.items()):
            j[key]=(x,y-15*a if key not in ("fl","fr") else y-10*a)
        j.update(el=(147,112-15*a),hl=(124,106-15*a),
                 er=(213,112-15*a),hr=(236,106-15*a))
    return j

def equipment(draw, index, a, theta):
    steel="#6c96a7"; dim="#3a7085"; mint="#7be8cc"
    if index == 2:  # parede
        draw.rounded_rectangle((308,20,329,218),radius=3, fill="#46616e")
        for y in range(34,215,34):
            draw.line((311,y,326,y),fill="#69838d",width=2)
    elif index in (3,5,11):
        draw.rounded_rectangle((65,210,325,222),radius=7,fill="#336e83",outline=mint,width=2)
    elif index in (7,19):
        draw.rounded_rectangle((112,173,181,188),radius=4,fill=dim)
        draw.line((119,187,116,215),fill=steel,width=5)
        draw.line((165,187,171,215),fill=steel,width=5)
        draw.line((311,125,311,219),fill=steel,width=7)
    elif index == 13:
        draw.rounded_rectangle((70,207,303,223),radius=7,fill="#325267",outline=steel,width=2)
        draw.line((284,202,302,83),fill=steel,width=7)
        draw.rounded_rectangle((280,72,333,95),radius=6,fill=dim,outline=mint,width=2)
        draw.line((280,113,337,113),fill=steel,width=5)
    elif index == 14:
        draw.line([(140,207),(190,155),(236,208),(140,207)],fill=steel,width=7,joint="curve")
        draw.line((189,155,225,135),fill=steel,width=6)
        draw.line((218,132,251,132),fill=mint,width=5)
        draw.line((154,166,200,166),fill=mint,width=5)
        for x,y in ((139,208),(237,208)):
            draw.ellipse((x-15,y-15,x+15,y+15),outline=steel,width=4)
    elif index == 15:
        draw.polygon([(54,101),(69,86),(193,203),(178,213)],fill="#47637a")
        draw.line((310,100,326,159),fill=steel,width=9)
        draw.line((323,154,323,211),fill=steel,width=5)
    elif index in (16,17,18,20,23,24):
        draw.rounded_rectangle((109,170,204,181),radius=4,fill=dim)
        draw.line((116,178,105,216),fill=steel,width=6)
        draw.line((198,178,210,217),fill=steel,width=6)
    if index in (18,22,23):
        draw.line((180,10,180,65 if index==22 else 38),fill=steel,width=3)
        draw.rounded_rectangle((110,22,250,30),radius=3,fill=steel)
    if index == 24:
        draw.rounded_rectangle((129,76-15*a,231,91-15*a),radius=7,fill=dim,outline=steel,width=2)
        draw.line((116,39,116,213),fill=steel,width=4)
        draw.line((242,39,242,213),fill=steel,width=4)

def props_in_front(draw, index, j, a):
    steel="#82a6b5"; mint="#8ce9ce"
    if index in (7,19):
        hand=j["hl"]
        draw.line([p(*hand), (312,146)],fill=mint,width=4)
        draw.ellipse((303,136,321,155),fill="#466678")
    if index == 18:
        h1=j["hl"];h2=j["hr"]
        draw.line([p(*h1),p(*h2)],fill=steel,width=8)
    if index in (21,):
        for h in (j["hl"],j["hr"]):
            draw.line((h[0]-13,h[1]-5,h[0]+13,h[1]+5),fill=steel,width=8)
            for dx in (-13,13):
                draw.ellipse((h[0]+dx-5,h[1]-10,h[0]+dx+5,h[1]+10),fill="#5b7d95")
    if index == 22:
        draw.line((180,30,180,111),fill=steel,width=3)
        draw.line([p(*j["hl"]),(180,112),p(*j["hr"])],fill=mint,width=4)
    if index in (20,23):
        for h in (j["hl"],j["hr"]):
            draw.rounded_rectangle((h[0]-9,h[1]-5,h[0]+9,h[1]+5),radius=3,fill=steel)

def draw_body(draw, j):
    skin="#f6c4a2"; limb="#96ead3"; core="#4ecba7"
    sh=j["shoulder"];hip=j["hip"]
    for k,f in (("kl","fl"),("kr","fr")):
        segment(draw,hip,j[k],16,core)
        segment(draw,j[k],j[f],13,limb)
        shoe=j[f]
        draw.ellipse((shoe[0]-10,shoe[1]-3,shoe[0]+12,shoe[1]+5),fill="#d3f9f0")
    segment(draw,sh,hip,24,core)
    for e,h in (("el","hl"),("er","hr")):
        segment(draw,sh,j[e],13,limb)
        segment(draw,j[e],j[h],11,limb)
        x,y=j[h];draw.ellipse((x-6,y-6,x+6,y+6),fill=skin)
    x,y=j["head"]
    draw.ellipse((x-15,y-17,x+15,y+17),fill=skin,outline="#113149",width=2)
    draw.arc((x-15,y-17,x+15,y+17),182,345,fill="#254e5b",width=3)
    x,y=hip;draw.ellipse((x-7,y-7,x+7,y+7),fill="#b6ffee")

def render(index, frame, total=20):
    theta=2*pi*frame/total
    a=(1-cos(theta))/2
    img=Image.new("RGB",(W,H),"#0d2335")
    d=ImageDraw.Draw(img)
    for y in range(H):
        f=y/H
        col=(int(13+7*f),int(35+14*f),int(53+20*f))
        d.line((0,y,W,y),fill=col)
    d.ellipse((65,10,300,245),outline="#205668",width=2)
    d.ellipse((86,30,280,225),outline="#245061",width=2)
    d.line((40,220,320,220),fill="#3e6677",width=2)
    # Faixa e contador diferentes identificam exercícios mesmo sem texto na página.
    d.rounded_rectangle((10,9,64,31),radius=8,fill="#244a56")
    d.text((20,15),f"{index:02}",fill="#bbf5e4")
    equipment(d,index,a,theta)
    joints=pose(index,a,theta)
    draw_body(d,joints)
    props_in_front(d,index,joints,a)
    # Um discreto indicador de ciclo facilita reconhecer que o arquivo anima.
    x=112+int(136*frame/(total-1))
    d.rounded_rectangle((110,231,250,234),radius=2,fill="#426376")
    d.ellipse((x-3,228,x+3,236),fill="#b5ffe4")
    return img.convert("P",palette=Image.Palette.ADAPTIVE,colors=90)

def main():
    assert len(NAMES)==len(GROUPS)==24
    for n in range(1,len(NAMES)+1):
        frames=[render(n,i) for i in range(20)]
        path=OUTPUT/f"ex-{n:02}.gif"
        frames[0].save(path,save_all=True,append_images=frames[1:],
                       duration=90,loop=0,optimize=True,disposal=2)
        with Image.open(path) as gif:
            assert getattr(gif,"n_frames",1)>=12,f"Sem animação: {path}"
        print(f"{path.name}: {NAMES[n-1]}, {path.stat().st_size} bytes")
    print("24 GIFs distintos, com movimentos por exercício.")

if __name__=="__main__":
    main()
