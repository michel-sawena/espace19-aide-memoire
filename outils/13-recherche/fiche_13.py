"""Fiche aide-mémoire 13 « Je fais une recherche et je reconnais une réponse d'IA » (4 pages, modèle fiche_v3).
Usage : python3 fiche_13.py out.pdf url_sujet url_tous img_dir url_page_interactive"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG, URL_PAGE = sys.argv[1:6]
NB, NUM = 4, "13"
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
.navs img{width:100%;border-radius:3mm}
.ia-ex{border:3px solid #FF7A59}
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

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 10 MIN</span>
<h1>Je fais une recherche sur Internet</h1><div class="s">Trouver une information, et reconnaître une réponse écrite par l'IA.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Une recette, un horaire, une adresse : un <b>moteur de recherche</b> trouve les pages pour vous.</p>
<p style="margin:0">C'est comme un <b>bibliothécaire</b> : vous dites ce que vous cherchez, il vous montre les bons livres.</p></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>les mots au clavier</div><div class="ge">{ENTREE}<b>Entrée</b>pour lancer</div></div></div></div>
<div class="box jc" style="margin-bottom:3.5mm"><h3>Le mot du jour : « moteur de recherche »</h3>
<div class="deux" style="align-items:center"><p style="margin:0">Un site qui cherche des pages sur Internet. Le plus connu est <b>Google</b>. Il en existe d'autres : <b>Bing</b> (de Microsoft), <b>Qwant</b> (français), <b>Ecosia</b> (aide à planter des arbres). Ils marchent tous de la même façon.</p>
<div class="navs"><img src="{img('moteurs')}"></div></div></div>
<div class="rassure"><b>Prenez votre temps.</b> Chercher ne change rien à votre ordinateur : vous ne pouvez rien casser.</div>
{titre("Je fais une recherche", "1")}
{etape(1, "Allez sur google.fr", "Ouvrez le navigateur, puis tapez <b>google.fr</b> dans la barre d'adresse, et Entrée (voir l'aide-mémoire n° 12).", "aller", CLAV, "clavier")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(2, "Cliquez dans la grande case", "Elle est <b>au milieu</b> de la page. Un petit trait clignote : vous pouvez écrire.", "case", SG, "clic gauche")}
{etape(3, "Tapez quelques mots, puis Entrée", "Simplement, comme vous parlez. Par exemple : <b>soupe au potiron</b>. Puis la touche <b>Entrée</b> : la liste des résultats s'affiche.", "taper", ENTREE, "touche Entrée")}
{titre("Je lis les résultats", "2")}
{etape(4, "En haut : l'« Aperçu IA »", "Parfois, un encadré marqué <b>Aperçu IA</b>. Ce texte est écrit par une <b>intelligence artificielle</b> : un programme, pas une personne. Pratique, mais <b>il peut se tromper</b>, et ce n'est pas un site.", "ia")}
{etape(5, "En dessous : les liens vers les sites", "Chaque lien montre le <b>nom du site</b>, puis un <b>titre en bleu</b>. Cliquez sur un titre bleu : le site s'ouvre.", "clic", SG, "clic gauche")}
{etape(6, "Revenez à la liste", "Cliquez sur la <b>flèche vers la gauche</b>, tout en haut à gauche de la fenêtre.", "retour", SG, "clic gauche")}
{pied(2)}</section>''')

P.append(f'''<section class="page">
<div class="box cor" style="margin-bottom:3mm"><h3>Pas de panique</h3><div class="deux">
<p><b>Pas de grande case ?</b> Vérifiez que vous êtes bien sur <b>google.fr</b> : regardez la barre d'adresse, tout en haut.</p>
<p><b>Les résultats ne vont pas ?</b> Changez ou ajoutez un mot, puis Entrée. Pas besoin de faire des phrases.</p></div></div>
<div class="box vert" style="margin-bottom:3mm"><h3>Le bon réflexe : vérifier</h3>
<p style="margin:0">Pour une information <b>importante</b> (santé, argent, démarche), ne vous fiez pas à l'Aperçu IA : vérifiez sur un <b>site officiel</b>, ou sur <b>plusieurs sites</b>.</p></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : je cherche</h3>
<div class="check"><i></i>Je vais sur google.fr</div>
<div class="check"><i></i>Je tape « horaires de la mairie »</div>
<div class="check"><i></i>J'appuie sur Entrée</div>
<div class="check"><i></i>Je repère l'Aperçu IA</div>
<div class="check"><i></i>Je clique sur un titre bleu</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour chercher, je tape…<div class="ch"><span>A. quelques mots</span><span>B. une lettre</span></div></li>
<li>L'Aperçu IA est écrit par…<div class="ch"><span>A. une personne</span><span>B. un programme</span></div></li>
<li>Pour ouvrir un site, je clique sur…<div class="ch"><span>A. un titre bleu</span><span>B. l'Aperçu IA</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Je fais une recherche</h3>
<div class="row"><div><i>1</i>google.fr</div><div><i>2</i>Quelques<br>mots + Entrée</div><div><i>3</i>Aperçu IA :<br>peut se tromper</div><div><i>4</i>Titre bleu :<br>le site</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>faire une recherche</b> et <b>reconnaître une réponse d'IA</b>. Prochain aide-mémoire : les favoris.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:10pt;margin:0"><b>S'entraîner en ligne :</b> {URL_PAGE.replace("https://","")}</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos recherches, les sites utiles que vous avez trouvés…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je fais une recherche sur Internet</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
