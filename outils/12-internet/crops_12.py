"""Images zoomées (cadre jaune) pour la fiche 12. Usage : python3 crops_12.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_12 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, YEL, W, H = V.R, V.O, V.YEL, V.W, V.H

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im = V.screen(); d = ImageDraw.Draw(im); frame(d, V.EDGE, 4); R.cursor(d, *R.center(V.EDGE), 1.2); save(im, (420, 520, 1000, 720), "ouvrir")
im = V.screen("browser"); d = ImageDraw.Draw(im); frame(d, V.ADDR, 5); save(im, (V.BX, V.BY, V.BX + 760, V.PAGE_Y + 40), "barre", 0.9)
im = V.screen("browser", typed=V.ADRESSE, focus=True); d = ImageDraw.Draw(im); frame(d, V.ADDR, 5); save(im, (V.BX + 80, V.BAR_Y - 10, V.BX + 560, V.BAR_Y + 70), "taper", 1.0)
im = V.screen("browser", typed=V.ADRESSE, page="google"); save(im, (V.BX + 200, V.BY, V.BX + V.BW - 200, V.PAGE_Y + 280), "page", 0.8)
im = V.screen("browser", typed=V.ADRESSE, page="google", close_hover=True); d = ImageDraw.Draw(im); frame(d, V.CLOSE, 5); R.cursor(d, *R.center(V.CLOSE), 1.2)
save(im, (V.BX + V.BW - 380, V.BY - 20, V.BX + V.BW + 30, V.BY + 120), "fermer")
im = O.room(); d = ImageDraw.Draw(im); V.reseau(d, 1.0, False); save(im, (160, 120, 1120, 500), "reseau", 0.5)
im = O.room(); d = ImageDraw.Draw(im); V.pastilles(d, 0.8, 1.0); save(im, (100, 200, 1180, 430), "navs", 0.6)
print("ok")
