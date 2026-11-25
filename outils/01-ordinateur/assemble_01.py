"""Assemble vidéo + voix pour le sujet 01 (Découvrir l'ordinateur : fixe et portable).
Usage : python3 assemble_01.py script_01.json 01.mp3 sortie.mp4

Même principe que ../assemble.py (chaque paragraphe de voix calé au début de sa scène), avec quatre différences :
- les fins de phrase sont trouvées par ../aligne.py (débit en syllabes), plus fiable que la position des pauses ;
- le module de rendu est celui du sujet (render_01_ordinateur.py), importé directement ;
- la voix est encodée en mono 64 kbit/s (fichier < 3 Mo, sous la limite d'envoi vers Drive) ;
- les sous-titres suivent les VRAIS débuts et fins de phrase mesurés dans la voix
  (et non une répartition proportionnelle au nombre de caractères).
"""
import json, os, re, subprocess, sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
sys.path.insert(0, os.path.join(ICI, ".."))
import render_01 as R
import render_01_ordinateur as V
import aligne as A

script, voix, out = sys.argv[1:4]
sc = json.load(open(script))
parlees = [s for s in sc["scenes"] if s["narration"]]
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voix]))

# phrases, dans le même découpage que les sous-titres
phr = []   # (index_paragraphe, texte)
for pi, s_ in enumerate(parlees):
    for x in R._phrases(s_["narration"]):
        phr.append((pi, x))
# alignement par syllabes (voir ../aligne.py)
bornes_ph, rapport_ph = A.aligne(voix, [x for _, x in phr])   # phrase k : [bornes_ph[k], bornes_ph[k+1]]
douteuses = [(phr[k][1], round(q, 2)) for k, q in enumerate(rapport_ph) if not 0.75 <= q <= 1.35]
if douteuses:
    sys.exit(f"Alignement douteux, vérifier : {douteuses}")
coupes = bornes_ph[1:-1]
cuts = [coupes[k] for k in range(len(coupes)) if phr[k][0] != phr[k + 1][0]]
bornes = [0.0] + cuts + [total]
seg = {s["id"]: (bornes[i], bornes[i + 1]) for i, s in enumerate(parlees)}

# durées : paragraphe + marge pour refaire ; scènes muettes gardent leur durée
MARGE = {"uc": 1.5, "souris": 1.5, "pave": 2, "prises": 2, "usb": 1.5, "cotes": 1.5, "pause1": 3, "exercice": 2}
DEBUT = 0.4
durs, decal, t = {}, [], 0.0
subs = {}   # narration -> [(début, fin, phrase)] en temps de scène
for s in sc["scenes"]:
    if s["id"] in seg:
        a, b = seg[s["id"]]
        D = round((b - a) + MARGE.get(s["id"], 1.0), 2)
        decal.append((t, a, b - a))
        pi = parlees.index(s)
        lst = []
        for k, (p, x) in enumerate(phr):
            if p == pi:
                lst.append((DEBUT + bornes_ph[k] - a, DEBUT + bornes_ph[k + 1] - a, x))
        subs[s["narration"]] = lst
    else:
        D = 10.0 if s["id"] == "attente" else 3.0
    durs[s["id"]] = D; t += D
json.dump(durs, open(out + ".durations.json", "w"), indent=1)

def sub_exact(narr, tt, D, start=DEBUT):
    lst = subs.get(narr)
    if not lst: return ""
    for i, (d0, f0, x) in enumerate(lst):
        fin = lst[i + 1][0] if i + 1 < len(lst) else D - 0.3   # la dernière phrase reste jusqu'à la fin de la scène
        if d0 - 0.15 <= tt < fin: return x
    return ""
R.sub_at = sub_exact

muette = out + ".muette.mp4"
V.main(script, out + ".durations.json", muette)

# piste voix : chaque paragraphe placé au début de sa scène (+0,4 s)
filt, ins = [], []
for i, (t0, a, l) in enumerate(decal):
    ms = int((t0 + DEBUT) * 1000)
    filt.append(f"[1:a]atrim={a:.3f}:{a + l:.3f},asetpts=PTS-STARTPTS,adelay={ms}|{ms}[a{i}]")
    ins.append(f"[a{i}]")
filt.append("".join(ins) + f"amix=inputs={len(ins)}:normalize=0:duration=longest,apad=whole_dur={t:.2f}[aout]")
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", muette, "-i", voix, "-filter_complex", ";".join(filt),
                       "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-ac", "1", "-b:a", "64k", "-movflags", "+faststart", out])

# contrôle : durée de voix de chaque scène vs longueur du texte (~0,07 s/caractère + 1,3 s/phrase)
controle = []
for s in parlees:
    a, b = seg[s["id"]]; nph = len(R._phrases(s["narration"]))
    att = 0.07 * len(s["narration"]) + 1.3 * nph
    controle.append({"scene": s["id"], "voix_s": round(b - a, 2), "attendu_s": round(att, 2), "ecart": round((b - a) / att, 2)})
json.dump({"phrases": [{"debut": round(bornes_ph[k], 2), "fin": round(bornes_ph[k + 1], 2), "texte": x} for k, (_, x) in enumerate(phr)],
           "controle": controle, "rapport_phrases": [round(q, 2) for q in rapport_ph], "durees": durs}, open(out + ".rapport.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(controle, ensure_ascii=False))
print("duree_voix", total, "duree_video", t)
