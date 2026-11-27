"""Images zoomées (cadre jaune) pour la fiche 22. Usage : python3 crops_22.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_22 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R, O, YEL = V.R, V.O, V.YEL
BX, BY, BW, PAGE_Y, ADDR = V.BX, V.BY, V.BW, V.PAGE_Y, V.ADDR

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im = O.room(); d = ImageDraw.Draw(im); V.carte_vitale(d, 300, 170, 1.4); frame(d, (320, 360, 756, 400), 4); save(im, (270, 140, 800, 500), "carte", 0.6)
im = V.screen("browser", typed=V.ADRESSE, focus=True); d = ImageDraw.Draw(im); frame(d, ADDR, 5); save(im, (BX, BY, BX + 620, V.PAGE_Y + 10), "adresse", 0.9)
im = V.B(page="site")(); d = ImageDraw.Draw(im); frame(d, V.BTN_COMPTE, 5); R.cursor(d, V.BTN_COMPTE[2] - 30, V.BTN_COMPTE[3] - 12, 1.2)
save(im, (BX + BW - 640, PAGE_Y - 10, BX + BW - 10, PAGE_Y + 220), "site", 0.8)
im = V.B(page="login", num=V.NUM, mdp="xxxxxxxx")(); d = ImageDraw.Draw(im); frame(d, V.F_NUM, 5); frame(d, V.F_MDP, 5)
save(im, (V.CX - 260, PAGE_Y + 60, V.CX + 360, PAGE_Y + 250), "login", 0.8)
im = V.B(page="login", num=V.NUM, mdp="xxxxxxxx")(); d = ImageDraw.Draw(im); frame(d, V.BTN_CO, 5); R.cursor(d, V.BTN_CO[2] - 30, V.BTN_CO[3] - 14, 1.2)
save(im, (V.CX - 260, PAGE_Y + 150, V.CX + 260, PAGE_Y + 350), "connecter", 0.8)
im = V.B(page="code", code="482 913")(); d = ImageDraw.Draw(im); frame(d, V.F_CODE, 5)
save(im, (V.CX - 290, PAGE_Y + 95, V.CX + 300, PAGE_Y + 315), "code", 0.8)
im = V.B(page="compte")(); d = ImageDraw.Draw(im); frame(d, V.BTN_ATT, 5); R.cursor(d, V.BTN_ATT[2] - 40, V.BTN_ATT[3] - 20, 1.2)
save(im, (BX + 40, PAGE_Y + 90, BX + BW - 30, PAGE_Y + 420), "compte", 0.7)
im = V.B(page="attestation")(); save(im, (V.CX - 230, PAGE_Y + 95, V.CX + 230, PAGE_Y + 460), "attestation", 0.6)
im = O.room(); d = ImageDraw.Draw(im); V.telephone_message(d); save(im, (450, 110, 830, 560), "faux_sms", 0.55)
print("ok")
