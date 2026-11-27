"""Fiche aide-mémoire 12 « Je découvre Internet et les navigateurs » (4 pages, modèle fiche_v3).
Usage : python3 fiche_04.py out.pdf url_sujet url_tous img_dir   (pas de page interactive pour ce sujet)"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "12"
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
<h1>Je découvre Internet et les navigateurs</h1><div class="s">Ce qu'est Internet, et comment ouvrir un site.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('reseau')}"><div><h3>Comme des routes</h3>
<p>Un <b>réseau</b>, ce sont des ordinateurs <b>reliés entre eux</b>, comme des maisons reliées par des routes.</p>
<p style="margin:0"><b>Internet</b> relie des réseaux du <b>monde entier</b> : ordinateurs, téléphones, tablettes.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>les lettres au clavier</div><div class="ge">{ENTREE}<b>Entrée</b>pour valider</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « navigateur »</h3>
<p style="margin:0">Le <b>navigateur</b> est le programme qui permet d'aller sur Internet et d'afficher les <b>sites</b>. C'est votre <b>voiture</b> pour rouler sur les routes d'Internet. Les plus connus : <b>Microsoft Edge</b> (déjà installé sur les ordinateurs Windows), <b>Google Chrome</b>, <b>Mozilla Firefox</b>, <b>Safari</b> (appareils Apple). Ils font tous la même chose.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Ouvrir un site ne change rien à votre ordinateur : vous ne pouvez rien casser.</div>
{titre("J'ouvre un site", "1")}
{etape(1, "Ouvrez le navigateur", "En bas de l'écran, dans la <b>barre des tâches</b> : cliquez <b>une fois</b> sur l'icône du navigateur. Une fenêtre s'ouvre.", "ouvrir", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(2, "Cliquez dans la barre d'adresse", "C'est la <b>longue case</b>, tout en haut de la fenêtre. Un petit trait clignote : vous pouvez écrire.", "barre", SG, "clic gauche")}
{etape(3, "Tapez l'adresse du site", "Par exemple : <b>google.fr</b> (google, un point, puis f et r). Sans espace.", "taper", CLAV, "clavier")}
{etape(4, "Appuyez sur la touche Entrée", "La page du site s'affiche. <b>Bravo !</b>", "page", ENTREE, "touche Entrée")}
{etape(5, "Pour fermer : cliquez sur la croix", "Tout <b>en haut à droite</b> de la fenêtre. Elle devient rouge quand la souris passe dessus.", "fermer", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>La page ne s'affiche pas ?</b> Vérifiez l'adresse, lettre par lettre, et le point. Effacez avec la touche marquée d'une <b>flèche vers la gauche</b>, juste au-dessus de Entrée, corrigez, puis Entrée.</p>
<p><b>Je ne trouve pas l'icône ?</b> Cliquez sur <b>Démarrer</b> et tapez le nom du navigateur, par exemple <b>Edge</b>. Ou demandez à Espace 19.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Un peu d'histoire", "★")}
<div class="box vc" style="margin-bottom:3.5mm"><div class="deux" style="align-items:center">
<div><p><b>1969 :</b> aux États-Unis, naissance du premier réseau, appelé <b>Arpanet</b>.</p>
<p style="margin:0"><b>1989 :</b> au <b>CERN</b>, près de Genève, Tim Berners-Lee invente le <b>Web</b> : les pages que l'on consulte avec un navigateur.</p></div>
<div class="navs"><img src="{img('navs')}"></div></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : j'ouvre un site</h3>
<div class="check"><i></i>J'ouvre le navigateur</div>
<div class="check"><i></i>Je clique dans la barre d'adresse</div>
<div class="check"><i></i>Je tape google.fr</div>
<div class="check"><i></i>J'appuie sur Entrée</div>
<div class="check"><i></i>Je ferme avec la croix</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Internet, c'est…<div class="ch"><span>A. un grand réseau</span><span>B. un ordinateur</span></div></li>
<li>Pour aller sur Internet, j'utilise…<div class="ch"><span>A. la Corbeille</span><span>B. un navigateur</span></div></li>
<li>L'adresse du site se tape…<div class="ch"><span>A. tout en haut</span><span>B. tout en bas</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>J'ouvre un site Internet</h3>
<div class="row"><div><i>1</i>Icône du<br>navigateur</div><div><i>2</i>Barre<br>d'adresse</div><div><i>3</i>Je tape<br>l'adresse</div><div><i>4</i>Entrée</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez ce qu'est <b>Internet</b> et vous savez <b>ouvrir un site</b>. Prochain aide-mémoire : faire une recherche.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, les adresses de vos sites préférés…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je découvre Internet et les navigateurs</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
