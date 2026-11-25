"""Images zoomées (cadre jaune) pour la fiche 02. Usage : python3 crops_02.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_02 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; O = V.O; R = V.R

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.0):
    c = im.crop(crop); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

im, d = V.fixe(None); frame(d, O.power_button_rect()); save(im, (300, 90, 1040, 570), "fixe", 0.9)
im, d = V.laptop(True, False); frame(d, V.LAP_BTN, 7); save(im, (330, 80, 950, 500), "portable", 0.9)
im, d = V.lock_screen(); save(im, (240, 90, 1040, 340), "verrou", 0.8)
im = V.screen(V.S0); d = ImageDraw.Draw(im); frame(d, V.start_rect(), 6); R.cursor(d, *R.center(V.start_rect()), 1.2); save(im, (330, 520, 950, 720), "demarrer", 1.0)
im = V.screen(V.S1); d = ImageDraw.Draw(im); frame(d, V.PWR, 6); save(im, (V.SM[0] - 10, 300, V.SM[2] + 20, 575), "marche", 0.9)
im = V.screen(dict(V.S2, hover=1)); d = ImageDraw.Draw(im); frame(d, V.pm_item(1), 6); save(im, (V.PM[0] - 80, V.PM[1] - 20, V.PM[2] + 30, V.SM[3] + 15), "arreter", 1.1)
im = V.screen(dict(V.S2, hover=2)); d = ImageDraw.Draw(im); frame(d, V.pm_item(2), 6); save(im, (V.PM[0] - 80, V.PM[1] - 20, V.PM[2] + 30, V.SM[3] + 15), "redemarrer", 1.1)
im, d = V.laptop_lid(0.85); save(im, (330, 80, 950, 500), "veille", 0.9)
print("ok")
