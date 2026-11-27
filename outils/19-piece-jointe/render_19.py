"""Vidéo « 19 - Joindre et lire une pièce jointe » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_19.py script.json durations.json out.mp4
        python3 render_19.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, barre des tâches, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes)
et ../01-ordinateur/render_01_ordinateur.py (étiquettes).
Messagerie DESSINÉE, simplifiée et NEUTRE : aucun logo, aucune couleur ni charte de marque. Libellés écrits tels quels
(voir sources_19.md) : « Nouveau message », « Envoyer », le trombone, la flèche vers le bas, « Téléchargements ».
Noms et documents fictifs (Paul Martin, photo_jardin.jpg).
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); BLEU = (0, 103, 192); GRIS = (110, 110, 120); ROUGE = (200, 40, 40)

# ---------- géométrie ----------
BX, BY, BW, BH = 70, 64, 1140, 584
TOP = BY + 44                 # bas de la barre d'onglet
NEW = (BX + 20, TOP + 20, BX + 230, TOP + 72)
LIST_X = BX + 260
ROW_H = 58
COMP = (BX + 560, TOP + 30, BX + BW - 20, TOP + 470)      # fenêtre « Nouveau message »
SEND = (COMP[0] + 20, COMP[3] - 56, COMP[0] + 150, COMP[3] - 14)
CLIP = (COMP[0] + 168, COMP[3] - 56, COMP[0] + 216, COMP[3] - 14)
CHIP = (COMP[0] + 20, COMP[3] - 116, COMP[0] + 300, COMP[3] - 72)
DLG = (BX + 180, TOP + 50, BX + 820, TOP + 430)           # fenêtre des dossiers de l'ordinateur
TILES = [("photo_jardin.jpg", "img"), ("facture_eau.pdf", "pdf"), ("lettre.docx", "doc")]
def tile_rect(i): x = DLG[0] + 210 + i * 140; return (x, DLG[1] + 90, x + 120, DLG[1] + 230)
PHOTO = tile_rect(0)
ROW0 = (LIST_X, TOP + 20, BX + BW - 20, TOP + 20 + ROW_H)  # première ligne de la liste
THUMB = (LIST_X + 30, TOP + 270, LIST_X + 230, TOP + 400)  # vignette dans le message ouvert
DLBTN = (THUMB[2] - 52, THUMB[1] + 10, THUMB[2] - 10, THUMB[1] + 52)

def clip_icon(d, cx, cy, s=1.0, col=INK, w=3):
    """Trombone dessiné."""
    w = max(2, int(w * s))
    d.arc([cx - 7 * s, cy - 16 * s, cx + 7 * s, cy - 2 * s], 180, 360, fill=col, width=w)
    d.line([cx - 7 * s, cy - 9 * s, cx - 7 * s, cy + 10 * s], fill=col, width=w)
    d.line([cx + 7 * s, cy - 9 * s, cx + 7 * s, cy + 6 * s], fill=col, width=w)
    d.arc([cx - 7 * s, cy + 3 * s, cx + 3 * s, cy + 17 * s], 0, 180, fill=col, width=w)
    d.line([cx + 3 * s, cy + 10 * s, cx + 3 * s, cy - 7 * s], fill=col, width=w)
    d.arc([cx - 2 * s, cy - 12 * s, cx + 3 * s, cy - 4 * s], 180, 360, fill=col, width=w)

def garden(d, r):
    """Petite photo de jardin dessinée (document fictif)."""
    x0, y0, x1, y1 = r; h = y1 - y0
    d.rectangle(r, fill=(150, 200, 240))
    d.rectangle([x0, y0 + h * 0.62, x1, y1], fill=(90, 170, 80))
    sr = h * 0.12; d.ellipse([x1 - sr * 3, y0 + sr, x1 - sr, y0 + sr * 3], fill=(255, 210, 60))
    for k in range(5):
        fx = x0 + (x1 - x0) * (0.12 + k * 0.18); fy = y0 + h * 0.72
        d.line([fx, fy, fx, fy + h * 0.15], fill=(40, 120, 40), width=max(2, int(h / 60)))
        rr = h * 0.05; d.ellipse([fx - rr, fy - rr, fx + rr, fy + rr], fill=[(230, 60, 90), (250, 200, 50), (240, 120, 200)][k % 3])

def doc_icon(d, r, kind):
    if kind == "img":
        garden(d, (r[0] + 14, r[1] + 10, r[2] - 14, r[3] - 40))
    else:
        x0, y0, x1, y1 = r[0] + 30, r[1] + 10, r[2] - 30, r[3] - 40
        d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(150, 150, 160), width=2)
        col = (200, 60, 60) if kind == "pdf" else (40, 90, 180)
        d.rectangle([x0, y1 - 22, x1, y1], fill=col)
        for k in range(4): d.line([x0 + 8, y0 + 14 + k * 12, x1 - 8, y0 + 14 + k * 12], fill=(180, 180, 190), width=2)

def window(d, title="Ma messagerie"):
    d.rounded_rectangle([BX + 6, BY + 8, BX + BW + 6, BY + BH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([BX, BY, BX + BW, BY + BH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([BX, BY, BX + BW, TOP + 6], 10, fill=(222, 226, 236)); d.rectangle([BX, BY + 20, BX + BW, TOP], fill=(222, 226, 236))
    d.rounded_rectangle([BX + 12, BY + 6, BX + 330, TOP + 2], 8, fill=(250, 250, 252))
    d.rounded_rectangle([BX + 24, BY + 15, BX + 46, BY + 31], 3, outline=GRIS, width=2); d.line([BX + 24, BY + 15, BX + 35, BY + 25, BX + 46, BY + 15], fill=GRIS, width=2)
    d.text((BX + 56, BY + 12), title + " (dessin simplifié)", font=F(16), fill=(30, 30, 30))

def sidebar(d):
    d.rounded_rectangle(NEW, 18, fill=(232, 236, 246), outline=(160, 170, 190), width=2)
    d.line([NEW[0] + 22, NEW[1] + 36, NEW[0] + 34, NEW[1] + 16], fill=INK, width=3)   # crayon
    d.text((NEW[0] + 46, NEW[1] + 13), "Nouveau message", font=F(19, "s"), fill=INK)
    d.rounded_rectangle([BX + 14, TOP + 92, BX + 240, TOP + 130], 16, fill=(220, 226, 240))
    d.text((BX + 34, TOP + 99), "Mes messages", font=F(18, "s"), fill=INK)
    d.text((BX + 34, TOP + 145), "Messages envoyés", font=F(18), fill=INK)

MSGS = [("Paul Martin", "Photos du jardin", True), ("Mairie (EXEMPLE)", "Horaires des fêtes", False),
        ("Claire", "Repas de dimanche", False), ("Espace 19", "Prochain atelier", False)]
def inbox(d, rows=MSGS, new_bold=True):
    for i, (who, subj, att) in enumerate(rows):
        y = TOP + 20 + i * ROW_H
        d.rectangle([LIST_X, y, BX + BW - 20, y + ROW_H - 4], fill=(255, 255, 255) if (i or not new_bold) else (246, 248, 255))
        d.line([LIST_X, y + ROW_H - 4, BX + BW - 20, y + ROW_H - 4], fill=(225, 228, 235), width=1)
        fw = "b" if (i == 0 and new_bold) else "r"
        d.text((LIST_X + 20, y + 16), who, font=F(20, fw), fill=INK)
        d.text((LIST_X + 300, y + 16), subj, font=F(20, fw), fill=INK)
        if att: clip_icon(d, BX + BW - 70, y + 27, 1.0)

def composer(d, fill=1.0, chip=False):
    x0, y0, x1, y1 = COMP
    d.rounded_rectangle([x0 + 5, y0 + 6, x1 + 5, y1 + 6], 10, fill=(120, 125, 140))
    d.rounded_rectangle(COMP, 10, fill=(255, 255, 255), outline=(140, 145, 160), width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 44], 10, fill=(60, 66, 84)); d.rectangle([x0, y0 + 30, x1, y0 + 44], fill=(60, 66, 84))
    d.text((x0 + 18, y0 + 10), "Nouveau message", font=F(19, "s"), fill=(255, 255, 255))
    vals = [("À", "paul.martin@exemple.fr"), ("Objet", "Ma photo")]
    for k, (lab, v) in enumerate(vals):
        y = y0 + 58 + k * 50
        d.text((x0 + 18, y + 8), lab, font=F(19), fill=GRIS)
        n = int(len(v) * max(0, min(1, fill * 3 - k)))
        d.text((x0 + 90, y + 8), v[:n], font=F(19), fill=INK)
        d.line([x0 + 14, y + 42, x1 - 14, y + 42], fill=(225, 228, 235), width=1)
    body = "Bonjour Paul, voici la photo."
    n = int(len(body) * max(0, min(1, fill * 3 - 2)))
    d.text((x0 + 18, y0 + 170), body[:n], font=F(19), fill=INK)
    if chip:
        d.rounded_rectangle(CHIP, 8, fill=(242, 244, 248), outline=(170, 175, 190), width=2)
        garden(d, (CHIP[0] + 8, CHIP[1] + 7, CHIP[0] + 48, CHIP[3] - 7))
        d.text((CHIP[0] + 58, CHIP[1] + 10), "photo_jardin.jpg", font=F(18, "s"), fill=INK)
    d.rounded_rectangle(SEND, 20, fill=BLEU); d.text((SEND[0] + 24, SEND[1] + 8), "Envoyer", font=F(20, "b"), fill=(255, 255, 255))
    clip_icon(d, *R.center(CLIP), 1.1)

def dialog(d):
    x0, y0, x1, y1 = DLG
    d.rounded_rectangle([x0 + 6, y0 + 8, x1 + 6, y1 + 8], 10, fill=(90, 95, 110))
    d.rounded_rectangle(DLG, 10, fill=(250, 250, 252), outline=(130, 135, 150), width=2)
    d.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 44], fill=(232, 235, 242))
    d.text((x0 + 18, y0 + 12), "Les dossiers de votre ordinateur", font=F(18, "s"), fill=INK)
    for i, n in enumerate(R.NAV_ITEMS[1:6]):
        y = y0 + 64 + i * 46
        if n == "Images": d.rounded_rectangle([x0 + 10, y - 6, x0 + 180, y + 32], 6, fill=(214, 228, 248))
        R.folder_icon(d, x0 + 18, y, 0.3); d.text((x0 + 54, y + 2), n, font=F(17), fill=INK)
    for i, (n, kind) in enumerate(TILES):
        r = tile_rect(i); doc_icon(d, r, kind)
        f = F(14); tw = d.textlength(n, font=f); d.text(((r[0] + r[2]) / 2 - tw / 2, r[3] - 30), n, font=f, fill=INK)

def message_view(d, hover=False):
    x0 = LIST_X; y0 = TOP + 20
    d.text((x0 + 20, y0 + 6), "Photos du jardin", font=F(28, "b"), fill=INK)
    d.ellipse([x0 + 20, y0 + 60, x0 + 64, y0 + 104], fill=(120, 150, 200)); d.text((x0 + 33, y0 + 68), "P", font=F(22, "b"), fill=(255, 255, 255))
    d.text((x0 + 80, y0 + 62), "Paul Martin", font=F(20, "b"), fill=INK)
    d.text((x0 + 80, y0 + 88), "à moi", font=F(16), fill=GRIS)
    d.text((x0 + 20, y0 + 130), "Bonjour ! Voici une photo de mon jardin. À bientôt, Paul", font=F(20), fill=INK)
    d.line([x0 + 20, y0 + 225, x0 + 700, y0 + 225], fill=(225, 228, 235), width=1)
    d.rounded_rectangle(THUMB, 8, fill=(255, 255, 255), outline=(170, 175, 190), width=2)
    garden(d, (THUMB[0] + 6, THUMB[1] + 6, THUMB[2] - 6, THUMB[3] - 38))
    d.text((THUMB[0] + 12, THUMB[3] - 30), "photo_jardin.jpg", font=F(16, "s"), fill=INK)
    if hover:
        d.rounded_rectangle(DLBTN, 8, fill=(40, 44, 60))
        cx, cy = R.center(DLBTN)
        d.line([cx, cy - 12, cx, cy + 8], fill=(255, 255, 255), width=4); d.line([cx - 9, cy, cx, cy + 9, cx + 9, cy], fill=(255, 255, 255), width=4)
        d.line([cx - 11, cy + 14, cx + 11, cy + 14], fill=(255, 255, 255), width=3)

def screen(state="inbox", **kw):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if state is None: return im
    window(d); sidebar(d)
    if state == "inbox": inbox(d, **{k: v for k, v in kw.items() if k in ("rows", "new_bold")})
    if state == "compose": inbox(d); composer(d, kw.get("fill", 1.0), kw.get("chip", False))
    if state == "dialog": inbox(d); composer(d, 1.0, False); dialog(d)
    if state == "msg": message_view(d, kw.get("hover", False))
    if state == "preview":
        message_view(d); ov = Image.new("RGB", (W, H), (20, 22, 28)); im = Image.blend(im, ov, 0.85); d = ImageDraw.Draw(im)
        garden(d, (290, 110, 990, 560)); d.text((300, 80), "photo_jardin.jpg", font=F(20, "s"), fill=(255, 255, 255))
    return im

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None, double=False):
    c = R.center(r); tc = 0.6 * D
    im = (after if t >= tc + 0.3 else before)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    if double: R.ripple(d, c[0], c[1], (t - tc - 0.25) / 0.6)
    if double and tc - 0.4 < t < tc + 1.2: O.label(d, "double-clic", (c[0], r[3] + 40))
    R.caption(d, cap); return im

def envelope(d, cx, cy, s=1.0, open_=True):
    w, h = 220 * s, 140 * s
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=(245, 225, 180), outline=(150, 120, 70), width=3)
    if open_: d.polygon([(cx - w / 2, cy - h / 2), (cx, cy - h / 2 - 80 * s), (cx + w / 2, cy - h / 2)], fill=(235, 210, 160), outline=(150, 120, 70))
    d.line([cx - w / 2, cy + h / 2, cx, cy + 5 * s, cx + w / 2, cy + h / 2], fill=(150, 120, 70), width=3)

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Joindre et lire une pièce jointe", ["Aide-mémoire n° 19 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); envelope(d, W / 2 - 40, 380, 0.9); clip_icon(d, W / 2 + 90, 360, 3.0, VIO, 3); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); cx, cy = W / 2, 400
        envelope(d, cx, cy, 1.4)
        q = R.ease((p - 0.15) / 0.3); y = 160 + 170 * q
        d.rectangle([cx - 120, y, cx - 10, y + 140], fill=(255, 255, 255), outline=INK, width=2)
        for k in range(5): d.line([cx - 110, y + 20 + k * 22, cx - 20, y + 20 + k * 22], fill=GRIS, width=2)
        if p > 0.35:
            q2 = R.ease((p - 0.35) / 0.3); y2 = 160 + 170 * q2
            garden(d, (cx + 10, y2, cx + 130, y2 + 90)); d.rectangle([cx + 10, y2, cx + 130, y2 + 90], outline=INK, width=2)
        envelope(d, cx, cy, 1.4, open_=False) if p > 0.7 else None
        if p > 0.15: O.label(d, "la lettre = le message", (300, 200))
        if p > 0.4: O.label(d, "la photo = la pièce jointe", (980, 200))
        R.caption(d, cap); return im
    if sid == "nouveau":
        tc = 0.4 * D
        if t < tc + 0.3:
            return act(lambda: screen("inbox"), lambda: screen("compose", fill=0), NEW, (W / 2, H / 2), t, tc / 0.6, cap, place=(500, 400))
        im = screen("compose", fill=(t - tc - 0.3) / (0.45 * D)); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "trombone":
        return act(lambda: screen("compose"), lambda: screen("dialog"), CLIP, R.center(NEW), t, D, cap, place=(400, 380))
    if sid == "choisir":
        if t < 0.3 * D:
            im = screen("dialog"); d = ImageDraw.Draw(im)
            if p > 0.08: O.label(d, "les dossiers de l'ordinateur", (W / 2, DLG[3] + 40))
            R.caption(d, cap); return im
        return act(lambda: screen("dialog"), lambda: screen("compose", chip=True), PHOTO, (DLG[0] + 100, DLG[3] - 40), t - 0.3 * D, 0.7 * D, cap,
                   show_loupe=False, double=True)
    if sid == "joint":
        if t < 0.45 * D:
            im = screen("compose", chip=True); clean = im.copy(); d = ImageDraw.Draw(im)
            if p > 0.05:
                R.highlight(d, CHIP, t); R.loupe(im, CHIP, place=(400, 400), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        tt = t - 0.45 * D; DD = 0.4 * D
        if tt < DD:
            return act(lambda: screen("compose", chip=True), lambda: screen("inbox"), SEND, R.center(CHIP), tt, DD, cap, place=(400, 400))
        im = screen("inbox"); d = ImageDraw.Draw(im); O.label(d, "Bravo ! Le message est parti.", (W / 2, 470)); R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "recu":
        clipr = (BX + BW - 90, ROW0[1] + 4, BX + BW - 50, ROW0[3] - 8)
        if t < 0.45 * D:
            im = screen("inbox"); clean = im.copy(); d = ImageDraw.Draw(im)
            if p > 0.08:
                R.highlight(d, clipr, t); R.arrow(d, clipr, t); R.loupe(im, clipr, place=(640, 420), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        return act(lambda: screen("inbox"), lambda: screen("msg"), (LIST_X + 10, ROW0[1] + 6, LIST_X + 520, ROW0[3] - 8), (640, 450), t - 0.45 * D, 0.55 * D, cap, show_loupe=False)
    if sid == "lire":
        if t < 0.3 * D:
            im = screen("msg"); d = ImageDraw.Draw(im)
            if p > 0.08: R.highlight(d, THUMB, t); O.label(d, "la vignette", (R.center(THUMB)[0] + 330, R.center(THUMB)[1]))
            R.caption(d, cap); return im
        tt = t - 0.3 * D; DD = 0.45 * D
        if tt < DD:
            return act(lambda: screen("msg"), lambda: screen("preview"), THUMB, (900, 300), tt, DD, cap, show_loupe=False)
        im = screen("preview"); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "garder":
        if t < 0.3 * D:
            im = screen("msg", hover=t > 0.2 * D); d = ImageDraw.Draw(im)
            R.cursor(d, *R.move(t, 0.02 * D, 0.2 * D, (900, 300), R.center(THUMB))); R.caption(d, cap); return im
        tt = t - 0.3 * D; DD = 0.45 * D
        if tt < DD:
            return act(lambda: screen("msg", hover=True), lambda: screen("msg", hover=True), DLBTN, R.center(THUMB), tt, DD, cap, place=(900, 380))
        im = screen("msg", hover=True); d = ImageDraw.Draw(im)
        d.rounded_rectangle([760, 300, 1160, 440], 14, fill=(255, 250, 230), outline=YEL, width=6)
        R.folder_icon(d, 785, 330, 0.8); d.text((880, 330), "Téléchargements", font=F(24, "b"), fill=INK)
        d.text((880, 375), "photo_jardin.jpg", font=F(20), fill=INK)
        R.caption(d, cap); return im
    if sid == "prudence":
        rows = [("Inconnu (EXEMPLE)", "Vous avez gagné ! Ouvrez vite", True)] + MSGS[1:]
        im = screen("inbox", rows=rows); d = ImageDraw.Draw(im)
        if p > 0.1 and (t % 0.7) < 0.5:
            d.rounded_rectangle([ROW0[0] - 8, ROW0[1] - 8, ROW0[2] + 8, ROW0[3] + 4], 10, outline=ROUGE, width=8)
        if p > 0.25:
            cx, cy = W / 2, 430
            d.polygon([(cx, cy - 90), (cx - 100, cy + 80), (cx + 100, cy + 80)], fill=(255, 122, 89), outline=(120, 30, 20))
            f = F(110, "b"); d.text((cx - 18, cy - 60), "!", font=f, fill=(255, 255, 255))
            O.label(d, "Un inconnu ? Je n'ouvre pas.", (cx, cy + 120))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Envoyez-vous une photo", "à vous-même, en pièce jointe.", "Puis ouvrez-la."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Le trombone, la photo, Envoyer.", "Puis ouvrez le message reçu."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 5; k = min(4, int(t // q)); tt = t - k * q
        if k == 0: return act(lambda: screen("inbox"), lambda: screen("compose"), NEW, (W / 2, H / 2), tt, q, cap, show_loupe=False)
        if k == 1: return act(lambda: screen("compose"), lambda: screen("dialog"), CLIP, R.center(NEW), tt, q, cap, show_loupe=False)
        if k == 2: return act(lambda: screen("dialog"), lambda: screen("compose", chip=True), PHOTO, R.center(CLIP), tt, q, cap, show_loupe=False, double=True)
        if k == 3: return act(lambda: screen("compose", chip=True), lambda: screen("msg"), SEND, R.center(PHOTO), tt, q, cap, show_loupe=False)
        return act(lambda: screen("msg"), lambda: screen("preview"), THUMB, R.center(SEND), tt, q, cap, show_loupe=False)
    if sid == "resume":
        return R.card("À retenir", ["Le trombone = la pièce jointe", "Double-clic sur le document, puis Envoyer", "Pour lire : cliquez sur la vignette", "Jamais de pièce jointe d'un inconnu"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
