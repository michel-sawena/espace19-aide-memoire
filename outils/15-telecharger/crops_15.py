"""Images zoomées (cadre jaune) pour la fiche 15. Usage : python3 crops_15.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_15 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, W, H = V.R, V.O, V.W, V.H

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=V.YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im = V.screen("site"); d = ImageDraw.Draw(im); frame(d, V.LINK, 6); R.cursor(d, *R.center(V.LINK), 1.2)
save(im, (V.BX + 20, V.PAGE_Y + 90, V.BX + 540, V.PAGE_Y + 320), "lien", 0.9)
im = V.screen("site", panel=True); d = ImageDraw.Draw(im); frame(d, V.PITEM, 6); R.cursor(d, *R.center(V.PITEM), 1.2)
save(im, (V.PANEL[0] - 120, V.BAR_Y - 10, V.BX + V.BW + 10, V.PANEL[3] + 30), "panneau", 0.85)
im = V.screen("site"); d = ImageDraw.Draw(im); frame(d, V.IMG, 6); c = R.center(V.IMG); R.cursor(d, *c, 1.2); V.click_label(d, c)
save(im, (V.IMG[0] - 30, V.IMG[1] - 30, V.IMG[2] + 30, V.IMG[3] + 40), "clicdroit", 0.7)
im = V.screen("site", menu=True, hover=True); d = ImageDraw.Draw(im); frame(d, V.SAVE_ITEM, 5); R.cursor(d, *R.center(V.SAVE_ITEM), 1.2)
x, y = V.menu_pos(); save(im, (x - 20, y - 20, x + V.MENU_W + 30, y + 260), "menu", 0.8)
im = V.screen("site", dialog=True); d = ImageDraw.Draw(im); frame(d, V.BTN_OK, 6); frame(d, V.DNAV, 4); R.cursor(d, *R.center(V.BTN_OK), 1.2)
save(im, (V.DX - 10, V.DY - 10, V.DX + V.DW + 10, V.DY + V.DH + 20), "dialogue", 0.6)
im = V.screen("explorer", view="Téléchargements"); d = ImageDraw.Draw(im); r = R.rect_of("nav:Téléchargements"); frame(d, r, 5); R.cursor(d, *R.center(r), 1.2)
save(im, (R.WX, R.WY, R.WX + 700, R.WY + 380), "explorateur", 0.75)
im = O.room(); d = ImageDraw.Draw(im); V.illustration(d, 1.0); save(im, (160, 150, 1120, 540), "illustration", 0.5)
print("ok")
