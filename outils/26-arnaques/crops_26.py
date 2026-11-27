"""Images zoomées (cadres jaunes) pour la fiche 26. Usage : python3 crops_26.py dossier_sortie
Tous les messages sont INVENTÉS et marqués « EXEMPLE INVENTÉ »."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_26 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; F = V.F

def frame(d, r, pad=6, col=YEL):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=col, width=6)

def tag(d, n, x, y):
    d.ellipse([x, y, x + 44, y + 44], fill=YEL, outline=(0, 0, 0), width=2)
    d.text((x + 14, y + 5), str(n), font=F(28, "b"), fill=(20, 20, 20))

def save(im, crop, name):
    im.crop(tuple(int(v) for v in crop)).save(f"{OUT}/{name}.png")

PX, PY, PW = V.PX, V.PY, V.PW
# SMS : les 3 signes numérotés
im = V.phone("sms"); d = ImageDraw.Draw(im)
for i, r in enumerate([V.R_URG, V.R_LIEN, V.R_CODE]):
    frame(d, r, 4); tag(d, i + 1, r[2] + 4, r[1] + (r[3] - r[1]) / 2 - 22)
save(im, (PX - 16, PY + 30, PX + PW + 16, PY + 420), "sms")
# SMS sans indice (exercice)
save(V.phone("sms"), (PX - 16, PY + 30, PX + PW + 16, PY + 420), "sms_exo")
# mail : adresse, fautes, menace
im = V.mail(); d = ImageDraw.Draw(im)
for i, r in enumerate([V.R_ADR, V.R_FAUTE, V.R_MENACE]):
    frame(d, r, 3); tag(d, i + 1, r[2] + 8, r[1] + (r[3] - r[1]) / 2 - 22)
save(im, (V.MX, V.MY, V.MX + 830, V.MY + 440), "mail")
# appel : faux conseiller, bouton raccrocher encadré
im = V.phone("appel"); d = ImageDraw.Draw(im)
frame(d, (PX + 60, PY + 414, PX + 160, PY + 545), 4)
save(im, (PX - 16, PY + 20, PX + PW + 16, PY + 560), "appel")
print("ok")
