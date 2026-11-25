"""Vidéo « 01 - Découvrir l'ordinateur : fixe et portable » (appareils dessinés, sans voix, sous-titrée).
Usage : python3 render_01_ordinateur.py script.json durations.json out.mp4
Réutilise les surcouches de ../render_01.py (curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes).
"""
import json, math, os, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import render_01 as R
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
DESK_Y = 470
INK = (40, 40, 50)

# ---------- décor ----------
_room = None
def room():
    global _room
    if _room is None:
        im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
        for y in range(H):
            t = y / H
            d.line([(0, y), (W, y)], fill=(int(236 - 20 * t), int(228 - 22 * t), int(240 - 14 * t)))
        d.rectangle([0, DESK_Y, W, H], fill=(196, 150, 104))
        d.rectangle([0, DESK_Y, W, DESK_Y + 10], fill=(170, 124, 82))
        for i in range(6):
            y = DESK_Y + 40 + i * 40
            d.line([(0, y), (W, y + 6)], fill=(186, 140, 96), width=2)
        _room = im
    return _room.copy()

def wallpaper(d, r):
    x0, y0, x1, y1 = r
    for y in range(int(y0), int(y1)):
        t = (y - y0) / max(1, y1 - y0)
        d.line([(x0, y), (x1, y)], fill=(int(40 + 60 * t), int(90 + 60 * t), int(170 + 50 * t)))
    # petites icônes de bureau
    for i in range(3):
        d.rounded_rectangle([x0 + 14, y0 + 14 + i * 34, x0 + 38, y0 + 36 + i * 34], 4, fill=(250, 210, 90))
    d.rectangle([x0, y1 - 16, x1, y1], fill=(230, 232, 238))

# ---------- appareils ----------
MON = (330, 130, 730, 380)       # écran du fixe (dalle)
TOWER = (840, 160, 990, 468)
KEYB = (330, 486, 730, 548)
MOUSE = (790, 492, 836, 552)

def draw_monitor(d, r=MON, aio=False):
    x0, y0, x1, y1 = r
    cx = (x0 + x1) / 2
    d.rounded_rectangle([cx - 22, y1, cx + 22, DESK_Y + 6], 4, fill=(70, 72, 82))
    d.rounded_rectangle([cx - 90, DESK_Y - 4, cx + 90, DESK_Y + 12], 6, fill=(60, 62, 72))
    pad = 14 if not aio else 16
    d.rounded_rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + (pad if not aio else 46)], 14, fill=(30, 32, 40))
    if aio:
        d.ellipse([cx - 5, y1 + 22, cx + 5, y1 + 32], fill=(90, 92, 102))
    wallpaper(d, r)

def draw_tower(d, r=TOWER):
    x0, y0, x1, y1 = r
    d.rounded_rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 4], 12, fill=(120, 90, 60))
    d.rounded_rectangle(r, 12, fill=(52, 54, 64), outline=(30, 30, 36), width=3)
    d.rounded_rectangle([x0 + 14, y0 + 16, x1 - 14, y0 + 30], 4, fill=(80, 82, 92))
    pb = power_button_rect(r)
    d.ellipse(pb, fill=(80, 82, 92), outline=(200, 200, 210), width=3)
    c = R.center(pb); d.arc([c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9], 300, 240, fill=(230, 230, 240), width=3)
    d.line([c[0], c[1] - 12, c[0], c[1] - 1], fill=(230, 230, 240), width=3)
    for i in range(2):
        d.rectangle([x0 + 28 + i * 34, y0 + 110, x0 + 52 + i * 34, y0 + 120], fill=(20, 20, 24))
    for i in range(10):
        d.line([x0 + 20, y0 + 150 + i * 14, x1 - 20, y0 + 150 + i * 14], fill=(64, 66, 76), width=4)

def power_button_rect(r=TOWER):
    cx = (r[0] + r[2]) / 2; return (cx - 18, r[1] + 50, cx + 18, r[1] + 86)

def draw_keyboard(d, r=KEYB):
    x0, y0, x1, y1 = r
    d.polygon([(x0 + 14, y0), (x1 - 14, y0), (x1, y1), (x0, y1)], fill=(235, 236, 240), outline=(120, 120, 130))
    rows = 4
    for j in range(rows):
        yy = y0 + 6 + j * ((y1 - y0 - 10) / rows)
        inset = 14 * (1 - j / rows)
        n = 14
        ww = (x1 - x0 - 2 * inset - 20) / n
        for i in range(n):
            xx = x0 + inset + 10 + i * ww
            d.rounded_rectangle([xx + 1, yy, xx + ww - 2, yy + (y1 - y0 - 10) / rows - 3], 2, fill=(255, 255, 255), outline=(170, 170, 180))
    # barre d'espace
    d.rounded_rectangle([x0 + 130, y1 - 12, x1 - 130, y1 - 4], 2, fill=(255, 255, 255), outline=(170, 170, 180))

def draw_mouse(d, r=MOUSE, cable_to=None):
    x0, y0, x1, y1 = r
    if cable_to:
        d.line([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y0 - 12), cable_to], fill=(60, 60, 70), width=3)
    d.ellipse(r, fill=(245, 245, 248), outline=(90, 90, 100), width=3)
    d.line([(x0 + x1) / 2, y0 + 2, (x0 + x1) / 2, y0 + (y1 - y0) * 0.42], fill=(90, 90, 100), width=2)
    d.line([x0 + 4, y0 + (y1 - y0) * 0.42, x1 - 4, y0 + (y1 - y0) * 0.42], fill=(90, 90, 100), width=2)

def draw_fixe(d, cables=True):
    if cables:
        d.line([(R.center(KEYB)[0] + 150, KEYB[1]), (820, 476), (TOWER[0] + 10, TOWER[3] - 20)], fill=(60, 60, 70), width=3)
        d.line([(MON[2] + 14, MON[3] - 20), (TOWER[0], MON[3] - 20)], fill=(60, 60, 70), width=4)
    draw_monitor(d)
    draw_tower(d)
    draw_keyboard(d)
    draw_mouse(d, cable_to=(TOWER[0] + 10, TOWER[3] - 10) if cables else None)

# portable (vu de face, ouvert)
LAP_SCR = (450, 110, 830, 340)
LAP_BASE = [(400, 368), (880, 368), (930, 470), (350, 470)]
PAD = (575, 428, 705, 462)
def draw_laptop(d, closed_p=0.0):
    x0, y0, x1, y1 = LAP_SCR
    d.polygon([(340, 470), (940, 470), (930, 482), (350, 482)], fill=(110, 112, 122))
    d.polygon(LAP_BASE, fill=(190, 192, 200), outline=(110, 112, 122))
    # touches
    for j in range(4):
        yy = 376 + j * 12
        inset = 60 - j * 8
        n = 16; ww = (480 - 2 * inset + j * 22) / n
        xs = 400 + inset - j * 11
        for i in range(n):
            xx = xs + i * ww
            d.rounded_rectangle([xx + 1, yy, xx + ww - 2, yy + 9], 2, fill=(40, 42, 50))
    d.rounded_rectangle(PAD, 6, fill=(170, 172, 182), outline=(120, 122, 132), width=2)
    # écran
    d.rounded_rectangle([x0 - 16, y0 - 18, x1 + 16, 368], 12, fill=(30, 32, 40))
    d.ellipse([(x0 + x1) / 2 - 4, y0 - 12, (x0 + x1) / 2 + 4, y0 - 4], fill=(90, 92, 102))
    wallpaper(d, LAP_SCR)

def draw_charger(d, plug_at):
    bx, by = 1010, 520
    d.rounded_rectangle([bx, by, bx + 90, by + 46], 8, fill=(40, 42, 50))
    d.line([(bx, by + 23), (plug_at[0] + 30, by + 23), (plug_at[0] + 8, plug_at[1])], fill=(40, 42, 50), width=5)
    d.line([(bx + 90, by + 23), (1180, by + 23), (1190, 440)], fill=(40, 42, 50), width=5)
    # prise murale
    d.rounded_rectangle([1160, 380, 1220, 440], 10, fill=(250, 250, 250), outline=(150, 150, 150), width=2)
    d.ellipse([1176, 396, 1184, 404], fill=(60, 60, 60)); d.ellipse([1196, 396, 1204, 404], fill=(60, 60, 60))

def label(d, text, at, anchor="c"):
    f = F(26, "b"); tw = d.textlength(text, font=f)
    x, y = at
    if anchor == "c": x -= tw / 2
    elif anchor == "r": x -= tw
    d.rounded_rectangle([x - 12, y - 6, x + tw + 12, y + 36], 10, fill=(147, 17, 126))
    d.text((x, y), text, font=f, fill=(255, 255, 255))

def battery(d, x, y, level):
    d.rounded_rectangle([x, y, x + 120, y + 56], 10, outline=INK, width=5, fill=(255, 255, 255))
    d.rectangle([x + 120, y + 18, x + 132, y + 38], fill=INK)
    col = (230, 70, 60) if level < 0.25 else (43, 179, 163)
    d.rectangle([x + 9, y + 9, x + 9 + 102 * level, y + 47], fill=col)

# ---------- prises (vue de dos de l'unité centrale) ----------
BACK = (300, 100, 980, 540)
PORTS = {
    "alim": (360, 150, 500, 250),
    "hdmi": (560, 280, 700, 330),
    "usb1": (560, 380, 640, 412), "usb2": (660, 380, 740, 412),
    "usb3": (560, 432, 640, 464), "usb4": (660, 432, 740, 464),
    "jack": (800, 300, 840, 340),
}
def draw_back(d):
    x0, y0, x1, y1 = BACK
    d.rounded_rectangle(BACK, 16, fill=(70, 72, 82), outline=(30, 30, 36), width=4)
    d.text((x0 + 20, y0 + 10), "arrière de l'unité centrale", font=F(20, "s"), fill=(220, 220, 230))
    a = PORTS["alim"]
    d.rounded_rectangle([a[0] - 20, a[1] - 20, a[2] + 20, a[3] + 60], 10, fill=(40, 42, 50))
    d.polygon([(a[0], a[1]), (a[2], a[1]), (a[2], a[3] - 25), (a[2] - 25, a[3]), (a[0] + 25, a[3]), (a[0], a[3] - 25)], fill=(20, 20, 24), outline=(150, 150, 160))
    for i in range(3):
        d.rectangle([a[0] + 30 + i * 32, a[1] + 40, a[0] + 42 + i * 32, a[1] + 66], fill=(200, 200, 210))
    for i in range(4):
        d.line([a[0] - 10, a[3] + 18 + i * 9, a[2] + 10, a[3] + 18 + i * 9], fill=(70, 72, 82), width=3)
    h = PORTS["hdmi"]
    d.polygon([(h[0], h[1]), (h[2], h[1]), (h[2], h[1] + 30), (h[2] - 14, h[3]), (h[0] + 14, h[3]), (h[0], h[1] + 30)], fill=(20, 20, 24), outline=(190, 190, 200))
    for k in ("usb1", "usb2", "usb3", "usb4"):
        u = PORTS[k]
        d.rectangle(u, fill=(20, 20, 24), outline=(190, 190, 200), width=2)
        d.rectangle([u[0] + 8, u[1] + 6, u[2] - 8, u[1] + 14], fill=(40, 110, 220) if k in ("usb1", "usb2") else (230, 230, 235))
    j = PORTS["jack"]
    d.ellipse([j[0] - 8, j[1] - 8, j[2] + 8, j[3] + 8], fill=(60, 170, 90))
    d.ellipse([j[0] + 8, j[1] + 8, j[2] - 8, j[3] - 8], fill=(20, 20, 24))
    j2 = (j[0], j[1] + 70, j[2], j[3] + 70)
    d.ellipse([j2[0] - 8, j2[1] - 8, j2[2] + 8, j2[3] + 8], fill=(230, 120, 170))
    d.ellipse([j2[0] + 8, j2[1] + 8, j2[2] - 8, j2[3] - 8], fill=(20, 20, 24))
    for i in range(6):
        d.line([880, 150 + i * 30, 950, 150 + i * 30], fill=(50, 52, 60), width=8)

def usb_all():
    xs = [PORTS[k] for k in ("usb1", "usb2", "usb3", "usb4")]
    return (min(r[0] for r in xs), min(r[1] for r in xs), max(r[2] for r in xs), max(r[3] for r in xs))

# ---------- côté du portable ----------
SIDE = (180, 250, 1100, 420)
SIDE_PORTS = {"charge": (260, 315, 300, 345), "usbc": (350, 318, 400, 340), "usb": (450, 314, 530, 346), "hdmi2": (580, 312, 690, 348), "jack2": (1000, 316, 1030, 346)}
def draw_side(d):
    x0, y0, x1, y1 = SIDE
    d.rounded_rectangle([x0, y0 + 30, x1, y1], 18, fill=(190, 192, 200), outline=(110, 112, 122), width=3)
    d.rounded_rectangle([x0 + 10, y0, x1 - 10, y0 + 36], 12, fill=(60, 62, 72))
    d.text((x0 + 24, y1 + 14), "côté du portable (vu de profil)", font=F(20, "s"), fill=INK)
    c = SIDE_PORTS["charge"]; d.ellipse(c, fill=(20, 20, 24), outline=(120, 120, 130), width=2); d.ellipse([c[0] + 14, c[1] + 14, c[2] - 14, c[3] - 14], fill=(200, 200, 210))
    u = SIDE_PORTS["usbc"]; d.rounded_rectangle(u, 11, fill=(20, 20, 24), outline=(120, 120, 130), width=2)
    u = SIDE_PORTS["usb"]; d.rectangle(u, fill=(20, 20, 24), outline=(120, 120, 130), width=2); d.rectangle([u[0] + 8, u[1] + 6, u[2] - 8, u[1] + 14], fill=(40, 110, 220))
    h = SIDE_PORTS["hdmi2"]; d.polygon([(h[0], h[1]), (h[2], h[1]), (h[2], h[1] + 24), (h[2] - 12, h[3]), (h[0] + 12, h[3]), (h[0], h[1] + 24)], fill=(20, 20, 24), outline=(120, 120, 130))
    j = SIDE_PORTS["jack2"]; d.ellipse(j, fill=(20, 20, 24), outline=(120, 120, 130), width=2)

# ---------- prise USB (geste) ----------
def usb_scene(d, p, t):
    # prise femelle
    px, py = 760, 300
    d.rounded_rectangle([px - 40, py - 80, px + 300, py + 140], 18, fill=(70, 72, 82))
    d.rectangle([px, py, px + 170, py + 60], fill=(20, 20, 24), outline=(200, 200, 210), width=4)
    d.rectangle([px + 10, py + 6, px + 160, py + 24], fill=(40, 110, 220))  # languette en HAUT
    # fiche mâle
    flip = p > 0.45
    k = R.ease((p - 0.1) / 0.25) if p < 0.45 else R.ease((p - 0.6) / 0.25)
    if p < 0.45:
        x = 160 + k * 380
        if p > 0.3: x = 540 + 6 * math.sin(t * 40)
    else:
        x = 340 + k * (px - 340)
    y = py
    d.rectangle([x - 260, y - 10, x - 120, y + 70], fill=(40, 42, 50))
    d.line([x - 420, y + 30, x - 260, y + 30], fill=(40, 42, 50), width=14)
    d.rectangle([x - 120, y, x + 50, y + 60], fill=(205, 208, 215), outline=(120, 120, 130), width=3)
    # languette de la fiche : en haut (mauvais sens) puis en bas (bon sens)
    if flip:
        d.rectangle([x - 110, y + 36, x + 40, y + 54], fill=(250, 250, 250))
    else:
        d.rectangle([x - 110, y + 6, x + 40, y + 24], fill=(250, 250, 250))
    if 0.3 < p < 0.45:
        d.line([480, 160, 580, 260], fill=(230, 60, 50), width=14); d.line([580, 160, 480, 260], fill=(230, 60, 50), width=14)
        d.text((380, 420), "ça bloque : on ne force pas", font=F(30, "b"), fill=(230, 60, 50))
    if 0.45 <= p < 0.6:
        d.arc([380, 150, 520, 290], 200, 520, fill=YEL, width=10)
        d.text((380, 420), "on retourne la fiche", font=F(30, "b"), fill=INK)
    if p >= 0.85:
        d.ellipse([560, 130, 660, 230], fill=(43, 179, 163))
        d.line([585, 182, 605, 202, 640, 158], fill=(255, 255, 255), width=12)
        d.text((380, 420), "elle rentre toute seule !", font=F(30, "b"), fill=(20, 130, 115))

# ---------- périphériques ----------
def draw_periphs(d, p):
    draw_tower(d, (565, 200, 715, 460))
    items = [("Imprimante", (250, 200)), ("Haut-parleurs", (1030, 200)), ("Casque", (250, 430)), ("Clé USB", (1030, 430))]
    for i, (name, (x, y)) in enumerate(items):
        if p < 0.2 + i * 0.15: continue
        d.line([(640, 330), (x, y)], fill=(147, 17, 126), width=4)
        d.ellipse([x - 70, y - 70, x + 70, y + 70], fill=(255, 255, 255), outline=(147, 17, 126), width=4)
        if name == "Imprimante":
            d.rectangle([x - 45, y - 15, x + 45, y + 25], fill=(90, 92, 102)); d.rectangle([x - 28, y - 40, x + 28, y - 15], fill=(250, 250, 250), outline=INK, width=2); d.rectangle([x - 28, y + 20, x + 28, y + 40], fill=(250, 250, 250), outline=INK, width=2)
        elif name == "Haut-parleurs":
            for dx in (-28, 28):
                d.rounded_rectangle([x + dx - 18, y - 35, x + dx + 18, y + 35], 6, fill=(60, 62, 72)); d.ellipse([x + dx - 11, y - 2, x + dx + 11, y + 20], fill=(150, 150, 160))
        elif name == "Casque":
            d.arc([x - 40, y - 40, x + 40, y + 30], 180, 360, fill=INK, width=8)
            d.rounded_rectangle([x - 48, y - 5, x - 28, y + 32], 6, fill=INK); d.rounded_rectangle([x + 28, y - 5, x + 48, y + 32], 6, fill=INK)
        else:
            d.rounded_rectangle([x - 15, y - 40, x + 15, y + 20], 6, fill=(147, 17, 126)); d.rectangle([x - 11, y + 20, x + 11, y + 42], fill=(205, 208, 215), outline=INK, width=2)
        label(d, name, (x, y + 78))

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Découvrir l'ordinateur", ["fixe et portable", "Aide-mémoire n° 01 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([W / 2 - 130, 330, W / 2 + 10, 420], 8, fill=(30, 32, 40)); wallpaper(d, (W / 2 - 120, 340, W / 2, 410))
        d.rounded_rectangle([W / 2 + 40, 340, W / 2 + 150, 420], 8, fill=(30, 32, 40)); wallpaper(d, (W / 2 + 48, 348, W / 2 + 142, 404))
        d.polygon([(W / 2 + 30, 420), (W / 2 + 160, 420), (W / 2 + 172, 440), (W / 2 + 18, 440)], fill=(150, 152, 162))
        return im
    if sid == "intro":
        im = room(); d = ImageDraw.Draw(im)
        # à gauche : petit fixe ; à droite : portable
        s_mon = (120, 170, 420, 360)
        draw_monitor(d, s_mon); draw_tower(d, (450, 220, 550, 468))
        d.polygon([(150, 486), (390, 486), (400, 520), (140, 520)], fill=(235, 236, 240), outline=(120, 120, 130))
        if p > 0.15: label(d, "Fixe : reste sur la table", (320, 100))
        lx = 380
        d.rounded_rectangle([700 + 30, 200, 1080, 400], 10, fill=(30, 32, 40)); wallpaper(d, (746, 214, 1064, 388))
        d.polygon([(710, 405), (1100, 405), (1140, 470), (670, 470)], fill=(190, 192, 200), outline=(110, 112, 122))
        if p > 0.35: label(d, "Portable : vous suit partout", (905, 100))
        R.caption(d, cap); return im
    if sid in ("fixe", "uc", "ecran", "clavier", "souris"):
        im = room(); d = ImageDraw.Draw(im); draw_fixe(d); clean = im.copy()
        tgt = {"uc": TOWER, "ecran": (MON[0] - 14, MON[1] - 14, MON[2] + 14, MON[3] + 14), "clavier": KEYB, "souris": MOUSE}.get(sid)
        if sid == "fixe":
            names = [("Écran", (530, 82)), ("Unité centrale", (915, 110)), ("Clavier", (240, 500)), ("Souris", (900, 560))]
            for i, (n, at) in enumerate(names):
                if p > 0.25 + i * 0.12: label(d, n, at, "c" if n != "Clavier" else "c")
        else:
            R.highlight(d, tgt, t); R.arrow(d, tgt, t)
            if sid == "uc":
                pb = power_button_rect()
                if p > 0.6:
                    R.loupe(im, pb, place=(170, 250), clean=clean); d = ImageDraw.Draw(im)
                    label(d, "bouton pour allumer", (170, 400))
            if sid == "souris":
                off = 26 * math.sin(t * 2.2)
                im = room(); d = ImageDraw.Draw(im)
                draw_monitor(d); draw_tower(d); draw_keyboard(d)
                m = (MOUSE[0] + off, MOUSE[1], MOUSE[2] + off, MOUSE[3])
                draw_mouse(d, m, cable_to=(TOWER[0] + 10, TOWER[3] - 10))
                R.highlight(d, (m[0] - 10, m[1] - 10, m[2] + 10, m[3] + 10), t)
                R.arrow(d, m, t)
                # pointeur à l'écran qui suit
                R.cursor(d, 520 + off * 4, 250, 1.2)
            if sid == "clavier" and p > 0.3:
                txt = "Bonjour 123"[: int(11 * R.ease((p - 0.3) / 0.5))]
                d.rounded_rectangle([400, 230, 660, 280], 6, fill=(255, 255, 255))
                d.text((412, 238), txt + "|", font=F(28, "s"), fill=INK)
            if sid == "ecran" and p > 0.3:
                label(d, "comme une télévision", (530, 82))
        R.caption(d, cap); return im
    if sid == "toutenun":
        im = room(); d = ImageDraw.Draw(im)
        big = (380, 120, 900, 400)
        draw_monitor(d, big, aio=True)
        draw_keyboard(d, (390, 488, 790, 550)); draw_mouse(d, (850, 494, 896, 554))
        tgt = (big[0] - 16, big[1] - 16, big[2] + 16, big[3] + 46)
        R.highlight(d, tgt, t)
        if p > 0.3:
            # fantôme de l'unité centrale qui « rentre » derrière l'écran
            k = R.ease((p - 0.3) / 0.35)
            x = 1100 - k * 380
            if k < 1:
                d.rounded_rectangle([x, 200, x + 110, 440], 12, outline=(147, 17, 126), width=4)
            label(d, "unité centrale", (1060, 170)); label(d, "cachée derrière", (1060, 214))
        R.caption(d, cap); return im
    if sid == "portable":
        im = room(); d = ImageDraw.Draw(im); draw_laptop(d)
        R.highlight(d, (LAP_SCR[0] - 16, LAP_SCR[1] - 18, 930, 482), t)
        if p > 0.3: label(d, "Écran", (300, 200))
        if p > 0.45: label(d, "Clavier", (1050, 380))
        R.caption(d, cap); return im
    if sid == "pave":
        im = room(); d = ImageDraw.Draw(im); draw_laptop(d); clean = im.copy()
        R.highlight(d, PAD, t); R.arrow(d, PAD, t)
        if p > 0.25:
            R.loupe(im, PAD, place=(1040, 250), clean=clean); d = ImageDraw.Draw(im)
        if p > 0.5:
            off = 40 * math.sin(t * 2.0)
            fx, fy = 640 + off * 0.8, 445
            d.ellipse([fx - 12, fy - 12, fx + 12, fy + 12], fill=(240, 200, 170), outline=(150, 100, 80), width=2)
            R.cursor(d, 620 + off * 3, 200, 1.1)
        R.caption(d, cap); return im
    if sid == "batterie":
        im = room(); d = ImageDraw.Draw(im); draw_laptop(d)
        plugged = p > 0.5
        lvl = 0.12 if not plugged else min(1.0, 0.12 + (p - 0.5) * 1.6)
        battery(d, 110, 150, lvl)
        if plugged:
            draw_charger(d, (930, 455))
            R.highlight(d, (1000, 510, 1110, 576), t)
            d.text((105, 220), "⚡ en charge", font=F(24, "b"), fill=(20, 130, 115))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et regardez votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "peripheriques":
        im = room(); d = ImageDraw.Draw(im); draw_periphs(d, p)
        R.caption(d, cap); return im
    if sid == "prises":
        im = room(); d = ImageDraw.Draw(im); draw_back(d); clean = im.copy()
        a = PORTS["alim"]; seq = [((a[0] - 20, a[1] - 20, a[2] + 20, a[3] + 60), "Alimentation", 0.05, 0.42), (PORTS["hdmi"], "Écran (HDMI)", 0.42, 0.62), (usb_all(), "Clavier et souris (USB)", 0.62, 1.01)]
        for r, name, a0, a1 in seq:
            if p >= a0:
                lx = (r[0] + r[2]) / 2
                label(d, name, {"Alimentation": (430, 325), "Écran (HDMI)": (630, 236)}.get(name, (lx, r[3] + 10)))
            if a0 <= p < a1:
                R.highlight(d, r, t); R.arrow(d, r, t)
        if p < 0.42:
            # prise murale + câble
            d.rounded_rectangle([1060, 260, 1160, 360], 14, fill=(250, 250, 250), outline=(150, 150, 150), width=2)
            d.ellipse([1088, 300, 1100, 312], fill=(60, 60, 60)); d.ellipse([1120, 300, 1132, 312], fill=(60, 60, 60))
            d.line([(a[2] + 20, a[1] + 50), (1060, 310)], fill=(30, 30, 36), width=8)
            d.text((1040, 370), "prise électrique", font=F(22, "s"), fill=INK)
        R.caption(d, cap); return im
    if sid == "usb":
        im = room(); d = ImageDraw.Draw(im); usb_scene(d, p, t)
        R.caption(d, cap); return im
    if sid == "cotes":
        im = room(); d = ImageDraw.Draw(im); draw_side(d); clean = im.copy()
        R.highlight(d, (SIDE[0] + 50, SIDE[1] + 45, SIDE[2] - 40, SIDE[3] - 10), t) if p < 0.35 else None
        if p >= 0.35:
            c = SIDE_PORTS["charge"]; R.highlight(d, (c[0] - 4, c[1] - 4, SIDE_PORTS["usbc"][2] + 4, c[3] + 4), t)
            R.arrow(d, (c[0], c[1], SIDE_PORTS["usbc"][2], c[3]), t)
            label(d, "chargeur : prise ronde", (280, 160)); label(d, "ou ovale (USB-C)", (280, 200))
            R.loupe(im, (c[0], c[1], SIDE_PORTS["usbc"][2], c[3]), place=(1000, 215), clean=clean); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Regardez votre ordinateur :", "est-il fixe ou portable ?", "Trouvez l'écran, le clavier,", "la souris ou le pavé tactile."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Regardez bien", "votre ordinateur."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        im = room(); d = ImageDraw.Draw(im)
        draw_monitor(d, (90, 170, 330, 330)); draw_tower(d, (380, 200, 470, 468))
        d.polygon([(110, 486), (310, 486), (320, 520), (100, 520)], fill=(235, 236, 240), outline=(120, 120, 130))
        draw_mouse(d, (350, 490, 380, 530))
        d.rounded_rectangle([760, 190, 1080, 380], 10, fill=(30, 32, 40)); wallpaper(d, (774, 204, 1066, 368))
        d.polygon([(730, 385), (1110, 385), (1150, 470), (690, 470)], fill=(190, 192, 200), outline=(110, 112, 122))
        d.rounded_rectangle([870, 435, 970, 462], 5, fill=(170, 172, 182))
        if p > 0.15:
            R.highlight(d, (70, 150, 490, 540), t) if p < 0.55 else None
            label(d, "Séparés : FIXE", (280, 96))
        if p > 0.55:
            R.highlight(d, (670, 160, 1170, 490), t)
            label(d, "Réunis : PORTABLE", (920, 96))
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["L'écran · le clavier · la souris", "l'unité centrale", "Portable : le pavé tactile", "remplace la souris"], "Bravo ! À bientôt à Espace 19 Numérique !")
    raise KeyError(sid)

def main(script, durs, out):
    sc = json.load(open(script)); du = json.load(open(durs))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    total = 0
    for s in sc["scenes"]:
        D = du[s["id"]]; n = int(round(D * FPS)); total += n
        for i in range(n):
            im = frame(s["id"], i / FPS, D, s["caption"])
            R.subtitle(im, R.sub_at(s["narration"], i / FPS, D, s.get("_start", 0.4)))
            p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    print("frames", total, "duree", total / FPS)

def estimate(script):
    """Durées sans voix : ~13 caractères/s (voix lente) + marge pour refaire."""
    sc = json.load(open(script)); MARGE = {"uc": 1.5, "souris": 1.5, "pave": 2, "prises": 2, "usb": 1.5, "cotes": 1.5, "pause1": 3}
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
