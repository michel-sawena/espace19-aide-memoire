"""Test Playwright de la page 14 : réussite, 3 échecs -> solution, démonstration, aucune erreur JavaScript."""
import sys, os
from playwright.sync_api import sync_playwright
URL = "file://" + os.path.abspath(sys.argv[1]); SHOT = sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 900}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL); pg.click("#b-exo")
    for i in ("#etoile", "#b-valider", "#points", "#mi-favoris", "#fav-google"):
        pg.click(i); pg.wait_for_timeout(150)
    pg.wait_for_timeout(1500); ok = pg.is_visible("#bravo"); pg.screenshot(path=SHOT + "_reussite.png")
    pg.click("#bravo [data-act=recommencer]")
    for i in range(3): pg.click("#croix"); pg.wait_for_timeout(100)
    pg.wait_for_timeout(300); essais = pg.inner_text("#essais")
    pg.wait_for_timeout(22000); fin = pg.is_visible("#fin"); pg.screenshot(path=SHOT + "_solution.png")
    pg.click("#fin [data-act=terminer]")
    pg.reload(); pg.click("#b-demo"); pg.wait_for_timeout(9000); pg.screenshot(path=SHOT + "_demo.png")
    demo_dlg = pg.inner_text("#essais")
    pg.wait_for_timeout(32000); exo = pg.inner_text("#essais")
    print({"reussite": ok, "apres_3_echecs": essais, "solution_affichee": fin, "demo": demo_dlg, "apres_demo": exo, "erreurs_js": errs})
    b.close()
