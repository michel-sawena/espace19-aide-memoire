"""Fiche aide-mémoire 07 « Je découvre le clavier » (4 pages, modèle fiche_v3).
Usage : python3 fiche_04.py out.pdf url_sujet url_tous img_dir   url_page_entrainement"""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, IMG, URL_PAGE = sys.argv[1:6]
NB, NUM = 4, "07"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
SG = re.search(r"SG = '(.*?)'\n", SRC).group(1)     # pictogramme clic gauche du modèle
CSS += '''
.et{grid-template-columns:11mm 1fr 62mm;padding:3mm 4mm;margin-bottom:3mm}
.z img{max-height:36mm}
.et.w{grid-template-columns:11mm 1fr 92mm}
.duo img{max-height:34mm;object-fit:contain;background:#fff}
.p2 .z img{max-height:35mm}
.p2 .et{grid-template-columns:11mm 1fr 66mm;padding:2.5mm 4mm;margin-bottom:2.5mm}
.p2 .box.cor p{margin-bottom:1mm;font-size:10.3pt}
.analog img{width:58mm;flex:none;border-radius:2mm}
.kbd{display:inline-block;border:2px solid #3a0a33;border-bottom-width:4px;border-radius:2mm;padding:0 2mm;font-weight:800;background:#fff;font-size:10.5pt}
.z img.large{max-height:30mm}
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
TOUCHE = '<svg viewBox="0 0 120 70" class="pic key"><rect x="30" y="8" width="60" height="50" rx="8" fill="#fff" stroke="#3a0a33" stroke-width="4"/><rect x="30" y="52" width="60" height="10" rx="4" fill="#3a0a33"/><text x="60" y="44" font-size="28" font-weight="800" text-anchor="middle" fill="#3a0a33" font-family="Inter">A</text></svg>'
GARDER = '<svg viewBox="0 0 120 70" class="pic key"><rect x="8" y="14" width="50" height="44" rx="7" fill="#FFC72C" stroke="#3a0a33" stroke-width="4"/><text x="33" y="44" font-size="15" font-weight="800" text-anchor="middle" fill="#3a0a33" font-family="Inter">Maj</text><text x="70" y="45" font-size="26" font-weight="800" fill="#93117E" font-family="Inter">+</text><rect x="86" y="14" width="30" height="44" rx="7" fill="#fff" stroke="#3a0a33" stroke-width="4"/><text x="101" y="44" font-size="20" font-weight="800" text-anchor="middle" fill="#3a0a33" font-family="Inter">P</text></svg>'
EFFACE = '<svg viewBox="0 0 120 70" class="pic key"><rect x="14" y="12" width="92" height="46" rx="8" fill="#fff" stroke="#3a0a33" stroke-width="4"/><path d="M84 35 H36 M48 23 L36 35 L48 47" fill="none" stroke="#93117E" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
K = lambda t: f'<span class="kbd">{t}</span>'

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
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 10 MIN</span>
<h1>Je découvre le clavier</h1><div class="s">Les parties du clavier et les touches les plus utiles.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Le clavier sert à <b>écrire</b>, comme une <b>machine à écrire</b> : un message, une adresse, un mot de passe.</p>
<p style="margin:0">Chaque touche porte une <b>lettre</b>, un <b>chiffre</b> ou un <b>signe</b>.</p></div>
<div class="box"><h3>Les 3 gestes utiles</h3><div class="gestes">
<div class="ge">{TOUCHE}<b>Appuyer</b>une fois, puis lâcher</div><div class="ge">{GARDER}<b>Garder le doigt</b>sur une touche, puis appuyer sur une autre</div><div class="ge">{EFFACE}<b>Effacer</b>la lettre à gauche</div></div></div></div>
<div class="box jc" style="margin-bottom:3mm"><h3>Le mot du jour : « AZERTY »</h3>
<p style="margin:0">C'est le nom du clavier français : ce sont les <b>6 premières lettres</b> de la rangée du haut. A, Z, E, R, T, Y.</p></div>
<div class="rassure"><b>Prenez votre temps.</b> Appuyer sur une touche ne casse rien. Une faute ? Elle s'efface.</div>
{titre("Les parties du clavier", "1")}
<div class="box" style="padding:3mm"><div class="z" style="text-align:center"><img src="{img('zones')}" style="max-height:52mm;max-width:100%"></div>
<p style="margin:2mm 0 0;font-size:10.5pt"><b style="color:#b8860b">Cadre jaune</b> : les <b>lettres</b>, au milieu. <b style="color:#e0603f">Cadre corail</b> : la <b>rangée de chiffres</b>, en haut. <b style="color:#1f8c80">Cadre vert</b> : le <b>pavé numérique</b>, à droite, comme une calculatrice. Sur beaucoup d'ordinateurs <b>portables</b>, il n'existe pas : on utilise les chiffres du haut.</p></div>
{titre("Les touches à connaître", "2")}
{etape(1, "La barre d'espace", "La plus longue touche, en bas. Elle met un <b>espace</b> entre deux mots.", "espace", TOUCHE, "appuyer")}
{pied(1)}</section>''')

P.append(f'''<section class="page p2">
{etape(2, "Entrée : passer à la ligne", f"La touche {K('Entrée ↵')}, à droite, avec une flèche coudée. Elle sert aussi à <b>valider</b>.", "entree", TOUCHE, "appuyer")}
{etape(3, "Retour arrière : effacer", f"La flèche {K('←')} au-dessus d'Entrée efface la lettre <b>à gauche</b> du curseur.", "retour", EFFACE, "effacer")}
{etape(4, "Une majuscule : Maj + la lettre", f"Gardez le doigt sur {K('⇧ Maj')} (la flèche qui monte), puis appuyez sur la lettre. Lâchez.", "maj", GARDER, "garder le doigt")}
{etape(5, "Un chiffre du haut : Maj + le chiffre", f"Gardez le doigt sur {K('⇧ Maj')}, puis appuyez sur le chiffre. Sans Maj, c'est le signe du bas qui s'écrit (é, &amp;…).", "chiffres", GARDER, "garder le doigt")}
{etape(6, "L'arobase @ : Alt Gr + la touche du zéro", f"Pour une adresse mail : gardez le doigt sur {K('Alt Gr')}, à droite de l'espace, puis appuyez sur la touche <b>0 à @</b>.", "arobase", GARDER, "garder le doigt")}
{titre("Pas de panique", "!")}
<div class="box cor"><div class="deux">
<p><b>Tout s'écrit en MAJUSCULES ?</b> La touche {K('Verr Maj')} (le cadenas) est allumée. Appuyez dessus une fois.</p>
<p><b>Un signe à la place du chiffre ?</b> Effacez avec {K('←')}, puis gardez le doigt sur {K('⇧ Maj')} en tapant le chiffre.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("Bon à savoir", "★")}
<div class="box vc" style="margin-bottom:3mm"><div class="deux" style="align-items:center">
<div><p>{K('Verr Maj')} (cadenas) : <b>tout en majuscules</b>. Appuyez encore pour revenir aux minuscules.</p>
<p>{K('Suppr')} efface la lettre <b>à droite</b> du curseur. {K('Échap')}, en haut à gauche, <b>annule</b> ce qui est en cours.</p></div>
<div class="duo"><div><img src="{img('verrmaj')}"><small>Verr Maj et son voyant</small></div></div></div></div>
{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice : j'écris mon prénom</h3>
<div class="check"><i></i>Maj + la 1<sup>re</sup> lettre de mon prénom</div>
<div class="check"><i></i>Les autres lettres, en minuscules</div>
<div class="check"><i></i>La barre d'espace</div>
<div class="check"><i></i>Maj + 1, puis Maj + 9</div>
<div class="check"><i></i>Entrée pour passer à la ligne</div>
<div style="margin-top:2mm"><img src="{img('resultat')}" style="width:44mm;border-radius:2mm"><br><small>Le résultat attendu, avec Paul</small></div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Pour une majuscule, je garde le doigt sur…<div class="ch"><span>A. Maj</span><span>B. Entrée</span></div></li>
<li>Pour effacer la lettre à gauche…<div class="ch"><span>A. Échap</span><span>B. Retour arrière</span></div></li>
<li>Pour passer à la ligne…<div class="ch"><span>A. Entrée</span><span>B. la barre d'espace</span></div></li></ol>
<div class="rep">Réponses : 1 → A · 2 → B · 3 → A</div></div></div>
<div class="memo" style="margin-top:4mm"><span class="cis">✂ à découper et à garder près de l'ordinateur</span><h3>Les touches du clavier</h3>
<div class="row"><div><i>1</i>Espace<br>entre les mots</div><div><i>2</i>Entrée<br>à la ligne</div><div><i>3</i>← efface<br>à gauche</div><div><i>4</i>Maj : majuscule<br>et chiffres</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous connaissez <b>les parties du clavier</b> et ses touches utiles. Entraînez-vous : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:30mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici vos questions, les touches que vous voulez retenir…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je découvre le clavier</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
