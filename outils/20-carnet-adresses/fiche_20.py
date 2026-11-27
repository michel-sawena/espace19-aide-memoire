"""Fiche aide-mémoire 20 « Je tiens mon carnet d'adresses » (4 pages, modèle fiche_v3).
Usage : python3 fiche_20.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "20"
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
<h1>Je tiens mon carnet d'adresses</h1><div class="s">Garder les adresses mail de mes proches, et les retrouver sans effort.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Vous avez sans doute un <b>petit répertoire en papier</b>, avec les noms de vos proches. Le carnet d'adresses, c'est <b>la même chose pour vos mails</b> : il retient les adresses à votre place.</p></div>
<div class="box"><h3>Les gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>je clique sur un bouton</div><div class="ge">{KEY}<b>Clavier</b>je tape le nom et l'adresse</div></div></div></div>
<div class="box jc" style="margin-bottom:3mm"><h3>Le mot du jour : « un contact »</h3>
<p>Un <b>contact</b>, c'est une personne rangée dans votre carnet, avec son nom et son <b>adresse mail</b> (par exemple <b>paul.durand@exemple.fr</b>). Une adresse s'écrit <b>sans espace</b>, avec le signe <b>@</b> (on dit « arobase »).</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous ne pouvez rien casser : une fiche se corrige à tout moment.</div>
{titre("J'ouvre mon carnet", "1")}
{etape(1, "Tapez l'adresse du carnet", "Connectez-vous d'abord à votre messagerie (aide-mémoire n° 17). Dans la <b>barre d'adresse</b> du navigateur, tapez <b>contacts.google.com</b>, puis appuyez sur <b>Entrée</b>. La liste de vos contacts apparaît.", "adresse", KEY, "Entrée")}
{titre("J'ajoute une personne", "2")}
{etape(2, "Cliquez sur « Créer un contact »", "Le bouton est <b>en haut à gauche</b>. Une fiche vide s'ouvre.", "creer", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page">
{etape(3, "Remplissez la fiche", "Tapez le <b>prénom</b>, puis le <b>nom</b> dans les premières cases. Dans la case à côté de l'<b>enveloppe</b>, tapez l'<b>adresse mail</b>. Vérifiez bien chaque lettre.", "remplir", KEY, "clavier")}
{etape(4, "Cliquez sur « Enregistrer »", "Le bouton est <b>en haut à droite</b>. Bravo : la personne est dans votre carnet.", "enregistrer", SG, "clic gauche")}
{titre("Je retrouve et je corrige", "3")}
{etape(5, "Cherchez la personne", "Cliquez dans la <b>barre de recherche</b>, en haut. Tapez les <b>premières lettres</b> du nom, puis cliquez sur la bonne personne : sa fiche s'ouvre.", "chercher", KEY, "clavier")}
{etape(6, "« Modifier », puis « Enregistrer »", "Une adresse a changé ? Dans la fiche, cliquez sur <b>Modifier</b>. Corrigez, puis cliquez sur <b>Enregistrer</b>.", "modifier", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><p><b>La personne n'est pas proposée dans la case « À » ?</b> Vérifiez les premières lettres tapées, ou cherchez la personne dans votre carnet pour lire son adresse.</p>
<p><b>Vous avez fermé la fiche sans enregistrer ?</b> Rien n'est cassé : recommencez avec « Créer un contact ».</p>
<p style="margin:0"><b>Votre mail revient avec un message d'erreur ?</b> L'adresse est sans doute mal écrite : ouvrez la fiche, cliquez sur « Modifier », vérifiez chaque lettre et chaque point.</p></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Écrire à un contact, ou le retirer", "4")}
<div class="box cor" style="margin-bottom:3mm"><div class="deux" style="align-items:center">
<div><p><b>Écrire :</b> ouvrez un nouveau mail (aide-mémoire n° 18). Dans la case <b>« À »</b>, tapez les premières lettres du nom. Le carnet vous propose la personne : <b>cliquez dessus</b>. L'adresse s'écrit toute seule !</p>
<p style="margin:0"><b>Retirer :</b> ouvrez la fiche, cliquez sur les <b>trois petits points</b> (appelés <b>Plus</b>), puis sur <b>Supprimer</b>, et confirmez.</p></div>
<div class="duo"><div><img src="{img('ecrire')}"><small>La case « À »</small></div><div><img src="{img('supprimer')}"><small>Plus, puis Supprimer</small></div></div></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<div class="check"><i></i>J'ouvre mon carnet d'adresses</div>
<div class="check"><i></i>J'ajoute « Jeanne Martin », jeanne.martin@exemple.fr</div>
<div class="check"><i></i>Je clique sur « Enregistrer »</div>
<div class="check"><i></i>Je la retrouve avec la recherche</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour ajouter une personne, je clique sur…<div class="ch"><span>A. Créer un contact</span><span>B. Supprimer</span></div></li>
<li>Une adresse mail contient toujours…<div class="ch"><span>A. un espace</span><span>B. le signe @</span></div></li>
<li>Pour garder la fiche, je clique sur…<div class="ch"><span>A. Enregistrer</span><span>B. la croix</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Mon carnet d'adresses</h3>
<div class="row"><div><i>1</i>contacts.google.com</div><div><i>2</i>Créer un contact</div><div><i>3</i>Nom + adresse<br>puis Enregistrer</div><div><i>4</i>Case « À » :<br>premières lettres</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>ajouter, retrouver, corriger et retirer</b> un contact. Vos proches sont à portée de clic.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici les adresses mail de vos proches, vos questions…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je tiens mon carnet d’adresses</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
