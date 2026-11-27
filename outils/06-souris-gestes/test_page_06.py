"""Test de la page interactive 06. Usage : python3 test_page_06.py dossier_captures"""
import asyncio, sys
from playwright.async_api import async_playwright
URL = "file:///home/claude/espace19-aide-memoire/06-souris-gestes/index.html"
SP = sys.argv[1]

async def centre(pg, sel):
    b = await pg.locator(sel).bounding_box(); return b["x"] + b["width"] / 2, b["y"] + b["height"] / 2

async def glisser(pg, cible="#rangement", lacher_avant=False):
    x, y = await centre(pg, "#lettre"); await pg.mouse.move(x, y); await pg.mouse.down()
    tx, ty = await centre(pg, cible)
    if lacher_avant: tx, ty = x + 300, y + 40
    for k in range(1, 11): await pg.mouse.move(x + (tx - x) * k / 10, y + (ty - y) * k / 10)
    await pg.mouse.up()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1280, "height": 900})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # 1) réussite complète
        await pg.click("#b-exo")
        await glisser(pg); assert not await pg.is_visible("#lettre"); print("1 glisser :", await pg.text_content("#txt"))
        await pg.click("#carre"); assert "max" in await pg.get_attribute("#fen", "class"); print("2 agrandir ok")
        x, y = await centre(pg, "#texte"); await pg.mouse.move(x, y)
        for _ in range(30): await pg.mouse.wheel(0, 300); await pg.wait_for_timeout(40)
        await pg.wait_for_timeout(300); print("3 molette :", await pg.text_content("#txt"))
        await pg.click("#carre"); assert "max" not in await pg.get_attribute("#fen", "class"); print("4 taille rendue")
        await pg.mouse.click(150, 600, button="right"); assert await pg.is_visible("#menuctx"); print("5 clic droit : menu ouvert")
        await pg.screenshot(path=SP + "/p_menu.png")
        await pg.mouse.click(1100, 700); ok1 = await pg.is_visible("#bravo"); print("6 clic à côté -> bravo:", ok1)
        await pg.screenshot(path=SP + "/p_bravo.png")
        # 2) 3 échecs -> solution
        await pg.click("#bravo [data-act=recommencer]")
        await glisser(pg, lacher_avant=True); print("essais:", await pg.text_content("#essais"))      # échec 1
        await glisser(pg)
        await pg.click("#croix"); print("essais:", await pg.text_content("#essais"))                   # échec 2
        await pg.screenshot(path=SP + "/p_echec.png")
        await pg.click("#trait")                                                                     # échec 3
        await pg.wait_for_timeout(500); print("consigne:", await pg.text_content("#txt"))
        await pg.wait_for_timeout(30000)
        ok2 = await pg.is_visible("#fin"); print("3 échecs -> solution puis fin:", ok2)
        await pg.screenshot(path=SP + "/p_fin.png")
        await pg.click("#fin [data-act=terminer]"); print("terminer:", await pg.text_content("#txt"))
        # 3) démonstration
        await pg.goto(URL); await pg.click("#b-demo"); await pg.wait_for_timeout(9000)
        print("démo : icône rangée =", not await pg.is_visible("#lettre"))
        await pg.wait_for_timeout(5000); print("démo agrandie =", "max" in await pg.get_attribute("#fen", "class"))
        await pg.screenshot(path=SP + "/p_demo.png")
        await pg.wait_for_timeout(36000); print("démo -> exercice:", await pg.text_content("#essais"))
        await pg.set_viewport_size({"width": 700, "height": 800}); await pg.wait_for_timeout(300)
        # le glisser fonctionne aussi à petite échelle
        await glisser(pg); ok3 = not await pg.is_visible("#lettre"); print("petit écran, glisser ok:", ok3)
        await pg.screenshot(path=SP + "/p_petit.png")
        print("erreurs JS:", errs)
        await b.close()
        assert ok1 and ok2 and ok3 and not errs
asyncio.run(main())
