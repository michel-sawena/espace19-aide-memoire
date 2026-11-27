"""Vidéo « 25 - Doctolib » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_25.py script.json durations.json out.mp4
        python3 render_25.py --estimate script.json durations.json
Réutilise ../render_01.py et ../01-ordinateur/render_01_ordinateur.py.
Écrans SIMPLIFIÉS et NEUTRES : ni logo, ni couleurs, ni charte de Doctolib ; mention « dessin simplifié » ;
praticiens, adresses et motifs INVENTÉS (marqués « exemple »).
Libellés écrits tels quels (deux sources, voir sources_25.md) : « Rechercher », « Mes rendez-vous ».
Les boutons « prendre / confirmer / annuler » portent un pictogramme (✓, ✕), pas de texte.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
from PIL import ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); GRIS = (110, 110, 120)
BTN = (55, 60, 75); CORAIL = (255, 122, 89)
ADRESSE = "doctolib.fr"; METIER = "médecin généraliste"; VILLE = "Paris 19e"

BX, BY, BW, BH = 120, 60, 1040, 590
TAB_H, BAR_Y = 40, 60 + 40
ADDR = (BX + 150, BAR_Y + 10, BX + BW - 120, BAR_Y + 50)
PAGE_Y = BAR_Y + 62
EDGE = (lambda c: (c[0] - 24, c[1] - 22, c[0] + 24, c[1] + 22))(R.taskbar_icons()["edge"])
# zones cliquables (page)
F1 = (BX + 90, PAGE_Y + 130, BX + 480, PAGE_Y + 180)
F2 = (BX + 500, PAGE_Y + 130, BX + 760, PAGE_Y + 180)
RECH = (BX + 780, PAGE_Y + 130, BX + 950, PAGE_Y + 180)
PERSO = (BX + BW - 90, PAGE_Y + 14, BX + BW - 30, PAGE_Y + 60)
MENU_RDV = (BX + BW - 300, PAGE_Y + 70, BX + BW - 30, PAGE_Y + 115)
JOURS = ["lun. 30", "mar. 1er", "mer. 2"]
HEURES = [["09:00", "11:15"], ["10:30", "14:00"], ["08:45", "16:30"]]
def chip(card, j, k):
    x = BX + 600 + j * 135; y = PAGE_Y + 70 + card * 190 + 50 + k * 52
    return (x, y, x + 110, y + 40)
CREN = chip(0, 1, 0)
MOT1 = (BX + 260, PAGE_Y + 140, BX + 780, PAGE_Y + 190)
OKB = (BX + 420, PAGE_Y + 330, BX + 620, PAGE_Y + 385)
RDVC = (BX + 160, PAGE_Y + 120, BX + 880, PAGE_Y + 230)
ANN = (BX + 640, PAGE_Y + 260, BX + 760, PAGE_Y + 310)
RAIS1 = (BX + 260, PAGE_Y + 150, BX + 780, PAGE_Y + 200)
OKA = (BX + 420, PAGE_Y + 330, BX + 620, PAGE_Y + 385)

def globe(d, cx, cy, r, col=(0, 120, 200), line=(255, 255, 255)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col); w = max(2, int(r / 9))
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=line, width=w)
    d.line([cx, cy - r, cx, cy + r], fill=line, width=w); d.line([cx - r, cy, cx + r, cy], fill=line, width=w)

def check(d, cx, cy, s, col=(255, 255, 255), w=5):
    d.line([cx - s, cy, cx - s * 0.3, cy + s * 0.7, cx + s, cy - s * 0.7], fill=col, width=w, joint="curve")

def cross(d, cx, cy, s, col=(255, 255, 255), w=5):
    d.line([cx - s, cy - s, cx + s, cy + s], fill=col, width=w); d.line([cx - s, cy + s, cx + s, cy - s], fill=col, width=w)

def person(d, cx, cy, s, col=INK):
    d.ellipse([cx - s * 0.45, cy - s, cx + s * 0.45, cy - s * 0.1], outline=col, width=3)
    d.arc([cx - s * 0.9, cy, cx + s * 0.9, cy + s * 1.6], 180, 360, fill=col, width=3)

def field(d, r, text, ph, focus=False):
    d.rounded_rectangle(r, 10, fill=(255, 255, 255), outline=(0, 103, 192) if focus else (170, 175, 185), width=3 if focus else 2)
    d.text((r[0] + 16, r[1] + 12), text or ph, font=F(20), fill=(20, 20, 20) if text else GRIS)
    if focus:
        x = r[0] + 16 + d.textlength(text, font=F(20)) + 2; d.line([x, r[1] + 10, x, r[3] - 10], fill=(20, 20, 20), width=2)

def btn(d, r, text=None, icon=None, col=BTN):
    d.rounded_rectangle(r, 12, fill=col); cx, cy = R.center(r)
    if icon == "ok": check(d, cx, cy, 14)
    elif icon == "x": cross(d, cx, cy, 11)
    if text:
        f = F(21, "b"); tw = d.textlength(text, font=f); d.text((cx - tw / 2, cy - 13), text, font=f, fill=(255, 255, 255))

def note(d, x, y, t="dessin simplifié"):
    d.text((x, y), f"({t})", font=F(16), fill=GRIS)

def page(d, st):
    pg = st.get("page"); X0 = BX + 2
    if pg is None:
        globe(d, BX + BW / 2, PAGE_Y + 180, 60, (230, 236, 246), (190, 200, 220)); return
    person(d, *R.center(PERSO), 18); note(d, BX + 30, PAGE_Y + 16)
    if pg == "accueil":
        f = F(30, "b"); t = "Chercher un praticien"; d.text((BX + BW / 2 - d.textlength(t, font=f) / 2, PAGE_Y + 62), t, font=f, fill=INK)
        field(d, F1, st.get("m", ""), "métier ou nom", st.get("foc") == 1)
        field(d, F2, st.get("v", ""), "ville", st.get("foc") == 2)
        btn(d, RECH, "Rechercher")
    elif pg == "liste":
        d.text((BX + 30, PAGE_Y + 40), f"{METIER} · {VILLE}", font=F(20, "b"), fill=INK)
        for c, (nom, adr) in enumerate((("Dr Martin", "12 rue des Lilas"), ("Dr Bernard", "5 avenue des Roses"))):
            y = PAGE_Y + 70 + c * 190
            d.rounded_rectangle([BX + 30, y, BX + BW - 30, y + 175], 12, fill=(248, 248, 250), outline=(205, 208, 215), width=2)
            d.ellipse([BX + 50, y + 25, BX + 110, y + 85], fill=(215, 218, 226)); person(d, BX + 80, y + 52, 16, GRIS)
            d.text((BX + 130, y + 25), nom, font=F(24, "b"), fill=INK)
            d.text((BX + 130, y + 60), METIER, font=F(19), fill=INK); d.text((BX + 130, y + 90), adr, font=F(19), fill=INK)
            d.text((BX + 130, y + 125), "(exemple)", font=F(16), fill=GRIS)
            for j, jr in enumerate(JOURS):
                x = BX + 600 + j * 135; d.text((x + 10, y + 15), jr, font=F(18, "b"), fill=INK)
                for k, hh in enumerate(HEURES[(j + c) % 3]):
                    r = chip(c, j, k); sel = st.get("sel") and r == CREN
                    d.rounded_rectangle(r, 8, fill=(255, 236, 160) if sel else (225, 232, 245), outline=(120, 130, 150), width=1)
                    d.text((r[0] + 26, r[1] + 8), hh, font=F(20, "b"), fill=INK)
    elif pg == "motif":
        d.text((BX + 260, PAGE_Y + 60), "Dr Martin · mardi 1er · 10:30", font=F(22, "b"), fill=INK)
        d.text((BX + 260, PAGE_Y + 100), "Quel est le motif ?", font=F(20), fill=INK)
        for i, m in enumerate(("Consultation de suivi", "Première consultation", "Renouvellement d'ordonnance")):
            r = (MOT1[0], MOT1[1] + i * 62, MOT1[2], MOT1[3] + i * 62); sel = st.get("sel") and i == 0
            d.rounded_rectangle(r, 10, fill=(255, 246, 214) if sel else (255, 255, 255), outline=(170, 175, 185), width=2)
            d.ellipse([r[0] + 16, r[1] + 15, r[0] + 36, r[1] + 35], outline=INK, width=2)
            if sel: d.ellipse([r[0] + 21, r[1] + 20, r[0] + 31, r[1] + 30], fill=INK)
            d.text((r[0] + 50, r[1] + 12), m, font=F(20), fill=INK)
        note(d, BX + 260, PAGE_Y + 330, "motifs : exemples")
    elif pg in ("recap", "ok"):
        d.rounded_rectangle([BX + 260, PAGE_Y + 60, BX + 780, PAGE_Y + 300], 14, fill=(248, 248, 250), outline=(205, 208, 215), width=2)
        for i, (lab, val) in enumerate((("Praticien", "Dr Martin (exemple)"), ("Jour", "mardi 1er décembre"), ("Heure", "10:30"), ("Adresse", "12 rue des Lilas"), ("Motif", "Consultation de suivi"))):
            d.text((BX + 290, PAGE_Y + 80 + i * 42), lab, font=F(19), fill=GRIS); d.text((BX + 430, PAGE_Y + 80 + i * 42), val, font=F(20, "b"), fill=INK)
        if pg == "recap": btn(d, OKB, icon="ok", col=VERT)
        else:
            d.ellipse([BX + 480, PAGE_Y + 320, BX + 560, PAGE_Y + 400], fill=VERT); check(d, BX + 520, PAGE_Y + 360, 20, w=7)
    elif pg == "menu":
        d.text((BX + 30, PAGE_Y + 70), "", font=F(20))
        d.rounded_rectangle([MENU_RDV[0], MENU_RDV[1] - 6, MENU_RDV[2], MENU_RDV[3] + 54], 10, fill=(255, 255, 255), outline=(170, 175, 185), width=2)
        d.text((MENU_RDV[0] + 18, MENU_RDV[1] + 10), "Mes rendez-vous", font=F(21, "b"), fill=INK)
        d.text((MENU_RDV[0] + 18, MENU_RDV[1] + 62), "…", font=F(21), fill=GRIS)
    elif pg in ("rdv", "detail", "raison", "annule"):
        d.text((BX + 160, PAGE_Y + 60), "Mes rendez-vous", font=F(28, "b"), fill=INK)
        gone = pg == "annule"
        d.rounded_rectangle(RDVC, 12, fill=(240, 240, 242) if gone else (248, 248, 250), outline=(205, 208, 215), width=2)
        col = GRIS if gone else INK
        d.text((RDVC[0] + 24, RDVC[1] + 18), "mardi 1er décembre · 10:30", font=F(23, "b"), fill=col)
        d.text((RDVC[0] + 24, RDVC[1] + 58), "Dr Martin (exemple) · 12 rue des Lilas", font=F(20), fill=col)
        if gone:
            d.line([RDVC[0] + 20, RDVC[1] + 33, RDVC[0] + 360, RDVC[1] + 33], fill=CORAIL, width=4)
            d.ellipse([BX + 480, PAGE_Y + 270, BX + 560, PAGE_Y + 350], fill=VERT); check(d, BX + 520, PAGE_Y + 310, 20, w=7)
        if pg == "detail": btn(d, ANN, icon="x", col=CORAIL)
        if pg == "raison":
            d.rounded_rectangle([BX + 220, PAGE_Y + 90, BX + 820, PAGE_Y + 400], 14, fill=(255, 255, 255), outline=(150, 155, 165), width=2)
            d.text((BX + 260, PAGE_Y + 108), "Pourquoi annulez-vous ?", font=F(20, "b"), fill=INK)
            for i, m in enumerate(("Empêchement", "Autre raison")):
                r = (RAIS1[0], RAIS1[1] + i * 62, RAIS1[2], RAIS1[3] + i * 62); sel = st.get("sel") and i == 0
                d.rounded_rectangle(r, 10, fill=(255, 246, 214) if sel else (255, 255, 255), outline=(170, 175, 185), width=2)
                d.ellipse([r[0] + 16, r[1] + 15, r[0] + 36, r[1] + 35], outline=INK, width=2)
                if sel: d.ellipse([r[0] + 21, r[1] + 20, r[0] + 31, r[1] + 30], fill=INK)
                d.text((r[0] + 50, r[1] + 12), m, font=F(20), fill=INK)
            btn(d, OKA, icon="ok", col=VERT)

def browser(d, st):
    d.rounded_rectangle([BX + 6, BY + 8, BX + BW + 6, BY + BH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([BX, BY, BX + BW, BY + BH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([BX, BY, BX + BW, BY + TAB_H + 10], 10, fill=(222, 226, 236)); d.rectangle([BX, BY + 20, BX + BW, BY + TAB_H], fill=(222, 226, 236))
    d.rounded_rectangle([BX + 12, BY + 6, BX + 300, BY + TAB_H + 4], 8, fill=(250, 250, 252)); globe(d, BX + 32, BY + 23, 9)
    d.text((BX + 50, BY + 12), "doctolib.fr" if st.get("page") else "Nouvel onglet", font=F(17), fill=(30, 30, 30))
    d.rectangle([BX + 2, BAR_Y, BX + BW - 2, BAR_Y + 60], fill=(250, 250, 252))
    typed, focus = st.get("addr", ""), st.get("addr_focus", False)
    d.rounded_rectangle(ADDR, 20, fill=(255, 255, 255) if focus else (238, 240, 244), outline=(0, 103, 192) if focus else (200, 204, 212), width=3 if focus else 1)
    d.text((ADDR[0] + 22, ADDR[1] + 9), typed, font=F(20), fill=(20, 20, 20))
    if focus:
        x = ADDR[0] + 22 + d.textlength(typed, font=F(20)) + 2; d.line([x, ADDR[1] + 9, x, ADDR[3] - 9], fill=(20, 20, 20), width=2)
    d.line([BX + 2, PAGE_Y, BX + BW - 2, PAGE_Y], fill=(215, 218, 225), width=1)
    page(d, st)

def screen(**st):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if st: browser(d, st)
    return im

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None):
    c = R.center(r); tc = 0.6 * D
    im = (after if t >= tc + 0.3 else before)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    R.caption(d, cap); return im

def typing(s, t, t0, t1):
    return s[:int(len(s) * max(0, min(1, (t - t0) / max(t1 - t0, 0.1))))]

A = dict(addr=ADRESSE)
def recherche(t, D, cap, show_loupe=True):
    """clic case 1, tape métier, clic case 2, tape ville, clic Rechercher."""
    q = D / 5
    if t < q: return act(lambda: screen(page="accueil", **A), lambda: screen(page="accueil", foc=1, **A), F1, (W / 2, 520), t, q, cap, show_loupe=False)
    if t < 2 * q:
        im = screen(page="accueil", foc=1, m=typing(METIER, t, q, 1.8 * q), **A); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if t < 3 * q: return act(lambda: screen(page="accueil", m=METIER, **A), lambda: screen(page="accueil", m=METIER, foc=2, **A), F2, R.center(F1), t - 2 * q, q, cap, show_loupe=False)
    if t < 3.8 * q:
        im = screen(page="accueil", m=METIER, foc=2, v=typing(VILLE, t, 3 * q, 3.7 * q), **A); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    tt = t - 3.8 * q; dd = 1.2 * q
    return act(lambda: screen(page="accueil", m=METIER, v=VILLE, **A), lambda: screen(page="liste", **A), RECH, R.center(F2), tt, dd, cap, show_loupe=show_loupe, place=(640, 470))

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Doctolib : prendre rendez-vous", ["Aide-mémoire n° 25 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([W / 2 - 70, 300, W / 2 + 70, 420], 12, fill=(255, 255, 255), outline=VIO, width=5)
        d.rectangle([W / 2 - 70, 300, W / 2 + 70, 335], fill=VIO); check(d, W / 2, 378, 26, VERT, 8); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im)
        # agenda
        d.rounded_rectangle([340, 150, 940, 470], 16, fill=(255, 255, 255), outline=INK, width=4); d.rectangle([340, 150, 940, 205], fill=VIO)
        for j in range(4):
            for k in range(3):
                x, y = 370 + j * 140, 230 + k * 75; free = (j + k) % 2 == 0
                d.rounded_rectangle([x, y, x + 120, y + 55], 8, fill=(225, 245, 240) if free else (230, 230, 234), outline=(150, 150, 160))
                if free and p > 0.5: R.highlight(d, (x, y, x + 120, y + 55), t)
        if p > 0.2: O.label(d, "l'agenda du secrétariat", (640, 510))
        if p > 0.6: O.label(d, "ouvert jour et nuit", (640, 110))
        R.caption(d, cap); return im
    if sid == "compte":
        im = O.room(); d = ImageDraw.Draw(im)
        for i, (lab, x) in enumerate((("adresse mail", 420), ("téléphone", 860))):
            if p > 0.15 + i * 0.25:
                d.ellipse([x - 90, 190, x + 90, 370], fill=(255, 255, 255), outline=VIO, width=6)
                if i == 0:
                    d.rectangle([x - 50, 250, x + 50, 315], outline=INK, width=5); d.line([x - 50, 250, x, 290, x + 50, 250], fill=INK, width=5)
                else:
                    d.rounded_rectangle([x - 28, 225, x + 28, 335], 10, outline=INK, width=5)
                O.label(d, lab, (x, 420))
        if p > 0.7: O.label(d, "Pas de panique, prenez votre temps", (640, 520))
        R.caption(d, cap); return im
    if sid == "adresse":
        q = D / 3
        if t < q: return act(lambda: screen(), lambda: screen(addr="", page=None), EDGE, (W / 2 - 200, H / 2), t, q, cap, show_loupe=False)
        if t < 2.2 * q:
            if t < 1.3 * q:
                return act(lambda: screen(addr=""), lambda: screen(addr="", addr_focus=True), ADDR, (W / 2, 500), t - q, 0.3 * q / 0.9, cap, show_loupe=False)
            im = screen(addr=typing(ADRESSE, t, 1.35 * q, 2.1 * q), addr_focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
            R.loupe(im, (ADDR[0], ADDR[1], ADDR[0] + 240, ADDR[3]), place=(640, 420), clean=clean); d = ImageDraw.Draw(im); R.caption(d, cap); return im
        tt = t - 2.2 * q
        if tt < 0.45 * q:
            im = screen(addr=ADRESSE, addr_focus=True); d = ImageDraw.Draw(im); R.key_enter(d, tt, tt > 0.25 * q)
        else:
            im = screen(page="accueil", **A); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "recherche":
        return recherche(t, D, cap)
    if sid == "liste":
        im = screen(page="liste", **A); d = ImageDraw.Draw(im)
        if p > 0.45:
            r = (BX + 590, PAGE_Y + 75, BX + 1000, PAGE_Y + 245); R.highlight(d, r, t); O.label(d, "les heures libres", (W / 2 + 150, PAGE_Y + 270))
        R.caption(d, cap); return im
    if sid == "creneau":
        return act(lambda: screen(page="liste", **A), lambda: screen(page="motif", **A), CREN, (W / 2, 560), t, D * 0.7, cap, place=(400, 470)) if t < 0.7 * D * 0.6 / 0.6 + 0.3 else _motif_intro(t, cap)
    if sid == "motif":
        if t < 0.65 * D:
            return act(lambda: screen(page="motif", **A), lambda: screen(page="motif", sel=True, **A), MOT1, (W / 2, 560), t, 0.65 * D, cap, show_loupe=False)
        im = screen(page="motif", sel=True, **A); d = ImageDraw.Draw(im)
        R.highlight(d, PERSO, t); R.arrow(d, PERSO, t); O.label(d, "se connecter, si on vous le demande", (BX + BW - 330, PAGE_Y + 110))
        R.caption(d, cap); return im
    if sid == "confirmer":
        if t < 0.35 * D:
            im = screen(page="recap", **A); d = ImageDraw.Draw(im)
            R.highlight(d, (BX + 280, PAGE_Y + 115, BX + 770, PAGE_Y + 245), t); R.caption(d, cap); return im
        tt = t - 0.35 * D; dd = 0.45 * D
        if tt < dd * 0.6 + 0.3:
            return act(lambda: screen(page="recap", **A), lambda: screen(page="ok", **A), OKB, (W / 2, 300), tt, dd, cap, place=(900, 470))
        im = screen(page="ok", **A); d = ImageDraw.Draw(im); O.label(d, "Bravo !", (W / 2, PAGE_Y + 440)); R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et regardez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "mesrdv":
        h = D / 2
        if t < h: return act(lambda: screen(page="accueil", **A), lambda: screen(page="menu", **A), PERSO, (W / 2, 450), t, h, cap, show_loupe=False)
        tt = t - h
        if tt < h * 0.6 + 0.3:
            return act(lambda: screen(page="menu", **A), lambda: screen(page="rdv", **A), MENU_RDV, R.center(PERSO), tt, h, cap, place=(600, 420))
        im = screen(page="rdv", **A); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "annuler":
        q = D / 4
        if t < q: return act(lambda: screen(page="rdv", **A), lambda: screen(page="detail", **A), RDVC, (W / 2, 560), t, q, cap, show_loupe=False)
        if t < 2 * q: return act(lambda: screen(page="detail", **A), lambda: screen(page="raison", **A), ANN, R.center(RDVC), t - q, q, cap, place=(400, 450))
        if t < 3 * q:
            tt = t - 2 * q
            if tt < 0.5 * q: return act(lambda: screen(page="raison", **A), lambda: screen(page="raison", sel=True, **A), RAIS1, R.center(ANN), tt, 0.5 * q, cap, show_loupe=False)
            return act(lambda: screen(page="raison", sel=True, **A), lambda: screen(page="annule", **A), OKA, R.center(RAIS1), tt - 0.5 * q, 0.5 * q, cap, show_loupe=False)
        im = screen(page="annule", **A); d = ImageDraw.Draw(im); O.label(d, "la place est libérée", (W / 2, PAGE_Y + 400)); R.caption(d, cap); return im
    if sid == "delai":
        im = O.room(); d = ImageDraw.Draw(im)
        cx, cy = 430, 300; d.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], fill=(255, 255, 255), outline=INK, width=6)
        d.line([cx, cy, cx, cy - 75], fill=INK, width=7); d.line([cx, cy, cx + 55, cy + 20], fill=INK, width=7)
        if p > 0.45:
            x = 850; d.rounded_rectangle([x - 60, 190, x + 60, 410], 18, fill=(40, 44, 54)); d.rectangle([x - 48, 215, x + 48, 375], fill=(120, 190, 140))
            R.highlight(d, (x - 70, 180, x + 70, 420), t); O.label(d, "téléphonez au cabinet", (x, 460))
        else: O.label(d, "peu de temps avant", (cx, 460))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Sur doctolib.fr, cherchez", "un médecin généraliste", "dans votre ville.", "Regardez les heures libres,", "sans réserver."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Cherchez un médecin généraliste", "dans votre ville, sans réserver."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        if t < 0.8 * D: return recherche(t, 0.8 * D, cap, show_loupe=False)
        im = screen(page="liste", **A); d = ImageDraw.Draw(im); R.highlight(d, (BX + 590, PAGE_Y + 75, BX + 1000, PAGE_Y + 245), t); R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Cherchez le métier et la ville", "Cliquez sur une heure libre", "Choisissez le motif, puis confirmez", "Pour annuler : Mes rendez-vous"], "Bravo ! À bientôt à Espace 19 Numérique !")
    raise KeyError(sid)

def _motif_intro(t, cap):
    im = screen(page="motif", **A); d = ImageDraw.Draw(im); R.caption(d, cap); return im

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
