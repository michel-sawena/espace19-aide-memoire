"""Vidéo « 23 - La CAF en ligne » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_23.py script.json durations.json out.mp4
        python3 render_23.py --estimate script.json durations.json
Réutilise ../12-internet/render_12.py (navigateur dessiné, clic animé) et ../render_01.py.
Écrans SIMPLIFIÉS et NEUTRES : aucun logo, aucune couleur ni charte du site officiel ; « caf.fr » n'apparaît
qu'en texte simple. Libellés écrits tels quels car confirmés par les fiches officielles (voir sources_23.md) :
« Mon Compte », « Se connecter », « Mot de passe oublié ? », « S'identifier avec FranceConnect », « Envoyer le code »,
« Mes attestations », « Mes démarches », « Mon profil », « Télécharger », « Recevoir par courrier », « Déconnexion »,
« Mois précédent », « Une autre période ». Les petites légendes des cases (« numéro de sécurité sociale »…) sont
descriptives. Les chiffres affichés sont des EXEMPLES inventés.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as B
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); CORAIL = (255, 122, 89)
SLATE = (55, 65, 85); GRIS = (215, 218, 226); GRIS2 = (236, 238, 243)
BX, BY, BW, BH, PAGE_Y = B.BX, B.BY, B.BW, B.BH, B.PAGE_Y
L, Rr = BX + 2, BX + BW - 2
ADRESSE = "caf.fr"
NUM_EX = "1 23 45 67 890 12"

# zones cliquables
MONCOMPTE = (Rr - 230, PAGE_Y + 12, Rr - 20, PAGE_Y + 52)
PX0, PX1 = 400, 880
F1 = (PX0 + 20, PAGE_Y + 128, PX1 - 20, PAGE_Y + 168)
F2 = (PX0 + 20, PAGE_Y + 205, PX1 - 20, PAGE_Y + 245)
OUBLI = (PX0 + 20, PAGE_Y + 252, PX0 + 220, PAGE_Y + 276)
BTN_CO = (PX0 + 20, PAGE_Y + 288, PX1 - 20, PAGE_Y + 330)
BTN_FC = (PX0 + 20, PAGE_Y + 342, PX1 - 20, PAGE_Y + 380)
BTN_ENV = (PX0 + 120, PAGE_Y + 150, PX1 - 120, PAGE_Y + 192)
CODE_ROW = (PX0 + 60, PAGE_Y + 220, PX1 - 60, PAGE_Y + 270)
BTN_OK = (PX1 - 150, PAGE_Y + 290, PX1 - 60, PAGE_Y + 332)
DECO = (Rr - 190, PAGE_Y + 14, Rr - 20, PAGE_Y + 50)
TILES = [("Mes attestations", (L + 60, PAGE_Y + 110, L + 360, PAGE_Y + 230)),
         ("Mes démarches", (L + 370 + 6, PAGE_Y + 110, L + 676, PAGE_Y + 230)),
         ("Mon profil", (L + 692, PAGE_Y + 110, L + 992, PAGE_Y + 230))]
TILE_ATT = TILES[0][1]
R_PAI = (L + 80, PAGE_Y + 110, L + 520, PAGE_Y + 146)
R_QF = (L + 80, PAGE_Y + 156, L + 520, PAGE_Y + 192)
R_MOIS = (L + 560, PAGE_Y + 110, L + 900, PAGE_Y + 146)
R_AUTRE = (L + 560, PAGE_Y + 156, L + 900, PAGE_Y + 192)
BTN_TEL = (L + 80, PAGE_Y + 230, L + 330, PAGE_Y + 274)
BTN_COUR = (L + 350, PAGE_Y + 230, L + 660, PAGE_Y + 274)

def ctext(d, txt, cx, y, f, col=INK):
    d.text((cx - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col)

def bouton(d, r, txt, plein=True, size=20):
    d.rounded_rectangle(r, 8, fill=SLATE if plein else (255, 255, 255), outline=SLATE, width=2)
    f = F(size, "b"); ctext(d, txt, (r[0] + r[2]) / 2, (r[1] + r[3]) / 2 - size * 0.62, f, (255, 255, 255) if plein else SLATE)

def personne(d, cx, cy, col=SLATE):
    d.ellipse([cx - 7, cy - 12, cx + 7, cy + 2], fill=col); d.pieslice([cx - 12, cy + 2, cx + 12, cy + 24], 180, 360, fill=col)

def entete(d, connecte=False):
    d.rectangle([L, PAGE_Y + 1, Rr, PAGE_Y + 64], fill=GRIS2)
    d.text((L + 24, PAGE_Y + 16), "caf.fr", font=F(26, "b"), fill=SLATE)
    d.text((L + 130, PAGE_Y + 24), "(dessin simplifié)", font=F(15), fill=(110, 110, 120))
    if connecte:
        d.text((L + 330, PAGE_Y + 18), "Mon Compte", font=F(24, "b"), fill=INK)
        d.rounded_rectangle(DECO, 8, fill=(255, 255, 255), outline=SLATE, width=2)
        ctext(d, "Déconnexion", (DECO[0] + DECO[2]) / 2, DECO[1] + 7, F(19, "b"), SLATE)
    else:
        d.rounded_rectangle(MONCOMPTE, 8, fill=(255, 255, 255), outline=SLATE, width=2)
        personne(d, MONCOMPTE[0] + 30, MONCOMPTE[1] + 16)
        d.text((MONCOMPTE[0] + 54, MONCOMPTE[1] + 8), "Mon Compte", font=F(21, "b"), fill=SLATE)

def barres(d, x, y, w, n, h=12, gap=22):
    for i in range(n):
        d.rounded_rectangle([x, y + i * gap, x + w * (1 - 0.18 * (i % 3)), y + i * gap + h], 5, fill=GRIS)

def page(d, kind, st):
    if kind == "accueil":
        entete(d)
        for i in range(3):
            x = L + 60 + i * 330
            d.rounded_rectangle([x, PAGE_Y + 110, x + 290, PAGE_Y + 300], 12, fill=(250, 250, 252), outline=GRIS, width=2)
            barres(d, x + 24, PAGE_Y + 140, 230, 5)
    elif kind == "connexion":
        entete(d)
        d.rounded_rectangle([PX0, PAGE_Y + 76, PX1, PAGE_Y + 395], 14, fill=(250, 250, 252), outline=GRIS, width=2)
        ctext(d, "Mon Compte", (PX0 + PX1) / 2, PAGE_Y + 84, F(24, "b"))
        d.text((F1[0], F1[1] - 24), "numéro de sécurité sociale (13 chiffres)", font=F(16), fill=INK)
        d.text((F2[0], F2[1] - 24), "mot de passe", font=F(16), fill=INK)
        for r, val, foc in ((F1, st.get("num", ""), st.get("focus") == 1), (F2, "•" * st.get("mdp", 0), st.get("focus") == 2)):
            d.rounded_rectangle(r, 6, fill=(255, 255, 255), outline=(0, 103, 192) if foc else (160, 165, 175), width=3 if foc else 2)
            d.text((r[0] + 14, r[1] + 7), val, font=F(22, "s"), fill=INK)
            if foc:
                x = r[0] + 14 + d.textlength(val, font=F(22, "s")) + 2; d.line([x, r[1] + 8, x, r[3] - 8], fill=INK, width=2)
        d.text((OUBLI[0], OUBLI[1] + 2), "Mot de passe oublié ?", font=F(16, "s"), fill=(0, 80, 170))
        d.line([OUBLI[0], OUBLI[1] + 21, OUBLI[0] + d.textlength("Mot de passe oublié ?", font=F(16, "s")), OUBLI[1] + 21], fill=(0, 80, 170), width=1)
        bouton(d, BTN_CO, "Se connecter")
        bouton(d, BTN_FC, "S'identifier avec FranceConnect", plein=False, size=17)
    elif kind == "code":
        entete(d)
        d.rounded_rectangle([PX0, PAGE_Y + 76, PX1, PAGE_Y + 350], 14, fill=(250, 250, 252), outline=GRIS, width=2)
        ctext(d, "Code de sécurité", (PX0 + PX1) / 2, PAGE_Y + 86, F(24, "b"))
        ctext(d, "Un code à 6 chiffres est envoyé par mail.", (PX0 + PX1) / 2, PAGE_Y + 120, F(17))
        bouton(d, BTN_ENV, "Envoyer le code", plein=not st.get("envoye"))
        if st.get("envoye"):
            code = st.get("code", ""); bw = (CODE_ROW[2] - CODE_ROW[0] - 50) / 6
            for i in range(6):
                x = CODE_ROW[0] + i * (bw + 10)
                d.rounded_rectangle([x, CODE_ROW[1], x + bw, CODE_ROW[3]], 6, fill=(255, 255, 255), outline=(160, 165, 175), width=2)
                if i < len(code): ctext(d, code[i], x + bw / 2, CODE_ROW[1] + 8, F(28, "b"))
            bouton(d, BTN_OK, "→", size=26)
    elif kind == "espace":
        entete(d, connecte=True)
        d.text((L + 60, PAGE_Y + 76), "Bonjour ! (espace personnel)", font=F(20, "s"), fill=INK)
        for n, r in TILES:
            d.rounded_rectangle(r, 12, fill=(250, 250, 252), outline=SLATE, width=2)
            ctext(d, n, (r[0] + r[2]) / 2, r[1] + 46, F(22, "b"), SLATE)
        barres(d, L + 60, PAGE_Y + 260, 900, 3)
    elif kind == "attest":
        entete(d, connecte=True)
        d.text((L + 60, PAGE_Y + 74), "Mes attestations", font=F(24, "b"), fill=INK)
        for r, n, on in ((R_PAI, "Attestation de paiement", st.get("pai")), (R_QF, "Attestation de quotient familial", False),
                         (R_MOIS, "Mois précédent", st.get("mois")), (R_AUTRE, "Une autre période", False)):
            cy = (r[1] + r[3]) / 2
            d.ellipse([r[0], cy - 11, r[0] + 22, cy + 11], outline=SLATE, width=3, fill=(255, 255, 255))
            if on: d.ellipse([r[0] + 6, cy - 5, r[0] + 16, cy + 5], fill=SLATE)
            d.text((r[0] + 34, cy - 13), n, font=F(20, "s"), fill=INK)
        bouton(d, BTN_TEL, "Télécharger")
        bouton(d, BTN_COUR, "Recevoir par courrier", plein=False)

def document(d, x=760, y=160):
    d.rectangle([x + 8, y + 8, x + 348, y + 438], fill=(60, 60, 70))
    d.rectangle([x, y, x + 340, y + 430], fill=(255, 255, 255), outline=INK, width=2)
    d.text((x + 24, y + 22), "ATTESTATION", font=F(24, "b"), fill=INK)
    d.text((x + 24, y + 54), "DE PAIEMENT", font=F(24, "b"), fill=INK)
    barres(d, x + 24, y + 110, 290, 8)
    d.text((x + 70, y + 330), "EXEMPLE", font=F(40, "b"), fill=CORAIL)

def screen(kind=None, **st):
    im = R.screen({"window": False})
    if kind is None: return im
    d = ImageDraw.Draw(im)
    B.browser(d, typed=st.pop("typed", ADRESSE if kind != "vide" else ""), focus=st.pop("focus_addr", False))
    d.rectangle([BX + 44, BY + 9, BX + 296, BY + 38], fill=(250, 250, 252))
    d.text((BX + 50, BY + 12), "caf.fr" if kind != "vide" else "Nouvel onglet", font=F(17), fill=(30, 30, 30))
    if kind != "vide":
        d.rectangle([L, PAGE_Y + 1, Rr, BY + BH - 4], fill=(255, 255, 255)); page(d, kind, st)
    if st.get("doc"): document(d)
    return im

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None):
    return B.act(before, after, r, start, t, D, cap, show_loupe, place)

# ---------- illustrations ----------
def carte_vitale(d, x, y):
    d.rounded_rectangle([x - 110, y - 70, x + 110, y + 70], 14, fill=(120, 190, 120), outline=INK, width=3)
    d.rounded_rectangle([x - 85, y - 30, x - 40, y + 5], 5, fill=(230, 200, 90), outline=INK, width=2)
    barres(d, x - 20, y - 30, 110, 3, 10, 18)

def cle(d, x, y):
    d.ellipse([x - 70, y - 30, x - 10, y + 30], outline=INK, width=10)
    d.line([x - 10, y, x + 80, y], fill=INK, width=12); d.line([x + 55, y, x + 55, y + 28], fill=INK, width=10); d.line([x + 75, y, x + 75, y + 22], fill=INK, width=10)

def enveloppe(d, x, y, s=1.0):
    d.rectangle([x - 90 * s, y - 58 * s, x + 90 * s, y + 58 * s], fill=(255, 255, 255), outline=INK, width=4)
    d.line([x - 90 * s, y - 58 * s, x, y + 6 * s, x + 90 * s, y - 58 * s], fill=INK, width=4)

def bulle_mail(d, p):
    x0, y0 = 860, 250
    d.rounded_rectangle([x0 + 6, y0 + 6, x0 + 386, y0 + 236], 16, fill=(60, 60, 70))
    d.rounded_rectangle([x0, y0, x0 + 380, y0 + 230], 16, fill=(255, 255, 255), outline=YEL, width=6)
    enveloppe(d, x0 + 60, y0 + 50, 0.35)
    d.text((x0 + 110, y0 + 32), "Votre boîte mail", font=F(22, "b"), fill=INK)
    d.text((x0 + 30, y0 + 92), "Votre code :", font=F(22), fill=INK)
    d.text((x0 + 30, y0 + 124), "482 913", font=F(46, "b"), fill=VIO)
    d.text((x0 + 230, y0 + 186), "EXEMPLE", font=F(22, "b"), fill=CORAIL)

def cadenas(d, x, y):
    d.arc([x - 40, y - 80, x + 40, y], 180, 360, fill=INK, width=14)
    d.rounded_rectangle([x - 60, y - 40, x + 60, y + 60], 12, fill=CORAIL, outline=INK, width=4)

CODE_EX = "482913"
ACC = lambda: screen("accueil")
CON = lambda **k: (lambda: screen("connexion", **k))

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("La CAF en ligne", ["Aide-mémoire n° 23 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); B.maison(d, W / 2 - 120, 330, (250, 236, 200)); enveloppe(d, W / 2 + 120, 360, 0.7); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); O.draw_fixe(d)
        if p > 0.15: B.maison(d, 1080, 170, (250, 236, 200)); O.label(d, "l'aide au logement", (1080, 280))
        if p > 0.45: O.label(d, "caf.fr", (640, 140))
        R.caption(d, cap); return im
    if sid == "avant":
        im = O.room(); d = ImageDraw.Draw(im)
        items = [(carte_vitale, 260, "carte Vitale", 0.12), (cle, 640, "mot de passe CAF", 0.4), (enveloppe, 1020, "boîte mail", 0.68)]
        for fn, x, lab, s in items:
            if p > s:
                fn(d, x, 300); O.label(d, lab, (x, 430))
                if s < p < s + 0.25: R.highlight(d, (x - 130, 210, x + 130, 390), t)
        R.caption(d, cap); return im
    if sid == "site":
        q = 0.22 * D
        if t < q:
            return act(lambda: screen("vide"), lambda: screen("vide", focus_addr=True), B.ADDR, (W / 2, 500), t, q / 0.6 - 0.01, cap, show_loupe=False)
        if t < 0.6 * D:
            n = int(len(ADRESSE) * min(1, (t - q) / (0.25 * D)))
            im = screen("vide", typed=ADRESSE[:n], focus_addr=True); clean = im.copy(); d = ImageDraw.Draw(im)
            R.loupe(im, (B.ADDR[0], B.ADDR[1], B.ADDR[0] + 240, B.ADDR[3]), place=(640, 420), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        if t < 0.78 * D:
            im = screen("vide", typed=ADRESSE, focus_addr=True); d = ImageDraw.Draw(im); R.key_enter(d, t, t > 0.68 * D)
        else:
            im = ACC(); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "moncompte":
        return act(ACC, CON(), MONCOMPTE, (W / 2, 450), t, D, cap, place=(640, 420))
    if sid == "identifiant":
        q = 0.25 * D
        if t < q:
            return act(CON(), CON(focus=1), F1, (W / 2, 520), t, q / 0.6 - 0.01, cap, show_loupe=False)
        n = int(len(NUM_EX) * min(1, (t - q) / (0.4 * D)))
        im = screen("connexion", focus=1, num=NUM_EX[:n]); clean = im.copy(); d = ImageDraw.Draw(im)
        R.loupe(im, (F1[0], F1[1], F1[0] + 260, F1[3]), place=(1000, 420), clean=clean); d = ImageDraw.Draw(im)
        if p > 0.55: carte_vitale(d, 240, 400); O.label(d, "sur la carte Vitale", (240, 500))
        d.text((F1[2] - 120, F1[1] + 10), "EXEMPLE", font=F(16, "b"), fill=CORAIL)
        R.caption(d, cap); return im
    if sid == "motdepasse":
        q = 0.2 * D
        if t < q:
            return act(CON(num=NUM_EX), CON(num=NUM_EX, focus=2), F2, (W / 2, 520), t, q / 0.6 - 0.01, cap, show_loupe=False)
        if t < 0.5 * D:
            n = int(10 * min(1, (t - q) / (0.25 * D)))
            im = screen("connexion", num=NUM_EX, focus=2, mdp=n); d = ImageDraw.Draw(im); R.caption(d, cap); return im
        return act(CON(num=NUM_EX, mdp=10), lambda: screen("code"), BTN_CO, R.center(F2), t - 0.5 * D, 0.5 * D, cap, place=(1000, 420))
    if sid == "code":
        if t < 0.3 * D:
            return act(lambda: screen("code"), lambda: screen("code", envoye=True), BTN_ENV, (W / 2, 520), t, 0.3 * D, cap, show_loupe=False)
        if t < 0.62 * D:
            im = screen("code", envoye=True); d = ImageDraw.Draw(im); bulle_mail(d, p); R.caption(d, cap); return im
        if t < 0.85 * D:
            n = int(6 * min(1, (t - 0.62 * D) / (0.18 * D)))
            im = screen("code", envoye=True, code=CODE_EX[:n]); d = ImageDraw.Draw(im); R.highlight(d, CODE_ROW, t); R.caption(d, cap); return im
        return act(lambda: screen("code", envoye=True, code=CODE_EX), lambda: screen("espace"), BTN_OK, R.center(CODE_ROW), t - 0.85 * D, 0.15 * D, cap, show_loupe=False)
    if sid == "secret":
        im = R.card("Ce code est secret", ["Ne le donnez à personne,", "même au téléphone."], "Un conseiller de la CAF ne vous le demandera jamais.")
        d = ImageDraw.Draw(im); cadenas(d, W / 2, 400); return im
    if sid == "espace":
        im = screen("espace"); d = ImageDraw.Draw(im)
        if p > 0.2: R.highlight(d, (TILES[0][1][0], TILES[0][1][1], TILES[2][1][2], TILES[2][1][3]), t)
        if p > 0.5: O.label(d, "Bravo !", (W / 2, PAGE_Y + 330))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "attest":
        if t < 0.45 * D:
            im = screen("espace"); d = ImageDraw.Draw(im); document(d, 820, 200); R.caption(d, cap); return im
        return act(lambda: screen("espace"), lambda: screen("attest"), TILE_ATT, (W / 2, 500), t - 0.45 * D, 0.55 * D, cap, place=(900, 420))
    if sid == "choix":
        h = 0.5 * D
        if t < h:
            return act(lambda: screen("attest"), lambda: screen("attest", pai=True), R_PAI, (W / 2, 520), t, h, cap, place=(1000, 450))
        return act(lambda: screen("attest", pai=True), lambda: screen("attest", pai=True, mois=True), R_MOIS, R.center(R_PAI), t - h, h, cap, place=(330, 450))
    if sid == "telecharger":
        if t < 0.55 * D:
            return act(lambda: screen("attest", pai=True, mois=True), lambda: screen("attest", pai=True, mois=True, doc=True), BTN_TEL, (W / 2, 520), t, 0.55 * D, cap, place=(900, 450))
        im = screen("attest", pai=True, mois=True, doc=True); d = ImageDraw.Draw(im)
        if p > 0.7: O.label(d, "enregistrer ou imprimer", (420, 520))
        R.caption(d, cap); return im
    if sid == "deconnexion":
        if t < 0.7 * D:
            return act(lambda: screen("espace"), ACC, DECO, (W / 2, 500), t, 0.7 * D, cap, place=(640, 430))
        im = ACC(); d = ImageDraw.Draw(im); O.label(d, "porte fermée à clé", (W / 2, PAGE_Y + 340)); R.caption(d, cap); return im
    if sid == "panique":
        if t < 0.5 * D:
            im = screen("connexion"); clean = im.copy(); d = ImageDraw.Draw(im)
            if p > 0.1:
                R.highlight(d, OUBLI, t); R.loupe(im, OUBLI, place=(1020, 420), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        im = O.room(); d = ImageDraw.Draw(im)
        f = F(80, "b"); ctext(d, "3230", 380, 220, f, VIO); O.label(d, "téléphone de la CAF", (380, 340))
        if p > 0.75: ctext(d, "Espace 19", 920, 230, F(60, "b"), VIO); O.label(d, "on vous aide", (920, 340))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Connectez-vous à Mon Compte,", "puis téléchargez", "une attestation de paiement."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Mon Compte, puis", "Mes attestations."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 4; k = min(3, int(t / q)); tt = t - k * q
        steps = [(ACC, CON(), MONCOMPTE), (CON(num=NUM_EX, mdp=10), lambda: screen("code"), BTN_CO),
                 (lambda: screen("espace"), lambda: screen("attest"), TILE_ATT),
                 (lambda: screen("attest", pai=True, mois=True), lambda: screen("attest", pai=True, mois=True, doc=True), BTN_TEL)]
        b, a, r = steps[k]
        return act(b, a, r, (W / 2, 520), tt, q, cap, show_loupe=False)
    if sid == "resume":
        return R.card("À retenir", ["Mon Compte sur caf.fr", "Carte Vitale + mot de passe", "Le code reçu par mail (secret)", "Toujours « Déconnexion » à la fin"], "Bravo ! À bientôt à Espace 19 Numérique !")
    raise KeyError(sid)

def main(script, durs, out):
    sc = json.load(open(script)); du = json.load(open(durs))
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "31", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
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
