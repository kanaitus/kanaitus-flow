import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:8501")
        try:
            await page.wait_for_selector('[data-testid="stToggle"]', timeout=10000)
            element = await page.locator('[data-testid="stToggle"]').first.element_handle()
            html = await element.evaluate("el => el.outerHTML")
            print("--- HTML START ---")
            print(html)
            print("--- HTML END ---")
        except Exception as e:
            print("Error:", e)
        finally:
            await browser.close()

asyncio.run(main())
