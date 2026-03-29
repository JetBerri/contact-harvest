from playwright.async_api import async_playwright
from scraper.util.statusMessage import print_log_msg, MsgType

async def get_urls(query = "example"):

    print_log_msg(MsgType.INFO, f"Searching Google for: {query.strip()}")

    async with async_playwright() as p:

        browser = await p.chromium.launch(
          
            headless = True,
          
            args = ["--disable-blink-features=AutomationControlled"]
        
        )

        context = await browser.new_context(
        
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        
        )

        page = await context.new_page()

        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        await page.goto(f"https://www.google.com/search?q={query}")

        await page.wait_for_load_state("networkidle")

        anchors = await page.query_selector_all("a[href]")

        hrefs = [await a.get_attribute("href") for a in anchors]

        await browser.close()

    excluded = (
        "google", "youtube.com", "googleusercontent.com",
        "instagram.com", "x.com", "twitter.com",
        "microsoft.com", "wikipedia.org", "wikipedia.com",
        "facebook.com", "tiktok.com", "linkedin.com",
        "amazon.com", "amazon.es", "ebay.com", "ebay.es",
        "tripadvisor.com", "tripadvisor.es", "yelp.com",
        "apple.com", "maps.google",
    )

    url_list = list(dict.fromkeys([

        href for href in hrefs

        if href and href.startswith("http")

        and not any(d in href for d in excluded)

    ]))

    print_log_msg(MsgType.SUCCESS, f"Found {len(url_list)} URLs")

    return url_list
