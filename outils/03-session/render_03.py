"""Vidéo « 03 - Ouvrir sa session et découvrir le bureau » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_03.py script.json durations.json out.mp4
        python3 render_03.py --estimate script.json durations.json
Réutilise ../render_01.py (fond, barre des tâches, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes)
et ../02-allumer/render_02.py (menu Démarrer, écran de verrouillage).
Libellés écrits tels quels (voir sources_03.md) : « Démarrer », « Corbeille », « Rechercher », « Épinglé ».
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../02-allumer"):
    sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_02 as V2
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163)
NOM = "Marie"

# ---------- bureau ----------
BIN = (44, 36, 124, 136)          # icône Corbeille (zone cliquable)
DOS = (44, 168, 124, 268)         # dossier « Photos »
CLOCK = (W - 150, H - R.TB_H + 4, W - 10, H - 4)

def bin_icon(d, x, y, s=1.0):
    """Poubelle dessinée (x, y = coin haut gauche, ~56 px de large à s=1)."""
    d.rounded_rectangle([x, y + 6 * s, x + 56 * s, y + 14 * s], 3, fill=(225, 230, 240), outline=(120, 130, 150), width=2)
    d.rectangle([x + 20 * s, y, x + 36 * s, y + 7 * s], fill=(225, 230, 240), outline=(120, 130, 150), width=2)
    d.polygon([(x + 5 * s, y + 15 * s), (x + 51 * s, y + 15 * s), (x + 45 * s, y + 62 * s), (x + 11 * s, y + 62 * s)], fill=(235, 240, 248), outline=(120, 130, 150))
    for k in (17, 28, 39):
        d.line([x + k * s, y + 22 * s, x + (k + (28 - k) * 0.1) * s, y + 55 * s], fill=(150, 160, 180), width=max(2, int(3 * s)))

def draw_clock(d, hl=False):
    d.text((CLOCK[0] + 34, CLOCK[1] + 3), "10:30", font=F(17, "s"), fill=(20, 20, 20))
    d.text((CLOCK[0] + 22, CLOCK[1] + 24), "25/11/2026", font=F(15), fill=(20, 20, 20))

def desktop():
    im = R.bg(); d = ImageDraw.Draw(im)
    bin_icon(d, BIN[0] + 12, BIN[1] + 4)
    d.text((BIN[0] + 2, BIN[1] + 74), "Corbeille", font=F(16, "s"), fill=(255, 255, 255), stroke_width=2, stroke_fill=(20, 40, 90))
    R.folder_icon(d, DOS[0] + 2, DOS[1] + 6, 0.8)
    d.text((DOS[0] + 8, DOS[1] + 74), "Photos", font=F(16, "s"), fill=(255, 255, 255), stroke_width=2, stroke_fill=(20, 40, 90))
    R.draw_taskbar(d); draw_clock(d)
    return im

def start_rect(): return V2.start_rect()
def search_rect():
    x, y = R.taskbar_icons()["search"]; return (x - 24, y - 22, x + 24, y + 22)
TASKBAR = (0, H - R.TB_H, W, H)

SM, PWR = V2.SM, V2.PWR
ACC = (SM[0] + 30, SM[3] - 56, SM[0] + 230, SM[3] - 6)
PIN = (SM[0] + 30, SM[1] + 70, SM[2] - 30, SM[1] + 330)
def screen(menu=False):
    """Bureau, avec ou sans menu Démarrer (menu du sujet 02 + titre « Épinglé » + nom du compte)."""
    im = desktop()
    if not menu: return im
    m = V2.screen({"start": True})
    box = (int(SM[0]) - 2, int(SM[1]) - 2, int(SM[2]) + 10, int(SM[3]) + 10)
    im.paste(m.crop(box), box[:2]); d = ImageDraw.Draw(im)
    d.text((SM[0] + 50, SM[1] + 70), "Épinglé", font=F(19, "b"), fill=(30, 30, 40))
    d.rounded_rectangle([SM[0] + 88, SM[3] - 40, SM[0] + 210, SM[3] - 18], 5, fill=(232, 234, 240))
    d.text((SM[0] + 90, SM[3] - 44), NOM, font=F(20, "s"), fill=(30, 30, 40))
    return im

# ---------- écrans de connexion ----------
def lock(): return V2.lock_screen()

AV = (W / 2, 210)
CASE = (W / 2 - 200, 360, W / 2 + 200, 410)
def login(n_points=0, caret=True, t=0.0):
    im = R.bg().filter(ImageFilter.GaussianBlur(10)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=None)
    x, y = AV
    d.ellipse([x - 80, y - 80, x + 80, y + 80], fill=(200, 205, 220))
    d.ellipse([x - 30, y - 50, x + 30, y + 10], fill=(140, 150, 175))
    d.chord([x - 56, y + 10, x + 56, y + 110], 180, 360, fill=(140, 150, 175))
    f = F(40, "s"); tw = d.textlength(NOM, font=f); d.text((x - tw / 2, 305), NOM, font=f, fill=(255, 255, 255))
    d.rounded_rectangle(CASE, 6, fill=(255, 255, 255), outline=(120, 130, 160), width=2)
    for i in range(n_points):
        cx = CASE[0] + 30 + i * 30; d.ellipse([cx - 7, 378, cx + 7, 392], fill=(20, 20, 20))
    if caret and (t % 1.0) < 0.6:
        cx = CASE[0] + 18 + n_points * 30; d.line([cx, 372, cx, 398], fill=(20, 20, 20), width=2)
    return im, d

def key(d, r, label, pressed=False, logo=False):
    off = 6 if pressed else 0
    d.rounded_rectangle([r[0] + 5, r[1] + 9, r[2] + 5, r[3] + 9], 14, fill=(60, 60, 70))
    rr = (r[0] + off / 2, r[1] + off, r[2] + off / 2, r[3] + off)
    d.rounded_rectangle(rr, 14, fill=(245, 245, 248), outline=(80, 80, 90), width=3)
    c = R.center(rr)
    if logo:
        for dx in (-17, 2):
            for dy in (-17, 2):
                d.rectangle([c[0] + dx, c[1] + dy, c[0] + dx + 15, c[1] + dy + 15], fill=(0, 120, 215))
    else:
        f = F(40, "b"); tw = d.textlength(label, font=f); d.text((c[0] - tw / 2, c[1] - 26), label, font=f, fill=(20, 20, 20))

def check(d, x, y, s=50): V2.check(d, x, y, s)

# ---------- clic animé sur l'écran ----------
def act(menu_b, menu_a, r, start, t, D, cap, show_loupe=True):
    c = R.center(r); tc = 0.6 * D
    im = screen(menu_a if t >= tc + 0.3 else menu_b); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3:
        R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6); R.caption(d, cap)
    return im

def show(im, r, t, cap, loupe=True, arrow=True, place=None):
    clean = im.copy(); d = ImageDraw.Draw(im)
    R.highlight(d, r, t)
    if arrow: R.arrow(d, r, t)
    if loupe:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.caption(d, cap); return im

def typing(p, a, b, n=4): return max(0, min(n, int((p - a) / (b - a) * n) + (1 if p >= a else 0))) if p >= a else 0

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Ouvrir sa session", ["et découvrir le bureau", "Aide-mémoire n° 03 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); d.ellipse([W / 2 - 60, 330, W / 2 + 60, 450], fill=VIO)
        d.rounded_rectangle([W / 2 - 26, 384, W / 2 + 26, 424], 6, fill=(255, 255, 255))
        d.arc([W / 2 - 18, 352, W / 2 + 18, 400], 180, 360, fill=(255, 255, 255), width=8)
        return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im)
        # porte + clé
        d.rounded_rectangle([170, 130, 400, 470], 8, fill=(150, 95, 60), outline=(90, 55, 30), width=5)
        d.ellipse([360, 290, 382, 312], fill=YEL)
        if p > 0.15:
            d.ellipse([440, 260, 490, 310], outline=YEL, width=10); d.line([490, 285, 560, 285], fill=YEL, width=10)
            d.line([540, 285, 540, 305], fill=YEL, width=8); d.line([555, 285, 555, 300], fill=YEL, width=8)
            O.label(d, "votre code = la clé", (420, 120))
        if p > 0.5:
            sc = (720, 170, 1140, 420); d.rounded_rectangle([sc[0] - 14, sc[1] - 14, sc[2] + 14, sc[3] + 14], 12, fill=(30, 32, 40))
            mini = desktop().resize((sc[2] - sc[0], sc[3] - sc[1]), Image.LANCZOS); im.paste(mini, sc[:2]); d = ImageDraw.Draw(im)
            O.label(d, "le bureau = votre table de travail", (930, 470))
        R.caption(d, cap); return im
    if sid == "verrou":
        im, d = lock()
        if p > 0.35:
            key(d, (W / 2 - 230, 400, W / 2 - 70, 500), "A", pressed=(p % 0.25) < 0.1)
            d.text((W / 2 - 22, 430), "ou", font=F(34, "b"), fill=(255, 255, 255))
            R.cursor(d, W / 2 + 120, 430, 2.0); R.ripple(d, W / 2 + 125, 435, ((p - 0.35) % 0.3) / 0.3)
        R.caption(d, cap); return im
    if sid == "code":
        n = typing(p, 0.42, 0.75)
        im, d = login(n, t=t)
        if p < 0.42:
            R.highlight(d, CASE, t); R.arrow(d, CASE, t)
        if p > 0.78:
            O.label(d, "votre code reste secret", (W / 2, 470))
        R.caption(d, cap); return im
    if sid == "entree":
        im, d = login(4, caret=False)
        key(d, (W / 2 - 120, 450, W / 2 + 120, 560), "Entrée ↵", pressed=p > 0.55)
        if (t % 0.7) < 0.47 and p < 0.55: d.rounded_rectangle([W / 2 - 132, 438, W / 2 + 132, 572], 18, outline=YEL, width=9)
        R.caption(d, cap); return im
    if sid == "bureau":
        im = screen(False); d = ImageDraw.Draw(im)
        if p > 0.15: check(d, 1150, 130)
        if p > 0.5:
            R.highlight(d, BIN, t); R.highlight(d, DOS, t); O.label(d, "des icônes", (300, 150))
        R.caption(d, cap); return im
    if sid == "corbeille":
        return show(screen(False), BIN, t, cap, place=(700, 330))
    if sid == "barre":
        im = screen(False); d = ImageDraw.Draw(im)
        R.highlight(d, (8, TASKBAR[1] + 4, W - 8, H - 4), t)
        b = 10 * math.sin(t * 6)
        for x in (300, 640, 980):
            d.line([x, 470 + b, x, 600 + b], fill=(0, 0, 0), width=22); d.line([x, 470 + b, x, 600 + b], fill=YEL, width=14)
            d.polygon([(x - 26, 600 + b), (x + 26, 600 + b), (x, 640 + b)], fill=YEL, outline=(0, 0, 0))
        R.caption(d, cap); return im
    if sid == "demarrer":
        return show(screen(False), start_rect(), t, cap)
    if sid == "rechercher":
        return show(screen(False), search_rect(), t, cap)
    if sid == "heure":
        return show(screen(False), CLOCK, t, cap, arrow=True, place=(1000, 330))
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et ouvrez votre session."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "menu":
        if p < 0.45:
            return act(False, True, start_rect(), (W / 2 + 220, H / 2 - 60), t, 0.45 * D, cap)
        im = screen(True); d = ImageDraw.Draw(im)
        R.highlight(d, PIN, t); O.label(d, "Épinglé : vos programmes", (W / 2 + 150, 100))
        R.caption(d, cap); return im
    if sid == "compte":
        im = screen(True); d = ImageDraw.Draw(im)
        R.highlight(d, ACC, t)
        if p > 0.45: R.highlight(d, PWR, t + 0.35)
        O.label(d, "votre nom", (ACC[0] - 10, ACC[1] - 40)) if p < 0.45 else O.label(d, "Marche/Arrêt", (PWR[0] + 10, PWR[1] - 40))
        R.caption(d, cap); return im
    if sid == "fermer":
        if p < 0.75:
            return act(True, False, start_rect(), R.center(PWR), t, 0.75 * D, cap)
        im = screen(False); d = ImageDraw.Draw(im); check(d, 1150, 130); R.caption(d, cap); return im
    if sid == "verrouiller":
        if p < 0.6:
            im = screen(False); d = ImageDraw.Draw(im)
            d.rounded_rectangle([250, 170, 1030, 470], 24, fill=(255, 255, 255), outline=YEL, width=6)
            pr = (p % 0.3) > 0.18 and p > 0.15
            key(d, (330, 240, 490, 380), "", pressed=pr, logo=True)
            d.text((560, 270), "+", font=F(80, "b"), fill=INK)
            key(d, (690, 240, 850, 380), "L", pressed=pr)
            d.text((395, 400), "Windows", font=F(26, "s"), fill=INK); d.text((735, 400), "lettre L", font=F(26, "s"), fill=INK)
        else:
            im, d = lock(); O.label(d, "écran verrouillé", (W / 2, 420))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Ouvrez votre session :", "une touche, puis votre code.", "Ouvrez le menu « Démarrer »,", "puis fermez-le."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Ouvrez votre session,", "puis le menu « Démarrer »."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        if p < 0.15:
            im, d = lock(); key(d, (W / 2 - 80, 400, W / 2 + 80, 500), "A", pressed=p > 0.08)
        elif p < 0.42:
            im, d = login(typing(p, 0.18, 0.36), t=t)
        elif p < 0.71:
            return act(False, True, start_rect(), (W / 2, H / 2), t - 0.42 * D, 0.29 * D, cap, show_loupe=False)
        else:
            return act(True, False, start_rect(), (W / 2 + 200, H / 2), t - 0.71 * D, 0.29 * D, cap, show_loupe=False)
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Ouvrir : une touche, puis mon code", "Le bureau : ma table de travail", "En bas : la barre des tâches", "Tout commence par « Démarrer »"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
