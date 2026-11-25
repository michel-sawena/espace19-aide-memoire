"""Vidéo « 02 - Allumer et éteindre l'ordinateur » (appareils et écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_02.py script.json durations.json out.mp4
        python3 render_02.py --estimate script.json durations.json
Réutilise ../render_01.py (écran Windows, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes)
et ../01-ordinateur/render_01_ordinateur.py (pièce, unité centrale, portable).
Libellés écrits tels quels : « Démarrer », « Marche/Arrêt », « Arrêter », « Redémarrer » (voir sources_02.md).
La première ligne du petit menu (mise en veille) est dessinée sans texte : libellé non confirmé par deux sources.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, "..")); sys.path.insert(0, os.path.join(ICI, "..", "01-ordinateur"))
import render_01 as R
import render_01_ordinateur as O
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); ROUGE = (230, 60, 50)

# ---------- symbole Marche/Arrêt ----------
def power_symbol(d, cx, cy, r, col=(255, 255, 255), w=None):
    w = w or max(3, int(r / 4))
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 240, fill=col, width=w)
    d.line([cx, cy - r - w / 2, cx, cy + w / 4], fill=col, width=w)

def spinner(d, cx, cy, t, r=30):
    for i in range(6):
        a = t * 5 - i * 0.45
        k = 1 - i / 7
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        s = 3 + 5 * k
        d.ellipse([x - s, y - s, x + s, y + s], fill=(int(255 * k), int(255 * k), int(255 * k)))

# ---------- ordinateurs ----------
def fixe(spin=None, led=False):
    """spin : None = écran éteint ; un temps t = points qui tournent."""
    im = O.room(); d = ImageDraw.Draw(im); O.draw_fixe(d)
    d.rectangle(O.MON, fill=(8, 8, 12))
    if spin is not None:
        spinner(d, R.center(O.MON)[0], R.center(O.MON)[1] + 30, spin, 22)
    if led:
        pb = O.power_button_rect(); c = R.center(pb)
        d.ellipse([c[0] - 22, c[1] - 22, c[0] + 22, c[1] + 22], outline=(80, 160, 255), width=4)
    return im, d

LAP_BTN = (836, 372, 868, 388)
def laptop(open_=True, on=False, t=0.0):
    im = O.room(); d = ImageDraw.Draw(im)
    if open_:
        O.draw_laptop(d)
        d.rounded_rectangle(LAP_BTN, 4, fill=(40, 42, 50))
        power_symbol(d, *R.center(LAP_BTN), 5, (230, 230, 240), 2)
        if not on:
            d.rectangle(O.LAP_SCR, fill=(8, 8, 12))
        elif on is True:
            pass
        else:
            d.rectangle(O.LAP_SCR, fill=(8, 8, 12)); spinner(d, R.center(O.LAP_SCR)[0], R.center(O.LAP_SCR)[1] + 20, t, 18)
    else:
        d.polygon([(340, 470), (940, 470), (930, 482), (350, 482)], fill=(110, 112, 122))
        d.polygon([(350, 452), (930, 452), (940, 470), (340, 470)], fill=(150, 152, 162), outline=(110, 112, 122))
    return im, d

LID = (O.LAP_SCR[0] - 16, O.LAP_SCR[1] - 18, O.LAP_SCR[2] + 16, 368)
def laptop_lid(k, screen_on=True):
    """Portable dont l'écran se rabat : k = 0 ouvert, k = 1 fermé. Renvoie (image, dessin)."""
    full = O.room(); df = ImageDraw.Draw(full); O.draw_laptop(df)
    df.rounded_rectangle(LAP_BTN, 4, fill=(40, 42, 50)); power_symbol(df, *R.center(LAP_BTN), 5, (230, 230, 240), 2)
    if not screen_on: df.rectangle(O.LAP_SCR, fill=(8, 8, 12))
    bg_ = (LID[0] - 3, LID[1] - 3, LID[2] + 3, LID[3]); im = full.copy(); im.paste(O.room().crop(bg_), bg_[:2])
    lid = full.crop((LID[0], LID[1], LID[2] + 1, LID[3])); h = max(10, int(lid.height * (1 - k)))
    lid = lid.resize((lid.width, h), Image.LANCZOS)
    im.paste(lid, (LID[0], LID[3] - h))
    return im, ImageDraw.Draw(im)

def finger(d, x, y):
    d.rounded_rectangle([x - 16, y, x + 16, y + 110], 16, fill=(240, 200, 170), outline=(150, 100, 80), width=3)
    d.ellipse([x - 9, y + 6, x + 9, y + 20], fill=(250, 225, 210))

def press(d, r, p, t, a=0.35, b=0.6):
    """Doigt qui descend sur le bouton r puis remonte, entre a et b (fraction de scène)."""
    c = R.center(r); q = (p - a) / (b - a)
    y = c[1] + 120 - (110 * math.sin(math.pi * q) if 0 <= q <= 1 else 0)
    if 0 <= q <= 1: finger(d, c[0], y)
    if 0.4 < q < 1.0: R.ripple(d, c[0], c[1], (q - 0.4) / 0.6)

# ---------- écran Windows : menu Démarrer ----------
SM = (W / 2 - 310, 110, W / 2 + 310, 550)
PWR = (W / 2 + 240, 500, W / 2 + 288, 540)
PM = (W / 2 + 60, 330, W / 2 + 300, 480)
def pm_item(i): return (PM[0] + 8, PM[1] + 8 + i * 47, PM[2] - 8, PM[1] + 50 + i * 47)
def start_rect():
    x, y = R.taskbar_icons()["start"]; return (x - 24, y - 22, x + 24, y + 22)

def screen(st):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if st.get("start"):
        d.rounded_rectangle([SM[0] + 6, SM[1] + 8, SM[2] + 6, SM[3] + 8], 14, fill=(10, 30, 70))
        d.rounded_rectangle(SM, 14, fill=(243, 244, 248), outline=(170, 175, 190), width=2)
        d.rounded_rectangle([SM[0] + 30, SM[1] + 24, SM[2] - 30, SM[1] + 64], 20, fill=(255, 255, 255), outline=(190, 195, 205), width=2)
        d.ellipse([SM[0] + 46, SM[1] + 34, SM[0] + 64, SM[1] + 52], outline=(80, 80, 90), width=3)
        cols = [(0, 120, 215), (250, 200, 70), (0, 140, 200), (230, 90, 60), (80, 180, 90), (140, 90, 200)]
        for j in range(3):
            for i in range(6):
                x = SM[0] + 50 + i * 90; y = SM[1] + 100 + j * 100
                d.rounded_rectangle([x, y, x + 44, y + 44], 8, fill=cols[(i + j * 2) % 6])
                d.rounded_rectangle([x - 4, y + 54, x + 50, y + 64], 4, fill=(200, 204, 212))
        d.rectangle([SM[0] + 2, SM[3] - 62, SM[2] - 2, SM[3] - 2], fill=(232, 234, 240))
        d.line([SM[0] + 2, SM[3] - 62, SM[2] - 2, SM[3] - 62], fill=(210, 214, 222), width=2)
        d.ellipse([SM[0] + 40, SM[3] - 48, SM[0] + 76, SM[3] - 12], fill=(160, 170, 190))
        d.rounded_rectangle([SM[0] + 90, SM[3] - 36, SM[0] + 200, SM[3] - 24], 5, fill=(190, 195, 205))
        if st.get("power"):
            d.rounded_rectangle(PWR, 8, fill=(215, 225, 240))
        power_symbol(d, *R.center(PWR), 11, (40, 40, 50), 3)
    if st.get("power"):
        d.rounded_rectangle([PM[0] + 4, PM[1] + 6, PM[2] + 4, PM[3] + 6], 10, fill=(60, 70, 100))
        d.rounded_rectangle(PM, 10, fill=(252, 252, 254), outline=(170, 175, 190), width=2)
        hov = st.get("hover")
        for i, lab in enumerate((None, "Arrêter", "Redémarrer")):
            r = pm_item(i)
            if hov == i: d.rounded_rectangle(r, 6, fill=(220, 232, 248))
            ix, iy = r[0] + 24, (r[1] + r[3]) / 2
            if lab is None:
                d.ellipse([ix - 9, iy - 9, ix + 9, iy + 9], outline=(120, 120, 130), width=3)
                d.rounded_rectangle([r[0] + 50, iy - 6, r[0] + 170, iy + 6], 5, fill=(215, 218, 226))
            else:
                if lab == "Arrêter": power_symbol(d, ix, iy, 9, (40, 40, 50), 3)
                else:
                    d.arc([ix - 10, iy - 10, ix + 10, iy + 10], 20, 330, fill=(40, 40, 50), width=3)
                    d.polygon([(ix + 6, iy - 14), (ix + 14, iy - 6), (ix + 4, iy - 4)], fill=(40, 40, 50))
                d.text((r[0] + 50, iy - 13), lab, font=F(21, "s"), fill=(20, 20, 20))
    return im

def act(st_b, st_a, r, start, t, D, cap, show_loupe=True):
    """Curseur vers la cible, cadre clignotant + flèche + loupe, clic à 60 %."""
    c = R.center(r); tc = 0.6 * D
    st = st_a if t >= tc + 0.3 else st_b
    im = screen(st); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3:
        R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6); R.caption(d, cap)
    return im

def black(t, spin=True):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    if spin: spinner(d, W / 2, H / 2 + 40, t)
    return im, d

def lock_screen():
    im = R.bg(); d = ImageDraw.Draw(im)
    f = F(120, "s"); tw = d.textlength("10:30", font=f); d.text((W / 2 - tw / 2, 120), "10:30", font=f, fill=(255, 255, 255))
    f2 = F(32, "s"); s = "mercredi 25 novembre"; tw = d.textlength(s, font=f2); d.text((W / 2 - tw / 2, 270), s, font=f2, fill=(255, 255, 255))
    return im, d

def check(d, x, y, s=50):
    d.ellipse([x - s, y - s, x + s, y + s], fill=VERT)
    d.line([x - s * 0.5, y + s * 0.02, x - s * 0.1, y + s * 0.4, x + s * 0.55, y - s * 0.4], fill=(255, 255, 255), width=int(s / 4))

def cross(d, r):
    d.line([r[0], r[1], r[2], r[3]], fill=ROUGE, width=12); d.line([r[2], r[1], r[0], r[3]], fill=ROUGE, width=12)

# ---------- scènes ----------
S0 = {}; S1 = {"start": True}; S2 = {"start": True, "power": True}
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Allumer et éteindre", ["l'ordinateur", "Aide-mémoire n° 02 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); d.ellipse([W / 2 - 60, 330, W / 2 + 60, 450], fill=VIO); power_symbol(d, W / 2, 390, 34, (255, 255, 255), 9)
        return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im)
        d.ellipse([200, 170, 440, 410], fill=(52, 54, 64)); power_symbol(d, 320, 290, 60, (255, 255, 255), 14)
        if p > 0.15: O.label(d, "Allumer : un bouton", (320, 430))
        if p > 0.4:
            sc = (760, 160, 1120, 380); d.rounded_rectangle([sc[0] - 14, sc[1] - 14, sc[2] + 14, sc[3] + 14], 12, fill=(30, 32, 40)); O.wallpaper(d, sc)
            R.cursor(d, 960, 280, 1.4)
            O.label(d, "Éteindre : par l'écran", (940, 430))
        R.caption(d, cap); return im
    if sid == "bouton":
        im = O.room(); d = ImageDraw.Draw(im)
        d.ellipse([W / 2 - 150, 120, W / 2 + 150, 420], fill=(52, 54, 64), outline=(30, 30, 36), width=6)
        power_symbol(d, W / 2, 270, 80, (255, 255, 255), 18)
        R.highlight(d, (W / 2 - 150, 120, W / 2 + 150, 420), t)
        if p > 0.45:
            O.label(d, "un rond ouvert", (260, 200)); O.label(d, "+ un petit trait", (1020, 200))
        R.caption(d, cap); return im
    if sid == "fixe":
        on = p > 0.55
        im, d = fixe(t if on else None, led=on); clean = im.copy()
        pb = O.power_button_rect()
        if p < 0.55:
            R.highlight(d, pb, t); R.arrow(d, pb, t)
        if 0.15 < p < 0.6:
            R.loupe(im, pb, place=(170, 250), clean=clean); d = ImageDraw.Draw(im)
        press(d, pb, p, t, 0.3, 0.6)
        if p > 0.62: O.label(d, "une seule fois", (170, 140))
        R.caption(d, cap); return im
    if sid == "portable":
        if p < 0.3:
            im, d = laptop_lid(1 - R.ease(p / 0.25), screen_on=False)
            O.label(d, "j'ouvre l'écran", (640, 160))
        else:
            on = p > 0.75
            im, d = laptop(True, "spin" if on else False, t); clean = im.copy()
            if not on:
                R.highlight(d, LAP_BTN, t); R.arrow(d, LAP_BTN, t)
            if 0.35 < p < 0.78:
                R.loupe(im, LAP_BTN, place=(1080, 250), clean=clean); d = ImageDraw.Draw(im)
            press(d, LAP_BTN, p, t, 0.55, 0.75)
            if p > 0.78: O.label(d, "une seule fois", (1080, 140))
        R.caption(d, cap); return im
    if sid == "attendre":
        im, d = black(t)
        k = int(t) % 4
        d.text((W / 2 - 150, H / 2 + 110), "je patiente" + "." * k, font=F(34, "b"), fill=YEL)
        R.caption(d, cap); return im
    if sid == "verrou":
        im, d = lock_screen()
        if p > 0.35: check(d, 1120, 200)
        if p > 0.35: O.label(d, "écran de verrouillage", (W / 2, 380))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et allumez votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "eteindre":
        im, d = fixe(False);
        im = O.room(); d = ImageDraw.Draw(im); O.draw_tower(d, (120, 180, 300, 468))
        pb = O.power_button_rect((120, 180, 300, 468))
        if p > 0.15: cross(d, (pb[0] - 30, pb[1] - 30, pb[2] + 30, pb[3] + 30)); O.label(d, "pas le bouton", (210, 120))
        if p > 0.4:
            d.rounded_rectangle([420, 140, 1180, 470], 22, fill=(255, 255, 255), outline=YEL, width=6)
            for i, s in enumerate(("Démarrer", "Marche/Arrêt", "Arrêter")):
                if p > 0.45 + i * 0.12:
                    y = 175 + i * 95
                    d.ellipse([450, y, 520, y + 70], fill=YEL); d.text((472, y + 12), str(i + 1), font=F(38, "b"), fill=INK)
                    d.text((550, y + 14), "Cliquez sur « " + s + " »", font=F(34, "b"), fill=INK)
        R.caption(d, cap); return im
    if sid == "demarrer":
        return act(S0, S1, start_rect(), (W / 2 + 220, H / 2), t, D, cap)
    if sid == "marche":
        return act(S1, S2, PWR, R.center(start_rect()), t, D, cap)
    if sid == "arreter":
        if p < 0.68:
            return act(dict(S2, hover=1) if p > 0.45 else S2, dict(S2, hover=1), pm_item(1), R.center(PWR), t, D, cap)
        return _after_arreter(t, cap)
    if sid == "noir":
        if p < 0.35:
            im, d = black(t)
        else:
            im, d = laptop(True, False)
            if p > 0.5:
                R.highlight(d, (O.LAP_SCR[0] - 16, O.LAP_SCR[1] - 18, O.LAP_SCR[2] + 16, 368), t)
            if p > 0.6: check(d, 1100, 220, 46); O.label(d, "écran noir : éteint", (1050, 300))
        R.caption(d, cap); return im
    if sid == "redemarrer":
        im = screen(dict(S2, hover=2)); clean = im.copy(); d = ImageDraw.Draw(im)
        r = pm_item(2); R.highlight(d, r, t); R.arrow(d, r, t)
        R.loupe(im, r, clean=clean); d = ImageDraw.Draw(im)
        R.cursor(d, *R.center(r))
        R.caption(d, cap); return im
    if sid == "capot":
        im, d = laptop_lid(R.ease((p - 0.2) / 0.4) if p > 0.2 else 0)
        if p > 0.65:
            d.text((980, 330), "Z z z", font=F(56, "b"), fill=VIO)
            O.label(d, "en veille, pas éteint", (W / 2, 140))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Éteignez votre ordinateur :", "Démarrer › Marche/Arrêt › Arrêter", "puis rallumez-le", "(un appui bref sur le bouton)."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Éteignez, puis rallumez", "votre ordinateur."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        seg = [(S0, S1, start_rect(), (W / 2, H / 2), 0.0, 0.2), (S1, S2, PWR, R.center(start_rect()), 0.2, 0.4), (S2, S2, pm_item(1), R.center(PWR), 0.4, 0.58)]
        for a_, b_, r, s, x0, x1 in seg:
            if x0 * D <= t < x1 * D:
                return act(a_, b_, r, s, t - x0 * D, (x1 - x0) * D, cap, show_loupe=False)
        if p < 0.72:
            im, d = black(t)
        else:
            on = p > 0.88
            im, d = fixe(t if on else None, led=on); pb = O.power_button_rect()
            if not on: R.highlight(d, pb, t)
            press(d, pb, (p - 0.72) / 0.28, t, 0.2, 0.55)
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Allumer : un appui bref sur le bouton", "Éteindre : Démarrer", "› Marche/Arrêt › Arrêter", "Puis attendre l'écran noir"], "Bravo ! À bientôt à Espace 19 Numérique !")
    raise KeyError(sid)

def _after_arreter(t, cap):
    im, d = black(t); R.caption(d, cap); return im

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
