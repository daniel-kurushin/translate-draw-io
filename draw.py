import numpy as np
from json import load
from PIL import Image, ImageDraw, ImageFont, ImageOps

d = load(open('dic.json'))
image = Image.new('L', (512, 256), (255))
drawer = ImageDraw.Draw(image)

for k, v in d.items():
    if len(v) < 20:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 18)
    else:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 14)
    MAX_W, MAX_H = np.array(drawer.textsize(v, font=font)) + 4
    im = Image.new('L', (MAX_W, MAX_H), (255))
    dr = ImageDraw.Draw(im)
    ch = 2
    for l in v.split('\n'):
        w, h = dr.textsize(l, font=font)
        dr.text(((MAX_W - w) / 2, ch), l, fill="black", font=font)
        ch += h + 1
    
    out = Image.new('RGBA', (MAX_W, MAX_H), (255, 255, 255))
    out = im.copy()
    mask = ImageOps.invert(im)
    out.putalpha(mask)
    out.save("/tmp/111/%s.png" % k[:40], 'PNG')
    
