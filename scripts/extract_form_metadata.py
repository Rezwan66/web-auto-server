import asyncio
from playwright.async_api import async_playwright
import json

async def extract_metadata():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Go to the target form page
        await page.goto('http://localhost:5173/form')

        # Wait for the form to load
        await page.wait_for_selector('form')

        # Gather all input fields
        form_elements = await page.query_selector_all('input, textarea, select')
        field_data = []
        for field in form_elements:
            tag = await field.evaluate("el => el.tagName.toLowerCase()")
            field_info = {
                "tag": tag,
                "type": await field.get_attribute("type"),
                "name": await field.get_attribute("name"),
                "id": await field.get_attribute("id")
            }
            field_data.append(field_info)

        # Gather the submit button
        submit_button = await page.query_selector('button[type="submit"], input[type="submit"]')
        submit_info = None
        if submit_button:
            tag = await submit_button.evaluate("el => el.tagName.toLowerCase()")
            submit_info = {
                "tag": tag,
                "text": await submit_button.inner_text(),
                "type": "submit",
                "id": await submit_button.get_attribute("id"),
                "name": await submit_button.get_attribute("name")
            }

        # Close the browser
        await browser.close()

        # Prepare the metadata output
        metadata = {
            "url": "http://localhost:5173/form",
            "fields": field_data,
            "submit": submit_info
        }

        print(json.dumps(metadata, indent=2))
        return metadata

# Run the async function
asyncio.run(extract_metadata())
