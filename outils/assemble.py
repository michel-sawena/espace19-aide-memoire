"""Assemble vidéo + voix : découpe la voix aux silences entre scènes, recale la durée
de chaque scène sur sa phrase, rend la vidéo et ajoute la voix.
Usage : python3 assemble.py script.json voix.mp3 sortie.mp4
"""
import json, re, subprocess, sys
sys.path.insert(0, "/home/claude/work")

script, voix, out = sys.argv[1:4]
sc = json.load(open(script))
parlees = [s for s in sc["scenes"] if s["narration"]]
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voix]))

def silences(noise, d):
    log = subprocess.run(["ffmpeg", "-i", voix, "-af", f"silencedetect=noise={noise}dB:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    return [((a + b) / 2, b - a) for a, b in zip(st, en) if 0.3 < a and b < total - 0.2]

# on garde les N-1 silences les plus longs (N = scènes parlées), en ajustant le seuil
need = len(parlees) - 1
for noise, d in ((-35, 0.5), (-35, 0.4), (-30, 0.35), (-30, 0.3), (-28, 0.25)):
    sil = silences(noise, d)
    if len(sil) >= need: break
if len(sil) < need:
    sys.exit(f"Découpe impossible : {len(sil)} silences pour {need} coupures")
cuts = sorted(m for m, _ in sorted(sil, key=lambda x: -x[1])[:need])
bornes = [0.0] + cuts + [total]
seg = {s["id"]: (bornes[i], bornes[i + 1]) for i, s in enumerate(parlees)}

# durées : phrase + marge (pause pour refaire) ; scènes muettes gardent leur durée
MARGE = {"ouvrir": 3, "documents": 3, "nouveau": 3, "dossier": 3, "taper": 3, "entree": 2, "clicdroit": 4, "pause1": 3, "exercice": 2}
durs, decal, t = {}, [], 0.0
for s in sc["scenes"]:
    if s["id"] in seg:
        a, b = seg[s["id"]]
        D = round((b - a) + MARGE.get(s["id"], 1.0), 2)
        decal.append((t, a, b - a))
    else:
        D = 10.0 if s["id"] == "attente" else 3.0
    durs[s["id"]] = D; t += D
json.dump(durs, open(out + ".durations.json", "w"), indent=1)

muette = out + ".muette.mp4"
subprocess.check_call(["python3", "/home/claude/work/render_01.py", script, out + ".durations.json", muette])

# piste voix : chaque phrase placée au début de sa scène (+0,4 s)
filt, ins = [], []
for i, (t0, a, l) in enumerate(decal):
    filt.append(f"[1:a]atrim={a:.3f}:{a + l:.3f},asetpts=PTS-STARTPTS,adelay={int((t0 + 0.4) * 1000)}|{int((t0 + 0.4) * 1000)}[a{i}]")
    ins.append(f"[a{i}]")
filt.append("".join(ins) + f"amix=inputs={len(ins)}:normalize=0:duration=longest,apad=whole_dur={t:.2f}[aout]")
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", muette, "-i", voix, "-filter_complex", ";".join(filt),
                       "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out])
print(json.dumps({"duree_voix": total, "coupures": cuts, "durees": durs}, ensure_ascii=False))
