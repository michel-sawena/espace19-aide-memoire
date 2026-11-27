"""Vidéo « 26 - Repérer les arnaques » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_26.py script.json durations.json out.mp4
        python3 render_26.py --estimate script.json durations.json
Réutilise ../render_01.py (fond, cadre jaune, flèche, loupe, titres, sous-titres, cartes).
Tous les messages montrés sont INVENTÉS et marqués « EXEMPLE » ; aucun logo ni charte de site réel.
Conseils et numéros vérifiés : voir sources_26.md.
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, ".."))
import render_01 as R
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIOLET = (147, 17, 126); CORAIL = (255, 122, 89); VERT = (43, 179, 163); ROUGE = (210, 40, 40)

# ---------- éléments communs ----------
def tampon(d, x, y, s=1.0):
    """Étiquette « EXEMPLE » (message inventé)."""
    f = F(int(22 * s), "b"); tw = d.textlength("EXEMPLE INVENTÉ", font=f)
    d.rounded_rectangle([x, y, x + tw + 24 * s, y + 36 * s], 8, fill=CORAIL)
    d.text((x + 12 * s, y + 5 * s), "EXEMPLE INVENTÉ", font=f, fill=(255, 255, 255))

def wrap(d, txt, f, wmax):
    lines, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > wmax: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]

# ---------- téléphone avec SMS ----------
PX, PY, PW, PH = 420, 92, 440, 560
SMS_LINES = [("Votre colis est bloqué.", "u"), ("Payez 1,99 € AUJOURD'HUI", "u"), ("sinon il sera renvoyé :", "u"),
             ("http://colis-livr4ison.top", "l"), ("Saisissez le code reçu", "c"), ("par SMS pour valider.", "c")]

def phone(kind="sms"):
    im = R.bg(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([PX - 14, PY - 14, PX + PW + 14, PY + PH + 14], 46, fill=(20, 20, 26))
    d.rounded_rectangle([PX, PY, PX + PW, PY + PH], 34, fill=(246, 246, 250))
    d.rounded_rectangle([PX + PW / 2 - 50, PY + 8, PX + PW / 2 + 50, PY + 26], 9, fill=(20, 20, 26))
    if kind == "sms":
        d.rectangle([PX, PY + 40, PX + PW, PY + 100], fill=(232, 232, 238))
        d.ellipse([PX + 20, PY + 50, PX + 60, PY + 90], fill=(170, 170, 185))
        d.text((PX + 74, PY + 52), "+33 7 00 00 00 00", font=F(22, "s"), fill=INK)
        d.text((PX + 74, PY + 78), "Numéro inconnu", font=F(16), fill=(90, 90, 100))
        tampon(d, PX + 20, PY + 116)
        d.rounded_rectangle([PX + 20, PY + 170, PX + PW - 40, PY + 170 + 34 * len(SMS_LINES) + 30], 22, fill=(225, 226, 232))
        for i, (t, k) in enumerate(SMS_LINES):
            d.text((PX + 40, PY + 186 + 34 * i), t, font=F(23, "s" if k == "u" else "r"), fill=(0, 80, 200) if k == "l" else INK)
    else:  # appel
        d.rectangle([PX, PY + 30, PX + PW, PY + PH], fill=(40, 46, 70))
        d.ellipse([PX + PW / 2 - 60, PY + 90, PX + PW / 2 + 60, PY + 210], fill=(120, 130, 160))
        d.text((PX + PW / 2 - 112, PY + 230), "« Service fraude »", font=F(30, "b"), fill=(255, 255, 255))
        d.text((PX + PW / 2 - 92, PY + 276), "appel entrant…", font=F(22), fill=(210, 215, 230))
        tampon(d, PX + PW / 2 - 115, PY + 40)
        for cx, col, sym in ((PX + 110, ROUGE, "non"), (PX + PW - 110, VERT, "tel")):
            d.ellipse([cx - 44, PY + 420, cx + 44, PY + 508], fill=col); picto(d, sym, cx, PY + 464, 30)
        d.text((PX + 40, PY + 516), "Raccrocher", font=F(20, "s"), fill=(255, 255, 255))
    return im

def sms_rect(i0, i1):
    return (PX + 32, PY + 182 + 34 * i0, PX + PW - 52, PY + 182 + 34 * (i1 + 1))

R_URG, R_LIEN, R_CODE = sms_rect(0, 2), sms_rect(3, 3), sms_rect(4, 5)

# ---------- faux mail ----------
MX, MY, MW, MH = 150, 100, 980, 520
def mail():
    im = R.bg(); d = ImageDraw.Draw(im)
    d.rounded_rectangle([MX, MY, MX + MW, MY + MH], 12, fill=(255, 255, 255))
    d.rounded_rectangle([MX, MY, MX + MW, MY + 44], 12, fill=(232, 236, 244)); d.rectangle([MX, MY + 30, MX + MW, MY + 44], fill=(232, 236, 244))
    d.text((MX + 18, MY + 10), "Messagerie", font=F(20, "s"), fill=INK)
    tampon(d, MX + MW - 240, MY + 56)
    d.text((MX + 30, MY + 62), "Objet : Dernier avertissement !!!", font=F(28, "b"), fill=INK)
    d.text((MX + 30, MY + 112), "De : Service Client <securite@banque-verif-24.xyz>", font=F(24), fill=INK)
    body = ["Cher client, votre compte va etre bloquer dans 24h.", "Pour eviter sa, confirmez vos information ici :",
            "Cliquez ici", "Sans réponse, des frais vous serons facturé."]
    for i, t in enumerate(body):
        if i == 2:
            d.rounded_rectangle([MX + 30, MY + 236 + 52 * i, MX + 230, MY + 280 + 52 * i], 8, fill=(0, 103, 192))
            d.text((MX + 62, MY + 244 + 52 * i), t, font=F(24, "b"), fill=(255, 255, 255))
        else:
            d.text((MX + 30, MY + 240 + 52 * i), t, font=F(25), fill=INK)
    return im

R_ADR = (MX + 92, MY + 108, MX + 690, MY + 146)
R_FAUTE = (MX + 24, MY + 234, MX + 720, MY + 330)
R_MENACE = (MX + 24, MY + 386, MX + 760, MY + 426)

def label(d, txt, x, y, col=YEL):
    d.text((x, y), txt, font=F(34, "b"), fill=col, stroke_width=4, stroke_fill=(0, 0, 0))

# ---------- pictos dessinés ----------
def picto(d, kind, cx, cy, r, col=(255, 255, 255)):
    w = max(4, int(r / 4))
    if kind == "non":
        d.line([cx - r * .45, cy - r * .45, cx + r * .45, cy + r * .45], fill=col, width=w); d.line([cx - r * .45, cy + r * .45, cx + r * .45, cy - r * .45], fill=col, width=w)
    elif kind == "oui":
        d.line([cx - r * .5, cy, cx - r * .1, cy + r * .4, cx + r * .55, cy - r * .4], fill=col, width=w, joint="curve")
    elif kind == "mail":
        d.rectangle([cx - r * .7, cy - r * .45, cx + r * .7, cy + r * .45], outline=col, width=w); d.line([cx - r * .7, cy - r * .45, cx, cy + r * .1, cx + r * .7, cy - r * .45], fill=col, width=w)
    elif kind == "tel":
        d.rounded_rectangle([cx - r * .38, cy - r * .7, cx + r * .38, cy + r * .7], int(r * .15), outline=col, width=w); d.ellipse([cx - r * .08, cy + r * .45, cx + r * .08, cy + r * .6], fill=col)
    elif kind == "bulle":
        d.rounded_rectangle([cx - r * .7, cy - r * .5, cx + r * .7, cy + r * .3], int(r * .2), outline=col, width=w); d.polygon([(cx - r * .4, cy + r * .28), (cx - r * .5, cy + r * .65), (cx - r * .05, cy + r * .28)], fill=col)

# ---------- cartes ----------
def card_icons(title, items, cap):
    im = R.card(title, [], None); d = ImageDraw.Draw(im)
    for i, (sym, txt) in enumerate(items):
        y = 170 + i * 100
        d.ellipse([200, y, 270, y + 70], fill=CORAIL if sym == "non" else VERT); picto(d, sym, 235, y + 35, 30)
        d.text((300, y + 14), txt, font=F(36, "s"), fill=(30, 30, 30))
    return im

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Repérer les arnaques", ["Faux SMS · faux mails · faux appels", "", "Aide-mémoire n° 26 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); d.ellipse([W / 2 - 60, 380, W / 2 + 60, 500], fill=CORAIL)
        d.text((W / 2 - 18, 395), "!", font=F(80, "b"), fill=(255, 255, 255)); return im
    if sid == "intro":
        im = R.card("", [], None); d = ImageDraw.Draw(im)
        for i, (sym, lab) in enumerate([("mail", "faux mail"), ("tel", "faux appel"), ("bulle", "faux SMS")]):
            if p > 0.1 + i * 0.15:
                x = 250 + i * 290
                d.ellipse([x, 140, x + 160, 300], fill=(248, 234, 245), outline=VIOLET, width=6)
                picto(d, sym, x + 80, 220, 60, VIOLET)
                tw = d.textlength(lab, font=F(30, "b")); d.text((x + 80 - tw / 2, 320), lab, font=F(30, "b"), fill=VIOLET)
        if p > 0.65:
            d.text((W / 2 - 250, 400), "Pas de panique !", font=F(52, "b"), fill=VERT)
        R.caption(d, cap); return im
    if sid == "sms":
        im = phone("sms"); d = ImageDraw.Draw(im)
        if p > 0.5: R.highlight(d, (PX + 26, PY + 176, PX + PW - 46, PY + 170 + 34 * len(SMS_LINES) + 24), t)
        R.caption(d, cap); return im
    if sid == "signes":
        im = phone("sms"); d = ImageDraw.Draw(im); clean = im.copy()
        k = 0 if p < 0.17 else 1 if p < 0.48 else 2
        r = [R_URG, R_LIEN, R_CODE][k]; R.highlight(d, r, t); R.arrow(d, r, t)
        for j in range(k + 1):
            label(d, ["1. Urgence", "2. Lien inconnu", "3. Argent, code"][j], 70, 220 + j * 90, YEL if j == k else (255, 255, 255))
        R.loupe(im, r, place=(1080, 360), clean=clean); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "mail":
        im = mail(); d = ImageDraw.Draw(im)
        if p > 0.25:
            k = 0 if p < 0.55 else 1 if p < 0.8 else 2
            r = [R_ADR, R_FAUTE, R_MENACE][k]; R.highlight(d, r, t)
            label(d, ["Adresse bizarre", "Fautes", "Menace"][k], r[2] + 24, r[1] + 6)
        R.caption(d, cap); return im
    if sid == "appel":
        im = phone("appel"); d = ImageDraw.Draw(im)
        if p > 0.55:
            d.rounded_rectangle([PX - 300, 300, PX - 20, 420], 20, fill=(255, 255, 255), outline=YEL, width=6)
            d.text((PX - 284, 318), "« Donnez-moi le", font=F(28, "s"), fill=INK); d.text((PX - 284, 360), "code reçu par SMS »", font=F(28, "s"), fill=INK)
            label(d, "PIÈGE !", PX - 230, 440, CORAIL)
        R.caption(d, cap); return im
    if sid == "regle":
        im = R.card("La règle d'or", ["Votre banque ne vous demande JAMAIS", "vos codes ni votre mot de passe.", "Une administration non plus."], "Ni par mail, ni par SMS, ni au téléphone.")
        d = ImageDraw.Draw(im); d.ellipse([W / 2 - 50, 360, W / 2 + 50, 460], fill=VERT); picto(d, "oui", W / 2, 410, 45); return im
    if sid == "reflexe":
        items = [("non", "Je ne clique pas"), ("non", "Je ne réponds pas, je ne donne rien"), ("non", "Au téléphone : je raccroche"), ("oui", "J'appelle ma banque, numéro habituel")]
        return card_icons("Le bon réflexe", items[:1 + min(3, int(p * 4.5))], cap)
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et relisez les signes d'arnaque."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "signaler":
        im = R.card("Signaler", [], None); d = ImageDraw.Draw(im)
        d.rounded_rectangle([170, 170, 620, 430], 20, fill=(255, 246, 214)); d.rounded_rectangle([660, 170, 1110, 430], 20, fill=(248, 234, 245))
        d.text((210, 190), "Faux SMS", font=F(34, "b"), fill=INK); d.text((210, 250), "33 700", font=F(70, "b"), fill=VIOLET); d.text((210, 350), "envoi gratuit", font=F(28), fill=INK)
        d.text((700, 190), "Faux mail", font=F(34, "b"), fill=INK); d.text((700, 260), "Signal Spam", font=F(52, "b"), fill=VIOLET); d.text((700, 350), "signal-spam.fr", font=F(28), fill=INK)
        return im
    if sid == "victime":
        im = R.card("Vous avez donné un code ?", [], None); d = ImageDraw.Draw(im)
        rows = [("1", "Appelez votre banque : opposition"), ("2", "17Cyber : 17cyber.gouv.fr"), ("3", "Info Escroqueries : 0 805 805 817")]
        for i, (n, txt) in enumerate(rows):
            if p > 0.2 + i * 0.2:
                y = 170 + i * 92; d.ellipse([170, y, 236, y + 66], fill=YEL); d.text((193, y + 10), n, font=F(38, "b"), fill=INK)
                d.text((260, y + 12), txt, font=F(36, "s"), fill=(30, 30, 30))
        d.text((300, 450), "appel gratuit, du lundi au vendredi", font=F(26), fill=(70, 70, 70))
        return im
    if sid == "exercice":
        im = phone("sms"); d = ImageDraw.Draw(im); label(d, "Trouvez", 80, 260); label(d, "les 3 signes", 80, 310)
        R.caption(d, cap); return im
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        im = phone("sms"); d = ImageDraw.Draw(im); label(d, "À vous !", 80, 260)
        d.text((80, 330), f"Solution dans {left} s", font=F(30, "s"), fill=(255, 255, 255)); return im
    if sid == "solution":
        im = phone("sms"); d = ImageDraw.Draw(im)
        k = 0 if p < 0.15 else 1 if p < 0.35 else 2 if p < 0.5 else 3
        for j, r in enumerate([R_URG, R_LIEN, R_CODE][:k]):
            d.rounded_rectangle([r[0] - 8, r[1] - 6, r[2] + 8, r[3] + 6], 8, outline=CORAIL if j < k - 1 else YEL, width=7)
            label(d, f"{j + 1}. " + ["Urgence", "Lien bizarre", "Code demandé"][j], 60, 220 + j * 80)
        if p > 0.65:
            d.rounded_rectangle([PX + PW + 40, 300, PX + PW + 360, 400], 18, fill=CORAIL)
            d.text((PX + PW + 70, 325), "ARNAQUE !", font=F(46, "b"), fill=(255, 255, 255))
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Urgence · lien bizarre · code ou argent", "→ c'est une arnaque", "Je ne clique pas, je ne donne rien", "Dans le doute, je demande conseil"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
