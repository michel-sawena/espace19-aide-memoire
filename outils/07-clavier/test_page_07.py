"""Test de la page interactive 07. Usage : python3 test_page_07.py dossier_captures"""
import asyncio, sys
from playwright.async_api import async_playwright
URL = "file:///home/claude/espace19-aide-memoire/07-clavier/index.html"
SP = sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1280, "height": 1000})
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # 1) démonstration
        await pg.click("#b-demo"); await pg.wait_for_timeout(800); await pg.screenshot(path=f"{SP}/p07_demo.png")
        await pg.wait_for_timeout(18000)
        assert (await pg.text_content("#texte")) == "Paul 19", await pg.text_content("#texte")
        # 2) réussite avec le vrai clavier
        await pg.click("#b-exo"); await pg.keyboard.type("Paul 19"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(900)
        assert await pg.is_visible("#bravo"); await pg.screenshot(path=f"{SP}/p07_bravo.png")
        # 3) réussite à la souris (clavier à l'écran)
        await pg.click("#b-rec")
        for k in ["maj", "P", "A", "U", "L", "space", "maj", "k1", "maj", "k9", "enter"]:
            await pg.click(f'.t[data-id="{k}"]')
        await pg.wait_for_timeout(900); assert await pg.is_visible("#bravo")
        # 4) trois échecs -> solution
        await pg.click("#b-rec")
        await pg.keyboard.type("paul 19"); await pg.keyboard.press("Enter")
        m1 = await pg.text_content("#message"); await pg.screenshot(path=f"{SP}/p07_echec.png")
        for _ in range(7): await pg.keyboard.press("Backspace")
        await pg.keyboard.type("Paul19"); await pg.keyboard.press("Enter"); m2 = await pg.text_content("#message")
        await pg.keyboard.type("x"); await pg.keyboard.press("Enter")
        assert await pg.is_visible("#fin")
        await pg.click("#b-sol"); await pg.wait_for_timeout(18000)
        assert (await pg.text_content("#texte")) == "Paul 19"
        await pg.screenshot(path=f"{SP}/p07_solution.png")
        # 5) téléphone
        m = await b.new_page(viewport={"width": 390, "height": 844}); await m.goto(URL); await m.screenshot(path=f"{SP}/p07_mobile.png")
        sw = await m.evaluate("document.documentElement.scrollWidth")
        print("messages:", m1, "|", m2); print("largeur mobile", sw); print("erreurs JS:", errs)
        await b.close()
asyncio.run(main())
