"""Images zoomées (cadre jaune) pour la fiche 06. Usage : python3 crops_06.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_06 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; R = V.R; W, H = V.W, V.H

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

# 1. glisser une icône : position de départ (fantôme), icône en cours de déplacement
mid = (330, 250)
im, d = V.desktop(mid, sel=True, ghost=V.ICON0); R.cursor(d, mid[0] + 30, mid[1] + 35, 1.3)
d.line([V.ICON0[0] + 70, V.ICON0[1] + 40, mid[0] - 30, mid[1] + 40], fill=YEL, width=6)
d.polygon([(mid[0] - 26, mid[1] + 40), (mid[0] - 46, mid[1] + 28), (mid[0] - 46, mid[1] + 52)], fill=YEL)
frame(d, V.icon_rect(mid), 4); save(im, (20, 150, 470, 400), "glisser", 1.0)
# 2. barre du haut de la fenêtre
im, d = V.win_screen(V.WIN0); bar = (V.WIN0[0] + 2, V.WIN0[1] + 2, V.WIN0[2] - 145, V.WIN0[1] + 40)
frame(d, bar, 4); R.cursor(d, V.WIN0[0] + 140, V.WIN0[1] + 18, 1.3); save(im, (V.WIN0[0] - 20, V.WIN0[1] - 20, V.WIN0[2] + 20, V.WIN0[1] + 160), "barre", 0.8)
# 3. les trois boutons, le carré encadré
im, d = V.win_screen(V.WIN0, hover="carre"); b = V.btn_rects(V.WIN0); frame(d, b["carre"], 4); cb = R.center(b["carre"]); R.cursor(d, cb[0], cb[1], 1.2)
save(im, (V.WIN0[2] - 230, V.WIN0[1] - 20, V.WIN0[2] + 20, V.WIN0[1] + 80), "carre", 1.6)
# 4. le coin et la double flèche
im, d = V.win_screen(V.WIN0); c = (V.WIN0[2], V.WIN0[3]); frame(d, (c[0] - 26, c[1] - 26, c[0] + 26, c[1] + 26), 2); V.dbl_arrow(d, *c)
save(im, (c[0] - 260, c[1] - 160, c[0] + 80, c[1] + 70), "coin", 1.0)
# 5. menu du clic droit
im, d = V.desktop(); V.ctx_menu(d); R.cursor(d, V.MENU_AT[0] - 6, V.MENU_AT[1] - 6, 1.2); frame(d, (V.MENU_AT[0], V.MENU_AT[1], V.MENU_AT[0] + 260, V.MENU_AT[1] + 270), 6)
save(im, (V.MENU_AT[0] - 120, V.MENU_AT[1] - 40, V.MENU_AT[0] + 300, V.MENU_AT[1] + 300), "menu", 0.8)
# 6. la molette
im = Image.new("RGB", (300, 340), (255, 255, 255)); d = ImageDraw.Draw(im); V.big_mouse(d, 150, 170, 1.0, "molette", 0.1); im.save(f"{OUT}/molette.png")
# 7. souris : bouton droit
im = Image.new("RGB", (300, 340), (255, 255, 255)); d = ImageDraw.Draw(im); V.big_mouse(d, 150, 170, 1.0, "droit", 0.1); im.save(f"{OUT}/droit.png")
# 8. fenêtre agrandie (résultat de l'exercice)
im, d = V.win_screen(V.WMAX, maxed=True); save(im, (0, 0, W, H), "resultat", 0.35)
# 9. analogie : la feuille sur la table
im = R.bg(); d = ImageDraw.Draw(im)
d.rounded_rectangle([120, 330, 1160, 380], 12, fill=(176, 120, 70), outline=(140, 90, 50), width=4)
V.doc_icon(d, 260, 250, 1.1, name=None); V.doc_icon(d, 600, 190, 1.1, name=None); V.doc_icon(d, 900, 250, 1.1, name=None)
d.line([340, 240, 590, 200], fill=YEL, width=7); d.line([680, 200, 890, 240], fill=YEL, width=7)
save(im, (150, 150, 1100, 420), "table", 0.5)
print("ok")
