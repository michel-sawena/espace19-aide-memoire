import asyncio, sys
from playwright.async_api import async_playwright
URL = "file:///home/claude/espace19-aide-memoire/02-allumer-eteindre/index.html"
SP = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":1280,"height":900})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # 1) réussite
        await pg.click("#b-exo")
        await pg.click("#demarrer"); await pg.click("#marche"); await pg.click("#arreter")
        await pg.wait_for_timeout(2800)
        assert await pg.is_visible("#noir"), "écran noir attendu"
        await pg.click("#bouton"); await pg.wait_for_timeout(3300)
        ok1 = await pg.is_visible("#bravo"); print("réussite -> bravo:", ok1)
        await pg.screenshot(path=SP + "/p_bravo.png")
        # 2) 3 échecs
        await pg.click("#bravo [data-act=recommencer]")
        await pg.click("#bouton")                                   # échec 1 : bouton pour éteindre
        print("essais:", await pg.text_content("#essais"))
        await pg.click("#demarrer"); await pg.click("#marche"); await pg.click("#redemarrer")   # échec 2
        print("essais:", await pg.text_content("#essais"))
        await pg.click("#bouton")                                   # échec 3 -> solution
        await pg.wait_for_timeout(500)
        print("consigne:", await pg.text_content("#txt"))
        await pg.wait_for_timeout(2500 + 3600*2 + 6000*2 + 500)
        ok2 = await pg.is_visible("#fin"); print("3 échecs -> solution puis fin:", ok2)
        await pg.screenshot(path=SP + "/p_fin.png")
        await pg.click("#fin [data-act=terminer]"); print("terminer:", await pg.text_content("#txt"))
        # 3) démonstration (début)
        await pg.goto(URL); await pg.click("#b-demo"); await pg.wait_for_timeout(4000)
        print("démo menu ouvert:", await pg.is_visible("#menu"))
        await pg.screenshot(path=SP + "/p_demo.png")
        # 4) petit écran
        await pg.set_viewport_size({"width":700,"height":800}); await pg.wait_for_timeout(300)
        print("erreurs JS:", errs)
        await b.close()
        assert ok1 and ok2 and not errs
asyncio.run(main())
