"""Vidéo « 16 - Créer une adresse Gmail » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_16.py script.json durations.json out.mp4
        python3 render_16.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes),
../01-ordinateur/render_01_ordinateur.py (pièce, étiquettes) et ../12-internet/render_12.py (fenêtre du navigateur).
Écrans SIMPLIFIÉS et NEUTRES : aucun logo, aucune couleur ni charte de Google ; mention « dessin simplifié » sur chaque page.
Libellés écrits tels quels (confirmés, voir sources_16.md) : « Créer un compte », « Pour mon usage personnel »,
« Pour mon enfant », « Pour le travail ou mon entreprise », « Suivant », « J'accepte ». Les autres textes dessinés
(noms de cases) sont indicatifs et ne sont jamais cités dans la fiche.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as B
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); GRIS = (90, 94, 104); NEUTRE = (64, 68, 80)
ADRESSE = "gmail.com"
EX = "marie.dupont"

# carte du formulaire (dans la page du navigateur)
CX0, CY0, CX1, CY1 = 380, B.PAGE_Y + 14, 900, B.PAGE_Y + 462
BTN_CREER = (535, B.PAGE_Y + 250, 745, B.PAGE_Y + 296)
MENU = [("Pour mon usage personnel", (520, B.PAGE_Y + 304, 860, B.PAGE_Y + 342)),
        ("Pour mon enfant", (520, B.PAGE_Y + 342, 860, B.PAGE_Y + 380)),
        ("Pour le travail ou mon entreprise", (520, B.PAGE_Y + 380, 860, B.PAGE_Y + 418))]
SUIVANT = (760, CY1 - 66, 880, CY1 - 20)

def field(y, x0=CX0 + 40, x1=CX1 - 40):
    return (x0, y, x1, y + 50)

FIELDS = {
    "nom": [("Prénom", field(B.PAGE_Y + 120), "Marie"), ("Nom", field(B.PAGE_Y + 190), "Dupont")],
    "naissance": [("Jour", field(B.PAGE_Y + 120, CX0 + 40, CX0 + 170), "12"), ("Mois", field(B.PAGE_Y + 120, CX0 + 185, CX0 + 330), "mars"),
                  ("Année", field(B.PAGE_Y + 120, CX0 + 345, CX1 - 40), "1950"), ("Genre", field(B.PAGE_Y + 200), "Femme")],
    "motdepasse": [("Mot de passe", field(B.PAGE_Y + 120), "••••••••••"), ("Confirmer", field(B.PAGE_Y + 190), "••••••••••")],
    "telephone": [("Numéro de téléphone", field(B.PAGE_Y + 140), "06 12 34 56 78")],
}
TITRES = {"nom": "Créer un compte", "naissance": "Informations générales", "adresse": "Choisissez votre adresse",
          "motdepasse": "Créez un mot de passe", "telephone": "Numéro de téléphone (secours)", "regles": "Règles et conditions"}
OPTS = [f"{EX}1950@gmail.com", f"dupont.marie@gmail.com", "Écrire ma propre adresse"]
OPT_R = [(CX0 + 40, B.PAGE_Y + 110 + i * 62, CX1 - 40, B.PAGE_Y + 158 + i * 62) for i in range(3)]

def simple(d):
    d.text((CX0 + 40, CY1 - 50), "(dessin simplifié)", font=F(16), fill=(110, 110, 120))

def page(d, kind, vals=None, focus=None, menu=False, sel=None, typed_own=""):
    vals = vals or {}
    if kind == "accueil":
        cx = (B.BX + B.BW) / 2 + B.BX / 2
        f = F(56, "b"); t = "Gmail"; tw = d.textlength(t, font=f); d.text((640 - tw / 2, B.PAGE_Y + 60), t, font=f, fill=NEUTRE)
        f2 = F(22); s = "La messagerie gratuite"; tw = d.textlength(s, font=f2); d.text((640 - tw / 2, B.PAGE_Y + 150), s, font=f2, fill=GRIS)
        d.rounded_rectangle(BTN_CREER, 22, fill=NEUTRE)
        f3 = F(20, "b"); s = "Créer un compte"; tw = d.textlength(s, font=f3); d.text((640 - tw / 2, BTN_CREER[1] + 11), s, font=f3, fill=(255, 255, 255))
        if menu:
            d.rounded_rectangle([MENU[0][1][0] - 4, MENU[0][1][1] - 4, MENU[-1][1][2] + 4, MENU[-1][1][3] + 4], 8, fill=(255, 255, 255), outline=(170, 175, 185), width=2)
            for i, (lab, r) in enumerate(MENU):
                if sel == i: d.rectangle(r, fill=(232, 234, 240))
                d.text((r[0] + 14, r[1] + 8), lab, font=F(19), fill=(25, 25, 30))
        d.text((640 - 70, B.PAGE_Y + 440), "(dessin simplifié)", font=F(16), fill=(110, 110, 120))
        return
    if kind == "boite":
        d.rectangle([B.BX + 2, B.PAGE_Y + 1, B.BX + 260, B.BY + B.BH - 2], fill=(244, 245, 248))
        d.rounded_rectangle([B.BX + 20, B.PAGE_Y + 20, B.BX + 200, B.PAGE_Y + 66], 16, fill=(225, 228, 236))
        d.text((B.BX + 44, B.PAGE_Y + 31), "Nouveau message", font=F(18, "b"), fill=INK)
        d.rounded_rectangle([B.BX + 12, B.PAGE_Y + 86, B.BX + 248, B.PAGE_Y + 122], 12, fill=(215, 220, 232))
        d.text((B.BX + 30, B.PAGE_Y + 93), "Boîte de réception", font=F(18, "b"), fill=INK)
        d.text((B.BX + 290, B.PAGE_Y + 22), f"{EX}@gmail.com", font=F(22, "b"), fill=INK)
        for i in range(5):
            y = B.PAGE_Y + 70 + i * 56
            d.line([B.BX + 280, y + 50, B.BX + B.BW - 20, y + 50], fill=(225, 228, 234), width=1)
            d.rounded_rectangle([B.BX + 290, y + 16, B.BX + 290 + 160 - i * 12, y + 30], 6, fill=(205, 208, 216))
            d.rounded_rectangle([B.BX + 480, y + 16, B.BX + 780 - i * 25, y + 30], 6, fill=(225, 228, 234))
        d.text((B.BX + 290, B.BY + B.BH - 34), "(dessin simplifié)", font=F(16), fill=(110, 110, 120))
        return
    d.rounded_rectangle([CX0, CY0, CX1, CY1], 16, fill=(255, 255, 255), outline=(200, 204, 212), width=2)
    d.text((CX0 + 40, CY0 + 30), TITRES[kind], font=F(30, "b"), fill=INK)
    if kind in FIELDS:
        for i, (lab, r, val) in enumerate(FIELDS[kind]):
            foc = focus == i
            d.rounded_rectangle(r, 8, fill=(255, 255, 255), outline=(60, 90, 160) if foc else (160, 165, 175), width=3 if foc else 2)
            v = vals.get(i, "")
            if v:
                d.text((r[0] + 10, r[1] - 12), lab, font=F(15), fill=GRIS, stroke_width=4, stroke_fill=(255, 255, 255))
                d.text((r[0] + 14, r[1] + 11), v, font=F(22), fill=(20, 20, 20))
            else:
                d.text((r[0] + 14, r[1] + 12), lab, font=F(21), fill=GRIS)
            if foc:
                x = r[0] + 14 + (d.textlength(v, font=F(22)) if v else 0) + 2; d.line([x, r[1] + 11, x, r[3] - 11], fill=(20, 20, 20), width=2)
    if kind == "adresse":
        for i, (o, r) in enumerate(zip(OPTS, OPT_R)):
            cy = (r[1] + r[3]) / 2
            d.ellipse([r[0], cy - 12, r[0] + 24, cy + 12], outline=NEUTRE, width=3)
            if sel == i: d.ellipse([r[0] + 6, cy - 6, r[0] + 18, cy + 6], fill=NEUTRE)
            d.text((r[0] + 40, cy - 13), o, font=F(21), fill=(20, 20, 20))
        if sel == 2:
            r = (CX0 + 80, OPT_R[2][3] + 8, CX1 - 40, OPT_R[2][3] + 54)
            d.rounded_rectangle(r, 8, outline=(60, 90, 160), width=3)
            d.text((r[0] + 12, r[1] + 11), typed_own, font=F(21), fill=(20, 20, 20))
            d.text((r[0] + 14 + d.textlength(typed_own, font=F(21)), r[1] + 11), "@gmail.com", font=F(21), fill=GRIS)
    if kind == "regles":
        for i in range(7):
            d.rounded_rectangle([CX0 + 40, B.PAGE_Y + 110 + i * 34, CX1 - 40 - (i % 3) * 60, B.PAGE_Y + 124 + i * 34], 6, fill=(225, 228, 234))
    lab = "J'accepte" if kind == "regles" else "Suivant"
    d.rounded_rectangle(SUIVANT, 22, fill=NEUTRE)
    f = F(20, "b"); tw = d.textlength(lab, font=f); c = R.center(SUIVANT); d.text((c[0] - tw / 2, SUIVANT[1] + 11), lab, font=f, fill=(255, 255, 255))
    simple(d)

def screen(kind=None, typed=ADRESSE, **kw):
    im = B.screen("browser", typed=typed, page="x" if kind else None) if kind else B.screen("browser", typed=typed, focus=not kind)
    d = ImageDraw.Draw(im)
    if kind:
        d.rectangle([B.BX + 48, B.BY + 10, B.BX + 290, B.BY + 36], fill=(250, 250, 252))
        d.text((B.BX + 50, B.BY + 12), "Gmail", font=F(17), fill=(30, 30, 30))
        d.rectangle([B.BX + 2, B.PAGE_Y + 1, B.BX + B.BW - 2, B.BY + B.BH - 2], fill=(255, 255, 255))
        page(d, kind, **kw)
    return im

def fill_scene(kind, nxt, t, D, cap, nxt_kw=None):
    """Remplit les cases une à une (55 % du temps), puis clic sur Suivant."""
    fl = FIELDS[kind]; T1 = 0.55 * D; n = len(fl)
    if t < T1:
        k = min(n - 1, int(t / T1 * n)); tt = t - k * T1 / n; seg = T1 / n
        vals = {j: fl[j][2] for j in range(k)}
        v = fl[k][2]; vals[k] = v[:int(len(v) * max(0, min(1, (tt - 0.2 * seg) / (0.6 * seg))))]
        im = screen(kind, vals=vals, focus=k); d = ImageDraw.Draw(im)
        R.highlight(d, fl[k][1], t)
        R.cursor(d, fl[k][1][0] + 60, fl[k][1][1] + 30)
        R.caption(d, cap); return im
    full = {j: fl[j][2] for j in range(n)}
    return B.act(lambda: screen(kind, vals=full), lambda: screen(nxt, **(nxt_kw or {})), SUIVANT, (fl[-1][1][0] + 60, fl[-1][1][1] + 30), t - T1, D - T1, cap, place=(1035, 330))

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None):
    return B.act(before, after, r, start, t, D, cap, show_loupe=show_loupe, place=place)

# ---------- illustrations ----------
def enveloppe(d, x, y, s=1.0, col=(255, 255, 255)):
    w, h = 120 * s, 80 * s
    d.rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=col, outline=INK, width=4)
    d.line([x - w / 2, y - h / 2, x, y + 6 * s, x + w / 2, y - h / 2], fill=INK, width=4)

def arobase(d, x, y, size=150, col=VIO):
    f = F(size, "b"); tw = d.textlength("@", font=f); d.text((x - tw / 2, y - size * 0.62), "@", font=f, fill=col)

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Créer une adresse Gmail", ["Aide-mémoire n° 16 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); enveloppe(d, W / 2, 370, 1.3, (255, 246, 214)); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); O.draw_fixe(d)
        x = 350 + 600 * R.ease((p - 0.15) / 0.5)
        enveloppe(d, x, 220, 0.9, (255, 246, 214))
        if p > 0.45: O.label(d, "envoyer et recevoir des messages", (W / 2, 120))
        if p > 0.75: O.label(d, "C'est gratuit", (1050, 340))
        R.caption(d, cap); return im
    if sid == "analogie":
        im = O.room(); d = ImageDraw.Draw(im)
        enveloppe(d, 330, 260, 1.6, (255, 246, 214))
        d.text((262, 255), "Mme Marie Dupont", font=F(15, "b"), fill=INK); d.text((262, 275), "12 rue des Lilas", font=F(15), fill=INK)
        O.label(d, "adresse postale", (330, 380))
        if p > 0.3:
            d.rounded_rectangle([640, 200, 1180, 320], 16, fill=(255, 255, 255), outline=INK, width=3)
            f = F(30, "b"); s1, s2 = EX, "gmail.com"
            x = 660; d.text((x, 240), s1, font=f, fill=INK); x += d.textlength(s1, font=f)
            hl = p > 0.5
            if hl: d.rounded_rectangle([x - 2, 232, x + 38, 286], 8, fill=YEL)
            d.text((x, 238), "@", font=F(34, "b"), fill=VIO); x += 38; d.text((x, 240), s2, font=f, fill=INK)
            O.label(d, "adresse mail", (910, 380))
        if p > 0.5:
            arobase(d, 910, 520, 110)
            O.label(d, "l'arobase", (1080, 520))
        R.caption(d, cap); return im
    if sid == "ouvrir":
        q = 0.3 * D
        if t < q:
            return act(lambda: R.screen({"window": False}), lambda: B.screen("browser"), B.EDGE, (W / 2 - 200, H / 2), t, q, cap, show_loupe=False)
        tt = t - q
        if tt < 0.45 * (D - q):
            n = int(len(ADRESSE) * min(1, tt / (0.35 * (D - q))))
            im = B.screen("browser", typed=ADRESSE[:n], focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
            R.highlight(d, B.ADDR, t)
            O.label(d, "tapez : gmail.com", (640, 400))
            R.caption(d, cap); return im
        pressed = 0.45 * (D - q) < tt < 0.6 * (D - q)
        if tt < 0.6 * (D - q):
            im = B.screen("browser", typed=ADRESSE, focus=True); d = ImageDraw.Draw(im); R.key_enter(d, t, pressed)
        else:
            im = screen("accueil"); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "creer":
        return act(lambda: screen("accueil"), lambda: screen("accueil", menu=True), BTN_CREER, (W / 2, 330), t, D, cap, place=(1010, 330))
    if sid == "usage":
        r = MENU[0][1]
        return act(lambda: screen("accueil", menu=True, sel=0 if p > 0.4 else None), lambda: screen("nom"), r, (640, BTN_CREER[3] - 10), t, D, cap, place=(1010, 330))
    if sid == "nom":
        return fill_scene("nom", "naissance", t, D, cap)
    if sid == "naissance":
        return fill_scene("naissance", "adresse", t, D, cap)
    if sid == "adresse":
        T1 = 0.25 * D; T2 = 0.7 * D
        if t < T1:
            im = screen("adresse"); d = ImageDraw.Draw(im)
            if p > 0.08: R.highlight(d, (OPT_R[0][0] - 8, OPT_R[0][1] - 4, OPT_R[1][2], OPT_R[1][3] + 4), t)
            R.caption(d, cap); return im
        if t < T2:
            tt = t - T1; seg = T2 - T1
            if tt < 0.3 * seg:
                return act(lambda: screen("adresse"), lambda: screen("adresse", sel=2), OPT_R[2], (CX1 - 80, OPT_R[0][1]), tt, 0.3 * seg / 0.62, cap, show_loupe=False)
            n = int(len(EX) * min(1, (tt - 0.3 * seg) / (0.5 * seg)))
            im = screen("adresse", sel=2, typed_own=EX[:n]); d = ImageDraw.Draw(im)
            if tt > 0.85 * seg: O.label(d, "pas d'espace, pas d'accent", (640, 120))
            R.caption(d, cap); return im
        return act(lambda: screen("adresse", sel=2, typed_own=EX), lambda: screen("motdepasse"), SUIVANT, (CX1 - 200, OPT_R[2][3] + 30), t - T2, D - T2, cap, place=(1035, 330))
    if sid == "motdepasse":
        T1 = 0.55 * D
        if 0.45 * D < t < 0.62 * D:
            im = screen("motdepasse", vals={0: "••••••••••", 1: "••••••••••"}); d = ImageDraw.Draw(im)
            d.rounded_rectangle([930, 230, 1240, 470], 14, fill=(255, 246, 214), outline=INK, width=3)
            d.text((955, 250), "Mon carnet", font=F(24, "b"), fill=VIO)
            for i in range(5): d.line([955, 300 + i * 32, 1215, 300 + i * 32], fill=(200, 190, 160), width=2)
            d.text((960, 306), "Gmail :", font=F(20, "b"), fill=INK); d.text((960, 338), "mot de passe : ****", font=F(20), fill=INK)
            O.label(d, "secret !", (1085, 510))
            R.caption(d, cap); return im
        return fill_scene("motdepasse", "telephone", t, D, cap)
    if sid == "secours":
        T1 = 0.6 * D
        if t < T1:
            vals = {0: FIELDS["telephone"][0][2][:int(14 * min(1, t / (0.5 * D)))]}
            im = screen("telephone", vals=vals, focus=0); d = ImageDraw.Draw(im)
            R.highlight(d, FIELDS["telephone"][0][1], t)
            if p > 0.35: O.label(d, "pour retrouver votre compte", (640, B.PAGE_Y + 270))
            R.caption(d, cap); return im
        return act(lambda: screen("telephone", vals={0: FIELDS["telephone"][0][2]}), lambda: screen("regles"), SUIVANT, (640, 400), t - T1, D - T1, cap, show_loupe=False)
    if sid == "accepte":
        T1 = 0.6 * D
        if t < T1:
            return act(lambda: screen("regles"), lambda: screen("boite"), SUIVANT, (640, 360), t, T1, cap, place=(1035, 330))
        im = screen("boite"); d = ImageDraw.Draw(im)
        if p > 0.75: O.label(d, "Bravo !", (W / 2, 520))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et notez votre adresse dans votre carnet."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "exercice":
        return R.card("Exercice", ["Écrivez sur une feuille", "l'adresse que vous aimeriez avoir,", "avec l'arobase @."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Écrivez l'adresse que", "vous aimeriez avoir."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        im = O.room(); d = ImageDraw.Draw(im)
        parts = [("prénom", INK), (".", INK), ("nom", INK), ("@", VIO), ("gmail.com", INK)]
        f = F(54, "b"); x = 640 - sum(d.textlength(s, font=f) for s, _ in parts) / 2
        k = int(min(5, p * 9)) + 1
        for i, (s, c) in enumerate(parts[:k]):
            d.text((x, 210), s, font=f, fill=c); x += d.textlength(s, font=f)
        if p > 0.55: O.label(d, "Exemple : marie.dupont@gmail.com", (640, 360))
        if p > 0.75: O.label(d, "pas d'espace, pas d'accent", (640, 450))
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Tapez gmail.com", "Cliquez sur « Créer un compte »", "Suivez les étapes avec « Suivant »", "Gardez votre mot de passe secret"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
