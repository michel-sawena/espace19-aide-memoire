"""Fiche aide-mémoire 18 « J'envoie et je reçois un mail » (4 pages, modèle fiche_v3).
Usage : python3 fiche_18.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "18"
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

CLAV = '<svg viewBox="0 0 60 60" width="60" height="60"><rect x="4" y="16" width="52" height="30" rx="5" fill="#fff" stroke="#3a0a33" stroke-width="3"/>' + ''.join(f'<rect x="{9 + 9 * i}" y="{21 + 8 * j}" width="6" height="5" rx="1" fill="#3a0a33"/>' for j in range(2) for i in range(5)) + '<rect x="16" y="38" width="28" height="4" rx="1" fill="#FFC72C" stroke="#3a0a33"/></svg>'
_DBL = SG.replace('</svg>', '<text x="30" y="70" font-size="26" font-weight="800" text-anchor="middle" fill="#93117E" font-family="Inter">×2</text></svg>')

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
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 20 MIN</span>
<h1>J'envoie et je reçois un mail</h1><div class="s">Écrire à ses proches, en quelques secondes, sans timbre.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Un mail (ou courriel), c'est une <b>lettre qui voyage par Internet</b>. Elle arrive en <b>quelques secondes</b>, sans timbre ni enveloppe. Votre <b>Boîte de réception</b> est votre boîte aux lettres : les mails reçus y arrivent.</p></div>
<div class="box"><h3>Les gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>je clique sur un bouton ou dans une case</div><div class="ge">{CLAV}<b>Le clavier</b>je tape l'adresse et le message</div></div></div></div>
<div class="box jc" style="margin-bottom:3mm"><h3>Le mot du jour : « l'adresse mail »</h3>
<p>C'est l'adresse de la personne sur Internet, par exemple <b>paul.martin@exemple.fr</b>. Elle contient toujours le signe <b>@</b>, qu'on appelle <b>arobase</b> (un petit a entouré). Elle s'écrit <b>sans espace</b>, souvent en minuscules. Demandez-la à la personne et recopiez-la <b>lettre par lettre</b>.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous ne pouvez rien casser. Selon votre messagerie, les écrans changent un peu, mais les mots restent les mêmes.</div>
{titre("Je reçois", "1")}
{etape(1, "Cliquez sur « Boîte de réception »", "Ouvrez votre messagerie. À gauche, cliquez sur <b>Boîte de réception</b> : les mails reçus sont en liste, les plus récents en haut.", "boite", SG, "clic gauche")}
{etape(2, "Cliquez sur un mail pour le lire", "Cliquez sur la ligne du mail. Il s'ouvre en grand : vous voyez <b>qui l'a envoyé</b>, le sujet et le message.", "lire", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page">
{titre("J'écris et j'envoie", "2")}
{etape(3, "Cliquez sur « Nouveau message »", "En haut à gauche, cliquez sur <b>Nouveau message</b>. Selon la messagerie, ce bouton s'appelle parfois <b>Écrire</b>. Une fenêtre s'ouvre.", "nouveau", SG, "clic gauche")}
{etape(4, "Remplissez « À » et « Objet »", "Cliquez dans la case <b>À</b> et tapez l'adresse de la personne. Puis cliquez dans la case <b>Objet</b> et écrivez le sujet en quelques mots (ex. « Bonjour »).", [("case_a", "La case À : l'adresse"), ("objet", "La case Objet : le sujet")], CLAV, "taper")}
{etape(5, "Écrivez, puis cliquez sur « Envoyer »", "Cliquez dans le grand espace et écrivez votre message, comme une lettre. Relisez-vous, puis cliquez sur <b>Envoyer</b> : le mail part tout de suite.", [("texte", "Le message"), ("envoyer", "Envoyer")], SG, "clic gauche")}
{titre("Je réponds", "3")}
{etape(6, "Ouvrez le mail, puis « Répondre »", "Ouvrez le mail reçu et cliquez sur <b>Répondre</b>. L'adresse et l'objet sont <b>déjà remplis</b>. Écrivez votre réponse, puis cliquez sur <b>Envoyer</b>.", "repondre", SG, "clic gauche")}
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Pas de panique", "!")}
<div class="box cor" style="margin-bottom:3mm">
<p><b>Un mail attendu n'est pas arrivé ?</b> Attendez quelques minutes. Regardez aussi dans les <b>courriers indésirables</b> (aussi appelés <b>spams</b>).</p>
<p><b>La personne n'a pas reçu votre mail ?</b> Vérifiez l'adresse dans la case <b>À</b> : une seule lettre fausse, un espace ou un @ oublié, et le mail ne trouve pas son chemin.</p>
<p style="margin:0"><b>Vous avez fermé la fenêtre par erreur ?</b> Recommencez avec <b>Nouveau message</b>. Ce n'est pas grave.</p></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : un mail à moi-même</h3>
<div class="check"><i></i>Je clique sur « Nouveau message »</div>
<div class="check"><i></i>Case À : je tape <b>ma propre adresse</b></div>
<div class="check"><i></i>Objet : « Essai » · Message : « Bonjour ! »</div>
<div class="check"><i></i>Je clique sur « Envoyer »</div>
<div class="check"><i></i>Je l'ouvre dans ma Boîte de réception</div>
<img src="{img('recu')}" style="width:100%;margin-top:1.5mm;border-radius:2mm;border:1px solid #ddd"></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour écrire un mail, je clique sur…<div class="ch"><span>A. Nouveau message</span><span>B. Boîte de réception</span></div></li>
<li>L'adresse de la personne va dans…<div class="ch"><span>A. Objet</span><span>B. la case À</span></div></li>
<li>Une adresse mail contient toujours…<div class="ch"><span>A. le signe @</span><span>B. un espace</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:3mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>J'envoie un mail</h3>
<div class="row"><div><i>1</i>Nouveau<br>message</div><div><i>2</i>À :<br>l'adresse</div><div><i>3</i>Objet :<br>le sujet</div><div><i>4</i>Le message,<br>puis Envoyer</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>lire, écrire, envoyer et répondre</b> à un mail. Prochain aide-mémoire : joindre et lire une pièce jointe.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici votre adresse mail, celles de vos proches (lettre par lettre), vos questions…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - J’envoie et je reçois un mail</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
