"""Fiche aide-mémoire 16 « Je crée mon adresse Gmail » (4 pages, modèle fiche_v3).
Écrans dessinés simplifiés et neutres (sans logo ni charte de Google). Libellés cités : voir sources_16.md.
Usage : python3 fiche_16.py out.pdf url_sujet url_tous img_dir   (pas de page interactive pour ce sujet)"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "16"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)     # pictogramme clic gauche du modèle
CSS += '''
.et{grid-template-columns:11mm 1fr 62mm;padding:3mm 4mm;margin-bottom:3mm}
.z img{max-height:36mm}
.et.w{grid-template-columns:11mm 1fr 92mm}
.duo img{max-height:34mm;object-fit:contain;background:#fff}
.p2 .z img{max-height:28.5mm}
.p2 .et{grid-template-columns:11mm 1fr 50mm;margin-bottom:2.2mm;padding:2mm 4mm}
.p2 .et h3{margin-bottom:.5mm}
.p2 .et p{margin:0}
.arob{font-size:30pt;font-weight:800;color:var(--v);line-height:1}
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
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>Je crée mon adresse Gmail</h1><div class="s">Une adresse mail gratuite, pour envoyer et recevoir des messages.</div></div></div>
<div class="intro"><div class="box vc analog"><div class="arob" style="width:20mm;text-align:center">@</div><div><h3>Comme une adresse postale</h3>
<p>Une <b>adresse mail</b>, c'est votre adresse… pour Internet. On vous écrit, les messages arrivent dans votre <b>boîte mail</b>.</p>
<p style="margin:0">Exemple : <b>marie.dupont@gmail.com</b>. Au milieu, le petit signe <b>@</b> se dit « <b>arobase</b> ».</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>les lettres au clavier</div><div class="ge">{ENTREE}<b>Entrée</b>pour valider</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Avant de commencer, préparez :</h3>
<p style="margin:0">un <b>carnet</b> et un stylo (pour noter votre adresse et votre mot de passe), et votre <b>téléphone portable</b> (Google peut le demander pour votre sécurité). C'est <b>gratuit</b>.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Si vous vous trompez, vous pouvez revenir en arrière ou recommencer : vous ne pouvez rien casser.</div>
{titre("Je crée mon adresse", "1")}
{etape(1, "Allez sur gmail.com", "Ouvrez le navigateur. Cliquez dans la <b>barre d'adresse</b>, tapez <b>gmail.com</b>, puis appuyez sur <b>Entrée</b>.", "adresse", CLAV, "clavier")}
{etape(2, "Cliquez sur « Créer un compte »", "Un petit menu s'ouvre.", "creer", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(3, "Cliquez sur « Pour mon usage personnel »", "C'est le premier choix du petit menu.", "usage", SG, "clic gauche")}
{etape(4, "Tapez votre prénom et votre nom", "Puis cliquez sur <b>« Suivant »</b>.", "nom", CLAV, "clavier")}
{etape(5, "Date de naissance et genre", "Indiquez-les, puis cliquez sur <b>« Suivant »</b>.", "naissance", CLAV, "clavier")}
{etape(6, "Choisissez votre adresse", "Prenez une adresse proposée, ou écrivez la vôtre : <b>sans espace ni accent</b>. Déjà prise ? Ajoutez un chiffre. Puis <b>« Suivant »</b>.", "choix", SG, "clic gauche")}
{etape(7, "Inventez un mot de passe", "Tapez-le <b>deux fois</b>. Notez-le dans votre carnet, rangé chez vous. Ne le donnez à <b>personne</b>. Puis <b>« Suivant »</b>.", "motdepasse", CLAV, "clavier")}
{etape(8, "Votre numéro de téléphone", "Il sert à <b>retrouver votre compte</b> si vous oubliez le mot de passe. C'est utile.", "telephone", CLAV, "clavier")}
{etape(9, "Cliquez sur « J'accepte »", "Après avoir lu les règles. Votre <b>boîte mail</b> s'ouvre. <b>Bravo !</b>", "accepte", SG, "clic gauche")}
<div class="rassure" style="font-size:9.5pt;margin-top:1mm">Les images sont des <b>dessins simplifiés</b> : l'écran réel peut être un peu différent, et l'ordre des questions peut changer. Lisez chaque page, répondez, puis « Suivant ».</div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Pas de panique", "!")}
<div class="box cor" style="margin-bottom:3.5mm"><div class="deux">
<p><b>« Adresse déjà prise » ?</b> Quelqu'un l'a déjà. Ajoutez un chiffre (par exemple votre année de naissance) ou changez l'ordre : nom.prénom.</p>
<p><b>Mot de passe oublié ?</b> Pas de panique : votre <b>numéro de téléphone</b> permet de le retrouver. Venez à Espace 19, nous vous aiderons.</p></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : je prépare mon adresse</h3>
<div class="check"><i></i>J'écris l'adresse que j'aimerais :</div>
<p style="border-bottom:2px dotted #3a0a33;height:7mm;margin:0 0 2mm"><span style="float:right;font-weight:700">@gmail.com</span></p>
<div class="check"><i></i>Pas d'espace, pas d'accent</div>
<div class="check"><i></i>Je crée mon compte sur gmail.com</div>
<div class="check"><i></i>Je note adresse et mot de passe dans mon carnet</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Le signe @ se dit…<div class="ch"><span>A. arobase</span><span>B. étoile</span></div></li>
<li>Pour passer à la page suivante, je clique sur…<div class="ch"><span>A. « Suivant »</span><span>B. la croix</span></div></li>
<li>Mon mot de passe, je le donne…<div class="ch"><span>A. à personne</span><span>B. à qui le demande</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → A · 3 → A</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Je crée mon adresse Gmail</h3>
<div class="row"><div><i>1</i>gmail.com</div><div><i>2</i>Créer un<br>compte</div><div><i>3</i>Suivant…</div><div><i>4</i>J'accepte</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous avez votre <b>adresse mail</b>. Prochain aide-mémoire : se connecter et se déconnecter de sa messagerie.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici votre adresse mail, et vos questions. Votre mot de passe : plutôt dans un carnet rangé chez vous.</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je crée mon adresse Gmail</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
