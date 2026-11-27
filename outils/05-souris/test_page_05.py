"""Test de la page interactive 05. Usage : python3 test_page_05.py dossier_captures"""
import asyncio, sys
from playwright.async_api import async_playwright
URL = "file:///home/claude/espace19-aide-memoire/05-souris-clics/index.html"
SP = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":900})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # 1) réussite : clic, double-clic, croix
        await pg.click("#b-exo")
        await pg.click("#photos"); assert "sel" in await pg.get_attribute("#photos", "class")
        await pg.dblclick("#photos"); assert await pg.is_visible("#fen")
        await pg.click("#croix")
        ok1 = await pg.is_visible("#bravo") and not await pg.is_visible("#fen"); print("réussite -> bravo:", ok1)
        await pg.screenshot(path=SP + "/p_bravo.png")
        # 1 bis) double-clic direct
        await pg.click("#bravo [data-act=recommencer]")
        await pg.dblclick("#photos"); await pg.click("#croix")
        ok1b = await pg.is_visible("#bravo"); print("double-clic direct -> bravo:", ok1b)
        # 2) 3 échecs
        await pg.click("#bravo [data-act=recommencer]")
        await pg.click("#corbeille"); print("essais:", await pg.text_content("#essais"))   # échec 1
        await pg.click("#photos"); await pg.click("#bloc"); print("essais:", await pg.text_content("#essais"))  # échec 2
        await pg.screenshot(path=SP + "/p_echec.png")
        await pg.dblclick("#photos"); await pg.click("#fen .photos")                         # échec 3 -> solution
        await pg.wait_for_timeout(500); print("consigne:", await pg.text_content("#txt"))
        await pg.wait_for_timeout(2500 + 3 * 4500 + 800)
        ok2 = await pg.is_visible("#fin"); print("3 échecs -> solution puis fin:", ok2)
        await pg.screenshot(path=SP + "/p_fin.png")
        await pg.click("#fin [data-act=terminer]"); print("terminer:", await pg.text_content("#txt"))
        # 3) démonstration
        await pg.goto(URL); await pg.click("#b-demo"); await pg.wait_for_timeout(9000)
        print("démo : Photos choisi :", "sel" in await pg.get_attribute("#photos", "class"))
        await pg.wait_for_timeout(5000); print("démo fenêtre ouverte:", await pg.is_visible("#fen"))
        await pg.screenshot(path=SP + "/p_demo.png")
        await pg.wait_for_timeout(12000); print("démo -> exercice:", await pg.text_content("#essais"), "| fenêtre fermée:", not await pg.is_visible("#fen"))
        await pg.set_viewport_size({"width":700,"height":800}); await pg.wait_for_timeout(300)
        await pg.screenshot(path=SP + "/p_petit.png")
        print("erreurs JS:", errs)
        await b.close()
        assert ok1 and ok1b and ok2 and not errs
asyncio.run(main())
