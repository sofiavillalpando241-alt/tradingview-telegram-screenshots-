import asyncio
import os
from playwright.async_api import async_playwright
import httpx
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHART_URL = os.getenv("CHART_URL")

async def screenshot_and_send():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1920, "height": 1080})
            await page.goto(CHART_URL, wait_until="networkidle")
            await page.wait_for_timeout(3000)
            screenshot = await page.screenshot()
            await browser.close()
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                data={"chat_id": CHAT_ID, "caption": f"Chart update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"},
                files={"photo": ("chart.png", screenshot, "image/png")}
            )
        print(f"✅ Screenshot enviado — {datetime.now()}")
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    print("🚀 Bot iniciado — enviará screenshot cada 30 minutos")
    while True:
        await screenshot_and_send()
        await asyncio.sleep(300)

asyncio.run(main())
