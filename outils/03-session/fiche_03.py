"""Fiche aide-mémoire 03 « J'ouvre ma session et je découvre le bureau » (4 pages, modèle fiche_v3 / fiche_02).
Usage : python3 fiche_03.py out.pdf url_sujet url_tous url_page img_dir"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "03"
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
TOUCHE = '<svg viewBox="0 0 90 90" class="pic"><rect x="10" y="18" width="70" height="58" rx="10" fill="#3a0a33"/><rect x="10" y="12" width="70" height="58" rx="10" fill="#fff" stroke="#3a0a33" stroke-width="4"/><text x="45" y="53" font-family="Inter" font-weight="800" font-size="30" text-anchor="middle" fill="#3a0a33">A</text></svg>'
CODE = '<svg viewBox="0 0 90 90" class="pic"><rect x="6" y="28" width="78" height="34" rx="6" fill="#fff" stroke="#3a0a33" stroke-width="4"/><circle cx="24" cy="45" r="5" fill="#3a0a33"/><circle cx="39" cy="45" r="5" fill="#3a0a33"/><circle cx="54" cy="45" r="5" fill="#3a0a33"/><circle cx="69" cy="45" r="5" fill="#3a0a33"/><rect x="34" y="66" width="22" height="16" rx="3" fill="#FFC72C" stroke="#3a0a33" stroke-width="3"/><path d="M38 66 V60 a7 7 0 0 1 14 0 V66" fill="none" stroke="#3a0a33" stroke-width="3"/></svg>'
ENTREE = '<svg viewBox="0 0 90 90" class="pic"><rect x="8" y="16" width="74" height="58" rx="10" fill="#fff" stroke="#3a0a33" stroke-width="4"/><path d="M64 30 V50 H28" fill="none" stroke="#3a0a33" stroke-width="6" stroke-linecap="round"/><path d="M36 41 L26 50 L36 59" fill="none" stroke="#3a0a33" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PORTE = '<svg viewBox="0 0 220 170" class="folder"><rect x="20" y="10" width="90" height="150" rx="6" fill="#93117E" stroke="#3a0a33" stroke-width="5"/><circle cx="95" cy="88" r="7" fill="#FFC72C"/><circle cx="140" cy="88" r="16" fill="none" stroke="#FFC72C" stroke-width="9"/><path d="M156 88 H205 M190 88 V104 M202 88 V100" stroke="#FFC72C" stroke-width="9" stroke-linecap="round"/></svg>'

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
<h1>J'ouvre ma session et je découvre le bureau</h1><div class="s">Une touche, mon code, et me voilà chez moi.</div></div></div>
<div class="intro"><div class="box vc analog">{PORTE}<div><h3>À quoi ça sert ?</h3>
<p>Ouvrir sa <b>session</b>, c'est comme ouvrir la <b>porte de chez soi</b> : votre <b>code</b> est la clé.</p>
<p style="margin:0">Derrière la porte, il y a le <b>bureau</b> : votre <b>table de travail</b>, où tout commence.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{TOUCHE}<b>Une touche</b>n'importe laquelle</div><div class="ge">{CODE}<b>Votre code</b>tapé au clavier</div><div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div></div></div></div>
<div class="rassure"><b>Prenez votre temps.</b> Vous ne pouvez rien casser. Si le code est faux, l'ordinateur vous laisse simplement réessayer.</div>
{titre("J'ouvre ma session", "1")}
{etape(1, "Appuyez sur une touche, ou cliquez", "L'ordinateur est allumé : l'<b>heure et la date</b> s'affichent. Appuyez sur <b>une touche du clavier</b>, ou <b>cliquez</b> avec la souris.", "verrou", TOUCHE, "une touche")}
{etape(2, "Tapez votre code", "Une case apparaît <b>sous votre nom</b>. Tapez votre code. Des <b>petits points</b> s'affichent à la place des chiffres : c'est normal, votre code reste <b>secret</b>.", "code", CODE, "votre code")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(3, "Si rien ne se passe : touche Entrée", "Souvent, la session s'ouvre toute seule. Sinon, appuyez sur la touche <b>Entrée</b> (la grande touche avec une flèche coudée).", "entree", ENTREE, "touche Entrée")}
{titre("Je découvre le bureau", "2")}
<div class="carte-bureau"><img src="{img('bureau')}"><ul>
<li><b>Les icônes</b> : les petits dessins posés sur le bureau.</li>
<li><b>La Corbeille</b>, en haut à gauche : elle garde ce que vous jetez, comme une poubelle.</li>
<li><b>La barre des tâches</b> : la longue bande en bas de l'écran. Elle est toujours là.</li>
<li>Au milieu de la barre : le bouton <b>Démarrer</b> (quatre carreaux bleus) et la <b>loupe « Rechercher »</b>. Tout à droite : <b>l'heure et la date</b>.</li></ul></div>
<div class="mot"><b>Le mot du jour : « session ».</b> C'est votre espace personnel sur l'ordinateur, avec vos affaires et vos réglages. On l'ouvre avec son code.</div>
{titre("J'ouvre et je ferme le menu Démarrer", "3")}
{etape(4, "Cliquez sur « Démarrer »", "Le <b>menu Démarrer</b> s'ouvre. En haut, la zone <b>« Épinglé »</b> : vos programmes, rangés comme sur une étagère. En bas : votre nom, et le bouton Marche/Arrêt.", "menu", SG, "clic gauche")}
{etape(5, "Cliquez de nouveau sur « Démarrer »", "Le menu se ferme : vous revenez au bureau. Bravo !", "fermer", SG, "clic gauche")}
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Pas de panique", "!")}
<div class="box cor" style="margin-bottom:3.5mm"><div class="deux">
<p><b>J'ai oublié mon code ?</b> Sous la case, un lien parle d'un <b>code oublié</b>. Demandez de l'aide à Espace 19 avant de l'utiliser.</p>
<p><b>Le code est refusé ?</b> Retapez-le lentement. Vérifiez que vous tapez bien des <b>chiffres</b>, pas des lettres.</p>
<p><b>Le menu Démarrer s'ouvre tout seul ?</b> Cliquez de nouveau sur « Démarrer », ou sur le bureau : il se ferme.</p>
<p><b>Bon à savoir :</b> avant de vous absenter, appuyez <b>en même temps</b> sur la touche <b>Windows</b> et la lettre <b>L</b>. L'écran se verrouille ; pour revenir, tapez votre code.</p></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<div class="check"><i></i>J'appuie sur une touche</div>
<div class="check"><i></i>Je tape mon code</div>
<div class="check"><i></i>Je montre du doigt la Corbeille</div>
<div class="check"><i></i>Je clique sur « Démarrer »</div>
<div class="check"><i></i>Je clique de nouveau : le menu se ferme</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Des points remplacent mon code, c'est…<div class="ch"><span>A. une panne</span><span>B. normal</span></div></li>
<li>La barre des tâches est…<div class="ch"><span>A. en bas</span><span>B. en haut</span></div></li>
<li>Pour ouvrir le menu, je clique sur…<div class="ch"><span>A. la Corbeille</span><span>B. « Démarrer »</span></div></li></ol>
<div class="rep">Réponses : 1 → B · 2 → A · 3 → B</div></div></div>
<div class="memo" style="margin-top:5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>J'ouvre ma session</h3>
<div class="row"><div><i>1</i>Une touche</div><div><i>2</i>Mon code</div><div><i>3</i>Le bureau</div><div><i>4</i>« Démarrer »</div></div></div>
<div class="box vert bravo" style="margin-top:3.5mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>ouvrir votre session</b> et vous repérer sur le <b>bureau</b>. Prochain aide-mémoire : comprendre l'arborescence.</p></div></div>
<div class="box" style="margin-top:3.5mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, ce que vous voyez sur votre bureau… (jamais votre code !)</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - J\'ouvre ma session et je découvre le bureau</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
