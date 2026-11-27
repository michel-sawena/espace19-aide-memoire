"""Images zoomées (cadre jaune) pour la fiche 10. Usage : python3 crops_10.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_10 as V
from PIL import Image, ImageDraw

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL = V.YEL; R = V.R
def frame(d, r, pad=8): d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=8)
def save(im, crop, name, scale=1.0):
    c = im.crop(tuple(int(v) for v in crop)); c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS); c.save(f"{OUT}/{name}.png")
def shot(im, r, crop, name, scale=1.0, cur=True):
    d = ImageDraw.Draw(im); frame(d, r)
    if cur: R.cursor(d, *R.center(r), 1.2)
    save(im, crop, name, scale)

shot(V.desktop(), V.START, (330, 520, 950, 720), "demarrer")
shot(V.desktop("hover", "Bloc-notes"), V.RESULT, (V.SM[0] - 10, V.SM[1] - 10, V.SM[2] + 10, V.SM[1] + 240), "taper", 0.9)
im = V.notepad(3); save(im, (V.NX - 6, V.NY - 6, V.NX + 520, V.NY + 260), "page", 0.9)
shot(V.notepad(3, menu="hover"), V.ITEM_ENR, (V.NX - 6, V.NY + 40, V.NX + 420, V.DROP[3] + 10), "fichier", 0.9)
shot(V.save_dialog(), V.D_DOC, (V.DX - 6, V.DY + 30, V.DX + 520, V.DY + 320), "documents", 0.9)
im = V.save_dialog(True, V.NOM); d = ImageDraw.Draw(im); frame(d, V.NAME_FIELD, 5); shot(im, V.BTN_ENR, (V.DX, V.DY + V.DH - 160, V.DX + V.DW + 10, V.DY + V.DH + 10), "nom", 0.75)
im = V.notepad(3, name=V.NOM + ".txt"); d = ImageDraw.Draw(im); frame(d, V.TAB, 5); save(im, (V.NX - 6, V.NY - 6, V.NX + 520, V.NY + 200), "enregistre", 0.9)
shot(V.notepad(3, name=V.NOM + ".txt"), V.CLOSE, (V.NX + V.NW - 460, V.NY - 20, V.NX + V.NW + 20, V.NY + 200), "fermer", 0.9)
shot(V.explorer_docs(True), V.FILE_R, (R.WX - 6, R.WY - 6, R.WX + 840, R.WY + 360), "retrouver", 0.7)
print("ok")
