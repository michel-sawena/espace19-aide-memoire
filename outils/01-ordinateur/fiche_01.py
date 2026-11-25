"""Fiche aide-mémoire 01 « Je découvre mon ordinateur » (4 pages, modèle fiche_v3).
Usage : python3 fiche_01.py out.pdf url_sujet url_tous img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "01"
# même feuille de style que la fiche validée (fiche_v3.py)
CSS = re.search(r"CSS = '''(.*?)'''", open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read(), re.S).group(1)
CSS += '''
.et{grid-template-columns:11mm 1fr 70mm}
.z img{max-height:40mm}
.duo img{max-height:37mm;object-fit:contain;background:#fff}
.et.w{grid-template-columns:11mm 1fr 96mm}
.p2 .z img{max-height:36mm}
.p2 .box.cor p{margin-bottom:1.2mm;font-size:10.5pt}
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
MOUSE = '<svg viewBox="0 0 90 90" class="pic"><rect x="22" y="8" width="46" height="74" rx="23" fill="#fff" stroke="#3a0a33" stroke-width="5"/><path d="M22 36 H68 M45 8 V36" stroke="#3a0a33" stroke-width="5"/><path d="M4 50 H14 M76 50 H86" stroke="#93117E" stroke-width="5" stroke-linecap="round"/><path d="M8 44 L2 50 L8 56 M82 44 L88 50 L82 56" fill="none" stroke="#93117E" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PAD = '<svg viewBox="0 0 100 90" class="pic"><rect x="8" y="30" width="84" height="52" rx="8" fill="#e6e7ec" stroke="#3a0a33" stroke-width="5"/><ellipse cx="50" cy="40" rx="11" ry="16" fill="#FFC72C" stroke="#3a0a33" stroke-width="4"/><path d="M50 24 V6" stroke="#3a0a33" stroke-width="12" stroke-linecap="round"/><path d="M24 62 H76" stroke="#93117E" stroke-width="5" stroke-linecap="round" stroke-dasharray="6 6"/></svg>'
PLUG = '<svg viewBox="0 0 110 90" class="pic"><rect x="62" y="22" width="44" height="46" rx="6" fill="#3a0a33"/><rect x="70" y="36" width="30" height="16" fill="#fff"/><rect x="16" y="34" width="40" height="20" fill="#d8dae0" stroke="#3a0a33" stroke-width="4"/><path d="M2 44 H16" stroke="#3a0a33" stroke-width="8"/><path d="M30 18 L46 18" stroke="#2BB3A3" stroke-width="5" stroke-linecap="round"/></svg>'
PC = '<svg viewBox="0 0 220 170" class="folder"><rect x="8" y="20" width="120" height="80" rx="6" fill="#1e2028"/><rect x="16" y="28" width="104" height="64" fill="#4a7fd0"/><rect x="58" y="100" width="20" height="22" fill="#55575f"/><rect x="36" y="120" width="64" height="8" rx="3" fill="#55575f"/><rect x="140" y="30" width="46" height="100" rx="6" fill="#34363f"/><circle cx="163" cy="48" r="7" fill="none" stroke="#fff" stroke-width="3"/><rect x="14" y="138" width="120" height="20" rx="3" fill="#eceef2" stroke="#888" stroke-width="2"/><ellipse cx="160" cy="150" rx="10" ry="13" fill="#fff" stroke="#555" stroke-width="2"/></svg>'

def pied(n):
    return f'<div class="pied"><img src="{LOGO}"><span>Espace 19 Numérique · Formation débutant · Aide-mémoire n° {NUM}</span><span class="pn">{n} / {NB}</span></div>'

def titre(t, ico):
    return f'<h2><span class="ico">{ico}</span>{t}</h2>'

def etape(n, action, detail, image, geste="", nom=""):
    g = f'<span class="g">{geste}{nom}</span>' if (geste or nom) else ""
    zone = f'<div class="z"><img src="{img(image)}"></div>' if isinstance(image, str) else f'<div class="duo">{"".join(f"<div><img src={chr(34)}{img(i)}{chr(34)}><small>{c}</small></div>" for i, c in image)}</div>'
    cls = "et" if isinstance(image, str) else "et w"
    return f'<div class="{cls}"><div class="n">{n}</div><div class="t"><h3>{action}</h3><p>{detail}</p>{g}</div>{zone}</div>'

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 10 MIN</span>
<h1>Je découvre mon ordinateur</h1><div class="s">Ordinateur fixe ou portable : je reconnais chaque élément.</div></div></div>
<div class="intro"><div class="box vc analog">{PC}<div><h3>Fixe ou portable ?</h3>
<p>L'ordinateur <b>fixe</b> ressemble à une <b>chaîne hi-fi</b> : plusieurs éléments séparés, reliés par des fils. Il reste sur la table.</p>
<p style="margin:0">Le <b>portable</b> ressemble à un <b>poste de radio à piles</b> : tout est réuni, vous pouvez l'emporter.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{MOUSE}<b>Glisser la souris</b>à plat sur la table</div><div class="ge">{PAD}<b>Glisser un doigt</b>sur le pavé tactile</div><div class="ge">{PLUG}<b>Brancher</b>doucement, dans le bon sens</div></div></div></div>
<div class="rassure"><b>Prenez votre temps.</b> Regarder et toucher votre ordinateur ne l'abîme pas. Vous ne pouvez rien casser.</div>
{titre("Je reconnais l'ordinateur fixe", "1")}
{etape(1, "L'écran", "Il <b>affiche les images</b>, comme une télévision. Sur le fixe, l'écran est posé sur un pied.", "ecran")}
{etape(2, "Le clavier", "Il sert à <b>écrire</b> des lettres et des chiffres. Il est posé devant l'écran.", "clavier")}
{etape(3, "La souris", "Elle sert à <b>montrer</b> et à <b>cliquer</b>. Posez-la à plat et faites-la glisser : la petite flèche bouge à l'écran.", "souris", MOUSE, "glisser")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">{titre("Je reconnais l'ordinateur fixe (suite)", "1")}
{etape(4, "L'unité centrale… ou le tout-en-un", "La grande boîte est l'<b>unité centrale</b> : le <b>cerveau</b> de l'ordinateur. Le <b>bouton pour l'allumer</b> est dessus. Sur un <b>tout-en-un</b>, elle est cachée <b>derrière l'écran</b>.", [("uc", "Unité centrale (bouton entouré)"), ("toutenun", "Tout-en-un")])}
{titre("Je reconnais l'ordinateur portable", "2")}
{etape(5, "Tout est réuni", "Le portable s'ouvre comme un livre : <b>écran</b> et <b>clavier</b> dans un seul objet. Le <b>pavé tactile</b>, sous le clavier, <b>remplace la souris</b>. Il a une <b>batterie</b>, comme un téléphone.", "portable", PAD, "glisser un doigt")}
{titre("Où brancher les câbles ?", "3")}
{etape(6, "Derrière l'unité centrale", "<b>Alimentation</b> (vers la prise électrique), <b>écran</b> (HDMI), <b>clavier et souris</b> (prises USB). Sur le portable, les prises sont <b>sur les côtés</b> : le <b>chargeur</b> va dans sa petite prise ronde ou ovale.", [("prises", "Arrière de l'unité centrale"), ("cotes", "Côté du portable : chargeur")])}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>La prise USB ne rentre pas ?</b> Elle ne rentre que dans un sens : <b>retournez-la</b>. Ne forcez jamais.</p>
<p><b>Un câble s'est débranché ?</b> Rebranchez-le doucement, dans le bon sens. Rien n'est cassé.</p>
<p><b>La batterie du portable est presque vide ?</b> Branchez le chargeur : vous pouvez continuer à travailler.</p>
<p><b>Je ne trouve pas l'unité centrale ?</b> C'est peut-être un tout-en-un : regardez derrière l'écran.</p>
<p><b>Le câble d'alimentation ?</b> Ne le débranchez que lorsque l'ordinateur est éteint.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : regardez votre ordinateur</h3>
<div class="check"><i></i>Il est <b>&nbsp;fixe&nbsp;</b> ou <b>&nbsp;portable</b> ?</div>
<div class="check"><i></i>Je montre l'écran</div>
<div class="check"><i></i>Je montre le clavier</div>
<div class="check"><i></i>Je montre la souris ou le pavé tactile</div>
<div class="check"><i></i>Je trouve une prise USB</div>
<div class="mot" style="margin-top:2.5mm"><h3 style="margin:0 0 1mm">Le mot du jour : « périphérique »</h3><p style="margin:0;font-size:10.5pt">Tout ce que l'on <b>branche</b> à l'ordinateur : imprimante, haut-parleurs, casque, clé USB…</p></div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Sur un portable, qu'est-ce qui remplace la souris ?<div class="ch"><span>A. l'écran</span><span>B. le pavé tactile</span></div></li>
<li>Le cerveau de l'ordinateur fixe s'appelle…<div class="ch"><span>A. l'unité centrale</span><span>B. le clavier</span></div></li>
<li>La prise USB ne rentre pas : je…<div class="ch"><span>A. force un peu</span><span>B. la retourne</span></div></li></ol>
<div class="rep">Réponses : 1 → B · 2 → A · 3 → B</div></div></div>
{titre("Je retiens", "✓")}
<div class="memo" style="margin-top:2mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Les 4 éléments de l'ordinateur</h3>
<div class="row"><div><i>1</i>L'écran</div><div><i>2</i>Le clavier</div><div><i>3</i>La souris<br><small style="font-weight:600">(ou le pavé tactile)</small></div><div><i>4</i>L'unité centrale</div></div></div>
<div class="box vert bravo" style="margin-top:4mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>reconnaître votre ordinateur</b>. Prochain aide-mémoire : allumer et éteindre l'ordinateur.</p></div></div>
<div class="box" style="margin-top:4mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:32mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">Pas de page d'entraînement pour ce sujet : entraînez-vous sur votre propre ordinateur.</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, la marque de votre ordinateur, où se trouvent ses prises…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je découvre mon ordinateur</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
open(out.replace(".pdf", ".html"), "w").write(HTML)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto("file://" + out.replace(".pdf", ".html")); await pg.wait_for_timeout(400)
        over = await pg.evaluate("""() => [...document.querySelectorAll('.page')].map((s,i)=>{const pied=s.querySelector('.pied').getBoundingClientRect().top;let m=0;s.querySelectorAll('*').forEach(e=>{if(e.closest('.pied'))return;const b=e.getBoundingClientRect();if(b.bottom>m)m=b.bottom});return {page:i+1,deborde:Math.round(m-pied)}})""")
        print(over)
        await pg.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
