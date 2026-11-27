"""Fiche aide-mémoire 04 « Je comprends l'arborescence » (4 pages, modèle fiche_v3).
Usage : python3 fiche_04.py out.pdf url_sujet url_tous img_dir   (pas de page interactive pour ce sujet)"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "04"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)     # pictogramme clic gauche du modèle
CSS += '''
.et{grid-template-columns:11mm 1fr 62mm;padding:3mm 4mm;margin-bottom:3mm}
.z img{max-height:36mm}
.et.w{grid-template-columns:11mm 1fr 92mm}
.duo img{max-height:34mm;object-fit:contain;background:#fff}
.p2 .z img{max-height:44mm}
.p2 .et{grid-template-columns:11mm 1fr 78mm}
.p2 .box.cor p{margin-bottom:1mm;font-size:10.3pt}
.analog img{width:34mm;flex:none;border-radius:3mm}
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
<h1>Je comprends l'arborescence</h1><div class="s">Où sont rangés mes documents, et comment les retrouver.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('armoire')}"><div><h3>Comme une armoire</h3>
<p>Une <b>armoire</b>, des <b>tiroirs</b>, des <b>chemises</b> en carton, et des <b>feuilles</b> dedans.</p>
<p style="margin:0">Dans l'ordinateur : les tiroirs et les chemises sont des <b>dossiers</b>, les feuilles sont des <b>fichiers</b>.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{DBL}<b>Double-clic</b>deux clics rapides : j'ouvre</div><div class="ge">{CHEMIN}<b>Lire le chemin</b>en haut de la fenêtre</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « arborescence »</h3>
<p style="margin:0">Le rangement ressemble à un <b>arbre</b> : un tronc (l'ordinateur), des branches (les <b>dossiers</b>), des feuilles (les <b>fichiers</b>). D'où son nom : l'<b>arborescence</b>.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Regarder dans les dossiers ne change rien : vous ne pouvez rien casser.</div>
{titre("Je regarde le rangement", "1")}
{etape(1, "Ouvrez l'Explorateur de fichiers", "Dans la barre des tâches, en bas : cliquez sur le <b>dossier jaune</b>. Une fenêtre s'ouvre : c'est l'<b>Explorateur de fichiers</b>.", "ouvrir", SG, "clic gauche")}
{etape(2, "À gauche : les grands tiroirs", "La colonne de gauche montre les grands rangements : <b>Bureau</b>, <b>Téléchargements</b>, <b>Documents</b>, <b>Images</b>, <b>Musique</b>, <b>Vidéos</b>.", "tiroirs")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(3, "Cliquez sur « Documents »", "À droite, son contenu s'affiche : des <b>dossiers jaunes</b> (vos chemises).", "documents", SG, "clic gauche")}
{etape(4, "Double-cliquez sur un dossier", "Par exemple « Lettres » : <b>deux clics rapides</b> avec le bouton gauche. Le dossier s'ouvre : voici les <b>fichiers</b>, vos feuilles.", "lettres", DBL, "double-clic")}
{etape(5, "Lisez le chemin, en haut", "La <b>barre d'adresse</b> montre le <b>chemin</b> : « Documents › Lettres ». C'est l'adresse de votre rangement : on lit de gauche à droite, du plus grand au plus petit.", "chemin", CHEMIN, "le chemin")}
{etape(6, "Remontez : cliquez sur « Documents »", "Dans la barre d'adresse, cliquez sur <b>Documents</b> : vous remontez d'un étage, au tiroir Documents.", "remonter", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>Le dossier ne s'ouvre pas ?</b> Les deux clics étaient trop lents. Recommencez, plus vite, sans bouger la souris.</p>
<p><b>Je suis perdu ?</b> Regardez le <b>chemin</b> en haut : il dit où vous êtes. Cliquez sur <b>Documents</b> à gauche pour repartir du début.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Bon à savoir", "★")}
<div class="box vc" style="margin-bottom:3.5mm"><div class="deux" style="align-items:center">
<div><p><b>La petite flèche qui monte</b>, à gauche de la barre d'adresse, fait remonter d'un étage, comme un clic sur le nom.</p>
<p style="margin:0"><b>Raccourci :</b> la touche <b>Windows</b> + la lettre <b>E</b> ouvre aussi l'Explorateur de fichiers.</p></div>
<div class="duo"><div><img src="{img('fleche')}"><small>La flèche qui monte</small></div></div></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : je me promène</h3>
<div class="check"><i></i>J'ouvre l'Explorateur de fichiers</div>
<div class="check"><i></i>Je clique sur « Documents »</div>
<div class="check"><i></i>J'ouvre un dossier (double-clic)</div>
<div class="check"><i></i>Je lis le chemin en haut</div>
<div class="check"><i></i>Je remonte : clic sur « Documents »</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Une feuille, dans l'ordinateur, c'est…<div class="ch"><span>A. un fichier</span><span>B. un dossier</span></div></li>
<li>Pour ouvrir un dossier, je fais…<div class="ch"><span>A. un double-clic</span><span>B. un clic droit</span></div></li>
<li>Le chemin, en haut, me dit…<div class="ch"><span>A. l'heure</span><span>B. où je suis</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → A · 3 → B</div></div></div>
<div class="memo" style="margin-top:5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Le rangement de l'ordinateur</h3>
<div class="row"><div><i>1</i>Dossier jaune<br>en bas</div><div><i>2</i>Documents</div><div><i>3</i>Double-clic<br>sur un dossier</div><div><i>4</i>Le chemin<br>pour remonter</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>où sont rangés vos documents</b> et comment vous y promener. Prochain aide-mémoire : la souris, le curseur et les clics.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, le nom de vos dossiers importants, leur chemin…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je comprends l\'arborescence</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
