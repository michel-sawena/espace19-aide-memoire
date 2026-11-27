"""Images zoomées (cadre jaune) pour la fiche 11. Usage : python3 crops_11.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_11 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; R = V.R; W, H = V.W, V.H

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)
def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")
def ctx(items, view, i, name, corbeille=False):
    im = V.window(view, items, sel=i); d = ImageDraw.Draw(im); V.draw_ctx(d, i, hover=name, corbeille=corbeille)
    r = V.ctx_restaurer_rect(i) if corbeille else V.ctx_icon_rect(i, name); frame(d, r, 5); R.cursor(d, *R.center(r), 1.2)
    return im, V.item_rect(i), V.ctx_pos(i)

# menu du clic droit : les icônes
im, r, (x, y) = ctx(V.DOCS0, "Documents", 2, "Renommer"); save(im, (r[0] - 20, r[1] - 60, x + V.CTX_W + 20, y + 230), "renommer", 0.9)
im = V.window("Documents", V.DOCS0, edit=(2, "Liste de courses", False)); d = ImageDraw.Draw(im); r = V.item_rect(2); frame(d, (r[0] - 10, r[1] + 88, r[2] + 10, r[3] - 6), 4)
save(im, (r[0] - 330, r[1] - 20, r[2] + 170, r[3] + 20), "taper", 0.9)
# glisser
im = V.window("Documents", V.DOCS1, hide=2, sel=0); d = ImageDraw.Draw(im); dst = V.item_rect(0); frame(d, dst, 5)
V.file_icon(d, dst[2] - 20, dst[1] + 50, 0.8); R.cursor(d, dst[2] + 5, dst[1] + 90, 1.2)
save(im, (dst[0] - 20, dst[1] - 20, dst[0] + 640, dst[3] + 40), "glisser", 0.9)
im, r, (x, y) = ctx(V.DOCS2, "Documents", 2, "Copier"); save(im, (r[0] - 20, r[1] - 60, x + V.CTX_W + 20, y + 230), "copier", 0.9)
im = V.window("Famille", V.FAM0, bar_hover="Coller"); d = ImageDraw.Draw(im); b = V.bar_rect("Coller"); frame(d, b, 5); V.tooltip(d, "Coller", R.center(b)[0], R.CMD_Y + 56); R.cursor(d, *R.center(b), 1.2)
save(im, (R.WX, R.WY, R.WX + 620, R.WY + 330), "coller", 0.9)
im, r, (x, y) = ctx(V.FAM1, "Famille", 1, "Supprimer"); save(im, (r[0] - 20, r[1] - 60, x + V.CTX_W + 20, y + 230), "supprimer", 0.9)
im = V.desktop(); d = ImageDraw.Draw(im); frame(d, V.CORB, 3); R.cursor(d, *R.center(V.CORB), 1.2); save(im, (0, 0, 420, 200), "corbeille", 0.9)
im, r, (x, y) = ctx([("Photo", "f")], "Corbeille", 0, "Restaurer", corbeille=True); save(im, (r[0] - 20, r[1] - 50, x + V.CTX_W + 20, y + 190), "restaurer", 0.9)
print("ok")
