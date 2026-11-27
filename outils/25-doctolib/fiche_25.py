"""Fiche aide-mémoire 25 « Je prends rendez-vous sur Doctolib » (4 pages, modèle fiche_v3).
Usage : python3 fiche_25.py out.pdf url_sujet url_tous img_dir   (pas de page interactive pour ce sujet)"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "25"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)     # pictogramme clic gauche du modèle
CSS += '''
.et{grid-template-columns:11mm 1fr 62mm;padding:3mm 4mm;margin-bottom:3mm}
.z img{max-height:36mm}
.et.w{grid-template-columns:11mm 1fr 92mm}
.duo img{max-height:34mm;object-fit:contain;background:#fff}
.p2 .z img{max-height:36mm}
.p2 .et{grid-template-columns:11mm 1fr 82mm;margin-bottom:2.2mm;padding:2.2mm 4mm}
.p3 .et{grid-template-columns:11mm 1fr 60mm;margin-bottom:2.5mm}
.p3 .z img{max-height:28mm}
.ex{font-size:9.6pt;color:#6b5a68}
.p2 .box.cor p{margin-bottom:1mm;font-size:10.3pt}
.analog img{width:34mm;flex:none;border-radius:3mm}
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

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>Je prends rendez-vous sur Doctolib</h1><div class="s">Trouver un praticien, prendre et annuler un rendez-vous.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('agenda')}"><div><h3>Comme l'agenda du secrétariat</h3>
<p><b>Doctolib</b> est un site pour prendre rendez-vous chez un <b>médecin</b>, un <b>dentiste</b> ou un <b>kiné</b>, <b>sans téléphoner</b>.</p>
<p style="margin:0">C'est comme l'agenda du secrétariat, <b>ouvert jour et nuit</b>.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>les lettres au clavier</div><div class="ge">{ENTREE}<b>Entrée</b>pour valider</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Le mot du jour : « créneau »</h3>
<p style="margin:0">Un <b>créneau</b>, c'est une <b>heure libre</b> dans l'agenda du praticien : une case vide où votre rendez-vous peut se placer. Un <b>praticien</b>, c'est un professionnel de santé : médecin, dentiste, kiné…</p></div>
<div class="rassure"><b>Avant de commencer :</b> il vous faut un <b>compte Doctolib</b> (votre adresse mail et votre téléphone). Prenez votre temps : regarder les heures libres ne réserve rien.</div>
{titre("Je trouve un praticien", "1")}
{etape(1, "Allez sur doctolib.fr", "Ouvrez le navigateur. Dans la <b>barre d'adresse</b>, tapez <b>doctolib.fr</b>, puis appuyez sur <b>Entrée</b>.", "adresse", CLAV, "clavier")}
{etape(2, "Remplissez les deux cases", "Au milieu de la page : dans la <b>première</b>, le métier (ex. <b>médecin généraliste</b>) ; dans la <b>seconde</b>, votre <b>ville</b>.", "cases", CLAV, "clavier")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(3, "Cliquez sur Rechercher", "La <b>liste des praticiens</b> s'affiche, avec leur adresse.", "rechercher", SG, "clic gauche")}
{titre("Je prends rendez-vous", "2")}
{etape(4, "Cliquez sur une heure libre", "À côté de chaque praticien : les <b>jours</b> et les <b>heures libres</b>. Cliquez sur celle qui vous convient.", "creneau", SG, "clic gauche")}
{etape(5, "Choisissez le motif", "Le <b>motif</b>, c'est la raison du rendez-vous. Si on vous le demande, <b>connectez-vous</b> à votre compte (petit bonhomme, en haut à droite).", "motif", SG, "clic gauche")}
{etape(6, "Vérifiez, puis confirmez", "Vérifiez le <b>jour</b>, l'<b>heure</b> et l'<b>adresse</b>. Puis cliquez sur le <b>bouton pour confirmer</b>. Votre rendez-vous est pris. <b>Bravo !</b>", "confirmer", SG, "clic gauche")}
<p class="ex">L'ordre des questions (heure, motif, connexion) peut changer d'un praticien à l'autre. Lisez bien chaque écran. Les images sont des dessins simplifiés ; les noms et adresses sont des exemples.</p>
{titre("Je retrouve et j'annule", "3")}
{etape(7, "Cliquez sur Mes rendez-vous", "Connectez-vous, puis ouvrez <b>Mes rendez-vous</b> : la liste de vos rendez-vous.", "mesrdv", SG, "clic gauche")}
{pied(2)}</section>''')

P.append(f'''<section class="page p3">
{etape(8, "Un empêchement ? Annulez", "Ouvrez le rendez-vous et cliquez sur le <b>bouton pour annuler</b>. Indiquez la <b>raison</b>, puis confirmez. La place est libérée pour un autre patient. <b>Bonus :</b> le bouton « Déplacer le rendez-vous » permet de changer d'heure.", "annuler", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>Je ne peux plus annuler en ligne ?</b> Peu de temps avant le rendez-vous, l'annulation en ligne peut être fermée. <b>Téléphonez au cabinet.</b></p>
<p><b>Aucune heure libre ?</b> Essayez un autre praticien, une autre ville proche, ou revenez un autre jour : de nouvelles heures apparaissent.</p></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice (sans réserver)</h3>
<div class="check"><i></i>Je vais sur doctolib.fr</div>
<div class="check"><i></i>Je tape « médecin généraliste »</div>
<div class="check"><i></i>Je tape ma ville</div>
<div class="check"><i></i>Je clique sur Rechercher</div>
<div class="check"><i></i>Je regarde les heures libres</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Un créneau, c'est…<div class="ch"><span>A. une heure libre</span><span>B. un médecin</span></div></li>
<li>Pour annuler, je vais dans…<div class="ch"><span>A. Rechercher</span><span>B. Mes rendez-vous</span></div></li>
<li>Trop tard pour annuler en ligne ? Je…<div class="ch"><span>A. téléphone au cabinet</span><span>B. ne fais rien</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Je prends rendez-vous</h3>
<div class="row"><div><i>1</i>Métier<br>+ ville</div><div><i>2</i>Heure<br>libre</div><div><i>3</i>Motif</div><div><i>4</i>Je<br>confirme</div></div></div>
<div class="deux" style="margin-top:3mm;align-items:stretch"><div class="box vert bravo" style="margin:0"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>prendre</b> et <b>annuler</b> un rendez-vous sur Doctolib.</p></div></div>
<div class="box" style="margin:0;display:flex;gap:4mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:28mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo</h3><p style="font-size:10pt;margin:0">Visez ce QR code avec l'appareil photo du téléphone, puis touchez le lien.</p></div></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, les noms de vos praticiens, vos prochains rendez-vous…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je prends rendez-vous sur Doctolib</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
