"""Test de la page interactive 15 : réussite, 3 échecs → solution, démonstration, aucune erreur JavaScript.
Usage : python3 test_page_15.py chemin/vers/index.html dossier_captures"""
import sys, os
from playwright.sync_api import sync_playwright
page_path, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 900})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    url = "file://" + os.path.abspath(page_path)
    # 1. réussite
    pg.goto(url); pg.click("#b-go")
    pg.click("#lien"); assert pg.is_visible("#panneau")
    pg.click("#image", button="right"); assert pg.is_visible("#menu"); pg.screenshot(path=f"{out}/menu.png")
    pg.click("#m-enr"); assert pg.is_visible("#dialogue"); pg.screenshot(path=f"{out}/dialogue.png")
    pg.click("#b-enr"); pg.click("#b-explo"); assert pg.is_visible("#explo")
    pg.click("#e-tel"); assert "fleur.png" in pg.inner_text("#econt") and "Programme.pdf" in pg.inner_text("#econt")
    assert pg.is_visible("#fin") and pg.inner_text("#fin-t") == "Bravo !"
    pg.screenshot(path=f"{out}/reussite.png"); print("réussite OK")
    # 2. trois échecs → solution animée
    pg.click("#b-re"); pg.click("#lien")
    pg.click("#image")                                   # clic gauche au lieu du droit
    assert "droit" in pg.inner_text("#txt")
    pg.click("#image", button="right"); pg.click("#m-enr")
    pg.click("#b-ann")                                   # Annuler au lieu d'Enregistrer
    pg.click("#b-explo")                                 # mauvais endroit → 3e échec
    pg.wait_for_selector("#fin", state="visible", timeout=60000)
    assert pg.inner_text("#fin-t") == "Voici la solution"; pg.screenshot(path=f"{out}/solution.png"); print("solution OK")
    pg.click("#b-stop"); assert "terminée" in pg.inner_text("#txt")
    # 3. démonstration
    pg.goto(url); pg.click("#b-demo"); pg.wait_for_function("document.querySelector('#txt').innerText.startsWith('1.')", timeout=60000)
    assert pg.is_visible("#lien"); print("démonstration OK")
    # 4. petit écran (téléphone) : la page s'adapte
    pg.set_viewport_size({"width": 400, "height": 800}); pg.goto(url); pg.screenshot(path=f"{out}/mobile.png")
    b.close()
print("erreurs JS :", errs); assert not errs
