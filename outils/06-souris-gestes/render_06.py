"""Vidéo « 06 - La souris : déplacer, agrandir, menu du clic droit, molette » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_06.py script.json durations.json out.mp4
        python3 render_06.py --estimate script.json durations.json
Réutilise ../render_01.py (fond, barre des tâches, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes).
Choix d'écriture (voir sources_06.md) : les trois boutons sont désignés par leur forme (trait, carré, croix) ;
le menu du clic droit est dessiné sans texte (ses libellés changent selon l'endroit et la version).
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, ".."))
import render_01 as R
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
TB = R.TB_H
INK = (40, 40, 50); VIO = (147, 17, 126); ORANGE = (255, 120, 0)
lerp, ease, move, center = R.lerp, R.ease, R.move, R.center

# ---------- bureau ----------
ICON0 = (70, 200)          # position de départ de l'icône « Ma lettre »
ICON1 = (560, 300)         # position d'arrivée
def doc_icon(d, x, y, s=1.0, name="Ma lettre", sel=False):
    w, h = 54 * s, 70 * s
    if sel: d.rounded_rectangle([x - 22, y - 8, x + w + 22, y + h + 36], 8, fill=(120, 160, 230), outline=(200, 220, 255), width=2)
    d.polygon([(x, y), (x + w - 16 * s, y), (x + w, y + 16 * s), (x + w, y + h), (x, y + h)], fill=(255, 255, 255), outline=(110, 120, 140))
    for k in range(4): d.line([x + 9 * s, y + (28 + k * 10) * s, x + w - 9 * s, y + (28 + k * 10) * s], fill=(0, 103, 192), width=3)
    if name:
        tw = d.textlength(name, font=F(16, "s")); d.text((x + w / 2 - tw / 2, y + h + 6), name, font=F(16, "s"), fill=(255, 255, 255), stroke_width=2, stroke_fill=(20, 30, 60))
def icon_rect(pos): return (pos[0] - 14, pos[1] - 6, pos[0] + 68, pos[1] + 98)

def desktop(icon=ICON0, sel=False, ghost=None):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if ghost: doc_icon(d, *ghost, name=None)
    doc_icon(d, *icon, sel=sel)
    return im, d

# ---------- fenêtre « Ma lettre » ----------
WIN0 = (330, 130, 930, 520)
WIN1 = (420, 170, 1020, 560)
WMAX = (0, 0, W, H - TB)
def btn_rects(r):
    x1, y0 = r[2], r[1]
    return {"trait": (x1 - 138, y0 + 2, x1 - 94, y0 + 40), "carre": (x1 - 92, y0 + 2, x1 - 48, y0 + 40), "croix": (x1 - 46, y0 + 2, x1 - 2, y0 + 40)}
LIGNES = 40
def draw_win(d, r, scroll=0.0, hover=None, maxed=False):
    x0, y0, x1, y1 = [int(v) for v in r]
    d.rounded_rectangle([x0 + 6, y0 + 8, x1 + 6, y1 + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([x0, y0, x1, y1], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 42], 10, fill=(232, 236, 244)); d.rectangle([x0, y0 + 22, x1, y0 + 42], fill=(232, 236, 244))
    doc_icon(d, x0 + 14, y0 + 9, 0.32, name=None)
    d.text((x0 + 42, y0 + 10), "Ma lettre", font=F(18, "s"), fill=(30, 30, 30))
    b = btn_rects(r)
    for k, rr in b.items():
        if hover == k: d.rectangle(rr, fill=(232, 17, 35) if k == "croix" else (205, 210, 222))
        cx, cy = center(rr); col = (255, 255, 255) if hover == "croix" and k == "croix" else (40, 40, 50)
        if k == "trait": d.line([cx - 9, cy, cx + 9, cy], fill=col, width=2)
        elif k == "carre":
            if maxed:
                d.rectangle([cx - 6, cy - 9, cx + 9, cy + 6], outline=col, width=2); d.rectangle([cx - 9, cy - 6, cx + 6, cy + 9], fill=(232, 236, 244) if hover != k else (205, 210, 222), outline=col, width=2)
            else: d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], outline=col, width=2)
        else:
            d.line([cx - 8, cy - 8, cx + 8, cy + 8], fill=col, width=2); d.line([cx - 8, cy + 8, cx + 8, cy - 8], fill=col, width=2)
    # texte de la lettre (lignes grises), avec défilement
    top, bot = y0 + 56, y1 - 12
    lh = 30; off = scroll * (LIGNES * lh - (bot - top))
    for k in range(LIGNES):
        y = top + k * lh - off
        if top - 4 <= y <= bot - 14:
            if k % 8 == 0:
                d.text((x0 + 30, y - 4), f"Paragraphe {k // 8 + 1}", font=F(18, "b"), fill=VIO)
            else:
                wl = (x1 - x0 - 90) * (0.55 + 0.4 * ((k * 37) % 10) / 10)
                d.rounded_rectangle([x0 + 30, y + 4, x0 + 30 + wl, y + 14], 4, fill=(190, 196, 208))
    # barre de défilement
    d.rounded_rectangle([x1 - 14, top, x1 - 6, bot], 4, fill=(232, 234, 240))
    hh = (bot - top) * 0.25; yy = top + (bot - top - hh) * scroll
    d.rounded_rectangle([x1 - 14, yy, x1 - 6, yy + hh], 4, fill=(140, 145, 160))

def win_screen(r, **kw):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im); draw_win(d, r, **kw); return im, d

# ---------- souris en grand ----------
def big_mouse(d, cx, cy, s=1.0, hl=None, t=0.0, roll=0):
    w, h = 150 * s, 230 * s
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0 + 6, y0 + 8, x0 + w + 6, y0 + h + 8], int(70 * s), fill=(20, 30, 60))
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], int(70 * s), fill=(245, 246, 250), outline=(60, 60, 70), width=4)
    d.line([cx, y0, cx, y0 + 95 * s], fill=(60, 60, 70), width=3); d.line([x0 + 8, y0 + 95 * s, x0 + w - 8, y0 + 95 * s], fill=(60, 60, 70), width=3)
    blink = (t % 0.7) < 0.47
    if hl == "gauche" and blink: d.rounded_rectangle([x0 + 10, y0 + 10, cx - 6, y0 + 88 * s], int(30 * s), fill=YEL)
    if hl == "droit" and blink: d.rounded_rectangle([cx + 6, y0 + 10, x0 + w - 10, y0 + 88 * s], int(30 * s), fill=ORANGE)
    wr = (cx - 13 * s, y0 + 22 * s, cx + 13 * s, y0 + 78 * s)
    d.rounded_rectangle(wr, int(12 * s), fill=YEL if hl == "molette" and blink else (90, 95, 110), outline=(30, 30, 40), width=2)
    for k in range(4):
        yy = wr[1] + ((k * 14 * s + roll * 6) % (56 * s))
        d.line([wr[0] + 4, yy, wr[2] - 4, yy], fill=(30, 30, 40), width=2)

def inset(d, hl, t, txt):
    """Petite souris en haut à droite, bouton concerné en couleur."""
    d.rounded_rectangle([W - 250, 96, W - 20, 330], 18, fill=(255, 255, 255), outline=YEL, width=5)
    big_mouse(d, W - 135, 195, 0.62, hl, t)
    tw = d.textlength(txt, font=F(20, "b")); d.text((W - 135 - tw / 2, 290), txt, font=F(20, "b"), fill=INK)

def tag(d, text, at, col=YEL):
    f = F(30, "b"); tw = d.textlength(text, font=f)
    x = min(max(at[0] - tw / 2, 20), W - tw - 20)
    d.text((x, at[1]), text, font=f, fill=col, stroke_width=4, stroke_fill=(0, 0, 0))

def dbl_arrow(d, x, y):
    for col, wd in (((255, 255, 255), 9), ((0, 0, 0), 4)):
        d.line([x - 20, y - 20, x + 20, y + 20], fill=col, width=wd)
        for (px, py, sx) in ((x - 20, y - 20, 1), (x + 20, y + 20, -1)):
            d.polygon([(px, py), (px + 16 * sx, py + 2 * sx), (px + 2 * sx, py + 16 * sx)], fill=col)

# ---------- menu du clic droit (sans texte) ----------
MENU_AT = (640, 230)
def ctx_menu(d, at=MENU_AT):
    x, y = at
    d.rounded_rectangle([x + 5, y + 7, x + 265, y + 277], 10, fill=(20, 30, 60))
    d.rounded_rectangle([x, y, x + 260, y + 270], 10, fill=(250, 250, 252), outline=(170, 175, 190), width=2)
    for i in range(6):
        yy = y + 22 + i * 42
        d.rounded_rectangle([x + 18, yy, x + 40, yy + 22], 5, fill=(200, 206, 220))
        d.rounded_rectangle([x + 56, yy + 5, x + 56 + (150 - (i * 23) % 60), yy + 17], 5, fill=(150, 156, 172))

# ---------- scènes ----------
def s_drag_icon(t, D, cap, show_inset=True, label=True):
    p = t / D; t_press, t_rel = 0.32 * D, 0.78 * D
    if t < t_press:
        pos_i = ICON0; cur = move(t, 0.05 * D, 0.27 * D, (W / 2, H / 2), (ICON0[0] + 30, ICON0[1] + 35))
    else:
        k = ease((t - t_press - 0.08 * D) / (t_rel - t_press - 0.12 * D))
        pos_i = (lerp(ICON0[0], ICON1[0], k), lerp(ICON0[1], ICON1[1], k)); cur = (pos_i[0] + 30, pos_i[1] + 35)
    holding = t_press <= t < t_rel
    im, d = desktop(pos_i, sel=t >= t_press, ghost=ICON0 if holding else None)
    if t < t_press:
        R.highlight(d, icon_rect(ICON0), t); R.arrow(d, icon_rect(ICON0), t)
    R.cursor(d, *cur)
    if t_press <= t < t_press + 0.6: R.ripple(d, *cur, (t - t_press) / 0.6)
    if label:
        if holding: tag(d, "bouton gauche ENFONCÉ", (cur[0] + 40, cur[1] + 70))
        elif t >= t_rel: tag(d, "je relâche", (cur[0] + 40, cur[1] + 70), (43, 179, 163))
    if show_inset and holding: inset(d, "gauche", t, "gardez enfoncé")
    R.caption(d, cap); return im

def s_move_win(t, D, cap):
    t_press, t_rel = 0.35 * D, 0.8 * D; bar = (WIN0[0] + 120, WIN0[1] + 21)
    if t < t_press:
        r = WIN0; cur = move(t, 0.05 * D, 0.3 * D, (W / 2, H - 120), bar)
    else:
        k = ease((t - t_press - 0.05 * D) / (t_rel - t_press - 0.1 * D))
        r = tuple(lerp(a, b, k) for a, b in zip(WIN0, WIN1)); cur = (bar[0] + r[0] - WIN0[0], bar[1] + r[1] - WIN0[1])
    im, d = win_screen(r)
    if t < t_press:
        zone = (r[0] + 2, r[1] + 2, r[2] - 145, r[1] + 40); R.highlight(d, zone, t)
        tag(d, "la barre du haut", (center(zone)[0], r[1] - 52))
    R.cursor(d, *cur)
    if t_press <= t < t_press + 0.6: R.ripple(d, *cur, (t - t_press) / 0.6)
    if t_press <= t < t_rel: inset(d, "gauche", t, "gardez enfoncé")
    R.caption(d, cap); return im

def s_agrandir(t, D, cap, loupe=True):
    c1, c2 = 0.42 * D, 0.82 * D
    maxed = c1 + 0.3 <= t < c2 + 0.3
    r = WMAX if maxed else WIN0
    b = btn_rects(r)["carre"]; cb = center(b)
    if t < c1: cur = move(t, 0.12 * D, 0.32 * D, (W / 2, H / 2 + 60), cb)
    else: cur = cb
    im, d = win_screen(r, maxed=maxed, hover="carre" if abs(cur[0] - cb[0]) < 3 else None); clean = im.copy()
    if t < c1 + 0.3:
        R.highlight(d, b, t); R.arrow(d, b, t)
        if loupe and 0.18 * D < t: R.loupe(im, btn_rects(r)["carre"], place=(700, 420), clean=clean); d = ImageDraw.Draw(im)
    elif maxed and t < c2 - 0.1 * D:
        tag(d, "tout l'écran !", (W / 2, H / 2 - 20))
    elif maxed:
        R.highlight(d, b, t)
    R.cursor(d, *cur)
    R.ripple(d, *cb, (t - c1) / 0.6); R.ripple(d, *cb, (t - c2) / 0.6)
    R.caption(d, cap); return im

def s_coin(t, D, cap):
    t_press, t_rel = 0.42 * D, 0.82 * D
    big = (WIN0[0], WIN0[1], WIN0[2] + 180, WIN0[3] + 70)
    k = ease((t - t_press - 0.05 * D) / (t_rel - t_press - 0.1 * D)) if t >= t_press else 0
    r = tuple(lerp(a, b, k) for a, b in zip(WIN0, big))
    corner = (r[2], r[3])
    im, d = win_screen(r); clean = im.copy()
    near = t >= 0.3 * D
    cur = move(t, 0.05 * D, 0.3 * D, (W / 2 - 100, H / 2), corner) if t < t_press else corner
    if t < t_press:
        zone = (corner[0] - 26, corner[1] - 26, corner[0] + 26, corner[1] + 26); R.highlight(d, zone, t)
        if 0.15 * D < t: R.loupe(im, zone, place=(200, 330), clean=clean); d = ImageDraw.Draw(im)
    if near: dbl_arrow(d, *cur)
    else: R.cursor(d, *cur)
    if near and t < t_press: tag(d, "double flèche", (cur[0] - 40, cur[1] + 34))
    if t_press <= t < t_rel: inset(d, "gauche", t, "gardez enfoncé")
    R.caption(d, cap); return im

def s_clicdroit(t, D, cap, menu_until=None, inset_on=True):
    t_c = 0.35 * D; spot = (MENU_AT[0] - 6, MENU_AT[1] - 6)
    cur = move(t, 0.05 * D, 0.3 * D, (W / 2 - 300, H / 2 + 120), spot) if t < t_c else spot
    im, d = desktop()
    if t >= t_c + 0.2: ctx_menu(d)
    if t < t_c:
        zone = (spot[0] - 30, spot[1] - 30, spot[0] + 30, spot[1] + 30); R.highlight(d, zone, t)
    R.cursor(d, *cur)
    R.ripple(d, *spot, (t - t_c) / 0.6, ORANGE)
    if t_c - 0.4 < t < t_c + 1.2: tag(d, "clic DROIT", (spot[0] - 120, spot[1] + 40), ORANGE)
    if inset_on: inset(d, "droit", t, "bouton droit")
    if t > t_c + 0.8 * 1 and t > 0.55 * D:
        R.highlight(d, (MENU_AT[0], MENU_AT[1], MENU_AT[0] + 260, MENU_AT[1] + 270), t)
        tag(d, "le menu", (MENU_AT[0] + 130, MENU_AT[1] + 285))
    R.caption(d, cap); return im

def s_fermer(t, D, cap):
    t_c = 0.5 * D; start = (MENU_AT[0] - 6, MENU_AT[1] - 6); beside = (330, 430)
    cur = move(t, 0.1 * D, 0.42 * D, start, beside) if t < t_c else beside
    im, d = desktop()
    if t < t_c + 0.3: ctx_menu(d)
    if t < t_c:
        zone = (beside[0] - 40, beside[1] - 40, beside[0] + 40, beside[1] + 40); R.highlight(d, zone, t); R.arrow(d, zone, t)
        tag(d, "à côté", (beside[0], beside[1] + 50))
    R.cursor(d, *cur); R.ripple(d, *beside, (t - t_c) / 0.6)
    if t > t_c + 0.5: tag(d, "menu fermé", (W / 2 + 60, 300), (43, 179, 163))
    R.caption(d, cap); return im

def s_molette(t, D, cap):
    p = t / D
    # 0.25-0.55 : vers soi (descend) ; 0.65-0.92 : vers l'écran (remonte)
    if p < 0.25: sc, dirn = 0.0, 0
    elif p < 0.55: sc, dirn = ease((p - 0.25) / 0.3), 1
    elif p < 0.65: sc, dirn = 1.0, 0
    else: sc, dirn = 1 - ease((p - 0.65) / 0.27), -1
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    draw_win(d, (470, 110, 1200, 600), scroll=sc)
    d.rounded_rectangle([60, 120, 410, 600], 22, fill=(255, 255, 255), outline=YEL, width=6)
    big_mouse(d, 235, 330, 1.0, "molette", t, roll=int(t * 12) * (dirn or 0))
    if dirn == 1:
        tag(d, "vers vous", (235, 470)); d.text((225, 505), "↓", font=F(60, "b"), fill=VIO)
        tag(d, "la page descend", (835, 80), YEL)
    elif dirn == -1:
        tag(d, "vers l'écran", (235, 470)); d.text((225, 505), "↑", font=F(60, "b"), fill=VIO)
        tag(d, "la page remonte", (835, 80), YEL)
    R.caption(d, cap); return im

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("La souris : déplacer, agrandir,", ["clic droit et molette", "Aide-mémoire n° 06 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); big_mouse(d, W / 2, 420, 0.75); return im
    if sid == "intro":
        im = R.screen({"window": False}); d = ImageDraw.Draw(im)
        big_mouse(d, W / 2, 330, 1.2, ["gauche", "gauche", "droit", "molette"][min(3, int(p * 4))], t)
        for i, (txt, at) in enumerate((("déplacer", (300, 200)), ("changer la taille", (300, 420)), ("un petit menu", (990, 200)), ("faire défiler", (990, 420)))):
            if p > 0.12 + i * 0.15: tag(d, txt, at)
        R.caption(d, cap); return im
    if sid == "glisser":
        im = R.bg(); d = ImageDraw.Draw(im)
        d.rounded_rectangle([120, 330, 1160, 380], 12, fill=(176, 120, 70), outline=(140, 90, 50), width=4)
        d.rectangle([170, 380, 200, 600], fill=(140, 90, 50)); d.rectangle([1080, 380, 1110, 600], fill=(140, 90, 50))
        k = ease((p - 0.35) / 0.4); x = lerp(260, 900, k); lift = 60 * math.sin(math.pi * max(0, min(1, (p - 0.35) / 0.4)))
        doc_icon(d, x, 250 - lift, 1.1, name=None)
        if p > 0.2: tag(d, "je prends", (300, 140))
        if p > 0.45: tag(d, "je porte", (W / 2, 140))
        if p > 0.78: tag(d, "je pose", (960, 140), (43, 179, 163))
        R.caption(d, cap); return im
    if sid == "deplacer": return s_drag_icon(t, D, cap)
    if sid == "fenetre": return s_move_win(t, D, cap)
    if sid == "agrandir": return s_agrandir(t, D, cap)
    if sid == "coin": return s_coin(t, D, cap)
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "clicdroit": return s_clicdroit(t, D, cap)
    if sid == "fermer": return s_fermer(t, D, cap)
    if sid == "molette": return s_molette(t, D, cap)
    if sid == "exercice":
        return R.card("Exercice", ["1. Déplacez une icône.", "2. Agrandissez une fenêtre.", "3. Ouvrez le menu du clic droit,", "puis fermez-le."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Faites l'exercice", "sur votre ordinateur."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        if p < 0.36: return s_drag_icon(t, 0.36 * D, cap, show_inset=False)
        if p < 0.62: return s_agrandir(t - 0.36 * D, 0.26 * D, cap, loupe=False)
        if p < 0.82: return s_clicdroit(t - 0.62 * D, 0.2 * D, cap, inset_on=False)
        return s_fermer(t - 0.82 * D, 0.18 * D, cap)
    if sid == "resume":
        return R.card("À retenir", ["Gauche enfoncé : je déplace", "Le carré : j'agrandis", "Clic droit : un menu", "La molette : je fais défiler"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
