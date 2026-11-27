"""Fiche aide-mémoire 11 « Je gère mes fichiers » (4 pages, modèle fiche_v3).
Usage : python3 fiche_11.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "11"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)     # pictogramme clic gauche du modèle
SD = re.search(r"SD = '(.*?)'\n", SRC).group(1)     # clic droit
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
GLISSE = '<svg viewBox="0 0 120 70" class="pic key"><rect x="8" y="10" width="34" height="44" rx="4" fill="#fff" stroke="#3a0a33" stroke-width="4"/><path d="M46 32 h40 M76 22 l12 10 -12 10" fill="none" stroke="#93117E" stroke-width="6" stroke-linecap="round"/><rect x="92" y="18" width="24" height="30" rx="3" fill="#FFC72C" stroke="#3a0a33" stroke-width="3"/></svg>'
KEY_ENTREE = '<svg viewBox="0 0 120 70" class="pic key"><rect x="4" y="9" width="112" height="58" rx="10" fill="#6b5a68"/><rect x="4" y="4" width="112" height="56" rx="10" fill="#fff" stroke="#3a0a33" stroke-width="4"/><text x="60" y="41" font-size="22" font-weight="800" text-anchor="middle" fill="#3a0a33" font-family="Inter">Entrée ↵</text></svg>'
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

CSS += """
.p2 .et{grid-template-columns:11mm 1fr 66mm}
.p2 .z img{max-height:38mm}
.et.w .duo{display:flex;gap:2mm}
.et.w .duo>div{flex:1;text-align:center}
"""
P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>Je gère mes fichiers</h1><div class="s">Renommer, déplacer, copier, supprimer… et récupérer un fichier.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Un <b>fichier</b>, c'est comme une <b>feuille de papier</b>. On peut lui changer son nom, la ranger dans une autre chemise, la photocopier, la jeter à la poubelle… et la reprendre dans la poubelle !</p>
<p style="margin:0">Tout commence par un <b>clic droit</b> sur le fichier.</p></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SD}<b>Clic droit</b>bouton droit : le menu</div><div class="ge">{SG}<b>Clic gauche</b>je choisis</div><div class="ge">{GLISSE}<b>Glisser</b>bouton gauche appuyé</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « Corbeille »</h3>
<p style="margin:0">C'est la <b>poubelle</b> de l'ordinateur, sur le bureau. Un fichier supprimé y attend : tant que la Corbeille n'est pas vidée, on peut le <b>récupérer</b>.</p></div>
<div class="rassure"><b>Pas d'inquiétude.</b> En haut du menu du clic droit, il y a de petites icônes. <b>Posez la souris dessus</b> : leur nom apparaît.</div>
{titre("Je change le nom d'un fichier", "1")}
{etape(1, "Clic droit sur le fichier, puis « Renommer »", "Dans le menu, cliquez sur l'icône <b>Renommer</b>. Le nom devient bleu.", "renommer", SD, "clic droit")}
{etape(2, "Tapez le nouveau nom, puis Entrée", "Par exemple « Liste de courses ». Appuyez sur la touche <b>Entrée</b> pour valider.", "taper", KEY_ENTREE, "touche Entrée")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{titre("Je range et je copie", "2")}
{etape(3, "Déplacer : faites glisser le fichier", "Cliquez sur le fichier et <b>gardez le bouton appuyé</b>. Faites glisser jusqu'au dossier, puis <b>lâchez</b>. Le fichier est rangé dedans.", "glisser", GLISSE, "glisser")}
{etape(4, "Copier : clic droit, puis « Copier »", "Comme une <b>photocopie</b> : l'original reste à sa place.", "copier", SD, "clic droit")}
{etape(5, "Ouvrez le dossier, puis « Coller »", "Ouvrez le dossier où vous voulez la copie. En haut de la fenêtre, cliquez sur l'icône <b>Coller</b>. La copie apparaît.", "coller", SG, "clic gauche")}
{titre("Je jette… et je récupère", "3")}
{etape(6, "Supprimer : clic droit, puis « Supprimer »", "Le fichier part dans la <b>Corbeille</b>, comme une feuille dans la poubelle.", "supprimer", SD, "clic droit")}
{etape(7, "Récupérer : ouvrez la Corbeille", "Sur le bureau, <b>double-cliquez</b> sur la Corbeille. Puis <b>clic droit</b> sur votre fichier et <b>Restaurer</b> : il retourne à sa place d'origine.", [("corbeille", "La Corbeille"), ("restaurer", "Restaurer")], SD, "clic droit")}
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Pas de panique", "!")}
<div class="box cor" style="margin-bottom:3.5mm"><div class="deux">
<p><b>Le fichier a disparu en glissant ?</b> Il est sûrement dans le dossier où vous l'avez lâché. Ouvrez ce dossier.</p>
<p><b>J'ai supprimé par erreur ?</b> Ouvrez la Corbeille, clic droit sur le fichier, <b>Restaurer</b>.</p></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : un fichier qui voyage</h3>
<div class="check"><i></i>Je renomme un fichier</div>
<div class="check"><i></i>Je le range dans un dossier (glisser)</div>
<div class="check"><i></i>Je le supprime</div>
<div class="check"><i></i>J'ouvre la Corbeille</div>
<div class="check"><i></i>Je le restaure</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour voir le menu, je fais…<div class="ch"><span>A. un clic droit</span><span>B. un double-clic</span></div></li>
<li>Un fichier supprimé va…<div class="ch"><span>A. dans la Corbeille</span><span>B. nulle part</span></div></li>
<li>Pour le récupérer, je clique sur…<div class="ch"><span>A. Copier</span><span>B. Restaurer</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → A · 3 → B</div></div></div>
<div class="memo" style="margin-top:5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Gérer un fichier</h3>
<div class="row"><div><i>1</i>Clic droit<br>sur le fichier</div><div><i>2</i>Renommer<br>Copier · Supprimer</div><div><i>3</i>Glisser<br>pour ranger</div><div><i>4</i>Corbeille<br>→ Restaurer</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>renommer, ranger, copier, jeter et récupérer</b> un fichier. Vous êtes maître de vos papiers !</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, le nom de vos fichiers importants, le dossier où vous les rangez…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je gère mes fichiers</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
