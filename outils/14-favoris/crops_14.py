"""Images zoomées (cadre jaune) pour la fiche 14. Usage : python3 crops_14.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_14 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, N, YEL = V.R, V.O, V.N, V.YEL

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

BX, BY, BW, PAGE_Y = V.BX, V.BY, V.BW, V.PAGE_Y
im = V.scr(); d = ImageDraw.Draw(im); frame(d, V.ADDR, 5); save(im, (BX, BY, BX + BW, PAGE_Y + 200), "site", 0.7)
im = V.scr(); d = ImageDraw.Draw(im); frame(d, V.STAR, 6); R.cursor(d, *R.center(V.STAR), 1.2); save(im, (BX + BW - 520, BY + 20, BX + BW + 10, PAGE_Y + 60), "etoile")
im = V.scr(dlg=True); d = ImageDraw.Draw(im); frame(d, V.BTN, 6); R.cursor(d, *R.center(V.BTN), 1.2); save(im, (V.DLG[0] - 20, V.BAR_Y - 5, V.DLG[2] + 30, V.DLG[3] + 30), "valider", 0.8)
im = V.scr(filled=True); d = ImageDraw.Draw(im); frame(d, V.STAR, 6); save(im, (BX + BW - 520, BY + 20, BX + BW + 10, PAGE_Y + 60), "rempli")
im = V.scr(page=None); d = ImageDraw.Draw(im); frame(d, V.DOTS, 6); R.cursor(d, *R.center(V.DOTS), 1.2); save(im, (BX + BW - 520, BY + 20, BX + BW + 10, PAGE_Y + 60), "points")
im = V.scr(page=None, mnu=True); d = ImageDraw.Draw(im); frame(d, V.FAVITEM, 6); R.cursor(d, *R.center(V.FAVITEM), 1.2); save(im, (V.MENU[0] - 30, V.BAR_Y, V.MENU[2] + 30, V.MENU[3] + 20), "favoris", 0.8)
im = V.scr(page=None, pnl=True); d = ImageDraw.Draw(im); frame(d, V.FAVROW, 6); R.cursor(d, *R.center(V.FAVROW), 1.2); save(im, (V.PANEL[0] - 30, V.BAR_Y, V.PANEL[2] + 30, V.PANEL[3] + 20), "liste", 0.8)
im = O.room(); d = ImageDraw.Draw(im); V.livre(d, 0.9); save(im, (230, 120, 1000, 540), "livre", 0.5)
print("ok")
