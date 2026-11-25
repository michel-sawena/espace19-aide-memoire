import sys, qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.utils import ImageReader
pdfmetrics.registerFont(TTFont('R','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('B','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
out, url_sujet, url_tous, img = sys.argv[1:5]
W,H=A4; c=canvas.Canvas(out,pagesize=A4); c.setTitle("01 - Créer un dossier personnel"); c.setAuthor("Espace 19 Numérique")
NAVY=HexColor('#0F2864'); YEL=HexColor('#FFD400')
def qr(u, x, y, s):
    q=qrcode.QRCode(border=2,box_size=10); q.add_data(u); q.make(); c.drawImage(ImageReader(q.make_image(fill_color='black',back_color='white').get_image()),x,y,s,s)
def header(sub):
    c.setFillColor(NAVY); c.rect(0,H-95,W,95,fill=1,stroke=0)
    c.setFillColor(YEL); c.rect(0,H-101,W,6,fill=1,stroke=0)
    c.setFillColor(white); c.setFont('B',26); c.drawString(36,H-50,"Créer un dossier personnel")
    c.setFont('R',13); c.drawString(36,H-76,sub)
def footer(n):
    c.setFillColor(HexColor('#555555')); c.setFont('R',10); c.drawString(36,24,"Espace 19 Numérique · Formation débutant · Aide-mémoire n° 01"); c.drawRightString(W-36,24,f"page {n}/2")
steps=[("Ouvrez l'Explorateur de fichiers","Cliquez une fois sur le dossier jaune, en bas de l'écran.","e1"),
       ("Cliquez sur « Documents »","Dans la colonne de gauche.","e2"),
       ("Cliquez sur « Nouveau »","En haut à gauche de la fenêtre.","e3"),
       ("Cliquez sur « Dossier »","Un nouveau dossier apparaît.","e4"),
       ("Tapez le nom du dossier","Ne cliquez nulle part : tapez directement. Exemple : Famille.","e5"),
       ("Appuyez sur la touche Entrée","Votre dossier est créé !","e6")]
header("Aide-mémoire n° 01 · Windows 11 · Dossiers, fichiers et stockage")
y=H-118
for i,(t,s,im) in enumerate(steps):
    bh=104; top=y-i*(bh+10)
    c.setStrokeColor(HexColor('#D0D6E2')); c.setFillColor(HexColor('#F6F8FC')); c.roundRect(30,top-bh,W-60,bh,10,fill=1,stroke=1)
    c.setFillColor(YEL); c.circle(62,top-bh/2,20,fill=1,stroke=0); c.setFillColor(black); c.setFont('B',20); c.drawCentredString(62,top-bh/2-7,str(i+1))
    c.setFillColor(NAVY); c.setFont('B',16); c.drawString(94,top-36,t)
    c.setFillColor(black); c.setFont('R',13)
    words=s.split(); line=''; yy=top-62
    for w in words:
        if c.stringWidth(line+' '+w,'R',13)>270: c.drawString(94,yy,line.strip()); yy-=17; line=''
        line+=' '+w
    c.drawString(94,yy,line.strip())
    c.drawImage(f"{img}/{im}.png",W-30-160,top-bh+7,160,90)
footer(1); c.showPage()
header("Autre méthode, exercice et vidéo")
c.setFillColor(NAVY); c.setFont('B',19); c.drawString(36,H-140,"Autre méthode : le clic droit")
c.setFillColor(black); c.setFont('R',14)
for k,l in enumerate(["1. Clic DROIT dans un espace vide.","2. Pointez « Nouveau », puis « Dossier ».","3. Tapez le nom, puis appuyez sur Entrée."]): c.drawString(36,H-168-k*22,l)
c.drawImage(f"{img}/m2.png",W-36-150,H-200,150,84.4)
c.setFillColor(HexColor('#FFF6C7')); c.setStrokeColor(YEL); c.setLineWidth(3); c.roundRect(30,H-400,W-60,120,12,fill=1,stroke=1)
c.setFillColor(NAVY); c.setFont('B',19); c.drawString(50,H-315,"Exercice")
c.setFillColor(black); c.setFont('R',15); c.drawString(50,H-345,"Dans « Documents », créez un dossier nommé : Recettes")
c.setFont('R',11); c.setFillColor(HexColor('#444444')); c.drawString(50,H-372,"Attention : pas de point, de tiret, de barre oblique ni de deux-points dans le nom.")
c.setFillColor(NAVY); c.setFont('B',19); c.drawString(36,H-450,"Revoir la vidéo")
c.setFillColor(black); c.setFont('R',13); c.drawString(36,H-474,"Visez le QR code avec l'appareil photo de votre téléphone.")
qr(url_sujet,60,H-720,220); c.setFont('B',15); c.setFillColor(NAVY); c.drawCentredString(170,H-740,"Revoir cette vidéo")
qr(url_tous,W-60-120,H-640,120); c.setFont('B',12); c.drawCentredString(W-120,H-660,"Tous les aide-mémoire")
footer(2); c.save()
