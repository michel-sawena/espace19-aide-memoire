"""Images zoomées (cadre jaune) pour la fiche 24. Usage : python3 crops_24.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_24 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, B, YEL = V.R, V.O, V.B, V.YEL
BX, BY, BW, PAGE_Y = V.BX, V.BY, V.BW, V.PAGE_Y

def frame(d, r, pad=8):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im = O.room(); d = ImageDraw.Draw(im); V.avis_papier(d, 640, 330, 1.0, cadre=False); r = (498, 214, 782, 282); frame(d, r, 4); save(im, (470, 110, 810, 450), "avis")
im = V.screen("vide", url=V.ADRESSE, addr_focus=True); d = ImageDraw.Draw(im); frame(d, B.ADDR, 5); save(im, (BX, BY, BX + 640, V.PAGE_Y + 30), "adresse", 0.9)
im = V.screen("accueil"); d = ImageDraw.Draw(im); frame(d, V.CONNEX, 5); R.cursor(d, *R.center(V.CONNEX), 1.2); save(im, (BX + BW - 560, BY + 40, BX + BW, PAGE_Y + 150), "connexion")
im = V.screen("numero", typed=V.NUMFISC); d = ImageDraw.Draw(im); frame(d, V.CASE_NUM, 5); save(im, (V.CX - 290, PAGE_Y + 70, V.CX + 330, PAGE_Y + 390), "numero", 0.8)
im = V.screen("mdp", typed="•" * 10); d = ImageDraw.Draw(im); frame(d, V.CASE_MDP, 5); save(im, (V.CX - 260, PAGE_Y + 70, V.CX + 260, PAGE_Y + 280), "mdp", 0.8)
im = V.screen("espace", hover=0); d = ImageDraw.Draw(im); frame(d, V.tuile_rect(0), 5); save(im, (BX + 30, PAGE_Y + 70, BX + BW - 30, PAGE_Y + 380), "espace", 0.7)
im = V.screen("espace"); d = ImageDraw.Draw(im); frame(d, V.QUITTER, 5); R.cursor(d, *R.center(V.QUITTER), 1.2); save(im, (BX + BW - 480, BY + 40, BX + BW, PAGE_Y + 140), "quitter")
im = O.room(); d = ImageDraw.Draw(im); V.faux_sms(d, 0.5, 0); save(im, (440, 100, 840, 570), "sms", 0.6)
print("ok")
