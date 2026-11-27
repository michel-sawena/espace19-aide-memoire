"""Images zoomées (cadre jaune) pour la fiche 16. Usage : python3 crops_16.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_16 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, B, YEL = V.R, V.O, V.B, V.YEL
PY = B.PAGE_Y

def frame(d, r, pad=8):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

CARD = (V.CX0 - 10, V.CY0 - 10, V.CX1 + 10, V.CY1 + 10)
im = B.screen("browser", typed="gmail.com", focus=True); d = ImageDraw.Draw(im); frame(d, B.ADDR, 5); save(im, (B.BX, B.BY, B.BX + 640, B.PAGE_Y + 30), "adresse", 0.9)
im = V.screen("accueil"); d = ImageDraw.Draw(im); frame(d, V.BTN_CREER); R.cursor(d, *R.center(V.BTN_CREER), 1.2); save(im, (400, PY + 30, 880, PY + 330), "creer", 0.8)
im = V.screen("accueil", menu=True, sel=0); d = ImageDraw.Draw(im); frame(d, V.MENU[0][1], 5); R.cursor(d, 600, V.MENU[0][1][1] + 20, 1.2); save(im, (440, PY + 230, 900, PY + 430), "usage", 0.85)
im = V.screen("nom", vals={0: "Marie", 1: "Dupont"}); d = ImageDraw.Draw(im); frame(d, V.SUIVANT, 5); save(im, CARD, "nom", 0.6)
im = V.screen("naissance", vals={0: "12", 1: "mars", 2: "1950", 3: "Femme"}); d = ImageDraw.Draw(im); frame(d, V.SUIVANT, 5); save(im, CARD, "naissance", 0.6)
im = V.screen("adresse", sel=2, typed_own=V.EX); d = ImageDraw.Draw(im); frame(d, (V.OPT_R[0][0], V.OPT_R[0][1], V.CX1 - 40, V.OPT_R[2][3] + 54), 6); save(im, CARD, "choix", 0.6)
im = V.screen("motdepasse", vals={0: "••••••••••", 1: "••••••••••"}); d = ImageDraw.Draw(im); frame(d, (V.FIELDS["motdepasse"][0][1][0], V.FIELDS["motdepasse"][0][1][1], V.FIELDS["motdepasse"][1][1][2], V.FIELDS["motdepasse"][1][1][3]), 6); save(im, CARD, "motdepasse", 0.6)
im = V.screen("telephone", vals={0: "06 12 34 56 78"}); d = ImageDraw.Draw(im); frame(d, V.FIELDS["telephone"][0][1], 6); save(im, CARD, "telephone", 0.6)
im = V.screen("regles"); d = ImageDraw.Draw(im); frame(d, V.SUIVANT, 5); R.cursor(d, *R.center(V.SUIVANT), 1.2); save(im, CARD, "accepte", 0.6)
im = V.screen("boite"); save(im, (B.BX, B.PAGE_Y, B.BX + B.BW, B.PAGE_Y + 360), "boite", 0.5)
print("ok")
