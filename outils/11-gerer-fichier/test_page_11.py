"""Test de la page interactive 11. Usage : python3 test_page_11.py dossier_captures"""
import asyncio, sys
from playwright.async_api import async_playwright
URL = "file:///home/claude/espace19-aide-memoire/11-gerer-fichier/index.html"
SP = sys.argv[1]
async def glisser(pg, src, dst):
    a = await pg.locator(src).bounding_box(); b = await pg.locator(dst).bounding_box()
    await pg.mouse.move(a["x"] + a["width"] / 2, a["y"] + a["height"] / 2); await pg.mouse.down()
    for k in range(1, 11): await pg.mouse.move(a["x"] + a["width"] / 2 + (b["x"] - a["x"]) * k / 10, a["y"] + a["height"] / 2 + (b["y"] - a["y"]) * k / 10)
    await pg.mouse.up()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1280, "height": 900})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # 1) réussite complète
        await pg.click("#b-exo")
        await pg.click("#it-Courses", button="right"); await pg.click("#ctx [data-a=Renommer]")
        await pg.fill("#nom", "Liste de courses"); await pg.press("#nom", "Enter")
        await glisser(pg, "#it-Liste_de_courses", "#it-Famille")
        assert await pg.locator("#it-Liste_de_courses").count() == 0
        await pg.click("#it-Photo", button="right"); await pg.hover("#ctx [data-a=Supprimer]")
        tip = await pg.is_visible("#ctx [data-a=Supprimer] .tip"); await pg.click("#ctx [data-a=Supprimer]")
        await pg.dblclick("#corbeille"); print("vue:", await pg.text_content("#vue"))
        await pg.click("#it-Photo", button="right"); await pg.click("#restaurer")
        ok1 = await pg.is_visible("#bravo"); print("réussite -> bravo:", ok1, "| nom visible au survol:", tip)
        await pg.screenshot(path=SP + "/p_bravo.png")
        # 2) 3 échecs -> solution animée -> fin
        await pg.click("#bravo [data-act=recommencer]")
        await pg.click("#it-Photo", button="right"); print("essais:", await pg.text_content("#essais"))   # échec 1
        await pg.click("#it-Courses", button="right"); await pg.click("#ctx [data-a=Copier]"); print("essais:", await pg.text_content("#essais"))  # échec 2
        await pg.screenshot(path=SP + "/p_echec.png")
        await pg.click("#it-Courses", button="right"); await pg.click("#ctx [data-a=Supprimer]")   # échec 3
        await pg.wait_for_timeout(500); print("consigne:", await pg.text_content("#txt"))
        await pg.wait_for_function("document.getElementById('fin').style.display === 'flex'", timeout=90000)
        print("3 échecs -> solution puis fin: True"); await pg.screenshot(path=SP + "/p_fin.png")
        await pg.click("#fin [data-act=terminer]"); print("terminer:", await pg.text_content("#txt"))
        # 3) démonstration jusqu'à l'exercice
        await pg.goto(URL); await pg.click("#b-demo"); await pg.wait_for_timeout(9000)
        await pg.screenshot(path=SP + "/p_demo.png")
        await pg.wait_for_function("document.getElementById('essais').textContent.startsWith('Essais')", timeout=90000)
        print("démo -> exercice:", await pg.text_content("#essais"))
        await pg.set_viewport_size({"width": 700, "height": 800}); await pg.wait_for_timeout(300); await pg.screenshot(path=SP + "/p_petit.png")
        print("erreurs JS:", errs)
        await b.close()
        assert ok1 and tip and not errs
asyncio.run(main())
