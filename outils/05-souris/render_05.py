"""Vidéo « 05 - La souris : le curseur et les clics » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_05.py script.json durations.json out.mp4
        python3 render_05.py --estimate script.json durations.json
Réutilise ../render_01.py (fond, barre des tâches, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes)
et ../01-ordinateur/render_01_ordinateur.py (pièce, étiquettes).
Libellés écrits tels quels (voir sources_05.md) : « Corbeille », « Photos » (nom de dossier fictif), « Bloc-notes ».
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur"):
    sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); BLEU = (0, 103, 192)

# ---------- bureau ----------
BIN = (44, 36, 124, 136)
DOS = (44, 168, 124, 268)          # dossier « Photos »
BLOC = (44, 300, 124, 400)         # programme « Bloc-notes »
CLOCK = (W - 150, H - R.TB_H + 4, W - 10, H - 4)

def bin_icon(d, x, y, s=1.0):
    d.rounded_rectangle([x, y + 6 * s, x + 56 * s, y + 14 * s], 3, fill=(225, 230, 240), outline=(120, 130, 150), width=2)
    d.rectangle([x + 20 * s, y, x + 36 * s, y + 7 * s], fill=(225, 230, 240), outline=(120, 130, 150), width=2)
    d.polygon([(x + 5 * s, y + 15 * s), (x + 51 * s, y + 15 * s), (x + 45 * s, y + 62 * s), (x + 11 * s, y + 62 * s)], fill=(235, 240, 248), outline=(120, 130, 150))
    for k in (17, 28, 39):
        d.line([x + k * s, y + 22 * s, x + (k + (28 - k) * 0.1) * s, y + 55 * s], fill=(150, 160, 180), width=max(2, int(3 * s)))

def note_icon(d, x, y, s=1.0):
    """Bloc-notes dessiné : feuille blanche à spirale bleue."""
    d.rounded_rectangle([x, y + 6 * s, x + 52 * s, y + 66 * s], 5, fill=(255, 255, 255), outline=(90, 110, 150), width=2)
    d.rectangle([x, y + 6 * s, x + 52 * s, y + 16 * s], fill=(70, 150, 230))
    for k in range(4):
        cx = x + 9 * s + k * 12 * s; d.ellipse([cx - 3 * s, y, cx + 3 * s, y + 12 * s], outline=(60, 60, 70), width=2)
    for k in range(4):
        d.line([x + 8 * s, y + 28 * s + k * 9 * s, x + 44 * s, y + 28 * s + k * 9 * s], fill=(150, 160, 180), width=2)

def draw_clock(d):
    d.text((CLOCK[0] + 34, CLOCK[1] + 3), "10:30", font=F(17, "s"), fill=(20, 20, 20))
    d.text((CLOCK[0] + 22, CLOCK[1] + 24), "27/11/2026", font=F(15), fill=(20, 20, 20))

def icon_label(d, r, txt):
    f = F(16, "s"); tw = d.textlength(txt, font=f)
    d.text(((r[0] + r[2]) / 2 - tw / 2, r[1] + 74), txt, font=f, fill=(255, 255, 255), stroke_width=2, stroke_fill=(20, 40, 90))

_BG = None
def desktop(sel=None):
    global _BG
    if _BG is None: _BG = R.bg()
    im = _BG.copy(); d = ImageDraw.Draw(im)
    for name, r in (("dos", DOS), ("bloc", BLOC), ("bin", BIN)):
        if sel == name:
            d.rounded_rectangle([r[0] - 8, r[1] - 4, r[2] + 8, r[3] + 2], 6, fill=(120, 170, 230), outline=(200, 225, 255), width=2)
    bin_icon(d, BIN[0] + 12, BIN[1] + 4); icon_label(d, BIN, "Corbeille")
    R.folder_icon(d, DOS[0] - 4, DOS[1] + 6, 0.9); icon_label(d, DOS, "Photos")
    note_icon(d, BLOC[0] + 14, BLOC[1] + 2); icon_label(d, BLOC, "Bloc-notes")
    R.draw_taskbar(d); draw_clock(d)
    return im

# ---------- fenêtres ----------
WIN = (250, 90, 1110, 600)
CLOSE = (WIN[2] - 54, WIN[1] + 2, WIN[2] - 4, WIN[1] + 42)

def window(kind, typed=""):
    im = desktop(); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = WIN
    d.rounded_rectangle([x0 + 6, y0 + 8, x1 + 6, y1 + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle(WIN, 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 44], 10, fill=(232, 236, 244)); d.rectangle([x0, y0 + 24, x1, y0 + 44], fill=(232, 236, 244))
    if kind == "photos":
        R.folder_icon(d, x0 + 14, y0 + 12, 0.25); d.text((x0 + 46, y0 + 11), "Photos", font=F(18, "s"), fill=(30, 30, 30))
        for i in range(6):
            col, row = i % 3, i // 3
            px, py = x0 + 60 + col * 260, y0 + 90 + row * 220
            d.rounded_rectangle([px, py, px + 220, py + 160], 8, fill=[(120, 190, 240), (250, 200, 120), (140, 210, 150)][col])
            d.polygon([(px + 20, py + 150), (px + 90, py + 60), (px + 150, py + 150)], fill=(70, 120, 90))
            d.polygon([(px + 100, py + 150), (px + 150, py + 90), (px + 205, py + 150)], fill=(90, 140, 100))
            d.ellipse([px + 160, py + 18, px + 196, py + 54], fill=(255, 230, 90))
            d.text((px + 60, py + 168), f"Photo {i + 1}", font=F(17), fill=(30, 30, 30))
    else:
        note_icon(d, x0 + 14, y0 + 8, 0.45); d.text((x0 + 46, y0 + 11), "Bloc-notes", font=F(18, "s"), fill=(30, 30, 30))
        d.rectangle([x0 + 2, y0 + 44, x1 - 2, y0 + 80], fill=(246, 248, 252))
        for i in range(3):
            d.rounded_rectangle([x0 + 20 + i * 90, y0 + 54, x0 + 90 + i * 90, y0 + 70], 4, fill=(215, 220, 230))
        d.text((x0 + 30, y0 + 100), typed, font=F(30), fill=(20, 20, 20))
        cx = x0 + 32 + d.textlength(typed, font=F(30)); d.line([cx, y0 + 102, cx, y0 + 138], fill=(20, 20, 20), width=2)
    for i, c in enumerate(("—", "☐")):
        d.text((x1 - 140 + i * 44, y0 + 10), c, font=F(19), fill=(60, 60, 60))
    cx, cy = R.center(CLOSE)
    d.line([cx - 9, cy - 9, cx + 9, cy + 9], fill=(40, 40, 40), width=3); d.line([cx - 9, cy + 9, cx + 9, cy - 9], fill=(40, 40, 40), width=3)
    return im

# ---------- souris dessinée en grand ----------
def big_mouse(d, cx, cy, s=1.0, press=None, hand=False):
    """Souris vue de dessus. press : 'L' pour le bouton gauche enfoncé."""
    w, h = 170 * s, 270 * s
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0 + 8, y0 + 12, x0 + w + 8, y0 + h + 12], int(80 * s), fill=(20, 30, 60))
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], int(80 * s), fill=(235, 238, 245), outline=(60, 60, 70), width=4)
    d.line([cx, y0 + 4, cx, y0 + 115 * s], fill=(60, 60, 70), width=4)
    d.line([x0 + 6, y0 + 115 * s, x0 + w - 6, y0 + 115 * s], fill=(60, 60, 70), width=4)
    if press == "L":
        d.pieslice([x0 + 4, y0 + 4, x0 + w - 4, y0 + 230 * s], 180, 270, fill=YEL)
        d.rectangle([x0 + 4, y0 + 80 * s, cx - 2, y0 + 113 * s], fill=YEL)
    d.rounded_rectangle([cx - 10 * s, y0 + 40 * s, cx + 10 * s, y0 + 80 * s], 8, fill=(90, 90, 100))
    if hand:
        skin, edge = (240, 200, 170), (150, 100, 80)
        d.rounded_rectangle([x0 + 18 * s, y0 - 40 * s, x0 + 70 * s, y0 + 105 * s], int(24 * s), fill=skin, outline=edge, width=3)
        d.rounded_rectangle([cx + 12 * s, y0 - 55 * s, cx + 64 * s, y0 + 105 * s], int(24 * s), fill=skin, outline=edge, width=3)
        d.rounded_rectangle([x0 - 10 * s, y0 + 95 * s, x0 + w + 10 * s, y0 + 320 * s], int(60 * s), fill=skin, outline=edge, width=3)

def clic_word(d, x, y, txt):
    d.text((x, y), txt, font=F(44, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))

def spinner(d, cx, cy, t, r=34):
    for k in range(10):
        a = t * 6 + k * 2 * math.pi / 10
        c = int(80 + 17 * k)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(c // 3, c // 2 + 40, 255))

# ---------- gestes animés ----------
def dbl_click(base_b, base_a, r, start, t, D, cap, show_loupe=True, double=True):
    """Curseur jusqu'à la cible ; clic (ou double-clic) à 60 % ; écran 'après' ensuite."""
    c = R.center(r); tc = 0.6 * D
    im = base_a() if t >= tc + 0.5 else base_b(t >= tc)
    clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.5:
        R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.12 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc:
        R.loupe(im, r, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos)
    R.ripple(d, c[0], c[1], (t - tc) / 0.4)
    if double:
        R.ripple(d, c[0], c[1], (t - tc - 0.25) / 0.4)
        if tc <= t < tc + 0.9: clic_word(d, c[0] + 40, c[1] - 70, "clic clic !")
    elif tc <= t < tc + 0.9:
        clic_word(d, c[0] - 160, c[1] + 30, "clic !")
    R.caption(d, cap); return im

def open_photos(start, t, D, cap, loupe=True):
    return dbl_click(lambda hit: desktop("dos" if hit else None), lambda: window("photos"), DOS, start, t, D, cap, loupe)

def close_win(kind, start, t, D, cap, typed="", loupe=True):
    return dbl_click(lambda hit: window(kind, typed), lambda: desktop(), CLOSE, start, t, D, cap, loupe, double=False)

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("La souris", ["le curseur et les clics", "Aide-mémoire n° 05 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); big_mouse(d, W / 2, 420, 0.5)
        return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im)
        # table + souris qui glisse ; écran avec curseur qui suit
        d.rounded_rectangle([90, 470, 560, 600], 16, fill=(180, 130, 90), outline=(120, 80, 50), width=4)
        dx = 120 * math.sin(t * 1.3)
        big_mouse(d, 325 + dx, 520, 0.35)
        sc = (680, 150, 1170, 430)
        d.rounded_rectangle([sc[0] - 14, sc[1] - 14, sc[2] + 14, sc[3] + 14], 12, fill=(30, 32, 40))
        mini = desktop().resize((sc[2] - sc[0], sc[3] - sc[1]), Image.LANCZOS); im.paste(mini, sc[:2]); d = ImageDraw.Draw(im)
        R.cursor(d, 900 + dx * 1.2, 270, 1.3)
        if p > 0.45:
            O.label(d, "le curseur", (925 + dx * 1.2, 230)); O.label(d, "la souris", (325, 440))
        R.caption(d, cap); return im
    if sid == "tenir":
        im = R.bg(); d = ImageDraw.Draw(im)
        big_mouse(d, W / 2, 400, 1.0, press="L" if p > 0.3 and p < 0.62 and (t % 0.7) < 0.47 else None, hand=p > 0.15)
        if p > 0.3: O.label(d, "index : bouton gauche", (W / 2 - 290, 210))
        if p > 0.62: O.label(d, "majeur : bouton droit", (W / 2 + 290, 210))
        R.caption(d, cap); return im
    if sid == "bouger":
        im = R.bg(); d = ImageDraw.Draw(im)
        d.rounded_rectangle([40, 230, 600, 640], 20, fill=(180, 130, 90), outline=(120, 80, 50), width=4)
        if p < 0.6:
            a = t * 1.1; mx, my = 320 + 170 * math.cos(a), 450 + 110 * math.sin(a); lift = 0
        else:  # au bord : on soulève et on repose
            q = (p - 0.6) / 0.4; mx = 480 - 300 * R.ease(q); my = 450; lift = 60 * math.sin(math.pi * min(1, q))
        d.ellipse([mx - 60, my + 70, mx + 60, my + 100], fill=(120, 80, 50))
        big_mouse(d, mx, my - lift, 0.45)
        sc = (680, 150, 1220, 450)
        d.rounded_rectangle([sc[0] - 14, sc[1] - 14, sc[2] + 14, sc[3] + 14], 12, fill=(30, 32, 40))
        mini = desktop().resize((sc[2] - sc[0], sc[3] - sc[1]), Image.LANCZOS); im.paste(mini, sc[:2]); d = ImageDraw.Draw(im)
        cxr = 950 + (mx - 320) * 1.2 if p < 0.6 else 950 + 160 * 1.2
        R.cursor(d, cxr, 300 + (my - 450) * 1.0 if p < 0.6 else 300, 1.3)
        if p > 0.6: O.label(d, "soulevez, puis reposez", (320, 190))
        R.caption(d, cap); return im
    if sid == "clic":
        sel = p > 0.55
        im = desktop("dos" if sel else None); d = ImageDraw.Draw(im)
        pos = R.move(t, 0.1 * D, 0.45 * D, (600, 400), (R.center(DOS)[0] - 4, R.center(DOS)[1] - 4))
        big_mouse(d, 900, 360, 0.7, press="L" if 0.5 < p < 0.56 else None)
        if 0.5 < p < 0.65: clic_word(d, 1010, 180, "clic !")
        if sel: R.highlight(d, DOS, t); O.label(d, "choisie : en bleu", (330, 220))
        R.cursor(d, *pos); R.caption(d, cap); return im
    if sid == "double":
        im = desktop(); d = ImageDraw.Draw(im)
        q = (t % 2.2) / 2.2
        pr = "L" if (0.3 < q < 0.38 or 0.48 < q < 0.56) else None
        big_mouse(d, W / 2, 380, 0.9, press=pr)
        if q > 0.3: clic_word(d, W / 2 + 120, 200, "clic" if q < 0.48 else "clic clic !")
        O.label(d, "2 fois, très vite, sans bouger", (W / 2, 610))
        R.caption(d, cap); return im
    if sid == "ouvrir":
        if p < 0.75: return open_photos((640, 420), t, 0.75 * D, cap)
        im = window("photos"); d = ImageDraw.Draw(im); O.label(d, "une fenêtre s'ouvre", (680, 650)); R.caption(d, cap); return im
    if sid == "fermer":
        if p < 0.8: return close_win("photos", (700, 400), t, 0.8 * D, cap)
        im = desktop(); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et entraînez-vous :", "un clic, un double-clic."], "Relancez la vidéo quand vous êtes prêt.", None)
    if sid == "programme":
        if p < 0.55:
            return dbl_click(lambda hit: desktop("bloc" if hit else None), lambda: window("bloc"), BLOC, (640, 420), t, 0.55 * D, cap)
        txt = "Bonjour !"[:max(0, int((p - 0.62) / 0.3 * 9))]
        im = window("bloc", txt); d = ImageDraw.Draw(im); O.label(d, "on peut y écrire", (680, 450)); R.caption(d, cap); return im
    if sid == "quitter":
        if p < 0.8: return close_win("bloc", (700, 400), t, 0.8 * D, cap, typed="Bonjour !")
        im = desktop(); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "panique":
        im = desktop(); d = ImageDraw.Draw(im)
        d.rounded_rectangle([230, 130, 1050, 520], 24, fill=(255, 255, 255), outline=(255, 122, 89), width=8)
        d.text((290, 160), "Pas de panique !", font=F(44, "b"), fill=(255, 122, 89))
        d.text((290, 250), "Rien ne s'ouvre ?", font=F(32, "s"), fill=INK)
        d.text((290, 295), "Recommencez, un peu plus vite.", font=F(30), fill=INK)
        if p > 0.5:
            d.text((390, 390), "Un cercle tourne ? Patientez.", font=F(30, "s"), fill=INK)
            spinner(d, 330, 410, t)
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Double-cliquez sur « Photos » :", "la fenêtre s'ouvre.", "Cliquez sur la croix :", "elle se ferme."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Ouvrez le dossier « Photos »,", "puis fermez-le."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        if p < 0.5: return open_photos((640, 420), t, 0.5 * D, cap, loupe=False)
        return close_win("photos", (700, 400), t - 0.5 * D, 0.5 * D, cap, loupe=False)
    if sid == "resume":
        return R.card("À retenir", ["Un clic : pour choisir", "Un double-clic : pour ouvrir", "La croix : pour fermer", "Toujours le bouton gauche"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
