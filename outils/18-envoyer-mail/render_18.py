"""Vidéo « 18 - Envoyer et recevoir un mail » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_18.py script.json durations.json out.mp4
        python3 render_18.py --estimate script.json durations.json
Messagerie FICTIVE et NEUTRE (aucun logo, aucune marque, aucune charte de site réel), dans une fenêtre de navigateur
simplifiée. Réutilise ../render_01.py (fond, barre des tâches, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes).
Libellés écrits tels quels (voir sources_18.md) : « Boîte de réception », « Nouveau message » (parfois « Écrire »),
« À », « Objet », « Envoyer », « Répondre ».
Adresses et noms inventés (domaine « exemple.fr », affiché seulement).
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, ".."))
import render_01 as R
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (30, 30, 40); BLEU = (0, 103, 192); GRIS = (90, 95, 110); VIOLET = (147, 17, 126)
BX, BY, BW, BH = 70, 34, 1140, 600            # fenêtre du navigateur
TOP = BY + 78                                  # début de la messagerie
SIDE_W = 230
MOI = "marie.dupont@exemple.fr"

RECUS = [("Club de lecture", "Prochaine réunion", "Bonjour Marie, la prochaine réunion a lieu jeudi à 14 h.", True),
         ("Paul Martin", "Photos du jardin", "Voici les photos promises.", False),
         ("Pharmacie du Centre", "Votre commande", "Votre commande est prête.", False)]

# ---------- géométrie ----------
def rect(name):
    if name == "nouveau": return (BX + 18, TOP + 16, BX + SIDE_W - 18, TOP + 66)
    if name == "boite": return (BX + 10, TOP + 86, BX + SIDE_W - 10, TOP + 130)
    if name == "envoyes": return (BX + 10, TOP + 134, BX + SIDE_W - 10, TOP + 178)
    if name.startswith("mail:"):
        i = int(name[5:]); y = TOP + 64 + i * 74; return (BX + SIDE_W + 12, y, BX + BW - 16, y + 68)
    if name == "repondre": return (BX + SIDE_W + 30, TOP + 360, BX + SIDE_W + 200, TOP + 408)
    # fenêtre Nouveau message
    if name == "compose": return (BX + 470, BY + 110, BX + BW - 30, BY + BH - 20)
    cx0, cy0, cx1, cy1 = BX + 470, BY + 110, BX + BW - 30, BY + BH - 20
    if name == "case_a": return (cx0 + 14, cy0 + 56, cx1 - 14, cy0 + 100)
    if name == "objet": return (cx0 + 14, cy0 + 106, cx1 - 14, cy0 + 150)
    if name == "texte": return (cx0 + 14, cy0 + 160, cx1 - 14, cy1 - 76)
    if name == "envoyer": return (cx0 + 16, cy1 - 64, cx0 + 170, cy1 - 16)
    raise KeyError(name)

def C(name): return R.center(rect(name))

# ---------- dessins ----------
def env_icon(d, x, y, s=1.0, col=VIOLET):
    d.rounded_rectangle([x, y, x + 60 * s, y + 42 * s], 5, fill=(255, 255, 255), outline=col, width=max(2, int(3 * s)))
    d.line([x + 2, y + 3, x + 30 * s, y + 24 * s, x + 60 * s - 2, y + 3], fill=col, width=max(2, int(3 * s)))

def cross(d, x, y, s, col):
    d.line([x, y, x + s, y + s], fill=col, width=3); d.line([x, y + s, x + s, y], fill=col, width=3)

def wctl(d, x, y, col):
    d.line([x, y + 8, x + 14, y + 8], fill=col, width=2); d.rectangle([x + 40, y, x + 54, y + 14], outline=col, width=2); cross(d, x + 80, y, 14, col)

def pen(d, x, y):
    d.line([x + 2, y + 20, x + 18, y + 4], fill=INK, width=5); d.polygon([(x, y + 24), (x + 2, y + 17), (x + 6, y + 22)], fill=INK)

def larrow(d, x, y):
    d.line([x + 4, y + 8, x + 18, y + 8, x + 22, y + 14, x + 22, y + 20], fill=INK, width=3, joint="curve")
    d.polygon([(x, y + 8), (x + 8, y + 2), (x + 8, y + 14)], fill=INK)

def browser(d, url="messagerie"):
    d.rounded_rectangle([BX + 6, BY + 8, BX + BW + 6, BY + BH + 8], 10, fill=(10, 30, 70))
    d.rounded_rectangle([BX, BY, BX + BW, BY + BH], 10, fill=(255, 255, 255), outline=(150, 160, 180), width=2)
    d.rounded_rectangle([BX, BY, BX + BW, BY + 70], 10, fill=(232, 236, 244)); d.rectangle([BX, BY + 50, BX + BW, BY + 70], fill=(232, 236, 244))
    d.rounded_rectangle([BX + 14, BY + 8, BX + 260, BY + 34], 7, fill=(255, 255, 255))
    env_icon(d, BX + 24, BY + 13, 0.27, BLEU); d.text((BX + 50, BY + 11), "Ma messagerie", font=F(15, "s"), fill=INK)
    wctl(d, BX + BW - 120, BY + 12, (60, 60, 60))
    d.rounded_rectangle([BX + 14, BY + 40, BX + BW - 14, BY + 66], 12, fill=(255, 255, 255), outline=(205, 210, 220))
    d.text((BX + 32, BY + 43), "Adresse de votre messagerie", font=F(15), fill=GRIS)
    d.line([BX + 2, TOP - 6, BX + BW - 2, TOP - 6], fill=(220, 224, 230), width=2)

def side(d, sel="boite", unread=1):
    d.rectangle([BX + 2, TOP - 5, BX + SIDE_W, BY + BH - 4], fill=(246, 247, 251))
    r = rect("nouveau"); d.rounded_rectangle(r, 14, fill=(255, 225, 140), outline=(200, 160, 40), width=2)
    pen(d, r[0] + 14, r[1] + 14); d.text((r[0] + 40, r[1] + 13), "Nouveau message", font=F(16, "b"), fill=INK)
    for key, lab in (("boite", "Boîte de réception"), ("envoyes", "Messages envoyés")):
        r = rect(key)
        if sel == key: d.rounded_rectangle(r, 10, fill=(214, 228, 248))
        env_icon(d, r[0] + 10, r[1] + 14, 0.3, INK)
        d.text((r[0] + 40, r[1] + 11), lab, font=F(17, "b" if key == "boite" and unread else "r"), fill=INK)
    for k in range(3): d.rounded_rectangle([BX + 30, TOP + 200 + k * 40, BX + 170 - 25 * (k % 2), TOP + 214 + k * 40], 5, fill=(225, 228, 234))

def liste(d, mails):
    d.text((BX + SIDE_W + 20, TOP + 16), "Boîte de réception", font=F(24, "b"), fill=INK)
    for i, (who, obj, txt, nonlu) in enumerate(mails):
        r = rect(f"mail:{i}")
        d.rounded_rectangle(r, 8, fill=(255, 255, 255) if nonlu else (247, 248, 251), outline=(225, 228, 235))
        env_icon(d, r[0] + 14, r[1] + 20, 0.4, VIOLET if nonlu else GRIS)
        w = "b" if nonlu else "r"
        d.text((r[0] + 54, r[1] + 10), who, font=F(19, w), fill=INK)
        d.text((r[0] + 54, r[1] + 38), obj + "  –  " + txt[:40], font=F(16, w), fill=INK if nonlu else GRIS)
        d.text((r[2] - 70, r[1] + 12), ("10:42", "Hier", "Lun.", "10:44")[i % 4], font=F(15, w), fill=INK)

def lecture(d, mail):
    who, obj, txt, _ = mail
    x = BX + SIDE_W + 30
    d.text((x, TOP + 16), "← Boîte de réception", font=F(17), fill=BLEU)
    d.text((x, TOP + 60), obj, font=F(30, "b"), fill=INK)
    d.ellipse([x, TOP + 116, x + 50, TOP + 166], fill=(200, 210, 235)); d.text((x + 16, TOP + 126), who[0], font=F(24, "b"), fill=INK)
    d.text((x + 64, TOP + 116), who, font=F(20, "b"), fill=INK)
    d.text((x + 64, TOP + 144), "à moi", font=F(16), fill=GRIS)
    yy = TOP + 196
    for ln in [txt, "", "Bien cordialement."]:
        d.text((x, yy), ln, font=F(20), fill=INK); yy += 32
    r = rect("repondre"); d.rounded_rectangle(r, 22, fill=(255, 255, 255), outline=(150, 155, 170), width=2)
    larrow(d, r[0] + 18, r[1] + 14); d.text((r[0] + 52, r[1] + 11), "Répondre", font=F(19, "s"), fill=INK)

def compose(d, a="", objet="", texte="", titre="Nouveau message", focus=None):
    r = rect("compose")
    d.rounded_rectangle([r[0] + 6, r[1] + 8, r[2] + 6, r[3] + 8], 12, fill=(120, 125, 140))
    d.rounded_rectangle(r, 12, fill=(255, 255, 255), outline=(150, 155, 170), width=2)
    d.rounded_rectangle([r[0], r[1], r[2], r[1] + 46], 12, fill=(60, 64, 80)); d.rectangle([r[0], r[1] + 30, r[2], r[1] + 46], fill=(60, 64, 80))
    d.text((r[0] + 18, r[1] + 11), titre, font=F(19, "b"), fill=(255, 255, 255)); cross(d, r[2] - 30, r[1] + 16, 14, (255, 255, 255))
    for key, lab, val in (("case_a", "À", a), ("objet", "Objet", objet)):
        q = rect(key)
        if focus == key: d.rectangle(q, fill=(240, 246, 255))
        d.line([q[0], q[3], q[2], q[3]], fill=(210, 214, 222), width=2)
        d.text((q[0] + 6, q[1] + 10), lab, font=F(19, "s"), fill=GRIS)
        d.text((q[0] + 80, q[1] + 10), val, font=F(19), fill=INK)
        if focus == key: cx = q[0] + 82 + d.textlength(val, font=F(19)); d.line([cx, q[1] + 10, cx, q[1] + 36], fill=INK, width=2)
    q = rect("texte")
    if focus == "texte": d.rectangle(q, fill=(240, 246, 255))
    yy = q[1] + 8
    lines = texte.split("\n") if texte else [""]
    for ln in lines:
        d.text((q[0] + 6, yy), ln, font=F(19), fill=INK); yy += 30
    if focus == "texte":
        cx = q[0] + 8 + d.textlength(lines[-1], font=F(19)); d.line([cx, yy - 28, cx, yy - 4], fill=INK, width=2)
    e = rect("envoyer"); d.rounded_rectangle(e, 22, fill=BLEU)
    d.text((e[0] + 30, e[1] + 11), "Envoyer", font=F(20, "b"), fill=(255, 255, 255))
    for k in range(4): d.rounded_rectangle([e[2] + 24 + k * 44, e[1] + 14, e[2] + 46 + k * 44, e[1] + 34], 4, fill=(215, 218, 226))

def screen(view="liste", mails=None, unread=1, comp=None, mail=None):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 150, 140], fill=R.BG.getpixel((80, 80)))   # cache l'icône du bureau sous la fenêtre
    browser(d); side(d, "boite", unread)
    if view == "liste": liste(d, mails if mails is not None else RECUS)
    elif view == "lecture": lecture(d, mail or RECUS[0])
    if comp is not None:
        liste(d, mails if mails is not None else RECUS) if view == "vide" else None
        compose(d, **comp)
    return im

def toast(d, txt="Message envoyé"):
    f = F(22, "s"); tw = d.textlength(txt, font=f)
    d.rounded_rectangle([BX + 24, BY + BH - 70, BX + 60 + tw, BY + BH - 22], 10, fill=(40, 44, 60))
    d.text((BX + 42, BY + BH - 60), txt, font=f, fill=(255, 255, 255))

def big(d, txt, y=None):
    f = F(52, "b"); tw = d.textlength(txt, font=f)
    d.text((W / 2 - tw / 2, y or H / 2 + 90), txt, font=f, fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))

# ---------- gestes ----------
def click(base, after, target, t, D, cap, start, t_click=0.55, loupe=False, loupe_place=None):
    c = R.center(target); tc = t_click * D
    im = (after if t >= tc + 0.3 else base)(); d = ImageDraw.Draw(im)
    if t < tc + 0.3:
        clean = im.copy(); R.highlight(d, target, t); R.arrow(d, target, t)
        if loupe and t > 0.15 * D: R.loupe(im, target, place=loupe_place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *R.move(t, 0.08 * D, tc - 0.15 * D, start, (c[0] - 4, c[1] - 4)))
    R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    R.caption(d, cap); return im

def typing(make, field, word, t, D, cap, p0=0.2, p1=0.75, loupe_place=None):
    p = t / D; k = int(len(word) * R.ease((p - p0) / (p1 - p0))) if p > p0 else 0
    im = make(word[:k]); d = ImageDraw.Draw(im); r = rect(field); clean = im.copy()
    R.highlight(d, r, t)
    if p > 0.1 and loupe_place: R.loupe(im, (r[0], r[1], r[0] + 260, r[3]), place=loupe_place, clean=clean); d = ImageDraw.Draw(im)
    R.caption(d, cap); return im

def label(d, txt, xy):
    d.text(xy, txt, font=F(30, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))

# ---------- scènes ----------
ADR = "paul.martin@exemple.fr"
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Envoyer et recevoir", ["un mail", "", "Aide-mémoire n° 18 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); env_icon(d, W / 2 - 60, 360, 2.0); return im
    if sid == "intro":
        im = R.card("", [], None); d = ImageDraw.Draw(im)
        x = R.lerp(200, W - 380, R.ease((p - 0.1) / 0.5))
        d.ellipse([170, 190, 330, 350], outline=(15, 40, 100), width=6); d.text((205, 245), "Moi", font=F(40, "b"), fill=(15, 40, 100))
        d.ellipse([W - 330, 190, W - 170, 350], outline=(15, 40, 100), width=6); d.text((W - 300, 245), "Paul", font=F(40, "b"), fill=(15, 40, 100))
        for k in range(8): d.line([360 + k * 70, 270, 390 + k * 70, 270], fill=(180, 185, 200), width=4)
        env_icon(d, x + 60, 240, 1.4)
        if p > 0.45:
            for i, s in enumerate(["quelques secondes", "sans timbre"]):
                tw = d.textlength(s, font=F(34, "b")); d.text((W / 2 - tw / 2, 390 + i * 52), s, font=F(34, "b"), fill=VIOLET)
        R.caption(d, cap); return im
    if sid == "boite":
        im = click(lambda: screen("liste"), lambda: screen("liste"), rect("boite"), t, D, cap, (W / 2, H / 2), t_click=0.45, loupe=True, loupe_place=(BX + 700, 420))
        if p > 0.6:
            d = ImageDraw.Draw(im); R.highlight(d, (rect("mail:0")[0], rect("mail:0")[1], rect("mail:2")[2], rect("mail:2")[3]), t)
            label(d, "Les mails reçus", (BX + 600, TOP + 300))
        return im
    if sid == "lire":
        im = click(lambda: screen("liste"), lambda: screen("lecture", unread=0), rect("mail:0"), t, D, cap, C("boite"), t_click=0.35)
        if p > 0.55:
            d = ImageDraw.Draw(im); x = BX + SIDE_W + 30
            R.highlight(d, (x - 6, TOP + 110, x + 330, TOP + 172), t); label(d, "Qui l'a envoyé", (x + 360, TOP + 120))
        return im
    if sid == "nouveau":
        im = click(lambda: screen("liste"), lambda: screen("liste", comp={}), rect("nouveau"), t, D, cap, (W / 2, H / 2), t_click=0.5, loupe=True, loupe_place=(BX + 700, 400))
        if 0.25 < p < 0.55:
            d = ImageDraw.Draw(im); label(d, "parfois « Écrire »", (BX + 20, TOP + 250))
        return im
    if sid == "case_a":
        if p < 0.2:
            return click(lambda: screen("liste", comp={}), lambda: screen("liste", comp={"focus": "case_a"}), rect("case_a"), t, 0.2 * D, cap, C("nouveau"))
        im = typing(lambda s: screen("liste", comp={"a": s, "focus": "case_a"}), "case_a", ADR, t - 0.2 * D, 0.8 * D, cap, 0.05, 0.55, loupe_place=(BX + 250, 420))
        if p > 0.65:
            d = ImageDraw.Draw(im); r = rect("case_a"); x = r[0] + 82 + d.textlength("paul.martin", font=F(19))
            R.highlight(d, (x - 4, r[1] + 6, x + 24, r[3] - 6), t); label(d, "@ = arobase", (r[0] + 40, r[3] + 120))
        return im
    if sid == "objet":
        if p < 0.2:
            return click(lambda: screen("liste", comp={"a": ADR}), lambda: screen("liste", comp={"a": ADR, "focus": "objet"}), rect("objet"), t, 0.2 * D, cap, C("case_a"))
        return typing(lambda s: screen("liste", comp={"a": ADR, "objet": s, "focus": "objet"}), "objet", "Bonjour", t - 0.2 * D, 0.8 * D, cap, 0.1, 0.5, loupe_place=(BX + 250, 420))
    if sid == "texte":
        msg = "Bonjour Paul,\nMerci pour les photos du jardin !\nÀ bientôt,\nMarie"
        if p < 0.15:
            return click(lambda: screen("liste", comp={"a": ADR, "objet": "Bonjour"}), lambda: screen("liste", comp={"a": ADR, "objet": "Bonjour", "focus": "texte"}), rect("texte"), t, 0.15 * D, cap, C("objet"))
        return typing(lambda s: screen("liste", comp={"a": ADR, "objet": "Bonjour", "texte": s, "focus": "texte"}), "texte", msg, t - 0.15 * D, 0.85 * D, cap, 0.05, 0.8)
    if sid == "envoyer":
        msg = "Bonjour Paul,\nMerci pour les photos du jardin !\nÀ bientôt,\nMarie"
        full = {"a": ADR, "objet": "Bonjour", "texte": msg}
        im = click(lambda: screen("liste", comp=full), lambda: screen("liste"), rect("envoyer"), t, D, cap, C("texte"), t_click=0.45, loupe=True, loupe_place=(BX + 250, 400))
        if p > 0.5:
            d = ImageDraw.Draw(im); toast(d); big(d, "Bravo !", H / 2 - 40)
        return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "repondre":
        mail = RECUS[1]; rep = {"a": ADR, "objet": "RE: Photos du jardin", "titre": "Répondre"}
        if p < 0.4:
            im = click(lambda: screen("lecture", unread=0, mail=mail), lambda: screen("lecture", unread=0, mail=mail, comp=rep), rect("repondre"), t, 0.4 * D, cap, (W / 2, H / 2 - 100), t_click=0.6, loupe=True, loupe_place=(BX + 820, 300))
            return im
        if p < 0.75:
            im = screen("lecture", unread=0, mail=mail, comp=rep); d = ImageDraw.Draw(im)
            R.highlight(d, (rect("case_a")[0], rect("case_a")[1], rect("objet")[2], rect("objet")[3]), t); label(d, "Déjà remplis !", (BX + 600, rect("objet")[3] + 120))
            R.caption(d, cap); return im
        rep2 = dict(rep, texte="Merci Paul !")
        im = click(lambda: screen("lecture", unread=0, mail=mail, comp=rep2), lambda: screen("lecture", unread=0, mail=mail), rect("envoyer"), t - 0.75 * D, 0.25 * D, cap, C("texte"), t_click=0.6)
        if p > 0.93: d = ImageDraw.Draw(im); toast(d)
        return im
    if sid == "panique":
        im = R.card("Pas de panique !", ["Un mail attendu n'est pas arrivé ?", "1. Attendez quelques minutes.", "2. Regardez dans les courriers", "indésirables (spams)."], None)
        return im
    if sid == "exercice":
        return R.card("Exercice", ["Envoyez un mail à vous-même :", "À : votre propre adresse", "Objet : Essai · Message : Bonjour !"], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Envoyez-vous un mail :", "objet « Essai », message « Bonjour ! »."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        if p < 0.15:
            return click(lambda: screen("liste"), lambda: screen("liste", comp={}), rect("nouveau"), t, 0.15 * D, cap, (W / 2, H / 2))
        if p < 0.4:
            return typing(lambda s: screen("liste", comp={"a": s, "focus": "case_a"}), "case_a", MOI, t - 0.15 * D, 0.25 * D, cap, 0.05, 0.7)
        if p < 0.52:
            return typing(lambda s: screen("liste", comp={"a": MOI, "objet": s, "focus": "objet"}), "objet", "Essai", t - 0.4 * D, 0.12 * D, cap, 0.05, 0.7)
        if p < 0.64:
            return typing(lambda s: screen("liste", comp={"a": MOI, "objet": "Essai", "texte": s, "focus": "texte"}), "texte", "Bonjour !", t - 0.52 * D, 0.12 * D, cap, 0.05, 0.7)
        if p < 0.76:
            full = {"a": MOI, "objet": "Essai", "texte": "Bonjour !"}
            return click(lambda: screen("liste", comp=full), lambda: screen("liste"), rect("envoyer"), t - 0.64 * D, 0.12 * D, cap, C("texte"), t_click=0.6)
        mails = [("Moi", "Essai", "Bonjour !", True)] + RECUS[1:] if p > 0.84 else RECUS
        im = screen("liste", mails=[(m[0], m[1], m[2], m[3] if i == 0 or p <= 0.84 else False) for i, m in enumerate(mails)], unread=1)
        d = ImageDraw.Draw(im)
        if p <= 0.84: toast(d)
        else: R.highlight(d, rect("mail:0"), t); big(d, "Bravo !", H / 2 + 60)
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["1. Nouveau message", "2. À : l'adresse · Objet : le sujet", "3. Le message, puis Envoyer", "4. Pour répondre : Répondre"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
