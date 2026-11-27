"""Test de la page interactive 09 : réussite, 3 échecs → solution, démonstration, aucune erreur JavaScript.
Usage : python3 test_page_09.py chemin/vers/index.html dossier_captures"""
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
    pg.click(".dos[data-nom='Essai']", button="right"); pg.hover("[data-n='Renommer']")
    assert pg.is_visible("#bulle") and pg.inner_text("#bulle") == "Renommer"
    pg.screenshot(path=f"{out}/menu.png"); pg.click("[data-n='Renommer']")
    pg.fill("#saisie", "Vacances"); pg.press("#saisie", "Enter")
    assert pg.locator(".dos[data-nom='Vacances']").count() == 1
    pg.click(".dos[data-nom='Vacances']", button="right"); pg.click("[data-n='Supprimer']")
    assert pg.is_visible("#fin") and pg.inner_text("#fin-t") == "Bravo !"; assert pg.locator(".dos[data-nom='Vacances']").count() == 0
    pg.screenshot(path=f"{out}/reussite.png"); print("réussite OK")
    # 2. trois échecs → solution animée
    pg.click("#b-re"); pg.click(".dos[data-nom='Essai']")                 # clic gauche au lieu du droit
    pg.click(".dos[data-nom='Courrier']", button="right")                   # mauvais dossier
    pg.click(".dos[data-nom='Essai']", button="right"); pg.click("[data-n='Copier']")   # mauvaise image → 3e échec
    pg.wait_for_selector("#fin", state="visible", timeout=40000)
    assert pg.inner_text("#fin-t") == "Voici la solution"; pg.screenshot(path=f"{out}/solution.png"); print("solution OK")
    pg.click("#b-stop"); assert "terminée" in pg.inner_text("#txt")
    # 3. démonstration
    pg.goto(url); pg.click("#b-demo"); pg.wait_for_function("document.querySelector('#txt').innerText.startsWith('1.')", timeout=40000)
    assert pg.locator(".dos[data-nom='Essai']").count() == 1; print("démonstration OK")
    b.close()
print("erreurs JS :", errs); assert not errs
