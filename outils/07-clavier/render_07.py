"""Vidéo « 07 - Découvrir le clavier » (clavier AZERTY dessiné, sans voix, sous-titrée).
Usage : python3 render_07.py script.json durations.json out.mp4
        python3 render_07.py --estimate script.json durations.json
Réutilise ../render_01.py (cadre jaune, flèche, loupe, titres, sous-titres, cartes) et ../01-ordinateur (pièce, étiquettes).
Libellés écrits tels quels (voir sources_07.md) : Entrée, Retour arrière, Suppr, Maj, Verr Maj, Alt Gr, Échap, barre d'espace, pavé numérique.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126)
U = 52                     # largeur d'une touche
KY = 234                   # haut du clavier

# ---------- disposition AZERTY ----------
ROW1 = [("²", "", ""), ("&", "1", ""), ("é", "2", "~"), ('"', "3", "#"), ("'", "4", "{"), ("(", "5", "["), ("-", "6", "|"),
        ("è", "7", "`"), ("_", "8", "\\"), ("ç", "9", "^"), ("à", "0", "@"), (")", "°", "]"), ("=", "+", "}")]
ROW2 = list("AZERTYUIOP") + ["^", "$"]
ROW3 = list("QSDFGHJKLM") + ["ù", "*"]
ROW4 = ["<"] + list("WXCVBN") + [",", ";", ":", "!"]

def layout(numpad=True):
    """Dictionnaire nom -> (x0, y0, x1, y1, libellé bas, libellé haut, libellé AltGr)."""
    total = 15 + (8 if numpad else 0) if numpad else 15
    X0 = (W - (23.2 if numpad else 15) * U) / 2
    K = {}; g = 3
    def add(name, col, row, w=1.0, h=1.0, lo="", hi="", ag=""):
        x = X0 + col * U; y = KY + row * U + (8 if row > 0 else 0)
        K[name] = (x + g, y + g, x + w * U - g, y + h * U - g, lo, hi, ag)
    add("esc", 0, 0, lo="Échap")
    for i in range(12): add(f"F{i+1}", 1.5 + i + (i // 4) * 0.25, 0, lo=f"F{i+1}")
    for i, (lo, hi, ag) in enumerate(ROW1): add("k" + (hi or lo), i, 1, lo=lo, hi=hi, ag=ag)
    add("back", 13, 1, 2, lo="←", hi="Retour arrière")
    add("tab", 0, 2, 1.5, lo="⇥")
    for i, c in enumerate(ROW2): add(c, 1.5 + i, 2, lo=c)
    add("enter", 13.5, 2, 1.5, 2, lo="Entrée ↵")
    add("verr", 0, 3, 1.75, lo="Verr Maj")
    for i, c in enumerate(ROW3): add(c, 1.75 + i, 3, lo=c)
    add("maj", 0, 4, 1.25, lo="⇧ Maj")
    for i, c in enumerate(ROW4): add("r4" + c, 1.25 + i, 4, lo=c)
    add("majd", 12.25, 4, 2.75, lo="⇧ Maj")
    for name, col, w, lo in (("ctrl", 0, 1.25, "Ctrl"), ("win", 1.25, 1.25, ""), ("alt", 2.5, 1.25, "Alt"), ("space", 3.75, 6.25, ""),
                             ("altgr", 10, 1.25, "Alt Gr"), ("win2", 11.25, 1.25, ""), ("menu", 12.5, 1.25, "≡"), ("ctrld", 13.75, 1.25, "Ctrl")):
        add(name, col, 5, w, lo=lo)
    if numpad:
        add("suppr", 15.2, 1, lo="Suppr")
        add("up", 16.2, 4, lo="↑")
        for i, a in enumerate("←↓→"): add("ar" + a, 15.2 + i, 5, lo=a)
        nx = 19.2
        for r, rowk in enumerate([["/", "*", "-"], ["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"]]):
            for c, k in enumerate(rowk): add("n" + k, nx + c, 1 + r, lo=k)
        add("n+", nx + 3, 2, 1, 2, lo="+"); add("nent", nx + 3, 4, 1, 2, lo="↵")
        add("n0", nx, 5, 2, lo="0"); add("n.", nx + 2, 5, lo=".")
        add("nlock", nx + 3, 1, lo="")
    else:
        add("suppr", 14, 0, lo="Suppr")
    return K

KB = layout(True); KP = layout(False)

def rect(name, K=None):
    k = (K or KB)[name]; return k[:4]

def union(names, K=None):
    rs = [rect(n, K) for n in names]
    return (min(r[0] for r in rs), min(r[1] for r in rs), max(r[2] for r in rs), max(r[3] for r in rs))

LETTRES = union(["A", "r4!"]); CHIFFRES = union(["k²", "k+"])
PAVE = union(["n/", "n."]) if "n/" in KB else None

def lock_icon(d, x, y, s=1.0):
    d.arc([x, y, x + 12 * s, y + 14 * s], 180, 360, fill=INK, width=max(2, int(2 * s)))
    d.rounded_rectangle([x - 2 * s, y + 7 * s, x + 14 * s, y + 19 * s], 2, fill=INK)

def keyboard(d, K=None, pressed=(), caps=False):
    K = K or KB
    xs = [k[0] for k in K.values()]; xe = [k[2] for k in K.values()]
    d.rounded_rectangle([min(xs) - 16, KY - 14, max(xe) + 16, KY + 6 * U + 26], 18, fill=(60, 62, 72))
    for name, (x0, y0, x1, y1, lo, hi, ag) in K.items():
        dn = name in pressed; off = 4 if dn else 0
        d.rounded_rectangle([x0, y0 + 4, x1, y1 + 4], 6, fill=(30, 30, 36))
        d.rounded_rectangle([x0, y0 + off, x1, y1 + off], 6, fill=(205, 225, 250) if dn else (248, 248, 250), outline=(150, 150, 160), width=1)
        y0 += off; y1 += off
        if hi and len(hi) > 1:      # « Retour arrière » : flèche seule sur la touche
            d.text((x0 + 10, y0 + 6), lo, font=F(24, "b"), fill=INK)
        elif hi:
            d.text((x0 + 6, y0 + 3), hi, font=F(17, "b"), fill=INK)
            d.text((x0 + 6, y1 - 23), lo, font=F(17, "s"), fill=INK)
            if ag: d.text((x1 - 16, y1 - 23), ag, font=F(15, "s"), fill=(0, 90, 170))
        elif lo:
            f = F(22, "b") if len(lo) == 1 else F(14, "s")
            if name == "enter": d.text((x0 + 8, y0 + 8), lo, font=F(13, "b"), fill=INK)
            elif len(lo) == 1: d.text((x0 + 8, y0 + 6), lo, font=f, fill=INK)
            else: d.text((x0 + 6, y0 + 6), lo, font=f, fill=INK)
        if name in ("win", "win2"):
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            for a in (-1, 1):
                for b in (-1, 1):
                    d.rectangle([cx + (1 if a > 0 else -9), cy + (1 if b > 0 else -9), cx + (9 if a > 0 else -1), cy + (9 if b > 0 else -1)], fill=(0, 103, 192))
        if name == "verr":
            lock_icon(d, x1 - 22, y0 + 6, 0.9)
            d.ellipse([x1 - 14, y1 - 14, x1 - 6, y1 - 6], fill=(60, 200, 90) if caps else (200, 200, 205))

# ---------- feuille de texte ----------
SHEET = (250, 90, 1030, 220)
def sheet(d, text, t=0.0):
    d.rounded_rectangle([SHEET[0] + 6, SHEET[1] + 6, SHEET[2] + 6, SHEET[3] + 6], 12, fill=(120, 100, 90))
    d.rounded_rectangle(SHEET, 12, fill=(255, 255, 255), outline=(200, 200, 210), width=2)
    lines = text.split("\n"); f = F(40, "s"); y = SHEET[1] + 14
    for i, ln in enumerate(lines[-2:]):
        d.text((SHEET[0] + 28, y), ln, font=f, fill=(20, 20, 20))
        if i == len(lines[-2:]) - 1 and (t % 1.0) < 0.6:
            x = SHEET[0] + 30 + d.textlength(ln, font=f)
            d.line([x, y + 4, x, y + 48], fill=(20, 20, 20), width=3)
        y += 56

def base(text, t, pressed=(), caps=False, K=None, show_sheet=True):
    im = O.room().copy(); d = ImageDraw.Draw(im)
    if show_sheet: sheet(d, text, t)
    keyboard(d, K, pressed, caps)
    return im, d

def act(keys, before, after, t, D, cap, hold=None, caps=False, place=None, label=None):
    """Montre une touche (cadre, flèche, loupe), puis l'appui : hold (maintenue) puis keys."""
    tc = 0.55 * D
    pressed = set()
    if hold and 0.4 * D <= t < tc + 0.8: pressed.add(hold)
    if tc <= t < tc + 0.5: pressed.update(keys)
    im, d = base(after if t >= tc else before, t, pressed, caps)
    clean = im.copy()
    tgt = union(([hold] if hold else []) + list(keys)) if hold else union(list(keys))
    if t < tc + 1.0:
        for k in ([hold] if hold else []) + list(keys): R.highlight(d, rect(k), t)
        R.arrow(d, rect(keys[-1]), t)
    if 0.15 * D < t < tc + 1.0:
        for k in ([hold] if hold else []):
            pass
        R.loupe(im, rect(keys[-1]), place=place or (1120, 120), clean=clean); d = ImageDraw.Draw(im)
    if label and t > 0.2 * D: O.label(d, label, (640, 600 - 360) if False else label_pos(keys[-1]))
    R.caption(d, cap); return im

def label_pos(k):
    r = rect(k); return ((r[0] + r[2]) / 2, KY - 62) if False else (min(max((r[0] + r[2]) / 2, 200), 1080), 236)

# ---------- scènes ----------
def typing(seq, t, D, t0, t1, start_text="", caps=False):
    """seq : liste de (touches appuyées, maintenue, texte après). Renvoie (texte, touches enfoncées)."""
    n = len(seq); step = (t1 - t0) * D / n; text = start_text; pressed = set()
    for i, (keys, hold, after) in enumerate(seq):
        ts = t0 * D + i * step
        if hold and ts - 0.25 * step <= t < ts + 0.45 * step: pressed.add(hold)
        if ts + 0.15 * step <= t < ts + 0.45 * step: pressed.update(keys)
        if t >= ts + 0.15 * step: text = after
    return text, pressed

SOL = [(["P"], "maj", "P"), (["A"], None, "Pa"), (["U"], None, "Pau"), (["L"], None, "Paul"), (["space"], None, "Paul "),
       (["k1"], "maj", "Paul 1"), (["k9"], "maj", "Paul 19")]

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Découvrir le clavier", ["Aide-mémoire n° 07 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im)
        for i, c in enumerate("AZERTY"):
            x = W / 2 - 3 * 78 + i * 78
            d.rounded_rectangle([x, 300, x + 66, 366], 10, fill=(248, 248, 250), outline=(60, 62, 72), width=4)
            d.text((x + 20, 312), c, font=F(34, "b"), fill=INK)
        return im
    if sid == "intro":
        seq = [([c], "maj" if i == 0 else None, "Bonjour"[:i + 1]) for i, c in enumerate("BONJOUR")]
        text, pr = typing(seq, t, D, 0.15, 0.75)
        im, d = base(text, t, pr)
        if p > 0.8: O.label(d, "une touche = une lettre, un chiffre ou un signe", (640, 236))
        R.caption(d, cap); return im
    if sid == "zones":
        im, d = base("", t, show_sheet=False)
        if 0.12 < p < 0.42: R.highlight(d, LETTRES, t); O.label(d, "les lettres", (640, 150))
        if 0.42 <= p < 0.68: R.highlight(d, CHIFFRES, t); O.label(d, "la rangée de chiffres", (480, 150))
        if p >= 0.68: R.highlight(d, PAVE, t); O.label(d, "le pavé numérique", (1050, 150))
        R.caption(d, cap); return im
    if sid == "portable":
        im, d = base("", t, K=KP, show_sheet=False)
        if 0.15 < p <= 0.55: O.label(d, "pas de pavé numérique", (640, 150))
        if p > 0.55: R.highlight(d, union(["k²", "k+"], KP), t); O.label(d, "on utilise les chiffres du haut", (640, 200))
        R.caption(d, cap); return im
    if sid == "espace":
        return act(["space"], "Bonjour", "Bonjour ", t, D, cap, place=(1120, 130))
    if sid == "entree":
        return act(["enter"], "Bonjour Paul", "Bonjour Paul\n", t, D, cap, place=(150, 130))
    if sid == "retour":
        return act(["back"], "Bonjourr", "Bonjour", t, D, cap, place=(150, 130))
    if sid == "maj":
        return act(["P"], "", "P", t, D, cap, hold="maj", place=(1120, 130))
    if sid == "verrmaj":
        caps = 0.2 * D <= t < 0.8 * D
        seq = [([c], None, "PAUL"[:i + 1]) for i, c in enumerate("PAUL")]
        text, pr = typing(seq, t, D, 0.3, 0.7)
        if 0.12 * D <= t < 0.2 * D or 0.8 * D <= t < 0.86 * D: pr.add("verr")
        im, d = base(text, t, pr, caps); clean = im.copy()
        R.highlight(d, rect("verr"), t)
        if p < 0.3 or p > 0.75: R.loupe(im, rect("verr"), place=(1120, 130), clean=clean); d = ImageDraw.Draw(im)
        O.label(d, "majuscules : OUI" if caps else "majuscules : non", (860, 196))
        R.caption(d, cap); return im
    if sid == "chiffres":
        return act(["k1"], "Paul ", "Paul 1", t, D, cap, hold="maj", place=(1120, 130))
    if sid == "arobase":
        return act(["k0"], "paul", "paul@", t, D, cap, hold="altgr", place=(1120, 130))
    if sid == "echap":
        im, d = base("", t, ("esc",) if 0.5 * D <= t < 0.6 * D else (), show_sheet=False); clean = im.copy()
        R.highlight(d, rect("esc"), t); R.arrow(d, rect("esc"), t)
        if p > 0.15: R.loupe(im, rect("esc"), place=(980, 160), clean=clean); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "exercice":
        return R.card("Exercice", ["Écrivez votre prénom", "avec une majuscule,", "puis un espace,", "puis le nombre 19."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Votre prénom, un espace, 19"], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        text, pr = typing(SOL, t, D, 0.08, 0.92)
        im, d = base(text, t, pr)
        for k in pr: R.highlight(d, rect(k), 0.1)
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Barre d'espace : entre les mots", "Entrée : je passe à la ligne", "Retour arrière : j'efface", "Maj : majuscules et chiffres"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
