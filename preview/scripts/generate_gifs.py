"""Gera 24 GIFs esquemáticos originais para a prévia TreinoX.
Não usar como demonstração biomecânica nem orientação profissional.
"""
from pathlib import Path
from math import sin, pi
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "gifs"
OUT.mkdir(parents=True, exist_ok=True)
CATEGORIES = ["pernas","peito","gluteos","cardio","abdomen","pernas","costas","pernas","cardio","mobilidade","abdomen","gluteos","cardio","cardio","pernas","pernas","pernas","costas","costas","peito","bracos","bracos","ombros","pernas"]
assert len(CATEGORIES) == 24
WIDTH, HEIGHT = 280, 195

def draw_frame(category, t):
    image = Image.new("RGB",(WIDTH,HEIGHT),"#132c42")
    d = ImageDraw.Draw(image)
    d.ellipse((30,10,250,230),outline="#2e6b6b",width=2)
    d.ellipse((48,27,232,211),outline="#254c59",width=2)
    d.line((28,171,252,171),fill="#4b6975",width=3)
    wave = sin(2*pi*t/16)
    squat = 13*(wave+1)/2 if category in ("pernas","gluteos") else 0
    sway = 16*wave if category in ("cardio","mobilidade") else 0
    arm = 13*wave if category in ("bracos","ombros","costas","peito") else 0
    head_y = 41 + squat
    cx = 140 + (sway if category=="cardio" else 0)
    d.ellipse((cx-15,head_y-15,cx+15,head_y+15),fill="#ffd4ae",outline="#0a162a",width=2)
    shoulders=(cx,head_y+18); hip=(cx,head_y+75)
    d.line((*shoulders,*hip),fill="#83ebc9",width=17)
    # Braços articulares animados
    l_el=(cx-24,head_y+43+arm); l_hand=(cx-39,head_y+67+arm)
    r_el=(cx+24,head_y+43-arm); r_hand=(cx+39,head_y+67-arm)
    for elbow,hand in ((l_el,l_hand),(r_el,r_hand)):
        d.line((*shoulders,*elbow),fill="#a8f5dc",width=10)
        d.line((*elbow,*hand),fill="#a8f5dc",width=9)
        d.ellipse((hand[0]-5,hand[1]-5,hand[0]+5,hand[1]+5),fill="#ffd4ae")
    # Pernas alteram amplitude conforme categoria
    step=12*wave if category=="cardio" else 0
    knees=[(cx-18-step,head_y+101),(cx+18+step,head_y+101)]
    feet=[(cx-29-step,169),(cx+29+step,169)]
    if category in ("pernas","gluteos"):
        knees=[(cx-25,head_y+97),(cx+25,head_y+97)]
    for knee,foot in zip(knees,feet):
        d.line((*hip,*knee),fill="#a8f5dc",width=12)
        d.line((*knee,*foot),fill="#a8f5dc",width=10)
    d.ellipse((cx-6,head_y+68,cx+6,head_y+81),fill="#6ce3bd")
    image = image.quantize(colors=36, method=Image.Quantize.FASTOCTREE)
    return image

for index,category in enumerate(CATEGORIES,1):
    frames=[draw_frame(category,t) for t in range(16)]
    path=OUT/f"ex-{index:02}.gif"
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=88,loop=0,optimize=True,disposal=2)
print(f"24 GIFs originais gerados em: {OUT}")

# CI trigger
