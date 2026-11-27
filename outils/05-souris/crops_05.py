"""Images zoomées (cadre jaune) pour la fiche 05. Usage : python3 crops_05.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_05 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; R = V.R; W, H = V.W, V.H

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop([int(v) for v in crop]); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im = R.bg(); d = ImageDraw.Draw(im); V.big_mouse(d, W / 2, 400, 1.0, press="L", hand=True)
V.O.label(d, "index : bouton gauche", (W / 2 - 290, 210)); V.O.label(d, "majeur : bouton droit", (W / 2 + 290, 210))
save(im, (90, 150, 1190, 640), "tenir", 0.55)
im = V.desktop("dos"); d = ImageDraw.Draw(im); frame(d, V.DOS, 10); R.cursor(d, *R.center(V.DOS), 1.4); save(im, (0, 0, 420, 300), "clic", 1.0)
im = V.desktop(); d = ImageDraw.Draw(im); frame(d, V.DOS, 10); R.cursor(d, *R.center(V.DOS), 1.4); V.clic_word(d, 150, 150, "clic clic !"); save(im, (0, 0, 470, 300), "double", 1.0)
im = V.window("photos"); d = ImageDraw.Draw(im); save(im, (230, 70, 1130, 620), "fenetre", 0.5)
im = V.window("photos"); d = ImageDraw.Draw(im); frame(d, V.CLOSE, 6); R.cursor(d, *R.center(V.CLOSE), 1.4); save(im, (V.WIN[2] - 420, V.WIN[1] - 30, V.WIN[2] + 40, V.WIN[1] + 200), "croix", 0.9)
im = V.desktop(); d = ImageDraw.Draw(im); frame(d, V.BLOC, 10); R.cursor(d, *R.center(V.BLOC), 1.4); V.clic_word(d, 150, 280, "clic clic !"); save(im, (0, 200, 470, 450), "bloc", 1.0)
im = V.window("bloc", "Bonjour !"); d = ImageDraw.Draw(im); frame(d, V.CLOSE, 6); save(im, (230, 70, 1130, 400), "bloc_ouvert", 0.6)
im = V.frame("bouger", 12.0, 15.0, ""); save(im, (30, 140, 1240, 650), "glisser", 0.5)
print("ok")
