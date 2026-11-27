"""Images zoomées (cadre jaune) pour la fiche 25. Usage : python3 crops_25.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_25 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, YEL, A = V.R, V.O, V.YEL, V.A
BX, BY, BW, PY = V.BX, V.BY, V.BW, V.PAGE_Y

def frame(d, r, pad=7):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=7)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im = V.screen(addr=V.ADRESSE, addr_focus=True); d = ImageDraw.Draw(im); frame(d, V.ADDR, 5); save(im, (BX + 80, V.BAR_Y - 10, BX + 640, V.BAR_Y + 70), "adresse")
im = V.screen(page="accueil", m=V.METIER, v=V.VILLE, **A); d = ImageDraw.Draw(im); frame(d, V.F1); frame(d, V.F2); save(im, (BX + 60, PY + 100, BX + 990, PY + 210), "cases", 0.8)
im = V.screen(page="accueil", m=V.METIER, v=V.VILLE, **A); d = ImageDraw.Draw(im); frame(d, V.RECH); R.cursor(d, *R.center(V.RECH), 1.2); save(im, (BX + 470, PY + 100, BX + 990, PY + 225), "rechercher")
im = V.screen(page="liste", **A); d = ImageDraw.Draw(im); frame(d, V.CREN, 5); R.cursor(d, *R.center(V.CREN), 1.2); save(im, (BX + 30, PY + 60, BX + BW - 30, PY + 250), "creneau", 0.7)
im = V.screen(page="motif", sel=True, **A); d = ImageDraw.Draw(im); frame(d, V.MOT1); save(im, (BX + 240, PY + 50, BX + 800, PY + 340), "motif", 0.7)
im = V.screen(page="recap", **A); d = ImageDraw.Draw(im); frame(d, V.OKB); R.cursor(d, *R.center(V.OKB), 1.2); save(im, (BX + 250, PY + 50, BX + 790, PY + 400), "confirmer", 0.65)
im = V.screen(page="menu", **A); d = ImageDraw.Draw(im); frame(d, V.MENU_RDV, 5); save(im, (BX + BW - 420, PY + 5, BX + BW - 5, PY + 185), "mesrdv")
im = V.screen(page="detail", **A); d = ImageDraw.Draw(im); frame(d, V.ANN, 5); R.cursor(d, *R.center(V.ANN), 1.2); save(im, (BX + 140, PY + 40, BX + 900, PY + 340), "annuler", 0.6)
im = V.screen(page="raison", sel=True, **A); d = ImageDraw.Draw(im); frame(d, V.OKA); save(im, (BX + 210, PY + 80, BX + 830, PY + 410), "raison", 0.6)
im = O.room(); d = ImageDraw.Draw(im); V.frame  # agenda (analogie)
im = V.frame("intro", 9.0, 10.0, ""); save(im, (330, 140, 950, 480), "agenda", 0.5)
print("ok")
