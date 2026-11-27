"""Images zoomées (cadre jaune) pour la fiche 19. Usage : python3 crops_19.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_19 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R = V.R; YEL = V.YEL

def cadre(d, r, pad=8):
    d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=7)

def save(im, crop, name):
    im.crop(tuple(int(v) for v in crop)).save(f"{OUT}/{name}.png")

def shot(state, target, crop, name, kw=None, cur=True):
    im = V.screen(state, **(kw or {})); d = ImageDraw.Draw(im); cadre(d, target)
    if cur: R.cursor(d, *R.center(target), 1.2)
    save(im, crop, name)

shot("inbox", V.NEW, (V.BX, V.TOP, V.BX + 560, V.TOP + 200), "nouveau")
shot("compose", V.CLIP, (V.COMP[0] - 10, V.COMP[1], V.COMP[2] + 10, V.COMP[3] + 12), "trombone")
shot("dialog", V.PHOTO, (V.DLG[0] - 10, V.DLG[1] - 10, V.DLG[2] + 10, V.DLG[3] + 10), "choisir")
shot("compose", V.SEND, (V.COMP[0] - 10, V.COMP[1], V.COMP[2] + 10, V.COMP[3] + 12), "envoyer", {"chip": True})
im = V.screen("inbox"); d = ImageDraw.Draw(im); r = (V.BX + V.BW - 90, V.ROW0[1] + 4, V.BX + V.BW - 50, V.ROW0[3] - 8); cadre(d, r, 6)
save(im, (V.LIST_X - 10, V.TOP + 6, V.BX + V.BW - 10, V.TOP + 140), "recu")
shot("msg", V.THUMB, (V.LIST_X - 10, V.TOP + 10, V.LIST_X + 720, V.TOP + 420), "vignette")
shot("msg", V.DLBTN, (V.LIST_X - 10, V.TOP + 240, V.LIST_X + 420, V.TOP + 420), "fleche", {"hover": True})
print("ok")
