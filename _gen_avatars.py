from PIL import Image, ImageDraw
import math

W = 320
GOLD = (199,169,87)
GOLD_LT = (232,213,160)
INK = (42,42,40)

def base(bg_top, bg_bot):
    img = Image.new("RGB",(W,W),GOLD)
    d = ImageDraw.Draw(img)
    for y in range(W):
        t = y/W
        r = int(bg_top[0]+(bg_bot[0]-bg_top[0])*t)
        g = int(bg_top[1]+(bg_bot[1]-bg_top[1])*t)
        b = int(bg_top[2]+(bg_bot[2]-bg_top[2])*t)
        d.line([(0,y),(W,y)], fill=(r,g,b))
    return img, d

def face(d, cx, cy, skin, w=118, h=132):
    d.ellipse([cx-w/2,cy-h/2,cx+w/2,cy+h/2], fill=skin)

def neck_shoulders(d, cx, cy, skin, cloth):
    # neck
    d.rectangle([cx-26,cy+40,cx+26,cy+95], fill=skin)
    # shoulders / clothing arc
    d.pieslice([cx-150,cy+55,cx+150,cy+330], 180, 360, fill=cloth)

def eyes(d, cx, cy, color=(60,48,40)):
    for dx in (-30,30):
        d.arc([cx+dx-16,cy-8,cx+dx+16,cy+14], 200, 340, fill=color, width=4)

def mouth(d, cx, cy, color=(150,100,90), smile=True):
    if smile:
        d.arc([cx-22,cy+18,cx+22,cy+44], 20, 160, fill=color, width=4)
    else:
        d.line([cx-18,cy+34,cx+18,cy+34], fill=color, width=4)

def wrinkles(d, cx, cy, color):
    # crow's feet + forehead lines for elderly
    for dx in (-46,46):
        sgn = -1 if dx<0 else 1
        d.line([cx+dx, cy-2, cx+dx+10*sgn, cy+4], fill=color, width=2)
        d.line([cx+dx, cy+4, cx+dx+10*sgn, cy+10], fill=color, width=2)
    d.line([cx-34,cy-46,cx+34,cy-46], fill=color, width=2)
    d.line([cx-30,cy-40,cx+30,cy-40], fill=color, width=2)

def glasses(d, cx, cy, color=(70,60,55)):
    for dx in (-30,30):
        d.ellipse([cx+dx-20,cy-22,cx+dx+20,cy+18], outline=color, width=4)
    d.line([cx-10,cy-2,cx+10,cy-2], fill=color, width=4)

# ---- 1) 70s man ----
img, d = base((250,238,214),(214,196,160))
cx, cy = W//2, 132
skin = (224,193,160)
neck_shoulders(d, cx, cy, skin, (70,76,82))
face(d, cx, cy, skin, 122, 134)
# gray short hair (top + sides, receding)
d.pieslice([cx-64,cy-78,cx+64,cy+26], 180, 360, fill=(214,212,206))
d.ellipse([cx-66,cy-44,cx-46,cy+10], fill=(214,212,206))
d.ellipse([cx+46,cy-44,cx+66,cy+10], fill=(214,212,206))
glasses(d, cx, cy-6)
mouth(d, cx, cy, (150,104,92), smile=True)
wrinkles(d, cx, cy-30, (190,160,135))
img.save("70s_man.png")

# ---- 2) 50s woman ----
img, d = base((247,233,224),(224,200,196))
cx, cy = W//2, 132
skin = (232,201,178)
neck_shoulders(d, cx, cy, skin, (122,84,92))
face(d, cx, cy, skin, 116, 130)
# dark hair w/ soft bob, slight gray streak
d.pieslice([cx-78,cy-86,cx+78,cy+60], 180, 360, fill=(54,46,46))
d.pieslice([cx-70,cy-70,cx+70,cy+70], 180, 360, fill=skin)
d.pieslice([cx-78,cy-86,cx+78,cy+30], 180, 360, fill=(54,46,46))
d.line([cx+38,cy-70,cx+50,cy+10], fill=(150,146,144), width=3)
eyes(d, cx, cy-10)
mouth(d, cx, cy+4, (176,104,108), smile=True)
img.save("50s_woman.png")

# ---- 3) 40s man ----
img, d = base((233,238,232),(196,206,198))
cx, cy = W//2, 132
skin = (220,188,156)
neck_shoulders(d, cx, cy, skin, (52,58,66))
face(d, cx, cy, skin, 120, 132)
# dark short hair
d.pieslice([cx-66,cy-82,cx+66,cy+8], 180, 360, fill=(40,36,34))
eyes(d, cx, cy-8)
mouth(d, cx, cy+6, (158,104,94), smile=True)
img.save("40s_man.png")

# ---- 4) 70s woman ----
img, d = base((247,238,226),(226,210,196))
cx, cy = W//2, 132
skin = (228,197,172)
neck_shoulders(d, cx, cy, skin, (150,104,118))
face(d, cx, cy, skin, 116, 128)
# white-gray hair, soft short style
d.pieslice([cx-80,cy-84,cx+80,cy+50], 180, 360, fill=(225,222,216))
d.pieslice([cx-72,cy-68,cx+72,cy+70], 180, 360, fill=skin)
d.pieslice([cx-80,cy-84,cx+80,cy+22], 180, 360, fill=(225,222,216))
eyes(d, cx, cy-6)
mouth(d, cx, cy+8, (176,118,116), smile=True)
wrinkles(d, cx, cy-26, (205,178,158))
img.save("70s_woman.png")

print("done")
