"""Fiche aide-mémoire 02 « J'allume et j'éteins mon ordinateur » (4 pages, modèle fiche_v3).
Usage : python3 fiche_02.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "02"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)   # pictogramme clic gauche du modèle
CSS += '''
.et{grid-template-columns:11mm 1fr 66mm;padding:3mm 4mm;margin-bottom:3mm}
.z img{max-height:38mm}
.et.w{grid-template-columns:11mm 1fr 92mm}
.duo img{max-height:34mm;object-fit:contain;background:#fff}
.p2 .box.cor p{margin-bottom:1mm;font-size:10.3pt}
.analog .folder{width:19mm}
.mot{background:var(--jc);border:1.5px solid #f2d675;border-radius:4mm;padding:3mm 4.5mm}
'''
b64 = lambda path: "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
img = lambda n: b64(f"{IMG}/{n}.png")
LOGO = b64(f"{IMG}/logo.png")

def qr(u):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#3a0a33", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

# pictogrammes
PWR = '<svg viewBox="0 0 90 90" class="pic"><circle cx="45" cy="45" r="40" fill="#34363f"/><path d="M30 28 A22 22 0 1 0 60 28" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/><path d="M45 18 V44" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>'
DOIGT = '<svg viewBox="0 0 90 90" class="pic"><circle cx="45" cy="20" r="14" fill="#FFC72C" stroke="#3a0a33" stroke-width="4"/><rect x="33" y="30" width="24" height="56" rx="12" fill="#f0c8aa" stroke="#3a0a33" stroke-width="4"/><path d="M14 14 L22 20 M76 14 L68 20 M45 2 V6" stroke="#93117E" stroke-width="5" stroke-linecap="round"/></svg>'
SABLIER = '<svg viewBox="0 0 90 90" class="pic"><path d="M22 6 H68 M22 84 H68" stroke="#3a0a33" stroke-width="6" stroke-linecap="round"/><path d="M27 8 C27 34 63 34 63 8 Z M27 82 C27 56 63 56 63 82 Z" fill="#fff" stroke="#3a0a33" stroke-width="4"/><path d="M35 76 C38 66 52 66 55 76 Z" fill="#FFC72C"/><path d="M45 34 V60" stroke="#FFC72C" stroke-width="3"/></svg>'
LAMPE = '<svg viewBox="0 0 220 170" class="folder"><path d="M70 20 H150 L175 90 H45 Z" fill="#FFC72C" stroke="#3a0a33" stroke-width="5"/><rect x="104" y="90" width="12" height="50" fill="#3a0a33"/><rect x="70" y="140" width="80" height="14" rx="5" fill="#3a0a33"/><circle cx="175" cy="125" r="22" fill="#34363f"/><path d="M166 116 A12 12 0 1 0 184 116" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/><path d="M175 108 V125" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg>'

def pied(n):
    return f'<div class="pied"><img src="{LOGO}"><span>Espace 19 Numérique · Formation débutant · Aide-mémoire n° {NUM}</span><span class="pn">{n} / {NB}</span></div>'

def titre(t, ico):
    return f'<h2><span class="ico">{ico}</span>{t}</h2>'

def etape(n, action, detail, image, geste="", nom=""):
    g = f'<span class="g">{geste}{nom}</span>' if (geste or nom) else ""
    if image is None:
        zone = ""; cls = "et"; style = ' style="grid-template-columns:11mm 1fr"'
    elif isinstance(image, str):
        zone = f'<div class="z"><img src="{img(image)}"></div>'; cls = "et"; style = ""
    else:
        zone = f'<div class="duo">{"".join(f"<div><img src={chr(34)}{img(i)}{chr(34)}><small>{c}</small></div>" for i, c in image)}</div>'; cls = "et w"; style = ""
    return f'<div class="{cls}"{style}><div class="n">{n}</div><div class="t"><h3>{action}</h3><p>{detail}</p>{g}</div>{zone}</div>'

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 10 MIN</span>
<h1>J'allume et j'éteins mon ordinateur</h1><div class="s">Un appui pour allumer, trois clics pour éteindre.</div></div></div>
<div class="intro"><div class="box vc analog">{LAMPE}<div><h3>Pourquoi éteindre « par l'écran » ?</h3>
<p>Pour <b>allumer</b>, c'est comme une <b>lampe</b> : un appui sur le bouton.</p>
<p style="margin:0">Pour <b>éteindre</b>, on ne coupe pas d'un coup : on demande à l'ordinateur de <b>ranger ses affaires</b>, comme on range la cuisine avant de fermer la porte.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{DOIGT}<b>Appui bref</b>sur le bouton, puis lâcher</div><div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{SABLIER}<b>Patienter</b>sans appuyer de nouveau</div></div></div></div>
<div class="rassure"><b>Prenez votre temps.</b> Allumer et éteindre ne peut rien abîmer, si vous suivez ces étapes.</div>
{titre("J'allume mon ordinateur", "1")}
{etape(1, "Ordinateur fixe : appuyez une fois", "Le bouton est sur l'<b>unité centrale</b>. Il porte ce dessin : <b>un rond ouvert avec un petit trait</b>. Appuyez <b>une seule fois, brièvement</b>, puis lâchez.", "fixe", PWR, "bouton de mise en marche")}
{etape(2, "Portable : ouvrez, puis appuyez", "Ouvrez d'abord l'écran. Le bouton est souvent <b>au-dessus du clavier</b>, ou <b>sur le côté</b>. Appuyez <b>une seule fois</b>.", "portable", DOIGT, "appui bref")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">{titre("J'allume mon ordinateur (suite)", "1")}
{etape(3, "Patientez", "Des petits points tournent à l'écran. <b>N'appuyez pas de nouveau.</b> Quand l'<b>heure et la date</b> s'affichent, l'ordinateur est allumé. Bravo !", "verrou", SABLIER, "patienter")}
{titre("J'éteins mon ordinateur en 3 clics", "2")}
{etape(4, "Cliquez sur « Démarrer »", "En bas de l'écran, le bouton aux <b>quatre carreaux bleus</b>. Un menu s'ouvre.", "demarrer", SG, "clic gauche")}
{etape(5, "Cliquez sur « Marche/Arrêt »", "En bas à droite du menu : <b>le rond avec un petit trait</b>. Un petit menu s'ouvre.", "marche", SG, "clic gauche")}
{etape(6, "Cliquez sur « Arrêter »", "Puis <b>patientez</b> : quand l'écran est <b>tout noir</b>, l'ordinateur est éteint. Vous pouvez alors refermer le portable.", "arreter", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>Rien ne s'allume ?</b> Vérifiez que le câble est branché à la prise (le chargeur pour un portable), puis appuyez <b>une fois</b>.</p>
<p><b>L'écran du fixe reste noir ?</b> L'écran a souvent <b>son propre bouton</b> : appuyez dessus.</p>
<p><b>Tout est bloqué, rien ne répond ?</b> En dernier recours : <b>maintenez</b> le bouton enfoncé <b>une dizaine de secondes</b>. Attendez un peu, puis rallumez.</p>
<p><b>Un message parle de mises à jour ?</b> Laissez faire et patientez. Ne débranchez pas l'ordinateur.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Bon à savoir", "★")}
<div class="box vc" style="margin-bottom:3.5mm"><div class="deux" style="align-items:center">
<div><p><b>« Redémarrer »</b> (même petit menu) : l'ordinateur s'éteint puis se rallume <b>tout seul</b>. Utile quand il est lent, ou quand il vous le demande.</p>
<p style="margin:0"><b>Refermer le portable ne l'éteint pas</b> : il se met en <b>veille</b>, comme endormi. Rouvrez-le, il se réveille.</p></div>
<div class="duo"><div><img src="{img('redemarrer')}"><small>« Redémarrer »</small></div><div><img src="{img('veille')}"><small>Portable refermé : en veille</small></div></div></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : éteindre, puis rallumer</h3>
<div class="check"><i></i>Je clique sur « Démarrer »</div>
<div class="check"><i></i>Je clique sur « Marche/Arrêt »</div>
<div class="check"><i></i>Je clique sur « Arrêter »</div>
<div class="check"><i></i>J'attends l'écran tout noir</div>
<div class="check"><i></i>Je rallume : un appui bref sur le bouton</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour éteindre, je…<div class="ch"><span>A. passe par l'écran</span><span>B. appuie sur le bouton</span></div></li>
<li>Pour allumer, j'appuie sur le bouton…<div class="ch"><span>A. longtemps</span><span>B. une fois, brièvement</span></div></li>
<li>Je referme le portable : il est…<div class="ch"><span>A. éteint</span><span>B. en veille</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → B</div></div></div>
<div class="memo" style="margin-top:5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Éteindre en 3 clics</h3>
<div class="row"><div><i>1</i>Démarrer</div><div><i>2</i>Marche/Arrêt</div><div><i>3</i>Arrêter</div><div><i>4</i>J'attends<br>l'écran noir</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>allumer et éteindre votre ordinateur</b>. Prochain aide-mémoire : ouvrir sa session et découvrir le bureau.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, où se trouve le bouton de votre ordinateur…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - J\'allume et j\'éteins mon ordinateur</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
