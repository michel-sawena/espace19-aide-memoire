import sys; sys.path.insert(0,'/home/claude/work')
import render_01 as r
from PIL import Image, ImageDraw
OUT='/home/claude/work/01/fiche/'
B=r.BASE_DOCS
def shot(name, st, crop, target=None, curs=None, extra=None):
    im=r.screen(st); d=ImageDraw.Draw(im)
    if target: 
        rr=r.rect_of(target) if isinstance(target,str) else target
        d.rounded_rectangle([rr[0]-9,rr[1]-9,rr[2]+9,rr[3]+9],10,outline=r.YEL,width=8)
    if extra: extra(d)
    if curs: r.cursor(d,*curs)
    c=im.crop(crop); c=c.resize((c.width*2,c.height*2),Image.LANCZOS); c.save(OUT+name+'.png')
docs={"window":True,"view":"Documents","folders":B}
cx=r.center
shot('e1',{"window":False},(470,610,810,720),'explorer',(cx(r.rect_of('explorer'))[0]+2,cx(r.rect_of('explorer'))[1]+2))
shot('e2',{"window":True,"view":"Accueil","folders":[]},(150,120,600,420),'nav:Documents',(cx(r.rect_of('nav:Documents'))[0],cx(r.rect_of('nav:Documents'))[1]))
shot('e3',docs,(150,92,700,360),'nouveau',(cx(r.rect_of('nouveau'))[0]+10,cx(r.rect_of('nouveau'))[1]))
shot('e4',dict(docs,menu=True),(150,92,700,360),'menu:dossier',(cx(r.rect_of('menu:dossier'))[0],cx(r.rect_of('menu:dossier'))[1]))
f2=r.rect_of('folder:2')
shot('e5',dict(docs,folders=B+['x'],edit=("Nouveau dossier",True)),(350,200,900,400),(f2[0]-10,f2[1]+85,f2[2]+10,f2[3]-5))
shot('e5b',dict(docs,folders=B+['x'],edit=("Famille",False)),(350,200,900,400),(f2[0]-10,f2[1]+85,f2[2]+10,f2[3]-5))
shot('e6',dict(docs,folders=B+['Famille']),(350,200,900,400),'folder:2')
shot('m1',dict(docs,folders=B+['Famille'],ctx=2),(560,370,1130,580),'ctx:nouveau')
shot('m2',dict(docs,folders=B+['Famille'],ctx=2),(560,370,1130,580),'ctx:dossier',(cx(r.rect_of('ctx:dossier'))[0],cx(r.rect_of('ctx:dossier'))[1]))
shot('ex',dict(docs,folders=B+['Famille','Recettes']),(350,200,1050,400),'folder:3')
print('ok')
