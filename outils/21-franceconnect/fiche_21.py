"""Fiche aide-mémoire 21 « Je crée un compte en ligne et j'utilise FranceConnect » (4 pages, modèle fiche_v3).
Usage : python3 fiche_21.py out.pdf url_sujet url_tous img_dir   (pas de page interactive pour ce sujet)
Écrans neutres et inventés (marqués EXEMPLE), sans logo ni charte de site officiel."""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG = sys.argv[1:5]
NB, NUM = 4, "21"
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
.ex{display:inline-block;background:#FF7A59;color:#fff;font-weight:800;font-size:9pt;border-radius:2mm;padding:.3mm 2mm;margin-left:2mm;vertical-align:middle}
.trio{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin-bottom:3mm}
.tc{border:2px solid #e9cfe4;border-radius:3mm;padding:2.5mm;background:#fff}
.tc .th{display:flex;gap:2mm;align-items:center;margin-bottom:1mm}.tc .th .n{flex:none;width:9mm;height:9mm;border-radius:50%;background:var(--j);font-size:13pt;font-weight:800;display:flex;align-items:center;justify-content:center}
.tc h3{font-size:11pt;margin:0}.tc p{font-size:10.5pt;margin:0 0 1.5mm}.tc img{width:100%;max-height:27mm;object-fit:cover;object-position:top;border:1px solid #ccc;border-radius:2mm}
.ges{font-size:10pt;margin:0 0 3mm}.ges .pic{height:6mm;width:auto;vertical-align:middle}
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

def trio(items):
    cs = "".join(f'<div class="tc"><div class="th"><div class="n">{n}</div><h3>{a}</h3></div><p>{d}</p><img src="{img(i)}"></div>' for n, a, d, i in items)
    return f'<div class="trio">{cs}</div>'

P = []
EX = '<span class="ex">EXEMPLE</span>'
P.append(f"""<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>Je crée un compte en ligne et j'utilise FranceConnect</h1><div class="s">Identifiant, mot de passe, code reçu, et une seule clé pour mes démarches.</div></div></div>
<div class="intro"><div class="box vc analog"><img src="{img('boite')}"><div><h3>Comme une boîte aux lettres</h3>
<p>Un <b>compte</b>, c'est votre boîte aux lettres <b>à votre nom</b>, sur un site.</p>
<p style="margin:0">Pour l'ouvrir : un <b>identifiant</b> (qui vous êtes : souvent votre adresse mail ou un numéro) et un <b>mot de passe</b> (votre clé, secrète).</p></div></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{SG}<b>Clic gauche</b>bouton gauche, une fois</div><div class="ge">{CLAV}<b>Taper</b>les lettres au clavier</div><div class="ge">{ENTREE}<b>Valider</b>bouton ou touche Entrée</div></div></div></div>
<div class="box jc" style="margin-bottom:4mm"><h3>Un bon mot de passe</h3>
<p>Il est <b>long</b> : au moins <b>12 caractères</b>. Il contient un <b>nombre</b>, une <b>majuscule</b> et un <b>signe</b> (! ? $…).</p>
<p style="margin:0"><b>Astuce :</b> pensez à une phrase, gardez la <b>première lettre</b> de chaque mot, les chiffres et la ponctuation. {EX} « Mon chat Félix a 3 ans ! » → <b>McFa3a!</b> (à allonger avec une phrase plus longue, et à ne pas copier tel quel). Évitez 1234.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Le mot de passe et le code reçu sont <b>secrets</b> : ne les donnez à personne, même au téléphone.</div>
{titre("Je crée un compte", "1")}
{etape(1, "Cliquez sur le bouton pour créer un compte", f"Sur le site de la démarche. Le nom du bouton change d'un site à l'autre. {EX}", "creer", SG, "clic gauche")}
{pied(1)}</section>""")

P.append(f"""<section class="page p2">
{etape(2, "Remplissez les cases", "Votre <b>adresse mail</b>, puis votre <b>mot de passe</b>. Cliquez d'abord dans la case, puis tapez.", "form", CLAV, "clavier")}
{etape(3, "Recopiez le code reçu, puis validez", "Le site envoie un <b>code</b> par <b>SMS</b> ou par <b>mail</b>. Recopiez-le dans la case. <b>Votre compte est créé. Bravo !</b>", [("sms", "SMS reçu"), ("code", "je recopie le code")], CLAV, "clavier")}
{titre("Je me connecte avec FranceConnect", "2")}
<div class="box vc analog" style="margin-bottom:3mm"><img src="{img('portes')}" style="width:42mm"><div><h3>Le mot du jour : « FranceConnect »</h3>
<p style="margin:0">C'est <b>la solution de l'État</b> pour vous connecter à vos démarches en ligne avec un compte <b>que vous avez déjà</b> : impots.gouv.fr, ameli.fr, L'Identité Numérique La Poste, MSA, France Identité… Comme un <b>passe-partout</b> : pas besoin de créer un compte différent pour chaque démarche.</p></div></div>
{etape(4, "Cliquez sur « S'identifier avec FranceConnect »", f"Sur le site de la démarche. {EX}", "fc_bouton", SG, "clic gauche")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>Le code n'arrive pas ?</b> Attendez quelques minutes. Regardez vos SMS et votre messagerie. Sinon, demandez à Espace 19.</p>
<p><b>Quelqu'un vous appelle et demande votre code ?</b> Ne le donnez pas : raccrochez.</p>
<p><b>Impôts avec le compte ameli ?</b> Sur impots.gouv.fr, cette connexion est suspendue : choisissez votre compte <b>impots.gouv.fr</b>.</p>
<p><b>Ça ne marche pas ?</b> Votre compte doit porter votre nom exact, comme sur votre acte de naissance. Une mairie ou un conseiller France services peut aider.</p></div></div>
{pied(2)}</section>""")

P.append(f"""<section class="page">{trio([(5, "Choisissez un compte que vous avez déjà", "Par exemple : impôts.", "fc_choix"), (6, "Tapez identifiant et mot de passe", "Ceux de ce compte, puis validez.", "fc_saisie"), (7, "Cliquez sur « Continuer »", "Vous êtes connecté. <b>Bravo !</b>", "fc_cont")])}
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<div class="check"><i></i>Je trouve le bouton « S'identifier avec FranceConnect »</div>
<div class="check"><i></i>Je choisis mon compte</div>
<div class="check"><i></i>Je tape identifiant et mot de passe</div>
<div class="check"><i></i>Je clique sur « Continuer »</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Un bon mot de passe a au moins…<div class="ch"><span>A. 4 caractères</span><span>B. 12 caractères</span></div></li>
<li>Le code reçu par SMS, je le donne…<div class="ch"><span>A. à personne</span><span>B. si on m'appelle</span></div></li>
<li>FranceConnect utilise…<div class="ch"><span>A. un compte que j'ai déjà</span><span>B. un nouveau compte</span></div></li></ol>
<div class="rep">Réponses : 1 → B · 2 → A · 3 → A</div></div></div>
<div class="memo" style="margin-top:3mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Je me connecte avec FranceConnect</h3>
<div class="row"><div><i>1</i>S'identifier avec<br>FranceConnect</div><div><i>2</i>Mon compte<br>(impôts…)</div><div><i>3</i>Identifiant +<br>mot de passe</div><div><i>4</i>Continuer</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez créer un compte et vous connecter avec <b>FranceConnect</b>. Prochain aide-mémoire : ameli.fr.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p></div></div>
{pied(3)}</section>""")

P.append(f"""<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, les sites où vous avez un compte (jamais vos mots de passe !)…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>""")

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je crée un compte en ligne et j’utilise FranceConnect</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
