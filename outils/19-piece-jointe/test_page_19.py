"""Test de la page interactive 19 : réussite, 3 échecs → solution, démonstration, aucune erreur JavaScript.
Usage : python3 test_page_19.py chemin/vers/index.html dossier_captures"""
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
    pg.click("#b-nouveau"); pg.click("#b-trom"); pg.screenshot(path=f"{out}/dialogue.png")
    pg.dblclick(".fic[data-f='photo']"); assert pg.is_visible("#puce")
    pg.click("#b-env"); assert pg.locator(".ligne[data-obj='Ma photo']").count() == 1
    pg.click(".ligne[data-obj='Ma photo']"); pg.click("#vign"); assert pg.is_visible("#grand")
    pg.wait_for_selector("#fin", state="visible", timeout=5000)
    assert pg.inner_text("#fin-t") == "Bravo !"; pg.screenshot(path=f"{out}/reussite.png"); print("réussite OK")
    # 2. trois échecs → solution animée
    pg.click("#b-re"); pg.click("#b-nouveau")
    pg.click("#b-env")                                   # envoyer sans pièce jointe
    pg.click("#b-trom"); pg.dblclick(".fic[data-f='facture']")   # mauvais document
    pg.dblclick(".fic[data-f='lettre']")                 # 3e échec
    pg.wait_for_selector("#fin", state="visible", timeout=40000)
    assert pg.inner_text("#fin-t") == "Voici la solution"; pg.screenshot(path=f"{out}/solution.png"); print("solution OK")
    pg.click("#b-stop"); assert "terminée" in pg.inner_text("#txt")
    # 3. démonstration
    pg.goto(url); pg.click("#b-demo"); pg.wait_for_function("document.querySelector('#txt').innerText.startsWith('1.')", timeout=40000)
    assert not pg.is_visible("#compo"); print("démonstration OK")
    b.close()
print("erreurs JS :", errs); assert not errs
