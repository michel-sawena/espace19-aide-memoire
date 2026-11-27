"""Vidéo « 15 - Télécharger un fichier ou une image » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_15.py script.json durations.json out.mp4
        python3 render_15.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, Explorateur, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes),
../01-ordinateur/render_01_ordinateur.py (étiquettes) et ../12-internet/render_12.py (globe, ordinateur).
Le site montré est INVENTÉ (« Club des jardiniers – site d'exemple ») : aucun site réel, aucun logo.
Libellés écrits tels quels (voir sources_15.md) : « Enregistrer l'image sous », « Téléchargements », « Enregistrer », « Annuler ».
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as N
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); BLEU = (0, 103, 192); ORANGE = (255, 120, 0)
ADRESSE = "club-jardiniers.exemple"

# ---------- navigateur ----------
BX, BY, BW, BH = 110, 64, 1060, 590
TAB_H = 40; BAR_Y = BY + TAB_H; PAGE_Y = BAR_Y + 62
ADDR = (BX + 150, BAR_Y + 10, BX + BW - 140, BAR_Y + 50)
DLI = (BX + BW - 118, BAR_Y + 10, BX + BW - 78, BAR_Y + 50)          # icône des téléchargements
LINK = (BX + 60, PAGE_Y + 250, BX + 470, PAGE_Y + 290)               # lien « Télécharger le programme (PDF) »
IMG = (BX + 600, PAGE_Y + 110, BX + 960, PAGE_Y + 380)               # image de la fleur
PANEL = (BX + BW - 470, BAR_Y + 56, BX + BW - 20, BAR_Y + 176)
PITEM = (PANEL[0] + 14, PANEL[1] + 48, PANEL[2] - 14, PANEL[1] + 106)

def fleur(d, r):
    x0, y0, x1, y1 = r
    d.rectangle(r, fill=(214, 236, 250)); d.rectangle([x0, y1 - (y1 - y0) * 0.28, x1, y1], fill=(120, 190, 90))
    cx, cy = (x0 + x1) / 2, y0 + (y1 - y0) * 0.42; s = (x1 - x0) / 360
    d.line([cx, cy, cx, y1 - 10 * s], fill=(50, 130, 50), width=int(8 * s) + 1)
    d.ellipse([cx + 4 * s, cy + 70 * s, cx + 60 * s, cy + 100 * s], fill=(70, 160, 70))
    for k in range(8):
        a = k * math.pi / 4; px, py = cx + 42 * s * math.cos(a), cy + 42 * s * math.sin(a)
        d.ellipse([px - 26 * s, py - 26 * s, px + 26 * s, py + 26 * s], fill=(240, 90, 130))
    d.ellipse([cx - 24 * s, cy - 24 * s, cx + 24 * s, cy + 24 * s], fill=(255, 200, 40))

def pdf_icon(d, x, y, s=1.0):
    d.polygon([(x, y), (x + 44 * s, y), (x + 60 * s, y + 16 * s), (x + 60 * s, y + 76 * s), (x, y + 76 * s)], fill=(255, 255, 255), outline=(120, 120, 130))
    d.rectangle([x + 6 * s, y + 46 * s, x + 54 * s, y + 66 * s], fill=(200, 40, 40)); d.text((x + 13 * s, y + 46 * s), "PDF", font=F(int(17 * s) + 1, "b"), fill=(255, 255, 255))
    for k in range(3): d.line([x + 8 * s, y + (14 + 9 * k) * s, x + 40 * s, y + (14 + 9 * k) * s], fill=(170, 170, 180), width=2)

def dl_icon(d, r, col=(60, 60, 70)):
    cx, cy = R.center(r)
    d.line([cx, cy - 12, cx, cy + 6], fill=col, width=3); d.line([cx - 8, cy - 2, cx, cy + 7, cx + 8, cy - 2], fill=col, width=3)
    d.line([cx - 11, cy + 12, cx + 11, cy + 12], fill=col, width=3)

def browser(d, page="site", panel=False, saved=None):
    d.rounded_rectangle([BX + 6, BY + 8, BX + BW + 6, BY + BH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([BX, BY, BX + BW, BY + BH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([BX, BY, BX + BW, BY + TAB_H + 10], 10, fill=(222, 226, 236)); d.rectangle([BX, BY + 20, BX + BW, BY + TAB_H], fill=(222, 226, 236))
    d.rounded_rectangle([BX + 12, BY + 6, BX + 320, BY + TAB_H + 4], 8, fill=(250, 250, 252))
    N.globe(d, BX + 32, BY + 23, 9)
    d.text((BX + 50, BY + 12), "Programme.pdf" if page == "pdf" else "Club des jardiniers", font=F(17), fill=(30, 30, 30))
    d.line([BX + BW - 150, BY + 20, BX + BW - 132, BY + 20], fill=(60, 60, 60), width=2)
    d.rectangle([BX + BW - 100, BY + 12, BX + BW - 84, BY + 28], outline=(60, 60, 60), width=2)
    cx = BX + BW - 29; cy = BY + 20
    d.line([cx - 9, cy - 9, cx + 9, cy + 9], fill=(40, 40, 40), width=3); d.line([cx - 9, cy + 9, cx + 9, cy - 9], fill=(40, 40, 40), width=3)
    d.rectangle([BX + 2, BAR_Y, BX + BW - 2, BAR_Y + 60], fill=(250, 250, 252))
    for i, x in enumerate((BX + 30, BX + 70)):
        y = BAR_Y + 30; s = -1 if i == 0 else 1
        d.line([x - 9 * s, y, x + 9 * s, y], fill=(110, 110, 120), width=3)
        d.line([x + 2 * s, y - 7, x + 9 * s, y, x + 2 * s, y + 7], fill=(110, 110, 120), width=3)
    d.arc([BX + 100, BAR_Y + 19, BX + 124, BAR_Y + 43], 40, 320, fill=(110, 110, 120), width=3)
    d.rounded_rectangle(ADDR, 20, fill=(238, 240, 244), outline=(200, 204, 212), width=1)
    d.text((ADDR[0] + 22, ADDR[1] + 9), ADRESSE + ("/programme.pdf" if page == "pdf" else ""), font=F(20), fill=(20, 20, 20))
    if panel: d.rounded_rectangle(DLI, 8, fill=(220, 232, 248))
    dl_icon(d, DLI, BLEU if panel else (60, 60, 70))
    d.line([BX + 2, PAGE_Y, BX + BW - 2, PAGE_Y], fill=(215, 218, 225), width=1)
    if page == "site":
        d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, PAGE_Y + 70], fill=(232, 244, 228))
        d.text((BX + 60, PAGE_Y + 14), "Club des jardiniers", font=F(34, "b"), fill=(40, 100, 50))
        d.text((BX + BW - 250, PAGE_Y + 26), "(site d'exemple)", font=F(18), fill=(90, 90, 100))
        d.text((BX + 60, PAGE_Y + 110), "Les ateliers de l'hiver", font=F(26, "s"), fill=INK)
        for k, w in enumerate((420, 380, 400)):
            d.rounded_rectangle([BX + 60, PAGE_Y + 160 + k * 26, BX + 60 + w, PAGE_Y + 172 + k * 26], 5, fill=(220, 223, 230))
        pdf_icon(d, LINK[0], LINK[1] - 4, 0.55)
        d.text((LINK[0] + 44, LINK[1] + 6), "Télécharger le programme (PDF)", font=F(20, "s"), fill=BLEU)
        tw = d.textlength("Télécharger le programme (PDF)", font=F(20, "s")); d.line([LINK[0] + 44, LINK[1] + 32, LINK[0] + 44 + tw, LINK[1] + 32], fill=BLEU, width=2)
        fleur(d, IMG)
        d.text((IMG[0] + 100, IMG[3] + 10), "Notre fleur du mois", font=F(18), fill=(90, 90, 100))
    elif page == "pdf":
        d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, BY + BH - 2], fill=(82, 86, 96))
        x0 = BX + BW / 2 - 230; d.rectangle([x0, PAGE_Y + 24, x0 + 460, BY + BH - 4], fill=(255, 255, 255))
        d.text((x0 + 40, PAGE_Y + 60), "Programme des ateliers", font=F(28, "b"), fill=(40, 100, 50))
        for k in range(7):
            d.rounded_rectangle([x0 + 40, PAGE_Y + 130 + k * 34, x0 + 40 + (360 if k % 3 else 260), PAGE_Y + 142 + k * 34], 5, fill=(215, 218, 226))
    if panel:
        d.rounded_rectangle([PANEL[0] + 4, PANEL[1] + 6, PANEL[2] + 4, PANEL[3] + 6], 12, fill=(150, 155, 170))
        d.rounded_rectangle(PANEL, 12, fill=(255, 255, 255), outline=(170, 175, 190), width=2)
        d.rounded_rectangle([PANEL[0] + 14, PANEL[1] + 16, PANEL[0] + 200, PANEL[1] + 30], 5, fill=(225, 228, 234))
        pdf_icon(d, PITEM[0] + 6, PITEM[1] + 2, 0.66)
        d.text((PITEM[0] + 62, PITEM[1] + 6), "Programme.pdf", font=F(22, "s"), fill=(20, 20, 20))
        d.text((PITEM[0] + 62, PITEM[1] + 34), "✔", font=F(18, "b"), fill=VERT)
        d.rounded_rectangle([PITEM[0] + 86, PITEM[1] + 40, PITEM[0] + 230, PITEM[1] + 50], 4, fill=(225, 228, 234))
    if saved:
        O.label(d, saved, (BX + BW / 2, PAGE_Y + 330))

# ---------- menu du clic droit ----------
MENU_W, ROW = 400, 44
def menu_pos(): return (IMG[0] - 120, IMG[1] + 60)
ITEMS = [None, None, "Enregistrer l'image sous", None, None]
def item_rect(i):
    x, y = menu_pos(); return (x + 8, y + 8 + i * ROW, x + MENU_W - 8, y + 8 + (i + 1) * ROW - 4)
SAVE_ITEM = item_rect(2)
def draw_menu(d, hover=False):
    x, y = menu_pos(); h = 16 + len(ITEMS) * ROW
    d.rounded_rectangle([x + 5, y + 6, x + MENU_W + 5, y + h + 6], 10, fill=(120, 125, 140))
    d.rounded_rectangle([x, y, x + MENU_W, y + h], 10, fill=(253, 253, 254), outline=(184, 190, 201), width=2)
    for i, it in enumerate(ITEMS):
        r = item_rect(i)
        if it:
            if hover: d.rounded_rectangle(r, 6, fill=(225, 235, 250))
            d.text((r[0] + 14, r[1] + 8), it, font=F(21, "s"), fill=(20, 20, 20))
        else:
            d.rounded_rectangle([r[0] + 14, r[1] + 14, r[0] + 14 + (220 if i % 2 else 280), r[1] + 26], 5, fill=(225, 228, 234))

# ---------- fenêtre « Enregistrer sous » ----------
DX, DY, DW, DH = 250, 120, 780, 440
DNAV = (DX + 16, DY + 120, DX + 230, DY + 160)            # « Téléchargements » sélectionné
BTN_OK = (DX + DW - 330, DY + DH - 64, DX + DW - 180, DY + DH - 20)
BTN_NO = (DX + DW - 165, DY + DH - 64, DX + DW - 20, DY + DH - 20)
def dialog(d):
    d.rounded_rectangle([DX + 6, DY + 8, DX + DW + 6, DY + DH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([DX, DY, DX + DW, DY + DH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([DX, DY, DX + DW, DY + 44], 10, fill=(232, 236, 244)); d.rectangle([DX, DY + 24, DX + DW, DY + 44], fill=(232, 236, 244))
    d.text((DX + 18, DY + 11), "Enregistrer sous", font=F(19, "s"), fill=(20, 20, 20))
    for k, nm in enumerate(["Bureau", "Téléchargements", "Documents", "Images"]):
        r = (DX + 16, DY + 70 + k * 50, DX + 230, DY + 110 + k * 50)
        if nm == "Téléchargements": d.rounded_rectangle(r, 6, fill=(204, 228, 247))
        R.folder_icon(d, r[0] + 8, r[1] + 10, 0.23); d.text((r[0] + 40, r[1] + 9), nm, font=F(18), fill=(20, 20, 20))
    d.line([DX + 246, DY + 60, DX + 246, DY + DH - 90], fill=(225, 228, 235), width=2)
    d.text((DX + 270, DY + 70), "Téléchargements", font=F(22, "b"), fill=(30, 30, 30))
    pdf_icon(d, DX + 280, DY + 115, 0.7); d.text((DX + 262, DY + 175), "Programme.pdf", font=F(15), fill=(30, 30, 30))
    d.rounded_rectangle([DX + 270, DY + DH - 130, DX + DW - 20, DY + DH - 90], 6, fill=(255, 255, 255), outline=(150, 155, 170), width=2)
    d.text((DX + 284, DY + DH - 122), "fleur.png", font=F(20), fill=(20, 20, 20))
    d.rounded_rectangle(BTN_OK, 8, fill=BLEU); tw = d.textlength("Enregistrer", font=F(20, "s")); c = R.center(BTN_OK)
    d.text((c[0] - tw / 2, c[1] - 13), "Enregistrer", font=F(20, "s"), fill=(255, 255, 255))
    d.rounded_rectangle(BTN_NO, 8, fill=(240, 242, 246), outline=(150, 155, 170), width=2); tw = d.textlength("Annuler", font=F(20, "s")); c = R.center(BTN_NO)
    d.text((c[0] - tw / 2, c[1] - 13), "Annuler", font=F(20, "s"), fill=(20, 20, 20))

# ---------- écrans ----------
def screen(state=None, **kw):
    if state == "explorer":
        im = R.screen({"window": True, "view": kw.get("view", "Accueil"), "folders": []}); d = ImageDraw.Draw(im)
        if kw.get("view") == "Téléchargements":
            r0, r1 = R.rect_of("folder:0"), R.rect_of("folder:1")
            d.rectangle([r0[0], r0[1], r1[2], r1[3]], fill=(255, 255, 255))
            pdf_icon(d, r0[0] + 35, r0[1] + 8, 1.0); d.text((r0[0] + 6, r0[1] + 95), "Programme.pdf", font=F(17), fill=(20, 20, 20))
            fleur(d, (r1[0] + 15, r1[1] + 10, r1[0] + 115, r1[1] + 85)); d.text((r1[0] + 30, r1[1] + 95), "fleur.png", font=F(17), fill=(20, 20, 20))
        return im
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if state in ("site", "pdf"): browser(d, state, panel=kw.get("panel", False), saved=kw.get("saved"))
    if kw.get("menu"): draw_menu(d, kw.get("hover", False))
    if kw.get("dialog"): dialog(d)
    return im

def click_label(d, c, txt="clic DROIT"):
    d.text((c[0] - 80, c[1] + 50), txt, font=F(30, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None, right=False):
    c = R.center(r); tc = 0.6 * D
    im = (after if t >= tc + 0.3 else before)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6, ORANGE if right else YEL)
    if right and 0.4 * D < t < tc + 0.3: click_label(d, c)
    R.caption(d, cap); return im

def site(**kw): return lambda: screen("site", **kw)

# ---------- illustrations ----------
def illustration(d, p):
    N.globe(d, 300, 290, 110)
    O.label(d, "Internet", (300, 420))
    N.pc(d, 980, 290, 2.6)
    O.label(d, "votre ordinateur", (980, 420))
    q = R.ease((p - 0.15) / 0.35)
    if q > 0:
        x = 430 + (840 - 430) * q
        pdf_icon(d, x - 30, 250, 1.0)
        d.line([430, 330, 840, 330], fill=YEL, width=10); d.polygon([(860, 330), (830, 312), (830, 348)], fill=YEL)
    if p > 0.55: O.label(d, "comme une photocopie que vous gardez", (W / 2, 500))

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Télécharger un fichier ou une image", ["Aide-mémoire n° 15 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); r = (W / 2 - 70, 290, W / 2 + 70, 430); d.ellipse(r, fill=(255, 246, 214), outline=YEL, width=6)
        cx, cy = R.center(r)
        d.line([cx, cy - 40, cx, cy + 20], fill=VIO, width=12); d.line([cx - 28, cy - 8, cx, cy + 24, cx + 28, cy - 8], fill=VIO, width=12)
        d.line([cx - 36, cy + 42, cx + 36, cy + 42], fill=VIO, width=10); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); illustration(d, p); R.caption(d, cap); return im
    if sid == "dossier":
        im = screen("explorer", view="Téléchargements"); clean = im.copy(); d = ImageDraw.Draw(im)
        r = R.rect_of("nav:Téléchargements")
        if p > 0.25:
            R.highlight(d, r, t); R.loupe(im, r, place=(1000, 300), clean=clean); d = ImageDraw.Draw(im)
            O.label(d, "le dossier Téléchargements", (900, 470))
        R.caption(d, cap); return im
    if sid == "fichier":
        return act(site(), site(panel=True), LINK, (W / 2 + 200, H / 2 + 150), t, D, cap, place=(880, 520))
    if sid == "liste":
        im = screen("site", panel=True); clean = im.copy(); d = ImageDraw.Draw(im)
        if p > 0.2:
            R.highlight(d, PANEL, t); R.loupe(im, PITEM, place=(420, 470), clean=clean); d = ImageDraw.Draw(im)
            O.label(d, "en haut à droite", (PANEL[0] + 200, PANEL[3] + 30))
        R.caption(d, cap); return im
    if sid == "ouvrir":
        if p < 0.7:
            return act(site(panel=True), lambda: screen("pdf"), PITEM, (W / 2, H / 2 + 100), t, 0.7 * D / 0.9, cap, show_loupe=False)
        im = screen("pdf"); d = ImageDraw.Draw(im); O.label(d, "Bravo !", (W / 2, PAGE_Y + 300)); R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "image":
        return act(site(), site(menu=True), IMG, (W / 2 - 300, H / 2 + 150), t, D, cap, show_loupe=False, right=True)
    if sid == "menu":
        return act(site(menu=True), site(dialog=True), SAVE_ITEM, R.center(IMG), t, D, cap, place=(420, 470))
    if sid == "enregistrer":
        if p < 0.35:
            im = site(dialog=True)(); clean = im.copy(); d = ImageDraw.Draw(im)
            if p > 0.08: R.highlight(d, DNAV, t); R.loupe(im, DNAV, place=(560, 560), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        tt = t - 0.35 * D; DD = 0.65 * D
        if tt < 0.75 * DD:
            return act(site(dialog=True), site(saved="fleur.png est enregistrée"), BTN_OK, R.center(DNAV), tt, 0.75 * DD / 0.9, cap, place=(500, 500))
        im = site(saved="fleur.png est enregistrée")(); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "retrouver":
        q = D / 2
        if t < q:
            return act(lambda: screen(), lambda: screen("explorer"), R.rect_of("explorer"), (W / 2 - 200, H / 2), t, q, cap, place=(640, 330))
        tt = t - q
        if tt < 0.75 * q:
            return act(lambda: screen("explorer"), lambda: screen("explorer", view="Téléchargements"), R.rect_of("nav:Téléchargements"), (W / 2, H / 2 + 100), tt, 0.75 * q / 0.9, cap, place=(1000, 330))
        im = screen("explorer", view="Téléchargements"); d = ImageDraw.Draw(im); O.label(d, "ils sont tous là", (850, 520)); R.caption(d, cap); return im
    if sid == "prudence":
        im = R.card("Prudence", ["Téléchargez seulement sur des sites", "que vous connaissez.", "En cas de doute :"], "Pas de panique : on peut toujours annuler.")
        d = ImageDraw.Draw(im); r = (W / 2 - 100, 360, W / 2 + 100, 420)
        if p > 0.45:
            d.rounded_rectangle(r, 10, fill=(240, 242, 246), outline=(150, 155, 170), width=3); tw = d.textlength("Annuler", font=F(30, "s"))
            d.text((W / 2 - tw / 2, 370), "Annuler", font=F(30, "s"), fill=(20, 20, 20)); R.highlight(d, r, t)
        return im
    if sid == "exercice":
        return R.card("Exercice", ["Enregistrez une image :", "1. clic droit sur l'image", "2. Enregistrer l'image sous", "3. Enregistrer"], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Clic droit sur une image,", "Enregistrer l'image sous, puis Enregistrer."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 3
        if t < q: return act(site(), site(menu=True), IMG, (W / 2 - 300, H / 2 + 150), t, q, cap, show_loupe=False, right=True)
        if t < 2 * q: return act(site(menu=True), site(dialog=True), SAVE_ITEM, R.center(IMG), t - q, q, cap, show_loupe=False)
        return act(site(dialog=True), site(saved="fleur.png est enregistrée"), BTN_OK, R.center(DNAV), t - 2 * q, q, cap, show_loupe=False)
    if sid == "resume":
        return R.card("À retenir", ["Télécharger = copier sur l'ordinateur", "Un document : cliquer sur le lien", "Une image : clic droit,", "« Enregistrer l'image sous »", "Tout arrive dans Téléchargements"], "Bravo ! À bientôt à Espace 19 Numérique !")
    raise KeyError(sid)

def main(script, durs, out):
    sc = json.load(open(script)); du = json.load(open(durs))
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    total = 0
    for s in sc["scenes"]:
        D = du[s["id"]]; n = int(round(D * FPS)); total += n
        for i in range(n):
            im = frame(s["id"], i / FPS, D, s["caption"])
            R.subtitle(im, R.sub_at(s["narration"], i / FPS, D, s.get("_start", 0.4)))
            pr.stdin.write(im.tobytes())
    pr.stdin.close(); pr.wait()
    print("frames", total, "duree", total / FPS)

def estimate(script):
    sc = json.load(open(script)); MARGE = sc.get("marges", {})
    out = {}
    for s in sc["scenes"]:
        if s["id"] == "attente": out[s["id"]] = 10.0
        elif not s["narration"]: out[s["id"]] = 3.0
        else: out[s["id"]] = round(len(s["narration"]) / 15 + 1.0 + MARGE.get(s["id"], 0.4), 1)
    return out

if __name__ == "__main__":
    if sys.argv[1] == "--estimate":
        json.dump(estimate(sys.argv[2]), open(sys.argv[3], "w"), indent=1); print(open(sys.argv[3]).read())
    else:
        main(*sys.argv[1:4])
