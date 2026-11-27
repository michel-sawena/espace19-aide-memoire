"""Test de la page interactive 10. Usage : python3 test_page_10.py dossier_captures"""
import asyncio, sys
from playwright.async_api import async_playwright
URL = "file:///home/claude/espace19-aide-memoire/10-fichier-texte/index.html"
SP = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1280, "height": 900})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # 1) réussite à la souris
        await pg.click("#b-exo"); await pg.click("#demarrer"); await pg.fill("#rech", "Bloc-notes")
        await pg.click("#res"); await pg.fill("#zone", "Marie")
        await pg.click("#fichier"); await pg.click("#enr"); await pg.click("#docs")
        await pg.fill("#nom", "Courses"); await pg.click("#benr")
        print("onglet:", await pg.text_content("#onglet"))
        await pg.click("#croix"); ok1 = await pg.is_visible("#bravo"); print("réussite -> bravo:", ok1)
        await pg.screenshot(path=SP + "/p_bravo.png")
        # 1 bis) clavier : Ctrl+S et Entrée
        await pg.click("#bravo [data-act=recommencer]")
        await pg.click("#demarrer"); await pg.keyboard.type("bloc"); await pg.click("#res")
        await pg.keyboard.type("Paul"); await pg.keyboard.press("Control+s")
        await pg.click("#docs"); await pg.keyboard.type("Moi"); await pg.keyboard.press("Enter")
        await pg.click("#croix"); ok1b = await pg.is_visible("#bravo"); print("clavier -> bravo:", ok1b)
        # 2) 3 échecs
        await pg.click("#bravo [data-act=recommencer]")
        await pg.click("#ic3"); print("essais:", await pg.text_content("#essais"))                 # échec 1
        await pg.click("#demarrer"); await pg.fill("#rech", "bloc"); await pg.click("#res"); await pg.fill("#zone", "x")
        await pg.click("#croix"); print("essais:", await pg.text_content("#essais"))               # échec 2
        await pg.screenshot(path=SP + "/p_echec.png")
        await pg.click("#fichier"); await pg.click("#enr"); await pg.click("#benr")              # échec 3 -> solution
        await pg.wait_for_timeout(500); print("consigne:", await pg.text_content("#txt"))
        await pg.wait_for_timeout(2500 + 10 * 3600 + 2000 + 1500)
        ok2 = await pg.is_visible("#fin"); print("3 échecs -> solution puis fin:", ok2)
        await pg.screenshot(path=SP + "/p_fin.png")
        await pg.click("#fin [data-act=terminer]"); print("terminer:", await pg.text_content("#txt"))
        # 3) démonstration
        await pg.goto(URL); await pg.click("#b-demo"); await pg.wait_for_timeout(30000)
        print("démo texte :", repr(await pg.input_value("#zone")))
        await pg.screenshot(path=SP + "/p_demo.png")
        await pg.wait_for_timeout(35000); print("démo onglet:", await pg.text_content("#onglet"), "| fermé:", not await pg.is_visible("#np"))
        await pg.wait_for_timeout(8000); print("démo -> exercice:", await pg.text_content("#essais"))
        await pg.set_viewport_size({"width": 700, "height": 800}); await pg.wait_for_timeout(300)
        await pg.screenshot(path=SP + "/p_petit.png")
        print("erreurs JS:", errs)
        await b.close()
        assert ok1 and ok1b and ok2 and not errs
asyncio.run(main())
