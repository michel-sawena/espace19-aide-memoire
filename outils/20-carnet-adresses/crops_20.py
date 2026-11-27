"""Images zoomées (cadre jaune) pour la fiche 20. Usage : python3 crops_20.py dossier_sortie"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_20 as V
from PIL import Image, ImageDraw
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
R = V.R; YEL = V.YEL; BX, TOP, BW = V.BX, V.TOP, V.BW

def frame(d, r, pad=8): d.rounded_rectangle([r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad], 10, outline=YEL, width=7)
def save(im, crop, name):
    im.crop(tuple(int(v) for v in crop)).save(f"{OUT}/{name}.png")

im, d = V.browser("", typing="contacts.google.com"); frame(d, V.ADDR, 5); save(im, (BX, V.BY, BX + 760, V.BY + 64), "adresse")
im, d = V.page_list(); frame(d, V.CREATE, 5); R.cursor(d, *R.center(V.CREATE), 1.2); save(im, (BX, TOP, BX + 640, TOP + 260), "creer")
im, d = V.page_form(V.NEW); [frame(d, r, 4) for r in V.FIELDS]; save(im, (BX + 290, TOP + 130, BX + 820, TOP + 380), "remplir")
im, d = V.page_form(V.NEW); frame(d, V.SAVE, 5); R.cursor(d, *R.center(V.SAVE), 1.2); save(im, (BX + BW - 520, TOP, BX + BW, TOP + 200), "enregistrer")
im, d = V.page_list([V.CONTACTS[2]], query="Pau"); frame(d, V.SEARCH, 5); save(im, (BX + 260, TOP, BX + 960, TOP + 200), "chercher")
im, d = V.page_fiche("Paul Durand", V.NEW[2]); frame(d, V.EDIT, 5); R.cursor(d, *R.center(V.EDIT), 1.2); save(im, (BX + BW - 560, TOP, BX + BW, TOP + 200), "modifier")
im, d = V.page_mail("Pau", sugg=True); frame(d, V.SUGG, 4); R.cursor(d, V.SUGG[0] + 300, V.SUGG[1] + 40, 1.2); save(im, (BX + 310, TOP + 76, BX + 900, TOP + 226), "ecrire")
im, d = V.page_fiche("Sophie Dubois", V.CONTACTS[3][1], menu=True); frame(d, V.PLUS, 4); frame(d, V.MENU_SUPPR, 4); save(im, (BX + BW - 520, TOP, BX + BW, TOP + 200), "supprimer")
im, d = V.page_fiche("Jeanne Martin", V.JEANNE[2]); save(im, (BX + 100, TOP + 100, BX + 960, TOP + 380), "resultat")
print("ok")
