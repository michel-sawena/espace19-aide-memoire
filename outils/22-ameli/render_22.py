"""Vidéo « 22 - ameli.fr » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_22.py script.json durations.json out.mp4
        python3 render_22.py --estimate script.json durations.json
Réutilise ../render_01.py, ../01-ordinateur/render_01_ordinateur.py et ../12-internet/render_12.py (fenêtre du navigateur).
Écrans du site SIMPLIFIÉS et NEUTRES : ni logo, ni couleurs, ni charte de l'Assurance Maladie (règle de Michel).
Libellés écrits tels quels seulement s'ils sont confirmés (voir sources_22.md) : « Numéro de sécurité sociale »,
« Mot de passe », « Me connecter », « Mot de passe oublié ? », « Créer un compte », « Code de sécurité »,
« Attestation de droits ». Numéros et noms : exemples inventés, marqués « EXEMPLE ».
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as N
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); VERT = (43, 179, 163); GRIS = (90, 96, 110); BLEU = (0, 103, 192)
ADRESSE = "ameli.fr"
NUM = "1 55 03 75 123 456"      # EXEMPLE inventé (13 chiffres)
CODE = "482 913"                 # EXEMPLE inventé
BX, BY, BW, BH, PAGE_Y, ADDR = N.BX, N.BY, N.BW, N.BH, N.PAGE_Y, N.ADDR
CX = BX + BW / 2

# zones cliquables du site dessiné
BTN_COMPTE = (BX + BW - 290, PAGE_Y + 22, BX + BW - 40, PAGE_Y + 72)
F_NUM = (CX - 230, PAGE_Y + 92, CX + 230, PAGE_Y + 138)
F_MDP = (CX - 230, PAGE_Y + 186, CX + 230, PAGE_Y + 232)
BTN_CO = (CX - 130, PAGE_Y + 254, CX + 130, PAGE_Y + 302)
LIEN_OUBLI = (CX - 230, PAGE_Y + 312, CX - 30, PAGE_Y + 340)
F_CODE = (CX - 150, PAGE_Y + 185, CX + 150, PAGE_Y + 239)
BTN_ATT = (BX + 560, PAGE_Y + 120, BX + BW - 60, PAGE_Y + 200)

def entete(d, sous=""):
    d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, PAGE_Y + 92], fill=(244, 245, 248))
    d.text((BX + 40, PAGE_Y + 24), "ameli.fr", font=F(34, "b"), fill=INK)
    if sous: d.text((BX + 220, PAGE_Y + 36), sous, font=F(20), fill=GRIS)
    d.text((BX + 40, BY + BH - 34), "(dessin simplifié)", font=F(16), fill=GRIS)

def champ(d, r, label, val="", focus=False, secret=False):
    d.text((r[0], r[1] - 30), label, font=F(19, "s"), fill=INK)
    d.rounded_rectangle(r, 8, fill=(255, 255, 255), outline=BLEU if focus else (150, 155, 165), width=3 if focus else 2)
    t = "•" * len(val) if secret else val
    d.text((r[0] + 14, r[1] + 10), t, font=F(22), fill=(20, 20, 20))
    if focus:
        x = r[0] + 14 + d.textlength(t, font=F(22)) + 2; d.line([x, r[1] + 10, x, r[3] - 10], fill=(20, 20, 20), width=2)

def bouton(d, r, txt, actif=True):
    d.rounded_rectangle(r, 10, fill=INK if actif else (150, 150, 160))
    f = F(22, "b"); tw = d.textlength(txt, font=f); c = R.center(r)
    d.text((c[0] - tw / 2, c[1] - 14), txt, font=f, fill=(255, 255, 255))

def personne(d, x, y, col=(255, 255, 255)):
    d.ellipse([x - 8, y - 14, x + 8, y + 2], fill=col); d.pieslice([x - 14, y + 2, x + 14, y + 30], 180, 360, fill=col)

def page_site(d):
    entete(d)
    d.rounded_rectangle(BTN_COMPTE, 10, fill=INK); personne(d, BTN_COMPTE[0] + 30, BTN_COMPTE[1] + 22)
    d.text((BTN_COMPTE[0] + 56, BTN_COMPTE[1] + 11), "Compte ameli", font=F(22, "b"), fill=(255, 255, 255))
    for i, w in enumerate((520, 440, 480)):
        d.rounded_rectangle([BX + 60, PAGE_Y + 140 + i * 60, BX + 60 + w, PAGE_Y + 168 + i * 60], 8, fill=(226, 229, 236))
    for i in range(3):
        x = BX + 640 + (i % 2) * 180; y = PAGE_Y + 130 + (i // 2) * 110
        d.rounded_rectangle([x, y, x + 160, y + 90], 12, fill=(236, 238, 243))

def page_login(d, num="", mdp="", focus=None):
    entete(d, "Compte ameli · connexion")
    champ(d, F_NUM, "Numéro de sécurité sociale", num, focus == "num")
    champ(d, F_MDP, "Mot de passe", mdp, focus == "mdp", secret=True)
    bouton(d, BTN_CO, "Me connecter")
    d.text((LIEN_OUBLI[0], LIEN_OUBLI[1]), "Mot de passe oublié ?", font=F(18), fill=BLEU)
    d.text((CX + 60, LIEN_OUBLI[1]), "Créer un compte", font=F(18), fill=BLEU)
    if num: d.text((F_NUM[2] + 14, F_NUM[1] + 12), "EXEMPLE", font=F(16, "b"), fill=(200, 60, 40))

def page_code(d, code=""):
    entete(d, "Compte ameli · connexion")
    d.text((CX - 270, PAGE_Y + 108), "Un code à 6 chiffres vous a été envoyé par mail.", font=F(20), fill=INK)
    champ(d, F_CODE, "", code, focus=True)
    d.text((F_CODE[0], F_CODE[1] - 30), "Code de sécurité", font=F(19, "s"), fill=INK)
    if code: d.text((F_CODE[2] + 14, F_CODE[1] + 16), "EXEMPLE", font=F(16, "b"), fill=(200, 60, 40))
    bouton(d, (CX - 80, PAGE_Y + 258, CX + 80, PAGE_Y + 304), "✓", True)

def page_compte(d, survol=False):
    entete(d, "Compte ameli")
    personne(d, BX + 70, PAGE_Y + 140, INK)
    d.text((BX + 100, PAGE_Y + 124), "Bonjour !", font=F(26, "b"), fill=INK)
    # remboursements : pictogramme euro + lignes (pas de libellé non confirmé)
    d.rounded_rectangle([BX + 60, PAGE_Y + 190, BX + 520, PAGE_Y + 400], 14, fill=(244, 245, 248))
    d.ellipse([BX + 80, PAGE_Y + 206, BX + 130, PAGE_Y + 256], fill=VERT); d.text((BX + 95, PAGE_Y + 212), "€", font=F(30, "b"), fill=(255, 255, 255))
    for i in range(4):
        d.rounded_rectangle([BX + 80, PAGE_Y + 276 + i * 30, BX + 480 - i * 40, PAGE_Y + 292 + i * 30], 6, fill=(214, 218, 226))
    d.rounded_rectangle(BTN_ATT, 14, fill=(255, 246, 214) if survol else (244, 245, 248), outline=INK, width=2)
    d.rectangle([BTN_ATT[0] + 22, BTN_ATT[1] + 16, BTN_ATT[0] + 62, BTN_ATT[1] + 64], fill=(255, 255, 255), outline=INK, width=2)
    for k in range(3): d.line([BTN_ATT[0] + 30, BTN_ATT[1] + 28 + k * 10, BTN_ATT[0] + 54, BTN_ATT[1] + 28 + k * 10], fill=INK, width=2)
    d.text((BTN_ATT[0] + 80, BTN_ATT[1] + 26), "Attestation de droits", font=F(24, "b"), fill=INK)

def page_attestation(d):
    entete(d, "Compte ameli")
    x0, y0 = CX - 200, PAGE_Y + 110
    d.rectangle([x0 + 8, y0 + 8, x0 + 408, y0 + 338], fill=(200, 204, 214))
    d.rectangle([x0, y0, x0 + 400, y0 + 330], fill=(255, 255, 255), outline=INK, width=2)
    f = F(22, "b"); t = "Attestation de droits"; d.text((x0 + 200 - d.textlength(t, font=f) / 2, y0 + 20), t, font=f, fill=INK)
    for i in range(6):
        d.rounded_rectangle([x0 + 30, y0 + 80 + i * 32, x0 + 370 - (i % 3) * 50, y0 + 94 + i * 32], 5, fill=(214, 218, 226))
    f2 = F(54, "b"); t2 = "EXEMPLE"; tw = d.textlength(t2, font=f2)
    d.text((x0 + 200 - tw / 2, y0 + 250), t2, font=f2, fill=(220, 90, 70))

PAGES = {"site": page_site, "login": page_login, "code": page_code, "compte": page_compte, "attestation": page_attestation}

def browser(d, typed="", focus=False, page=None, **kw):
    """Fenêtre du navigateur de render_12, avec nos pages à la place de la page google."""
    N.browser(d, typed=typed, focus=focus, page=None)
    if page:
        d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, BY + BH - 2], fill=(255, 255, 255))
        d.rounded_rectangle([BX + 12, BY + 6, BX + 300, BY + N.TAB_H + 4], 8, fill=(250, 250, 252))
        N.globe(d, BX + 32, BY + 23, 9); d.text((BX + 50, BY + 12), "ameli.fr", font=F(17), fill=(30, 30, 30))
        PAGES[page](d, **kw)

def screen(state=None, **kw):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if state == "browser": browser(d, **kw)
    return im

def B(**kw): return lambda: screen("browser", typed=ADRESSE, **kw)

def act(before, after, r, start, t, D, cap, show_loupe=True, place=None):
    c = R.center(r); tc = 0.6 * D
    im = (after if t >= tc + 0.3 else before)(); clean = im.copy(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if show_loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    R.caption(d, cap); return im

def carte_vitale(d, x, y, s=1.0):
    d.rounded_rectangle([x, y, x + 340 * s, y + 214 * s], 18, fill=(120, 190, 120), outline=(60, 110, 60), width=3)
    d.rounded_rectangle([x + 24 * s, y + 70 * s, x + 84 * s, y + 116 * s], 6, fill=(230, 200, 90))
    d.text((x + 24 * s, y + 18 * s), "carte Vitale", font=F(int(26 * s), "b"), fill=(255, 255, 255))
    d.text((x + 24 * s, y + 140 * s), NUM + " 12", font=F(int(22 * s), "b"), fill=(30, 40, 30))
    d.text((x + 24 * s, y + 176 * s), "EXEMPLE", font=F(int(18 * s), "b"), fill=(200, 60, 40))

def telephone_message(d):
    x, y = 470, 120
    d.rounded_rectangle([x, y, x + 340, y + 420], 30, fill=(40, 44, 54)); d.rounded_rectangle([x + 16, y + 30, x + 324, y + 400], 16, fill=(250, 250, 252))
    d.rounded_rectangle([x + 30, y + 60, x + 310, y + 250], 16, fill=(232, 234, 240))
    lignes = ["EXEMPLE de faux SMS :", "Votre remboursement", "est bloqué. Donnez", "votre mot de passe :", "http://ameli-rembours…"]
    for i, l in enumerate(lignes):
        d.text((x + 44, y + 74 + i * 34), l, font=F(20, "b" if i == 0 else "r"), fill=(200, 60, 40) if i in (0, 4) else INK)
    d.line([x + 20, y + 40, x + 320, y + 270], fill=(200, 40, 40), width=12); d.line([x + 320, y + 40, x + 20, y + 270], fill=(200, 40, 40), width=12)

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Mon compte ameli", ["Aide-mémoire n° 22 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); carte_vitale(d, W / 2 - 150, 300, 0.9); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); O.draw_fixe(d)
        if p > 0.3:
            d.rounded_rectangle([890, 110, 1200, 250], 14, fill=(255, 255, 255), outline=INK, width=3)
            d.ellipse([910, 130, 960, 180], fill=VERT); d.text((924, 134), "€", font=F(30, "b"), fill=(255, 255, 255))
            d.text((975, 140), "remboursements", font=F(22, "b"), fill=INK)
            d.rectangle([915, 195, 945, 235], fill=(255, 255, 255), outline=INK, width=2); d.text((975, 200), "documents", font=F(22, "b"), fill=INK)
        if p > 0.6: O.label(d, "sans vous déplacer", (1045, 300))
        R.caption(d, cap); return im
    if sid == "avant":
        im = O.room(); d = ImageDraw.Draw(im); carte_vitale(d, 300, 170, 1.4)
        if p > 0.35: R.highlight(d, (330, 360, 300 + 340 * 1.4 - 20, 400), t)
        if p > 0.4: O.label(d, "le numéro de sécurité sociale", (640, 520))
        R.caption(d, cap); return im
    if sid == "adresse":
        tc = 0.3 * D
        if t < tc + 0.3:
            return act(lambda: screen("browser"), lambda: screen("browser", focus=True), ADDR, (W / 2, 500), t, tc / 0.6, cap, show_loupe=False)
        if t < 0.75 * D:
            n = int(len(ADRESSE) * min(1, (t - tc - 0.3) / (0.3 * D)))
            im = screen("browser", typed=ADRESSE[:n], focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
            R.loupe(im, (ADDR[0], ADDR[1], ADDR[0] + 240, ADDR[3]), place=(640, 420), clean=clean); d = ImageDraw.Draw(im)
            R.caption(d, cap); return im
        if t < 0.85 * D:
            im = screen("browser", typed=ADRESSE, focus=True); d = ImageDraw.Draw(im); R.key_enter(d, t, t > 0.8 * D)
        else:
            im = B(page="site")(); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "compte":
        return act(B(page="site"), B(page="login"), BTN_COMPTE, (W / 2, 450), t, D, cap, place=(400, 400))
    if sid == "numero":
        h = D / 2
        if t < h:
            tt = t; n = int(len(NUM) * max(0, min(1, (tt - 0.35 * h) / (0.45 * h))))
            if tt < 0.35 * h:
                return act(B(page="login"), B(page="login", focus="num"), F_NUM, (W / 2, 520), tt, 0.35 * h / 0.6 - 0.01, cap, show_loupe=False)
            im = B(page="login", num=NUM[:n], focus="num")(); clean = im.copy(); d = ImageDraw.Draw(im)
            R.highlight(d, F_NUM, t); R.caption(d, cap); return im
        tt = t - h; n = int(8 * max(0, min(1, (tt - 0.35 * h) / (0.45 * h))))
        if tt < 0.35 * h:
            return act(B(page="login", num=NUM), B(page="login", num=NUM, focus="mdp"), F_MDP, R.center(F_NUM), tt, 0.35 * h / 0.6 - 0.01, cap, show_loupe=False)
        im = B(page="login", num=NUM, mdp="x" * n, focus="mdp")(); d = ImageDraw.Draw(im)
        R.highlight(d, F_MDP, t)
        if tt > 0.6 * h: O.label(d, "le mot de passe reste caché", (640, 470))
        R.caption(d, cap); return im
    if sid == "connecter":
        return act(B(page="login", num=NUM, mdp="xxxxxxxx"), B(page="code"), BTN_CO, R.center(F_MDP), t, D, cap, place=(980, 300))
    if sid == "code":
        n = int(6 * max(0, min(1, (p - 0.45) / 0.3))); code = CODE.replace(" ", "")[:n]
        im = B(page="code", code=(code[:3] + " " + code[3:]).strip())(); d = ImageDraw.Draw(im)
        if p < 0.45:
            d.rounded_rectangle([860, 330, 1150, 470], 14, fill=(255, 255, 255), outline=INK, width=3)
            d.rectangle([880, 350, 940, 395], outline=INK, width=3); d.line([880, 350, 910, 375, 940, 350], fill=INK, width=3)
            d.text((955, 352), "Nouveau mail", font=F(20, "b"), fill=INK); d.text((880, 410), "Code : " + CODE, font=F(24, "b"), fill=VIO)
            d.text((880, 440), "EXEMPLE", font=F(16, "b"), fill=(200, 60, 40))
        else: R.highlight(d, F_CODE, t)
        if p > 0.8: O.label(d, "valable 15 minutes", (640, 470))
        R.caption(d, cap); return im
    if sid == "accueil":
        im = B(page="compte")(); d = ImageDraw.Draw(im)
        if p > 0.3: O.label(d, "Bravo !", (BX + 290, PAGE_Y + 440))
        R.caption(d, cap); return im
    if sid == "attestation":
        return act(B(page="compte"), B(page="attestation"), BTN_ATT, (BX + 300, PAGE_Y + 300), t, D * 0.6, cap, place=(400, 400)) if t < 0.6 * D \
            else (lambda im: (R.caption(ImageDraw.Draw(im), cap), im)[1])(B(page="attestation")())
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "prudence":
        im = O.room(); d = ImageDraw.Draw(im); telephone_message(d)
        if p > 0.4: O.label(d, "jamais votre mot de passe", (640, 80 + 470))
        R.caption(d, cap); return im
    if sid == "aide":
        im = B(page="login")(); d = ImageDraw.Draw(im)
        if p < 0.5: R.highlight(d, LIEN_OUBLI, t)
        else:
            d.rounded_rectangle([830, 300, 1150, 440], 16, fill=(255, 255, 255), outline=YEL, width=6)
            d.text((860, 320), "Besoin d'aide ?", font=F(24, "b"), fill=INK); d.text((860, 360), "36 46", font=F(40, "b"), fill=VIO)
            d.text((990, 372), "ou Espace 19", font=F(20, "b"), fill=INK)
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Allez sur ameli.fr", "et connectez-vous", "à votre compte."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["ameli.fr, puis Entrée,", "numéro, mot de passe, Me connecter."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        q = D / 4; k = int(t // q); tt = t - k * q
        if k == 0:
            n = int(len(ADRESSE) * min(1, tt / (0.6 * q)))
            im = screen("browser", typed=ADRESSE[:n], focus=True); d = ImageDraw.Draw(im)
            if tt > 0.65 * q: R.key_enter(d, tt, tt > 0.8 * q)
            R.caption(d, cap); return im
        if k == 1: return act(B(page="site"), B(page="login"), BTN_COMPTE, (W / 2, 450), tt, q, cap, show_loupe=False)
        if k == 2:
            n = int(len(NUM) * min(1, tt / (0.5 * q))); m = int(8 * max(0, min(1, (tt - 0.5 * q) / (0.4 * q))))
            im = B(page="login", num=NUM[:n], mdp="x" * m, focus="mdp" if m else "num")(); d = ImageDraw.Draw(im); R.caption(d, cap); return im
        return act(B(page="login", num=NUM, mdp="xxxxxxxx"), B(page="code"), BTN_CO, R.center(F_MDP), tt, q, cap, show_loupe=False)
    if sid == "resume":
        return R.card("À retenir", ["Je tape ameli.fr moi-même", "Numéro de sécurité sociale + mot de passe", "Puis « Me connecter »", "Mon mot de passe reste secret"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
