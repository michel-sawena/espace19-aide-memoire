"""Fiche aide-mémoire (HTML -> PDF via Chromium). Usage : python3 fiche_html.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB = 9
import os
LOGO = IMG + "/logo.png"
LOGO_TAG = ('<img class="logo" src="' + "data:image/png;base64," + base64.b64encode(open(LOGO,"rb").read()).decode() + '">') if os.path.exists(LOGO) else '<div class="logo vide">LOGO<br>ESPACE 19</div>'

def img(n):
    return "data:image/png;base64," + base64.b64encode(open(f"{IMG}/{n}.png", "rb").read()).decode()

def qr(u):
    q = qrcode.QRCode(border=1, box_size=12); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#14234B", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

# ---------- pictogrammes ----------
SOURIS_G = '''<svg viewBox="0 0 60 90" class="picto"><rect x="5" y="5" width="50" height="80" rx="25" fill="#fff" stroke="#14234B" stroke-width="4"/><path d="M5 35 H55 M30 5 V35" stroke="#14234B" stroke-width="4"/><path d="M8 33 V30 A22 22 0 0 1 28 7 V33 Z" fill="#FFC72C"/></svg>'''
SOURIS_D = '''<svg viewBox="0 0 60 90" class="picto"><rect x="5" y="5" width="50" height="80" rx="25" fill="#fff" stroke="#14234B" stroke-width="4"/><path d="M5 35 H55 M30 5 V35" stroke="#14234B" stroke-width="4"/><path d="M52 33 V30 A22 22 0 0 0 32 7 V33 Z" fill="#FF7A59"/></svg>'''
TOUCHE = '''<svg viewBox="0 0 120 80" class="picto large"><rect x="4" y="8" width="112" height="68" rx="12" fill="#5b6478"/><rect x="4" y="4" width="112" height="64" rx="12" fill="#fff" stroke="#14234B" stroke-width="4"/><text x="60" y="44" font-size="22" font-weight="700" text-anchor="middle" fill="#14234B" font-family="Inter">Entrée ↵</text></svg>'''
DOSSIER = '''<svg viewBox="0 0 220 170" class="dossier"><rect x="20" y="30" width="80" height="30" rx="8" fill="#E8A92C"/><rect x="50" y="10" width="110" height="120" rx="6" fill="#fff" stroke="#c9cfdb" stroke-width="3" transform="rotate(-8 105 70)"/><rect x="70" y="18" width="110" height="120" rx="6" fill="#fff" stroke="#c9cfdb" stroke-width="3" transform="rotate(6 125 78)"/><line x1="85" y1="45" x2="160" y2="52" stroke="#d6dbe5" stroke-width="5"/><line x1="83" y1="62" x2="150" y2="68" stroke="#d6dbe5" stroke-width="5"/><rect x="20" y="50" width="185" height="115" rx="12" fill="#FFC72C" stroke="#E0A419" stroke-width="4"/><circle cx="160" cy="125" r="0"/></svg>'''

def pied(n):
    return f'<div class="pied"><span>Espace 19 Numérique · Aide-mémoire n° 01</span><span class="pnum">page {n} / {NB}</span></div>'

def etape(num, action, detail, image, geste=""):
    return f'''<div class="etape"><div class="num">{num}</div><div class="txt"><h3>{action}</h3><p>{detail}</p>{geste}</div>
    <div class="zoom"><img src="{img(image)}"><span class="loupe">zoom</span></div></div>'''

def notes(n=3):
    return '<div class="minotes"><b>✎ Mes notes</b>' + '<div class="ligne"></div>' * n + '</div>'

CSS = '''
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Regular.otf);font-weight:400}
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf);font-weight:600}
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Bold.otf);font-weight:700}
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-ExtraBold.otf);font-weight:800}
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:Inter,sans-serif;color:#14234B;font-size:15.5pt;line-height:1.4}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:16mm 16mm 22mm;background:#fff}
.page.creme{background:#FFF8E7}
h1{font-size:34pt;line-height:1.1;margin:0 0 6mm;font-weight:800}
h2{font-size:26pt;margin:0 0 5mm;font-weight:800;display:flex;align-items:center;gap:4mm}
h2 .pastille{background:#FFC72C;border-radius:10mm;padding:1mm 5mm;font-size:16pt}
h3{font-size:19pt;margin:0 0 2mm;font-weight:700}
p{margin:0 0 3mm}
.pied{position:absolute;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;font-size:10.5pt;color:#4a5572;border-top:2px solid #FFC72C;padding-top:2.5mm}
.pnum{font-weight:700;color:#14234B}
/* couverture */
.logo{position:absolute;right:18mm;top:16mm;height:24mm;background:#fff;border-radius:5mm;padding:2mm}.logo.vide{width:40mm;display:flex;align-items:center;justify-content:center;text-align:center;color:#14234B;font-weight:800;font-size:11pt;border:2px dashed #FFC72C}
.cover{background:linear-gradient(160deg,#14234B 0%,#1f3a7a 60%,#2BB3A3 140%);color:#fff;padding:22mm 18mm}
.cover .badge{display:inline-block;background:#FFC72C;color:#14234B;font-weight:800;border-radius:12mm;padding:2mm 7mm;font-size:15pt}
.cover h1{font-size:50pt;margin:14mm 0 6mm;color:#fff}
.cover .sous{font-size:19pt;opacity:.95;max-width:150mm}
.cover .dossier{width:105mm;display:block;margin:10mm auto 8mm}
.cover .infos{display:flex;gap:5mm;justify-content:center}
.cover .infos div{white-space:nowrap;background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.4);border-radius:6mm;padding:3mm 6mm;font-size:14pt;font-weight:600}
.cover .rassure{position:absolute;left:18mm;right:18mm;bottom:30mm;background:#fff;color:#14234B;border-radius:8mm;padding:6mm 8mm;font-size:16pt;border-left:10px solid #FFC72C}
.cover .pied{color:#dfe6f5;border-color:#FFC72C}.cover .pnum{color:#fff}
/* cartes */
.carte{background:#fff;border-radius:7mm;padding:6mm 7mm;margin-bottom:5mm;border:2px solid #eadfc3}
.carte.jaune{background:#FFF1C9;border-color:#FFC72C}
.carte.verte{background:#E3F6F3;border-color:#2BB3A3}
.carte.corail{background:#FFEDE7;border-color:#FF7A59}
.analogie{display:flex;gap:6mm;align-items:center}
.analogie .dossier{width:52mm;flex:none}
.gestes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm}
.geste{background:#fff;border:2px solid #e6e9f0;border-radius:6mm;padding:4mm;text-align:center;font-size:13.5pt}
.geste b{display:block;font-size:15pt;margin-top:2mm}
.picto{height:22mm;display:block;margin:0 auto}.picto.large{height:16mm;margin:3mm auto}
.mot{display:flex;gap:4mm;margin-bottom:3mm}.mot b{min-width:52mm}
/* étapes */
.etape{display:grid;grid-template-columns:18mm 1fr;grid-template-rows:auto auto;gap:3mm 5mm;background:#fff;border:2px solid #e6e9f0;border-radius:8mm;padding:6mm;margin-bottom:6mm;box-shadow:0 2mm 0 #FFE59A}
.etape .num{grid-row:1/3;width:18mm;height:18mm;border-radius:50%;background:#FFC72C;font-size:26pt;font-weight:800;display:flex;align-items:center;justify-content:center}
.etape .txt p{font-size:14.5pt;color:#2d3a5e}
.etape .zoom{grid-column:2;position:relative}
.etape .zoom img{width:100%;max-height:62mm;object-fit:contain;object-position:left;border-radius:5mm;border:3px solid #14234B}
.etape .loupe{position:absolute;left:3mm;top:3mm;background:#14234B;color:#FFC72C;font-size:10pt;font-weight:700;border-radius:3mm;padding:.5mm 3mm}
.inline-picto{display:inline-flex;align-items:center;gap:2mm;font-size:12.5pt;background:#F3F5FA;border-radius:4mm;padding:1mm 3mm;margin-top:1mm}
.inline-picto svg{height:9mm}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.duo img{width:100%;border-radius:4mm;border:3px solid #14234B}
.duo small{display:block;text-align:center;font-size:12pt;margin-top:1mm}
/* notes */
.minotes{margin-top:2mm;font-size:13pt}
.minotes .ligne{border-bottom:2px dotted #b7bfd0;height:10mm}
.pagenotes .ligne{border-bottom:2px solid #d9cfb5;height:11mm}
/* jeu */
.check{display:flex;align-items:center;gap:4mm;font-size:16pt;margin:2mm 0}
.check .case{width:11mm;height:11mm;border:3px solid #14234B;border-radius:2.5mm;flex:none;background:#fff}
.quiz ol{padding-left:7mm;margin:0}.quiz li{margin-bottom:2.5mm;font-size:14.5pt}
.quiz .choix{display:flex;gap:3mm;margin-top:1.5mm;flex-wrap:wrap}
.quiz .choix span{border:2px solid #14234B;border-radius:6mm;padding:.8mm 3mm;font-size:12.5pt;background:#fff;white-space:nowrap}
.reponses{transform:rotate(180deg);text-align:center;font-size:12pt;color:#4a5572;margin-top:4mm}
/* mémo */
.memo{border:3px dashed #14234B;border-radius:8mm;padding:6mm 8mm;background:#FFF8E7;position:relative}
.memo .ciseaux{position:absolute;top:-5.5mm;left:10mm;background:#fff;padding:0 2mm;font-size:13pt}
.memo ol{margin:2mm 0 0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:3mm}
.memo li{background:#fff;border-radius:5mm;padding:3mm 4mm;font-size:17pt;font-weight:700;border:2px solid #FFC72C}
.memo li i{font-style:normal;display:inline-block;width:9mm;height:9mm;border-radius:50%;background:#FFC72C;text-align:center;margin-right:2mm}
.bravo{display:flex;align-items:center;gap:6mm;background:#E3F6F3;border:3px solid #2BB3A3;border-radius:8mm;padding:5mm 7mm;margin:6mm 0}
.medaille{width:24mm;height:24mm;border-radius:50%;background:#FFC72C;border:4px solid #E0A419;display:flex;align-items:center;justify-content:center;font-size:24pt;font-weight:800;flex:none}
.qrs{display:flex;gap:8mm;align-items:flex-end}
.qr{text-align:center;font-weight:700}
.qr img{display:block;margin:0 auto 2mm;border:3px solid #14234B;border-radius:4mm;padding:2mm;background:#fff}
'''

P = []
# 1. couverture
P.append(f'''<section class="page cover">{LOGO_TAG}<span class="badge">Aide-mémoire n° 01</span>
<h1>Je crée mon<br>premier dossier</h1>
<div class="sous">Pour ranger mes documents sur l'ordinateur, comme dans une chemise en carton.</div>
{DOSSIER}
<div class="infos"><div>10 minutes</div><div>Niveau débutant</div><div>Ordinateur Windows</div></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous ne pouvez rien casser : on avance ensemble, une étape à la fois.</div>
{pied(1)}</section>''')

# 2. avant de commencer
P.append(f'''<section class="page creme"><h2><span class="pastille">1</span> Avant de commencer</h2>
<div class="carte analogie">{DOSSIER}<div><h3>Un dossier, à quoi ça sert ?</h3>
<p>Chez vous, vous rangez vos papiers dans des <b>chemises en carton</b> : une pour la santé, une pour les factures…</p>
<p>Sur l'ordinateur, c'est pareil : un <b>dossier</b> sert à <b>ranger vos documents</b> et à les retrouver facilement.</p></div></div>
<h3>Les 3 gestes à connaître</h3>
<div class="gestes"><div class="geste">{SOURIS_G}<b>Clic gauche</b>J'appuie une fois sur le bouton gauche de la souris.</div>
<div class="geste">{SOURIS_D}<b>Clic droit</b>J'appuie une fois sur le bouton droit de la souris.</div>
<div class="geste">{TOUCHE}<b>Touche Entrée</b>La grande touche à droite des lettres du clavier.</div></div>
<div class="carte jaune" style="margin-top:6mm"><h3>📖 Les mots du jour</h3>
<div class="mot"><b>Explorateur de fichiers</b><span>Le « meuble à tiroirs » de l'ordinateur, où sont rangés tous vos dossiers.</span></div>
<div class="mot"><b>Documents</b><span>Un tiroir déjà prêt, fait pour ranger vos papiers.</span></div>
<div class="mot"><b>Dossier</b><span>Une chemise que vous créez et à laquelle vous donnez un nom.</span></div></div>
{pied(2)}</section>''')

# 3-5. étapes
G = lambda s, t: f'<span class="inline-picto">{s}{t}</span>'
P.append(f'''<section class="page"><h2><span class="pastille">2</span> Pas à pas</h2>
{etape(1, "Ouvrez l'Explorateur de fichiers", "En bas de l'écran, cliquez <b>une fois</b> sur l'icône du <b>dossier jaune</b>. Une fenêtre s'ouvre.", "e1", G(SOURIS_G, "clic gauche"))}
{etape(2, "Cliquez sur « Documents »", "Dans la colonne de gauche de la fenêtre. C'est là que nous allons ranger notre dossier.", "e2", G(SOURIS_G, "clic gauche"))}
{pied(3)}</section>''')
P.append(f'''<section class="page"><h2><span class="pastille">2</span> Pas à pas <span style="font-size:15pt;font-weight:600">(suite)</span></h2>
{etape(3, "Cliquez sur « Nouveau »", "En haut à gauche de la fenêtre, le bouton avec un <b>+</b>. Un petit menu s'ouvre.", "e3", G(SOURIS_G, "clic gauche"))}
{etape(4, "Cliquez sur « Dossier »", "Dans le petit menu. Un nouveau dossier apparaît aussitôt.", "e4", G(SOURIS_G, "clic gauche"))}
{pied(4)}</section>''')
P.append(f'''<section class="page"><h2><span class="pastille">2</span> Pas à pas <span style="font-size:15pt;font-weight:600">(fin)</span></h2>
<div class="etape"><div class="num">5</div><div class="txt"><h3>Tapez le nom du dossier</h3>
<p>Le nom « Nouveau dossier » est <b>surligné en bleu</b>. <b>Ne cliquez nulle part</b> : tapez directement le nom au clavier, par exemple <b>Famille</b>.</p></div>
<div class="zoom duo"><div><img src="{img('e5')}"><small>Avant : surligné en bleu</small></div><div><img src="{img('e5b')}"><small>Après : j'ai tapé « Famille »</small></div></div></div>
{etape(6, "Appuyez sur la touche Entrée", "Votre dossier est créé, avec son nom. <b>Bravo !</b>", "e6")}
{notes(2)}
{pied(5)}</section>''')

# 6. bonus + pas de panique
P.append(f'''<section class="page creme"><h2><span class="pastille">★</span> Bonus : avec le clic droit</h2>
<p>Une autre façon d'arriver au même résultat. Utilisez celle que vous préférez !</p>
<div class="carte"><p><b>1.</b> Faites un <b>clic droit</b> dans un espace vide de la fenêtre. {G(SOURIS_D, "clic droit")}</p>
<p><b>2.</b> Posez la souris sur <b>« Nouveau »</b>, puis cliquez sur <b>« Dossier »</b>.</p>
<div class="duo"><div><img src="{img('m1')}"><small>Je pose la souris sur « Nouveau »</small></div><div><img src="{img('m2')}"><small>Je clique sur « Dossier »</small></div></div>
<p style="margin-top:3mm"><b>3.</b> Tapez le nom, puis appuyez sur <b>Entrée</b>.</p></div>
<h2 style="margin-top:6mm"><span class="pastille" style="background:#FF7A59;color:#fff">!</span> Pas de panique</h2>
<div class="carte corail"><p><b>La fenêtre a disparu ?</b> Cliquez de nouveau sur le dossier jaune en bas de l'écran.</p>
<p><b>Le petit menu s'est fermé ?</b> Cliquez de nouveau sur « Nouveau ».</p>
<p><b>J'ai cliqué ailleurs avant de taper le nom ?</b> Votre dossier s'appelle « Nouveau dossier ». Ce n'est pas grave : il est bien créé. Vous apprendrez à le renommer dans le prochain aide-mémoire.</p>
<p style="margin:0"><b>Le nom ne passe pas ?</b> Évitez le point, le tiret, la barre oblique et les deux-points dans le nom.</p></div>
{pied(6)}</section>''')

# 7. à vous de jouer
P.append(f'''<section class="page"><h2><span class="pastille" style="background:#2BB3A3;color:#fff">♪</span> À vous de jouer !</h2>
<div class="carte jaune"><h3>Exercice : créez le dossier « Recettes »</h3><p>Cochez chaque case quand c'est fait.</p>
<div class="check"><span class="case"></span>J'ouvre l'Explorateur de fichiers</div>
<div class="check"><span class="case"></span>Je clique sur « Documents »</div>
<div class="check"><span class="case"></span>Je clique sur « Nouveau », puis sur « Dossier »</div>
<div class="check"><span class="case"></span>Je tape <b>&nbsp;Recettes&nbsp;</b> et j'appuie sur Entrée</div>
<div class="duo" style="grid-template-columns:1fr;margin-top:3mm"><div><img src="{img('ex')}" style="max-height:38mm;object-fit:contain;object-position:left"><small>Voici ce que vous devez voir à la fin</small></div></div></div>
<div class="carte quiz"><h3>Petit quiz : entourez la bonne réponse</h3><ol>
<li>Un dossier sert à…<div class="choix"><span>A. ranger mes documents</span><span>B. allumer l’écran</span><span>C. aller sur Internet</span></div></li>
<li>Pour créer un dossier, je clique d'abord sur…<div class="choix"><span>A. la Corbeille</span><span>B. « Nouveau »</span><span>C. Internet</span></div></li>
<li>Après avoir tapé le nom, j'appuie sur…<div class="choix"><span>A. la touche Espace</span><span>B. la souris</span><span>C. la touche Entrée</span></div></li></ol>
<div class="reponses">Réponses : 1 → A · 2 → B · 3 → C</div></div>
{pied(7)}</section>''')

# 8. mes notes
P.append(f'''<section class="page creme pagenotes"><h2><span class="pastille">✎</span> Mes notes</h2>
<p>Écrivez ici ce qui vous aide : vos questions, vos astuces, les noms de vos dossiers…</p>
{''.join('<div class="ligne"></div>' for _ in range(19))}
{pied(8)}</section>''')

# 9. je retiens
P.append(f'''<section class="page"><h2><span class="pastille">✓</span> Je retiens</h2>
<div class="memo"><span class="ciseaux">✂ à découper et à garder près de l'ordinateur</span>
<h3 style="margin-top:2mm">Créer un dossier en 4 gestes</h3>
<ol><li><i>1</i>« Nouveau »</li><li><i>2</i>« Dossier »</li><li><i>3</i>Je tape le nom</li><li><i>4</i>Entrée</li></ol></div>
<div class="bravo"><div class="medaille">01</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez maintenant <b>créer un dossier</b> pour ranger vos documents. Prochaine étape : le renommer, le déplacer, le copier.</p></div></div>
<h3>Revoir et s'entraîner</h3>
<p style="font-size:13.5pt">Visez un QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<div class="qrs"><div class="qr"><img src="{qr(URL_SUJET)}" style="width:60mm">Revoir cette vidéo</div>
<div class="qr" style="font-size:12pt"><img src="{qr(URL_TOUS)}" style="width:32mm">Tous les aide-mémoire</div>
<div style="flex:1;font-size:12.5pt;background:#F3F5FA;border-radius:5mm;padding:4mm">
<b>S'entraîner sur ordinateur</b><br>Tapez cette adresse dans votre navigateur :<br><b style="word-break:break-all">{URL_PAGE.replace("https://", "")}</b></div></div>
{pied(9)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>01 - Créer un dossier personnel</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
open(out.replace(".pdf", ".html"), "w").write(HTML)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto("file://" + out.replace(".pdf", ".html")); await pg.wait_for_timeout(500)
        await pg.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
print("ok")
