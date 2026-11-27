"""Vidéo « 20 - Le carnet d'adresses » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_20.py script.json durations.json out.mp4
        python3 render_20.py --estimate script.json durations.json
Réutilise ../render_01.py (curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes).
Écrans SIMPLIFIÉS et NEUTRES : navigateur et carnet de contacts dessinés, sans logo ni charte d'un site.
Libellés écrits tels quels (confirmés, voir sources_20.md) : « Créer un contact », « Enregistrer », « Modifier »,
« Plus » (les trois points), « Supprimer », le champ « À » d'un nouveau mail.
Les cases de la fiche ne portent pas de nom (libellés non confirmés) : un pictogramme personne / enveloppe.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, ".."))
import render_01 as R
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (32, 33, 36); GRIS = (95, 99, 104); BLEU = (26, 115, 232); FOND = (248, 249, 250); LIGNE = (218, 220, 224)
VIO = (147, 17, 126)

# ---------- géométrie ----------
BX, BY, BW, BH = 60, 88, 1160, 560          # fenêtre du navigateur
ADDR = (BX + 120, BY + 14, BX + BW - 40, BY + 50)
TOP = BY + 64                                # début de la page
SEARCH = (BX + 280, TOP + 16, BX + 900, TOP + 62)
CREATE = (BX + 24, TOP + 18, BX + 244, TOP + 74)
LIST_X = BX + 290
SAVE = (BX + BW - 200, TOP + 18, BX + BW - 40, TOP + 66)
EDIT = (BX + BW - 260, TOP + 18, BX + BW - 110, TOP + 66)
PLUS = (BX + BW - 90, TOP + 18, BX + BW - 40, TOP + 66)
MENU_SUPPR = (BX + BW - 250, TOP + 74, BX + BW - 40, TOP + 120)
FIELDS = [(BX + 360, TOP + 150, BX + 800, TOP + 200), (BX + 360, TOP + 220, BX + 800, TOP + 270), (BX + 360, TOP + 310, BX + 800, TOP + 360)]
CONTACTS = [("Annie Leroy", "annie.leroy@exemple.fr"), ("Marc Bernard", "marc.bernard@exemple.fr"), ("Paul Durand", "paul.durand@exemple.fr"), ("Sophie Dubois", "sophie.dubois@exemple.fr")]
def row_rect(i): return (LIST_X, TOP + 120 + i * 62, BX + BW - 40, TOP + 176 + i * 62)

def avatar(d, cx, cy, r, letter, col=(124, 77, 255)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    f = F(int(r * 1.1), "s"); tw = d.textlength(letter, font=f)
    d.text((cx - tw / 2, cy - r * 0.68), letter, font=f, fill=(255, 255, 255))

def person_icon(d, x, y, col=GRIS):
    d.ellipse([x + 8, y, x + 24, y + 16], outline=col, width=3); d.arc([x, y + 16, x + 32, y + 44], 180, 360, fill=col, width=3)

def mail_icon(d, x, y, col=GRIS):
    d.rectangle([x, y + 4, x + 32, y + 28], outline=col, width=3); d.line([x, y + 4, x + 16, y + 18, x + 32, y + 4], fill=col, width=3)

def button(d, r, text, primary=False, hover=False):
    fill = BLEU if primary else ((232, 240, 254) if hover else (255, 255, 255))
    d.rounded_rectangle(r, (r[3] - r[1]) // 2, fill=fill, outline=None if primary else LIGNE, width=2)
    f = F(21, "s"); tw = d.textlength(text, font=f)
    d.text(((r[0] + r[2]) / 2 - tw / 2, (r[1] + r[3]) / 2 - 13), text, font=f, fill=(255, 255, 255) if primary else BLEU)

def browser(url, typing=None):
    im = R.bg().copy(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([BX, BY, BX + BW, BY + BH], 12, fill=(255, 255, 255), outline=(170, 170, 180), width=2)
    d.rounded_rectangle([BX, BY, BX + BW, BY + 62], 12, fill=(222, 225, 230)); d.rectangle([BX, BY + 40, BX + BW, BY + 62], fill=(222, 225, 230))
    for i, x in enumerate((BX + 30, BX + 70)):
        y = BY + 32; s = -1 if i == 0 else 1
        d.line([x - 8 * s, y, x + 8 * s, y], fill=(110, 110, 120), width=3); d.line([x + 2 * s, y - 7, x + 9 * s, y, x + 2 * s, y + 7], fill=(110, 110, 120), width=3)
    d.rounded_rectangle(ADDR, 18, fill=(255, 255, 255), outline=BLEU if typing is not None else (200, 200, 205), width=2)
    txt = typing if typing is not None else url
    d.text((ADDR[0] + 22, ADDR[1] + 6), txt, font=F(20), fill=INK)
    if typing is not None:
        x = ADDR[0] + 22 + d.textlength(txt, font=F(20)); d.line([x + 2, ADDR[1] + 7, x + 2, ADDR[3] - 7], fill=INK, width=2)
    return im, d

def topbar(d, query=None):
    d.rounded_rectangle(SEARCH, 23, fill=(241, 243, 244) if query is None else (255, 255, 255), outline=None if query is None else LIGNE, width=2)
    cx, cy = SEARCH[0] + 28, (SEARCH[1] + SEARCH[3]) / 2
    d.ellipse([cx - 9, cy - 11, cx + 7, cy + 5], outline=GRIS, width=3); d.line([cx + 5, cy + 3, cx + 13, cy + 11], fill=GRIS, width=3)
    if query: d.text((SEARCH[0] + 56, SEARCH[1] + 10), query, font=F(21), fill=INK)
    else: d.text((SEARCH[0] + 56, SEARCH[1] + 11), "rechercher", font=F(20), fill=GRIS)

def sidebar(d):
    d.rounded_rectangle(CREATE, 16, fill=(194, 231, 255))
    d.text((CREATE[0] + 18, CREATE[1] + 9), "+", font=F(30, "b"), fill=INK)
    d.text((CREATE[0] + 50, CREATE[1] + 15), "Créer un contact", font=F(21, "s"), fill=INK)
    d.rounded_rectangle([BX + 24, TOP + 100, BX + 244, TOP + 140], 20, fill=(211, 227, 253))
    person_icon(d, BX + 40, TOP + 104, INK); d.text((BX + 84, TOP + 108), "Contacts", font=F(19, "s"), fill=INK)

def page_list(contacts=CONTACTS, query=None, hover=None):
    im, d = browser("contacts.google.com"); topbar(d, query); sidebar(d)
    d.text((LIST_X, TOP + 84), f"Contacts ({len(contacts)})", font=F(20, "s"), fill=GRIS)
    for i, (n, m) in enumerate(contacts):
        r = row_rect(i)
        if hover == i: d.rectangle(r, fill=(241, 243, 244))
        avatar(d, r[0] + 30, (r[1] + r[3]) / 2, 22, n[0], [(124, 77, 255), (0, 137, 123), (230, 81, 0), (194, 24, 91), (25, 118, 210)][i % 5])
        d.text((r[0] + 70, r[1] + 15), n, font=F(22, "s"), fill=INK); d.text((r[0] + 380, r[1] + 17), m, font=F(20), fill=GRIS)
    return im, d

def page_form(vals=("", "", ""), active=None, save_hover=False):
    im, d = browser("contacts.google.com"); topbar(d)
    d.text((BX + 40, TOP + 26), "←", font=F(30, "b"), fill=GRIS)
    button(d, SAVE, "Enregistrer", primary=True)
    avatar(d, BX + 200, TOP + 230, 70, (vals[0][:1] or " ").upper(), (174, 203, 250))
    person_icon(d, BX + 310, TOP + 156); mail_icon(d, BX + 310, TOP + 320)
    for i, (r, v) in enumerate(zip(FIELDS, vals)):
        d.rounded_rectangle(r, 6, fill=(255, 255, 255), outline=BLEU if active == i else (150, 150, 155), width=3 if active == i else 2)
        d.text((r[0] + 16, r[1] + 11), v, font=F(22), fill=INK)
        if active == i:
            x = r[0] + 16 + d.textlength(v, font=F(22)); d.line([x + 2, r[1] + 10, x + 2, r[3] - 10], fill=INK, width=2)
    return im, d

def page_fiche(name, mail, menu=False):
    im, d = browser("contacts.google.com"); topbar(d)
    d.text((BX + 40, TOP + 26), "←", font=F(30, "b"), fill=GRIS)
    button(d, EDIT, "Modifier", primary=True)
    d.rounded_rectangle(PLUS, 24, fill=(255, 255, 255))
    cx = (PLUS[0] + PLUS[2]) / 2
    for k in range(3): d.ellipse([cx - 4, PLUS[1] + 10 + k * 11, cx + 4, PLUS[1] + 18 + k * 11], fill=GRIS)
    avatar(d, BX + 200, TOP + 210, 80, name[0])
    d.text((BX + 320, TOP + 160), name, font=F(40, "b"), fill=INK)
    d.rounded_rectangle([BX + 320, TOP + 260, BX + 900, TOP + 360], 12, fill=FOND, outline=LIGNE)
    mail_icon(d, BX + 345, TOP + 294); d.text((BX + 400, TOP + 296), mail, font=F(22), fill=BLEU)
    if menu:
        d.rounded_rectangle([MENU_SUPPR[0], MENU_SUPPR[1] - 6, MENU_SUPPR[2], MENU_SUPPR[3] + 60], 8, fill=(255, 255, 255), outline=LIGNE, width=2)
        d.text((MENU_SUPPR[0] + 20, MENU_SUPPR[1] + 10), "Supprimer", font=F(21, "s"), fill=INK)
        d.text((MENU_SUPPR[0] + 20, MENU_SUPPR[1] + 64), "…", font=F(21, "s"), fill=GRIS)
    return im, d

TO = (BX + 330, TOP + 86, BX + 1000, TOP + 136)
SUGG = (BX + 330, TOP + 140, BX + 1000, TOP + 210)
def page_mail(to_text="", sugg=False, chosen=False):
    im, d = browser("messagerie")
    d.rounded_rectangle([BX + 300, TOP + 20, BX + 1030, TOP + 480], 10, fill=(255, 255, 255), outline=LIGNE, width=2)
    d.rounded_rectangle([BX + 300, TOP + 20, BX + 1030, TOP + 70], 10, fill=(242, 246, 252)); d.rectangle([BX + 300, TOP + 50, BX + 1030, TOP + 70], fill=(242, 246, 252))
    d.text((BX + 320, TOP + 31), "Nouveau message", font=F(20, "s"), fill=INK)
    d.line([TO[0], TO[3], TO[2], TO[3]], fill=LIGNE, width=2)
    d.text((TO[0] + 8, TO[1] + 12), "À", font=F(22, "b"), fill=GRIS)
    if chosen:
        d.rounded_rectangle([TO[0] + 50, TO[1] + 8, TO[0] + 380, TO[3] - 8], 16, fill=(232, 240, 254))
        d.text((TO[0] + 64, TO[1] + 13), "paul.durand@exemple.fr", font=F(20), fill=INK)
    else:
        d.text((TO[0] + 50, TO[1] + 12), to_text, font=F(22), fill=INK)
        x = TO[0] + 50 + d.textlength(to_text, font=F(22)); d.line([x + 2, TO[1] + 12, x + 2, TO[3] - 12], fill=INK, width=2)
    d.line([TO[0], TO[3] + 52, TO[2], TO[3] + 52], fill=LIGNE, width=2)
    if sugg and not chosen:
        d.rounded_rectangle(SUGG, 8, fill=(255, 255, 255), outline=LIGNE, width=2)
        avatar(d, SUGG[0] + 36, (SUGG[1] + SUGG[3]) / 2, 22, "P", (230, 81, 0))
        d.text((SUGG[0] + 74, SUGG[1] + 8), "Paul Durand", font=F(21, "s"), fill=INK)
        d.text((SUGG[0] + 74, SUGG[1] + 36), "paul.durand@exemple.fr", font=F(18), fill=GRIS)
    return im, d

def label(d, text, pos):
    f = F(26, "b"); tw = d.textlength(text, font=f); x, y = pos
    d.rounded_rectangle([x - tw / 2 - 16, y - 8, x + tw / 2 + 16, y + 40], 12, fill=VIO)
    d.text((x - tw / 2, y), text, font=f, fill=(255, 255, 255))

def typed(s, p): return s[:int(len(s) * max(0, min(1, p)))]

def click(im, d, r, t, D, start, tc=0.6, loupe=True, place=None, clean=None):
    """Curseur qui va sur r, cadre et flèche avant le clic à tc*D, onde au clic."""
    c = R.center(r); T = tc * D
    if t < T + 0.3:
        R.highlight(d, r, t); R.arrow(d, r, t)
        if loupe and t > 0.2 * D:
            R.loupe(im, r, place=place, clean=clean); d = ImageDraw.Draw(im)
    pos = R.move(t, 0.1 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    R.cursor(d, *pos); R.ripple(d, c[0], c[1], (t - T) / 0.6)
    return d

NEW = ("Paul", "Durand", "paul.durand@exemple.fr")
JEANNE = ("Jeanne", "Martin", "jeanne.martin@exemple.fr")
def fill_form(t, D, vals, p0=0.0, p1=1.0):
    """Remplit les 3 cases entre p0 et p1 (fraction de D)."""
    p = (t / D - p0) / (p1 - p0); k = min(2, int(max(0, p) * 3)); sub = max(0, p) * 3 - k
    cur = [vals[i] if i < k else (typed(vals[i], sub) if i == k else "") for i in range(3)]
    if p >= 1: cur = list(vals)
    return page_form(tuple(cur), active=k if p < 1 else None)

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Le carnet d'adresses", ["Aide-mémoire n° 20 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); avatar(d, W / 2 - 90, 360, 50, "A", (0, 137, 123)); avatar(d, W / 2 + 30, 360, 50, "P", (230, 81, 0)); avatar(d, W / 2 + 150, 360, 50, "S", (194, 24, 91))
        return im
    if sid == "intro":
        im = R.bg().copy(); d = ImageDraw.Draw(im)
        # répertoire papier
        d.rounded_rectangle([170, 130, 560, 520], 18, fill=(160, 40, 60), outline=(110, 20, 40), width=6)
        d.rounded_rectangle([200, 150, 540, 500], 10, fill=(255, 250, 235))
        for k, n in enumerate(["Annie", "Marc", "Paul", "Sophie"]):
            d.text((230, 180 + k * 70), n, font=F(30, "s"), fill=INK); d.line([230, 222 + k * 70, 510, 222 + k * 70], fill=(200, 190, 170), width=2)
        for k, l in enumerate("ABCDEFG"):
            d.rounded_rectangle([540, 160 + k * 46, 575, 200 + k * 46], 6, fill=(255, 199, 44)); d.text((549, 166 + k * 46), l, font=F(20, "b"), fill=INK)
        if p > 0.4:
            d.text((610, 290), "=", font=F(70, "b"), fill=(255, 255, 255))
            d.rounded_rectangle([700, 150, 1110, 500], 18, fill=(255, 255, 255))
            for k, (n, m) in enumerate(CONTACTS[:3]):
                avatar(d, 750, 210 + k * 100, 26, n[0]); d.text((790, 188 + k * 100), n, font=F(24, "s"), fill=INK); d.text((790, 218 + k * 100), m, font=F(17), fill=GRIS)
        R.caption(d, cap); return im
    if sid == "ouvrir":
        url = "contacts.google.com"
        if p < 0.45:
            im, d = browser("", typing=typed(url, (p - 0.05) / 0.35)); clean = im.copy()
            if p > 0.1: R.highlight(d, ADDR, t)
            if p > 0.15: R.loupe(im, (ADDR[0], ADDR[1], ADDR[0] + 260, ADDR[3]), place=(640, 380), clean=clean); d = ImageDraw.Draw(im)
        elif p < 0.6:
            im, d = browser("", typing=url); R.key_enter(d, t, p > 0.52)
        else:
            im, d = page_list()
            if p > 0.7: R.highlight(d, (row_rect(0)[0], row_rect(0)[1], row_rect(3)[2], row_rect(3)[3]), t)
        R.caption(d, cap); return im
    if sid == "creer":
        im, d = page_list(); clean = im.copy()
        d = click(im, d, CREATE, t, D, (W / 2, H / 2), place=(700, 400), clean=clean)
        if p > 0.75: im, d = page_form(active=0)
        R.caption(d, cap); return im
    if sid == "remplir":
        im, d = fill_form(t, D, NEW, 0.12, 0.85)
        if p < 0.4: label(d, "le prénom, puis le nom", (1000, TOP + 180))
        elif p < 0.88: label(d, "l'adresse mail", (1000, TOP + 320))
        R.caption(d, cap); return im
    if sid == "enregistrer":
        if p < 0.55:
            im, d = page_form(NEW); clean = im.copy()
            d = click(im, d, SAVE, t, D, (700, 420), tc=0.45, place=(900, 420), clean=clean)
        else:
            im, d = page_fiche("Paul Durand", NEW[2])
            label(d, "Bravo !", (W / 2 + 300, TOP + 160))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "chercher":
        if p < 0.3:
            im, d = page_list(); clean = im.copy(); d = click(im, d, SEARCH, t, D * 0.3 / 0.3, (W / 2, H / 2 + 80), tc=0.25, loupe=False)
        elif p < 0.6:
            q = typed("Pau", (p - 0.3) / 0.2); res = [c for c in CONTACTS if c[0].lower().startswith(q.lower())] if q else CONTACTS
            im, d = page_list(res, query=q)
            if q: label(d, "les premières lettres", (W / 2 + 120, TOP + 300))
        else:
            im, d = page_list([CONTACTS[2]], query="Pau", hover=0); clean = im.copy()
            d = click(im, d, row_rect(0), t - 0.6 * D, 0.4 * D, (W / 2, H / 2), tc=0.55, loupe=False)
            if p > 0.9: im, d = page_fiche("Paul Durand", NEW[2])
        R.caption(d, cap); return im
    if sid == "modifier":
        if p < 0.45:
            im, d = page_fiche("Paul Durand", NEW[2]); clean = im.copy()
            d = click(im, d, EDIT, t, D, (W / 2, H / 2), tc=0.33, place=(800, 420), clean=clean)
        elif p < 0.75:
            new = "paul.durand@exemple.com"; k = (p - 0.45) / 0.25
            v = NEW[2][:-3] + typed(".fr", 1 - k * 2) if k < 0.5 else NEW[2][:-3] + typed(".com", (k - 0.5) * 2)
            im, d = page_form(("Paul", "Durand", v), active=2); label(d, "je corrige", (1000, TOP + 320))
        else:
            im, d = page_form(("Paul", "Durand", "paul.durand@exemple.com")); clean = im.copy()
            d = click(im, d, SAVE, t - 0.75 * D, 0.25 * D, (900, 400), tc=0.6, loupe=False)
        R.caption(d, cap); return im
    if sid == "ecrire":
        if p < 0.25:
            im, d = page_mail(""); R.highlight(d, TO, t); R.arrow(d, (TO[0], TO[1], TO[0] + 40, TO[3]), t)
        elif p < 0.5:
            im, d = page_mail(typed("Pau", (p - 0.25) / 0.15), sugg=p > 0.42)
            if p > 0.3: label(d, "les premières lettres", (W / 2 + 60, TOP + 300))
        elif p < 0.75:
            im, d = page_mail("Pau", sugg=True); clean = im.copy()
            d = click(im, d, SUGG, t - 0.5 * D, 0.25 * D, (W / 2 + 200, H / 2 + 100), tc=0.6, loupe=False)
        else:
            im, d = page_mail(chosen=True); label(d, "l'adresse s'écrit toute seule", (W / 2 + 60, TOP + 300))
        R.caption(d, cap); return im
    if sid == "supprimer":
        if p < 0.45:
            im, d = page_fiche("Sophie Dubois", CONTACTS[3][1]); clean = im.copy()
            d = click(im, d, PLUS, t, D, (W / 2, H / 2), tc=0.33, place=(760, 420), clean=clean)
            if p > 0.3: label(d, "Plus", (PLUS[0] - 40, TOP + 140))
        elif p < 0.8:
            im, d = page_fiche("Sophie Dubois", CONTACTS[3][1], menu=True)
            d = click(im, d, MENU_SUPPR, t - 0.45 * D, 0.35 * D, R.center(PLUS), tc=0.6, loupe=False)
        else:
            im, d = page_list(CONTACTS[:3]); label(d, "le contact est retiré", (W / 2 + 120, TOP + 340))
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Ajoutez le contact :", "Jeanne Martin", "jeanne.martin@exemple.fr"], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Ajoutez Jeanne Martin", "à votre carnet."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        if p < 0.25:
            im, d = page_list(); d = click(im, d, CREATE, t, 0.25 * D, (W / 2, H / 2), tc=0.6, loupe=False)
        elif p < 0.75:
            im, d = fill_form(t - 0.25 * D, 0.5 * D, JEANNE, 0.0, 0.9)
        elif p < 0.9:
            im, d = page_form(JEANNE); d = click(im, d, SAVE, t - 0.75 * D, 0.15 * D, (800, 420), tc=0.6, loupe=False)
        else:
            im, d = page_fiche("Jeanne Martin", JEANNE[2]); label(d, "Bravo !", (W / 2 + 300, TOP + 160))
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Le carnet garde les adresses", "« Créer un contact », puis « Enregistrer »", "La recherche pour retrouver", "La case « À » propose le nom"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
