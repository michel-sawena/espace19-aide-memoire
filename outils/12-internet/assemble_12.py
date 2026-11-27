"""Assemblage du sujet 12 : identique à ../assemble_v2.py, avec un seul ajustement du comptage
de syllabes pour les noms anglais de navigateurs (« Google Chrome » se prononce « gou-gueul crôme »,
4 syllabes, alors que la règle française en compte 2 et signalait à tort la phrase comme douteuse).
Vérifié le 27/11/2026 : la phrase est bornée par deux vraies pauses de la voix (84,8 s et 86,0 s).
Usage : python3 assemble_12.py script_12.json 12.mp3 sortie.mp4 render_12.py
"""
import os, re, runpy, sys

OUTILS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, OUTILS)
import aligne as A

_orig = A.syllabes
def syllabes(t):
    t = re.sub(r"(?i)google chrome", "gou gueul crô me", t)
    return _orig(t)
A.syllabes = syllabes

sys.argv = [os.path.join(OUTILS, "assemble_v2.py")] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
