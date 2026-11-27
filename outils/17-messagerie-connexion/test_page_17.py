"""Test de la page interactive 17 : réussite, 3 échecs → solution, démonstration, aucune erreur JavaScript.
Usage : python3 test_page_17.py chemin/vers/index.html dossier_captures"""
import sys, os
from playwright.sync_api import sync_playwright
page_path, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 900})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
    url = "file://" + os.path.abspath(page_path)
    # 1. réussite (bouton bleu pour l'adresse, touche Entrée pour le mot de passe)
    pg.goto(url); pg.click("#b-go")
    pg.click("#champ"); pg.fill("#champ", "Jean@exemple.fr "); pg.click("#suite")
    assert pg.is_visible("#pill") and pg.get_attribute("#champ", "type") == "password"
    pg.fill("#champ", "soleil"); pg.press("#champ", "Enter")
    assert pg.is_visible("#p-boite"); pg.screenshot(path=f"{out}/boite.png")
    pg.click("#rond"); assert pg.is_visible("#deco"); pg.screenshot(path=f"{out}/menu.png")
    pg.click("#deco")
    assert pg.is_visible("#fin") and pg.inner_text("#fin-t") == "Bravo !" and pg.is_visible("#p-cx")
    pg.screenshot(path=f"{out}/reussite.png"); print("réussite OK")
    # 2. trois échecs → solution animée
    pg.click("#b-re")
    pg.fill("#champ", "jean@exemple.com"); pg.click("#suite")          # mauvaise adresse
    assert "Essais manqués : 1 / 3" in pg.inner_text("#essais")
    pg.fill("#champ", "jean@exemple.fr"); pg.click("#suite")
    pg.fill("#champ", "Soleil"); pg.click("#suite")                     # mauvais mot de passe
    pg.fill("#champ", "soleil"); pg.click("#suite")
    pg.click(".msg >> nth=1")                                           # clic à côté du rond → 3e échec
    pg.wait_for_selector("#fin", state="visible", timeout=40000)
    assert pg.inner_text("#fin-t") == "Voici la solution"; pg.screenshot(path=f"{out}/solution.png"); print("solution OK")
    pg.click("#b-stop"); assert "terminée" in pg.inner_text("#txt")
    # 3. démonstration
    pg.goto(url); pg.click("#b-demo")
    pg.wait_for_function("document.querySelector('#txt').innerText.startsWith('1.')", timeout=40000)
    assert pg.is_visible("#p-cx"); print("démonstration OK")
    b.close()
print("erreurs JS :", errs); assert not errs
