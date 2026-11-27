"""Vidéo « 24 - impots.gouv.fr » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_24.py script.json durations.json out.mp4
        python3 render_24.py --estimate script.json durations.json
Réutilise ../render_01.py, ../01-ordinateur/render_01_ordinateur.py et ../12-internet/render_12.py (fenêtre du navigateur).
Écrans SIMPLIFIÉS ET NEUTRES : aucun logo, aucune Marianne, aucune couleur ni police du site officiel ; mention
« dessin simplifié » sur chaque page du site. Numéro fiscal, code et nom affichés : EXEMPLES inventés.
Libellés écrits tels quels (voir sources_24.md) : « espace Finances publiques », « numéro fiscal » (13 chiffres),
« Continuer », « FranceConnect », « messagerie sécurisée ». Le nom des rubriques de l'espace est décrit, pas recopié.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as B
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); BLEU = B.BLEU; GRIS = (110, 110, 120); CORAIL = (255, 122, 89)
ADRESSE = "impots.gouv.fr"
NUMFISC = "1234567890123"          # EXEMPLE inventé
BX, BY, BW, BH, PAGE_Y = B.BX, B.BY, B.BW, B.BH, B.PAGE_Y
CX = BX + BW / 2
# zones cliquables
CONNEX = (BX + BW - 330, PAGE_Y + 14, BX + BW - 24, PAGE_Y + 60)
CASE_NUM = (CX - 220, PAGE_Y + 150, CX + 220, PAGE_Y + 196)
BTN_CONT = (CX - 110, PAGE_Y + 220, CX + 110, PAGE_Y + 264)
CASE_MDP = (CX - 220, PAGE_Y + 150, CX + 220, PAGE_Y + 196)
BTN_FC = (CX - 150, PAGE_Y + 330, CX + 150, PAGE_Y + 376)
TUILES = [("Mes avis d'impôt", "doc"), ("Déclarer mes revenus", "stylo"), ("Payer mes impôts", "euro"), ("Messagerie sécurisée", "lettre")]
def tuile_rect(i):
    x0 = BX + 60 + (i % 2) * 470; y0 = PAGE_Y + 110 + (i // 2) * 130
    return (x0, y0, x0 + 440, y0 + 110)
QUITTER = (BX + BW - 210, PAGE_Y + 14, BX + BW - 24, PAGE_Y + 60)
ANNEE = (CX - 240, PAGE_Y + 150, CX + 240, PAGE_Y + 200)

def tab_title(d, txt):
    d.rounded_rectangle([BX + 12, BY + 6, BX + 300, BY + B.TAB_H + 4], 8, fill=(250, 250, 252))
    B.globe(d, BX + 32, BY + 23, 9); d.text((BX + 50, BY + 12), txt, font=F(17), fill=(30, 30, 30))

def btn(d, r, txt, fill=(60, 64, 80), col=(255, 255, 255), size=20):
    d.rounded_rectangle(r, 10, fill=fill)
    f = F(size, "b"); tw = d.textlength(txt, font=f); c = R.center(r)
    d.text((c[0] - tw / 2, c[1] - size * 0.62), txt, font=f, fill=col)

def case(d, r, txt="", focus=False, ph=""):
    d.rounded_rectangle(r, 6, fill=(255, 255, 255), outline=BLEU if focus else (150, 150, 160), width=3 if focus else 2)
    d.text((r[0] + 14, r[1] + 11), txt if txt else ph, font=F(22), fill=(20, 20, 20) if txt else GRIS)
    if focus:
        x = r[0] + 14 + d.textlength(txt, font=F(22)) + 2; d.line([x, r[1] + 9, x, r[3] - 9], fill=(20, 20, 20), width=2)

def entete(d, droite=None):
    d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, PAGE_Y + 74], fill=(242, 242, 246))
    d.text((BX + 30, PAGE_Y + 22), "impots.gouv.fr", font=F(28, "b"), fill=INK)
    d.text((BX + 270, PAGE_Y + 32), "(dessin simplifié)", font=F(16), fill=GRIS)
    if droite == "connexion": btn(d, CONNEX, "Connexion à mon espace", size=19)
    if droite == "quitter":
        d.ellipse([QUITTER[0] - 54, QUITTER[1] + 4, QUITTER[0] - 16, QUITTER[1] + 42], fill=(200, 200, 210))
        btn(d, QUITTER, "Déconnexion", fill=(255, 255, 255), col=INK, size=18); d.rounded_rectangle(QUITTER, 10, outline=INK, width=2)

def picto(d, kind, x, y):
    if kind == "doc":
        d.rectangle([x - 18, y - 24, x + 18, y + 24], fill=(255, 255, 255), outline=INK, width=3)
        for k in range(4): d.line([x - 10, y - 12 + k * 9, x + 10, y - 12 + k * 9], fill=INK, width=2)
    elif kind == "stylo":
        d.line([x - 18, y + 20, x + 18, y - 20], fill=INK, width=8); d.polygon([(x - 22, y + 26), (x - 20, y + 14), (x - 12, y + 22)], fill=INK)
    elif kind == "euro":
        d.ellipse([x - 24, y - 24, x + 24, y + 24], outline=INK, width=3); d.text((x - 9, y - 17), "€", font=F(28, "b"), fill=INK)
    else:
        d.rectangle([x - 24, y - 16, x + 24, y + 18], fill=(255, 255, 255), outline=INK, width=3); d.line([x - 24, y - 16, x, y + 4, x + 24, y - 16], fill=INK, width=3)

def site(d, page, typed="", focus=False, hover=None):
    """Contenu dessiné de la page (après B.browser)."""
    d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, BY + BH - 2], fill=(255, 255, 255))
    if page == "accueil":
        tab_title(d, "impots.gouv.fr"); entete(d, "connexion")
        d.text((BX + 60, PAGE_Y + 120), "Particulier", font=F(40, "b"), fill=INK)
        for i, l in enumerate(("Mon espace Finances publiques", "Questions fréquentes", "Contact")):
            d.rounded_rectangle([BX + 60, PAGE_Y + 200 + i * 70, BX + 560, PAGE_Y + 250 + i * 70], 8, fill=(246, 246, 250))
            d.text((BX + 80, PAGE_Y + 212 + i * 70), l, font=F(20), fill=INK)
    elif page in ("numero", "mdp", "code"):
        tab_title(d, "Connexion"); entete(d)
        titre = {"numero": "Connexion à mon espace", "mdp": "Mot de passe", "code": "Code de sécurité"}[page]
        f = F(28, "b"); tw = d.textlength(titre, font=f); d.text((CX - tw / 2, PAGE_Y + 76), titre, font=f, fill=INK)
        lab = {"numero": "Numéro fiscal (13 chiffres)", "mdp": "Mot de passe", "code": "Code reçu par mail (6 chiffres)"}[page]
        d.text((CASE_NUM[0], CASE_NUM[1] - 32), lab, font=F(20, "b"), fill=INK)
        case(d, CASE_NUM, typed, focus)
        btn(d, BTN_CONT, "Continuer" if page == "numero" else "Valider")
        if page == "numero":
            d.line([CX - 220, PAGE_Y + 300, CX - 20, PAGE_Y + 300], fill=(200, 200, 210), width=2); d.text((CX - 12, PAGE_Y + 289), "ou", font=F(20), fill=GRIS)
            d.line([CX + 30, PAGE_Y + 300, CX + 220, PAGE_Y + 300], fill=(200, 200, 210), width=2)
            btn(d, BTN_FC, "FranceConnect", fill=(255, 255, 255), col=INK); d.rounded_rectangle(BTN_FC, 10, outline=INK, width=3)
    elif page == "espace":
        tab_title(d, "Mon espace"); entete(d, "quitter")
        d.text((BX + 60, PAGE_Y + 84), "Bonjour Madame EXEMPLE", font=F(22, "b"), fill=INK)
        for i, (l, k) in enumerate(TUILES):
            r = tuile_rect(i)
            d.rounded_rectangle(r, 12, fill=(255, 246, 214) if hover == i else (246, 246, 250), outline=(200, 200, 210), width=2)
            picto(d, k, r[0] + 50, r[1] + 55); d.text((r[0] + 100, r[1] + 40), l, font=F(24, "b"), fill=INK)
    elif page == "avis":
        tab_title(d, "Mes avis d'impôt"); entete(d, "quitter")
        d.text((BX + 60, PAGE_Y + 90), "Mes avis d'impôt", font=F(30, "b"), fill=INK)
        for i, an in enumerate(("Avis d'impôt 2026", "Avis d'impôt 2025", "Avis d'impôt 2024")):
            r = (ANNEE[0], ANNEE[1] + i * 70, ANNEE[2], ANNEE[3] + i * 70)
            d.rounded_rectangle(r, 8, fill=(255, 246, 214) if (hover == 0 and i == 0) else (246, 246, 250), outline=(200, 200, 210), width=2)
            picto(d, "doc", r[0] + 34, r[1] + 25); d.text((r[0] + 70, r[1] + 12), an, font=F(22), fill=INK)
    elif page == "lecture":
        tab_title(d, "Avis d'impôt 2026"); entete(d, "quitter")
        d.rectangle([CX - 210, PAGE_Y + 90, CX + 210, BY + BH - 20], fill=(255, 255, 255), outline=INK, width=3)
        d.text((CX - 190, PAGE_Y + 110), "AVIS D'IMPÔT – EXEMPLE", font=F(22, "b"), fill=INK)
        for k in range(9): d.line([CX - 190, PAGE_Y + 160 + k * 32, CX + 190 - (k % 3) * 60, PAGE_Y + 160 + k * 32], fill=(170, 170, 180), width=6)
    elif page == "messagerie":
        tab_title(d, "Messagerie sécurisée"); entete(d, "quitter")
        d.text((BX + 60, PAGE_Y + 90), "Messagerie sécurisée", font=F(30, "b"), fill=INK)
        d.rounded_rectangle([BX + 60, PAGE_Y + 150, BX + BW - 60, PAGE_Y + 380], 10, fill=(255, 255, 255), outline=(150, 150, 160), width=2)
        msg = "Bonjour, j'ai une question sur mon avis d'impôt…"
        d.text((BX + 80, PAGE_Y + 170), msg[:typed and len(typed) or len(msg)] if isinstance(typed, str) and typed else msg, font=F(22), fill=INK)
        d.text((BX + 80, PAGE_Y + 340), "(exemple)", font=F(18), fill=GRIS)

def screen(page=None, url="", typed="", focus=False, hover=None, close_hover=False, addr_focus=False):
    im = R.screen({"window": False})
    if page is None: return im
    d = ImageDraw.Draw(im)
    if page == "vide":
        B.browser(d, typed=url, focus=addr_focus); return im
    B.browser(d, typed=url or ADRESSE, page="x", close_hover=close_hover)
    site(d, page, typed, focus, hover); return im

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None):
    c = R.center(r); tc = 0.6 * D
    im = (after if t >= tc + 0.3 else before)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    R.caption(d, cap); return im

def avis_papier(d, x, y, s=1.0, cadre=True, t=0):
    """Avis d'impôt dessiné (EXEMPLE), numéro fiscal en haut."""
    w, h = 300 * s, 400 * s
    d.rectangle([x - w / 2 + 8, y - h / 2 + 8, x + w / 2 + 8, y + h / 2 + 8], fill=(150, 150, 160))
    d.rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=(255, 255, 255), outline=INK, width=3)
    d.text((x - w / 2 + 16, y - h / 2 + 14), "AVIS D'IMPÔT", font=F(int(24 * s), "b"), fill=INK)
    d.text((x - w / 2 + 16, y - h / 2 + 52 * s), "EXEMPLE", font=F(int(16 * s), "b"), fill=CORAIL)
    ry = y - h / 2 + 90 * s
    d.text((x - w / 2 + 16, ry), "Numéro fiscal :", font=F(int(16 * s)), fill=INK)
    d.text((x - w / 2 + 16, ry + 24 * s), "1234 567 890 123", font=F(int(22 * s), "b"), fill=INK)
    r = (x - w / 2 + 8, ry - 6, x + w / 2 - 8, ry + 56 * s)
    if cadre: R.highlight(d, r, t)
    for k in range(7): d.line([x - w / 2 + 16, ry + (90 + k * 30) * s, x + w / 2 - 16 - (k % 3) * 40, ry + (90 + k * 30) * s], fill=(190, 190, 200), width=int(6 * s))
    return r

def boite(d, x, y, s=1.0):
    d.rounded_rectangle([x - 90 * s, y - 70 * s, x + 90 * s, y + 90 * s], 14, fill=(230, 200, 60), outline=INK, width=4)
    d.rectangle([x - 60 * s, y - 30 * s, x + 60 * s, y - 14 * s], fill=INK)
    d.ellipse([x + 40 * s, y + 30 * s, x + 64 * s, y + 54 * s], fill=INK)  # serrure
    d.rectangle([x - 8 * s, y + 90 * s, x + 8 * s, y + 160 * s], fill=(120, 90, 60))

def cadenas(d, x, y, s=1.0, col=VERT):
    d.arc([x - 26 * s, y - 56 * s, x + 26 * s, y], 180, 360, fill=col, width=int(10 * s))
    d.rounded_rectangle([x - 40 * s, y - 24 * s, x + 40 * s, y + 40 * s], 8, fill=col)

def mail_code(d, p):
    """Fenêtre de messagerie dessinée avec un code EXEMPLE."""
    d.rounded_rectangle([300, 150, 980, 520], 12, fill=(255, 255, 255), outline=INK, width=3)
    d.rectangle([302, 152, 978, 200], fill=(236, 236, 242)); d.text((322, 162), "Ma messagerie", font=F(22, "b"), fill=INK)
    d.text((330, 230), "Votre code de sécurité :", font=F(26), fill=INK)
    f = F(64, "b"); tw = d.textlength("4 8 1 5 2 6", font=f); d.text((640 - tw / 2, 290), "4 8 1 5 2 6", font=f, fill=VIO)
    d.text((330, 410), "EXEMPLE : votre code sera différent.", font=F(22, "b"), fill=CORAIL)

def faux_sms(d, p, t):
    d.rounded_rectangle([450, 110, 830, 560], 36, fill=(40, 44, 54)); d.rectangle([470, 160, 810, 520], fill=(245, 245, 248))
    d.rounded_rectangle([485, 190, 795, 330], 16, fill=(225, 228, 236))
    for k, l in enumerate(("EXEMPLE de faux SMS :", "« Remboursement d'impôt :", "donnez votre carte", "bancaire ici… »")):
        d.text((500, 200 + k * 30), l, font=F(20, "b" if k == 0 else "r"), fill=CORAIL if k == 0 else INK)
    if p > 0.35:
        d.line([480, 180, 800, 340], fill=CORAIL, width=12); d.line([480, 340, 800, 180], fill=CORAIL, width=12)
    if p > 0.55: O.label(d, "Jamais de coordonnées bancaires par mail, SMS ou téléphone", (640, 610))

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("impots.gouv.fr", ["Aide-mémoire n° 24 · Formation débutant", "Entrer dans mon espace Finances publiques"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); cadenas(d, W / 2, 380, 1.2); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); O.draw_fixe(d)
        if p > 0.25: avis_papier(d, 1060, 300, 0.6, cadre=False)
        if p > 0.5: O.label(d, "lire mes avis d'impôt, poser mes questions", (W / 2, 560))
        R.caption(d, cap); return im
    if sid == "preparer":
        im = O.room(); d = ImageDraw.Draw(im)
        avis_papier(d, 470, 330, 1.0, cadre=p > 0.3, t=t)
        if p > 0.3:
            R.loupe(im, (330, 205, 610, 285), place=(900, 260)); d = ImageDraw.Draw(im)
            O.label(d, "numéro fiscal : 13 chiffres", (900, 420))
        if p > 0.7: O.label(d, "+ votre mot de passe", (900, 500))
        R.caption(d, cap); return im
    if sid == "espace":
        im = O.room(); d = ImageDraw.Draw(im); boite(d, 420, 300)
        if p > 0.3: cadenas(d, 860, 300, 1.4)
        O.label(d, "mon espace Finances publiques", (W / 2, 120))
        if p > 0.45: O.label(d, "ma boîte aux lettres personnelle aux impôts", (W / 2, 560))
        R.caption(d, cap); return im
    if sid == "adresse":
        if t < 0.25 * D:
            return act(lambda: screen(), lambda: screen("vide"), B.EDGE, (W / 2 - 200, H / 2), t, 0.25 * D / 0.6 - 0.01, cap, show_loupe=False)
        n = int(len(ADRESSE) * min(1, (t - 0.3 * D) / (0.35 * D))) if t > 0.3 * D else 0
        if t < 0.75 * D:
            im = screen("vide", url=ADRESSE[:n], addr_focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
            R.highlight(d, B.ADDR, t); R.loupe(im, (B.ADDR[0], B.ADDR[1], B.ADDR[0] + 260, B.ADDR[3]), place=(640, 420), clean=clean); d = ImageDraw.Draw(im)
            if t > 0.65 * D: R.key_enter(d, t, 0.7 * D < t)
        else:
            im = screen("accueil"); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "verifier":
        im = screen("accueil"); clean = im.copy(); d = ImageDraw.Draw(im)
        x0 = B.ADDR[0] + 22 + d.textlength("impots", font=F(20)); r = (x0 - 4, B.ADDR[1] + 2, x0 + d.textlength(".gouv.fr", font=F(20)) + 4, B.ADDR[3] - 2)
        R.highlight(d, r, t); R.loupe(im, (B.ADDR[0], B.ADDR[1], B.ADDR[0] + 200, B.ADDR[3]), place=(640, 420), clean=clean); d = ImageDraw.Draw(im)
        if p > 0.4: O.label(d, ".gouv.fr = site officiel", (640, 570))
        R.caption(d, cap); return im
    if sid == "bouton":
        return act(lambda: screen("accueil"), lambda: screen("numero"), CONNEX, (W / 2, H / 2), t, D, cap, place=(700, 420))
    if sid == "numero":
        if t < 0.3 * D:
            return act(lambda: screen("numero"), lambda: screen("numero", focus=True), CASE_NUM, (W / 2, 600), t, 0.3 * D / 0.6 - 0.01, cap, show_loupe=False)
        if t < 0.7 * D:
            n = int(13 * min(1, (t - 0.3 * D) / (0.3 * D)))
            im = screen("numero", typed=NUMFISC[:n], focus=True); d = ImageDraw.Draw(im)
            d.text((CASE_NUM[2] + 14, CASE_NUM[1] + 12), "EXEMPLE", font=F(18, "b"), fill=CORAIL); R.caption(d, cap); return im
        return act(lambda: screen("numero", typed=NUMFISC), lambda: screen("mdp", focus=True), BTN_CONT, R.center(CASE_NUM), t - 0.7 * D, 0.3 * D / 0.6 - 0.01, cap, show_loupe=False)
    if sid == "motdepasse":
        n = int(10 * min(1, p / 0.5))
        if t < 0.75 * D:
            im = screen("mdp", typed="•" * n, focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
            if p > 0.3:
                R.loupe(im, CASE_MDP, place=(640, 520), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        return act(lambda: screen("mdp", typed="•" * 10), lambda: screen("code"), BTN_CONT, R.center(CASE_MDP), t - 0.75 * D, 0.25 * D / 0.6 - 0.01, cap, show_loupe=False)
    if sid == "code":
        if p < 0.55:
            im = O.room(); d = ImageDraw.Draw(im); mail_code(d, p); R.caption(d, cap); return im
        n = int(6 * min(1, (p - 0.55) / 0.35))
        im = screen("code", typed="481526"[:n], focus=True); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "franceconnect":
        im = screen("numero"); clean = im.copy(); d = ImageDraw.Draw(im)
        R.highlight(d, BTN_FC, t); R.arrow(d, BTN_FC, t)
        if p > 0.45: O.label(d, "par exemple avec mon compte ameli", (640, 600))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez avec votre avis d'impôt."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "accueil":
        im = screen("espace"); d = ImageDraw.Draw(im)
        k = min(3, int(p * 4.5))
        if p > 0.1: R.highlight(d, tuile_rect(k), t)
        R.caption(d, cap); return im
    if sid == "avis":
        if t < 0.45 * D:
            return act(lambda: screen("espace", hover=0), lambda: screen("avis"), tuile_rect(0), (W / 2, 600), t, 0.45 * D / 0.6 - 0.01, cap, show_loupe=False)
        if t < 0.85 * D:
            return act(lambda: screen("avis", hover=0), lambda: screen("lecture"), ANNEE, (W / 2, 600), t - 0.45 * D, 0.4 * D / 0.6 - 0.01, cap, show_loupe=False)
        im = screen("lecture"); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "messagerie":
        if t < 0.35 * D:
            return act(lambda: screen("espace", hover=3), lambda: screen("messagerie"), tuile_rect(3), (W / 2, 300), t, 0.35 * D / 0.6 - 0.01, cap, show_loupe=False)
        im = screen("messagerie"); d = ImageDraw.Draw(im)
        if p > 0.55: O.label(d, "sans vous déplacer", (640, 600))
        R.caption(d, cap); return im
    if sid == "quitter":
        if t < 0.55 * D:
            return act(lambda: screen("espace"), lambda: screen("accueil"), QUITTER, (W / 2, H / 2), t, 0.55 * D / 0.6 - 0.01, cap, place=(700, 420))
        hov = t > 0.75 * D
        return act(lambda: screen("accueil", close_hover=hov), lambda: screen(), B.CLOSE, R.center(QUITTER), t - 0.55 * D, 0.45 * D / 0.6 - 0.01, cap, show_loupe=False)
    if sid == "prudence":
        im = O.room(); d = ImageDraw.Draw(im); faux_sms(d, p, t); R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Prenez votre avis d'impôt.", "Allez sur impots.gouv.fr", "et entrez dans votre espace."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["impots.gouv.fr,", "numéro fiscal, puis mot de passe."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 4
        if t < q:
            n = int(len(ADRESSE) * min(1, t / (0.6 * q)))
            im = screen("vide", url=ADRESSE[:n], addr_focus=True); d = ImageDraw.Draw(im)
            if t > 0.7 * q: R.key_enter(d, t, t > 0.85 * q)
            R.caption(d, cap); return im
        if t < 2 * q:
            return act(lambda: screen("accueil"), lambda: screen("numero"), CONNEX, (W / 2, H / 2), t - q, q / 0.6 - 0.01, cap, show_loupe=False)
        if t < 3 * q:
            n = int(13 * min(1, (t - 2 * q) / (0.7 * q)))
            im = screen("numero", typed=NUMFISC[:n], focus=True); d = ImageDraw.Draw(im); R.caption(d, cap); return im
        n = int(10 * min(1, (t - 3 * q) / (0.6 * q)))
        im = screen("mdp", typed="•" * n, focus=True); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["L'avis d'impôt donne le numéro fiscal", "L'adresse finit par .gouv.fr", "Numéro fiscal, puis mot de passe", "Jamais de carte bancaire par mail"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
