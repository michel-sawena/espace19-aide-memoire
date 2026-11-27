"""Fiche aide-mémoire 24 « J'entre dans mon espace sur impots.gouv.fr » (4 pages, modèle fiche_v3).
Usage : python3 fiche_24.py out.pdf url_sujet url_tous img_dir   (pas de page interactive pour ce sujet)"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "24"
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
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉMARCHES EN LIGNE · 15 MIN</span>
<h1>J'entre dans mon espace sur impots.gouv.fr</h1><div class="s">Se connecter, lire ses avis d'impôt, poser une question.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('avis')}"><div><h3>Ma boîte aux lettres des impôts</h3>
<p>Votre <b>espace Finances publiques</b> est votre <b>boîte aux lettres personnelle</b> aux impôts : vos <b>avis d'impôt</b>, vos déclarations, vos questions.</p>
<p style="margin:0">À préparer : votre <b>dernier avis d'impôt</b> et votre <b>mot de passe</b>.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>chiffres et lettres</div><div class="ge">{ENTREE}<b>Entrée</b>pour valider</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « numéro fiscal »</h3>
<p style="margin:0">C'est votre <b>numéro personnel aux impôts</b> : <b>13 chiffres</b>. Il est écrit <b>en haut de votre avis d'impôt</b>. Il est demandé <b>à chaque connexion</b>.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Regarder son espace ne change rien à vos impôts : vous ne pouvez rien casser.</div>
{titre("J'entre dans mon espace", "1")}
{etape(1, "Tapez l'adresse : impots.gouv.fr", "Ouvrez le navigateur, cliquez dans la <b>barre d'adresse</b>, tapez <b>impots.gouv.fr</b> puis <b>Entrée</b>. Vérifiez que l'adresse finit par <b>.gouv.fr</b> : c'est la marque des sites officiels.", "adresse", CLAV, "clavier")}
{etape(2, "Cliquez sur le bouton de connexion", "<b>En haut à droite</b> de la page : le bouton de connexion à votre <b>espace Finances publiques</b>.", "connexion", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(3, "Tapez votre numéro fiscal", "Cliquez dans la case, tapez les <b>13 chiffres</b> de votre avis d'impôt, puis cliquez sur le bouton pour <b>continuer</b>.", "numero", CLAV, "clavier")}
{etape(4, "Tapez votre mot de passe, puis validez", "Des <b>petits points</b> s'affichent à la place des lettres : c'est normal. <b>Parfois</b>, un <b>code de 6 chiffres</b> arrive par mail : recopiez-le.", "mdp", CLAV, "clavier")}
{etape(5, "Consultez vos avis d'impôt", "Dans votre espace, cliquez sur la rubrique des <b>avis d'impôt</b>, puis sur l'année voulue. Pour une question : la <b>messagerie sécurisée</b>.", "espace", SG, "clic gauche")}
{etape(6, "Déconnectez-vous", "Quand vous avez fini : <b>déconnectez-vous</b>, en haut à droite, puis fermez le navigateur avec la <b>croix</b>.", "quitter", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>Mot de passe oublié ?</b> Sur la page de connexion, après le numéro fiscal, un lien permet de le <b>renouveler</b>. Autre solution : le bouton <b>FranceConnect</b> (avec votre compte ameli, par exemple).</p>
<p><b>Pas de numéro fiscal ?</b> Il est sur votre <b>avis d'impôt</b>. Sinon, contactez votre service des impôts, ou demandez à <b>Espace 19</b>.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Attention aux faux messages", "!")}
<div class="box cor" style="margin-bottom:3.5mm;display:flex;gap:5mm;align-items:center"><img src="{img('sms')}" style="width:30mm;border-radius:3mm">
<div><p>Les impôts ne demandent <b>jamais</b> vos <b>coordonnées bancaires</b> par mail, par SMS ou par téléphone.</p>
<p style="margin:0">Un message vous promet un remboursement ? <b>Ne cliquez pas.</b> Tapez vous-même <b>impots.gouv.fr</b> et regardez dans votre espace. (L'image est un <b>EXEMPLE</b> inventé.)</p></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : j'entre dans mon espace</h3>
<div class="check"><i></i>Je prends mon avis d'impôt</div>
<div class="check"><i></i>Je tape impots.gouv.fr</div>
<div class="check"><i></i>Je clique sur la connexion</div>
<div class="check"><i></i>Numéro fiscal, puis mot de passe</div>
<div class="check"><i></i>Je me déconnecte</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Mon numéro fiscal est écrit…<div class="ch"><span>A. sur mon avis d'impôt</span><span>B. sur ma carte Vitale</span></div></li>
<li>L'adresse officielle finit par…<div class="ch"><span>A. .gouv.fr</span><span>B. .com</span></div></li>
<li>Un SMS demande ma carte bancaire pour les impôts…<div class="ch"><span>A. je réponds</span><span>B. je ne clique pas</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → A · 3 → B</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>J'entre dans mon espace impots.gouv.fr</h3>
<div class="row"><div><i>1</i>impots<br>.gouv.fr</div><div><i>2</i>Bouton de<br>connexion</div><div><i>3</i>Numéro<br>fiscal</div><div><i>4</i>Mot de<br>passe</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez entrer dans votre <b>espace Finances publiques</b> et lire vos <b>avis d'impôt</b>.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions… Ne notez jamais votre mot de passe sur une feuille laissée près de l'ordinateur.</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - J’entre dans mon espace sur impots.gouv.fr</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
