"""Fiche aide-mémoire 23 « J'utilise la CAF en ligne » (4 pages, modèle fiche_v3, même structure que fiche_12).
Usage : python3 fiche_23.py out.pdf url_sujet url_tous img_dir   (pas de page interactive pour ce sujet)
Écrans simplifiés et neutres (aucun logo ni charte du site officiel). Libellés vérifiés : voir sources_23.md."""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "23"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)
CSS += '''
.et{grid-template-columns:11mm 1fr 66mm;padding:2.2mm 4mm;margin-bottom:2.2mm}
.z img{max-height:30mm}
.p2 .z img{max-height:32mm}
.p2 .box.cor p{margin-bottom:1mm;font-size:10.3pt}
.analog img{width:44mm;flex:none;border-radius:3mm;align-self:center}
'''
b64 = lambda path: "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
img = lambda n: b64(f"{IMG}/{n}.png")
LOGO = b64(f"{IMG}/logo.png")

def qr(u):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#3a0a33", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

ENTREE = '<svg viewBox="0 0 120 70" class="pic key"><rect x="4" y="10" width="112" height="50" rx="8" fill="#fff" stroke="#3a0a33" stroke-width="4"/><text x="60" y="44" font-size="22" font-weight="800" text-anchor="middle" fill="#3a0a33" font-family="Inter">Entrée ↵</text></svg>'
CLAV = '<svg viewBox="0 0 120 70" class="pic key"><rect x="4" y="14" width="112" height="42" rx="7" fill="#fff" stroke="#3a0a33" stroke-width="4"/><g fill="#93117E"><rect x="14" y="22" width="12" height="10" rx="2"/><rect x="32" y="22" width="12" height="10" rx="2"/><rect x="50" y="22" width="12" height="10" rx="2"/><rect x="68" y="22" width="12" height="10" rx="2"/><rect x="86" y="22" width="12" height="10" rx="2"/><rect x="28" y="38" width="64" height="10" rx="2"/></g></svg>'

def pied(n):
    return f'<div class="pied"><img src="{LOGO}"><span>Espace 19 Numérique · Formation débutant · Aide-mémoire n° {NUM}</span><span class="pn">{n} / {NB}</span></div>'

def titre(t, ico):
    return f'<h2><span class="ico">{ico}</span>{t}</h2>'

def etape(n, action, detail, image, geste="", nom=""):
    g = f'<span class="g">{geste}{nom}</span>' if (geste or nom) else ""
    return f'<div class="et"><div class="n">{n}</div><div class="t"><h3>{action}</h3><p>{detail}</p>{g}</div><div class="z"><img src="{img(image)}"></div></div>'

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · DÉMARCHES EN LIGNE · 15 MIN</span>
<h1>J'utilise la CAF en ligne</h1><div class="s">Me connecter à « Mon Compte » et télécharger une attestation.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('preparer')}"><div><h3>À quoi ça sert ?</h3>
<p>La CAF verse des aides, comme l'<b>aide au logement</b>. Votre espace <b>« Mon Compte »</b> sur <b>caf.fr</b> est un <b>guichet ouvert jour et nuit</b>, de chez vous.</p>
<p style="margin:0"><b>Préparez :</b> votre <b>carte Vitale</b>, votre <b>mot de passe de la CAF</b> et votre <b>boîte mail</b>.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>les chiffres au clavier</div><div class="ge">{ENTREE}<b>Entrée</b>pour valider</div></div></div></div>
<div class="box jc" style="margin-bottom:3mm"><h3>Le mot du jour : « attestation »</h3>
<p style="margin:0">Une <b>attestation</b> est un <b>papier officiel</b> qui prouve ce que la CAF vous verse. On vous la demande parfois (logement, banque…). Avec « Mon Compte », vous l'obtenez <b>tout de suite</b>, sans vous déplacer.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Regarder son dossier ne change rien à vos aides : vous ne pouvez rien casser.</div>
{titre("Je me connecte", "1")}
{etape(1, "Allez sur caf.fr", "Ouvrez le navigateur. Dans la <b>barre d'adresse</b>, tout en haut, tapez <b>caf.fr</b> puis appuyez sur <b>Entrée</b>.", "adresse", CLAV, "clavier + Entrée")}
{etape(2, "Cliquez sur « Mon Compte »", "En haut de la page d'accueil.", "moncompte", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(3, "Tapez votre numéro, puis votre mot de passe", "1<sup>re</sup> case : les <b>13 premiers chiffres</b> de votre <b>numéro de sécurité sociale</b> (sur la carte Vitale). 2<sup>e</sup> case : votre <b>mot de passe de la CAF</b>.", "cases", CLAV, "clavier")}
{etape(4, "Cliquez sur « Se connecter »", "Puis, si on vous le propose, cliquez sur <b>« Envoyer le code »</b>.", "seconnecter", SG, "clic gauche")}
{etape(5, "Tapez le code reçu par mail", "Ouvrez votre boîte mail : un code à <b>6 chiffres</b> vous attend (valable <b>15 minutes</b>). Tapez-le, puis validez. <b>Ce code est secret</b> : la CAF ne vous le demandera jamais.", "code", CLAV, "clavier")}
{titre("Je télécharge une attestation", "2")}
{etape(6, "Cliquez sur « Mes attestations »", "Dans votre espace « Mon Compte ».", "attestations", SG, "clic gauche")}
{etape(7, "Choisissez le type, puis la période", "Par exemple : <b>attestation de paiement</b>, puis <b>« Mois précédent »</b>.", "choix", SG, "clic gauche")}
{etape(8, "Cliquez sur « Télécharger »", "L'attestation s'ouvre : enregistrez-la ou imprimez-la. Autre choix : <b>« Recevoir par courrier »</b>.", "telecharger", SG, "clic gauche")}
{etape(9, "Quand c'est fini : « Déconnexion »", "Comme <b>fermer la porte à clé</b> en partant.", "deconnexion", SG, "clic gauche")}
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Pas de panique", "!")}
<div class="box cor" style="margin-bottom:2.5mm"><div class="deux">
<p><b>Mot de passe oublié ?</b> Sur la page de connexion, cliquez sur <b>« Mot de passe oublié ? »</b> : un code vous est envoyé par SMS ou par mail, au choix.</p>
<p><b>Pas de code reçu ?</b> Regardez dans les <b>courriers indésirables</b>, ou demandez un nouveau code. Besoin d'aide : la CAF au <b>3230</b> (service gratuit + prix d'un appel), ou Espace 19.</p></div></div>
<div class="box vert" style="margin-bottom:2.5mm"><p style="margin:0"><b>Bonus :</b> le bouton <b>« S'identifier avec FranceConnect »</b> vous connecte avec votre compte <b>ameli.fr</b> ou <b>impots.gouv.fr</b> (aide-mémoire n° 21).</p></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<div class="check"><i></i>caf.fr, puis « Mon Compte »</div>
<div class="check"><i></i>Numéro, mot de passe, code</div>
<div class="check"><i></i>Je télécharge une attestation</div>
<div class="check"><i></i>Je clique sur « Déconnexion »</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour me connecter, je tape…<div class="ch"><span>A. mon numéro de sécurité sociale</span><span>B. mon adresse</span></div></li>
<li>Un conseiller me demande le code reçu par mail…<div class="ch"><span>A. je le donne</span><span>B. je ne le donne jamais</span></div></li>
<li>À la fin, je clique sur…<div class="ch"><span>A. Déconnexion</span><span>B. rien</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:2.5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>La CAF en ligne</h3>
<div class="row"><div><i>1</i>caf.fr<br>Mon Compte</div><div><i>2</i>N° sécu<br>+ mot de passe</div><div><i>3</i>Code<br>par mail</div><div><i>4</i>Déconnexion</div></div></div>
<div class="box vert bravo" style="margin-top:2.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez vous connecter à la CAF et <b>télécharger une attestation</b>.</p></div></div>
<div class="box" style="margin-top:2.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions… Ne notez jamais votre mot de passe sur une feuille que d'autres peuvent voir.</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - J\'utilise la CAF en ligne</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
