"""Alignement phrase par phrase d'une voix off sur le texte du script (sans reconnaissance vocale).

Principe : on repère toutes les pauses de la voix (silencedetect), ce qui découpe la voix en
morceaux de parole. Chaque phrase du script occupe un groupe de morceaux consécutifs. On choisit
les groupes (programmation dynamique) pour que le temps de parole de chaque phrase soit
proportionnel à son nombre de syllabes (débit mesuré sur toute la voix), en préférant couper
sur les pauses longues. Plus robuste que le simple choix des pauses par position : la voix
marque aussi des pauses aux virgules et aux deux-points.

Contrôle : `rapport` vaut (parole mesurée / parole attendue) pour chaque phrase ;
entre 0,70 et 1,40 partout = alignement cohérent.
"""
import math, re, subprocess

def syllabes(t):
    t = t.lower().replace("usb", " u esse bé ").replace("19", " dix neuf ")
    n = 0
    for w in re.findall(r"[a-zàâäéèêëîïôöûùüœç]+", t):
        w2 = re.sub(r"(?<=[^aeiouyàâéèêëîïôûùœ])(e|es|ent)$", "", w) if len(w) > 3 else w
        n += max(1, len(re.findall(r"[aeiouyàâäéèêëîïôöûùüœ]+", w2)))
    return n

def duree(voix):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voix]))

def aligne(voix, phrases):
    """Renvoie (bornes, rapport) : la phrase k va de bornes[k] à bornes[k+1] (secondes)."""
    total = duree(voix)
    log = subprocess.run(["ffmpeg", "-i", voix, "-af", "silencedetect=noise=-30dB:d=0.15", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    sil = [(a, b) for a, b in zip(st, en) if a > 0.3 and b < total - 0.05]
    segs, cur = [], 0.0
    for a, b in sil:
        segs.append((cur, a, b - a)); cur = b
    segs.append((cur, total, 0.0))
    N, K = len(segs), len(phrases)
    if N < K:
        raise SystemExit(f"Alignement impossible : {N} morceaux de parole pour {K} phrases")
    S = [syllabes(x) for x in phrases]
    pre = [0.0]
    for s, e, _ in segs: pre.append(pre[-1] + e - s)
    r = pre[-1] / sum(S)
    INF = 1e18
    best = [[INF] * (N + 1) for _ in range(K + 1)]; bk = [[0] * (N + 1) for _ in range(K + 1)]
    best[0][0] = 0.0
    for k in range(1, K + 1):
        for j in range(1, N + 1):
            for i in range(max(0, j - 10), j):
                if best[k - 1][i] >= INF: continue
                if pre[j] - pre[i] <= 0.01: continue   # morceau vide (silences collés) : pas une phrase
                c = math.log((pre[j] - pre[i]) / (r * S[k - 1])) ** 2 * 10
                if j < N: c -= 1.5 * min(segs[j - 1][2], 1.5)
                if best[k - 1][i] + c < best[k][j]:
                    best[k][j] = best[k - 1][i] + c; bk[k][j] = i
    if best[K][N] >= INF:
        raise SystemExit("Alignement impossible")
    j, fins = N, []
    for k in range(K, 0, -1):
        fins.append(j); j = bk[k][j]
    fins.reverse()
    bornes = [0.0] + [(segs[j - 1][1] + segs[j][0]) / 2 for j in fins[:-1]] + [total]
    rapport, deb = [], 0
    for k, j in enumerate(fins):
        rapport.append((pre[j] - pre[deb]) / (r * S[k])); deb = j
    return bornes, rapport
