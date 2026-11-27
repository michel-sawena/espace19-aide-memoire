"""Vidéo « 10 - Créer, enregistrer, fermer un fichier texte » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_10.py script.json durations.json out.mp4
        python3 render_10.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, Explorateur, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes),
../01-ordinateur/render_01_ordinateur.py (pièce, étiquettes) et ../04-arborescence/render_04.py (icône de fichier).
Libellés écrits tels quels : « Bloc-notes », « Fichier », « Enregistrer », « Enregistrer sous », « Nom de fichier »,
« Documents », « Ctrl + S » (voir sources_10.md). Non écrits : nom d'un document neuf, question posée à la fermeture.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../04-arborescence"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_04 as Q
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); GRIS = (215, 219, 226)
TEXTE = ["du pain", "du lait", "des pommes"]
NOM = "Courses"

# ---------- géométrie ----------
NX, NY, NW, NH = 170, 96, 940, 500          # fenêtre Bloc-notes
TAB = (NX + 60, NY + 6, NX + 300, NY + 42)
CLOSE = (NX + NW - 54, NY + 2, NX + NW - 4, NY + 42)
MENU_FICHIER = (NX + 10, NY + 50, NX + 96, NY + 84)
TXT_ZONE = (NX + 10, NY + 96, NX + NW - 10, NY + NH - 10)
DROP = (NX + 10, NY + 88, NX + 300, NY + 88 + 7 * 40 + 12)
def drop_item(i): return (DROP[0] + 6, DROP[1] + 6 + i * 40, DROP[2] - 6, DROP[1] + 6 + i * 40 + 36)
ITEM_ENR = drop_item(3)

SM = (330, 120, 950, H - R.TB_H - 12)        # menu Démarrer
SEARCH = (SM[0] + 30, SM[1] + 26, SM[2] - 30, SM[1] + 78)
RESULT = (SM[0] + 30, SM[1] + 130, SM[2] - 30, SM[1] + 210)
START = R.rect_of("explorer"); _sx, _sy = R.taskbar_icons()["start"]; START = (_sx - 24, _sy - 22, _sx + 24, _sy + 22)

DX, DY, DW, DH = 190, 100, 900, 500         # fenêtre d'enregistrement
DNAV = ["Accueil", "Bureau", "Téléchargements", "Documents", "Images"]
def dnav(i): y = DY + 60 + i * 46; return (DX + 12, y, DX + 210, y + 40)
D_DOC = dnav(3)
NAME_FIELD = (DX + 230, DY + DH - 130, DX + DW - 24, DY + DH - 90)
BTN_ENR = (DX + DW - 330, DY + DH - 62, DX + DW - 180, DY + DH - 18)

def croix(d, cx, cy, r=8, w=3, col=(40, 40, 40)):
    d.line([cx - r, cy - r, cx + r, cy + r], fill=col, width=w); d.line([cx - r, cy + r, cx + r, cy - r], fill=col, width=w)

def notepad_icon(d, x, y, s=1.0):
    d.rounded_rectangle([x, y, x + 34 * s, y + 40 * s], 4, fill=(255, 255, 255), outline=(60, 120, 200), width=2)
    d.rectangle([x, y, x + 34 * s, y + 8 * s], fill=(60, 120, 200))
    for k in range(3): d.line([x + 6 * s, y + (16 + k * 8) * s, x + 28 * s, y + (16 + k * 8) * s], fill=(120, 130, 150), width=2)

# ---------- écrans ----------
def desktop(start=None, typed=""):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if start:
        d.rounded_rectangle([SM[0] + 5, SM[1] + 7, SM[2] + 5, SM[3] + 7], 14, fill=(10, 30, 70))
        d.rounded_rectangle(SM, 14, fill=(243, 245, 250), outline=(170, 175, 190), width=2)
        d.rounded_rectangle(SEARCH, 24, fill=(255, 255, 255), outline=(0, 103, 192) if typed else (180, 185, 195), width=2)
        d.ellipse([SEARCH[0] + 18, SEARCH[1] + 16, SEARCH[0] + 34, SEARCH[1] + 32], outline=(60, 60, 60), width=3)
        d.text((SEARCH[0] + 52, SEARCH[1] + 12), typed, font=F(22), fill=(20, 20, 20))
        if typed and len(typed) >= 5:
            d.rounded_rectangle(RESULT, 10, fill=(220, 232, 248) if start == "hover" else (255, 255, 255))
            notepad_icon(d, RESULT[0] + 20, RESULT[1] + 20)
            d.text((RESULT[0] + 76, RESULT[1] + 24), "Bloc-notes", font=F(24, "s"), fill=(20, 20, 20))
            for i in range(3): d.rounded_rectangle([SM[0] + 40, RESULT[3] + 30 + i * 50, SM[0] + 380, RESULT[3] + 48 + i * 50], 6, fill=GRIS)
        else:
            for i in range(6):
                x = SM[0] + 50 + (i % 3) * 190; y = SM[1] + 130 + (i // 3) * 120
                d.rounded_rectangle([x, y, x + 60, y + 60], 10, fill=GRIS); d.rounded_rectangle([x - 10, y + 72, x + 70, y + 86], 5, fill=GRIS)
    return im

def notepad(lines=0, name=None, menu=False, chars=None, base=None):
    im = base.copy() if base is not None else R.screen({"window": False}); d = ImageDraw.Draw(im)
    d.rounded_rectangle([NX + 6, NY + 8, NX + NW + 6, NY + NH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([NX, NY, NX + NW, NY + NH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([NX, NY, NX + NW, NY + 46], 10, fill=(232, 236, 244)); d.rectangle([NX, NY + 26, NX + NW, NY + 46], fill=(232, 236, 244))
    notepad_icon(d, NX + 16, NY + 8, 0.7)
    d.rounded_rectangle(TAB, 8, fill=(255, 255, 255))
    if name: d.text((TAB[0] + 14, TAB[1] + 7), name, font=F(18, "s"), fill=(20, 20, 20))
    else: d.rounded_rectangle([TAB[0] + 14, TAB[1] + 13, TAB[0] + 120, TAB[1] + 25], 5, fill=GRIS)
    croix(d, TAB[2] - 18, (TAB[1] + TAB[3]) / 2, 5, 2, (90, 90, 90))
    d.line([NX + NW - 140, NY + 23, NX + NW - 124, NY + 23], fill=(60, 60, 60), width=2)
    d.rectangle([NX + NW - 94, NY + 15, NX + NW - 78, NY + 31], outline=(60, 60, 60), width=2)
    croix(d, *R.center(CLOSE), 9, 3)
    d.rectangle([NX + 2, NY + 46, NX + NW - 2, NY + 88], fill=(250, 250, 252))
    if menu: d.rounded_rectangle(MENU_FICHIER, 6, fill=(220, 232, 248))
    d.text((MENU_FICHIER[0] + 10, MENU_FICHIER[1] + 6), "Fichier", font=F(19, "s"), fill=(20, 20, 20))
    for i in range(2): d.rounded_rectangle([NX + 120 + i * 100, NY + 62, NX + 190 + i * 100, NY + 74], 5, fill=GRIS)
    d.line([NX + 2, NY + 89, NX + NW - 2, NY + 89], fill=(225, 228, 235), width=2)
    txt = "\n".join(TEXTE[:lines])
    if chars is not None: txt = txt[:chars]
    y = TXT_ZONE[1] + 14
    for ln in (txt.split("\n") if txt else []):
        d.text((TXT_ZONE[0] + 16, y), ln, font=F(26), fill=(20, 20, 20)); y += 40
    if lines or chars is not None:
        last = txt.split("\n")[-1] if txt else ""
        cx = TXT_ZONE[0] + 18 + d.textlength(last, font=F(26)); cy = y - 40 if txt else y
        d.line([cx, cy + 2, cx, cy + 32], fill=(0, 0, 0), width=2)
    if menu:
        d.rounded_rectangle(DROP, 8, fill=(252, 252, 254), outline=(180, 185, 195), width=2)
        for i in range(7):
            r = drop_item(i)
            if i == 3: d.rounded_rectangle(r, 5, fill=(225, 235, 250) if menu == "hover" else (252, 252, 254)); d.text((r[0] + 14, r[1] + 7), "Enregistrer", font=F(19, "s"), fill=(20, 20, 20))
            elif i == 4: d.text((r[0] + 14, r[1] + 7), "Enregistrer sous", font=F(19), fill=(20, 20, 20))
            else: d.rounded_rectangle([r[0] + 14, r[1] + 12, r[0] + 150, r[1] + 24], 5, fill=GRIS)
    return im

def save_dialog(docs=False, typed=""):
    im = notepad(3); d = ImageDraw.Draw(im)
    d.rounded_rectangle([DX + 8, DY + 10, DX + DW + 8, DY + DH + 10], 12, fill=(10, 30, 70))
    d.rounded_rectangle([DX, DY, DX + DW, DY + DH], 12, fill=(255, 255, 255), outline=(140, 150, 170), width=2)
    d.rounded_rectangle([DX, DY, DX + DW, DY + 44], 12, fill=(232, 236, 244)); d.rectangle([DX, DY + 24, DX + DW, DY + 44], fill=(232, 236, 244))
    croix(d, DX + DW - 30, DY + 22, 7, 2, (60, 60, 60))
    for i, it in enumerate(DNAV):
        r = dnav(i)
        if docs and it == "Documents": d.rounded_rectangle(r, 6, fill=(204, 228, 247))
        R.folder_icon(d, r[0] + 8, r[1] + 9, 0.23, (120, 160, 220) if it == "Accueil" else (250, 200, 70))
        d.text((r[0] + 42, r[1] + 8), it, font=F(18), fill=(20, 20, 20))
    d.line([DX + 222, DY + 50, DX + 222, DY + DH - 150], fill=(225, 228, 235), width=2)
    if docs:
        d.text((DX + 250, DY + 58), "Documents", font=F(22, "b"), fill=(30, 30, 30))
        for i, n in enumerate(["Lettres", "Factures"]):
            x = DX + 260 + i * 160; R.folder_icon(d, x, DY + 110, 0.9)
            tw = d.textlength(n, font=F(17)); d.text((x + 40 - tw / 2, DY + 180), n, font=F(17), fill=(20, 20, 20))
    else:
        for i in range(3): d.rounded_rectangle([DX + 250, DY + 70 + i * 50, DX + 650, DY + 90 + i * 50], 6, fill=(243, 245, 249))
    d.rectangle([DX + 2, DY + DH - 150, DX + DW - 2, DY + DH - 2], fill=(246, 248, 252))
    d.text((DX + 30, NAME_FIELD[1] + 8), "Nom de fichier :", font=F(19, "s"), fill=(20, 20, 20))
    d.rounded_rectangle(NAME_FIELD, 5, fill=(255, 255, 255), outline=(0, 103, 192) if typed else (170, 175, 185), width=2)
    d.text((NAME_FIELD[0] + 12, NAME_FIELD[1] + 7), typed, font=F(20), fill=(20, 20, 20))
    if typed is not None and docs:
        cx = NAME_FIELD[0] + 14 + d.textlength(typed, font=F(20)); d.line([cx, NAME_FIELD[1] + 8, cx, NAME_FIELD[3] - 8], fill=(0, 0, 0), width=2)
    d.rounded_rectangle(BTN_ENR, 6, fill=(0, 103, 192))
    tw = d.textlength("Enregistrer", font=F(19, "s")); d.text(((BTN_ENR[0] + BTN_ENR[2]) / 2 - tw / 2, BTN_ENR[1] + 10), "Enregistrer", font=F(19, "s"), fill=(255, 255, 255))
    d.rounded_rectangle([BTN_ENR[2] + 14, BTN_ENR[1], BTN_ENR[2] + 154, BTN_ENR[3]], 6, fill=(255, 255, 255), outline=(170, 175, 185), width=2)
    d.rounded_rectangle([BTN_ENR[2] + 44, BTN_ENR[1] + 16, BTN_ENR[2] + 124, BTN_ENR[1] + 28], 5, fill=GRIS)
    return im

FILE_POS = 2
def explorer_docs(sel=False):
    im = R.screen({"window": True, "view": "Documents", "folders": ["Lettres", "Factures"]}); d = ImageDraw.Draw(im)
    r = R.rect_of(f"folder:{FILE_POS}"); Q.file_icon(d, r[0] + 33, r[1] + 4)
    tw = d.textlength(NOM, font=F(17)); d.text(((r[0] + r[2]) / 2 - tw / 2, r[1] + 95), NOM, font=F(17), fill=(20, 20, 20))
    if sel: d.rounded_rectangle(r, 8, outline=(0, 103, 192), width=3)
    return im
FILE_R = R.rect_of(f"folder:{FILE_POS}")

def key_combo(d, t, k1="Ctrl", k2="S"):
    for i, k in enumerate((k1, k2)):
        x = W / 2 - 230 + i * 260; y = H / 2 - 40; pressed = (t % 1.6) > 0.8; off = 8 if pressed else 0
        d.rounded_rectangle([x + 6, y + 10, x + 206, y + 130], 16, fill=(60, 60, 70))
        d.rounded_rectangle([x, y + off, x + 200, y + 120 + off], 16, fill=(245, 245, 248), outline=(80, 80, 90), width=3)
        tw = d.textlength(k, font=F(44, "b")); d.text((x + 100 - tw / 2, y + 32 + off), k, font=F(44, "b"), fill=(20, 20, 20))
        if (t % 0.7) < 0.47: d.rounded_rectangle([x - 12, y - 12, x + 212, y + 142], 18, outline=YEL, width=9)
    d.text((W / 2 - 15, H / 2), "+", font=F(56, "b"), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))

# ---------- action générique : cliquer sur r ----------
def act(sb, sa, r, start, t, D, cap, loupe=True, double=False, place=None):
    """sb/sa : fonctions sans argument qui dessinent l'écran avant / après le clic."""
    c = R.center(r); tc = 0.6 * D
    after = t >= tc + (0.5 if double else 0.3)
    im = (sa if after else sb)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if not after:
        R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    if double: R.ripple(d, c[0], c[1], (t - tc - 0.25) / 0.6)
    R.caption(d, cap); return im

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Créer, enregistrer, fermer", ["un fichier texte", "Aide-mémoire n° 10 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); Q.file_icon(d, W / 2 - 40, 330, 1.3); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im)
        d.rectangle([250, 170, 520, 520], fill=(255, 255, 255), outline=(150, 150, 160), width=3)
        for k in range(3):
            if p > 0.15 + k * 0.1: d.text((280, 210 + k * 50), TEXTE[k], font=F(30), fill=INK)
        if p > 0.1: O.label(d, "j'écris", (385, 130))
        x = 820 - 250 * R.ease((p - 0.55) / 0.2)
        R.folder_icon(d, 760, 280, 2.0)
        if p > 0.55:
            d.rectangle([x, 230, x + 120, 380], fill=(255, 255, 255), outline=(150, 150, 160), width=3) if p < 0.75 else None
            O.label(d, "je range", (850, 230))
        if p > 0.8: O.label(d, "je retrouve", (850, 470))
        R.caption(d, cap); return im
    if sid == "demarrer":
        return act(lambda: desktop(), lambda: desktop(True), START, (W / 2 + 200, H / 2), t, D, cap, place=(W / 2, 330))
    if sid == "taper":
        if p < 0.45:
            n = int(len("Bloc-notes") * R.ease(p / 0.4)); im = desktop(True, "Bloc-notes"[:n]); d = ImageDraw.Draw(im)
            R.highlight(d, SEARCH, t); R.caption(d, cap); return im
        return act(lambda: desktop("hover", "Bloc-notes"), lambda: notepad(), RESULT, (W / 2 + 300, H / 2 + 100), (t - 0.45 * D), 0.55 * D, cap, loupe=False)
    if sid == "page":
        if p < 0.3: return act(lambda: notepad(), lambda: notepad(chars=0), TXT_ZONE, (W - 200, H - 200), t, 0.3 * D, cap, loupe=False)
        n = int(len("\n".join(TEXTE)) * R.ease((p - 0.3) / 0.45)); im = notepad(3, chars=n); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "fichier":
        if p < 0.5: return act(lambda: notepad(3), lambda: notepad(3, menu=True), MENU_FICHIER, (W / 2, H / 2 + 100), t, 0.5 * D, cap, place=(850, 330))
        return act(lambda: notepad(3, menu="hover"), lambda: save_dialog(), ITEM_ENR, R.center(MENU_FICHIER), t - 0.5 * D, 0.5 * D, cap, place=(850, 330))
    if sid == "dossier":
        return act(lambda: save_dialog(), lambda: save_dialog(True), D_DOC, (W / 2 + 200, H / 2), t, D, cap, place=(850, 300))
    if sid == "nom":
        if p < 0.5:
            n = int(len(NOM) * R.ease((p - 0.1) / 0.3)); im = save_dialog(True, NOM[:max(0, n)]); clean = im.copy(); d = ImageDraw.Draw(im)
            R.highlight(d, NAME_FIELD, t)
            if p > 0.1: R.loupe(im, (NAME_FIELD[0] - 200, NAME_FIELD[1], NAME_FIELD[0] + 200, NAME_FIELD[3]), place=(800, 260), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        return act(lambda: save_dialog(True, NOM), lambda: notepad(3, name=NOM + ".txt"), BTN_ENR, R.center(NAME_FIELD), t - 0.5 * D, 0.5 * D, cap, place=(700, 260))
    if sid == "enregistre":
        im = notepad(3, name=NOM + ".txt"); clean = im.copy(); d = ImageDraw.Draw(im); R.highlight(d, TAB, t)
        if p > 0.2: R.loupe(im, (TAB[0], TAB[1], TAB[0] + 130, TAB[3]), place=(850, 360), clean=clean); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "raccourci":
        im = notepad(3, name=NOM + ".txt"); d = ImageDraw.Draw(im); d.rectangle([0, 0, W, H], fill=None)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 120)); im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(im)
        key_combo(d, t); R.caption(d, cap); return im
    if sid == "fermer":
        return act(lambda: notepad(3, name=NOM + ".txt"), lambda: desktop(), CLOSE, (W / 2, H / 2), t, D, cap, place=(850, 330))
    if sid == "question":
        im = R.card("Pas de panique", ["Une question en fermant ?", "Le texte n'est pas enregistré.", "Choisissez d'enregistrer."], "Enregistrez toujours avant de fermer.")
        return im
    if sid == "retrouver":
        seg = [(lambda: desktop(), lambda: R.screen({"window": True, "view": "Accueil", "folders": []}), R.rect_of("explorer"), (W / 2 + 200, H / 2), 0.0, 0.3, False),
               (lambda: R.screen({"window": True, "view": "Accueil", "folders": []}), lambda: explorer_docs(), R.rect_of("nav:Documents"), R.center(R.rect_of("explorer")), 0.3, 0.6, False),
               (lambda: explorer_docs(True), lambda: notepad(3, name=NOM + ".txt"), FILE_R, R.center(R.rect_of("nav:Documents")), 0.6, 1.01, True)]
        for sb, sa, r, s, x0, x1, dbl in seg:
            if x0 * D <= t < x1 * D: return act(sb, sa, r, s, t - x0 * D, (x1 - x0) * D, cap, loupe=(x0 == 0.6), double=dbl, place=(400, 330))
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "exercice":
        return R.card("Exercice", ["Ouvrez le Bloc-notes,", "écrivez votre prénom.", "Enregistrez dans « Documents »,", "puis fermez."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Écrivez, enregistrez,", "puis fermez."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        seg = [(lambda: desktop(), lambda: desktop(True, "Bloc-notes"), START, (W / 2, H / 2), 0.0, 0.15),
               (lambda: desktop("hover", "Bloc-notes"), lambda: notepad(3), RESULT, R.center(START), 0.15, 0.3),
               (lambda: notepad(3), lambda: notepad(3, menu=True), MENU_FICHIER, R.center(RESULT), 0.3, 0.42),
               (lambda: notepad(3, menu="hover"), lambda: save_dialog(), ITEM_ENR, R.center(MENU_FICHIER), 0.42, 0.54),
               (lambda: save_dialog(), lambda: save_dialog(True, NOM), D_DOC, R.center(ITEM_ENR), 0.54, 0.68),
               (lambda: save_dialog(True, NOM), lambda: notepad(3, name=NOM + ".txt"), BTN_ENR, R.center(D_DOC), 0.68, 0.84),
               (lambda: notepad(3, name=NOM + ".txt"), lambda: desktop(), CLOSE, R.center(BTN_ENR), 0.84, 1.01)]
        for sb, sa, r, s, x0, x1 in seg:
            if x0 * D <= t < x1 * D: return act(sb, sa, r, s, t - x0 * D, (x1 - x0) * D, cap, loupe=False)
    if sid == "resume":
        return R.card("À retenir", ["1. J'écris", "2. J'enregistre : « Fichier », « Enregistrer »", "3. Je ferme : la croix", "Je retrouve : « Documents »"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
