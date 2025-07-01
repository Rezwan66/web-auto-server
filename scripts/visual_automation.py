# scripts/visual_automation.py

import sys, json, asyncio
from playwright.async_api import async_playwright

async def run(actions_payload):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page    = await browser.new_page()
        await page.goto(actions_payload["url"])
        for act in actions_payload["actions"]:
            typ, sel, val = act["type"], act["selector"], act.get("value")
            await page.wait_for_selector(sel, timeout=5000)
            if typ == "fill":
                await page.fill(sel, val)
            elif typ == "click":
                await page.click(sel)
            await page.wait_for_timeout(500)  # so you can see each step
        await asyncio.Future()  # keep browser open

if __name__ == "__main__":
    payload = json.load(sys.stdin)
    asyncio.run(run(payload))
