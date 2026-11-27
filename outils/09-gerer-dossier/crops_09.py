"""Images zoomées (cadre jaune) pour la fiche 09. Usage : python3 crops_09.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_09 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R = V.R; YEL = V.YEL

def frame(d, r, pad=8):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=7)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

def menu_shot(name, target, item, view="Documents", folders=None, only=None):
    im = V.screen(view, folders); d = ImageDraw.Draw(im); pos = V.menu_pos(target)
    V.draw_menu(d, pos, hover=item, only=only); names = only or V.ICONES
    r = V.icon_rect(pos, names.index(item)); frame(d, r, 5); R.cursor(d, *R.center(r), 1.2)
    save(im, (target[0] - 20, target[1] - 10, pos[0] + 300, pos[1] + 150), name, 1.0)

F0, F1, F2 = V.F0, V.F1, V.F2
# clic droit sur un dossier
im = V.screen(); d = ImageDraw.Draw(im); frame(d, F0, 5); R.cursor(d, *R.center(F0), 1.2)
d.text((F0[0] + 10, F0[3] + 14), "clic DROIT", font=V.F(24, "b"), fill=YEL, stroke_width=3, stroke_fill=(0, 0, 0))
save(im, (R.CONT_X - 10, R.CONT_Y - 40, R.CONT_X + 470, R.CONT_Y + 190), "clicdroit", 1.0)
menu_shot("renommer", F0, "Renommer")
im = V.edit_box(V.screen("Documents"), 0, "Courrier", False); d = ImageDraw.Draw(im); frame(d, (F0[0] - 6, F0[1] + 88, F0[2] + 6, F0[3] - 6), 4)
save(im, (R.CONT_X - 10, R.CONT_Y - 40, R.CONT_X + 470, R.CONT_Y + 170), "taper", 1.0)
menu_shot("copier", F2, "Copier", folders=["Courrier", "Factures", "Recettes"])
menu_shot("couper", F1, "Couper", folders=["Courrier", "Factures", "Recettes"])
menu_shot("coller", V.EMPTY, "Coller", view="Bureau", folders=[], only=["Coller"])
menu_shot("supprimer", F1, "Supprimer", folders=["Courrier", "Factures", "Recettes"])
# corbeille : bureau et Restaurer
im = V.screen("bureau"); d = ImageDraw.Draw(im); frame(d, V.CORB, 5); R.cursor(d, *R.center(V.CORB), 1.2); save(im, (0, 0, 320, 200), "corbeille", 1.0)
im = V.screen("Corbeille", ["Factures"]); d = ImageDraw.Draw(im); pos = V.menu_pos(F0); V.text_menu(d, pos, hover=True); rr = V.restore_rect(pos); frame(d, rr, 5)
R.cursor(d, rr[0] + 150, rr[1] + 22, 1.2); save(im, (R.CONT_X - 10, R.CONT_Y - 40, R.CONT_X + 520, R.CONT_Y + 330), "restaurer", 1.0)
# menu complet avec les noms (pour l'encadré « les petites images »)
im = V.screen(); d = ImageDraw.Draw(im); pos = V.menu_pos(F0); V.draw_menu(d, pos)
save(im, (pos[0] - 4, pos[1] - 4, pos[0] + 296, pos[1] + 56), "icones", 1.6)
print("ok")
