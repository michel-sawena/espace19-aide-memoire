"""Fiche aide-mémoire 09 « Je range mes dossiers » (4 pages, modèle fiche_v3).
Usage : python3 fiche_19.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "19"
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
CLIP = '<svg viewBox="0 0 60 80" width="15mm" height="15mm"><path d="M38 22 V56 a10 10 0 0 1 -20 0 V18 a7 7 0 0 1 14 0 V54 a3 3 0 0 1 -6 0 V24" fill="none" stroke="#93117E" stroke-width="5" stroke-linecap="round"/></svg>'
P.append(f"""<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>J'envoie et je lis une pièce jointe</h1><div class="s">Une photo, une facture, une attestation : avec votre message.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Une pièce jointe, c'est un <b>document glissé dans l'enveloppe</b>, avec la lettre. Le message est la lettre ; la photo ou la facture est la <b>pièce jointe</b>.</p></div>
<div class="box"><h3>Les gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>je clique une fois</div><div class="ge">{DBL}<b>Double-clic</b>je choisis le document</div><div class="ge">{CLIP}<b>Le trombone</b>le dessin de la pièce jointe</div></div></div></div>
<div class="box jc" style="margin-bottom:3mm"><h3>Le mot du jour : « la vignette »</h3>
<p>Une <b>petite image</b> du document, en bas du message reçu. On clique dessus pour le voir en grand.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous pouvez vous entraîner en vous envoyant un message à vous-même.</div>
{titre("J'envoie un document", "1")}
{etape(1, "Cliquez sur « Nouveau message »", "Ouvrez votre messagerie. Cliquez sur <b>Nouveau message</b>. Écrivez l'adresse, l'objet et votre texte, comme d'habitude (aide-mémoire n° 18).", "nouveau", SG, "clic gauche")}
{etape(2, "Cliquez sur le trombone", "En bas de la fenêtre du message, cherchez le <b>petit trombone</b> et cliquez dessus.", "trombone", SG, "clic gauche")}
{pied(1)}</section>""")

P.append(f"""<section class="page">
{titre("J'envoie un document (suite)", "1")}
{etape(3, "Double-cliquez sur le document", "Une fenêtre s'ouvre avec les <b>dossiers de votre ordinateur</b>. Trouvez votre document (souvent dans <b>Images</b> ou <b>Documents</b>), puis <b>double-cliquez</b> dessus.", "choisir", DBL, "double-clic")}
{etape(4, "Vérifiez, puis « Envoyer »", "Le <b>nom du document</b> apparaît en bas du message : il est bien attaché. Cliquez sur <b>Envoyer</b>. Bravo !", "envoyer", SG, "clic gauche")}
{titre("Je lis un document reçu", "2")}
{etape(5, "Ouvrez le message au trombone", "Un <b>petit trombone</b> à côté d'un message veut dire : il y a une pièce jointe. Cliquez sur le message pour l'ouvrir.", "recu", SG, "clic gauche")}
{etape(6, "Cliquez sur la vignette", "En bas du message, cliquez sur la <b>vignette</b> : le document s'ouvre en grand. <b>Pour le garder</b> : posez la souris sur la vignette, puis cliquez sur la <b>flèche vers le bas</b>. Il va dans le dossier <b>Téléchargements</b>.", [("vignette", "Lire"), ("fleche", "Garder")], SG, "clic gauche")}
{pied(2)}</section>""")

P.append(f"""<section class="page">{titre("Pas de panique… et prudence", "!")}
<div class="box cor" style="margin-bottom:3mm">
<p><b>Je ne trouve pas le trombone ?</b> Il est <b>en bas</b> de la fenêtre du message, à côté du bouton Envoyer.</p>
<p><b>Je me suis trompé de document ?</b> Pas grave : envoyez un second message avec le bon document, et un petit mot d'explication.</p>
<p><b>Le document est trop gros ?</b> Une messagerie accepte environ <b>25 Mo</b> : envoyez les photos une par une, ou demandez conseil à Espace 19.</p>
<p style="margin:0"><b>Prudence :</b> n'ouvrez <b>jamais</b> une pièce jointe envoyée par un <b>inconnu</b>. Dans le doute, supprimez le message ou demandez conseil à Espace 19.</p></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<div class="check"><i></i>Nouveau message, à ma propre adresse</div>
<div class="check"><i></i>Le trombone, puis double-clic sur une photo</div>
<div class="check"><i></i>Envoyer</div>
<div class="check"><i></i>J'ouvre le message reçu et je clique sur la vignette</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Le dessin de la pièce jointe, c'est…<div class="ch"><span>A. une enveloppe</span><span>B. un trombone</span></div></li>
<li>Pour lire le document reçu, je clique sur…<div class="ch"><span>A. la vignette</span><span>B. Envoyer</span></div></li>
<li>Une pièce jointe d'un inconnu…<div class="ch"><span>A. je ne l'ouvre pas</span><span>B. je l'ouvre vite</span></div></li></ol>
<div class="rep">Réponses : 1 → B · 2 → A · 3 → A</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>La pièce jointe</h3>
<div class="row"><div><i>1</i>Nouveau<br>message</div><div><i>2</i>Le trombone</div><div><i>3</i>Double-clic<br>puis Envoyer</div><div><i>4</i>Lire : la<br>vignette</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>envoyer et lire une pièce jointe</b>. Prochain aide-mémoire : le carnet d'adresses.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>""")

P.append(f"""<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, les adresses de vos proches, les documents à envoyer…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>""")

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - J’envoie et je lis une pièce jointe</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
