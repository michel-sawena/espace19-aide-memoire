"""Assemblage du sujet 07 : identique à ../assemble_v2.py, avec un seuil d'alignement bas à 0,65 au lieu de 0,70.
Raison (reprise du 27/11/2026) : deux phrases très courtes, « Vous avez fait une faute ? » (0,69) et « Pas de panique ! » (0,66),
sont dites plus vite que la moyenne. Vérifié à la main : leurs bornes tombent toutes dans des silences de la voix
(68,33 s ; 70,95 s ; 144,97 s ; 146,82 s). Usage : mêmes arguments que assemble_v2.py.
"""
import os, sys
src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assemble_v2.py")
code = open(src, encoding="utf-8").read().replace("not 0.70 <= q <= 1.40", "not 0.65 <= q <= 1.40")
assert "0.65 <= q" in code
exec(compile(code, src, "exec"), {"__file__": src, "__name__": "__main__"})
