"""Vidéo « 11 - Renommer, déplacer, copier, supprimer, récupérer un fichier » (écrans dessinés, sous-titrée).
Usage : python3 render_11.py script.json durations.json out.mp4
        python3 render_11.py --estimate script.json durations.json
Réutilise ../render_01.py (bureau, fenêtre de l'Explorateur, curseur, cadre jaune, flèche, loupe, titres, sous-titres, cartes)
et ../01-ordinateur/render_01_ordinateur.py (pièce, étiquettes).
Libellés écrits tels quels (voir sources_11.md) : « Couper », « Copier », « Coller », « Renommer », « Partager », « Supprimer »
(icônes en haut du menu du clic droit et dans la barre de la fenêtre ; le nom apparaît quand on pose la souris),
« Corbeille », « Restaurer ». Non écrits (une seule source) : F2, Suppr, « Vider la Corbeille ».
"""
import json, math, os, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
for p in ("..", "../01-ordinateur", "../04-arborescence"): sys.path.insert(0, os.path.join(ICI, p))
import render_01 as R
import render_01_ordinateur as O
from PIL import Image, ImageDraw

W, H, FPS, YEL, F = R.W, R.H, R.FPS, R.YEL, R.F
INK = (40, 40, 50); VIO = (147, 17, 126); BLEU = (0, 103, 192)
WX, WY, WW, CMD_Y = R.WX, R.WY, R.WW, R.CMD_Y

# ---------- icônes de fichier ----------
def file_icon(d, x, y, s=1.0):
    w, h = 64 * s, 82 * s
    d.polygon([(x, y), (x + w - 18 * s, y), (x + w, y + 18 * s), (x + w, y + h), (x, y + h)], fill=(255, 255, 255), outline=(120, 130, 150))
    d.polygon([(x + w - 18 * s, y), (x + w - 18 * s, y + 18 * s), (x + w, y + 18 * s)], fill=(215, 222, 235), outline=(120, 130, 150))
    for k in range(4): d.line([x + 10 * s, y + (32 + k * 12) * s, x + w - 10 * s, y + (32 + k * 12) * s], fill=BLEU, width=max(2, int(3 * s)))

def item_rect(i): return R.rect_of(f"folder:{i}")

# ---------- les 6 icônes (menu du clic droit et barre de la fenêtre) ----------
ACTIONS = ["Couper", "Copier", "Coller", "Renommer", "Partager", "Supprimer"]
def glyph(d, name, cx, cy, s=1.0, col=(40, 40, 50)):
    w = max(2, int(2.5 * s))
    if name == "Couper":
        d.ellipse([cx - 9 * s, cy + 3 * s, cx - 1 * s, cy + 11 * s], outline=col, width=w); d.ellipse([cx + 1 * s, cy + 3 * s, cx + 9 * s, cy + 11 * s], outline=col, width=w)
        d.line([cx - 3 * s, cy + 4 * s, cx + 6 * s, cy - 11 * s], fill=col, width=w); d.line([cx + 3 * s, cy + 4 * s, cx - 6 * s, cy - 11 * s], fill=col, width=w)
    elif name == "Copier":
        d.rounded_rectangle([cx - 9 * s, cy - 6 * s, cx + 4 * s, cy + 11 * s], 3, outline=col, width=w)
        d.rounded_rectangle([cx - 4 * s, cy - 11 * s, cx + 9 * s, cy + 6 * s], 3, outline=col, width=w, fill=(255, 255, 255))
    elif name == "Coller":
        d.rounded_rectangle([cx - 9 * s, cy - 8 * s, cx + 9 * s, cy + 11 * s], 3, outline=col, width=w)
        d.rounded_rectangle([cx - 4 * s, cy - 12 * s, cx + 4 * s, cy - 5 * s], 2, fill=col)
    elif name == "Renommer":
        d.rounded_rectangle([cx - 11 * s, cy - 6 * s, cx + 11 * s, cy + 6 * s], 3, outline=col, width=w)
        d.line([cx + 4 * s, cy - 11 * s, cx + 4 * s, cy + 11 * s], fill=col, width=w)
    elif name == "Partager":
        d.line([cx - 8 * s, cy + 9 * s, cx - 8 * s, cy - 2 * s, cx + 6 * s, cy - 2 * s], fill=col, width=w)
        d.line([cx + 1 * s, cy - 8 * s, cx + 8 * s, cy - 2 * s, cx + 1 * s, cy + 4 * s], fill=col, width=w)
    elif name == "Supprimer":
        d.line([cx - 10 * s, cy - 8 * s, cx + 10 * s, cy - 8 * s], fill=col, width=w); d.line([cx - 3 * s, cy - 11 * s, cx + 3 * s, cy - 11 * s], fill=col, width=w)
        d.polygon([(cx - 7 * s, cy - 6 * s), (cx + 7 * s, cy - 6 * s), (cx + 5 * s, cy + 11 * s), (cx - 5 * s, cy + 11 * s)], outline=col)
        d.line([cx - 7 * s, cy - 6 * s, cx - 5 * s, cy + 11 * s, cx + 5 * s, cy + 11 * s, cx + 7 * s, cy - 6 * s], fill=col, width=w)

def tooltip(d, text, x, y):
    f = F(19, "s"); tw = d.textlength(text, font=f)
    d.rounded_rectangle([x - tw / 2 - 10, y, x + tw / 2 + 10, y + 34], 6, fill=(255, 255, 240), outline=(90, 90, 90), width=2)
    d.text((x - tw / 2, y + 6), text, font=f, fill=(20, 20, 20))

# barre de la fenêtre : les 6 icônes remplacent les rectangles gris de render_01
def bar_rect(name):
    i = ACTIONS.index(name); x = WX + 166 + i * 52
    return (x, CMD_Y + 8, x + 40, CMD_Y + 46)

def draw_bar(d, hover=None):
    d.rectangle([WX + 160, CMD_Y + 6, WX + 480, CMD_Y + 48], fill=(246, 248, 252))
    for n in ACTIONS:
        r = bar_rect(n)
        if n == hover: d.rounded_rectangle(r, 6, fill=(220, 232, 248))
        glyph(d, n, *R.center(r), 1.0)

# menu du clic droit sur un élément
CTX_W, CTX_H = 330, 210
def ctx_pos(i):
    r = item_rect(i); return (r[0] + 70, r[1] + 70)
def ctx_icon_rect(i, name):
    x, y = ctx_pos(i); k = ACTIONS.index(name) if name in ACTIONS else 0
    names = CTX_ICONS
    k = names.index(name); return (x + 12 + k * 52, y + 10, x + 56 + k * 52, y + 52)
CTX_ICONS = ["Couper", "Copier", "Renommer", "Partager", "Supprimer"]
def ctx_restaurer_rect(i):
    x, y = ctx_pos(i); return (x + 10, y + 62, x + CTX_W - 10, y + 104)

def draw_ctx(d, i, hover=None, corbeille=False):
    x, y = ctx_pos(i)
    if corbeille:
        d.rounded_rectangle([x, y, x + CTX_W, y + 170], 10, fill=(252, 252, 254), outline=(170, 175, 185), width=2)
        r = ctx_restaurer_rect(i)
        if hover == "Restaurer": d.rounded_rectangle(r, 6, fill=(220, 232, 248))
        d.text((r[0] + 46, r[1] + 9), "Restaurer", font=F(20, "s"), fill=(20, 20, 20))
        d.ellipse([r[0] + 12, r[1] + 10, r[0] + 34, r[1] + 32], outline=INK, width=3)
        for k in range(2): d.rounded_rectangle([x + 56, y + 122 + k * 0, x + 230, y + 136], 5, fill=(225, 228, 234))
        d.rounded_rectangle([x + 20, y + 14, x + 200, y + 30], 5, fill=(225, 228, 234))
        return
    d.rounded_rectangle([x, y, x + CTX_W, y + CTX_H], 10, fill=(252, 252, 254), outline=(170, 175, 185), width=2)
    for n in CTX_ICONS:
        r = ctx_icon_rect(i, n)
        if n == hover: d.rounded_rectangle(r, 6, fill=(220, 232, 248))
        glyph(d, n, *R.center(r), 1.0)
    d.line([x + 10, y + 60, x + CTX_W - 10, y + 60], fill=(225, 228, 235), width=2)
    for k in range(4):
        d.rounded_rectangle([x + 50, y + 78 + k * 32, x + 50 + (190 - 25 * (k % 2)), y + 92 + k * 32], 5, fill=(225, 228, 234))
    if hover in CTX_ICONS:
        r = ctx_icon_rect(i, hover); tooltip(d, hover, R.center(r)[0], r[1] - 44)

# ---------- écrans ----------
# items : liste de (nom, "d" dossier | "f" fichier) ; edit : (index, texte, sélectionné)
def window(view, items, title=None, edit=None, sel=None, hide=None, bar_hover=None):
    im = R.screen({"window": True, "view": "Documents" if view == "Corbeille" else view, "folders": []})
    d = ImageDraw.Draw(im)
    if view == "Corbeille":   # titre et en-tête de la vue Corbeille (la Corbeille n'est pas dans le volet de gauche)
        d.rectangle([WX + 40, WY + 6, WX + 400, WY + 32], fill=(232, 236, 244)); d.text((WX + 44, WY + 9), "Corbeille", font=F(17, "s"), fill=(30, 30, 30))
        d.rectangle([R.CONT_X + 10, R.CONT_Y - 34, R.CONT_X + 400, R.CONT_Y - 2], fill=(255, 255, 255))
        d.text((R.CONT_X + 20, R.CONT_Y - 30), "Corbeille", font=F(22, "b"), fill=(30, 30, 30))
        nav = R.rect_of("nav:Documents"); d.rounded_rectangle(nav, 6, fill=(255, 255, 255)); R.folder_icon(d, nav[0] + 8, nav[1] + 9, 0.23); d.text((nav[0] + 40, nav[1] + 8), "Documents", font=F(17), fill=(20, 20, 20))
    draw_bar(d, bar_hover)
    for i, (name, kind) in enumerate(items):
        if hide == i: continue
        r = item_rect(i)
        if sel == i: d.rounded_rectangle(r, 8, fill=(220, 232, 248), outline=BLEU, width=2)
        if kind == "d": R.folder_icon(d, r[0] + 20, r[1] + 10, 1.0)
        else: file_icon(d, r[0] + 33, r[1] + 4)
        if edit and edit[0] == i:
            txt, selected = edit[1], edit[2]; f = F(17); tw = d.textlength(txt or " ", font=f)
            bx0 = (r[0] + r[2]) / 2 - max(tw, 20) / 2 - 6
            d.rectangle([bx0, r[1] + 92, bx0 + max(tw, 20) + 12, r[1] + 120], fill=(255, 255, 255), outline=BLEU, width=2)
            if selected:
                d.rectangle([bx0 + 5, r[1] + 95, bx0 + 7 + tw, r[1] + 117], fill=BLEU); d.text((bx0 + 6, r[1] + 95), txt, font=f, fill=(255, 255, 255))
            else:
                d.text((bx0 + 6, r[1] + 95), txt, font=f, fill=(0, 0, 0)); d.line([bx0 + 7 + tw, r[1] + 96, bx0 + 7 + tw, r[1] + 116], fill=(0, 0, 0), width=2)
        else:
            f = F(17); tw = d.textlength(name, font=f)
            d.text(((r[0] + r[2]) / 2 - tw / 2, r[1] + 95), name, font=f, fill=(20, 20, 20))
    return im

DOCS0 = [("Famille", "d"), ("Factures", "d"), ("Courses", "f"), ("Photo", "f")]
DOCS1 = [("Famille", "d"), ("Factures", "d"), ("Liste de courses", "f"), ("Photo", "f")]
DOCS2 = [("Famille", "d"), ("Factures", "d"), ("Photo", "f")]
FAM0 = [("Liste de courses", "f")]
FAM1 = [("Liste de courses", "f"), ("Photo", "f")]

# bureau avec la Corbeille (render_01 dessine « Corbeille » à (40,40) sur le bureau)
CORB = (24, 30, 120, 124)
def desktop():
    im = R.screen({"window": False}); d = ImageDraw.Draw(im)
    d.rectangle([30, 34, 120, 96], fill=R.BG.getpixel((60, 60)))
    x, y = 48, 40   # poubelle dessinée à la place du dossier
    d.polygon([(x + 6, y + 14), (x + 46, y + 14), (x + 41, y + 56), (x + 11, y + 56)], fill=(225, 235, 245), outline=(80, 90, 110))
    d.rectangle([x + 2, y + 8, x + 50, y + 14], fill=(200, 215, 230), outline=(80, 90, 110))
    for k in range(3): d.line([x + 17 + k * 9, y + 20, x + 17 + k * 9, y + 50], fill=(120, 140, 170), width=2)
    return im

def act(base_im_fn, after_fn, r, start, t, D, cap, double=False, right=False, loupe=True, place=None, overlay=None, loupe_r=None):
    """Curseur qui va vers r, cadre + flèche + loupe, clic à 60 %."""
    c = R.center(r); tc = 0.6 * D
    after = t >= tc + (0.5 if double else 0.3)
    im = after_fn() if after else base_im_fn(); clean = im.copy(); d = ImageDraw.Draw(im)
    if overlay and not after: overlay(d)
    if not after:
        R.highlight(d, r, t); R.arrow(d, r, t)
    pos = R.move(t, 0.15 * D, 0.5 * D, start, (c[0] - 4, c[1] - 4))
    if loupe and 0.2 * D < t < tc + 0.3:
        R.loupe(im, loupe_r or r, place=place, clean=clean); d = ImageDraw.Draw(im)
    R.cursor(d, *pos)
    col = (255, 120, 0) if right else YEL
    R.ripple(d, c[0], c[1], (t - tc) / 0.6, col)
    if double: R.ripple(d, c[0], c[1], (t - tc - 0.25) / 0.6)
    if right and 0.3 * D < t < tc + 0.4:
        d.text((c[0] - 90, c[1] + 50), "clic DROIT", font=F(30, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
    R.caption(d, cap); return im

def ctx_click(items, view, i, name, t, D, cap, after_items=None, after_edit=None, start=None, corbeille=False, after_view=None):
    """Deux temps : clic droit sur l'élément i (0 → 45 %), puis clic sur l'icône « name » du menu (45 → 100 %)."""
    t1 = 0.45 * D
    st = start or (W / 2 + 200, H / 2 + 120)
    if t < t1:
        return act(lambda: window(view, items), lambda: (_w := window(view, items, sel=i), draw_ctx(ImageDraw.Draw(_w), i, corbeille=corbeille), _w)[2],
                   item_rect(i), st, t, t1, cap, right=True, loupe=False)
    r = ctx_restaurer_rect(i) if corbeille else ctx_icon_rect(i, name)
    def before():
        im = window(view, items, sel=i); dd = ImageDraw.Draw(im)
        draw_ctx(dd, i, hover=name if (t - t1) > 0.35 * (D - t1) else None, corbeille=corbeille); return im
    def after():
        return window(after_view or view, after_items if after_items is not None else items, edit=after_edit)
    lr = (r[0], r[1], r[0] + 170, r[3]) if corbeille else None
    return act(before, after, r, R.center(item_rect(i)), t - t1, D - t1, cap, loupe=True, place=(1040, 470), loupe_r=lr)

# ---------- scènes ----------
def frame(sid, t, D, cap):
    p = t / D
    if sid == "titre":
        im = R.card("Gérer un fichier", ["Renommer · déplacer · copier", "supprimer · récupérer", "Aide-mémoire n° 11 · Formation débutant"], "Espace 19 Numérique")
        d = ImageDraw.Draw(im); file_icon(d, W / 2 - 40, 360, 1.1); return im
    if sid == "intro":
        im = O.room(); d = ImageDraw.Draw(im)
        file_icon(d, 140, 200, 2.0)
        steps = [("changer son nom", "Renommer"), ("le ranger ailleurs", None), ("le photocopier", "Copier"), ("le jeter", "Supprimer"), ("le récupérer", None)]
        for k, (txt, g) in enumerate(steps):
            if p > 0.18 + k * 0.1:
                y = 130 + k * 80
                d.rounded_rectangle([420, y, 1100, y + 64], 14, fill=(255, 255, 255), outline=YEL, width=4)
                d.text((450, y + 13), f"{k + 1}. {txt}", font=F(32, "s"), fill=VIO)
        R.caption(d, cap); return im
    if sid == "menu":
        if p < 0.3:
            return act(lambda: window("Documents", DOCS0), lambda: window("Documents", DOCS0), item_rect(2), (W / 2 + 200, H / 2 + 100), t, 0.3 * D, cap, right=True, loupe=False)
        im = window("Documents", DOCS0, sel=2); d = ImageDraw.Draw(im)
        k = min(4, int((p - 0.45) / 0.1)) if p > 0.45 else -1
        hv = CTX_ICONS[k] if k >= 0 else None
        draw_ctx(d, 2, hover=hv)
        x, y = ctx_pos(2); R.highlight(d, (x + 8, y + 6, x + CTX_W - 8, y + 56), t)
        if hv: R.cursor(d, *R.center(ctx_icon_rect(2, hv)))
        else: R.cursor(d, *R.center(item_rect(2)))
        R.caption(d, cap); return im
    if sid == "renommer":
        if p < 0.6:
            return ctx_click(DOCS0, "Documents", 2, "Renommer", t, 0.6 * D, cap, after_edit=(2, "Courses", True))
        word = "Liste de courses"; k = int(len(word) * R.ease((p - 0.62) / 0.2)) if p > 0.62 else 0
        if p < 0.88:
            im = window("Documents", DOCS0, edit=(2, word[:k] if k else "Courses", k == 0)); d = ImageDraw.Draw(im)
            if p > 0.8: R.key_enter(d, t, p > 0.85)
        else:
            im = window("Documents", DOCS1); d = ImageDraw.Draw(im); R.highlight(d, item_rect(2), t)
            d.text((W / 2 - 110, H / 2 + 120), "Bravo !", font=F(56, "b"), fill=YEL, stroke_width=4, stroke_fill=(0, 0, 0))
        R.caption(d, cap); return im
    if sid == "deplacer":
        src, dst = item_rect(2), item_rect(0)
        if p < 0.25:
            im = window("Documents", DOCS1); d = ImageDraw.Draw(im); R.highlight(d, src, t); R.arrow(d, src, t)
            R.cursor(d, *R.move(t, 0, 0.2 * D, (W / 2 + 200, H / 2 + 150), R.center(src))); R.caption(d, cap); return im
        if p < 0.75:
            q = R.ease((p - 0.3) / 0.4); c = R.move(p, 0.3, 0.7, R.center(src), R.center(dst))
            im = window("Documents", DOCS1, hide=2 if p > 0.3 else None, sel=0 if q > 0.8 else None); d = ImageDraw.Draw(im)
            R.highlight(d, dst, t)
            file_icon(d, c[0] - 30, c[1] - 40, 0.9)
            d.text((c[0] + 40, c[1] + 30), "bouton appuyé", font=F(24, "b"), fill=YEL, stroke_width=3, stroke_fill=(0, 0, 0))
            R.cursor(d, c[0] - 4, c[1] - 4); R.caption(d, cap); return im
        im = window("Documents", DOCS2); d = ImageDraw.Draw(im); R.highlight(d, dst, t)
        O.label(d, "le fichier est dans « Famille »", (W / 2 + 120, 470)); R.cursor(d, *R.center(dst)); R.caption(d, cap); return im
    if sid == "copier":
        im = ctx_click(DOCS2, "Documents", 2, "Copier", t, D, cap)
        if p > 0.75: O.label(ImageDraw.Draw(im), "la copie est en mémoire", (W / 2 + 120, 470))
        return im
    if sid == "coller":
        if p < 0.4:
            return act(lambda: window("Documents", DOCS2), lambda: window("Famille", FAM0), item_rect(0), (W / 2, H / 2 + 100), t, 0.4 * D, cap, double=True, loupe=False)
        return act(lambda: window("Famille", FAM0, bar_hover="Coller" if p > 0.6 else None), lambda: window("Famille", FAM1),
                   bar_rect("Coller"), R.center(item_rect(0)), t - 0.4 * D, 0.6 * D, cap, place=(900, 420),
                   overlay=(lambda d: tooltip(d, "Coller", R.center(bar_rect("Coller"))[0], CMD_Y + 52)) if p > 0.6 else None)
    if sid == "pause1":
        return R.card("Pause", ["Mettez la vidéo en pause", "et essayez sur votre ordinateur."], "Relancez la vidéo quand vous êtes prêt.", "pause")
    if sid == "supprimer":
        im = ctx_click(FAM1, "Famille", 1, "Supprimer", t, D, cap, after_items=FAM0)
        if p > 0.75:
            d = ImageDraw.Draw(im); O.label(d, "direction la Corbeille", (W / 2 + 120, 470))
        return im
    if sid == "corbeille":
        def corb_win():
            return window("Corbeille", [("Photo", "f")])
        if p < 0.3:
            im = desktop(); d = ImageDraw.Draw(im)
            d.text((W / 2 - 300, H / 2 - 40), "Pas de panique !", font=F(64, "b"), fill=YEL, stroke_width=5, stroke_fill=(0, 0, 0))
            R.caption(d, cap); return im
        return act(desktop, corb_win, CORB, (W / 2, H / 2), t - 0.3 * D, 0.7 * D, cap, double=True, place=(400, 330))
    if sid == "restaurer":
        im = ctx_click([("Photo", "f")], "Corbeille", 0, "Restaurer", t, D, cap, after_items=[], corbeille=True)
        if p > 0.75:
            d = ImageDraw.Draw(im); O.label(d, "« Photo » est revenue dans « Famille »", (W / 2 + 120, 400))
        return im
    if sid == "bon":
        im = desktop(); d = ImageDraw.Draw(im); R.highlight(d, CORB, t)
        d.rounded_rectangle([230, 180, 1050, 470], 24, fill=(255, 255, 255), outline=YEL, width=6)
        for k, l in enumerate(["Tant que la Corbeille", "n'est pas vidée,", "vos fichiers peuvent revenir."]):
            tw = d.textlength(l, font=F(40, "b")); d.text((W / 2 + 0 - tw / 2 + 0, 220 + k * 70), l, font=F(40, "b"), fill=VIO)
        R.caption(d, cap); return im
    if sid == "exercice":
        return R.card("Exercice", ["Renommez un fichier,", "rangez-le dans un dossier,", "supprimez-le,", "puis restaurez-le."], "Mettez la vidéo en pause, puis faites l'exercice.")
    if sid == "attente":
        left = max(0, math.ceil(D - t))
        return R.card("À vous !", ["Renommer, ranger,", "supprimer, restaurer."], f"La solution arrive dans {left} s", "pause")
    if sid == "solution":
        segs = [0.0, 0.25, 0.5, 0.75, 1.01]
        k = next(i for i in range(4) if segs[i] * D <= t < segs[i + 1] * D)
        tt, DD = t - segs[k] * D, (segs[k + 1] - segs[k]) * D
        if k == 0:
            if tt < 0.7 * DD:
                return ctx_click(DOCS0, "Documents", 2, "Renommer", tt, 0.7 * DD, cap, after_edit=(2, "Courses", True))
            im = window("Documents", DOCS1); d = ImageDraw.Draw(im); R.highlight(d, item_rect(2), t); R.caption(d, cap); return im
        if k == 1:
            src, dst = item_rect(2), item_rect(0); q = tt / DD
            if q < 0.8:
                c = R.move(q, 0.1, 0.7, R.center(src), R.center(dst))
                im = window("Documents", DOCS1, hide=2 if q > 0.1 else None); d = ImageDraw.Draw(im); R.highlight(d, dst, t)
                if q > 0.1: file_icon(d, c[0] - 30, c[1] - 40, 0.9)
                R.cursor(d, c[0] - 4, c[1] - 4)
            else:
                im = window("Documents", DOCS2); d = ImageDraw.Draw(im); R.highlight(d, dst, t)
            R.caption(d, cap); return im
        if k == 2:
            return ctx_click(DOCS2, "Documents", 2, "Supprimer", tt, DD, cap, after_items=DOCS2[:2])
        if tt < 0.35 * DD:
            return act(desktop, lambda: window("Corbeille", [("Photo", "f")]), CORB, (W / 2, H / 2), tt, 0.35 * DD, cap, double=True, loupe=False)
        return ctx_click([("Photo", "f")], "Corbeille", 0, "Restaurer", tt - 0.35 * DD, 0.65 * DD, cap, after_items=[], corbeille=True)
    if sid == "resume":
        return R.card("À retenir", ["Clic droit sur le fichier", "Renommer · Copier · Supprimer", "Glisser : je range", "Corbeille → Restaurer"], "Bravo ! À bientôt à Espace 19 Numérique !")
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
