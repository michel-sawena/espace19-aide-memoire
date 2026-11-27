"""Vidéo « 12 - Internet et les navigateurs » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_12.py script.json durations.json out.mp4
        python3 render_12.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, barre des tâches, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes)
et ../01-ordinateur/render_01_ordinateur.py (pièce, étiquettes).
Aucun logo reproduit : les navigateurs sont des pastilles neutres avec leur nom ; la page google.fr est un dessin
simplifié (nom en police neutre + case de recherche), sans charte du site. Libellé écrit tel quel : « barre d'adresse »
(aide Microsoft Edge + aide Google Chrome, voir sources_12.md).
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); BLEU = (0, 103, 192)
ADRESSE = "google.fr"

# ---------- navigateur (fenêtre dessinée) ----------
BX, BY, BW, BH = 120, 70, 1040, 580
TAB_H, BAR_Y = 40, 70 + 40
CLOSE = (BX + BW - 52, BY + 4, BX + BW - 6, BY + 36)
ADDR = (BX + 150, BAR_Y + 10, BX + BW - 120, BAR_Y + 50)
PAGE_Y = BAR_Y + 62
EDGE = (lambda c: (c[0] - 24, c[1] - 22, c[0] + 24, c[1] + 22))(R.taskbar_icons()["edge"])

def globe(d, cx, cy, r, col=(0, 120, 200), line=(255, 255, 255)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    w = max(2, int(r / 9))
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=line, width=w)
    d.line([cx, cy - r, cx, cy + r], fill=line, width=w)
    d.line([cx - r, cy, cx + r, cy], fill=line, width=w)
    for k in (-0.5, 0.5):
        hw = r * math.sqrt(1 - k * k)
        d.line([cx - hw, cy + k * r, cx + hw, cy + k * r], fill=line, width=w)

def browser(d, typed="", focus=False, page=None, close_hover=False):
    d.rounded_rectangle([BX + 6, BY + 8, BX + BW + 6, BY + BH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([BX, BY, BX + BW, BY + BH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([BX, BY, BX + BW, BY + TAB_H + 10], 10, fill=(222, 226, 236)); d.rectangle([BX, BY + 20, BX + BW, BY + TAB_H], fill=(222, 226, 236))
    # onglet
    d.rounded_rectangle([BX + 12, BY + 6, BX + 300, BY + TAB_H + 4], 8, fill=(250, 250, 252))
    globe(d, BX + 32, BY + 23, 9)
    d.text((BX + 50, BY + 12), "Google" if page else "Nouvel onglet", font=F(17), fill=(30, 30, 30))
    # boutons de la fenêtre (dessin seul) ; croix de fermeture
    d.line([BX + BW - 150, BY + 20, BX + BW - 132, BY + 20], fill=(60, 60, 60), width=2)
    d.rectangle([BX + BW - 100, BY + 12, BX + BW - 84, BY + 28], outline=(60, 60, 60), width=2)
    if close_hover: d.rectangle(CLOSE, fill=(196, 43, 28))
    cx, cy = R.center(CLOSE); cc = (255, 255, 255) if close_hover else (40, 40, 40)
    d.line([cx - 9, cy - 9, cx + 9, cy + 9], fill=cc, width=3); d.line([cx - 9, cy + 9, cx + 9, cy - 9], fill=cc, width=3)
    # barre de navigation
    d.rectangle([BX + 2, BAR_Y, BX + BW - 2, BAR_Y + 60], fill=(250, 250, 252))
    for i, x in enumerate((BX + 30, BX + 70)):
        y = BAR_Y + 30; s = -1 if i == 0 else 1
        d.line([x - 9 * s, y, x + 9 * s, y], fill=(110, 110, 120), width=3)
        d.line([x + 2 * s, y - 7, x + 9 * s, y, x + 2 * s, y + 7], fill=(110, 110, 120), width=3)
    d.arc([BX + 100, BAR_Y + 19, BX + 124, BAR_Y + 43], 40, 320, fill=(110, 110, 120), width=3)
    d.rounded_rectangle(ADDR, 20, fill=(255, 255, 255) if focus else (238, 240, 244), outline=BLEU if focus else (200, 204, 212), width=3 if focus else 1)
    txt = typed if (typed or focus) else "Rechercher ou entrer une adresse"
    col = (20, 20, 20) if (typed or focus) else (110, 110, 120)
    d.text((ADDR[0] + 22, ADDR[1] + 9), txt, font=F(20), fill=col)
    if focus and not page:
        x = ADDR[0] + 22 + d.textlength(typed, font=F(20)) + 2; d.line([x, ADDR[1] + 9, x, ADDR[3] - 9], fill=(20, 20, 20), width=2)
    d.line([BX + 2, PAGE_Y, BX + BW - 2, PAGE_Y], fill=(215, 218, 225), width=1)
    if page == "google":
        cx = BX + BW / 2
        f = F(64, "b"); tw = d.textlength("Google", font=f)
        d.text((cx - tw / 2, PAGE_Y + 90), "Google", font=f, fill=(60, 64, 72))
        d.rounded_rectangle([cx - 290, PAGE_Y + 200, cx + 290, PAGE_Y + 250], 25, fill=(255, 255, 255), outline=(190, 195, 205), width=2)
        d.ellipse([cx - 268, PAGE_Y + 214, cx - 250, PAGE_Y + 232], outline=(110, 110, 120), width=2)
        d.text((cx - 140, PAGE_Y + 300), "(dessin simplifié)", font=F(18), fill=(110, 110, 120))
    else:
        cx = BX + BW / 2; globe(d, cx, PAGE_Y + 180, 60, (230, 236, 246), (190, 200, 220))

def screen(state=None, **kw):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if state == "browser": browser(d, **kw)
    return im

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None):
    """before/after : fonctions qui dessinent l'écran."""
    c = R.center(r); tc = 0.6 * D
    im = (after if t >= tc + 0.3 else before)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    R.caption(d, cap); return im

# ---------- illustrations ----------
def maison(d, x, y, col):
    d.polygon([(x - 46, y), (x, y - 44), (x + 46, y)], fill=(170, 60, 50))
    d.rectangle([x - 36, y, x + 36, y + 56], fill=col, outline=(120, 100, 80), width=2)
    d.rectangle([x - 9, y + 26, x + 9, y + 56], fill=(120, 80, 45))

def pc(d, x, y, s=1.0):
    d.rounded_rectangle([x - 40 * s, y - 30 * s, x + 40 * s, y + 22 * s], 6, fill=(40, 44, 54))
    d.rectangle([x - 34 * s, y - 24 * s, x + 34 * s, y + 16 * s], fill=(90, 150, 220))
    d.rectangle([x - 6 * s, y + 22 * s, x + 6 * s, y + 34 * s], fill=(40, 44, 54)); d.rectangle([x - 24 * s, y + 34 * s, x + 24 * s, y + 40 * s], fill=(40, 44, 54))

def phone(d, x, y, s=1.0):
    d.rounded_rectangle([x - 20 * s, y - 36 * s, x + 20 * s, y + 36 * s], 7, fill=(40, 44, 54)); d.rectangle([x - 16 * s, y - 28 * s, x + 16 * s, y + 26 * s], fill=(120, 190, 140))

def tablet(d, x, y, s=1.0):
    d.rounded_rectangle([x - 42 * s, y - 32 * s, x + 42 * s, y + 32 * s], 8, fill=(40, 44, 54)); d.rectangle([x - 36 * s, y - 26 * s, x + 36 * s, y + 26 * s], fill=(240, 190, 110))

NOEUDS = [(260, 250), (520, 190), (780, 260), (1020, 200), (380, 420), (660, 430), (920, 420)]
LIENS = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 6), (2, 5), (3, 6), (1, 5)]
def reseau(d, p, maisons):
    for k, (a, b) in enumerate(LIENS):
        q = R.ease((p - 0.1 - k * 0.05) / 0.15)
        if q > 0:
            (x0, y0), (x1, y1) = NOEUDS[a], NOEUDS[b]
            d.line([x0, y0, x0 + (x1 - x0) * q, y0 + (y1 - y0) * q], fill=(120, 120, 130) if maisons else BLEU, width=14 if maisons else 6)
    for i, (x, y) in enumerate(NOEUDS):
        if maisons: maison(d, x, y - 20, (250, 236, 200))
        else: pc(d, x, y, 0.9)

NAVS = [("Microsoft Edge", (0, 120, 200)), ("Google Chrome", (60, 150, 80)), ("Mozilla Firefox", (220, 110, 40)), ("Safari", (90, 110, 200))]
def pastilles(d, p, t):
    for i, (n, col) in enumerate(NAVS):
        if p > 0.1 + i * 0.17:
            x = 220 + i * 280; y = 300
            globe(d, x, y, 70, col)
            f = F(26, "b"); tw = d.textlength(n, font=f); d.text((x - tw / 2, y + 90), n, font=f, fill=INK)
            if 0.1 + i * 0.17 < p < 0.27 + i * 0.17: R.highlight(d, (x - 80, y - 80, x + 80, y + 80), t)
    if p > 0.82: O.label(d, "ils font tous la même chose", (W / 2, 470))

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Internet et les navigateurs", ["Aide-mémoire n° 12 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); globe(d, W / 2, 360, 85); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); O.draw_fixe(d)
        if p > 0.3: globe(d, 1100, 180, 70)
        if p > 0.45: O.label(d, "Internet", (1100, 270))
        R.caption(d, cap); return im
    if sid == "reseau":
        im = O.room(); d = ImageDraw.Draw(im)
        reseau(d, p * 2 if p < 0.5 else 1.0, maisons=p >= 0.5)
        O.label(d, "des ordinateurs reliés" if p < 0.5 else "comme des maisons reliées par des routes", (W / 2, 530))
        R.caption(d, cap); return im
    if sid == "internet":
        im = O.room(); d = ImageDraw.Draw(im); cx, cy = W / 2, 300
        globe(d, cx, cy, 120)
        devs = [(pc, 300, 170), (phone, 300, 420), (tablet, 980, 170), (pc, 980, 420), (phone, 640, 520), (tablet, 640, 110)]
        for i, (fn, x, y) in enumerate(devs):
            if p > 0.25 + i * 0.07:
                d.line([cx, cy, x, y], fill=BLEU, width=4); fn(d, x, y, 1.0)
        globe(d, cx, cy, 120)
        if p > 0.15: O.label(d, "le monde entier", (cx, cy + 135))
        R.caption(d, cap); return im
    if sid == "histoire":
        im = O.room(); d = ImageDraw.Draw(im)
        d.line([160, 300, 1120, 300], fill=INK, width=8)
        for x, an, l1, l2, seuil in ((330, "1969", "premier réseau : Arpanet", "États-Unis", 0.15), (900, "1989", "naissance du Web", "CERN, près de Genève", 0.55)):
            if p > seuil:
                d.ellipse([x - 22, 278, x + 22, 322], fill=YEL, outline=INK, width=4)
                f = F(56, "b"); tw = d.textlength(an, font=f); d.text((x - tw / 2, 180), an, font=f, fill=VIO)
                O.label(d, l1, (x, 350)); f2 = F(26, "s"); tw = d.textlength(l2, font=f2); d.text((x - tw / 2, 405), l2, font=f2, fill=INK)
        R.caption(d, cap); return im
    if sid == "navigateur":
        im = O.room(); d = ImageDraw.Draw(im)
        d.rectangle([0, 380, W, 470], fill=(90, 90, 100)); [d.rectangle([x, 420, x + 60, 430], fill=(255, 255, 255)) for x in range(20, W, 120)]
        x = 200 + 700 * R.ease(p)
        d.rounded_rectangle([x - 110, 330, x + 110, 400], 18, fill=(0, 120, 200)); d.polygon([(x - 60, 330), (x - 30, 290), (x + 50, 290), (x + 80, 330)], fill=(0, 100, 170))
        for wx in (x - 65, x + 65): d.ellipse([wx - 24, 380, wx + 24, 428], fill=(30, 30, 30))
        globe(d, x, 250, 30)
        if p > 0.3: O.label(d, "le navigateur = votre voiture", (W / 2, 140))
        if p > 0.55: O.label(d, "les routes d'Internet", (W / 2, 500))
        R.caption(d, cap); return im
    if sid == "noms":
        im = O.room(); d = ImageDraw.Draw(im); pastilles(d, p, t); R.caption(d, cap); return im
    if sid == "ouvrir":
        return act(lambda: screen(), lambda: screen("browser"), EDGE, (W / 2 - 200, H / 2), t, D, cap, place=(640, 330))
    if sid == "fenetre":
        im = screen("browser"); clean = im.copy(); d = ImageDraw.Draw(im)
        if p > 0.3:
            R.highlight(d, ADDR, t)
            R.loupe(im, (ADDR[0], ADDR[1], ADDR[0] + 240, ADDR[3]), place=(640, 420), clean=clean); d = ImageDraw.Draw(im)
            O.label(d, "la barre d'adresse", (640, 560))
        R.caption(d, cap); return im
    if sid == "adresse":
        tc = 0.35 * D
        if t < tc + 0.3:
            return act(lambda: screen("browser"), lambda: screen("browser", focus=True), ADDR, (W / 2, 500), t, (tc / 0.6), cap, show_loupe=False)
        n = int(len(ADRESSE) * min(1, (t - tc - 0.3) / (0.4 * D)))
        im = screen("browser", typed=ADRESSE[:n], focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
        R.loupe(im, (ADDR[0], ADDR[1], ADDR[0] + 240, ADDR[3]), place=(640, 420), clean=clean); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "entree":
        pressed = 0.35 * D < t < 0.45 * D
        if t < 0.45 * D:
            im = screen("browser", typed=ADRESSE, focus=True); d = ImageDraw.Draw(im); R.key_enter(d, t, pressed)
        else:
            im = screen("browser", typed=ADRESSE, page="google"); d = ImageDraw.Draw(im)
            if p > 0.6: O.label(d, "Bravo !", (W / 2, PAGE_Y + 380))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "fermer":
        tc = 0.6 * D; hov = t > 0.45 * D
        return act(lambda: screen("browser", typed=ADRESSE, page="google", close_hover=hov), lambda: screen(), CLOSE, (W / 2, H / 2), t, D, cap, place=(900, 360))
    if sid == "exercice":
        return R.card("Exercice", ["Ouvrez le navigateur.", "Tapez google.fr", "dans la barre d'adresse,", "puis appuyez sur Entrée."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Ouvrez le navigateur,", "tapez google.fr, puis Entrée."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 3
        if t < q:
            return act(lambda: screen(), lambda: screen("browser"), EDGE, (W / 2, H / 2), t, q, cap, show_loupe=False)
        if t < 2 * q:
            tt = t - q; n = int(len(ADRESSE) * max(0, min(1, (tt - 0.45 * q) / (0.4 * q))))
            if tt < 0.45 * q:
                return act(lambda: screen("browser"), lambda: screen("browser", focus=True), ADDR, R.center(EDGE), tt, 0.45 * q / 0.6 - 0.01, cap, show_loupe=False)
            im = screen("browser", typed=ADRESSE[:n], focus=True); d = ImageDraw.Draw(im); R.caption(d, cap); return im
        tt = t - 2 * q
        if tt < 0.4 * q:
            im = screen("browser", typed=ADRESSE, focus=True); d = ImageDraw.Draw(im); R.key_enter(d, tt, 0.25 * q < tt)
        else:
            im = screen("browser", typed=ADRESSE, page="google"); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Internet : un grand réseau mondial", "Le navigateur : le programme pour y aller", "L'adresse se tape en haut", "Puis la touche Entrée"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
