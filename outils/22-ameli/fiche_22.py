"""Fiche aide-mémoire 22 « Je me connecte à mon compte ameli » (4 pages, modèle fiche_v3).
Écrans simplifiés et neutres (ni logo ni charte du site officiel) ; numéros = exemples inventés.
Usage : python3 fiche_22.py out.pdf url_sujet url_tous img_dir   (pas de page interactive pour ce sujet)"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "22"
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
.analog img{width:38mm;flex:none;border-radius:3mm}
.sms img{width:30mm;flex:none;border-radius:3mm}
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
<h1>Je me connecte à mon compte ameli</h1><div class="s">Le site de l'Assurance Maladie, chez vous.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('carte')}"><div><h3>À quoi ça sert ?</h3>
<p>Le <b>compte ameli</b>, c'est comme un <b>guichet de l'Assurance Maladie ouvert chez vous</b>, jour et nuit.</p>
<p style="margin:0">Vous y suivez vos <b>remboursements</b> et vous obtenez vos <b>papiers</b>, sans vous déplacer.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>les chiffres et lettres</div><div class="ge">{ENTREE}<b>Entrée</b>pour valider</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Préparez avant de commencer</h3>
<p style="margin:0">Votre <b>carte Vitale</b> : votre <b>numéro de sécurité sociale</b> y est écrit. Vous taperez les <b>13 premiers chiffres</b>, sans les 2 derniers (la « clé »). Et votre <b>mot de passe</b> ameli. Le <b>mot de passe</b>, c'est la clé de votre compte : <b>il reste secret</b>, ne le donnez à personne.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous ne pouvez rien casser. Si vous vous trompez, vous recommencez.</div>
{titre("Je me connecte", "1")}
{etape(1, "Tapez ameli.fr dans la barre d'adresse", "Ouvrez le navigateur. Cliquez dans la <b>barre d'adresse</b>, tout en haut. Tapez <b>ameli.fr</b>, puis appuyez sur <b>Entrée</b>. Tapez toujours l'adresse <b>vous-même</b>.", "adresse", CLAV, "clavier")}
{etape(2, "Allez sur votre compte ameli", "Sur le site, cliquez sur l'accès au <b>compte ameli</b>. La page de connexion s'affiche.", "site", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(3, "Tapez votre numéro, puis votre mot de passe", "1<sup>re</sup> case : les <b>13 premiers chiffres</b> de votre numéro de sécurité sociale. 2<sup>e</sup> case : votre <b>mot de passe</b> (il s'affiche en petits points).", "login", CLAV, "clavier")}
{etape(4, "Cliquez sur « Me connecter »", "", "connecter", SG, "clic gauche")}
{etape(5, "Recopiez le code de sécurité", "Un <b>code à 6 chiffres</b> peut être demandé. Il arrive dans votre <b>boîte mail</b>. Recopiez-le. Il est valable <b>15 minutes</b>.", "code", CLAV, "clavier")}
{etape(6, "Cliquez sur « Attestation de droits »", "<b>Bravo, vous êtes dans votre compte !</b> Pour votre mutuelle, par exemple : cliquez sur <b>Attestation de droits</b>. Vous pouvez l'enregistrer ou l'imprimer.", "compte", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>Mot de passe oublié ?</b> Cliquez sur <b>« Mot de passe oublié ? »</b>. Il faut votre numéro, votre date de naissance et votre adresse mail.</p>
<p><b>Pas de code dans vos mails ?</b> Regardez dans les <b>courriers indésirables</b>. Code trop vieux : cliquez sur <b>« Recevoir un nouveau code de sécurité »</b>.</p>
<p><b>Bloqué après 3 erreurs ?</b> Attendez <b>15 minutes</b>, puis recommencez.</p>
<p><b>Pas encore de compte ?</b> Avec votre <b>carte Vitale</b> et votre <b>RIB</b> : cliquez sur <b>« Créer un compte »</b>. Ou appelez le <b>36 46</b> (service gratuit + prix de l'appel), ou venez à Espace 19.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Attention aux faux messages", "⚠")}
<div class="box cor sms" style="display:flex;gap:5mm;align-items:center;margin-bottom:3.5mm"><img src="{img('faux_sms')}"><div>
<p>L'Assurance Maladie ne vous demande <b>jamais</b> votre <b>mot de passe</b>, ni votre <b>numéro de carte bancaire</b>, par mail, par SMS ou par téléphone.</p>
<p style="margin:0">Un message vous presse de cliquer ? <b>Ne cliquez pas sur le lien.</b> Tapez <b>ameli.fr</b> vous-même, ou demandez à Espace 19.</p></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : je me connecte</h3>
<div class="check"><i></i>Je tape ameli.fr, puis Entrée</div>
<div class="check"><i></i>Je vais sur le compte ameli</div>
<div class="check"><i></i>Je tape mon numéro (13 chiffres)</div>
<div class="check"><i></i>Je tape mon mot de passe</div>
<div class="check"><i></i>Je clique sur « Me connecter »</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour aller sur ameli, je…<div class="ch"><span>A. tape ameli.fr</span><span>B. clique sur un lien reçu</span></div></li>
<li>Mon numéro est écrit sur…<div class="ch"><span>A. ma carte bancaire</span><span>B. ma carte Vitale</span></div></li>
<li>Un SMS me demande mon mot de passe :<div class="ch"><span>A. je ne réponds pas</span><span>B. je le donne</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Je me connecte à ameli</h3>
<div class="row"><div><i>1</i>ameli.fr<br>+ Entrée</div><div><i>2</i>Compte<br>ameli</div><div><i>3</i>Numéro<br>+ mot de passe</div><div><i>4</i>Me<br>connecter</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez vous connecter à votre <b>compte ameli</b> et trouver votre <b>attestation de droits</b>.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions. <b>N'écrivez pas votre mot de passe sur cette feuille.</b></p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je me connecte à mon compte ameli</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
