"""Images zoomées (cadre jaune) pour la fiche 18. Usage : python3 crops_18.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_18 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R = V.R; YEL = V.YEL; rect = V.rect; ADR = V.ADR
MSG = "Bonjour Paul,\nMerci pour les photos du jardin !\nÀ bientôt,\nMarie"

def frame(d, r, pad=6):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=7)

def save(im, crop, name):
    im.crop(tuple(int(v) for v in crop)).save(f"{OUT}/{name}.png")

def shot(name, im, target, crop, cursor=True):
    d = ImageDraw.Draw(im); frame(d, target)
    if cursor: R.cursor(d, target[2] - 26, (target[1] + target[3]) / 2, 1.2)
    save(im, crop, name)

B = V.BX; T = V.TOP
shot("boite", V.screen("liste"), rect("boite"), (B, T - 10, B + 760, T + 300))
shot("lire", V.screen("liste"), rect("mail:0"), (B + 200, T - 10, B + 1000, T + 170))
shot("nouveau", V.screen("liste"), rect("nouveau"), (B, T - 10, B + 520, T + 200))
C0 = rect("compose")
shot("case_a", V.screen("liste", comp={"a": ADR, "focus": "case_a"}), rect("case_a"), (C0[0] - 10, C0[1] - 10, C0[2] + 10, C0[1] + 170), False)
shot("objet", V.screen("liste", comp={"a": ADR, "objet": "Bonjour", "focus": "objet"}), rect("objet"), (C0[0] - 10, C0[1] - 10, C0[2] + 10, C0[1] + 170), False)
shot("texte", V.screen("liste", comp={"a": ADR, "objet": "Bonjour", "texte": MSG}), rect("texte"), (C0[0] - 10, C0[1] + 40, C0[2] + 10, C0[3] - 60), False)
shot("envoyer", V.screen("liste", comp={"a": ADR, "objet": "Bonjour", "texte": MSG}), rect("envoyer"), (C0[0] - 10, C0[3] - 230, C0[0] + 470, C0[3] + 10))
shot("repondre", V.screen("lecture", unread=0, mail=V.RECUS[1]), rect("repondre"), (B + V.SIDE_W + 10, T + 40, B + V.SIDE_W + 640, T + 430))
im = V.screen("liste", mails=[("Moi", "Essai", "Bonjour !", True)] + [(m[0], m[1], m[2], False) for m in V.RECUS[1:]])
shot("recu", im, rect("mail:0"), (B + 200, T - 10, B + 1000, T + 170), False)
print("ok")
