"""Test de la page interactive 03. Usage : python3 test_page_03.py dossier_captures"""
import asyncio, sys
from playwright.async_api import async_playwright
URL = "file:///home/claude/espace19-aide-memoire/03-session-bureau/index.html"
SP = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":900})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # 1) réussite (clic, code, Entrée, Démarrer, Démarrer)
        await pg.click("#b-exo")
        await pg.click("#verrou")
        assert await pg.is_visible("#connexion")
        await pg.fill("#code", "1234"); await pg.press("#code", "Enter")
        await pg.click("#demarrer"); assert await pg.is_visible("#menu")
        await pg.click("#demarrer")
        ok1 = await pg.is_visible("#bravo"); print("réussite -> bravo:", ok1)
        await pg.screenshot(path=SP + "/p_bravo.png")
        # 1 bis) ouverture au clavier + fermeture par clic sur le bureau
        await pg.click("#bravo [data-act=recommencer]")
        await pg.keyboard.press("a"); assert await pg.is_visible("#connexion")
        await pg.fill("#code", "1234"); await pg.click("#ok")
        await pg.click("#demarrer"); await pg.mouse.click(250, 650)
        ok1b = await pg.is_visible("#bravo"); print("touche + clic bureau -> bravo:", ok1b)
        # 2) 3 échecs
        await pg.click("#bravo [data-act=recommencer]")
        await pg.click("#verrou")
        await pg.fill("#code", "9999"); await pg.press("#code", "Enter")          # échec 1
        print("essais:", await pg.text_content("#essais"))
        await pg.fill("#code", "1234"); await pg.press("#code", "Enter")
        await pg.click("#corbeille")                                               # échec 2
        print("essais:", await pg.text_content("#essais"))
        await pg.screenshot(path=SP + "/p_echec.png")
        await pg.click("#loupe")                                                   # échec 3 -> solution
        await pg.wait_for_timeout(500); print("consigne:", await pg.text_content("#txt"))
        await pg.wait_for_timeout(2500 + 3800 + 6000 + 4500 + 4500 + 800)
        ok2 = await pg.is_visible("#fin"); print("3 échecs -> solution puis fin:", ok2)
        await pg.screenshot(path=SP + "/p_fin.png")
        await pg.click("#fin [data-act=terminer]"); print("terminer:", await pg.text_content("#txt"))
        # 3) démonstration
        await pg.goto(URL); await pg.click("#b-demo"); await pg.wait_for_timeout(13500)
        print("démo : code tapé =", await pg.input_value("#code"), "| bureau:", not await pg.is_visible("#connexion"))
        await pg.wait_for_timeout(11000); print("démo menu ouvert:", await pg.is_visible("#menu"))
        await pg.screenshot(path=SP + "/p_demo.png")
        await pg.wait_for_timeout(14000); print("démo -> exercice:", await pg.text_content("#essais"))
        await pg.set_viewport_size({"width":700,"height":800}); await pg.wait_for_timeout(300)
        await pg.screenshot(path=SP + "/p_petit.png")
        print("erreurs JS:", errs)
        await b.close()
        assert ok1 and ok1b and ok2 and not errs
asyncio.run(main())
