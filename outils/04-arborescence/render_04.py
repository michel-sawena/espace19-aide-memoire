"""Vidéo « 04 - Comprendre l'arborescence » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_04.py script.json durations.json out.mp4
        python3 render_04.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, fenêtre de l'Explorateur, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes)
et ../01-ordinateur/render_01_ordinateur.py (pièce, étiquettes).
Libellés écrits tels quels : « Explorateur de fichiers », noms du volet de gauche, « Documents » (voir sources_04.md).
La flèche « monter » est dessinée sans nom (libellé non confirmé).
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); BOIS = (176, 120, 70); BOIS2 = (140, 90, 50)
DOSSIERS = ["Lettres", "Factures", "Recettes"]
FICHIERS = ["Lettre à Paul", "Mairie", "Banque"]

# ---------- barre d'adresse (dessinée sur la ligne de commandes) ----------
CMD_Y, WX, WW = R.CMD_Y, R.WX, R.WW
UP = (WX + 96, CMD_Y + 10, WX + 132, CMD_Y + 42)
ADDR = (WX + 150, CMD_Y + 8, WX + WW - 20, CMD_Y + 44)
_d0 = ImageDraw.Draw(Image.new("RGB", (10, 10)))
def seg_rects(path):
    """Rectangles des noms dans la barre d'adresse."""
    x = ADDR[0] + 40; out = []
    for name in path:
        x += 26; tw = _d0.textlength(name, font=F(19, "s"))
        out.append((x - 6, ADDR[1] + 3, x + tw + 6, ADDR[3] - 3)); x += tw + 8
    return out

def addr_bar(d, path, hover=None):
    d.rectangle([WX + 2, CMD_Y, WX + WW - 2, CMD_Y + 52], fill=(246, 248, 252))
    for i, x in enumerate((WX + 22, WX + 58)):        # flèches gauche / droite (dessin seul)
        y = CMD_Y + 26; s = -1 if i == 0 else 1
        d.line([x - 8 * s, y, x + 8 * s, y], fill=(110, 110, 120), width=3)
        d.line([x + 2 * s, y - 7, x + 9 * s, y, x + 2 * s, y + 7], fill=(110, 110, 120), width=3)
    cx, cy = R.center(UP)
    d.line([cx, cy + 9, cx, cy - 9], fill=(40, 40, 50), width=3); d.line([cx - 7, cy - 2, cx, cy - 9, cx + 7, cy - 2], fill=(40, 40, 50), width=3)
    d.rounded_rectangle(ADDR, 6, fill=(255, 255, 255), outline=(190, 195, 205), width=2)
    R.folder_icon(d, ADDR[0] + 10, ADDR[1] + 6, 0.25)
    for i, (name, r) in enumerate(zip(path, seg_rects(path))):
        if hover == i: d.rounded_rectangle(r, 5, fill=(220, 232, 248))
        d.text((r[0] - 20, r[1] + 4), "›", font=F(19, "b"), fill=(90, 90, 100))
        d.text((r[0] + 6, r[1] + 4), name, font=F(19, "s"), fill=(20, 20, 20))

def file_icon(d, x, y, s=1.0):
    w, h = 64 * s, 82 * s
    d.polygon([(x, y), (x + w - 18 * s, y), (x + w, y + 18 * s), (x + w, y + h), (x, y + h)], fill=(255, 255, 255), outline=(120, 130, 150))
    d.polygon([(x + w - 18 * s, y), (x + w - 18 * s, y + 18 * s), (x + w, y + 18 * s)], fill=(215, 222, 235), outline=(120, 130, 150))
    for k in range(4): d.line([x + 10 * s, y + (32 + k * 12) * s, x + w - 10 * s, y + (32 + k * 12) * s], fill=(0, 103, 192), width=max(2, int(3 * s)))

def file_rect(i): return R.rect_of(f"folder:{i}")

# états : None = bureau seul ; "Accueil" ; "Documents" ; "Lettres"
def screen(view, hover=None, sel=None):
    if view is None: return R.screen({"window": False})
    if view == "Lettres":
        im = R.screen({"window": True, "view": "Lettres", "folders": []}); d = ImageDraw.Draw(im)
        for i, n in enumerate(FICHIERS):
            r = file_rect(i); file_icon(d, r[0] + 33, r[1] + 4)
            tw = d.textlength(n, font=F(17)); d.text(((r[0] + r[2]) / 2 - tw / 2, r[1] + 95), n, font=F(17), fill=(20, 20, 20))
        addr_bar(d, ["Documents", "Lettres"], hover)
    else:
        im = R.screen({"window": True, "view": view, "folders": DOSSIERS if view == "Documents" else []}); d = ImageDraw.Draw(im)
        addr_bar(d, ["Documents"] if view == "Documents" else ["Accueil"], hover)
    if sel is not None:
        r = R.rect_of(f"folder:{sel}"); d.rounded_rectangle(r, 8, outline=(0, 103, 192), width=3)
    return im

def act(vb, va, r, start, t, D, cap, show_loupe=True, double=False, hover=None, place=None):
    c = R.center(r); tc = 0.6 * D
    v = va if t >= tc + (0.5 if double else 0.3) else vb
    im = screen(v, hover=hover if v == vb else None); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3:
        R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    if double: R.ripple(d, c[0], c[1], (t - tc - 0.25) / 0.6)
    R.caption(d, cap); return im

# ---------- armoire et arbre ----------
def armoire(d, k_tiroir=0.0, k_chemise=0.0, x0=120, y0=110):
    """k_tiroir : 0 fermé → 1 ouvert ; k_chemise : 0 → 1 la chemise s'ouvre (feuilles visibles)."""
    d.rectangle([x0, y0, x0 + 300, y0 + 440], fill=BOIS, outline=BOIS2, width=6)
    for i in range(3):
        y = y0 + 30 + i * 135
        if i == 1 and k_tiroir > 0:
            off = 140 * k_tiroir
            d.rectangle([x0 + 20, y, x0 + 280, y + 110], fill=(70, 45, 25))
            d.polygon([(x0 + 20 + off, y + 10), (x0 + 280 + off, y + 10), (x0 + 280 + off, y + 120), (x0 + 20 + off, y + 120)], fill=(200, 145, 90), outline=BOIS2)
            for j in range(4):
                cx = x0 + 50 + off + j * 52
                d.rectangle([cx, y - 20, cx + 40, y + 40], fill=(240, 205, 120), outline=(190, 150, 70), width=2)
        else:
            d.rectangle([x0 + 20, y, x0 + 280, y + 110], fill=(200, 145, 90), outline=BOIS2, width=3)
        d.rounded_rectangle([x0 + 125, y + 48, x0 + 175, y + 62], 6, fill=(90, 60, 35))
    if k_chemise > 0:
        cx, cy = 820, 330
        d.polygon([(cx - 150, cy - 110), (cx, cy - 110), (cx, cy + 110), (cx - 150, cy + 110)], fill=(240, 205, 120), outline=(190, 150, 70))
        a = 150 * k_chemise
        d.polygon([(cx, cy - 110), (cx + a, cy - 110), (cx + a, cy + 110), (cx, cy + 110)], fill=(250, 220, 140), outline=(190, 150, 70))
        for j in range(3):
            if k_chemise > 0.5 + j * 0.15:
                file_icon(d, cx - 120 + j * 30, cy - 70 + j * 20, 1.3)

def arbre(d, p):
    tx, ty = 640, 560
    d.rectangle([tx - 30, ty - 230, tx + 30, ty], fill=(120, 80, 45))
    br = [(-1, 330, 250), (1, 330, 250), (-1, 230, 130), (1, 230, 130)]
    pts = []
    for k, (s, y, l) in enumerate(br):
        if p > 0.15 + k * 0.08:
            ex, ey = tx + s * l, y - 80
            d.line([tx, y, ex, ey], fill=(120, 80, 45), width=18); pts.append((ex, ey))
    if p > 0.55:
        for (ex, ey) in pts:
            for j in range(3):
                file_icon(d, ex - 40 + j * 26, ey - 70 + (j % 2) * 18, 0.6)
    if p > 0.3: O.label(d, "le tronc : l'ordinateur", (tx + 200, 470))
    if p > 0.45: O.label(d, "les branches : les dossiers", (260, 380))
    if p > 0.6: O.label(d, "les feuilles : les fichiers", (1020, 380))

# ---------- scènes ----------
NAV_DOC = R.rect_of("nav:Documents")
EXPL = R.rect_of("explorer")
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Comprendre l'arborescence", ["Aide-mémoire n° 04 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); R.folder_icon(d, W / 2 - 130, 300, 1.2); file_icon(d, W / 2 + 40, 290, 1.1)
        return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); armoire(d, x0=490, y0=100)
        if p > 0.4: O.label(d, "tout est rangé", (W / 2, 80))
        R.caption(d, cap); return im
    if sid == "armoire":
        im = O.room(); d = ImageDraw.Draw(im)
        armoire(d, R.ease((p - 0.15) / 0.2), R.ease((p - 0.5) / 0.25))
        if p > 0.05: O.label(d, "l'armoire", (270, 80))
        if p > 0.3: O.label(d, "un tiroir et ses chemises", (560, 200))
        if p > 0.65: O.label(d, "les feuilles", (870, 470))
        R.caption(d, cap); return im
    if sid == "mots":
        im = O.room(); d = ImageDraw.Draw(im)
        d.rounded_rectangle([170, 130, 1110, 520], 24, fill=(255, 255, 255), outline=YEL, width=6)
        d.rectangle([230, 200, 390, 300], fill=(200, 145, 90), outline=BOIS2, width=4); d.rectangle([250, 170, 290, 230], fill=(240, 205, 120))
        d.text((470, 225), "→", font=F(56, "b"), fill=INK); R.folder_icon(d, 560, 205, 1.0)
        if p > 0.25: d.text((690, 225), "un dossier", font=F(44, "b"), fill=VIO)
        file_icon(d, 270, 355, 1.1); d.text((470, 375), "→", font=F(56, "b"), fill=INK); file_icon(d, 580, 355, 1.1)
        if p > 0.6: d.text((690, 390), "un fichier", font=F(44, "b"), fill=VIO)
        R.caption(d, cap); return im
    if sid == "arbre":
        im = O.room(); d = ImageDraw.Draw(im); arbre(d, p); R.caption(d, cap); return im
    if sid == "ouvrir":
        return act(None, "Accueil", EXPL, (W / 2 + 200, H / 2), t, D, cap)
    if sid == "fenetre":
        im = screen("Accueil"); d = ImageDraw.Draw(im)
        if p > 0.25:
            R.highlight(d, (R.WX + 6, R.CMD_Y + 58, R.WX + R.NAV_W - 4, R.CMD_Y + 52 + 14 + 7 * 44), t)
            O.label(d, "les grands tiroirs", (R.WX + R.NAV_W + 160, 300))
        R.caption(d, cap); return im
    if sid == "documents":
        return act("Accueil", "Documents", NAV_DOC, (W / 2, H / 2), t, D, cap, place=(900, 330))
    if sid == "dossier":
        return act("Documents", "Lettres", R.rect_of("folder:0"), (W / 2 + 200, H / 2 + 100), t, D, cap, double=True, place=(900, 330))
    if sid == "fichiers":
        im = screen("Lettres"); d = ImageDraw.Draw(im)
        if p > 0.2: R.highlight(d, (file_rect(0)[0], file_rect(0)[1], file_rect(2)[2], file_rect(2)[3]), t)
        if p > 0.4: O.label(d, "les fichiers = les feuilles", (W / 2 + 120, 470))
        R.caption(d, cap); return im
    if sid == "adresse":
        im = screen("Lettres"); clean = im.copy(); d = ImageDraw.Draw(im)
        R.highlight(d, ADDR, t)
        if p > 0.3:
            R.loupe(im, (ADDR[0], ADDR[1], ADDR[0] + 260, ADDR[3]), place=(850, 330), clean=clean); d = ImageDraw.Draw(im)
            O.label(d, "le chemin", (850, 475))
        R.caption(d, cap); return im
    if sid == "remonter":
        r = seg_rects(["Documents", "Lettres"])[0]
        return act("Lettres", "Documents", r, (W / 2 + 200, H / 2), t, D, cap, hover=0, place=(900, 330))
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "fleche":
        im = screen("Lettres"); clean = im.copy(); d = ImageDraw.Draw(im)
        R.highlight(d, UP, t); R.arrow(d, UP, t)
        if p > 0.2: R.loupe(im, UP, place=(800, 330), clean=clean); d = ImageDraw.Draw(im); O.label(d, "la flèche qui monte", (800, 475))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Ouvrez l'Explorateur de fichiers,", "puis « Documents ».", "Ouvrez un dossier,", "puis remontez."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Ouvrez un dossier,", "puis remontez."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        seg = [(None, "Accueil", EXPL, (W / 2, H / 2), 0.0, 0.25, False, None),
               ("Accueil", "Documents", NAV_DOC, R.center(EXPL), 0.25, 0.5, False, None),
               ("Documents", "Lettres", R.rect_of("folder:0"), R.center(NAV_DOC), 0.5, 0.75, True, None),
               ("Lettres", "Documents", seg_rects(["Documents", "Lettres"])[0], R.center(R.rect_of("folder:0")), 0.75, 1.01, False, 0)]
        for vb, va, r, s, x0, x1, dbl, hv in seg:
            if x0 * D <= t < x1 * D:
                return act(vb, va, r, s, t - x0 * D, (x1 - x0) * D, cap, show_loupe=False, double=dbl, hover=hv)
    if sid == "resume":
        return R.card("À retenir", ["Dossier = tiroir, fichier = feuille", "Le dossier jaune ouvre l'Explorateur", "Double-clic : j'ouvre un dossier", "Le chemin en haut : je remonte"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
