import json,subprocess,sys,re
d=sys.argv[1]; sc=json.load(open(sys.argv[2])); r=json.load(open(d+'/video11.mp4.rapport.json')); durs=r['durees']
# start of each scene in video
t=0; start={}
for s in sc['scenes']: start[s['id']]=t; t+=durs[s['id']]
parl=[s for s in sc['scenes'] if s.get('narration','').strip()]
ph=r['phrases']
# assign phrases to scenes in order by count (same splitter as assemble)
sys.path.insert(0,'/home/claude/espace19-aide-memoire/outils'); import render_01 as R
out=[];k=0
for s in parl:
    n=len(R._phrases(s['narration'])); a=ph[k]['debut']
    for j in range(n):
        p=ph[k]; vs=start[s['id']]+0.4+p['debut']-a; ve=start[s['id']]+0.4+p['fin']-a
        out.append((k,s['id'],vs,ve,p['texte'])); k+=1
assert k==len(ph),(k,len(ph))
for k,sid,vs,ve,x in out:
    m=(vs+ve)/2
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{m:.2f}','-i',d+'/video11.mp4','-frames:v','1','-vf','scale=640:-1',f'{d}/c_{k:02d}.png'])
    v=subprocess.run(['ffmpeg','-ss',f'{vs+0.1:.2f}','-t',f'{max(ve-vs-0.2,0.3):.2f}','-i',d+'/video11.mp4','-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
    mv=re.search(r'mean_volume: (\S+)',v).group(1)
    print(f'{k:02d} {sid:10s} {vs:6.2f}-{ve:6.2f} vol {mv:>6} dB | {x}')
