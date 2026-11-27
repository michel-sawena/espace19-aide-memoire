"""Fiche aide-mémoire 06 « Je déplace, j'agrandis, j'ouvre le menu, je fais défiler » (4 pages, modèle fiche_v3).
Usage : python3 fiche_06.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "06"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)     # pictogramme clic gauche du modèle
CSS += '''
.et{grid-template-columns:11mm 1fr 58mm;padding:3mm 4mm;margin-bottom:3mm}
.z img{max-height:34mm}
.p2 .z img{max-height:40mm}
.p2 .et{grid-template-columns:11mm 1fr 62mm;margin-bottom:2.6mm}
.p2 .box.cor p{margin-bottom:1mm;font-size:10.3pt}
.analog img{width:40mm;flex:none;border-radius:3mm}
'''
b64 = lambda path: "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
img = lambda n: b64(f"{IMG}/{n}.png")
LOGO = b64(f"{IMG}/logo.png")

def qr(u):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#3a0a33", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

# pictogrammes
BASE = '<svg viewBox="0 0 60 90" class="pic"><rect x="5" y="5" width="50" height="80" rx="25" fill="#fff" stroke="#3a0a33" stroke-width="5"/><path d="M5 35 H55 M30 5 V35" stroke="#3a0a33" stroke-width="5"/>{}</svg>'
SD = BASE.format('<path d="M51 33 V30 A21 21 0 0 0 33 8 V33 Z" fill="#FF7A59"/>')
MOL = BASE.format('<rect x="24" y="11" width="12" height="20" rx="6" fill="#FFC72C" stroke="#3a0a33" stroke-width="3"/>')
MAINT = BASE.format('<path d="M9 33 V30 A21 21 0 0 1 27 8 V33 Z" fill="#FFC72C"/><path d="M18 60 h24 M34 52 l8 8 -8 8" fill="none" stroke="#93117E" stroke-width="5" stroke-linecap="round"/>')

def pied(n):
    return f'<div class="pied"><img src="{LOGO}"><span>Espace 19 Numérique · Formation débutant · Aide-mémoire n° {NUM}</span><span class="pn">{n} / {NB}</span></div>'

def titre(t, ico):
    return f'<h2><span class="ico">{ico}</span>{t}</h2>'

def etape(n, action, detail, image, geste="", nom=""):
    g = f'<span class="g">{geste}{nom}</span>' if (geste or nom) else ""
    return f'<div class="et"><div class="n">{n}</div><div class="t"><h3>{action}</h3><p>{detail}</p>{g}</div><div class="z"><img src="{img(image)}"></div></div>'

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>Je déplace, j'agrandis, je fais défiler</h1><div class="s">La souris : glisser-déposer, taille des fenêtres, clic droit et molette.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('table')}"><div><h3>Comme une feuille sur la table</h3>
<p style="margin:0">Pour déplacer une feuille, on la <b>prend</b>, on la <b>porte</b>, puis on la <b>pose</b> ailleurs. Avec la souris, c'est pareil : c'est le <b>glisser-déposer</b>.</p></div></div>
<div class="box"><h3>Les 4 gestes utiles</h3><div class="gestes">
<div class="ge">{MAINT}<b>Gauche enfoncé</b>je déplace</div><div class="ge">{SG}<b>Clic gauche</b>sur le carré : j'agrandis</div><div class="ge">{SD}<b>Clic droit</b>un petit menu</div><div class="ge">{MOL}<b>Molette</b>je fais défiler</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « menu contextuel »</h3>
<p style="margin:0">C'est le <b>petit menu</b> qui s'ouvre avec un <b>clic droit</b>. « Contextuel » veut dire : il propose des actions <b>pour l'endroit où vous avez cliqué</b>. Il change donc selon l'endroit.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Si vous lâchez le bouton trop tôt, rien de grave : recommencez. Vous ne pouvez rien casser.</div>
{titre("Je déplace", "1")}
{etape(1, "Déplacez une icône", "Placez la flèche sur l'icône. <b>Appuyez</b> sur le bouton gauche et <b>gardez-le enfoncé</b>. Déplacez la souris, puis <b>relâchez</b>.", "glisser", MAINT, "gauche enfoncé")}
{etape(2, "Déplacez une fenêtre", "Attrapez la fenêtre par sa <b>barre du haut</b> (là où est écrit son nom). Gardez le bouton gauche enfoncé, faites glisser, relâchez.", "barre", MAINT, "gauche enfoncé")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{titre("J'agrandis", "2")}
{etape(3, "Cliquez sur le carré", "En haut à droite : <b>un trait, un carré, une croix</b>. Le <b>carré</b> agrandit la fenêtre : elle remplit tout l'écran. Un nouveau clic : elle reprend sa taille.", "carre", SG, "clic gauche")}
{etape(4, "Ou tirez sur un coin", "Placez la flèche sur un <b>coin</b> de la fenêtre : elle devient une <b>double flèche</b>. Gardez le bouton gauche enfoncé et tirez.", "coin", MAINT, "gauche enfoncé")}
{titre("J'ouvre le menu et je fais défiler", "3")}
{etape(5, "Faites un clic droit", "Le <b>bouton droit</b> ouvre un petit menu d'actions. Pour le fermer sans rien choisir : cliquez <b>à côté</b>, avec le bouton gauche.", "menu", SD, "clic droit")}
{etape(6, "Tournez la molette", "La <b>petite roue</b> entre les deux boutons. <b>Vers vous</b> : la page descend. <b>Vers l'écran</b> : la page remonte.", "molette", MOL, "molette")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>L'icône n'a pas bougé ?</b> Le bouton a été relâché trop tôt. Gardez-le bien enfoncé pendant tout le trajet.</p>
<p><b>La fenêtre a disparu ?</b> Vous avez sans doute cliqué sur le <b>trait</b> : elle est rangée en bas, dans la barre des tâches. Cliquez sur son icône pour la retrouver.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : les 4 gestes</h3>
<div class="check"><i></i>Je déplace une icône du bureau</div>
<div class="check"><i></i>J'agrandis une fenêtre (le carré)</div>
<div class="check"><i></i>Je lui rends sa taille (le carré)</div>
<div class="check"><i></i>J'ouvre le menu du clic droit, puis je clique à côté</div>
<div class="check"><i></i>Je fais défiler une page avec la molette</div>
<div class="duo" style="margin-top:2mm"><div><img src="{img('resultat')}"><small>Fenêtre agrandie : elle remplit l'écran</small></div></div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour déplacer une icône, je garde enfoncé…<div class="ch"><span>A. le bouton gauche</span><span>B. la molette</span></div></li>
<li>Le carré, en haut à droite…<div class="ch"><span>A. ferme la fenêtre</span><span>B. l'agrandit</span></div></li>
<li>Le clic droit ouvre…<div class="ch"><span>A. un petit menu</span><span>B. Internet</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Les 4 gestes de la souris</h3>
<div class="row"><div><i>1</i>Gauche enfoncé :<br>je déplace</div><div><i>2</i>Le carré :<br>j'agrandis</div><div><i>3</i>Clic droit :<br>un menu</div><div><i>4</i>La molette :<br>je fais défiler</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>déplacer</b>, <b>agrandir</b>, ouvrir le <b>menu du clic droit</b> et <b>faire défiler</b>. Prochain aide-mémoire : découvrir le clavier.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, ce que vous avez réussi, ce que vous voulez revoir…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - La souris : déplacer, agrandir, clic droit, molette</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
