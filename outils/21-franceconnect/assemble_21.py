"""Lance ../assemble_v2.py en corrigeant le compte de syllabes de ../aligne.py pour deux voyelles accentuées
qui se suivent (« créé » = cré-é, 2 syllabes ; aligne.py en comptait 1, d'où un rapport douteux à 1,47 sur
« Votre compte est créé. »). Les outils communs ne sont pas modifiés (règle des séances parallèles).
Usage : identique à assemble_v2.py."""
import os, re, runpy, sys
ICI = os.path.dirname(os.path.abspath(__file__)); HAUT = os.path.join(ICI, "..")
sys.path.insert(0, HAUT)
import aligne
_orig = aligne.syllabes
def syllabes(t):
    return _orig(re.sub(r"([éè])([éeè])", r"\1-\2", t.lower()))
aligne.syllabes = syllabes
sys.argv = [os.path.join(HAUT, "assemble_v2.py")] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
