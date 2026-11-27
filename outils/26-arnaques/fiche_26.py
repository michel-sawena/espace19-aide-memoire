"""Fiche aide-mémoire 26 « Je repère les arnaques » (4 pages, modèle fiche_v3).
Usage : python3 fiche_26.py out.pdf url_sujet url_tous url_page img_dir
Messages INVENTÉS, marqués « EXEMPLE INVENTÉ ». Conseils et numéros : voir sources_26.md."""
import asyncio, base64, io, os, re, sys, qrcode
from playwright.async_api import async_playwright

out, URL_SUJET, URL_TOUS, URL_PAGE, IMG = sys.argv[1:6]
NB, NUM = 4, "26"
SRC = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fiche_v3.py")).read()
CSS = re.search(r"CSS = '''(.*?)'''", SRC, re.S).group(1)
CSS += '''
.et{grid-template-columns:11mm 1fr 70mm;padding:2.6mm 4mm;margin-bottom:2.6mm}
.z img{max-height:52mm}
.signes{margin:1mm 0 0;padding-left:5mm;font-size:10.5pt}
.signes li{margin-bottom:.8mm}
.num{display:inline-block;background:#FFC72C;border-radius:50%;width:5mm;height:5mm;text-align:center;font-weight:800;font-size:9pt;line-height:5mm;margin-right:1mm}
.box.cor p,.box.cor li{font-size:10.3pt}
.tel{font-size:13pt;font-weight:800;color:#93117E}
.regle{font-size:11.5pt}
'''
b64 = lambda path: "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
img = lambda n: b64(f"{IMG}/{n}.png")
LOGO = b64(f"{IMG}/logo.png")

def qr(u):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(u); q.make()
    b = io.BytesIO(); q.make_image(fill_color="#3a0a33", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

def pied(n):
    return f'<div class="pied"><img src="{LOGO}"><span>Espace 19 Numérique · Formation débutant · Aide-mémoire n° {NUM}</span><span class="pn">{n} / {NB}</span></div>'

def titre(t, ico):
    return f'<h2><span class="ico">{ico}</span>{t}</h2>'

def carte(n, action, detail, image):
    return f'<div class="et"><div class="n">{n}</div><div class="t"><h3>{action}</h3>{detail}</div><div class="z"><img src="{img(image)}"></div></div>'

N = lambda k: f'<span class="num">{k}</span>'

P = []
P.append(f'''<section class="page">
<div class="entete"><img src="{LOGO}"><div class="bandeau"><span class="k">AIDE-MÉMOIRE N° {NUM} · DÉBUTANT · 15 MIN</span>
<h1>Je repère les arnaques</h1><div class="s">Faux SMS, faux mails, faux conseillers au téléphone.</div></div></div>
<div class="intro"><div class="box vc"><h3>À quoi ça sert ?</h3>
<p>Certains messages sont des <b>pièges</b>. Comme un <b>faux facteur</b> qui sonne à la porte, ils se font passer pour votre banque, La Poste ou une administration, pour <b>voler votre argent</b> ou vos codes.</p></div>
<div class="box"><h3>La règle d'or</h3>
<p class="regle">Votre banque ne vous demande <b>JAMAIS</b> vos <b>codes</b> ni votre <b>mot de passe</b>. Une administration non plus. Ni par mail, ni par SMS, ni au téléphone.</p></div></div>
<div class="box jc" style="margin-bottom:3mm"><h3>Le mot du jour : « l'hameçonnage »</h3>
<p>C'est le nom de cette arnaque : un faux message vous « pêche » comme un poisson au bout d'un hameçon, pour que vous donniez vos informations. On dit aussi « phishing ».</p></div>
<div class="rassure"><b>Pas de panique.</b> Quelques signes suffisent pour reconnaître un piège. Dans le doute, ne faites rien et demandez conseil.</div>
{titre("Le faux SMS", "1")}
{carte(1, "Regardez bien le SMS", f'<p>Exemple inventé : un « colis bloqué ». Trois signes doivent vous alerter :</p><ol class="signes" style="list-style:none;padding:0"><li>{N(1)}<b>L\'urgence</b> : « aujourd\'hui », « sinon… ».</li><li>{N(2)}<b>Un lien</b> vers un site inconnu, à l\'adresse bizarre.</li><li>{N(3)}On vous demande <b>de l\'argent, votre carte ou un code</b>.</li></ol>', "sms")}
{pied(1)}</section>''')

P.append(f'''<section class="page">
{titre("Le faux mail", "2")}
{carte(2, "Regardez l'expéditeur et le texte", f'<p>Exemple inventé :</p><ol class="signes" style="list-style:none;padding:0"><li>{N(1)}<b>L\'adresse de l\'expéditeur</b> est bizarre (un seul caractère différent suffit).</li><li>{N(2)}Le texte a <b>des fautes</b>.</li><li>{N(3)}Il vous <b>menace</b> ou promet un gain, un remboursement.</li></ol>', "mail")}
{titre("Le faux conseiller au téléphone", "3")}
{carte(3, "Il dit appeler de votre banque", '<p>Il parle d\'<b>opérations suspectes</b> sur votre compte. Puis il demande un <b>code reçu par SMS</b>, ou de valider une opération « pour l\'annuler ».</p><p><b>C\'est un piège : raccrochez.</b> Puis appelez votre banque avec le <b>numéro habituel</b> (sur votre carte ou votre relevé).</p>', "appel")}
{titre("Le bon réflexe", "✓")}
<div class="box vert"><ul class="signes"><li>Je <b>ne clique pas</b> sur le lien. Je <b>ne réponds pas</b>.</li><li>Je <b>ne donne rien</b> : ni code, ni mot de passe, ni numéro de carte.</li><li>Au téléphone, je <b>raccroche</b>. Je rappelle moi-même ma banque.</li><li>Je <b>supprime</b> le message.</li></ul></div>
{titre("Signaler · Pas de panique", "!")}
<div class="deux" style="margin-bottom:0"><div class="box"><h3>Je signale</h3>
<p><b>Faux SMS</b> : envoyez-le au <span class="tel">33 700</span> (gratuit).</p>
<p style="margin:0"><b>Faux mail</b> : sur <b>signal-spam.fr</b>, ou marquez-le comme « indésirable ».</p></div>
<div class="box cor"><h3>J'ai donné un code ?</h3>
<p>1. Appelez <b>vite</b> votre banque : faites <b>opposition</b> sur la carte.</p>
<p>2. Faites-vous guider sur <b>17cyber.gouv.fr</b>.</p>
<p style="margin:0">3. Info Escroqueries : <span class="tel">0 805 805 817</span><br>appel gratuit, du lundi au vendredi, 9h-18h30.</p></div></div>
{pied(2)}</section>''')

P.append(f'''<section class="page">{titre("À vous de jouer !", "♪")}
<div class="deux"><div class="box jc"><h3>Exercice</h3>
<p style="margin:0 0 1mm">Trouvez les <b>3 signes</b> d'arnaque dans ce SMS (exemple inventé).</p>
<img src="{img('sms_exo')}" style="width:100%;max-height:44mm;object-fit:contain">
<div class="check"><i></i>L'urgence</div><div class="check"><i></i>Le lien bizarre</div><div class="check"><i></i>La demande de code</div></div>
<div class="box quiz"><h3>Petit quiz</h3><ol>
<li>Ma banque peut me demander mon code par SMS…<div class="ch"><span>A. oui</span><span>B. jamais</span></div></li>
<li>Un « conseiller » demande un code…<div class="ch"><span>A. je raccroche</span><span>B. je le donne</span></div></li>
<li>Un faux SMS, je l'envoie au…<div class="ch"><span>A. 33 700</span><span>B. 17</span></div></li></ol>
<div class="rep">Réponses : 1 → B · 2 → A · 3 → A</div></div></div>
<div class="memo" style="margin-top:3mm"><span class="cis">✂ à découper et à garder près du téléphone</span><h3>Je repère les arnaques</h3>
<div class="row"><div><i>1</i>Urgence<br>ou menace</div><div><i>2</i>Lien<br>bizarre</div><div><i>3</i>Code, carte<br>ou argent</div><div><i>4</i>Je ne donne rien,<br>je raccroche</div></div></div>
<div class="box vert bravo" style="margin-top:3mm"><div class="med">{NUM}</div><div><h3 style="margin:0">Bravo !</h3><p style="margin:0">Vous savez <b>reconnaître un piège</b> et quoi faire. Dans le doute, parlez-en à Espace 19 Numérique.</p></div></div>
<div class="box" style="margin-top:3mm;display:flex;gap:6mm;align-items:center"><img src="{qr(URL_SUJET)}" style="width:28mm;border:2px solid #3a0a33;border-radius:2.5mm;padding:1.5mm">
<div><h3>Revoir la vidéo de cet aide-mémoire</h3><p style="font-size:10.5pt;margin:0 0 1.5mm">Visez ce QR code avec l'appareil photo de votre téléphone, puis touchez le lien qui apparaît.</p>
<p style="font-size:9.5pt;color:#6b5a68;margin:0">S'entraîner sur ordinateur : <b>{URL_PAGE.replace("https://", "")}</b></p></div></div>
{pied(3)}</section>''')

P.append(f'''<section class="page">{titre("Mes notes", "✎")}
<p style="font-size:10.5pt;color:#6b5a68">Écrivez ici le numéro habituel de votre banque, les messages douteux reçus, vos questions…</p>
<div class="lignes">{''.join('<div class="l"></div>' for _ in range(21))}</div>
<div class="box vc" style="position:absolute;left:14mm;right:14mm;bottom:22mm;display:flex;gap:5mm;align-items:center"><img src="{qr(URL_TOUS)}" style="width:20mm;border:2px solid #3a0a33;border-radius:2mm;padding:1mm">
<div><h3 style="margin:0">Tous les aide-mémoire de la formation</h3><p style="margin:0;font-size:10pt">Ce QR code ouvre la liste complète : vidéos et fiches de tous les sujets.</p></div></div>
{pied(4)}</section>''')

HTML = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>{NUM} - Je repère les arnaques</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
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
