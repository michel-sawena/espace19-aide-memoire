"""Test de la page interactive 26 : réussite, 3 échecs → solution, démonstration, aucune erreur JavaScript.
Usage : python3 test_page_26.py chemin/vers/index.html dossier_captures"""
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
    for z in ("urgence", "lien", "code"): pg.click(f".zone[data-z='{z}']")
    assert pg.is_visible("#choix"); pg.screenshot(path=f"{out}/choix.png")
    pg.click("[data-c='supprimer']")
    assert pg.is_visible("#fin") and pg.inner_text("#fin-t") == "Bravo !"
    pg.screenshot(path=f"{out}/reussite.png"); print("réussite OK")
    # 2. trois échecs → solution animée
    pg.click("#b-re"); pg.click(".zone[data-z='bonjour']"); pg.click(".zone[data-z='colis']")
    assert "2 / 3" in pg.inner_text("#essais")
    pg.click(".zone[data-z='bonjour']")
    pg.wait_for_selector("#fin", state="visible", timeout=40000)
    assert pg.inner_text("#fin-t") == "Voici la solution"; pg.screenshot(path=f"{out}/solution.png"); print("solution OK")
    pg.click("#b-stop"); assert "terminée" in pg.inner_text("#txt")
    # 2 bis. mauvais choix de réflexe compte comme échec
    pg.goto(url); pg.click("#b-go")
    for z in ("urgence", "lien", "code"): pg.click(f".zone[data-z='{z}']")
    pg.click("[data-c='lien']"); assert "1 / 3" in pg.inner_text("#essais"); print("mauvais réflexe OK")
    # 3. démonstration
    pg.goto(url); pg.click("#b-demo"); pg.wait_for_function("document.querySelector('#txt').innerText.startsWith('Cliquez')", timeout=40000)
    assert pg.locator(".zone.trouve").count() == 0; print("démonstration OK")
    b.close()
print("erreurs JS :", errs); assert not errs
