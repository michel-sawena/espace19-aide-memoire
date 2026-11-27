"""Vidéo « 21 - Créer un compte en ligne et FranceConnect » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_21.py script.json durations.json out.mp4
        python3 render_21.py --estimate script.json durations.json
Réutilise ../render_01.py, ../01-ordinateur/render_01_ordinateur.py et ../12-internet/render_12.py (fenêtre de navigateur).
Écrans SIMPLIFIÉS ET NEUTRES : site de démarche inventé (« Mon espace démarches », marqué EXEMPLE), aucun logo,
aucune charte de site officiel. Le bouton « S'identifier avec FranceConnect » est dessiné en gris neutre, texte seul.
Libellés écrits tels quels (voir sources_21.md) : « S'identifier avec FranceConnect », « Continuer ».
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as N
from PIL import ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); BLEU = (0, 103, 192); GRIS = (90, 96, 110)
BX, BY, BW, BH, PY = N.BX, N.BY, N.BW, N.BH, N.PAGE_Y
CX = BX + BW / 2
MAIL, MDP, CODE = "jeanne.martin@exemple.fr", "••••••••••••", "482 913"

# ---------- zones cliquables ----------
B_CREER = (CX - 170, PY + 300, CX + 170, PY + 350)
B_FC = (CX - 230, PY + 220, CX + 230, PY + 280)
CASE_MAIL = (CX - 260, PY + 120, CX + 260, PY + 162)
CASE_MDP = (CX - 260, PY + 210, CX + 260, PY + 252)
B_VALID = (CX - 110, PY + 300, CX + 110, PY + 348)
CASE_CODE = (CX - 140, PY + 170, CX + 140, PY + 220)
COMPTES = ["impots.gouv.fr", "ameli.fr", "L'Identité Numérique La Poste", "MSA", "France Identité"]
def compte_rect(i):
    col, row = i % 2, i // 2
    x0 = CX - 420 + col * 430; y0 = PY + 120 + row * 82
    return (x0, y0, x0 + 410, y0 + 66)
B_CONT = (CX - 140, PY + 290, CX + 140, PY + 344)

def bouton(d, r, txt, fill=(255, 255, 255), col=INK, outline=GRIS, size=22, bold=True):
    d.rounded_rectangle(r, 10, fill=fill, outline=outline, width=2)
    f = F(size, "b" if bold else "s"); tw = d.textlength(txt, font=f)
    d.text(((r[0] + r[2]) / 2 - tw / 2, (r[1] + r[3]) / 2 - size * 0.62), txt, font=f, fill=col)

def case(d, r, label, val="", focus=False):
    d.text((r[0], r[1] - 30), label, font=F(19, "s"), fill=INK)
    d.rounded_rectangle(r, 6, fill=(255, 255, 255), outline=BLEU if focus else (170, 175, 185), width=3 if focus else 2)
    d.text((r[0] + 14, r[1] + 9), val, font=F(21), fill=(20, 20, 20))
    if focus:
        x = r[0] + 16 + d.textlength(val, font=F(21)); d.line([x, r[1] + 8, x, r[3] - 8], fill=(20, 20, 20), width=2)

def exemple(d):
    f = F(18, "b"); d.rounded_rectangle([BX + BW - 150, PY + 14, BX + BW - 24, PY + 44], 8, fill=(255, 122, 89))
    d.text((BX + BW - 134, PY + 18), "EXEMPLE", font=f, fill=(255, 255, 255))

def page(d, quoi, **kw):
    """Contenu de la page (site inventé, neutre)."""
    d.rectangle([BX + 2, PY + 1, BX + BW - 2, PY + 58], fill=(236, 238, 244))
    titre = "Connexion avec FranceConnect" if quoi.startswith("fc_") else "Mon espace démarches"
    d.text((BX + 30, PY + 14), titre, font=F(26, "b"), fill=INK); exemple(d)
    if quoi == "accueil":
        d.text((CX - 260, PY + 100), "Bienvenue ! Pour continuer, connectez-vous.", font=F(22, "s"), fill=INK)
        bouton(d, B_FC, "S'identifier avec FranceConnect", fill=(232, 235, 242), size=24)
        f = F(19); d.text((CX - 12, PY + 284 - 0), "", font=f)
        bouton(d, B_CREER, "Créer un compte", size=22)
    elif quoi == "form":
        case(d, CASE_MAIL, "Adresse mail", kw.get("mail", ""), kw.get("f") == "mail")
        case(d, CASE_MDP, "Mot de passe", kw.get("mdp", ""), kw.get("f") == "mdp")
        bouton(d, B_VALID, "Valider", fill=(232, 235, 242))
    elif quoi == "code":
        d.text((CX - 300, PY + 90), "Nous vous avons envoyé un code.", font=F(22, "s"), fill=INK)
        case(d, CASE_CODE, "Code reçu", kw.get("code", ""), kw.get("f") == "code")
        bouton(d, B_VALID, "Valider", fill=(232, 235, 242))
    elif quoi == "ok":
        d.ellipse([CX - 50, PY + 110, CX + 50, PY + 210], fill=VERT)
        d.line([CX - 24, PY + 162, CX - 6, PY + 182, CX + 28, PY + 138], fill=(255, 255, 255), width=10)
        f = F(30, "b"); t = kw.get("msg", "Votre compte est créé."); tw = d.textlength(t, font=f); d.text((CX - tw / 2, PY + 240), t, font=f, fill=INK)
    elif quoi == "fc_choix":
        d.text((CX - 420, PY + 76), "Choisissez un compte que vous avez déjà :", font=F(22, "s"), fill=INK)
        for i, n in enumerate(COMPTES): bouton(d, compte_rect(i), n, fill=(248, 248, 252), size=21, bold=False)
    elif quoi == "fc_saisie":
        d.text((CX - 260, PY + 366), "Compte choisi : impots.gouv.fr (dessin simplifié)", font=F(19, "s"), fill=GRIS)
        case(d, CASE_MAIL, "Identifiant", kw.get("mail", ""), kw.get("f") == "mail")
        case(d, CASE_MDP, "Mot de passe", kw.get("mdp", ""), kw.get("f") == "mdp")
        bouton(d, B_VALID, "Valider", fill=(232, 235, 242))
    elif quoi == "fc_cont":
        f = F(24, "s"); t = "Vous êtes identifié."; tw = d.textlength(t, font=f); d.text((CX - tw / 2, PY + 170), t, font=f, fill=INK)
        bouton(d, B_CONT, "Continuer", fill=(232, 235, 242), size=24)

def screen(quoi=None, **kw):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if quoi:
        N.browser(d, typed="demarches.exemple.fr", page=None)
        d.rectangle([BX + 2, PY + 1, BX + BW - 2, BY + BH - 2], fill=(255, 255, 255))
        d.rectangle([BX + 14, BY + 12, BX + 296, BY + 38], fill=(250, 250, 252)); d.text((BX + 50, BY + 12), "Mon espace démarches", font=F(17), fill=(30, 30, 30))
        page(d, quoi, **kw)
    return im

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None):
    c = R.center(r); tc = 0.6 * D
    im = (after if t >= tc + 0.3 else before)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    R.caption(d, cap); return im

def typing(full, t, t0, t1):
    return full[:int(len(full) * max(0, min(1, (t - t0) / max(0.01, t1 - t0))))]

# ---------- illustrations ----------
def boite(d, x, y, s=1.0, nom="Mme MARTIN"):
    d.rectangle([x - 8 * s, y + 70 * s, x + 8 * s, y + 200 * s], fill=(90, 70, 50))
    d.rounded_rectangle([x - 110 * s, y - 60 * s, x + 110 * s, y + 80 * s], 18, fill=(255, 199, 44), outline=INK, width=4)
    d.rectangle([x - 70 * s, y - 20 * s, x + 70 * s, y], fill=INK)
    f = F(int(24 * s), "b"); tw = d.textlength(nom, font=f); d.text((x - tw / 2, y + 22 * s), nom, font=f, fill=INK)

def cle(d, x, y, s=1.0, col=(255, 199, 44)):
    d.ellipse([x - 44 * s, y - 44 * s, x + 44 * s, y + 44 * s], fill=col, outline=INK, width=4)
    d.ellipse([x - 16 * s, y - 16 * s, x + 16 * s, y + 16 * s], fill=(255, 255, 255), outline=INK, width=3)
    d.rectangle([x + 40 * s, y - 10 * s, x + 200 * s, y + 10 * s], fill=col, outline=INK, width=3)
    for k in (130, 170): d.rectangle([x + k * s, y + 10 * s, x + (k + 18) * s, y + 40 * s], fill=col, outline=INK, width=3)

def badge(d, txt, at, col):
    f = F(30, "b"); tw = d.textlength(txt, font=f); x, y = at
    d.rounded_rectangle([x - tw / 2 - 20, y - 8, x + tw / 2 + 20, y + 48], 14, fill=col)
    d.text((x - tw / 2, y), txt, font=f, fill=(255, 255, 255))

def telephone(d, x, y, code_visible):
    d.rounded_rectangle([x - 90, y - 170, x + 90, y + 170], 22, fill=(40, 44, 54))
    d.rounded_rectangle([x - 78, y - 150, x + 78, y + 150], 10, fill=(245, 246, 250))
    if code_visible:
        d.rounded_rectangle([x - 70, y - 100, x + 70, y + 10], 12, fill=(220, 235, 250))
        d.text((x - 58, y - 92), "SMS", font=F(18, "b"), fill=BLEU)
        d.text((x - 58, y - 66), "Votre code :", font=F(18), fill=INK)
        d.text((x - 58, y - 38), CODE, font=F(26, "b"), fill=INK)

def portes(d, p):
    for i in range(5):
        x = 330 + i * 160; y = 330
        ouverte = p > 0.35 + i * 0.1
        d.rectangle([x - 55, y - 110, x + 55, y + 110], fill=(120, 80, 45) if not ouverte else (250, 236, 200), outline=INK, width=3)
        if ouverte: d.polygon([(x - 55, y - 110), (x - 15, y - 95), (x - 15, y + 125), (x - 55, y + 110)], fill=(150, 100, 60), outline=INK)
        else: d.ellipse([x + 30, y - 6, x + 42, y + 6], fill=YEL)

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Créer un compte en ligne", ["et FranceConnect", "Aide-mémoire n° 21 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); cle(d, W / 2 - 100, 400, 0.9); return im
    if sid == "intro":
        im = screen("accueil"); d = ImageDraw.Draw(im); R.caption(d, cap); return im
    if sid == "compte":
        im = O.room(); d = ImageDraw.Draw(im); boite(d, 400, 260)
        if p > 0.5: badge(d, "identifiant", (850, 220), VIO)
        if p > 0.7: badge(d, "+ mot de passe", (850, 320), VIO)
        R.caption(d, cap); return im
    if sid == "identifiant":
        im = O.room(); d = ImageDraw.Draw(im)
        badge(d, "Identifiant = qui vous êtes", (W / 2, 170), VIO)
        if p > 0.4: O.label(d, "votre adresse mail", (W / 2 - 230, 320))
        if p > 0.6: O.label(d, "ou un numéro", (W / 2 + 250, 320))
        R.caption(d, cap); return im
    if sid == "motdepasse":
        im = O.room(); d = ImageDraw.Draw(im); cle(d, 420, 300, 1.4)
        if p > 0.45: badge(d, "SECRET", (900, 230), (255, 122, 89))
        if p > 0.65: O.label(d, "ne le donnez à personne", (900, 330))
        R.caption(d, cap); return im
    if sid == "bonmdp":
        im = O.room(); d = ImageDraw.Draw(im)
        if p > 0.15: badge(d, "au moins 12 caractères", (W / 2, 120), VERT)
        if p > 0.45:
            ph = [("Mon", "M"), ("chat", "c"), ("Félix", "F"), ("a", "a"), ("3", "3"), ("ans", "a"), ("!", "!")]
            d.text((160, 220), "EXEMPLE (à ne pas utiliser tel quel) :", font=F(22, "s"), fill=GRIS)
            x = 160
            for w_, l_ in ph:
                f = F(36, "b"); tw = d.textlength(w_ + " ", font=f)
                d.text((x, 270), w_, font=f, fill=INK)
                if p > 0.7: d.text((x + 4, 340), l_, font=F(44, "b"), fill=VIO)
                x += tw + 14
            if p > 0.7:
                O.label(d, "première lettre de chaque mot", (W / 2, 430))
        R.caption(d, cap); return im
    if sid == "creer":
        q = 0.3 * D
        if t < q: return act(lambda: screen("accueil"), lambda: screen("form"), B_CREER, (W / 2, 600), t, q / 0.9, cap, show_loupe=False)
        tt = t - q; L = D - q
        if tt < 0.5 * L: im = screen("form", mail=typing(MAIL, tt, 0, 0.45 * L), f="mail"); r = CASE_MAIL
        else: im = screen("form", mail=MAIL, mdp=typing(MDP, tt, 0.5 * L, 0.9 * L), f="mdp"); r = CASE_MDP
        d = ImageDraw.Draw(im); R.highlight(d, r, t); R.caption(d, cap); return im
    if sid == "code":
        if p < 0.4:
            im = screen("code"); d = ImageDraw.Draw(im)
            d.rectangle([900, 140, 1180, 560], fill=(240, 242, 248)); telephone(d, 1040, 350, p > 0.12)
            if p > 0.15: R.highlight(d, (965, 245, 1115, 360), t)
        elif p < 0.8:
            im = screen("code", code=typing(CODE, t, 0.42 * D, 0.7 * D), f="code"); d = ImageDraw.Draw(im); R.highlight(d, CASE_CODE, t)
        else:
            return act(lambda: screen("code", code=CODE), lambda: screen("ok"), B_VALID, R.center(CASE_CODE), t - 0.8 * D, 0.2 * D / 0.9, cap, show_loupe=False)
        R.caption(d, cap); return im
    if sid == "codesecret":
        if p < 0.65:
            im = O.room(); d = ImageDraw.Draw(im); telephone(d, 400, 330, True)
            badge(d, "SECRET", (850, 200), (255, 122, 89))
            if p > 0.25: O.label(d, "ne le donnez jamais", (850, 300)); O.label(d, "à quelqu'un qui vous appelle", (850, 350))
        else:
            im = screen("ok"); d = ImageDraw.Draw(im); O.label(d, "Bravo !", (W / 2, PY + 320))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et prenez le temps de relire."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "fc_quoi":
        im = O.room(); d = ImageDraw.Draw(im)
        badge(d, "FranceConnect", (W / 2, 140), VIO)
        if p > 0.3: O.label(d, "la solution de l'État", (W / 2, 240))
        if p > 0.55: O.label(d, "avec un compte que vous avez déjà", (W / 2, 300))
        R.caption(d, cap); return im
    if sid == "fc_cle":
        im = O.room(); d = ImageDraw.Draw(im); cle(d, 120, 560, 0.7); portes(d, p)
        R.caption(d, cap); return im
    if sid == "fc_bouton":
        return act(lambda: screen("accueil"), lambda: screen("fc_choix"), B_FC, (W / 2, 640), t, D, cap, place=(1060, 330))
    if sid == "fc_choix":
        r = compte_rect(0)
        return act(lambda: screen("fc_choix"), lambda: screen("fc_saisie"), r, (W / 2, 640), t, D, cap, place=(980, 420))
    if sid == "fc_saisie":
        L = D
        if p < 0.45: im = screen("fc_saisie", mail=typing("1234567890123", t, 0.05 * L, 0.4 * L), f="mail"); r = CASE_MAIL
        else: im = screen("fc_saisie", mail="1234567890123", mdp=typing(MDP, t, 0.5 * L, 0.85 * L), f="mdp"); r = CASE_MDP
        d = ImageDraw.Draw(im); R.highlight(d, r, t); R.caption(d, cap); return im
    if sid == "fc_retour":
        q = 0.5 * D
        if t < q: return act(lambda: screen("fc_cont"), lambda: screen("ok", msg="Vous êtes connecté."), B_CONT, (W / 2, 640), t, q / 0.9, cap, place=(1060, 330))
        im = screen("ok", msg="Vous êtes connecté."); d = ImageDraw.Draw(im); O.label(d, "Bravo !", (W / 2, PY + 320)); R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Sur le site d'une démarche,", "cherchez le bouton", "« S'identifier avec FranceConnect »."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Cherchez le bouton", "« S'identifier avec FranceConnect »."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 4; k = int(min(3, t // q)); tt = t - k * q
        if k == 0: return act(lambda: screen("accueil"), lambda: screen("fc_choix"), B_FC, (W / 2, 640), tt, q / 0.9, cap, show_loupe=False)
        if k == 1: return act(lambda: screen("fc_choix"), lambda: screen("fc_saisie"), compte_rect(0), R.center(B_FC), tt, q / 0.9, cap, show_loupe=False)
        if k == 2:
            im = screen("fc_saisie", mail="1234567890123", mdp=typing(MDP, tt, 0, 0.8 * q), f="mdp"); d = ImageDraw.Draw(im); R.caption(d, cap); return im
        return act(lambda: screen("fc_cont"), lambda: screen("ok", msg="Vous êtes connecté."), B_CONT, (W / 2, 640), tt, q / 0.9, cap, show_loupe=False)
    if sid == "resume":
        return R.card("À retenir", ["Un compte = identifiant + mot de passe", "Le code reçu : à personne !", "FranceConnect : un seul compte", "pour de nombreuses démarches"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
