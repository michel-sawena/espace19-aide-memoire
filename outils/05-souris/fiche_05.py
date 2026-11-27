"""Fiche aide-mémoire 05 « Je prends en main la souris » (4 pages, modèle fiche_v3 / fiche_03).
Usage : python3 fiche_03.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "05"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)   # pictogramme clic gauche du modèle
CSS += '''
.et{grid-template-columns:11mm 1fr 76mm;padding:3mm 4mm;margin-bottom:3mm}
.z img{max-height:46mm}
.et.w{grid-template-columns:11mm 1fr 92mm}
.duo img{max-height:30mm;object-fit:contain;background:#fff}
.p2 .box.cor p{margin-bottom:1mm;font-size:10.3pt}
.analog .folder{width:21mm}
.carte-bureau{display:grid;grid-template-columns:88mm 1fr;gap:4mm;align-items:center;margin-bottom:3mm}
.carte-bureau img{width:100%;border-radius:3mm;border:2px solid var(--vf);display:block}
.carte-bureau ul{margin:0;padding-left:4.5mm;font-size:10.5pt}.carte-bureau li{margin-bottom:1.2mm}
.mot{background:var(--jc);border:1.5px solid #f2d675;border-radius:4mm;padding:2.5mm 4.5mm;font-size:10.3pt;margin-bottom:3mm}
'''
b64 = lambda path: "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
img = lambda n: b64(f"{IMG}/{n}.png")
LOGO = b64(f"{IMG}/logo.png")

def qr(u):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#3a0a33", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

# pictogrammes
SOURIS = '<svg viewBox="0 0 90 90" class="pic"><rect x="24" y="8" width="42" height="74" rx="21" fill="#fff" stroke="#3a0a33" stroke-width="4"/><path d="M24 36 H66 M45 8 V36" stroke="#3a0a33" stroke-width="4"/><path d="M58 60 l14 -8 M60 70 l16 0" stroke="#FFC72C" stroke-width="5" stroke-linecap="round"/></svg>'
DBL = '<svg viewBox="0 0 90 90" class="pic"><rect x="24" y="8" width="42" height="74" rx="21" fill="#fff" stroke="#3a0a33" stroke-width="4"/><path d="M26 30 A19 19 0 0 1 45 10 V36 H26 Z" fill="#FFC72C"/><path d="M24 36 H66 M45 8 V36" stroke="#3a0a33" stroke-width="4"/><text x="8" y="22" font-family="Inter" font-weight="800" font-size="20" fill="#93117E">2×</text></svg>'
CROIX = '<svg viewBox="0 0 90 90" class="pic"><rect x="12" y="16" width="66" height="58" rx="8" fill="#fff" stroke="#3a0a33" stroke-width="4"/><path d="M36 36 L54 54 M54 36 L36 54" stroke="#3a0a33" stroke-width="7" stroke-linecap="round"/></svg>'
MAIN = '<svg viewBox="0 0 220 170" class="folder"><rect x="70" y="40" width="80" height="125" rx="40" fill="#fff" stroke="#3a0a33" stroke-width="5"/><path d="M70 85 H150 M110 40 V85" stroke="#3a0a33" stroke-width="5"/><path d="M30 25 l18 18 M40 10 v22 M15 40 h22" stroke="#FFC72C" stroke-width="7" stroke-linecap="round"/><path d="M175 60 l20 -30 l4 22 l14 -6 z" fill="#3a0a33"/></svg>'

def pied(n):
    return f'<div class="pied"><img src="{LOGO}"><span>Espace 19 Numérique · Formation débutant · Aide-mémoire n° {NUM}</span><span class="pn">{n} / {NB}</span></div>'

def titre(t, ico):
    return f'<h2><span class="ico">{ico}</span>{t}</h2>'

def etape(n, action, detail, image, geste="", nom=""):
    g = f'<span class="g">{geste}{nom}</span>' if (geste or nom) else ""
    zone = f'<div class="z"><img src="{img(image)}"></div>'
    return f'<div class="et"><div class="n">{n}</div><div class="t"><h3>{action}</h3><p>{detail}</p>{g}</div>{zone}</div>'

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>Je prends en main la souris</h1><div class="s">Le curseur, le clic, le double-clic… et la croix pour fermer.</div></div></div>
<div class="intro"><div class="box vc analog">{MAIN}<div><h3>À quoi ça sert ?</h3>
<p>La <b>souris</b>, c'est <b>votre main dans l'ordinateur</b>. Quand vous la faites glisser sur la table, une petite flèche bouge à l'écran : le <b>curseur</b>.</p>
<p style="margin:0">Avec elle, vous <b>montrez</b>, vous <b>choisissez</b> et vous <b>ouvrez</b>.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic</b>une fois, pour choisir</div><div class="ge">{DBL}<b>Double-clic</b>deux fois vite, pour ouvrir</div><div class="ge">{CROIX}<b>La croix</b>en haut à droite, pour fermer</div></div></div></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous ne pouvez rien casser. Un clic de trop ? Il ne se passe rien de grave : recommencez.</div>
{titre("Je tiens la souris et je la fais glisser", "1")}
{etape(1, "Posez la main sur la souris", "Sans serrer. L'<b>index</b> se pose sur le <b>bouton gauche</b>, le <b>majeur</b> se repose sur le bouton droit (nous le verrons dans l'aide-mémoire n° 06).", "tenir", SOURIS, "la main posée")}
{etape(2, "Faites-la glisser doucement", "Le <b>curseur</b> suit le même chemin sur l'écran. Au bord de la table ? <b>Soulevez</b> la souris et reposez-la plus loin : le curseur ne bouge pas pendant ce temps.", "glisser", SOURIS, "glisser")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{titre("Je clique et je double-clique", "2")}
{etape(3, "Le clic : pour choisir", "Appuyez <b>une fois</b> sur le bouton gauche, puis relâchez. L'icône choisie se colore en <b>bleu</b>.", "clic", SG, "clic gauche")}
{etape(4, "Le double-clic : pour ouvrir", "Appuyez <b>deux fois très vite</b> sur le bouton gauche, <b>sans bouger</b> la souris. Ici, sur le dossier « Photos » : une <b>fenêtre</b> s'ouvre.", "double", DBL, "double-clic")}
{etape(5, "La croix : pour fermer", "Pour fermer la fenêtre, cliquez <b>une fois</b> sur la <b>croix</b>, tout en haut à droite. Vous revenez au bureau.", "croix", CROIX, "clic sur la croix")}
<div class="mot"><b>Le mot du jour : « curseur ».</b> C'est la petite flèche blanche qui suit les mouvements de la souris. On l'appelle aussi le <b>pointeur</b>.</div>
{titre("Je lance et je quitte un programme", "3")}
{etape(6, "Double-cliquez sur l'icône du programme", "Un <b>programme</b> s'ouvre comme un dossier. Ici, le <b>Bloc-notes</b>, pour écrire. Quand vous avez fini, cliquez sur la <b>croix</b> en haut à droite : le programme se ferme.", "bloc_ouvert", DBL, "double-clic, puis croix")}
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Pas de panique", "!")}
<div class="box cor" style="margin-bottom:3.5mm"><div class="deux">
<p><b>Rien ne s'ouvre ?</b> Le double-clic était peut-être trop lent. Recommencez, <b>un peu plus vite</b>, sans bouger la souris.</p>
<p><b>Un petit cercle tourne ?</b> L'ordinateur travaille. <b>Patientez</b> quelques secondes, ne cliquez pas encore.</p>
<p><b>Le curseur a disparu ?</b> Faites glisser la souris : il réapparaît. Regardez aussi au bord de l'écran.</p>
<p><b>Une fenêtre s'est ouverte deux fois ?</b> Pas grave : fermez-en une avec la <b>croix</b>.</p></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<div class="check"><i></i>Je pose la main sur la souris</div>
<div class="check"><i></i>Je promène le curseur sur l'écran</div>
<div class="check"><i></i>Je clique une fois sur une icône</div>
<div class="check"><i></i>Je double-clique sur un dossier</div>
<div class="check"><i></i>Je ferme la fenêtre avec la croix</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour ouvrir un dossier, je fais…<div class="ch"><span>A. un double-clic</span><span>B. un clic</span></div></li>
<li>J'appuie avec…<div class="ch"><span>A. le bouton droit</span><span>B. le bouton gauche</span></div></li>
<li>Pour fermer, je clique sur…<div class="ch"><span>A. la croix</span><span>B. l'heure</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>La souris</h3>
<div class="row"><div><i>1</i>Bouton gauche</div><div><i>2</i>Clic : choisir</div><div><i>3</i>Double-clic : ouvrir</div><div><i>4</i>Croix : fermer</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>cliquer</b>, <b>double-cliquer</b> et <b>fermer une fenêtre</b>. Prochain aide-mémoire : déplacer, agrandir, le clic droit et la molette.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, vos réussites, ce qui vous a semblé difficile…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je prends en main la souris</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
