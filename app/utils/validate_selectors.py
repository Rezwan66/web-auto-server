# app/utils/validate_selectors.py

from playwright.sync_api import sync_playwright

def validate_actions_sync(actions, url="http://localhost:5173/form"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page    = browser.new_page()
        page.goto(url)

        total, matched = len(actions), 0
        for act in actions:
            sel = act["selector"]
            try:
                page.wait_for_selector(sel, timeout=2000)
                matched += 1
            except:
                pass

        browser.close()
    return matched / total if total else 0.0
