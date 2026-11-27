"""Images zoomées (cadre jaune) pour la fiche 13. Usage : python3 crops_13.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_13 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, N, YEL = V.R, V.O, V.N, V.YEL
BX, BY, BW, PAGE_Y = V.BX, V.BY, V.BW, V.PAGE_Y

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im = V.screen("home"); d = ImageDraw.Draw(im); frame(d, N.ADDR, 5); save(im, (BX, BY, BX + 760, PAGE_Y + 178), "aller", 0.9)
im = V.screen("home"); d = ImageDraw.Draw(im); frame(d, V.SBOX, 6); R.cursor(d, *R.center(V.SBOX), 1.2); save(im, (V.SBOX[0] - 60, PAGE_Y + 60, V.SBOX[2] + 60, PAGE_Y + 290), "case", 0.9)
im = V.screen("home", typed="soupe au potiron", focus=True); d = ImageDraw.Draw(im); frame(d, V.SBOX, 6); save(im, (V.SBOX[0] - 30, V.SBOX[1] - 30, V.SBOX[2] + 30, V.SBOX[3] + 30), "taper")
im = V.screen("results"); save(im, (BX, BY, BX + BW, BY + V.BH), "resultats", 0.6)
im = V.screen("results"); d = ImageDraw.Draw(im); frame(d, V.AI, 6); save(im, (BX + 10, PAGE_Y + 60, BX + 790, PAGE_Y + 240), "ia", 0.85)
im = V.screen("results"); d = ImageDraw.Draw(im); frame(d, (BX + 36, V.RES_Y[0] - 4, BX + 560, V.RES_Y[1] + 104), 4); save(im, (BX + 10, V.RES_Y[0] - 22, BX + 600, V.RES_Y[1] + 124), "liens", 0.85)
r = V.title_rect(0); im = V.screen("results", hover=0); d = ImageDraw.Draw(im); frame(d, r, 6); R.cursor(d, (r[0] + r[2]) / 2, (r[1] + r[3]) / 2, 1.2)
save(im, (BX + 10, V.RES_Y[0] - 20, BX + 560, V.RES_Y[0] + 110), "clic")
im = V.screen("site"); d = ImageDraw.Draw(im); frame(d, V.BACK, 5); R.cursor(d, *R.center(V.BACK), 1.2); save(im, (BX - 10, BY - 10, BX + 520, PAGE_Y + 75), "retour", 0.9)
im = O.room(); d = ImageDraw.Draw(im); V.pastilles(d, 0.8, 1.0); save(im, (80, 200, 1200, 470), "moteurs", 0.6)
print("ok")
