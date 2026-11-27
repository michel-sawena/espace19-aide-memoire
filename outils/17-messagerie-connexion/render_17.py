"""Vidéo « 17 - Se connecter et se déconnecter de sa messagerie » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_17.py script.json durations.json out.mp4
        python3 render_17.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes),
../01-ordinateur/render_01_ordinateur.py (pièce, étiquettes) et ../12-internet/render_12.py (globe, ordinateur).
La messagerie est un dessin NEUTRE (« Ma messagerie ») : aucun logo ni charte d'un site réel.
Libellés écrits tels quels car confirmés par l'aide Google (voir sources_17.md) : « Déconnexion »,
« Utiliser un autre compte », « barre d'adresse ». Le bouton pour continuer n'a pas de texte (flèche seule) :
son libellé n'est pas confirmé par l'aide officielle. Adresses et messages : EXEMPLES inventés.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as B
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); BLEU = (0, 103, 192); GRIS = (110, 110, 120)
URL = "mail.google.com"
MAIL = "jean.exemple@gmail.com"
AUTRE = "paul.exemple@gmail.com"

BX, BY, BW, BH = B.BX, B.BY, B.BW, B.BH
ADDR, PAGE_Y = B.ADDR, B.PAGE_Y
CX = BX + BW / 2
CARD = (CX - 260, PAGE_Y + 30, CX + 260, PAGE_Y + 430)
FIELD = (CX - 210, PAGE_Y + 170, CX + 210, PAGE_Y + 222)
BTN = (CX + 90, PAGE_Y + 300, CX + 210, PAGE_Y + 350)
AUTRE_R = (CX - 210, PAGE_Y + 250, CX + 60, PAGE_Y + 280)
AV = (BX + BW - 70, PAGE_Y + 10, BX + BW - 20, PAGE_Y + 60)
MENU = (BX + BW - 330, PAGE_Y + 70, BX + BW - 16, PAGE_Y + 250)
DECO = (MENU[0] + 60, MENU[1] + 115, MENU[2] - 60, MENU[1] + 160)
MESSAGES = [("Espace 19 Numérique", "Bienvenue à l'atelier de lundi"), ("Marie (EXEMPLE)", "Photos du repas de dimanche"),
            ("Pharmacie (EXEMPLE)", "Votre commande est prête"), ("Paul (EXEMPLE)", "On se voit jeudi ?")]

def fleche(d, r, col=(255, 255, 255)):
    cx, cy = R.center(r)
    d.line([cx - 18, cy, cx + 16, cy], fill=col, width=5)
    d.line([cx + 4, cy - 12, cx + 17, cy, cx + 4, cy + 12], fill=col, width=5)

def avatar(d, r, s=26):
    d.ellipse(r, fill=VIO); f = F(s, "b"); cx, cy = R.center(r)
    tw = d.textlength("J", font=f); d.text((cx - tw / 2, cy - s * 0.62), "J", font=f, fill=(255, 255, 255))

def browser(d, url="", focus=False, tab="Nouvel onglet"):
    d.rounded_rectangle([BX + 6, BY + 8, BX + BW + 6, BY + BH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([BX, BY, BX + BW, BY + BH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([BX, BY, BX + BW, BY + B.TAB_H + 10], 10, fill=(222, 226, 236)); d.rectangle([BX, BY + 20, BX + BW, BY + B.TAB_H], fill=(222, 226, 236))
    d.rounded_rectangle([BX + 12, BY + 6, BX + 300, BY + B.TAB_H + 4], 8, fill=(250, 250, 252))
    B.globe(d, BX + 32, BY + 23, 9); d.text((BX + 50, BY + 12), tab, font=F(17), fill=(30, 30, 30))
    cx, cy = R.center(B.CLOSE)
    d.line([cx - 9, cy - 9, cx + 9, cy + 9], fill=(40, 40, 40), width=3); d.line([cx - 9, cy + 9, cx + 9, cy - 9], fill=(40, 40, 40), width=3)
    d.rectangle([BX + 2, B.BAR_Y, BX + BW - 2, B.BAR_Y + 60], fill=(250, 250, 252))
    d.rounded_rectangle(ADDR, 20, fill=(255, 255, 255) if focus else (238, 240, 244), outline=BLEU if focus else (200, 204, 212), width=3 if focus else 1)
    txt = url if (url or focus) else "Rechercher ou entrer une adresse"
    d.text((ADDR[0] + 22, ADDR[1] + 9), txt, font=F(20), fill=(20, 20, 20) if (url or focus) else GRIS)
    d.line([BX + 2, PAGE_Y, BX + BW - 2, PAGE_Y], fill=(215, 218, 225), width=1)

def connexion(d, etape="adresse", typed="", focus=False, choix=False):
    d.rounded_rectangle(CARD, 18, fill=(255, 255, 255), outline=(200, 204, 212), width=2)
    f = F(32, "b"); tw = d.textlength("Ma messagerie", font=f); d.text((CX - tw / 2, CARD[1] + 30), "Ma messagerie", font=f, fill=VIO)
    f2 = F(20); s = "(dessin simplifié)"; tw = d.textlength(s, font=f2); d.text((CX - tw / 2, CARD[3] - 36), s, font=f2, fill=GRIS)
    if choix:   # une adresse déjà affichée, qui n'est pas la vôtre
        d.rounded_rectangle(FIELD, 26, fill=(245, 245, 250), outline=(200, 204, 212), width=1)
        avatar(d, (FIELD[0] + 10, FIELD[1] + 8, FIELD[0] + 46, FIELD[1] + 44), 20)
        d.text((FIELD[0] + 60, FIELD[1] + 13), AUTRE, font=F(21), fill=INK)
        d.text((AUTRE_R[0] + 4, AUTRE_R[1] + 2), "Utiliser un autre compte", font=F(21, "b"), fill=BLEU)
        return
    if etape == "mdp":
        f3 = F(19); tw = d.textlength(MAIL, font=f3)
        d.rounded_rectangle([CX - tw / 2 - 16, FIELD[1] - 58, CX + tw / 2 + 16, FIELD[1] - 24], 17, outline=(200, 204, 212), width=1)
        d.text((CX - tw / 2, FIELD[1] - 52), MAIL, font=f3, fill=INK)
    d.rounded_rectangle(FIELD, 8, fill=(255, 255, 255), outline=BLEU if focus else (150, 156, 168), width=3 if focus else 2)
    ph = "Adresse e-mail" if etape == "adresse" else "Mot de passe"
    if typed:
        shown = typed if etape == "adresse" else "•" * len(typed)
        d.text((FIELD[0] + 16, FIELD[1] + 12), shown, font=F(23), fill=INK)
        x = FIELD[0] + 16 + d.textlength(shown, font=F(23)) + 2
    else:
        d.text((FIELD[0] + 16, FIELD[1] + 13), ph, font=F(22), fill=GRIS); x = FIELD[0] + 16
    if focus: d.line([x, FIELD[1] + 12, x, FIELD[3] - 12], fill=INK, width=2)
    d.rounded_rectangle(BTN, 25, fill=BLEU); fleche(d, BTN)

def boite(d, menu=False):
    d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, PAGE_Y + 70], fill=(248, 234, 245))
    d.text((BX + 30, PAGE_Y + 18), "Ma messagerie", font=F(28, "b"), fill=VIO)
    d.text((BX + 290, PAGE_Y + 26), "(dessin simplifié)", font=F(18), fill=GRIS)
    avatar(d, AV)
    for i, (qui, sujet) in enumerate(MESSAGES):
        y = PAGE_Y + 95 + i * 72
        d.rounded_rectangle([BX + 30, y, BX + BW - 30, y + 60], 8, fill=(255, 246, 214) if i == 0 else (247, 248, 251), outline=(220, 222, 230), width=1)
        d.ellipse([BX + 48, y + 18, BX + 72, y + 42], fill=VERT if i == 0 else (190, 195, 205))
        d.text((BX + 90, y + 16), qui, font=F(21, "b"), fill=INK); d.text((BX + 420, y + 17), sujet, font=F(21), fill=INK)
    if menu:
        d.rounded_rectangle([MENU[0] + 5, MENU[1] + 6, MENU[2] + 5, MENU[3] + 6], 14, fill=(150, 150, 160))
        d.rounded_rectangle(MENU, 14, fill=(255, 255, 255), outline=(190, 195, 205), width=2)
        avatar(d, ((MENU[0] + MENU[2]) / 2 - 26, MENU[1] + 14, (MENU[0] + MENU[2]) / 2 + 26, MENU[1] + 66))
        f = F(18); tw = d.textlength(MAIL, font=f); d.text(((MENU[0] + MENU[2]) / 2 - tw / 2, MENU[1] + 78), MAIL, font=f, fill=INK)
        d.rounded_rectangle(DECO, 22, fill=(255, 255, 255), outline=(150, 156, 168), width=2)
        f = F(22, "b"); tw = d.textlength("Déconnexion", font=f); cx, cy = R.center(DECO); d.text((cx - tw / 2, cy - 14), "Déconnexion", font=f, fill=INK)

def screen(state=None, **kw):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if state is None: return im
    if state == "vide": browser(d, **kw); return im
    if state in ("adresse", "mdp", "choix"):
        browser(d, url=URL, tab="Ma messagerie")
        connexion(d, etape=state, choix=state == "choix", **kw); return im
    if state == "boite":
        browser(d, url=URL, tab="Ma messagerie"); boite(d, **kw); return im
    raise KeyError(state)

act = B.act

def typing(state, text, t, t0, t1, cap, loupe_r=None):
    n = int(len(text) * max(0, min(1, (t - t0) / max(0.1, t1 - t0))))
    im = screen(state, typed=text[:n], focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
    if loupe_r: R.loupe(im, loupe_r, place=(1010, 420), clean=clean); d = ImageDraw.Draw(im)
    R.caption(d, cap); return im

# ---------- illustrations ----------
def boite_lettres(d, x, y, ouverte):
    d.rectangle([x - 8, y + 60, x + 8, y + 200], fill=(110, 80, 50))
    d.rounded_rectangle([x - 110, y - 70, x + 110, y + 70], 30, fill=VIO)
    d.rectangle([x - 70, y - 10, x + 70, y + 4], fill=(60, 10, 50))
    if ouverte:
        d.polygon([(x + 110, y - 50), (x + 190, y - 90), (x + 190, y + 50), (x + 110, y + 70)], fill=(190, 80, 170))
        for k in range(3): d.rectangle([x - 60 + k * 18, y - 40 - k * 6, x + 40 + k * 18, y + 20 - k * 6], fill=(255, 255, 255), outline=INK, width=2)

def cle(d, x, y, col=YEL):
    d.ellipse([x - 34, y - 34, x + 34, y + 34], outline=col, width=12)
    d.rectangle([x + 30, y - 7, x + 140, y + 7], fill=col); d.rectangle([x + 110, y, x + 124, y + 30], fill=col); d.rectangle([x + 84, y, x + 98, y + 24], fill=col)

def cadenas(d, x, y):
    d.arc([x - 32, y - 70, x + 32, y - 6], 180, 360, fill=INK, width=12)
    d.rounded_rectangle([x - 46, y - 30, x + 46, y + 50], 10, fill=YEL, outline=INK, width=4)

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Se connecter, se déconnecter", ["de sa messagerie", "Aide-mémoire n° 17 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); cle(d, W / 2 - 60, 430); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im)
        boite_lettres(d, 420, 300, 0.3 < p < 0.72)
        if 0.3 < p < 0.72: cle(d, 760, 260)
        if p > 0.3: O.label(d, "se connecter = ouvrir", (860, 360))
        if p > 0.72: cadenas(d, 820, 280); O.label(d, "se déconnecter = refermer", (860, 400))
        R.caption(d, cap); return im
    if sid == "besoin":
        im = O.room(); d = ImageDraw.Draw(im)
        for i, (titre, ex, seuil) in enumerate((("1. Adresse e-mail", MAIL, 0.1), ("2. Mot de passe", "••••••••", 0.35))):
            if p > seuil:
                x0 = 140 + i * 520; d.rounded_rectangle([x0, 170, x0 + 480, 380], 18, fill=(255, 255, 255), outline=VIO, width=4)
                d.text((x0 + 30, 200), titre, font=F(34, "b"), fill=VIO); d.text((x0 + 30, 290), ex, font=F(28), fill=INK)
                if seuil < p < seuil + 0.25: R.highlight(d, (x0, 170, x0 + 480, 380), t)
        if p > 0.65: O.label(d, "notés dans un endroit sûr, chez vous", (W / 2, 470))
        R.caption(d, cap); return im
    if sid == "ouvrir":
        t0 = 0.3 * D
        if t < t0:
            return act(lambda: screen("vide"), lambda: screen("vide", focus=True), ADDR, (W / 2, 500), t, t0 / 0.6, cap, show_loupe=False)
        if t < 0.7 * D:
            n = int(len(URL) * min(1, (t - t0) / (0.3 * D)))
            im = screen("vide", url=URL[:n], focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
            R.loupe(im, (ADDR[0], ADDR[1], ADDR[0] + 260, ADDR[3]), place=(640, 420), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        if t < 0.82 * D:
            im = screen("vide", url=URL, focus=True); d = ImageDraw.Draw(im); R.key_enter(d, t, t > 0.76 * D)
        else:
            im = screen("adresse"); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "adresse":
        t0 = 0.25 * D
        if t < t0 + 0.3: return act(lambda: screen("adresse"), lambda: screen("adresse", focus=True), FIELD, (W / 2, 620), t, t0 / 0.6, cap, show_loupe=False)
        if t < 0.62 * D: return typing("adresse", MAIL, t, t0 + 0.3, 0.55 * D, cap, (FIELD[0], FIELD[1] - 10, FIELD[0] + 220, FIELD[3] + 10))
        tt = t - 0.62 * D
        return act(lambda: screen("adresse", typed=MAIL, focus=True), lambda: screen("mdp"), BTN, R.center(FIELD), tt, 0.38 * D * 0.9, cap, place=(250, 430))
    if sid == "motdepasse":
        t0 = 0.12 * D; pw = "secret2026"
        if t < 0.5 * D:
            im = typing("mdp", pw, t, t0, 0.42 * D, cap, (FIELD[0], FIELD[1] - 10, FIELD[0] + 220, FIELD[3] + 10))
            if t > 0.3 * D: d = ImageDraw.Draw(im); O.label(d, "des petits points : c'est normal", (640, 440))
            return im
        tt = t - 0.5 * D
        return act(lambda: screen("mdp", typed=pw, focus=True), lambda: screen("boite"), BTN, R.center(FIELD), tt, 0.5 * D * 0.9, cap, place=(250, 430))
    if sid == "boite":
        im = screen("boite"); d = ImageDraw.Draw(im)
        if p > 0.4: O.label(d, "Bravo, vous êtes connecté !", (W / 2, 470))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "rond":
        return act(lambda: screen("boite"), lambda: screen("boite", menu=True), AV, (W / 2, 450), t, D * 0.85, cap, place=(760, 420))
    if sid == "deco":
        if t < 0.65 * D:
            return act(lambda: screen("boite", menu=True), lambda: screen("adresse"), DECO, R.center(AV), t, 0.65 * D * 0.95, cap, place=(500, 430))
        im = screen("adresse"); d = ImageDraw.Draw(im); O.label(d, "Votre boîte est refermée", (W / 2, 440)); R.caption(d, cap); return im
    if sid == "panique":
        if p < 0.6:
            return act(lambda: screen("choix"), lambda: screen("adresse"), AUTRE_R, (W / 2, 620), t, 0.6 * D * 0.95, cap, place=(1010, 420))
        im = screen("adresse"); d = ImageDraw.Draw(im); O.label(d, "Mot de passe oublié ? Demandez à Espace 19", (W / 2, 440)); R.caption(d, cap); return im
    if sid == "public":
        im = O.room(); d = ImageDraw.Draw(im)
        for i, x in enumerate((260, 520, 780, 1040)): B.pc(d, x, 300, 1.4)
        if p > 0.3: cadenas(d, 640, 470)
        if p > 0.5: O.label(d, "Toujours se déconnecter avant de partir", (W / 2, 580))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Connectez-vous à votre messagerie :", "adresse, puis mot de passe.", "Puis déconnectez-vous :", "le rond en haut à droite, puis Déconnexion."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Connectez-vous,", "puis déconnectez-vous."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 4
        if t < q: return typing("adresse", MAIL, t, 0.1 * q, 0.8 * q, cap)
        if t < 2 * q: return typing("mdp", "secret2026", t - q, 0.1 * q, 0.8 * q, cap)
        if t < 3 * q: return act(lambda: screen("boite"), lambda: screen("boite", menu=True), AV, (W / 2, 450), t - 2 * q, q * 0.95, cap, show_loupe=False)
        return act(lambda: screen("boite", menu=True), lambda: screen("adresse"), DECO, R.center(AV), t - 3 * q, q * 0.95, cap, show_loupe=False)
    if sid == "resume":
        return R.card("À retenir", ["Se connecter : l'adresse, puis le mot de passe", "Se déconnecter : le rond en haut à droite,", "puis « Déconnexion »", "Ordinateur public : toujours se déconnecter"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
