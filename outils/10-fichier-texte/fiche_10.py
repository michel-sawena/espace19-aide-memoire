"""Fiche aide-mémoire 10 « Je crée, j'enregistre et je ferme un fichier texte » (4 pages, modèle fiche_v3).
Usage : python3 fiche_10.py out.pdf url_sujet url_tous img_dir   (page d'entraînement : 10-fichier-texte/)"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "10"
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
DBL = SG.replace('class="pic"', 'class="pic"').replace('</svg>', '<text x="30" y="70" font-size="26" font-weight="800" text-anchor="middle" fill="#93117E" font-family="Inter">×2</text></svg>')
CLAV = '<svg viewBox="0 0 120 70" class="pic key"><rect x="4" y="12" width="112" height="46" rx="8" fill="#fff" stroke="#3a0a33" stroke-width="4"/><g fill="#93117E">' + ''.join(f'<rect x="{14+i*18}" y="22" width="12" height="10" rx="2"/>' for i in range(5)) + '<rect x="30" y="40" width="60" height="10" rx="2"/></g></svg>'
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
PAGE = "michel-sawena.github.io/espace19-aide-memoire/10-fichier-texte/"
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>J'écris, j'enregistre, je ferme</h1><div class="s">Créer un fichier texte avec le Bloc-notes, le ranger, puis le retrouver.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Un <b>fichier texte</b>, c'est une <b>feuille de papier</b> dans l'ordinateur : une liste de courses, une adresse, un petit mot.</p>
<p style="margin:0">Vous <b>écrivez</b>, puis vous <b>rangez</b> la feuille dans un dossier (<b>enregistrer</b>), pour la <b>retrouver</b> plus tard.</p></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper au clavier</b>pour écrire</div><div class="ge">{DBL}<b>Double-clic</b>pour rouvrir le fichier</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « enregistrer »</h3>
<p style="margin:0"><b>Enregistrer</b>, c'est ranger votre feuille dans un dossier, avec un <b>nom</b>. Sans cela, le texte peut se perdre quand on ferme.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous ne pouvez rien casser : au pire, vous recommencez la feuille.</div>
{titre("J'écris", "1")}
{etape(1, "Cliquez sur « Démarrer »", "En bas de l'écran, au milieu : le bouton aux <b>4 carreaux bleus</b>.", "demarrer", SG, "clic gauche")}
{etape(2, "Tapez « Bloc-notes »", "Tapez <b>Bloc-notes</b> au clavier, puis cliquez sur <b>Bloc-notes</b> dans la liste.", "taper", CLAV, "clavier")}
{etape(3, "Écrivez votre texte", "Une <b>page blanche</b> s'ouvre. Cliquez dedans, puis écrivez. Par exemple : du pain, du lait, des pommes.", "page", CLAV, "clavier")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{titre("J'enregistre", "2")}
{etape(4, "Cliquez sur « Fichier », puis « Enregistrer »", "« Fichier » est <b>en haut à gauche</b>. Un menu s'ouvre : cliquez sur <b>Enregistrer</b>.", "fichier", SG, "clic gauche")}
{etape(5, "Choisissez « Documents »", "Une fenêtre s'ouvre. Dans la colonne de gauche, cliquez sur <b>Documents</b> : le tiroir où votre fichier sera rangé.", "documents", SG, "clic gauche")}
{etape(6, "Donnez un nom, puis « Enregistrer »", "En bas, dans la case <b>Nom de fichier</b>, tapez un nom facile (ex. : <b>Courses</b>). Cliquez sur le bouton <b>Enregistrer</b>. Le nom apparaît en haut : c'est rangé !", "nom", SG, "clic gauche")}
<div class="box vc" style="padding:2.5mm 4mm"><p style="margin:0"><b>Bon à savoir :</b> les touches <b>Ctrl + S</b>, appuyées ensemble, enregistrent aussi. L'ordinateur ajoute <b>.txt</b> à la fin du nom : cela veut dire « fichier texte ».</p></div>
{titre("Je ferme", "3")}
{etape(7, "Fermez : cliquez sur la croix", "<b>En haut à droite</b> de la fenêtre. Enregistrez <b>toujours avant</b> de fermer.", "fermer", SG, "clic gauche")}
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Je retrouve mon fichier", "4")}
{etape(8, "Retrouvez votre fichier", "Ouvrez l'<b>Explorateur de fichiers</b> (dossier jaune, en bas), puis <b>Documents</b>. Un <b>double-clic</b> sur « Courses » le rouvre.", "retrouver", DBL, "double-clic")}
<div class="box cor"><h3 style="margin-bottom:1mm">Pas de panique</h3><div class="deux">
<p><b>Une question s'affiche en fermant ?</b> Le texte n'est pas encore rangé : choisissez d'<b>enregistrer</b>.</p>
<p><b>Il y a déjà un texte dans la case du nom ?</b> Effacez-le, puis tapez votre nom. Évitez les signes / \\ : * ? " &lt; &gt; |</p></div></div>
<div class="deux" style="margin-top:3mm"><div class="box jc"><h3>À vous de jouer !</h3>
<div class="check"><i></i>J'ouvre le Bloc-notes</div>
<div class="check"><i></i>J'écris mon prénom</div>
<div class="check"><i></i>J'enregistre dans « Documents »</div>
<div class="check"><i></i>Je ferme avec la croix</div>
<div class="check"><i></i>Je le retrouve et je le rouvre</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour ranger mon texte, je…<div class="ch"><span>A. l'enregistre</span><span>B. le ferme</span></div></li>
<li>« Enregistrer » est dans le menu…<div class="ch"><span>A. Fichier</span><span>B. Démarrer</span></div></li>
<li>Je ferme…<div class="ch"><span>A. avant d'enregistrer</span><span>B. après</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → A · 3 → B</div></div></div>
<div class="memo" style="margin-top:3mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Mon fichier texte</h3>
<div class="row"><div><i>1</i>Démarrer,<br>Bloc-notes</div><div><i>2</i>J'écris</div><div><i>3</i>Fichier,<br>Enregistrer</div><div><i>4</i>La croix</div></div></div>
<div class="deux" style="margin-top:3mm;align-items:stretch"><div class="box vert bravo"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>écrire, ranger et fermer</b> un fichier texte.</p></div></div>
<div class="box" style="display:flex;gap:4mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:28mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo</h3><p style="font-size:10pt;margin:0">Visez ce QR code avec l'appareil photo du téléphone.</p></div></div></div>
<p style="font-size:10pt;margin:2mm 0 0"><b>S'entraîner en ligne :</b> {PAGE}</p>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici les noms de vos fichiers, où vous les rangez, vos questions…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - J\'écris, j\'enregistre, je ferme</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
