"""Rendu de la vidéo « 01 - Créer un dossier personnel » (écrans dessinés, sans voix).
Usage : python3 render_01.py script.json durations.json out.mp4
durations.json : {"titre": 3.0, ...} en secondes par scène.
"""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 12
YEL = (255, 212, 0)
FONT_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
FONT_R = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
FONT_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
_fc = {}
def F(size, w="r"):
    k = (size, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype({"r": FONT_R, "b": FONT_B, "s": FONT_SB}[w], size)
    return _fc[k]

# ---------- géométrie ----------
WX, WY, WW, WH = 150, 92, 980, 540           # fenêtre Explorateur
TB_H = 52                                    # barre des tâches
NAV_W = 200
CMD_Y = WY + 38
CONT_X, CONT_Y = WX + NAV_W + 10, WY + 38 + 52 + 40
NAV_ITEMS = ["Accueil", "Bureau", "Téléchargements", "Documents", "Images", "Musique", "Vidéos"]

def taskbar_icons():
    cx = W // 2
    return {"start": (cx - 90, H - TB_H // 2), "search": (cx - 30, H - TB_H // 2),
            "explorer": (cx + 30, H - TB_H // 2), "edge": (cx + 90, H - TB_H // 2)}

def rect_of(name, st=None):
    """Rectangle (x0,y0,x1,y1) des éléments cliquables."""
    if name == "explorer":
        x, y = taskbar_icons()["explorer"]; return (x - 24, y - 22, x + 24, y + 22)
    if name.startswith("nav:"):
        i = NAV_ITEMS.index(name[4:]); y = CMD_Y + 52 + 14 + i * 44
        return (WX + 8, y, WX + NAV_W - 8, y + 38)
    if name == "nouveau":
        return (WX + 14, CMD_Y + 8, WX + 140, CMD_Y + 46)
    if name == "menu:dossier":
        return (WX + 14, CMD_Y + 52, WX + 270, CMD_Y + 96)
    if name.startswith("folder:"):
        i = int(name[7:]); col, row = i % 5, i // 5
        x = CONT_X + 20 + col * 150; y = CONT_Y + 20 + row * 150
        return (x, y, x + 130, y + 130)
    if name == "empty":
        return (CONT_X + 200, CONT_Y + 140, CONT_X + 260, CONT_Y + 200)
    if name == "ctx:nouveau":
        x, y = CTX_POS; return (x, y + 8, x + 230, y + 50)
    if name == "ctx:dossier":
        x, y = CTX_POS; return (x + 232, y + 8, x + 450, y + 50)
    raise KeyError(name)

CTX_POS = (CONT_X + 230, CONT_Y + 170)

def center(r): return ((r[0] + r[2]) / 2, (r[1] + r[3]) / 2)

# ---------- dessin de base ----------
def bg():
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(20 + 40 * t), int(60 + 70 * t), int(140 + 80 * t)))
    return im

BG = None
def folder_icon(d, x, y, s=1.0, color=(250, 200, 70)):
    w, h = 90 * s, 66 * s
    d.rounded_rectangle([x, y + 8 * s, x + 38 * s, y + 22 * s], 4, fill=(225, 170, 40))
    d.rounded_rectangle([x, y + 16 * s, x + w, y + h], 6, fill=color, outline=(200, 150, 30), width=2)

def draw_taskbar(d):
    d.rectangle([0, H - TB_H, W, H], fill=(238, 240, 245))
    ic = taskbar_icons()
    x, y = ic["start"]
    for dx in (-9, 3):
        for dy in (-9, 3):
            d.rectangle([x + dx, y + dy, x + dx + 9, y + dy + 9], fill=(0, 120, 215))
    x, y = ic["search"]; d.ellipse([x - 9, y - 11, x + 7, y + 5], outline=(60, 60, 60), width=3); d.line([x + 5, y + 3, x + 12, y + 10], fill=(60, 60, 60), width=3)
    x, y = ic["explorer"]; folder_icon(d, x - 18, y - 16, 0.4)
    x, y = ic["edge"]; d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=(0, 140, 200)); d.ellipse([x - 5, y - 3, x + 9, y + 9], fill=(80, 220, 120))

def draw_window(d, st):
    d.rounded_rectangle([WX + 6, WY + 8, WX + WW + 6, WY + WH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([WX, WY, WX + WW, WY + WH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([WX, WY, WX + WW, WY + 38], 10, fill=(232, 236, 244)); d.rectangle([WX, WY + 20, WX + WW, WY + 38], fill=(232, 236, 244))
    folder_icon(d, WX + 14, WY + 9, 0.25)
    d.text((WX + 44, WY + 9), st["view"], font=F(17, "s"), fill=(30, 30, 30))
    for i, c in enumerate(("—", "☐", "✕")):
        d.text((WX + WW - 120 + i * 40, WY + 8), c, font=F(17), fill=(60, 60, 60))
    # barre de commandes
    d.rectangle([WX + 2, CMD_Y, WX + WW - 2, CMD_Y + 52], fill=(246, 248, 252))
    r = rect_of("nouveau")
    d.rounded_rectangle(r, 6, fill=(225, 235, 250) if st.get("menu") else (246, 248, 252))
    d.text((r[0] + 10, r[1] + 4), "+", font=F(24, "b"), fill=(0, 103, 192))
    d.text((r[0] + 36, r[1] + 8), "Nouveau", font=F(19, "s"), fill=(20, 20, 20))
    d.text((r[2] - 18, r[1] + 8), "˅", font=F(16), fill=(80, 80, 80))
    for i in range(6):
        x = WX + 170 + i * 52
        d.rounded_rectangle([x, CMD_Y + 16, x + 22, CMD_Y + 36], 4, fill=(200, 205, 215))
    # fil d'Ariane
    d.rectangle([WX + 2, CMD_Y + 52, WX + WW - 2, CMD_Y + 53], fill=(220, 224, 230))
    # navigation
    for it in NAV_ITEMS:
        r = rect_of("nav:" + it)
        if it == st["view"]:
            d.rounded_rectangle(r, 6, fill=(204, 228, 247))
        folder_icon(d, r[0] + 8, r[1] + 9, 0.23, (250, 200, 70) if it not in ("Accueil",) else (120, 160, 220))
        d.text((r[0] + 40, r[1] + 8), it, font=F(17), fill=(20, 20, 20))
    d.line([WX + NAV_W, CMD_Y + 54, WX + NAV_W, WY + WH - 4], fill=(225, 228, 235), width=2)
    # contenu
    if st["view"] == "Accueil":
        d.text((CONT_X + 20, CONT_Y - 30), "Accueil", font=F(22, "b"), fill=(30, 30, 30))
        for i in range(3):
            d.rounded_rectangle([CONT_X + 20, CONT_Y + 30 + i * 60, CONT_X + 700, CONT_Y + 76 + i * 60], 6, fill=(243, 245, 249))
    else:
        d.text((CONT_X + 20, CONT_Y - 30), st["view"], font=F(22, "b"), fill=(30, 30, 30))
        for i, name in enumerate(st["folders"]):
            r = rect_of(f"folder:{i}")
            folder_icon(d, r[0] + 20, r[1] + 10, 1.0)
            edit = st.get("edit")
            if edit is not None and i == len(st["folders"]) - 1:
                txt, selected = edit
                tw = d.textlength(txt or " ", font=F(17))
                bx0 = (r[0] + r[2]) / 2 - max(tw, 20) / 2 - 6
                d.rectangle([bx0, r[1] + 92, bx0 + max(tw, 20) + 12, r[1] + 120], fill=(255, 255, 255), outline=(0, 103, 192), width=2)
                if selected:
                    d.rectangle([bx0 + 5, r[1] + 95, bx0 + 7 + tw, r[1] + 117], fill=(0, 103, 192))
                    d.text((bx0 + 6, r[1] + 95), txt, font=F(17), fill=(255, 255, 255))
                else:
                    d.text((bx0 + 6, r[1] + 95), txt, font=F(17), fill=(0, 0, 0))
                    cx = bx0 + 7 + tw
                    d.line([cx, r[1] + 96, cx, r[1] + 116], fill=(0, 0, 0), width=2)
            else:
                tw = d.textlength(name, font=F(17))
                d.text(((r[0] + r[2]) / 2 - tw / 2, r[1] + 95), name, font=F(17), fill=(20, 20, 20))
    if st.get("menu"):
        r = rect_of("menu:dossier")
        d.rounded_rectangle([r[0] - 4, r[1] - 6, r[2] + 4, r[1] + 150], 8, fill=(252, 252, 254), outline=(180, 185, 195), width=2)
        folder_icon(d, r[0] + 10, r[1] + 11, 0.28)
        d.text((r[0] + 50, r[1] + 10), "Dossier", font=F(19, "s"), fill=(20, 20, 20))
        for i in range(2):
            d.rounded_rectangle([r[0] + 12, r[1] + 62 + i * 40, r[0] + 200, r[1] + 76 + i * 40], 5, fill=(225, 228, 234))
    if st.get("ctx"):
        x, y = CTX_POS
        d.rounded_rectangle([x, y, x + 230, y + 190], 8, fill=(252, 252, 254), outline=(180, 185, 195), width=2)
        rn = rect_of("ctx:nouveau")
        if st["ctx"] >= 2:
            d.rounded_rectangle(rn, 5, fill=(225, 235, 250))
        d.text((rn[0] + 46, rn[1] + 9), "Nouveau", font=F(19, "s"), fill=(20, 20, 20))
        d.text((rn[2] - 24, rn[1] + 8), "›", font=F(20, "b"), fill=(60, 60, 60))
        for i in range(3):
            d.rounded_rectangle([x + 46, y + 72 + i * 38, x + 190, y + 86 + i * 38], 5, fill=(225, 228, 234))
        if st["ctx"] >= 2:
            rd = rect_of("ctx:dossier")
            d.rounded_rectangle([rd[0], y, rd[2], y + 130], 8, fill=(252, 252, 254), outline=(180, 185, 195), width=2)
            folder_icon(d, rd[0] + 10, rd[1] + 8, 0.28)
            d.text((rd[0] + 50, rd[1] + 9), "Dossier", font=F(19, "s"), fill=(20, 20, 20))
            for i in range(2):
                d.rounded_rectangle([rd[0] + 14, y + 70 + i * 32, rd[0] + 170, y + 82 + i * 32], 5, fill=(225, 228, 234))

def screen(st):
    global BG
    if BG is None: BG = bg()
    im = BG.copy(); d = ImageDraw.Draw(im)
    if not st.get("window"):
        # icônes du bureau
        folder_icon(d, 40, 40, 0.7); d.text((36, 98), "Corbeille", font=F(15), fill=(255, 255, 255))
    draw_taskbar(d)
    if st.get("window"):
        draw_window(d, st)
    return im

# ---------- surcouches ----------
def cursor(d, x, y, s=1.7):
    pts = [(0, 0), (0, 25), (6, 19), (11, 30), (15, 28), (10, 18), (18, 18)]
    pts = [(x + px * s, y + py * s) for px, py in pts]
    d.polygon(pts, fill=(255, 255, 255), outline=(0, 0, 0))
    d.line(pts + [pts[0]], fill=(0, 0, 0), width=3)

def ripple(d, x, y, p, color=YEL):
    if 0 <= p <= 1:
        r = 12 + 50 * p
        d.ellipse([x - r, y - r, x + r, y + r], outline=color, width=max(2, int(10 * (1 - p))))

def highlight(d, r, t):
    if (t % 0.7) < 0.47:
        d.rounded_rectangle([r[0] - 10, r[1] - 10, r[2] + 10, r[3] + 10], 10, outline=YEL, width=9)

def arrow(d, r, t):
    cx, cy = center(r)
    bounce = 10 * math.sin(t * 6)
    # flèche venant d'en haut à droite (ou d'en haut si près du bord)
    if cy > H - 140:
        tip = (cx, r[1] - 18 - bounce); ang = -math.pi / 2
    else:
        tip = (r[2] + 18 + bounce, cy); ang = 0
    L = 90
    bx = tip[0] + L * math.cos(ang); by = tip[1] + L * math.sin(ang)
    for col, wid in (((0, 0, 0), 22), (YEL, 14)):
        d.line([tip, (bx, by)], fill=col, width=wid)
    ux, uy = math.cos(ang), math.sin(ang); px, py = -uy, ux
    head = [tip, (tip[0] + 38 * ux + 26 * px, tip[1] + 38 * uy + 26 * py), (tip[0] + 38 * ux - 26 * px, tip[1] + 38 * uy - 26 * py)]
    d.polygon(head, fill=YEL, outline=(0, 0, 0)); d.line(head + [head[0]], fill=(0, 0, 0), width=3)

def loupe(im, r, place=None, clean=None):
    cx, cy = center(r); R, Z = 125, 2.0
    src = (clean or im).crop((int(cx - R / Z), int(cy - R / Z), int(cx + R / Z), int(cy + R / Z))).resize((2 * R, 2 * R), Image.LANCZOS)
    if place is None:
        place = (W - R - 40, R + 110) if cx < W / 2 else (R + 40, R + 110)
        if cy < 250: place = (place[0], H - TB_H - R - 30)
    mask = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(mask).ellipse([0, 0, 2 * R, 2 * R], fill=255)
    im.paste(src, (int(place[0] - R), int(place[1] - R)), mask)
    d = ImageDraw.Draw(im)
    d.ellipse([place[0] - R - 6, place[1] - R - 6, place[0] + R + 6, place[1] + R + 6], outline=(0, 0, 0), width=4)
    d.ellipse([place[0] - R - 3, place[1] - R - 3, place[0] + R + 3, place[1] + R + 3], outline=YEL, width=8)
    d.text((place[0] - 30, place[1] + R + 10), "zoom", font=F(18, "b"), fill=YEL, stroke_width=3, stroke_fill=(0, 0, 0))

def caption(d, text):
    if not text: return
    f = F(34, "b"); tw = d.textlength(text, font=f)
    x0 = W / 2 - tw / 2 - 24
    d.rounded_rectangle([x0, 18, x0 + tw + 48, 76], 14, fill=(15, 20, 40))
    d.rounded_rectangle([x0, 18, x0 + tw + 48, 76], 14, outline=YEL, width=3)
    d.text((W / 2 - tw / 2, 27), text, font=f, fill=(255, 255, 255))

def key_enter(d, t, pressed):
    x, y = W / 2 - 110, H / 2 + 60
    off = 8 if pressed else 0
    d.rounded_rectangle([x + 6, y + 10, x + 226, y + 130], 16, fill=(60, 60, 70))
    d.rounded_rectangle([x + off / 2, y + off, x + 220 + off / 2, y + 120 + off], 16, fill=(245, 245, 248), outline=(80, 80, 90), width=3)
    d.text((x + 50 + off / 2, y + 38 + off), "Entrée ↵", font=F(32, "b"), fill=(20, 20, 20))
    if (t % 0.7) < 0.47:
        d.rounded_rectangle([x - 12, y - 12, x + 236, y + 142], 18, outline=YEL, width=9)

def card(title, lines, sub=None, big_icon=None):
    im = bg(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([90, 36, W - 90, H - 140], 28, fill=(255, 255, 255))
    d.rounded_rectangle([90, 36, W - 90, H - 140], 28, outline=YEL, width=8)
    f = F(52, "b"); tw = d.textlength(title, font=f)
    d.text((W / 2 - tw / 2, 70), title, font=f, fill=(15, 40, 100))
    y = 160
    for ln in lines:
        f2 = F(34, "s"); tw = d.textlength(ln, font=f2)
        d.text((W / 2 - tw / 2, y), ln, font=f2, fill=(30, 30, 30)); y += 58
    if big_icon == "pause":
        d.rounded_rectangle([W/2-50, 330, W/2-16, 440], 8, fill=(15,40,100)); d.rounded_rectangle([W/2+16, 330, W/2+50, 440], 8, fill=(15,40,100))
    if sub:
        f3 = F(24); tw = d.textlength(sub, font=f3); d.text((W / 2 - tw / 2, H - 200), sub, font=f3, fill=(90, 90, 90))
    return im

# ---------- scènes ----------
def lerp(a, b, p): return a + (b - a) * p
def ease(p): p = max(0, min(1, p)); return p * p * (3 - 2 * p)

def move(t, t0, t1, a, b):
    p = ease((t - t0) / max(t1 - t0, 1e-6)); return (lerp(a[0], b[0], p), lerp(a[1], b[1], p))

BASE_DOCS = ["Lettres", "Factures"]

def act_click(st_before, st_after, target, start, t, D, cap, typed=None, show_loupe=True):
    """Gabarit : curseur qui va lentement vers la cible, cadre clignotant + flèche + loupe, clic à 60 %."""
    r = rect_of(target); c = center(r)
    tc = 0.6 * D
    st = st_after if t >= tc + 0.3 else st_before
    im = screen(st); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3:
        highlight(d, r, t); arrow(d, r, t)
    pos = move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        loupe(im, r, clean=clean); d = ImageDraw.Draw(im)
    cursor(d, *pos)
    ripple(d, c[0], c[1], (t - tc) / 0.6)
    caption(d, cap)
    return im, pos

def frame(sid, t, D, cap, ctx):
    p = t / D
    if sid == "titre":
        im = card("Créer un dossier personnel", ["Aide-mémoire n° 08", "Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); folder_icon(d, W / 2 - 70, 330, 1.55); return im
    if sid == "intro":
        im = screen({"window": False}); d = ImageDraw.Draw(im)
        folder_icon(d, W / 2 - 150, 200, 3.3)
        for i in range(3):
            if p > 0.25 + i * 0.15:
                d.rounded_rectangle([W / 2 - 110 + i * 25, 180 - i * 6, W / 2 + 60 + i * 25, 300 - i * 6], 6, fill=(255, 255, 255), outline=(150, 150, 150), width=2)
        folder_icon(d, W / 2 - 150, 230, 3.3)
        caption(d, cap); return im
    if sid == "ouvrir":
        im, _ = act_click({"window": False}, {"window": True, "view": "Accueil", "folders": []}, "explorer", (W / 2 + 200, H / 2), t, D, cap)
        return im
    if sid == "documents":
        im, _ = act_click({"window": True, "view": "Accueil", "folders": []}, {"window": True, "view": "Documents", "folders": BASE_DOCS}, "nav:Documents", (W / 2 + 40, H - 30), t, D, cap)
        return im
    if sid == "nouveau":
        b = {"window": True, "view": "Documents", "folders": BASE_DOCS}
        im, _ = act_click(b, dict(b, menu=True), "nouveau", center(rect_of("nav:Documents")), t, D, cap)
        return im
    if sid == "dossier":
        b = {"window": True, "view": "Documents", "folders": BASE_DOCS, "menu": True}
        a = {"window": True, "view": "Documents", "folders": BASE_DOCS + ["Nouveau dossier"], "edit": ("Nouveau dossier", True)}
        im, _ = act_click(b, a, "menu:dossier", center(rect_of("nouveau")), t, D, cap)
        return im
    if sid in ("taper",):
        word = "Famille"; k = int(len(word) * ease((p - 0.55) / 0.3)) if p > 0.55 else 0
        edit = ("Nouveau dossier", True) if k == 0 else (word[:k], False)
        st = {"window": True, "view": "Documents", "folders": BASE_DOCS + ["x"], "edit": edit}
        im = screen(st); clean = im.copy(); d = ImageDraw.Draw(im)
        r = rect_of("folder:2"); r2 = (r[0] - 10, r[1] + 85, r[2] + 10, r[3] - 5)
        highlight(d, r2, t); arrow(d, r2, t)
        loupe(im, r2, place=(W - 170, 420), clean=clean); d = ImageDraw.Draw(im)
        cursor(d, *center(rect_of("menu:dossier"))); caption(d, cap); return im
    if sid == "entree":
        done = p > 0.4
        st = {"window": True, "view": "Documents", "folders": BASE_DOCS + ["Famille"]}
        if not done: st["edit"] = ("Famille", False)
        im = screen(st); d = ImageDraw.Draw(im)
        if not done:
            key_enter(d, t, 0.33 < p < 0.4)
        else:
            r = rect_of("folder:2"); highlight(d, r, t)
            f = F(56, "b"); d.text((W / 2 - 110, H / 2 + 120), "Bravo !", font=f, fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
        caption(d, cap); return im
    if sid == "pause1":
        im = card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
        return im
    if sid == "clicdroit":
        base = {"window": True, "view": "Documents", "folders": BASE_DOCS + ["Famille"]}
        e = rect_of("empty"); ce = center(e)
        rn = rect_of("ctx:nouveau"); rd = rect_of("ctx:dossier")
        t1, t2, t3, t4 = 0.22 * D, 0.38 * D, 0.55 * D, 0.62 * D
        if t < t1:
            st = base; tgt = e; pos = move(t, 0.03 * D, 0.18 * D, center(rect_of("folder:2")), ce)
        elif t < t2:
            st = dict(base, ctx=1); tgt = rn; pos = move(t, t1 + 0.03 * D, t2 - 0.03 * D, ce, (center(rn)[0] - 40, center(rn)[1]))
        elif t < t4:
            st = dict(base, ctx=2); tgt = rd; pos = move(t, t2 + 0.02 * D, t3, (center(rn)[0] - 40, center(rn)[1]), center(rd))
        else:
            word = "Santé"; k = int(len(word) * ease((t - t4 - 0.15 * D) / (0.15 * D))) if t > t4 + 0.15 * D else 0
            done = t > 0.9 * D
            fol = BASE_DOCS + ["Famille", "Santé"]
            st = dict(base, folders=fol)
            if not done:
                st["edit"] = ("Nouveau dossier", True) if k == 0 else (word[:k], False)
            tgt = rect_of("folder:3"); pos = center(rd)
        im = screen(st); d = ImageDraw.Draw(im)
        if t < t4:
            highlight(d, tgt, t); arrow(d, tgt, t)
        else:
            r = rect_of("folder:3"); highlight(d, (r[0] - 10, r[1] + 85, r[2] + 10, r[3] - 5), t)
        cursor(d, *pos)
        if t < t1 + 0.6: ripple(d, ce[0], ce[1], (t - t1) / 0.6, (255, 120, 0))
        ripple(d, *center(rd), (t - t4) / 0.6)
        if t < t1:
            d.text((ce[0] - 120, ce[1] + 40), "clic DROIT", font=F(30, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
        caption(d, cap); return im
    if sid == "exercice":
        return card("Exercice", ["Dans « Documents »,", "créez un dossier nommé :", "Recettes"], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        im = card("À vous !", ["Faites l'exercice", "sur votre ordinateur."], f"La solution arrive dans {left} s", "pause")
        return im
    if sid == "solution":
        seg = [("nav:Documents", 0.0, 0.22), ("nouveau", 0.22, 0.42), ("menu:dossier", 0.42, 0.6)]
        base = {"window": True, "view": "Accueil", "folders": []}
        docs = {"window": True, "view": "Documents", "folders": BASE_DOCS}
        states = [(base, docs), (docs, dict(docs, menu=True)), (dict(docs, menu=True), dict(docs, folders=BASE_DOCS + ["x"], edit=("Nouveau dossier", True)))]
        starts = [(W / 2, H / 2), center(rect_of("nav:Documents")), center(rect_of("nouveau"))]
        for i, (tg, a, b) in enumerate(seg):
            if a * D <= t < b * D:
                im, _ = act_click(states[i][0], states[i][1], tg, starts[i], t - a * D, (b - a) * D, cap, show_loupe=False)
                return im
        word = "Recettes"
        if p < 0.85:
            k = int(len(word) * ease((p - 0.62) / 0.15)) if p > 0.62 else 0
            st = dict(docs, folders=BASE_DOCS + ["x"], edit=("Nouveau dossier", True) if k == 0 else (word[:k], False))
            im = screen(st); d = ImageDraw.Draw(im)
            if p > 0.78: key_enter(d, t, p > 0.82)
        else:
            im = screen(dict(docs, folders=BASE_DOCS + ["Recettes"])); d = ImageDraw.Draw(im)
            highlight(d, rect_of("folder:2"), t)
            d.text((W / 2 - 60, H / 2 + 120), "Prêt !", font=F(52, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
        caption(d, cap); return im
    if sid == "resume":
        return card("À retenir", ["1. Nouveau", "2. Dossier", "3. Je tape le nom", "4. Entrée"], "À bientôt à Espace 19 Numérique !")
    raise KeyError(sid)

import re as _re
def _phrases(txt):
    return [x.strip() for x in _re.split(r'(?<=[.!?])\s+', txt) if x.strip()]

def subtitle(im, text):
    if not text: return
    d = ImageDraw.Draw(im); f = F(27, "s")
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > W - 220: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    lh = 36; h = lh * len(lines) + 18; y0 = H - TB_H - 14 - h
    wmax = max(d.textlength(l, font=f) for l in lines)
    d.rounded_rectangle([W/2 - wmax/2 - 18, y0, W/2 + wmax/2 + 18, y0 + h], 10, fill=(0, 0, 0))
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=f)
        d.text((W/2 - tw/2, y0 + 9 + i*lh), l, font=f, fill=(255, 255, 255))

def sub_at(narr, t, D, start=0.4):
    """Phrase affichée au temps t : réparties selon leur longueur sur la durée parlée."""
    ph = _phrases(narr)
    if not ph: return ""
    tot = sum(len(x) for x in ph); parl = max(D - start - 1.0, 1.0); acc = start
    for x in ph:
        dd = parl * len(x) / tot
        if t < acc + dd: return x if t >= start - 0.2 else ""
        acc += dd
    return ph[-1] if t < D - 0.3 else ""

def main(script, durs, out):
    sc = json.load(open(script)); du = json.load(open(durs))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    total = 0
    for s in sc["scenes"]:
        D = du[s["id"]]; n = int(round(D * FPS)); total += n
        for i in range(n):
            im = frame(s["id"], i / FPS, D, s["caption"], None)
            subtitle(im, sub_at(s["narration"], i / FPS, D, s.get("_start", 0.4)))
            p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    print("frames", total, "duree", total / FPS)

if __name__ == "__main__":
    main(*sys.argv[1:4])
