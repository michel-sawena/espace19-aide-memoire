"""Test Playwright de la page 20 : réussite, 3 échecs -> solution, démonstration, aucune erreur JavaScript.
Usage : python3 test_page_20.py chemin/index.html"""
import sys
from playwright.sync_api import sync_playwright
URL = "file://" + __import__("os").path.abspath(sys.argv[1])
with sync_playwright() as p:
    b = p.chromium.launch(); errs = []
    def page():
        pg = b.new_page(viewport={"width": 1200, "height": 900}); pg.on("pageerror", lambda e: errs.append(str(e))); pg.goto(URL); return pg
    # 1. réussite
    pg = page(); pg.click("#b-go"); pg.click("#b-creer")
    pg.fill("#prenom", "Jeanne"); pg.fill("#nom", "Martin"); pg.fill("#adresse", "jeanne.martin@exemple.fr"); pg.click("#b-enr")
    pg.click("#b-nouveau"); pg.type("#a", "Jea"); pg.click("#prop .ligne")
    assert pg.is_visible("#fin") and pg.inner_text("#fin-t") == "Bravo !", "réussite"
    assert pg.inner_text("#puce") == "jeanne.martin@exemple.fr"
    print("réussite : OK")
    # 2. trois échecs -> solution animée
    pg = page(); pg.click("#b-go"); pg.click("#b-nouveau"); pg.click("#b-creer")
    pg.fill("#prenom", "Jeanne"); pg.fill("#nom", "Martin"); pg.fill("#adresse", "jeanne martin"); pg.click("#b-enr")
    assert "2 / 3" in pg.inner_text("#essais"), pg.inner_text("#essais")
    pg.click("#b-enr")
    pg.wait_for_selector("#fin", state="visible", timeout=60000)
    assert pg.inner_text("#fin-t") == "Voici la solution"
    print("3 échecs -> solution : OK")
    # 3. démonstration puis exercice
    pg = page(); pg.click("#b-demo"); pg.wait_for_function("document.getElementById('txt').innerText.startsWith('1.')", timeout=60000)
    print("démonstration -> exercice : OK")
    pg.screenshot(path=sys.argv[2] if len(sys.argv) > 2 else "/dev/null")
    b.close()
    print("erreurs JavaScript :", errs or "aucune")
    assert not errs
