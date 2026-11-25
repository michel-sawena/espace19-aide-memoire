"""Fiche aide-mémoire v3 : 4 pages max, sans couverture, logo Espace 19.
Usage : python3 fiche_v3.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB = 4
b64 = lambda path: "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
img = lambda n: b64(f"{IMG}/{n}.png")
LOGO = b64(f"{IMG}/logo.png")

def qr(u):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#3a0a33", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

SG = '<svg viewBox="0 0 60 90" class="pic"><rect x="5" y="5" width="50" height="80" rx="25" fill="#fff" stroke="#3a0a33" stroke-width="5"/><path d="M5 35 H55 M30 5 V35" stroke="#3a0a33" stroke-width="5"/><path d="M9 33 V30 A21 21 0 0 1 27 8 V33 Z" fill="#FFC72C"/></svg>'
SD = '<svg viewBox="0 0 60 90" class="pic"><rect x="5" y="5" width="50" height="80" rx="25" fill="#fff" stroke="#3a0a33" stroke-width="5"/><path d="M5 35 H55 M30 5 V35" stroke="#3a0a33" stroke-width="5"/><path d="M51 33 V30 A21 21 0 0 0 33 8 V33 Z" fill="#93117E"/></svg>'
KEY = '<svg viewBox="0 0 120 70" class="pic key"><rect x="4" y="9" width="112" height="58" rx="10" fill="#6b5a68"/><rect x="4" y="4" width="112" height="56" rx="10" fill="#fff" stroke="#3a0a33" stroke-width="4"/><text x="60" y="40" font-size="22" font-weight="700" text-anchor="middle" fill="#3a0a33" font-family="Inter">Entrée ↵</text></svg>'
FOLDER = '<svg viewBox="0 0 220 170" class="folder"><rect x="20" y="30" width="80" height="30" rx="8" fill="#E8A92C"/><rect x="50" y="10" width="110" height="120" rx="6" fill="#fff" stroke="#c9cfdb" stroke-width="3" transform="rotate(-8 105 70)"/><rect x="70" y="18" width="110" height="120" rx="6" fill="#fff" stroke="#c9cfdb" stroke-width="3" transform="rotate(6 125 78)"/><rect x="20" y="50" width="185" height="115" rx="12" fill="#FFC72C" stroke="#E0A419" stroke-width="4"/></svg>'

def pied(n):
    return f'<div class="pied"><img src="{LOGO}"><span>Espace 19 Numérique · Formation débutant · Aide-mémoire n° 08</span><span class="pn">{n} / {NB}</span></div>'

def titre(t, ico):
    return f'<h2><span class="ico">{ico}</span>{t}</h2>'

def etape(n, action, detail, image, geste=SG, nom="clic gauche"):
    return f'''<div class="et"><div class="n">{n}</div><div class="t"><h3>{action}</h3><p>{detail}</p>
    <span class="g">{geste}{nom}</span></div><div class="z"><img src="{img(image)}"></div></div>'''

CSS = '''
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Regular.otf);font-weight:400}
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf);font-weight:600}
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Bold.otf);font-weight:700}
@font-face{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-ExtraBold.otf);font-weight:800}
@page{size:A4;margin:0}
*{box-sizing:border-box}
:root{--v:#93117E;--vf:#3a0a33;--vc:#F8EAF5;--j:#FFC72C;--jc:#FFF6D6;--vert:#2BB3A3;--vertc:#E3F6F3;--cor:#FF7A59;--corc:#FFEDE7}
body{margin:0;font-family:Inter,sans-serif;color:var(--vf);font-size:11.5pt;line-height:1.38}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;padding:13mm 14mm 20mm}
h2{font-size:15pt;margin:0 0 3.5mm;font-weight:800;color:var(--v);display:flex;align-items:center;gap:2.5mm}
h2 .ico{width:8mm;height:8mm;border-radius:50%;background:var(--v);color:#fff;font-size:11pt;display:flex;align-items:center;justify-content:center}
h3{font-size:12.5pt;margin:0 0 1mm;font-weight:700}
p{margin:0 0 1.8mm}
b{font-weight:700}
.pied{position:absolute;left:14mm;right:14mm;bottom:8mm;display:flex;align-items:center;gap:4mm;font-size:8.5pt;color:#6b5a68;border-top:1.5px solid var(--v);padding-top:2mm}
.pied img{height:8mm}.pied .pn{margin-left:auto;font-weight:800;color:var(--v);font-size:10pt}
/* en-tête page 1 */
.entete{display:flex;align-items:center;gap:6mm;margin-bottom:5mm}
.entete img{height:22mm}
.bandeau{flex:1;background:var(--v);color:#fff;border-radius:5mm;padding:4.5mm 6mm;position:relative}
.bandeau .k{display:inline-block;background:var(--j);color:var(--vf);font-weight:800;font-size:9pt;border-radius:3mm;padding:.6mm 2.5mm;margin-bottom:1.5mm}
.bandeau h1{margin:0;font-size:23pt;line-height:1.1;font-weight:800}
.bandeau .s{font-size:10.5pt;opacity:.95;margin-top:1mm}
.intro{display:grid;grid-template-columns:1.25fr 1fr;gap:4mm;margin-bottom:4.5mm}
.box{border-radius:4mm;padding:3.5mm 4.5mm;border:1.5px solid #ead7e6;background:#fff}
.box.vc{background:var(--vc);border-color:#e2c2db}.box.jc{background:var(--jc);border-color:#f2d675}
.box.vert{background:var(--vertc);border-color:var(--vert)}.box.cor{background:var(--corc);border-color:var(--cor)}
.analog{display:flex;gap:3.5mm;align-items:center}.folder{width:26mm;flex:none}
.gestes{display:flex;gap:2mm}
.ge{flex:1;text-align:center;font-size:9pt;line-height:1.25}.ge b{display:block;font-size:10pt;margin-top:.8mm}
.pic{height:12mm;display:block;margin:0 auto}.pic.key{height:9mm;margin:1.5mm auto 1.5mm}
.rassure{font-size:10.5pt;background:var(--jc);border-left:5px solid var(--j);border-radius:2mm;padding:2mm 4mm;margin-bottom:4.5mm}
/* étapes */
.et{display:grid;grid-template-columns:11mm 1fr 78mm;gap:4mm;align-items:center;border:1.5px solid #ead7e6;border-radius:4.5mm;padding:3.5mm 4mm;margin-bottom:3.5mm;background:#fff}
.et .n{width:11mm;height:11mm;border-radius:50%;background:var(--j);font-size:15pt;font-weight:800;display:flex;align-items:center;justify-content:center;align-self:start}
.et p{font-size:10.5pt;color:#4b3a47}
.g{display:inline-flex;align-items:center;gap:1.5mm;font-size:9pt;background:var(--vc);border-radius:3mm;padding:.5mm 2.5mm}
.g .pic{height:6mm;margin:0}.g .pic.key{height:5mm}
.z img{width:100%;max-height:44mm;object-fit:contain;border-radius:3mm;border:2px solid var(--vf);display:block}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:2.5mm}
.duo img{width:100%;border-radius:2.5mm;border:2px solid var(--vf);display:block}
.duo small{display:block;text-align:center;font-size:8.5pt;margin-top:.8mm;color:#6b5a68}
.deux{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.check{display:flex;align-items:center;gap:2.5mm;font-size:11pt;margin:1.6mm 0}
.check i{width:6mm;height:6mm;border:2px solid var(--vf);border-radius:1.5mm;flex:none;background:#fff}
.quiz ol{padding-left:5mm;margin:0}.quiz li{margin-bottom:1.8mm;font-size:10.5pt}
.ch{display:flex;gap:1.5mm;flex-wrap:wrap;margin-top:.8mm}.ch span{border:1.5px solid var(--vf);border-radius:3mm;padding:.2mm 2mm;font-size:9.5pt;background:#fff}
.rep{transform:rotate(180deg);text-align:center;font-size:8.5pt;color:#6b5a68;margin-top:1mm}
.lignes .l{border-bottom:1.5px solid #dccfd8;height:8.5mm}
.memo{border:2.5px dashed var(--v);border-radius:5mm;padding:4mm 5mm 4.5mm;background:var(--vc);position:relative}
.memo .cis{position:absolute;top:-3.5mm;left:6mm;background:#fff;padding:0 2mm;font-size:9pt;color:var(--v)}
.memo .row{display:grid;grid-template-columns:repeat(4,1fr);gap:2.5mm;margin-top:2mm}
.memo .row div{background:#fff;border:1.5px solid var(--j);border-radius:3mm;padding:2mm;font-weight:700;font-size:11.5pt;text-align:center}
.memo .row i{font-style:normal;display:block;width:7mm;height:7mm;line-height:7mm;margin:0 auto 1mm;border-radius:50%;background:var(--j)}
.bravo{display:flex;align-items:center;gap:4mm}
.med{width:15mm;height:15mm;border-radius:50%;background:var(--j);border:3px solid #E0A419;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13pt;flex:none}
.qrs{display:flex;gap:6mm;align-items:flex-end}
.qr{text-align:center;font-weight:700;font-size:10pt}
.qr img{display:block;margin:0 auto 1.5mm;border:2px solid var(--vf);border-radius:2.5mm;padding:1.5mm;background:#fff}
'''

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° 08 · DÉBUTANT · 10 MIN</span>
<h1>Je crée mon premier dossier</h1><div class="s">Pour ranger mes documents sur l'ordinateur Windows.</div></div></div>
<div class="intro"><div class="box vc analog">{FOLDER}<div><h3>Un dossier, à quoi ça sert ?</h3>
<p>Chez vous, vous rangez vos papiers dans des <b>chemises en carton</b>. Sur l'ordinateur, un <b>dossier</b> sert pareil : <b>ranger vos documents</b> et les retrouver facilement.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{SD}<b>Clic droit</b>bouton droit, une fois</div><div class="ge">{KEY}<b>Entrée</b>grande touche à droite</div></div></div></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous ne pouvez rien casser. Suivez les étapes une par une.</div>
{titre("Pas à pas", "1")}
{etape(1, "Ouvrez l'Explorateur de fichiers", "En bas de l'écran, cliquez <b>une fois</b> sur l'icône du <b>dossier jaune</b>. Une fenêtre s'ouvre.", "e1")}
{etape(2, "Cliquez sur « Documents »", "Dans la colonne de gauche de la fenêtre. C'est le tiroir prévu pour vos papiers.", "e2")}
{etape(3, "Cliquez sur « Nouveau »", "En haut à gauche de la fenêtre, le bouton avec un <b>+</b>. Un petit menu s'ouvre.", "e3")}
{pied(1)}</section>''')

P.append(f'''<section class="page">{titre("Pas à pas (suite)", "1")}
{etape(4, "Cliquez sur « Dossier »", "Dans le petit menu. Un nouveau dossier apparaît aussitôt.", "e4")}
<div class="et"><div class="n">5</div><div class="t"><h3>Tapez le nom du dossier</h3><p>Le nom « Nouveau dossier » est <b>surligné en bleu</b>. <b>Ne cliquez nulle part</b> : tapez directement, par exemple <b>Famille</b>.</p><span class="g">⌨ au clavier</span></div>
<div class="duo"><div><img src="{img('e5')}"><small>Avant</small></div><div><img src="{img('e5b')}"><small>Après</small></div></div></div>
{etape(6, "Appuyez sur la touche Entrée", "Votre dossier est créé avec son nom. <b>Bravo !</b>", "e6", KEY, "")}
{titre("Bonus : avec le clic droit", "★")}
<div class="box vc" style="margin-bottom:4mm"><div class="deux" style="align-items:center"><div>
<p><b>1.</b> Faites un <b>clic droit</b> dans un espace vide de la fenêtre.</p>
<p><b>2.</b> Posez la souris sur <b>« Nouveau »</b>, puis cliquez sur <b>« Dossier »</b>.</p>
<p style="margin:0"><b>3.</b> Tapez le nom, puis appuyez sur <b>Entrée</b>.</p></div>
<div class="duo"><div><img src="{img('m1')}"><small>« Nouveau »</small></div><div><img src="{img('m2')}"><small>« Dossier »</small></div></div></div></div>
{titre("Pas de panique", "!")}
<div class="box cor" style="margin-bottom:4mm"><div class="deux">
<p><b>La fenêtre a disparu ?</b> Cliquez de nouveau sur le dossier jaune en bas de l'écran.</p>
<p><b>Le petit menu s'est fermé ?</b> Cliquez de nouveau sur « Nouveau ».</p>
<p><b>J'ai cliqué ailleurs avant de taper ?</b> Le dossier s'appelle « Nouveau dossier ». Il est bien créé : vous apprendrez à le renommer au prochain cours.</p>
<p><b>Le nom ne passe pas ?</b> Évitez le point, le tiret, la barre oblique et les deux-points.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : créez le dossier « Recettes »</h3>
<div class="check"><i></i>J'ouvre l'Explorateur de fichiers</div>
<div class="check"><i></i>Je clique sur « Documents »</div>
<div class="check"><i></i>Je clique sur « Nouveau », puis « Dossier »</div>
<div class="check"><i></i>Je tape Recettes, puis Entrée</div>
<img src="{img('ex')}" style="width:100%;margin-top:2mm;border-radius:2.5mm;border:2px solid #3a0a33"></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Un dossier sert à…<div class="ch"><span>A. ranger mes documents</span><span>B. allumer l'écran</span></div></li>
<li>Pour créer un dossier, je clique d'abord sur…<div class="ch"><span>A. la Corbeille</span><span>B. « Nouveau »</span></div></li>
<li>Après le nom, j'appuie sur…<div class="ch"><span>A. Espace</span><span>B. Entrée</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → B</div></div></div>
{titre("Je retiens", "✓")}
<div class="memo" style="margin-top:2mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Créer un dossier en 4 gestes</h3>
<div class="row"><div><i>1</i>« Nouveau »</div><div><i>2</i>« Dossier »</div><div><i>3</i>Je tape le nom</div><div><i>4</i>Entrée</div></div></div>
<div class="box vert bravo" style="margin-top:4mm"><div class="med">08</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>créer un dossier</b>. Prochain aide-mémoire : le renommer, le déplacer, le copier.</p></div></div>
<div class="box" style="margin-top:4mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:32mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, vos astuces, les noms de vos dossiers…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>08 - Je crée mon premier dossier</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
open(out.replace(".pdf", ".html"), "w").write(HTML)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto("file://" + out.replace(".pdf", ".html")); await pg.wait_for_timeout(400)
        # contrôle : aucun contenu ne déborde de sa page
        over = await pg.evaluate("""() => [...document.querySelectorAll('.page')].map((s,i)=>{const r=s.getBoundingClientRect();const pied=s.querySelector('.pied').getBoundingClientRect().top;let m=0;s.querySelectorAll('*').forEach(e=>{if(e.closest('.pied'))return;const b=e.getBoundingClientRect();if(b.bottom>m)m=b.bottom});return {page:i+1,deborde:Math.round(m-pied)}})""")
        print(over)
        await pg.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
