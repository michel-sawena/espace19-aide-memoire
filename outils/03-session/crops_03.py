"""Images zoomées (cadre jaune) pour la fiche 03. Usage : python3 crops_03.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_03 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; R = V.R; W, H = V.W, V.H

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop([int(v) for v in crop]); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im, d = V.lock(); V.key(d, (W / 2 - 230, 400, W / 2 - 70, 500), "A"); d.text((W / 2 - 22, 430), "ou", font=V.F(34, "b"), fill=(255, 255, 255)); R.cursor(d, W / 2 + 120, 430, 2.0)
save(im, (280, 90, 1000, 530), "verrou", 0.8)
im, d = V.login(4, caret=False); frame(d, V.CASE, 8); save(im, (W / 2 - 330, 110, W / 2 + 330, 440), "code", 0.9)
im, d = V.login(4, caret=False); V.key(d, (W / 2 - 120, 450, W / 2 + 120, 560), "Entrée ↵"); save(im, (W / 2 - 330, 345, W / 2 + 330, 590), "entree", 0.9)
im = V.screen(False); d = ImageDraw.Draw(im); frame(d, V.BIN, 6); save(im, (0, 0, 520, 300), "corbeille", 0.9)
im = V.screen(False); d = ImageDraw.Draw(im); frame(d, (4, H - R.TB_H + 2, W - 4, H - 2), 0); save(im, (330, H - 110, W, H), "barre", 0.8)
im = V.screen(False); d = ImageDraw.Draw(im); frame(d, V.start_rect(), 6); R.cursor(d, *R.center(V.start_rect()), 1.2); save(im, (330, 560, 950, 720), "demarrer", 1.0)
im = V.screen(True); d = ImageDraw.Draw(im); save(im, (V.SM[0] - 30, V.SM[1] - 20, V.SM[2] + 40, H), "menu", 0.75)
im = V.screen(True); d = ImageDraw.Draw(im); frame(d, V.start_rect(), 6); R.cursor(d, *R.center(V.start_rect()), 1.2); save(im, (330, V.SM[3] - 90, 950, 720), "fermer", 1.0)
im = V.screen(False); d = ImageDraw.Draw(im); save(im, (0, 0, W, H), "bureau", 0.5)
print("ok")
