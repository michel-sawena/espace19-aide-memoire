"""Images zoomées (cadre jaune) pour la fiche 21. Usage : python3 crops_21.py dossier_sortie
Écrans neutres et inventés (site « Mon espace démarches », marqué EXEMPLE), sans logo ni charte officielle."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_21 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, YEL, W, H, CX, PY = V.R, V.O, V.YEL, V.W, V.H, V.CX, V.PY

def frame(d, r, pad=7):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

ZONE = (CX - 330, PY + 62, CX + 330, PY + 390)
def cur(d, r): R.cursor(d, r[2] - 30, (r[1] + r[3]) / 2, 1.2)
im = V.screen("accueil"); d = ImageDraw.Draw(im); frame(d, V.B_CREER); cur(d, V.B_CREER); save(im, ZONE, "creer", 0.8)
im = V.screen("form", mail=V.MAIL, mdp=V.MDP); d = ImageDraw.Draw(im); frame(d, V.CASE_MAIL); frame(d, V.CASE_MDP); save(im, ZONE, "form", 0.8)
im = V.screen("code", code=V.CODE); d = ImageDraw.Draw(im); frame(d, V.CASE_CODE); save(im, ZONE, "code", 0.8)
im = O.room(); d = ImageDraw.Draw(im); d.rectangle([0, 0, W, H], fill=(245, 246, 250)); V.telephone(d, 200, 200, True); save(im, (100, 20, 300, 380), "sms", 0.6)
im = V.screen("accueil"); d = ImageDraw.Draw(im); frame(d, V.B_FC); cur(d, V.B_FC); save(im, ZONE, "fc_bouton", 0.8)
im = V.screen("fc_choix"); d = ImageDraw.Draw(im); frame(d, V.compte_rect(0)); save(im, (CX - 440, PY + 62, CX + 440, PY + 350), "fc_choix", 0.7)
im = V.screen("fc_saisie", mail="1234567890123", mdp=V.MDP); d = ImageDraw.Draw(im); frame(d, V.CASE_MAIL); frame(d, V.CASE_MDP); save(im, ZONE, "fc_saisie", 0.8)
im = V.screen("fc_cont"); d = ImageDraw.Draw(im); frame(d, V.B_CONT); cur(d, V.B_CONT); save(im, ZONE, "fc_cont", 0.8)
im = O.room(); d = ImageDraw.Draw(im); V.boite(d, 300, 230); save(im, (170, 150, 430, 440), "boite", 0.7)
im = O.room(); d = ImageDraw.Draw(im); V.cle(d, 120, 560, 0.7); V.portes(d, 1.0); save(im, (60, 200, 1000, 620), "portes", 0.5)
print("ok")
