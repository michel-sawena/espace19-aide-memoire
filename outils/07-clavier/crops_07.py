"""Images zoomées (cadre jaune) pour la fiche 07. Usage : python3 crops_07.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_07 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; O = V.O; R = V.R

def frame(d, r, pad=6):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 8, outline=YEL, width=7)

def kb(pressed=(), caps=False, K=None):
    im = O.room().copy(); d = ImageDraw.Draw(im); V.keyboard(d, K, pressed, caps); return im, d

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

KB = V.KB; Y0, Y1 = V.KY - 16, V.KY + 6 * V.U + 28
X0 = min(k[0] for k in KB.values()) - 18; X1 = max(k[2] for k in KB.values()) + 18
# 1. les zones
im, d = kb()
for r, col in ((V.LETTRES, YEL), (V.CHIFFRES, (255, 122, 89)), (V.PAVE, (43, 179, 163))):
    d.rounded_rectangle([r[0] - 6, r[1] - 6, r[2] + 6, r[3] + 6], 8, outline=col, width=7)
save(im, (X0, Y0, X1, Y1), "zones", 0.75)
# touches seules (région autour de la touche)
def zoom(name, keys, region, hold=None, scale=1.0):
    im, d = kb(pressed=set(keys) | ({hold} if hold else set()))
    for k in keys + ([hold] if hold else []): frame(d, V.rect(k))
    save(im, region, name, scale)
row = lambda r0, r1: (V.KY + r0 * V.U - 6, V.KY + r1 * V.U + 22)
sp = V.rect("space"); zoom("espace", ["space"], (sp[0] - 200, *row(4, 6)[:1], sp[2] + 120, row(4, 6)[1]))
en = V.rect("enter"); bk = V.rect("back")
zoom("entree", ["enter"], (en[0] - 330, row(1, 4)[0], en[2] + 40, row(1, 4)[1]))
zoom("retour", ["back"], (bk[0] - 300, row(0, 3)[0], bk[2] + 40, row(0, 3)[1]))
m = V.rect("maj"); zoom("maj", ["P"], (m[0] - 20, row(1, 5)[0], V.rect("P")[2] + 140, row(1, 5)[1]), hold="maj", scale=0.8)
zoom("chiffres", ["k1"], (m[0] - 20, row(1, 5)[0], V.rect("k6")[2], row(1, 5)[1]), hold="maj", scale=0.9)
ag = V.rect("altgr"); z = V.rect("k0")
zoom("arobase", ["k0"], (z[0] - 300, row(1, 6)[0], z[2] + 160, row(1, 6)[1]), hold="altgr", scale=0.8)
im, d = kb(caps=True); frame(d, V.rect("verr")); save(im, (X0, row(2, 5)[0], X0 + 420, row(2, 5)[1]), "verrmaj", 1.0)
es = V.rect("esc"); im, d = kb(); frame(d, es); save(im, (X0, Y0, X0 + 420, row(0, 2)[1]), "echap", 1.0)
# résultat attendu de l'exercice
im = O.room().copy(); d = ImageDraw.Draw(im); V.sheet(d, "Paul 19", 0.1); save(im, (V.SHEET[0] - 10, V.SHEET[1] - 10, V.SHEET[0] + 420, V.SHEET[3] + 14), "resultat", 0.8)
print("ok")
