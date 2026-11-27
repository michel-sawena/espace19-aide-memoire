"""Fiche aide-mémoire 09 « Je range mes dossiers » (4 pages, modèle fiche_v3).
Usage : python3 fiche_09.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "09"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)
SD = re.search(r"SD = '(.*?)'\n", SRC).group(1)
KEY = re.search(r"KEY = '(.*?)'\n", SRC).group(1)
CSS += '''
.et{grid-template-columns:11mm 1fr 66mm;padding:2.6mm 4mm;margin-bottom:2.6mm}
.z img{max-height:33mm}
.et.w{grid-template-columns:11mm 1fr 92mm}
.duo img{max-height:32mm;object-fit:contain;background:#fff}
.icn{display:flex;gap:2mm;align-items:center;flex-wrap:wrap}
.icn img{height:11mm}
.icn span{font-size:9.6pt}
.box.cor p{margin-bottom:1mm;font-size:10.3pt}
'''
b64 = lambda path: "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
img = lambda n: b64(f"{IMG}/{n}.png")
LOGO = b64(f"{IMG}/logo.png")

def qr(u):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#3a0a33", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

DBL = SG.replace('</svg>', '<text x="30" y="70" font-size="26" font-weight="800" text-anchor="middle" fill="#93117E" font-family="Inter">×2</text></svg>')

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
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>Je renomme, copie, déplace et jette un dossier</h1><div class="s">Quatre gestes pour garder un ordinateur bien rangé.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Un dossier est une <b>chemise en carton</b>. On peut changer son <b>étiquette</b> (renommer), en faire une <b>photocopie</b> (copier), la changer de <b>tiroir</b> (déplacer) ou la mettre à la <b>poubelle</b> (supprimer).</p></div>
<div class="box"><h3>Les gestes utiles</h3><div class="gestes">
<div class="ge">{SD}<b>Clic droit</b>bouton droit, une fois : un menu s'ouvre</div><div class="ge">{SG}<b>Clic gauche</b>je choisis dans le menu</div><div class="ge">{KEY}<b>Entrée</b>je valide le nom</div></div></div></div>
<div class="box jc" style="margin-bottom:3mm"><h3>Le mot du jour : « le menu du clic droit »</h3>
<p>Clic droit sur un dossier : un menu s'ouvre. <b>En haut, de petites images.</b> Posez la souris sur une image : <b>son nom apparaît</b>.</p>
<div class="icn"><img src="{img('icones')}"><span>De gauche à droite : <b>Couper</b>, <b>Copier</b>, <b>Coller</b>, <b>Renommer</b>, <b>Partager</b>, <b>Supprimer</b>.</span></div></div>
<div class="rassure"><b>Prenez votre temps.</b> Un dossier jeté par erreur se récupère dans la Corbeille (page 3).</div>
{titre("Je change le nom", "1")}
{etape(1, "Clic droit, puis « Renommer »", "Dans l'Explorateur de fichiers, faites un <b>clic droit</b> sur le dossier, puis cliquez sur l'image <b>Renommer</b>.", "renommer", SD, "clic droit")}
{etape(2, "Tapez le nouveau nom, puis Entrée", "Le nom est <b>surligné en bleu</b>. Ne cliquez nulle part : tapez le nouveau nom (ex. « Courrier »), puis appuyez sur <b>Entrée</b>.", "taper", KEY, "Entrée")}
{pied(1)}</section>''')

P.append(f'''<section class="page">
{titre("Je fais une copie", "2")}
{etape(3, "Clic droit, puis « Copier »", "Faites un <b>clic droit</b> sur le dossier à copier, puis cliquez sur l'image <b>Copier</b>.", "copier", SD, "clic droit")}
{etape(4, "Clic droit dans le vide, puis « Coller »", "Ouvrez l'endroit voulu (ex. <b>Bureau</b>, à gauche). Faites un <b>clic droit dans un espace vide</b>, puis cliquez sur <b>Coller</b>. Le dossier est maintenant à <b>deux endroits</b>.", "coller", SD, "clic droit")}
{titre("Je change de place", "3")}
{etape(5, "« Couper », puis « Coller »", "C'est presque pareil : clic droit sur le dossier, puis <b>Couper</b> (au lieu de Copier). Ouvrez l'endroit voulu, clic droit dans le vide, puis <b>Coller</b>. Le dossier <b>change de place</b>.", "couper", SD, "clic droit")}
{titre("Je jette", "4")}
{etape(6, "Clic droit, puis « Supprimer »", "Faites un <b>clic droit</b> sur le dossier, puis cliquez sur l'image <b>Supprimer</b>. Le dossier part dans la <b>Corbeille</b>, avec tout ce qu'il contient.", "supprimer", SD, "clic droit")}
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Pas de panique : la Corbeille", "!")}
<div class="box cor" style="margin-bottom:3mm"><div class="deux" style="align-items:center">
<div><p><b>Jeté par erreur ?</b> Sur le bureau, <b>double-cliquez</b> sur la <b>Corbeille</b>. Faites un <b>clic droit</b> sur le dossier, puis cliquez sur <b>Restaurer</b> : il retourne à sa place.</p>
<p style="margin:0"><b>Le menu ne montre pas les images ?</b> Vous avez cliqué à côté. Fermez le menu en cliquant ailleurs, puis refaites le clic droit <b>sur le dossier</b>.</p></div>
<div class="duo"><div><img src="{img('corbeille')}"><small>Double-clic</small></div><div><img src="{img('restaurer')}"><small>Restaurer</small></div></div></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<div class="check"><i></i>Je crée un dossier « Essai » (aide-mémoire n° 08)</div>
<div class="check"><i></i>Je le renomme en « Vacances »</div>
<div class="check"><i></i>Je le supprime</div>
<div class="check"><i></i>Je le restaure depuis la Corbeille</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour ouvrir le menu, je fais…<div class="ch"><span>A. un clic droit</span><span>B. un double-clic</span></div></li>
<li>Pour changer de place, je choisis…<div class="ch"><span>A. Copier</span><span>B. Couper</span></div></li>
<li>Un dossier supprimé va…<div class="ch"><span>A. dans la Corbeille</span><span>B. nulle part</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Je range mes dossiers</h3>
<div class="row"><div><i>1</i>Clic droit<br>sur le dossier</div><div><i>2</i>Renommer<br>puis Entrée</div><div><i>3</i>Copier ou Couper<br>puis Coller</div><div><i>4</i>Supprimer<br>(Corbeille)</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>renommer, copier, déplacer et jeter</b> un dossier. Prochain aide-mémoire : créer et enregistrer un fichier texte.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, le nom de vos dossiers, où vous les avez rangés…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je range mes dossiers</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
