"""Fiche aide-mémoire 15 « Je télécharge un fichier ou une image » (4 pages, modèle fiche_v3).
Usage : python3 fiche_15.py out.pdf url_sujet url_tous img_dir url_page"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG, URL_PAGE = sys.argv[1:6]
NB, NUM = 4, "15"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)     # pictogramme clic gauche du modèle
SD = re.search(r"SD = '(.*?)'\n", SRC).group(1)     # pictogramme clic droit du modèle
CSS += '''
.et{grid-template-columns:11mm 1fr 62mm;padding:3mm 4mm;margin-bottom:3mm}
.z img{max-height:36mm}
.et.w{grid-template-columns:11mm 1fr 92mm}
.duo img{max-height:34mm;object-fit:contain;background:#fff}
.p2 .z img{max-height:44mm}
.p2 .et{grid-template-columns:11mm 1fr 78mm}
.p2 .box.cor p{margin-bottom:1mm;font-size:10.3pt}
.analog img{width:34mm;flex:none;border-radius:3mm}
.navs img{width:100%;border-radius:3mm}
.chemin{display:flex;gap:2mm;align-items:center;flex-wrap:wrap;font-weight:700;font-size:11pt}
.chemin span{background:#fff;border:2px solid #3a0a33;border-radius:2.5mm;padding:1mm 2.5mm}
.chemin i{font-style:normal;color:var(--v);font-size:14pt}
'''
b64 = lambda path: "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
img = lambda n: b64(f"{IMG}/{n}.png")
LOGO = b64(f"{IMG}/logo.png")

def qr(u):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#3a0a33", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

# pictogrammes
ENTREE = '<svg viewBox="0 0 120 70" class="pic key"><rect x="4" y="10" width="112" height="50" rx="8" fill="#fff" stroke="#3a0a33" stroke-width="4"/><text x="60" y="44" font-size="22" font-weight="800" text-anchor="middle" fill="#3a0a33" font-family="Inter">Entrée ↵</text></svg>'
CLAV = '<svg viewBox="0 0 120 70" class="pic key"><rect x="4" y="14" width="112" height="42" rx="7" fill="#fff" stroke="#3a0a33" stroke-width="4"/><g fill="#93117E"><rect x="14" y="22" width="12" height="10" rx="2"/><rect x="32" y="22" width="12" height="10" rx="2"/><rect x="50" y="22" width="12" height="10" rx="2"/><rect x="68" y="22" width="12" height="10" rx="2"/><rect x="86" y="22" width="12" height="10" rx="2"/><rect x="28" y="38" width="64" height="10" rx="2"/></g></svg>'
DBL = SG.replace('class="pic"', 'class="pic"').replace('</svg>', '<text x="30" y="70" font-size="26" font-weight="800" text-anchor="middle" fill="#93117E" font-family="Inter">×2</text></svg>')
CHEMIN = '<svg viewBox="0 0 120 70" class="pic key"><rect x="4" y="14" width="112" height="42" rx="7" fill="#fff" stroke="#3a0a33" stroke-width="4"/><path d="M22 35 h14 M30 28 l8 7 -8 7 M58 35 h14 M66 28 l8 7 -8 7" fill="none" stroke="#93117E" stroke-width="5" stroke-linecap="round"/><rect x="86" y="27" width="20" height="16" rx="3" fill="#FFC72C"/></svg>'

def pied(n):
    return f'<div class="pied"><img src="{LOGO}"><span>Espace 19 Numérique · Formation débutant · Aide-mémoire n° {NUM}</span><span class="pn">{n} / {NB}</span></div>'

def titre(t, ico):
    return f'<h2><span class="ico">{ico}</span>{t}</h2>'

def etape(n, action, detail, image, geste="", nom=""):
    g = f'<span class="g">{geste}{nom}</span>' if (geste or nom) else ""
    if isinstance(image, str):
        zone = f'<div class="z"><img src="{img(image)}"></div>'; cls = "et"
    else:
        zone = f'<div class="duo">{"".join(f"<div><img src={chr(34)}{img(i)}{chr(34)}><small>{c}</small></div>" for i, c in image)}</div>'; cls = "et w"
    return f'<div class="{cls}"><div class="n">{n}</div><div class="t"><h3>{action}</h3><p>{detail}</p>{g}</div>{zone}</div>'

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 10 MIN</span>
<h1>Je télécharge un fichier ou une image</h1><div class="s">Garder sur mon ordinateur un document ou une image trouvés sur Internet.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('illustration')}"><div><h3>Comme une photocopie</h3>
<p><b>Télécharger</b>, c'est <b>copier sur votre ordinateur</b> un document trouvé sur Internet.</p>
<p style="margin:0">Comme une photocopie prise à la bibliothèque, que vous <b>gardez chez vous</b>.</p></div></div>
<div class="box"><h3>Les 2 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>pour un document : sur le lien</div><div class="ge">{SD}<b>Clic droit</b>pour une image : un menu s'ouvre</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « Téléchargements »</h3>
<p style="margin:0">C'est le <b>dossier</b> de votre ordinateur où arrive <b>tout ce que vous téléchargez</b>. On le trouve dans l'<b>Explorateur de fichiers</b> (le dossier jaune de la barre des tâches), dans la liste de gauche.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Télécharger ne change rien au site : vous gardez seulement une copie pour vous.</div>
{titre("Je télécharge un document", "1")}
{etape(1, "Cliquez sur le lien de téléchargement", "Sur le site, cherchez le lien ou le bouton pour télécharger. Cliquez <b>une fois</b> dessus.", "lien", SG, "clic gauche")}
{etape(2, "Le fichier apparaît en haut à droite", "Une petite fenêtre s'ouvre <b>en haut à droite</b>, avec le nom du fichier. Cliquez sur son nom pour l'ouvrir.", "panneau", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{titre("J'enregistre une image", "2")}
{etape(3, "Faites un clic droit sur l'image", "Posez la souris sur l'image, puis appuyez <b>une fois</b> sur le bouton <b>droit</b>. Un menu s'ouvre.", "clicdroit", SD, "clic droit")}
{etape(4, "Cliquez sur « Enregistrer l'image sous »", "Dans le menu, cliquez sur <b>Enregistrer l'image sous</b>.", "menu", SG, "clic gauche")}
{etape(5, "Cliquez sur « Enregistrer »", "Une fenêtre s'ouvre. Vérifiez que le dossier est <b>Téléchargements</b>, puis cliquez sur <b>Enregistrer</b>.", "dialogue", SG, "clic gauche")}
{titre("Je retrouve mes téléchargements", "3")}
{etape(6, "Explorateur de fichiers, puis « Téléchargements »", "Cliquez sur le <b>dossier jaune</b> de la barre des tâches. À gauche, cliquez sur <b>Téléchargements</b> : tout est là.", "explorateur", SG, "clic gauche")}
{pied(2)}</section>''')

P.append(f'''<section class="page"><div class="box cor" style="margin-bottom:3mm"><h3 style="margin-bottom:1mm">Pas de panique</h3><div class="deux">
<p style="margin:0"><b>Un doute sur un site ou un fichier ?</b> Téléchargez seulement sur des sites que vous connaissez. En cas de doute, cliquez sur <b>Annuler</b>.</p>
<p style="margin:0"><b>Pas de menu au clic droit ?</b> Vérifiez que la souris est bien <b>sur l'image</b>. Les images servent pour vous : ne les republiez pas.</p></div></div>
<div class="deux"><div class="box jc"><h3>Exercice : j'enregistre une image</h3>
<div class="check"><i></i>Clic droit sur une image</div>
<div class="check"><i></i>Enregistrer l'image sous</div>
<div class="check"><i></i>Enregistrer</div>
<div class="check"><i></i>Je la retrouve dans Téléchargements</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Télécharger, c'est…<div class="ch"><span>A. copier chez moi</span><span>B. effacer</span></div></li>
<li>Pour une image, je fais…<div class="ch"><span>A. un double clic</span><span>B. un clic droit</span></div></li>
<li>Mes fichiers arrivent dans…<div class="ch"><span>A. Téléchargements</span><span>B. la Corbeille</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:3mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Je garde une image</h3>
<div class="row"><div><i>1</i>Clic droit<br>sur l'image</div><div><i>2</i>Enregistrer<br>l'image sous</div><div><i>3</i>Enregistrer</div><div><i>4</i>Dossier<br>Téléchargements</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>télécharger un document</b> et <b>garder une image</b>. Prochain aide-mémoire : créer une adresse Gmail.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:28mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, les sites où vous téléchargez, le nom de vos fichiers…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je télécharge un fichier ou une image</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
open(out.replace(".pdf", ".html"), "w").write(HTML)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto("file://" + out.replace(".pdf", ".html")); await pg.wait_for_timeout(400)
        over = await pg.evaluate("""() => [...document.querySelectorAll('.page')].map((s,i)=>{const pied=s.querySelector('.pied').getBoundingClientRect().top;let m=0;s.querySelectorAll('*').forEach(e=>{if(e.closest('.pied'))return;if(e.closest('.box.vc')&&e.closest('.box.vc').style.position==='absolute')return;const b=e.getBoundingClientRect();if(b.bottom>m)m=b.bottom});return {page:i+1,deborde:Math.round(m-pied)}})""")
        print(over)
        await pg.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
