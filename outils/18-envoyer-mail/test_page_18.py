"""Test de la page interactive 18 : réussite, 3 échecs → solution, démonstration, aucune erreur JavaScript.
Usage : python3 test_page_18.py chemin/vers/index.html dossier_captures"""
import sys, os
from playwright.sync_api import sync_playwright
page_path, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 900})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    url = "file://" + os.path.abspath(page_path)
    # 1. réussite
    pg.goto(url); pg.click("#b-go"); pg.click("#b-nouveau")
    pg.type("#f-a", "paul@exemple.fr"); pg.click("#f-objet"); pg.type("#f-objet", "Bonjour")
    pg.click("#f-texte"); pg.type("#f-texte", "Merci !"); assert "Envoyer" in pg.inner_text("#txt")
    pg.screenshot(path=f"{out}/compose.png"); pg.click("#b-envoyer")
    pg.wait_for_selector(".mail.nonlu", timeout=5000); assert "Paul" in pg.inner_text("#txt")
    pg.screenshot(path=f"{out}/recu.png"); pg.click(".mail.nonlu")
    assert pg.is_visible("#fin") and pg.inner_text("#fin-t") == "Bravo !"
    pg.screenshot(path=f"{out}/reussite.png"); print("réussite OK")
    # 2. trois échecs → solution animée
    pg.click("#b-re"); pg.click(".mail >> nth=0")          # clique un mail au lieu de Nouveau message
    pg.click("#b-nouveau"); pg.click("#b-envoyer")         # case À vide
    pg.type("#f-a", "paul@exemple.fr"); pg.click("#b-envoyer")   # objet vide → 3e échec
    pg.wait_for_selector("#fin", state="visible", timeout=40000)
    assert pg.inner_text("#fin-t") == "Voici la solution"; pg.screenshot(path=f"{out}/solution.png"); print("solution OK")
    pg.click("#b-stop"); assert "terminée" in pg.inner_text("#txt")
    # 3. démonstration
    pg.goto(url); pg.click("#b-demo"); pg.wait_for_function("document.querySelector('#txt').innerText.startsWith('1.')", timeout=40000)
    assert pg.is_visible("#b-nouveau"); print("démonstration OK")
    b.close()
print("erreurs JS :", errs); assert not errs
