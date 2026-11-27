"""Images zoomées (cadre jaune) pour la fiche 17. Usage : python3 crops_17.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_17 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, B, YEL, W, H = V.R, V.O, V.B, V.YEL, V.W, V.H

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

BX, BY, PY, CX = V.BX, V.BY, V.PAGE_Y, V.CX
# 1. adresse du site dans la barre d'adresse
im = V.screen("vide", url=V.URL, focus=True); d = ImageDraw.Draw(im); frame(d, V.ADDR, 5)
save(im, (BX + 80, V.B.BAR_Y - 10, BX + 600, V.B.BAR_Y + 70), "site")
# 2. adresse e-mail
im = V.screen("adresse", typed=V.MAIL); d = ImageDraw.Draw(im); frame(d, V.FIELD, 6)
save(im, (V.CARD[0] - 10, V.CARD[1] - 10, V.CARD[2] + 10, V.CARD[3] + 10), "adresse", 0.75)
# 3. mot de passe + bouton bleu
im = V.screen("mdp", typed="secret2026"); d = ImageDraw.Draw(im); frame(d, V.FIELD, 6); frame(d, V.BTN, 6)
R.cursor(d, *R.center(V.BTN), 1.2)
save(im, (V.CARD[0] - 10, V.CARD[1] - 10, V.CARD[2] + 10, V.CARD[3] + 10), "motdepasse", 0.75)
# 4. connecté : la boîte de réception
im = V.screen("boite"); save(im, (BX, PY - 10, BX + V.BW, PY + 380), "boite", 0.6)
# 5. le rond en haut à droite
im = V.screen("boite"); d = ImageDraw.Draw(im); frame(d, V.AV, 6); R.cursor(d, *R.center(V.AV), 1.2)
save(im, (BX + V.BW - 420, PY - 20, BX + V.BW + 10, PY + 150), "rond")
# 6. Déconnexion
im = V.screen("boite", menu=True); d = ImageDraw.Draw(im); frame(d, V.DECO, 6); R.cursor(d, *R.center(V.DECO), 1.2)
save(im, (V.MENU[0] - 30, PY - 10, V.MENU[2] + 20, V.MENU[3] + 20), "deco")
# 7. Utiliser un autre compte
im = V.screen("choix"); d = ImageDraw.Draw(im); frame(d, V.AUTRE_R, 6)
save(im, (V.CARD[0] - 10, V.CARD[1] + 120, V.CARD[2] + 10, V.CARD[1] + 300), "autre", 0.75)
# illustration boîte aux lettres + clé
im = Image.new("RGB", (560, 360), (248, 234, 245)); d = ImageDraw.Draw(im)
V.boite_lettres(d, 170, 150, True); V.cle(d, 380, 140)
im.save(f"{OUT}/analogie.png")
print("ok")
