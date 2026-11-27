"""Images zoomées (cadre jaune) pour la fiche 04. Usage : python3 crops_04.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_04 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; R = V.R; O = V.O; W, H = V.W, V.H

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im = V.screen(None); d = ImageDraw.Draw(im); frame(d, V.EXPL, 6); R.cursor(d, *R.center(V.EXPL), 1.2); save(im, (330, 520, 950, 720), "ouvrir", 1.0)
im = V.screen("Accueil"); d = ImageDraw.Draw(im); frame(d, (R.WX + 6, R.CMD_Y + 58, R.WX + R.NAV_W - 4, R.CMD_Y + 52 + 14 + 7 * 44), 4)
save(im, (R.WX - 10, R.WY - 10, R.WX + 560, R.WY + 520), "tiroirs", 0.8)
im = V.screen("Accueil"); d = ImageDraw.Draw(im); frame(d, V.NAV_DOC, 5); R.cursor(d, *R.center(V.NAV_DOC), 1.2); save(im, (R.WX - 10, R.WY + 80, R.WX + 360, R.WY + 420), "documents", 1.0)
im = V.screen("Documents"); d = ImageDraw.Draw(im); frame(d, R.rect_of("folder:0"), 5); R.cursor(d, *R.center(R.rect_of("folder:0")), 1.2)
save(im, (R.CONT_X - 10, R.CONT_Y - 50, R.CONT_X + 500, R.CONT_Y + 170), "lettres", 1.0)
im = V.screen("Lettres"); d = ImageDraw.Draw(im); frame(d, (V.ADDR[0], V.ADDR[1], V.ADDR[0] + 270, V.ADDR[3]), 5); save(im, (R.WX, R.WY + 30, R.WX + 700, R.WY + 300), "chemin", 0.9)
im = V.screen("Lettres", hover=0); d = ImageDraw.Draw(im); r = V.seg_rects(["Documents", "Lettres"])[0]; frame(d, r, 5); R.cursor(d, *R.center(r), 1.2)
save(im, (R.WX, R.CMD_Y - 10, R.WX + 520, R.CMD_Y + 120), "remonter", 1.0)
im = V.screen("Lettres"); d = ImageDraw.Draw(im); frame(d, V.UP, 5); save(im, (R.WX, R.CMD_Y - 6, R.WX + 330, R.CMD_Y + 58), "fleche", 1.0)
im = O.room(); d = ImageDraw.Draw(im); V.armoire(d, 1.0, 1.0); save(im, (100, 90, 1000, 570), "armoire", 0.5)
print("ok")
