"""Vidéo « 13 - Faire une recherche (et reconnaître une réponse d'IA) » (écrans dessinés, sous-titrée).
Usage : python3 render_13.py script.json durations.json out.mp4
        python3 render_13.py --estimate script.json durations.json
Réutilise ../12-internet/render_12.py (fenêtre du navigateur, page google.fr simplifiée), ../render_01.py, ../01-ordinateur.
Aucun logo reproduit : moteurs = pastilles neutres avec leur nom ; page de résultats = dessin simplifié, sans charte.
Sites des résultats INVENTÉS (adresses « exemple-… »). Libellé écrit tel quel : « Aperçu IA » (blog Google France
22/07/2026 + L'Éclaireur Fnac 23/07/2026, voir sources_13.md).
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../12-internet"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
import render_12 as N
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); BLEU = (26, 13, 171); GRIS = (77, 81, 86); VERTS = (0, 110, 70)
BX, BY, BW, BH, PAGE_Y = N.BX, N.BY, N.BW, N.BH, N.PAGE_Y
CX = BX + BW / 2
SBOX = (CX - 290, PAGE_Y + 200, CX + 290, PAGE_Y + 250)          # grande case (page d'accueil)
BACK = (BX + 14, N.BAR_Y + 14, BX + 48, N.BAR_Y + 46)            # flèche vers la gauche
AI = (BX + 40, PAGE_Y + 78, BX + 760, PAGE_Y + 222)               # encadré Aperçu IA
RES_Y = (PAGE_Y + 246, PAGE_Y + 352)

QUESTIONS = {
 "soupe au potiron": {
   "ia": ["Pour une soupe au potiron, faites cuire le potiron", "en morceaux avec un oignon, puis mixez."],
   "res": [("Cuisine de saison", "www.exemple-cuisine.fr", "Soupe au potiron facile", "Une recette simple, pas à pas."),
           ("Le carnet de recettes", "www.exemple-recettes.fr", "Velouté de potiron : la recette", "Ingrédients, cuisson et conseils.")]},
 "horaires de la mairie": {
   "ia": ["Les mairies sont souvent ouvertes en semaine.", "Les horaires changent d'une mairie à l'autre."],
   "res": [("Mairie (exemple)", "www.exemple-mairie.fr", "Horaires d'ouverture de la mairie", "Accueil, état civil, adresse."),
           ("Annuaire (exemple)", "www.exemple-annuaire.fr", "Mairie : adresse et horaires", "Téléphone et jours d'ouverture.")]},
}

def title_rect(i, q="soupe au potiron"):
    y = RES_Y[i]; t = QUESTIONS[q]["res"][i][2]
    w = ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(t, font=F(24, "s"))
    return (BX + 40, y + 46, BX + 44 + w, y + 78)

def sparkle(d, cx, cy, r, col=VIO):
    d.polygon([(cx, cy - r), (cx + r * .28, cy - r * .28), (cx + r, cy), (cx + r * .28, cy + r * .28),
               (cx, cy + r), (cx - r * .28, cy + r * .28), (cx - r, cy), (cx - r * .28, cy - r * .28)], fill=col)

def results(d, q, hover=None):
    data = QUESTIONS[q]
    d.text((BX + 40, PAGE_Y + 22), "Google", font=F(28, "b"), fill=(60, 64, 72))
    d.rounded_rectangle([BX + 170, PAGE_Y + 16, BX + 700, PAGE_Y + 60], 22, fill=(255, 255, 255), outline=(190, 195, 205), width=2)
    d.text((BX + 196, PAGE_Y + 25), q, font=F(20), fill=(20, 20, 20))
    d.text((BX + 780, PAGE_Y + 28), "(dessin simplifié)", font=F(16), fill=(110, 110, 120))
    d.rounded_rectangle(AI, 14, fill=(240, 236, 250), outline=(205, 195, 230), width=2)
    sparkle(d, AI[0] + 30, AI[1] + 28, 13)
    d.text((AI[0] + 52, AI[1] + 14), "Aperçu IA", font=F(24, "b"), fill=INK)
    for k, l in enumerate(data["ia"]): d.text((AI[0] + 22, AI[1] + 60 + k * 32), l, font=F(21), fill=INK)
    for i, (nom, adr, tit, desc) in enumerate(data["res"]):
        y = RES_Y[i]
        d.ellipse([BX + 40, y + 4, BX + 68, y + 32], fill=(225, 228, 236)); N.globe(d, BX + 54, y + 18, 10, (150, 160, 180))
        d.text((BX + 78, y), nom, font=F(18, "s"), fill=INK); d.text((BX + 78, y + 22), adr, font=F(15), fill=GRIS)
        d.text((BX + 40, y + 46), tit, font=F(24, "s"), fill=BLEU)
        if hover == i:
            r = title_rect(i, q); d.line([r[0], r[3] - 2, r[2], r[3] - 2], fill=BLEU, width=2)
        d.text((BX + 40, y + 80), desc, font=F(18), fill=GRIS)

def site(d):
    d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, PAGE_Y + 70], fill=(250, 238, 220))
    d.text((BX + 40, PAGE_Y + 20), "Cuisine de saison (site d'exemple)", font=F(24, "b"), fill=(120, 60, 20))
    d.text((BX + 40, PAGE_Y + 100), "Soupe au potiron facile", font=F(36, "b"), fill=INK)
    for k, l in enumerate(["1. Coupez le potiron en morceaux.", "2. Faites cuire avec un oignon.", "3. Mixez. Bon appétit !"]):
        d.text((BX + 60, PAGE_Y + 170 + k * 44), l, font=F(24), fill=INK)
    d.ellipse([BX + 760, PAGE_Y + 140, BX + 940, PAGE_Y + 320], fill=(240, 140, 40)); d.rectangle([BX + 842, PAGE_Y + 120, BX + 858, PAGE_Y + 146], fill=(90, 120, 50))

def screen(state=None, q="soupe au potiron", typed="", focus=False, hover=None):
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    if state is None: return im
    page = "google" if state in ("home", "results", "site") else None
    N.browser(d, typed="google.fr" if state == "home" else ("www.exemple-cuisine.fr" if state == "site" else ("google.fr" if page else "")), page=page)
    if state == "home":
        if focus or typed:
            d.rounded_rectangle(SBOX, 25, fill=(255, 255, 255), outline=N.BLEU, width=3)
            d.ellipse([SBOX[0] + 22, SBOX[1] + 14, SBOX[0] + 40, SBOX[1] + 32], outline=(110, 110, 120), width=2)
            d.text((SBOX[0] + 56, SBOX[1] + 11), typed, font=F(22), fill=(20, 20, 20))
            x = SBOX[0] + 58 + d.textlength(typed, font=F(22)); d.line([x, SBOX[1] + 12, x, SBOX[3] - 12], fill=(20, 20, 20), width=2)
    elif state in ("results", "site"):
        d.rectangle([BX + 2, PAGE_Y + 1, BX + BW - 2, BY + BH - 4], fill=(255, 255, 255))
        d.rectangle([BX + 12, BY + 6, BX + 300, BY + N.TAB_H + 4], fill=(250, 250, 252)); N.globe(d, BX + 32, BY + 23, 9)
        d.text((BX + 50, BY + 12), (q[:18] + " - Recherche") if state == "results" else "Cuisine de saison", font=F(17), fill=(30, 30, 30))
        if state == "results": results(d, q, hover)
        else: site(d)
    return im

act = N.act

MOTEURS = [("Google", (66, 103, 178)), ("Bing", (0, 128, 128)), ("Qwant", (200, 60, 80)), ("Ecosia", (60, 150, 80))]
def pastilles(d, p, t):
    for i, (n, col) in enumerate(MOTEURS):
        if p > 0.05 + i * 0.16:
            x = 220 + i * 280; y = 290
            d.ellipse([x - 70, y - 70, x + 70, y + 70], fill=col); sparkle_mag(d, x, y)
            f = F(30, "b"); tw = d.textlength(n, font=f); d.text((x - tw / 2, y + 88), n, font=f, fill=INK)
            sub = ["le plus connu", "de Microsoft", "français", "plante des arbres"][i]
            f2 = F(22, "s"); tw = d.textlength(sub, font=f2); d.text((x - tw / 2, y + 128), sub, font=f2, fill=INK)
            if 0.05 + i * 0.16 < p < 0.21 + i * 0.16: R.highlight(d, (x - 80, y - 80, x + 80, y + 80), t)
    if p > 0.82: O.label(d, "ils marchent tous de la même façon", (W / 2, 530))

def sparkle_mag(d, x, y, s=1.0, col=(255, 255, 255)):
    d.ellipse([x - 28 * s, y - 34 * s, x + 20 * s, y + 14 * s], outline=col, width=int(8 * s))
    d.line([x + 12 * s, y + 8 * s, x + 36 * s, y + 34 * s], fill=col, width=int(11 * s))

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Faire une recherche", ["et reconnaître une réponse d'IA", "Aide-mémoire n° 13 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); d.ellipse([W / 2 - 70, 300, W / 2 + 70, 440], fill=VIO); sparkle_mag(d, W / 2, 375, 1.3); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im); O.draw_fixe(d)
        for k, (txt, pos) in enumerate((("une recette", (1050, 150)), ("un horaire", (1050, 260)), ("une adresse", (1050, 370)))):
            if p > 0.12 + k * 0.12: O.label(d, txt, pos)
        R.caption(d, cap); return im
    if sid == "moteur":
        im = O.room(); d = ImageDraw.Draw(im)
        for k in range(5):  # étagère de livres
            for j in range(9):
                c = [(170, 60, 50), (60, 110, 170), (80, 140, 80), (200, 150, 50)][(k + j) % 4]
                d.rectangle([150 + j * 44, 130 + k * 80, 186 + j * 44, 200 + k * 80], fill=c)
            d.rectangle([140, 200 + k * 80, 560, 208 + k * 80], fill=(120, 80, 45))
        if p > 0.4:
            d.ellipse([820, 160, 1020, 360], fill=VIO); sparkle_mag(d, 920, 260, 2.2)
            O.label(d, "le moteur de recherche", (920, 410))
        if p > 0.65:
            R.highlight(d, (150 + 4 * 44, 130 + 2 * 80, 186 + 4 * 44, 200 + 2 * 80), t)
            O.label(d, "comme un bibliothécaire", (920, 470))
        R.caption(d, cap); return im
    if sid == "noms":
        im = O.room(); d = ImageDraw.Draw(im); pastilles(d, p, t); R.caption(d, cap); return im
    if sid == "ouvrir":
        if t < 0.45 * D:
            return act(lambda: screen(), lambda: screen("blank"), N.EDGE, (W / 2 - 200, H / 2), t, 0.45 * D, cap, place=(640, 330))
        im = screen("home"); d = ImageDraw.Draw(im)
        if p > 0.55: R.highlight(d, N.ADDR, t)
        R.caption(d, cap); return im
    if sid == "case":
        return act(lambda: screen("home"), lambda: screen("home", focus=True), SBOX, (W / 2, 620), t, D, cap, place=(640, 560))
    if sid == "taper":
        Q = "soupe au potiron"; n = int(len(Q) * min(1, max(0, (p - 0.1) / 0.6)))
        im = screen("home", typed=Q[:n], focus=True); clean = im.copy(); d = ImageDraw.Draw(im)
        R.loupe(im, (SBOX[0], SBOX[1], SBOX[0] + 300, SBOX[3]), place=(640, 560), clean=clean); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid == "entree":
        if t < 0.45 * D:
            im = screen("home", typed="soupe au potiron", focus=True); d = ImageDraw.Draw(im); R.key_enter(d, t, 0.3 * D < t)
        else:
            im = screen("results"); d = ImageDraw.Draw(im)
        R.caption(d, cap); return im
    if sid in ("ia", "attention"):
        im = screen("results"); clean = im.copy(); d = ImageDraw.Draw(im)
        R.highlight(d, AI, t)
        if sid == "ia" and p > 0.15:
            R.loupe(im, (AI[0], AI[1], AI[0] + 260, AI[1] + 56), place=(1010, 330), clean=clean); d = ImageDraw.Draw(im)
            if p > 0.45: O.label(d, "écrit par un programme", (1010, 470))
        if sid == "attention" and p > 0.1:
            d.rounded_rectangle([830, 300, 1150, 440], 18, fill=(255, 122, 89)); d.text((860, 318), "L'IA peut", font=F(34, "b"), fill=(255, 255, 255))
            d.text((860, 368), "se tromper", font=F(34, "b"), fill=(255, 255, 255))
            if p > 0.55: O.label(d, "ce n'est pas un site", (990, 490))
        R.caption(d, cap); return im
    if sid == "liens":
        im = screen("results"); d = ImageDraw.Draw(im)
        if p > 0.15: R.highlight(d, (BX + 34, RES_Y[0] - 6, BX + 560, RES_Y[1] + 108), t)
        if p > 0.45:
            R.arrow(d, (BX + 78, RES_Y[0], BX + 300, RES_Y[0] + 40), t); O.label(d, "nom du site", (BX + 760, RES_Y[0] + 20))
        if p > 0.65: O.label(d, "titre en bleu", (BX + 760, RES_Y[0] + 80))
        R.caption(d, cap); return im
    if sid == "clic":
        return act(lambda: screen("results", hover=0 if p > 0.4 else None), lambda: screen("site"), title_rect(0), (W / 2, 640), t, D, cap, place=(900, 560))
    if sid == "retour":
        return act(lambda: screen("site"), lambda: screen("results"), BACK, (W / 2, H / 2), t, D, cap, place=(500, 330))
    if sid == "conseil":
        im = O.room(); d = ImageDraw.Draw(im)
        for k, txt in enumerate(["la santé", "l'argent", "une démarche"]):
            if p > 0.1 + k * 0.1: O.label(d, txt, (260 + k * 380, 200))
        if p > 0.5:
            d.rounded_rectangle([340, 300, 940, 440], 20, fill=(43, 179, 163)); f = F(40, "b")
            for k, l in enumerate(["Vérifiez sur un site officiel", "ou sur plusieurs sites"]):
                tw = d.textlength(l, font=F(32, "b")); d.text((W / 2 - tw / 2, 322 + k * 52), l, font=F(32, "b"), fill=(255, 255, 255))
        R.caption(d, cap); return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "exercice":
        return R.card("Exercice", ["Cherchez : horaires de la mairie", "Repérez l'Aperçu IA,", "puis cliquez sur un titre bleu."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Cherchez : horaires de la mairie", "Aperçu IA, puis un titre bleu."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        Q = "horaires de la mairie"; q = D / 4
        if t < q:
            n = int(len(Q) * min(1, t / (0.7 * q)))
            im = screen("home", typed=Q[:n], focus=True); d = ImageDraw.Draw(im)
        elif t < 1.4 * q:
            im = screen("home", typed=Q, focus=True); d = ImageDraw.Draw(im); R.key_enter(d, t - q, t - q > 0.2 * q)
        elif t < 2.5 * q:
            im = screen("results", q=Q); d = ImageDraw.Draw(im); R.highlight(d, AI, t)
        else:
            im = screen("results", q=Q, hover=0); d = ImageDraw.Draw(im); r = title_rect(0, Q); R.highlight(d, r, t)
            R.cursor(d, (r[0] + r[2]) / 2, (r[1] + r[3]) / 2)
        R.caption(d, cap); return im
    if sid == "resume":
        return R.card("À retenir", ["Quelques mots dans la case, puis Entrée", "En haut : l'Aperçu IA peut se tromper", "En dessous : les liens vers les sites", "Info importante : vérifiez"], "Bravo ! À bientôt à Espace 19 Numérique !")
    raise KeyError(sid)

main = None
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

estimate = N.estimate

if __name__ == "__main__":
    if sys.argv[1] == "--estimate":
        json.dump(estimate(sys.argv[2]), open(sys.argv[3], "w"), indent=1); print(open(sys.argv[3]).read())
    elif sys.argv[1] == "--stills":
        sc = json.load(open(sys.argv[2])); os.makedirs(sys.argv[3], exist_ok=True)
        for s in sc["scenes"]:
            for f in (0.3, 0.7):
                im = frame(s["id"], f * 8, 8, s["caption"]); R.subtitle(im, R.sub_at(s["narration"], f * 8, 8)); im.save(f"{sys.argv[3]}/{s['id']}_{int(f*10)}.png")
    else:
        main(*sys.argv[1:4])
