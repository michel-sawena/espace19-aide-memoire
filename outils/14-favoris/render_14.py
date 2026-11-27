"""Vidéo « 14 - Ajouter et retrouver ses favoris » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_14.py script.json durations.json out.mp4
        python3 render_14.py --estimate script.json durations.json
Réutilise ../render_01.py, ../01-ordinateur/render_01_ordinateur.py et ../12-internet/render_12.py (fenêtre du navigateur).
Navigateur dessiné de façon simplifiée, sans logo. Libellés écrits tels quels : « barre d'adresse », « Favoris »
(voir sources_14.md). Le bouton de validation n'a pas de texte (libellé non confirmé en français) : une coche blanche.
Les autres lignes du menu sont des barres grises (libellés non vérifiés, donc non écrits).
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as N
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); BLEU = (0, 103, 192)
BX, BY, BW, BH, BAR_Y, PAGE_Y, ADDR = N.BX, N.BY, N.BW, N.BH, N.BAR_Y, N.PAGE_Y, N.ADDR

STAR = (ADDR[2] - 50, ADDR[1] + 2, ADDR[2] - 12, ADDR[3] - 2)
DOTS = (BX + BW - 84, BAR_Y + 12, BX + BW - 40, BAR_Y + 48)
DLG = (ADDR[2] - 470, PAGE_Y + 8, ADDR[2] + 10, PAGE_Y + 250)
BTN = (DLG[2] - 150, DLG[3] - 62, DLG[2] - 24, DLG[3] - 18)
MENU = (BX + BW - 360, PAGE_Y + 2, BX + BW - 16, PAGE_Y + 330)
FAVITEM = (MENU[0] + 8, MENU[1] + 110, MENU[2] - 8, MENU[1] + 156)
PANEL = (BX + BW - 400, PAGE_Y + 2, BX + BW - 16, PAGE_Y + 260)
FAVROW = (PANEL[0] + 14, PANEL[1] + 70, PANEL[2] - 14, PANEL[1] + 118)

def star_shape(cx, cy, r):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

def star(d, r, filled):
    cx, cy = R.center(r); pts = star_shape(cx, cy, 15)
    if filled: d.polygon(pts, fill=BLEU, outline=BLEU)
    else: d.line(pts + [pts[0]], fill=(70, 70, 80), width=3)

def dots(d):
    cx, cy = R.center(DOTS)
    for k in (-12, 0, 12): d.ellipse([cx + k - 4, cy - 4, cx + k + 4, cy + 4], fill=(70, 70, 80))

def check(d, r, col=(255, 255, 255)):
    cx, cy = R.center(r); d.line([cx - 16, cy, cx - 4, cy + 12, cx + 18, cy - 12], fill=col, width=6, joint="curve")

def dialog(d):
    d.rounded_rectangle([DLG[0] + 5, DLG[1] + 7, DLG[2] + 5, DLG[3] + 7], 12, fill=(150, 155, 170))
    d.rounded_rectangle(DLG, 12, fill=(255, 255, 255), outline=(170, 175, 190), width=2)
    star(d, (DLG[0] + 20, DLG[1] + 14, DLG[0] + 56, DLG[1] + 50), True)
    d.text((DLG[0] + 66, DLG[1] + 18), "Favoris", font=F(24, "b"), fill=(30, 30, 30))
    for i, (lab, val) in enumerate((("Nom", "Google"), ("Dossier", "Favoris"))):
        y = DLG[1] + 66 + i * 54
        d.text((DLG[0] + 22, y + 9), lab, font=F(19), fill=(60, 60, 70))
        d.rounded_rectangle([DLG[0] + 120, y, DLG[2] - 22, y + 42], 6, fill=(246, 247, 250), outline=(180, 185, 195))
        d.text((DLG[0] + 134, y + 9), val, font=F(20), fill=(20, 20, 20))
    d.rounded_rectangle(BTN, 8, fill=BLEU); check(d, BTN)
    d.rounded_rectangle([BTN[0] - 150, BTN[1], BTN[0] - 18, BTN[3]], 8, fill=(255, 255, 255), outline=(180, 185, 195))

def menu(d):
    d.rounded_rectangle([MENU[0] + 5, MENU[1] + 7, MENU[2] + 5, MENU[3] + 7], 10, fill=(150, 155, 170))
    d.rounded_rectangle(MENU, 10, fill=(255, 255, 255), outline=(170, 175, 190), width=2)
    for i in range(6):
        y = MENU[1] + 20 + i * 50
        if i == 2:
            star(d, (MENU[0] + 20, y - 2, MENU[0] + 56, y + 34), False)
            d.text((MENU[0] + 70, y + 2), "Favoris", font=F(23, "s"), fill=(20, 20, 20))
        else:
            d.rounded_rectangle([MENU[0] + 28, y + 8, MENU[0] + 48, y + 26], 4, fill=(215, 218, 226))
            d.rounded_rectangle([MENU[0] + 70, y + 10, MENU[0] + 70 + 150 + 30 * (i % 3), y + 24], 6, fill=(225, 228, 234))

def panel(d):
    d.rounded_rectangle([PANEL[0] + 5, PANEL[1] + 7, PANEL[2] + 5, PANEL[3] + 7], 10, fill=(150, 155, 170))
    d.rounded_rectangle(PANEL, 10, fill=(255, 255, 255), outline=(170, 175, 190), width=2)
    d.text((PANEL[0] + 20, PANEL[1] + 18), "Favoris", font=F(24, "b"), fill=(30, 30, 30))
    N.globe(d, FAVROW[0] + 24, (FAVROW[1] + FAVROW[3]) / 2, 13)
    d.text((FAVROW[0] + 50, FAVROW[1] + 11), "Google", font=F(22, "s"), fill=(20, 20, 20))
    for i in range(2):
        y = FAVROW[3] + 22 + i * 46
        d.ellipse([FAVROW[0] + 12, y, FAVROW[0] + 36, y + 24], fill=(215, 218, 226))
        d.rounded_rectangle([FAVROW[0] + 50, y + 6, FAVROW[0] + 220 - 40 * i, y + 18], 6, fill=(225, 228, 234))

def scr(page="google", filled=False, dlg=False, mnu=False, pnl=False, typed=None):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    N.browser(d, typed=(N.ADRESSE if page and typed is None else (typed or "")), page=page)
    star(d, STAR, filled); dots(d)
    if dlg: dialog(d)
    if mnu: menu(d)
    if pnl: panel(d)
    return im

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None, label=None, lr=None):
    c = R.center(r); tc = 0.6 * D
    im = (after if t >= tc + 0.3 else before)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, lr or r, place=place, clean=clean); d = ImageDraw.Draw(im)
    if label and t < tc + 0.3: O.label(d, label, (W / 2, 560))
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    R.caption(d, cap); return im

def key(d, x, y, w, txt, pressed, t):
    off = 7 if pressed else 0
    d.rounded_rectangle([x + 6, y + 10, x + w + 6, y + 110], 16, fill=(60, 60, 70))
    d.rounded_rectangle([x, y + off, x + w, y + 100 + off], 16, fill=(245, 245, 248), outline=(80, 80, 90), width=3)
    f = F(40, "b"); tw = d.textlength(txt, font=f); d.text((x + w / 2 - tw / 2, y + 26 + off), txt, font=f, fill=(20, 20, 20))
    if pressed and (t % 0.7) < 0.47: d.rounded_rectangle([x - 12, y - 12, x + w + 12, y + 122], 18, outline=YEL, width=9)

def livre(d, p):
    cx, cy = W / 2, 330
    d.polygon([(cx - 300, cy - 150), (cx, cy - 120), (cx, cy + 150), (cx - 300, cy + 120)], fill=(255, 250, 235), outline=(120, 100, 80))
    d.polygon([(cx + 300, cy - 150), (cx, cy - 120), (cx, cy + 150), (cx + 300, cy + 120)], fill=(255, 250, 235), outline=(120, 100, 80))
    for k in range(6):
        y = cy - 90 + k * 36
        d.line([cx - 260, y - 8 + k * 2, cx - 40, y + k * 2], fill=(200, 195, 185), width=4)
        d.line([cx + 40, y + k * 2, cx + 260, y - 8 + k * 2], fill=(200, 195, 185), width=4)
    if p > 0.3:
        q = R.ease((p - 0.3) / 0.2)
        d.polygon([(cx + 150, cy - 200 + 60 * (1 - q)), (cx + 190, cy - 200 + 60 * (1 - q)), (cx + 190, cy + 40), (cx + 170, cy + 20), (cx + 150, cy + 40)], fill=VIO)
    if p > 0.5: O.label(d, "un marque-page", (cx + 170, cy + 175))
    if p > 0.7:
        d.polygon(star_shape(cx - 360, cy - 140, 55), fill=YEL, outline=INK); O.label(d, "un favori", (cx - 360, cy - 60))

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Ajouter et retrouver ses favoris", ["Aide-mémoire n° 14 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); d.polygon(star_shape(W / 2, 370, 90), fill=YEL, outline=INK); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); livre(d, p); R.caption(d, cap); return im
    if sid == "site":
        if p < 0.35: im = scr(page=None)
        else: im = scr()
        d = ImageDraw.Draw(im)
        if p > 0.6: R.highlight(d, ADDR, t); O.label(d, "le site que vous aimez", (W / 2, 560))
        R.caption(d, cap); return im
    if sid == "etoile":
        return act(lambda: scr(), lambda: scr(dlg=True), STAR, (W / 2, 450), t, D, cap, place=(700, 400), label="l'étoile, au bout de la barre d'adresse")
    if sid == "fenetre":
        if p < 0.3:
            im = scr(dlg=True); d = ImageDraw.Draw(im); R.highlight(d, DLG, t); R.caption(d, cap); return im
        return act(lambda: scr(dlg=True), lambda: scr(filled=True), BTN, (W / 2, 520), t - 0.3 * D, 0.7 * D, cap, place=(400, 380), label="le bouton bleu")
    if sid == "rempli":
        im = scr(filled=True); clean = im.copy(); d = ImageDraw.Draw(im)
        R.highlight(d, STAR, t); R.loupe(im, STAR, place=(330, 400), clean=clean); d = ImageDraw.Draw(im)
        if p > 0.4: O.label(d, "Bravo ! La page est dans vos favoris", (760, 520))
        R.caption(d, cap); return im
    if sid in ("pause1", "pause2"):
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "points":
        if p < 0.3:
            im = R.screen({"window": False}) if p < 0.15 else scr(page=None, filled=False)
            d = ImageDraw.Draw(im); O.label(d, "un autre jour…", (W / 2, 300)); R.caption(d, cap); return im
        return act(lambda: scr(page=None), lambda: scr(page=None, mnu=True), DOTS, (W / 2, 450), t - 0.3 * D, 0.7 * D, cap, place=(500, 400), label="les trois petits points")
    if sid == "favoris":
        return act(lambda: scr(page=None, mnu=True), lambda: scr(page=None, pnl=True), FAVITEM, (W / 2, 500), t, D, cap, place=(450, 400), lr=(FAVITEM[0], FAVITEM[1], FAVITEM[0] + 140, FAVITEM[3]))
    if sid == "liste":
        if p < 0.6:
            return act(lambda: scr(page=None, pnl=True), lambda: scr(filled=True), FAVROW, (W / 2, 500), t, 0.6 * D, cap, place=(450, 400), label="le nom du site", lr=(FAVROW[0], FAVROW[1], FAVROW[0] + 130, FAVROW[3]))
        im = scr(filled=True); d = ImageDraw.Draw(im); O.label(d, "Rien à taper !", (W / 2, PAGE_Y + 380)); R.caption(d, cap); return im
    if sid == "bonus":
        im = O.room(); d = ImageDraw.Draw(im)
        pr = p > 0.55 and (p < 0.9)
        key(d, W / 2 - 290, 250, 220, "Ctrl", pr, t)
        f = F(60, "b"); d.text((W / 2 - 20, 270), "+", font=f, fill=INK)
        key(d, W / 2 + 70, 250, 140, "D", pr, t)
        if p > 0.3: O.label(d, "en même temps", (W / 2, 420))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Allez sur google.fr.", "Ajoutez la page aux favoris.", "Fermez puis rouvrez le navigateur,", "et retrouvez la page dans vos favoris."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["L'étoile pour ajouter,", "les trois points puis Favoris pour retrouver."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 5; k = int(min(4, t // q)); tt = t - k * q
        steps = [(lambda: scr(), lambda: scr(dlg=True), STAR, (W / 2, 450)),
                 (lambda: scr(dlg=True), lambda: scr(filled=True), BTN, R.center(STAR)),
                 (lambda: scr(page=None), lambda: scr(page=None, mnu=True), DOTS, (W / 2, 450)),
                 (lambda: scr(page=None, mnu=True), lambda: scr(page=None, pnl=True), FAVITEM, R.center(DOTS)),
                 (lambda: scr(page=None, pnl=True), lambda: scr(filled=True), FAVROW, R.center(FAVITEM))]
        b, a, r, s = steps[k]
        return act(b, a, r, s, tt, q * 0.8, cap, show_loupe=False) if tt < q * 0.8 * 0.6 + 0.3 else (lambda im: (R.caption(ImageDraw.Draw(im), cap), im)[1])(a())
    if sid == "resume":
        return R.card("À retenir", ["L'étoile : pour ajouter un favori", "Les trois points, puis « Favoris » :", "pour retrouver la page", "Astuce : Ctrl + D"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
