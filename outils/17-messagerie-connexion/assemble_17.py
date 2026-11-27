"""Lance ../assemble_v2.py pour le sujet 17, avec un compte de syllabes corrigé pour deux noms
prononcés à l'anglaise : « Gmail » (dji-mèl, 2 syllabes) et « google » (gou-gueul, 2 syllabes).
Sans cette correction, la phrase « Pour Gmail : mail point google point com. » sortait de la plage
de contrôle (rapport 1,58). ../aligne.py n'est pas modifié (outil commun aux autres sujets).
Usage : python3 assemble_17.py script_17.json 17.mp3 sortie.mp4 render_17.py
"""
import os, re, runpy, sys
ICI = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ICI, "..")
sys.path.insert(0, OUT)
import aligne
_orig = aligne.syllabes
def syllabes(t):
    t = re.sub(r"(?i)gmail", " dji mel ", t); t = re.sub(r"(?i)google", " gou gueul ", t)
    return _orig(t)
aligne.syllabes = syllabes
sys.argv = [os.path.join(OUT, "assemble_v2.py")] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
