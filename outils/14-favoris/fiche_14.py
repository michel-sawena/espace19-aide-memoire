"""Fiche aide-mémoire 14 « J'ajoute et je retrouve mes favoris » (4 pages, modèle fiche_v3).
Usage : python3 fiche_14.py out.pdf url_sujet url_tous img_dir url_page"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG, URL_PAGE = sys.argv[1:6]
NB, NUM = 4, "14"
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
.analog img{width:40mm;flex:none;border-radius:3mm}
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

CTRLD = '<svg viewBox="0 0 120 70" class="pic key"><rect x="2" y="14" width="56" height="42" rx="7" fill="#fff" stroke="#3a0a33" stroke-width="4"/><text x="30" y="42" font-size="18" font-weight="800" text-anchor="middle" fill="#3a0a33" font-family="Inter">Ctrl</text><text x="68" y="44" font-size="20" font-weight="800" text-anchor="middle" fill="#93117E" font-family="Inter">+</text><rect x="78" y="14" width="40" height="42" rx="7" fill="#fff" stroke="#3a0a33" stroke-width="4"/><text x="98" y="43" font-size="20" font-weight="800" text-anchor="middle" fill="#3a0a33" font-family="Inter">D</text></svg>'
ETOILE = '<svg viewBox="0 0 120 70" class="pic key"><polygon points="60,6 69,27 92,28 74,42 80,64 60,51 40,64 46,42 28,28 51,27" fill="#FFC72C" stroke="#3a0a33" stroke-width="4"/></svg>'
P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 10 MIN</span>
<h1>J'ajoute et je retrouve mes favoris</h1><div class="s">Garder un site pour le retrouver sans rien taper.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('livre')}"><div><h3>Comme un marque-page</h3>
<p>Un <b>favori</b>, c'est comme un <b>marque-page</b> glissé dans un livre.</p>
<p style="margin:0">Vous retrouvez la page tout de suite, <b>sans chercher</b> et <b>sans taper l'adresse</b>.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{ETOILE}<b>L'étoile</b>pour ajouter</div><div class="ge">{CTRLD}<b>Ctrl + D</b>astuce clavier</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « favori »</h3>
<p style="margin:0">Un <b>favori</b> est un site que vous avez <b>gardé</b> dans votre navigateur (Microsoft Edge, Google Chrome…). Il reste enregistré même quand vous éteignez l'ordinateur. Les gestes sont les mêmes dans Edge et dans Chrome.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Ajouter un favori ne change rien au site : vous ne pouvez rien casser.</div>
{titre("J'ajoute un favori", "1")}
{etape(1, "Allez sur le site que vous aimez", "Ouvrez le navigateur, tapez l'adresse dans la <b>barre d'adresse</b>, puis Entrée. Par exemple : <b>google.fr</b>.", "site", SG, "clic gauche")}
{etape(2, "Cliquez sur l'étoile", "Au <b>bout de la barre d'adresse</b>, à droite : une petite <b>étoile</b>. Cliquez <b>une fois</b> dessus.", "etoile", SG, "clic gauche")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(3, "Cliquez sur le bouton bleu", "Une petite fenêtre montre le <b>nom</b> du favori. Rien à changer : cliquez sur le <b>bouton bleu</b> pour valider. L'étoile se <b>remplit</b>.", "valider", SG, "clic gauche")}
{titre("Je retrouve mon favori", "2")}
{etape(4, "Cliquez sur les trois petits points", "Un autre jour : ouvrez le navigateur. Tout <b>en haut à droite</b>, cliquez sur les <b>trois petits points</b>.", "points", SG, "clic gauche")}
{etape(5, "Cliquez sur « Favoris »", "Dans le menu qui s'ouvre, cliquez sur <b>Favoris</b>. La liste de vos favoris s'affiche.", "favoris", SG, "clic gauche")}
{etape(6, "Cliquez sur le nom du site", "La page s'ouvre. <b>Bravo</b>, vous n'avez rien eu à taper !", "liste", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>L'étoile est déjà remplie ?</b> La page est <b>déjà</b> dans vos favoris. Pas besoin de recommencer.</p>
<p><b>Je ne vois pas l'étoile ?</b> Appuyez sur <b>Ctrl</b> et, en même temps, sur <b>D</b> : la petite fenêtre s'ouvre aussi. Ou demandez à Espace 19.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : mon premier favori</h3>
<div class="check"><i></i>Je vais sur google.fr</div>
<div class="check"><i></i>Je clique sur l'étoile</div>
<div class="check"><i></i>Je clique sur le bouton bleu</div>
<div class="check"><i></i>Je ferme puis je rouvre le navigateur</div>
<div class="check"><i></i>Trois points › Favoris › le site</div>
<img src="{img('rempli')}" style="width:100%;margin-top:2mm;border-radius:2mm;border:2px solid #3a0a33"><small>Résultat attendu : l'étoile est remplie.</small></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Un favori, c'est comme…<div class="ch"><span>A. un marque-page</span><span>B. une poubelle</span></div></li>
<li>Pour ajouter un favori, je clique sur…<div class="ch"><span>A. la croix</span><span>B. l'étoile</span></div></li>
<li>Pour le retrouver : les trois points, puis…<div class="ch"><span>A. Favoris</span><span>B. Fermer</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Mes favoris</h3>
<div class="row"><div><i>1</i>L'étoile<br>(ajouter)</div><div><i>2</i>Bouton<br>bleu</div><div><i>3</i>Trois<br>points</div><div><i>4</i>Favoris<br>› le site</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>garder</b> un site et le <b>retrouver</b> en deux clics. Prochain aide-mémoire : télécharger un fichier.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:10pt;margin:1.5mm 0 0"><b>Pour s'entraîner :</b> {URL_PAGE.replace('https://','')}</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici les sites que vous avez mis en favoris, vos questions…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - J’ajoute et je retrouve mes favoris</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
