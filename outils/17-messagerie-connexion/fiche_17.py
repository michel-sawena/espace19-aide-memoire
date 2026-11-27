"""Fiche aide-mémoire 17 « Je me connecte et je me déconnecte de ma messagerie » (4 pages, modèle fiche_v3).
Usage : python3 fiche_17.py out.pdf url_sujet url_tous url_page img_dir
Écrans : messagerie dessinée NEUTRE (aucun logo ni charte d'un site réel). Libellés écrits tels quels
seulement s'ils sont confirmés par l'aide Google : « Déconnexion », « Utiliser un autre compte », « Connexion »."""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "17"
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
.res img{width:100%;border-radius:2mm;border:1px solid #ccc}
.pan{display:grid;grid-template-columns:1fr 52mm;gap:4mm;align-items:center}
.pan img{width:100%;border-radius:2mm}
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
<h1>Je me connecte et je me déconnecte de ma messagerie</h1><div class="s">Ouvrir sa boîte aux lettres sur Internet, puis la refermer.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('analogie')}"><div><h3>Comme une boîte aux lettres</h3>
<p>Votre <b>messagerie</b>, c'est votre <b>boîte aux lettres sur Internet</b>.</p>
<p style="margin:0"><b>Se connecter</b>, c'est l'ouvrir avec sa clé. <b>Se déconnecter</b>, c'est la refermer.</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>les lettres au clavier</div><div class="ge">{ENTREE}<b>Entrée</b>pour valider</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Ce qu'il vous faut : votre « clé »</h3>
<p style="margin:0"><b>1. Votre adresse e-mail</b>, par exemple <b>jean.exemple@gmail.com</b> (c'est un exemple). <b>2. Votre mot de passe</b> : un mot secret, que vous seul connaissez. Gardez-les <b>notés dans un endroit sûr, chez vous</b>, jamais à côté de l'ordinateur.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Les écrans changent un peu d'une messagerie à l'autre, mais les étapes restent les mêmes : <b>l'adresse, puis le mot de passe</b>.</div>
{titre("Je me connecte", "1")}
{etape(1, "Allez sur le site de votre messagerie", "Ouvrez le navigateur. Cliquez dans la <b>barre d'adresse</b>, tout en haut, et tapez l'adresse du site. Pour <b>Gmail</b> : <b>mail.google.com</b>. Puis appuyez sur <b>Entrée</b>.", "site", CLAV, "clavier, puis Entrée")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(2, "Tapez votre adresse e-mail", "Cliquez dans la case, tapez votre adresse <b>sans espace</b>. Puis cliquez sur le <b>bouton bleu</b> pour continuer.", "adresse", CLAV, "clavier")}
{etape(3, "Tapez votre mot de passe", "Il s'affiche en <b>petits points</b> : c'est normal, il est caché. Cliquez sur le <b>bouton bleu</b>. Vos messages s'affichent : <b>bravo, vous êtes connecté !</b>", "motdepasse", CLAV, "clavier")}
{titre("Je me déconnecte", "2")}
{etape(4, "Cliquez sur le petit rond, en haut à droite", "Il montre <b>votre photo</b>, ou <b>votre initiale</b>. Un petit menu s'ouvre.", "rond", SG, "clic gauche")}
{etape(5, "Cliquez sur « Déconnexion »", "Votre boîte est <b>refermée</b> : la page de connexion revient. Personne ne peut plus lire vos messages.", "deco", SG, "clic gauche")}
<div class="box vc" style="margin-top:1mm"><h3>Sur un ordinateur public (médiathèque, Espace 19…)</h3><p style="margin:0">Déconnectez-vous <b>toujours avant de partir</b>. Sinon, la personne suivante pourrait ouvrir votre boîte.</p></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Pas de panique", "!")}
<div class="box cor pan" style="margin-bottom:3mm"><div>
<p><b>Une adresse qui n'est pas la vôtre est déjà affichée ?</b> Cliquez sur <b>« Utiliser un autre compte »</b>, puis tapez votre adresse.</p>
<p><b>Vous voyez une page qui présente Gmail, sans case à remplir ?</b> Cliquez sur <b>« Connexion »</b>, en haut à droite.</p>
<p style="margin:0"><b>Mot de passe refusé ou oublié ?</b> Retapez-le lentement, en respectant les majuscules. Toujours bloqué ? Demandez de l'aide à <b>Espace 19</b>.</p></div>
<img src="{img('autre')}"></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<div class="check"><i></i>Je vais sur le site de ma messagerie</div>
<div class="check"><i></i>Je tape mon adresse, bouton bleu</div>
<div class="check"><i></i>Je tape mon mot de passe, bouton bleu</div>
<div class="check"><i></i>Le rond en haut à droite, puis « Déconnexion »</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour me connecter, il me faut…<div class="ch"><span>A. adresse + mot de passe</span><span>B. mon numéro de carte</span></div></li>
<li>Pour me déconnecter, je clique…<div class="ch"><span>A. en bas à gauche</span><span>B. sur le rond en haut à droite</span></div></li>
<li>Sur un ordinateur public…<div class="ch"><span>A. je me déconnecte</span><span>B. je laisse ouvert</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:2.5mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Ma messagerie</h3>
<div class="row"><div><i>1</i>Mon<br>adresse</div><div><i>2</i>Mon mot<br>de passe</div><div><i>3</i>Le rond en<br>haut à droite</div><div><i>4</i>Déconnexion</div></div></div>
<div class="box vert bravo" style="margin-top:2mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>ouvrir</b> et <b>refermer</b> votre messagerie. Prochain aide-mémoire : envoyer et recevoir un mail.</p></div></div>
<div class="box" style="margin-top:2mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:28mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur (messagerie d'exercice) : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions… mais <b>jamais votre mot de passe</b> sur une feuille qui reste près de l'ordinateur.</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je me connecte et je me déconnecte de ma messagerie</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
