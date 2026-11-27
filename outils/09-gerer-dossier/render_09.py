"""Vidéo « 09 - Renommer, déplacer, copier, effacer un dossier » (écrans dessinés, sans voix, sous-titrée).
Usage : python3 render_09.py script.json durations.json out.mp4
        python3 render_09.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, Explorateur, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes).
Libellés écrits tels quels (voir sources_09.md) : « Couper », « Copier », « Coller », « Renommer », « Partager »,
« Supprimer » (icônes en haut du menu du clic droit ; le nom apparaît quand on pointe l'icône), « Corbeille », « Restaurer ».
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, ".."))
import render_01 as R
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); BLEU = (0, 103, 192); ORANGE = (255, 120, 0)
DOCS = ["Lettres", "Factures", "Recettes"]
ICONES = ["Couper", "Copier", "Coller", "Renommer", "Partager", "Supprimer"]

# ---------- icônes du menu (dessin simple, sans logo) ----------
def ico(d, name, cx, cy, col=(40, 40, 50)):
    if name == "Couper":
        d.ellipse([cx - 11, cy + 3, cx - 3, cy + 11], outline=col, width=2); d.ellipse([cx + 3, cy + 3, cx + 11, cy + 11], outline=col, width=2)
        d.line([cx - 5, cy + 4, cx + 6, cy - 11], fill=col, width=2); d.line([cx + 5, cy + 4, cx - 6, cy - 11], fill=col, width=2)
    elif name == "Copier":
        d.rounded_rectangle([cx - 10, cy - 6, cx + 4, cy + 11], 2, outline=col, width=2); d.rounded_rectangle([cx - 4, cy - 12, cx + 10, cy + 5], 2, outline=col, width=2, fill=(252, 252, 254))
    elif name == "Coller":
        d.rounded_rectangle([cx - 10, cy - 9, cx + 10, cy + 12], 3, outline=col, width=2); d.rounded_rectangle([cx - 5, cy - 13, cx + 5, cy - 6], 2, fill=col)
    elif name == "Renommer":
        d.rounded_rectangle([cx - 12, cy - 7, cx + 12, cy + 7], 2, outline=col, width=2); d.line([cx + 3, cy - 12, cx + 3, cy + 12], fill=col, width=2)
        d.line([cx - 1, cy - 12, cx + 7, cy - 12], fill=col, width=2); d.line([cx - 1, cy + 12, cx + 7, cy + 12], fill=col, width=2)
    elif name == "Partager":
        d.rounded_rectangle([cx - 10, cy - 2, cx + 10, cy + 12], 2, outline=col, width=2); d.line([cx, cy + 4, cx, cy - 12], fill=col, width=2)
        d.line([cx - 6, cy - 6, cx, cy - 12, cx + 6, cy - 6], fill=col, width=2)
    elif name == "Supprimer":
        d.rectangle([cx - 8, cy - 6, cx + 8, cy + 12], outline=col, width=2); d.line([cx - 12, cy - 8, cx + 12, cy - 8], fill=col, width=2)
        d.line([cx - 4, cy - 12, cx + 4, cy - 12], fill=col, width=2)

# ---------- menus du clic droit ----------
def menu_pos(r):
    return (r[2] - 30, r[1] + 50)

def icon_rect(pos, i):
    x, y = pos; return (x + 10 + i * 46, y + 8, x + 50 + i * 46, y + 48)

def draw_menu(d, pos, hover=None, only=None):
    """Menu du clic droit : rangée d'icônes en haut, puis des lignes. only : icônes affichées (menu dans le vide)."""
    names = only or ICONES; x, y = pos; w = max(290, 20 + 46 * len(names))
    d.rounded_rectangle([x + 5, y + 6, x + w + 5, y + 236], 10, fill=(150, 155, 170))
    d.rounded_rectangle([x, y, x + w, y + 230], 10, fill=(252, 252, 254), outline=(180, 185, 195), width=2)
    for i, n in enumerate(names):
        r = icon_rect(pos, i)
        if hover == n: d.rounded_rectangle(r, 6, fill=(220, 232, 248))
        ico(d, n, *R.center(r))
    d.line([x + 10, y + 56, x + w - 10, y + 56], fill=(225, 228, 234), width=2)
    if only:
        d.text((x + 46, y + 70), "Nouveau", font=F(19, "s"), fill=(20, 20, 20)); d.text((x + w - 30, y + 69), "›", font=F(20, "b"), fill=(60, 60, 60))
        k0 = 1
    else:
        k0 = 0
    for k in range(k0, 4):
        d.rounded_rectangle([x + 46, y + 76 + k * 38, x + 46 + 150 - 25 * (k % 2), y + 90 + k * 38], 5, fill=(225, 228, 234))
    if hover:
        i = names.index(hover); r = icon_rect(pos, i); f = F(18, "s"); tw = d.textlength(hover, font=f)
        tx = R.center(r)[0] - tw / 2 - 10
        d.rounded_rectangle([tx, r[1] - 44, tx + tw + 20, r[1] - 10], 6, fill=(255, 255, 255), outline=(120, 125, 140), width=2)
        d.text((tx + 10, r[1] - 40), hover, font=f, fill=(20, 20, 20))

def text_menu(d, pos, hover=False):
    """Menu du clic droit dans la Corbeille : « Restaurer » en premier (texte)."""
    x, y = pos
    d.rounded_rectangle([x + 5, y + 6, x + 245, y + 166], 10, fill=(150, 155, 170))
    d.rounded_rectangle([x, y, x + 240, y + 160], 10, fill=(252, 252, 254), outline=(180, 185, 195), width=2)
    r = restore_rect(pos)
    if hover: d.rounded_rectangle(r, 6, fill=(220, 232, 248))
    d.text((r[0] + 14, r[1] + 8), "Restaurer", font=F(20, "s"), fill=(20, 20, 20))
    for k in range(3):
        d.rounded_rectangle([x + 24, y + 70 + k * 30, x + 190 - 20 * (k % 2), y + 82 + k * 30], 5, fill=(225, 228, 234))

def restore_rect(pos): x, y = pos; return (x + 8, y + 10, x + 232, y + 50)

# ---------- écrans ----------
def screen(view="Documents", folders=None, edit=None, faded=None, sel=None):
    """view : 'bureau' (bureau seul), 'Documents', 'Bureau', 'Corbeille'."""
    if view == "bureau":
        im = R.screen({"window": False}); d = ImageDraw.Draw(im)
        d.rectangle([30, 30, 130, 125], fill=R.BG.getpixel((80, 80)))
        trash(d, 58, 40); d.text((40, 100), "Corbeille", font=F(16, "s"), fill=(255, 255, 255))
        return im
    folders = DOCS if folders is None else folders
    st = {"window": True, "view": view, "folders": folders}
    if edit is not None: st["edit"] = edit
    im = R.screen(st); d = ImageDraw.Draw(im)
    if view == "Corbeille":
        d.rectangle([R.WX + 2, R.CMD_Y, R.WX + R.WW - 2, R.CMD_Y + 52], fill=(246, 248, 252))
        trash(d, R.WX + 14, R.WY + 6, 0.45)
    if faded is not None:
        r = R.rect_of(f"folder:{faded}")
        ov = Image.new("RGBA", (int(r[2] - r[0]), int(r[3] - r[1])), (255, 255, 255, 140)); im.paste(ov, (int(r[0]), int(r[1])), ov)
    if sel is not None:
        r = R.rect_of(f"folder:{sel}"); ImageDraw.Draw(im).rounded_rectangle(r, 8, fill=None, outline=BLEU, width=3)
    return im

def trash(d, x, y, s=1.0):
    d.polygon([(x + 6 * s, y + 14 * s), (x + 40 * s, y + 14 * s), (x + 36 * s, y + 56 * s), (x + 10 * s, y + 56 * s)], fill=(220, 235, 250), outline=(90, 110, 140))
    d.rectangle([x + 2 * s, y + 8 * s, x + 44 * s, y + 14 * s], fill=(180, 200, 225), outline=(90, 110, 140))
    for k in range(3): d.line([x + (15 + k * 8) * s, y + 20 * s, x + (15 + k * 8) * s, y + 50 * s], fill=(90, 110, 140), width=max(1, int(2 * s)))

def click_label(d, c, txt="clic DROIT"):
    d.text((c[0] - 80, c[1] + 50), txt, font=F(30, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))

def ctx_action(base, after, target, item, t, D, cap, start, menu_only=None, show_loupe=True):
    """Clic droit sur target (rectangle), puis clic sur l'icône item. base/after : fonctions qui rendent l'écran."""
    pos = menu_pos(target); names = menu_only or ICONES
    ir = icon_rect(pos, names.index(item)); ct = R.center(target); ci = R.center(ir)
    t1, t2, t3 = 0.28 * D, 0.62 * D, 0.72 * D
    if t < t1:
        im = base(); d = ImageDraw.Draw(im); R.highlight(d, target, t); R.arrow(d, target, t)
        cur = R.move(t, 0.04 * D, 0.22 * D, start, ct); R.cursor(d, *cur)
        if t > 0.2 * D: click_label(d, ct)
    elif t < t3 + 0.3:
        im = base(); clean = None; d = ImageDraw.Draw(im)
        cur = R.move(t, t1 + 0.04 * D, t2 - 0.06 * D, ct, (ci[0] - 4, ci[1] - 4))
        near = math.dist(cur, ci) < 30
        draw_menu(d, pos, hover=item if near else None, only=menu_only)
        clean = im.copy()
        R.highlight(d, ir, t)
        if show_loupe and near and t < t3: R.loupe(im, ir, place=(R.WX + 230, 380), clean=clean); d = ImageDraw.Draw(im)
        R.cursor(d, *cur); R.ripple(d, ct[0], ct[1], (t - t1) / 0.6, ORANGE); R.ripple(d, ci[0], ci[1], (t - t3) / 0.6)
    else:
        im = after(); d = ImageDraw.Draw(im); R.cursor(d, *ci)
    R.caption(d, cap); return im

def text_ctx(base, after, target, t, D, cap, start):
    pos = menu_pos(target); rr = restore_rect(pos); ct = R.center(target); ci = R.center(rr)
    t1, t3 = 0.3 * D, 0.72 * D
    if t < t1:
        im = base(); d = ImageDraw.Draw(im); R.highlight(d, target, t); R.arrow(d, target, t)
        R.cursor(d, *R.move(t, 0.04 * D, 0.22 * D, start, ct))
        if t > 0.2 * D: click_label(d, ct)
    elif t < t3 + 0.3:
        im = base(); d = ImageDraw.Draw(im); cur = R.move(t, t1 + 0.04 * D, t3 - 0.08 * D, ct, (ci[0] - 40, ci[1] - 4))
        text_menu(d, pos, hover=math.dist(cur, (ci[0] - 40, ci[1])) < 40); R.highlight(d, rr, t)
        R.cursor(d, *cur); R.ripple(d, ct[0], ct[1], (t - t1) / 0.6, ORANGE); R.ripple(d, ci[0] - 40, ci[1], (t - t3) / 0.6)
    else:
        im = after(); d = ImageDraw.Draw(im)
    R.caption(d, cap); return im

def click(base, after, target, t, D, cap, start, double=False):
    c = R.center(target); tc = 0.6 * D
    im = (after if t >= tc + (0.5 if double else 0.3) else base)(); d = ImageDraw.Draw(im)
    if t < tc + 0.3: R.highlight(d, target, t); R.arrow(d, target, t)
    R.cursor(d, *R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4)))
    R.ripple(d, c[0], c[1], (t - tc) / 0.6)
    if double: R.ripple(d, c[0], c[1], (t - tc - 0.25) / 0.6)
    R.caption(d, cap); return im

# ---------- scènes ----------
F0, F1, F2 = (R.rect_of(f"folder:{i}") for i in range(3))
EMPTY = (R.CONT_X + 120, R.CONT_Y + 200, R.CONT_X + 180, R.CONT_Y + 250)
NAV_B = R.rect_of("nav:Bureau"); NAV_D = R.rect_of("nav:Documents")
CORB = (40, 34, 130, 124)

def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Renommer, déplacer, copier,", ["effacer un dossier", "", "Aide-mémoire n° 09 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); R.folder_icon(d, W / 2 - 60, 345, 1.3); return im
    if sid == "intro":
        im = R.card("", [], None); d = ImageDraw.Draw(im)
        items = [("Renommer", "Courrier"), ("Copier", "×2"), ("Déplacer", "→"), ("Supprimer", "")]
        for i, (lab, extra) in enumerate(items):
            if p > 0.12 + i * 0.13:
                x = 170 + i * 250; R.folder_icon(d, x, 140, 1.5)
                ico(d, {"Déplacer": "Couper"}.get(lab, lab), x + 68, 300, (147, 17, 126))
                tw = d.textlength(lab, font=F(30, "b")); d.text((x + 68 - tw / 2, 340), lab, font=F(30, "b"), fill=(147, 17, 126))
        R.caption(d, cap); return im
    if sid == "menu":
        pos = menu_pos(F0); seq = ICONES
        if p < 0.3:
            im = screen(); d = ImageDraw.Draw(im); R.highlight(d, F0, t); R.cursor(d, *R.move(t, 0.02 * D, 0.2 * D, (W / 2 + 200, H / 2 + 100), R.center(F0)))
            if p > 0.2: click_label(d, R.center(F0))
        else:
            k = min(len(seq) - 1, int((p - 0.45) / 0.09)) if p > 0.45 else None
            im = screen(); d = ImageDraw.Draw(im); hv = seq[k] if k is not None else None
            draw_menu(d, pos, hover=hv)
            if p < 0.45: R.highlight(d, (pos[0] + 6, pos[1] + 4, pos[0] + 290, pos[1] + 52), t)
            cur = R.center(icon_rect(pos, k)) if k is not None else R.center(F0)
            R.cursor(d, *cur); R.ripple(d, *R.center(F0), (t - 0.3 * D) / 0.6, ORANGE)
        R.caption(d, cap); return im
    if sid == "renommer":
        return ctx_action(lambda: screen(), edit_first, F0, "Renommer", t, D, cap, (W / 2 + 200, H / 2 + 100))
    if sid == "taper":
        return typing_first("Courrier", t, D, cap)
    if sid == "copier":
        base = lambda: screen("Documents", ["Courrier", "Factures", "Recettes"])
        return ctx_action(base, lambda: screen("Documents", ["Courrier", "Factures", "Recettes"], sel=2), F2, "Copier", t, D, cap, (W / 2, H / 2 + 120))
    if sid == "coller":
        docs = lambda: screen("Documents", ["Courrier", "Factures", "Recettes"], sel=2)
        if p < 0.35:
            return click(docs, lambda: screen("Bureau", []), NAV_B, t, 0.35 * D, cap, R.center(F2))
        tt = t - 0.35 * D; DD = 0.65 * D
        im = ctx_action(lambda: screen("Bureau", []), lambda: screen("Bureau", ["Recettes"]), EMPTY, "Coller", tt, DD, cap, R.center(NAV_B), menu_only=["Coller"])
        if tt > 0.85 * DD:
            d = ImageDraw.Draw(im); R.highlight(d, F0, t); d.text((W / 2 - 40, H / 2 + 110), "Copié !", font=F(52, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
        return im
    if sid == "deplacer":
        D3 = ["Courrier", "Factures", "Recettes"]
        if p < 0.42:
            return ctx_action(lambda: screen("Documents", D3), lambda: screen("Documents", D3, faded=1), F1, "Couper", t, 0.42 * D, cap, (W / 2, H / 2 + 120))
        tt = t - 0.42 * D
        if p < 0.6:
            return click(lambda: screen("Documents", D3, faded=1), lambda: screen("Bureau", ["Recettes"]), NAV_B, tt, 0.18 * D, cap, R.center(F1))
        tt = t - 0.6 * D; DD = 0.4 * D
        im = ctx_action(lambda: screen("Bureau", ["Recettes"]), lambda: screen("Bureau", ["Recettes", "Factures"]), EMPTY, "Coller", tt, DD, cap, R.center(NAV_B), menu_only=["Coller"], show_loupe=False)
        if tt > 0.85 * DD:
            d = ImageDraw.Draw(im); R.highlight(d, F1, t)
        return im
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "supprimer":
        D3 = ["Courrier", "Factures", "Recettes"]
        im = ctx_action(lambda: screen("Documents", D3), lambda: screen("Documents", ["Courrier", "Recettes"]), F1, "Supprimer", t, D, cap, (W / 2, H / 2 + 120))
        if p > 0.8:
            d = ImageDraw.Draw(im); d.text((W / 2 - 40, H / 2 + 110), "→ Corbeille", font=F(44, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
        return im
    if sid == "corbeille":
        if p < 0.12:
            im = R.card("Pas de panique !", ["Un dossier jeté par erreur", "se récupère."], None); d = ImageDraw.Draw(im); trash(d, W / 2 - 46, 300, 2.0); return im
        if p < 0.42:
            return click(lambda: screen("bureau"), lambda: screen("Corbeille", ["Factures"]), CORB, t - 0.12 * D, 0.3 * D, cap, (W / 2, H / 2), double=True)
        tt = t - 0.42 * D; DD = 0.58 * D
        im = text_ctx(lambda: screen("Corbeille", ["Factures"]), lambda: screen("Corbeille", []), F0, tt, DD, cap, (W / 2, H / 2))
        if tt > 0.8 * DD:
            d = ImageDraw.Draw(im); d.text((W / 2 - 200, H / 2 + 60), "Il retourne à sa place", font=F(40, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
        return im
    if sid == "exercice":
        return R.card("Exercice", ["Renommez le dossier « Essai »", "en « Vacances ».", "Puis supprimez-le."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Renommez « Essai » en « Vacances »,", "puis supprimez-le."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        S = ["Courrier", "Essai"]; e = R.rect_of("folder:1")
        if p < 0.3:
            return ctx_action(lambda: screen("Documents", S), lambda: edit_last(S), e, "Renommer", t, 0.3 * D, cap, (W / 2, H / 2 + 120), show_loupe=False)
        if p < 0.62:
            return typing_last(S, "Vacances", t - 0.3 * D, 0.32 * D, cap)
        im = ctx_action(lambda: screen("Documents", ["Courrier", "Vacances"]), lambda: screen("Documents", ["Courrier"]), e, "Supprimer", t - 0.62 * D, 0.38 * D, cap, R.center(e), show_loupe=False)
        if p > 0.92:
            d = ImageDraw.Draw(im); d.text((W / 2 - 60, H / 2 + 110), "Bravo !", font=F(52, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
        return im
    if sid == "resume":
        return R.card("À retenir", ["1. Clic droit sur le dossier", "2. Renommer · Copier · Couper", "3. Clic droit dans le vide : Coller", "4. Supprimer → la Corbeille garde tout"], "Bravo ! À bientôt à Espace 19 Numérique !")
    raise KeyError(sid)

# --- renommer le PREMIER dossier : render_01 n'édite que le dernier, on dessine donc l'édition nous-mêmes ---
def edit_box(im, idx, txt, selected):
    d = ImageDraw.Draw(im); r = R.rect_of(f"folder:{idx}")
    d.rectangle([r[0] - 6, r[1] + 90, r[2] + 6, r[1] + 122], fill=(255, 255, 255))
    tw = d.textlength(txt or " ", font=F(17)); bx0 = (r[0] + r[2]) / 2 - max(tw, 20) / 2 - 6
    d.rectangle([bx0, r[1] + 92, bx0 + max(tw, 20) + 12, r[1] + 120], fill=(255, 255, 255), outline=BLEU, width=2)
    if selected:
        d.rectangle([bx0 + 5, r[1] + 95, bx0 + 7 + tw, r[1] + 117], fill=BLEU); d.text((bx0 + 6, r[1] + 95), txt, font=F(17), fill=(255, 255, 255))
    else:
        d.text((bx0 + 6, r[1] + 95), txt, font=F(17), fill=(0, 0, 0)); cx = bx0 + 7 + tw; d.line([cx, r[1] + 96, cx, r[1] + 116], fill=(0, 0, 0), width=2)
    return im

def edit_first(): return edit_box(screen(), 0, "Lettres", True)
def edit_last(S): return edit_box(screen("Documents", S), len(S) - 1, S[-1], True)

def _typing(S, idx, word, t, D, cap, final=None):
    p = t / D; p0, p1, ent = 0.25, 0.6, 0.72
    if p < ent + 0.08:
        k = int(len(word) * R.ease((p - p0) / (p1 - p0))) if p > p0 else 0
        im = edit_box(screen("Documents", S), idx, S[idx] if k == 0 else word[:k], k == 0); d = ImageDraw.Draw(im)
        r = R.rect_of(f"folder:{idx}"); r2 = (r[0] - 10, r[1] + 85, r[2] + 10, r[3] - 5)
        if p < ent - 0.05:
            R.highlight(d, r2, t); clean = im.copy()
            if p > 0.1: R.loupe(im, r2, place=(W - 230, 330), clean=clean); d = ImageDraw.Draw(im)
        else:
            R.key_enter(d, t, p > ent)
    else:
        nf = list(S); nf[idx] = word
        im = screen("Documents", nf); d = ImageDraw.Draw(im); R.highlight(d, R.rect_of(f"folder:{idx}"), t)
        if final: d.text((W / 2 - 80, H / 2 + 120), final, font=F(56, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
    R.caption(d, cap); return im

def typing_first(word, t, D, cap): return _typing(DOCS, 0, word, t, D, cap, "Bravo !")
def typing_last(S, word, t, D, cap): return _typing(S, len(S) - 1, word, t, D, cap)

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
