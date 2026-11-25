"""Images zoomées (cadre jaune) pour la fiche 01. Usage : python3 crops_01_ordinateur.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_01_ordinateur as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL

def frame(d, r, pad=9):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)

def save(im, crop, name, scale=1.5):
    c = im.crop(crop); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")

def fixe():
    im = V.room(); d = ImageDraw.Draw(im); V.draw_fixe(d); return im, d

im, d = fixe(); frame(d, (V.MON[0] - 14, V.MON[1] - 14, V.MON[2] + 14, V.MON[3] + 14)); save(im, (280, 90, 1020, 570), "ecran")
im, d = fixe(); frame(d, V.KEYB); save(im, (290, 380, 880, 570), "clavier")
im, d = fixe(); frame(d, V.MOUSE); save(im, (600, 380, 1010, 570), "souris")
im, d = fixe(); frame(d, V.TOWER); pb = V.power_button_rect(); d.ellipse([pb[0] - 6, pb[1] - 6, pb[2] + 6, pb[3] + 6], outline=(255, 122, 89), width=5); save(im, (760, 120, 1060, 500), "uc")
im = V.room(); d = ImageDraw.Draw(im); big = (380, 120, 900, 400); V.draw_monitor(d, big, aio=True); V.draw_keyboard(d, (390, 488, 790, 550)); V.draw_mouse(d, (850, 494, 896, 554))
frame(d, (big[0] - 16, big[1] - 16, big[2] + 16, big[3] + 46)); save(im, (330, 80, 960, 570), "toutenun")
im = V.room(); d = ImageDraw.Draw(im); V.draw_laptop(d); frame(d, V.PAD); save(im, (330, 80, 950, 500), "portable")
im = V.room(); d = ImageDraw.Draw(im); V.draw_back(d)
a = V.PORTS["alim"]; frame(d, (a[0] - 20, a[1] - 20, a[2] + 20, a[3] + 60)); frame(d, V.PORTS["hdmi"]); frame(d, V.usb_all())
save(im, (290, 128, 990, 550), "prises", 1.2)
im = V.room(); d = ImageDraw.Draw(im); V.draw_side(d); c = V.SIDE_PORTS["charge"]; frame(d, (c[0], c[1], V.SIDE_PORTS["usbc"][2], c[3]), 8)
save(im, (170, 240, 760, 428), "cotes")
im = V.room(); d = ImageDraw.Draw(im); V.usb_scene(d, 0.95, 0); save(im, (120, 120, 1110, 470), "usb", 0.9)
print("ok")
