"""Images zoomées (cadre jaune) pour la fiche 23. Usage : python3 crops_23.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_23 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, YEL, B = V.R, V.O, V.YEL, V.B

def cadre(d, r, pad=8):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=7)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

P, L, Rr = V.PAGE_Y, V.L, V.Rr
im = V.screen("vide", typed="caf.fr", focus_addr=True); d = ImageDraw.Draw(im); cadre(d, B.ADDR, 5); save(im, (V.BX + 80, B.BAR_Y - 10, V.BX + 560, B.BAR_Y + 70), "adresse")
im = V.screen("accueil"); d = ImageDraw.Draw(im); cadre(d, V.MONCOMPTE); R.cursor(d, *R.center(V.MONCOMPTE), 1.2); save(im, (Rr - 560, P - 5, Rr + 10, P + 130), "moncompte")
im = V.screen("connexion", num=V.NUM_EX, mdp=10); d = ImageDraw.Draw(im); cadre(d, V.F1, 5); cadre(d, V.F2, 5)
d.text((V.F1[2] - 120, V.F1[1] + 10), "EXEMPLE", font=V.F(16, "b"), fill=V.CORAIL); save(im, (V.PX0 - 10, P + 70, V.PX1 + 10, P + 285), "cases")
im = V.screen("connexion", num=V.NUM_EX, mdp=10); d = ImageDraw.Draw(im); cadre(d, V.BTN_CO, 5); R.cursor(d, *R.center(V.BTN_CO), 1.2); save(im, (V.PX0 - 10, P + 240, V.PX1 + 10, P + 395), "seconnecter")
im = V.screen("code", envoye=True, code=V.CODE_EX); d = ImageDraw.Draw(im); cadre(d, V.BTN_ENV, 5); cadre(d, V.CODE_ROW, 5); save(im, (V.PX0 - 10, P + 70, V.PX1 + 10, P + 355), "code")
im = V.screen("code", envoye=True); d = ImageDraw.Draw(im); V.bulle_mail(d, 0); save(im, (850, 240, 1255, 490), "mail", 0.9)
im = V.screen("espace"); d = ImageDraw.Draw(im); cadre(d, V.TILE_ATT); R.cursor(d, *R.center(V.TILE_ATT), 1.2); save(im, (L, P, L + 720, P + 250), "attestations", 0.9)
im = V.screen("attest", pai=True, mois=True); d = ImageDraw.Draw(im); cadre(d, V.R_PAI, 5); cadre(d, V.R_MOIS, 5); save(im, (L + 40, P + 60, L + 940, P + 210), "choix", 0.85)
im = V.screen("attest", pai=True, mois=True); d = ImageDraw.Draw(im); cadre(d, V.BTN_TEL, 5); R.cursor(d, *R.center(V.BTN_TEL), 1.2); save(im, (L + 40, P + 200, L + 700, P + 300), "telecharger")
im = V.screen("espace"); d = ImageDraw.Draw(im); cadre(d, V.DECO, 5); R.cursor(d, *R.center(V.DECO), 1.2); save(im, (Rr - 520, P - 5, Rr + 10, P + 120), "deconnexion")
im = V.screen("connexion"); d = ImageDraw.Draw(im); cadre(d, V.OUBLI, 5); cadre(d, V.BTN_FC, 5); save(im, (V.PX0 - 10, P + 240, V.PX1 + 10, P + 395), "oubli")
im = O.room(); d = ImageDraw.Draw(im); V.carte_vitale(d, 200, 300); V.cle(d, 560, 300); V.enveloppe(d, 900, 300); save(im, (60, 200, 1020, 400), "preparer", 0.5)
print("ok")
