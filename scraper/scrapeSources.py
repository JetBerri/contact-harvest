import re
import asyncio
import aiohttp

from scraper.util.statusMessage import print_log_msg, MsgType

MAX_DEPTH = 1

async def _scrape_single(session, url, depth):

    try:

        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as res:

            if res.status >= 400:
          
                print_log_msg(MsgType.ERROR, f"Unreachable ({res.status}): {url}")
          
                return None

            body = await res.text()

    except aiohttp.ClientConnectorError:
       
        print_log_msg(MsgType.ERROR, f"DNS / connection error: {url}")
       
        return None

    except asyncio.TimeoutError:
       
        print_log_msg(MsgType.ERROR, f"Timeout: {url}")
       
        return None

    except Exception as e:
       
        print_log_msg(MsgType.ERROR, f"Request error {url}: {e}")
       
        return None

    data = {
       
        "url":       url,
        "emails":    [e for e in re.findall(r'[\w\.-]+@[\w\.-]+\.\w{2,}', body)
                      if not re.search(r'\.(png|jpg|jpeg|gif|svg|webp|pdf|zip|js|css|xml|json)$', e, re.IGNORECASE)],
        "linkedins": re.findall(r'linkedin\.com/in/[\w\-]+', body),
        "twitters":  re.findall(r'twitter\.com/[\w]+|x\.com/[\w]+', body),
        "titles":    re.findall(r'\b(CEO|CTO|CFO|COO|Director|Manager|Founder|Co-Founder|VP|Head of [\w]+)\b', body, re.IGNORECASE),
        "cif":       re.findall(r'\b[A-HJNP-SUVW]\d{7}[0-9A-J]\b', body),
        "nif":       re.findall(r'\b\d{8}[A-Z]\b', body),
        "addresses": re.findall(r'\b(Calle|Av\.|Avenida|Plaza|C\/|Street|St\.|Avenue|Blvd)[\w\s\.,º]+\d{4,5}\b', body, re.IGNORECASE),
        "whatsapps": re.findall(r'wa\.me/[\d]+|whatsapp\.com/[\w/]+', body),
    
    }

    print_log_msg(MsgType.SUCCESS, f"Scraped: {url}")

    if depth < MAX_DEPTH:

        hrefs = re.findall(r'href="(https?://[^"]+)"', body)
    
        internal_url_list = list(dict.fromkeys(hrefs))  # deduplicate preserving order
    
        data["internal"] = await scrape_url(internal_url_list, depth=depth + 1)

    else:

        data["internal"] = {}

    return data


async def scrape_url(url_list, depth=0):

    if depth > MAX_DEPTH or not url_list:
    
        return {}

    print_log_msg(MsgType.INFO, f"Scraping {len(url_list)} URL(s) at depth {depth}")

    async with aiohttp.ClientSession() as session:

        tasks = [_scrape_single(session, url, depth) for url in url_list]
        results_list = await asyncio.gather(*tasks)

    return {data["url"]: data for data in results_list if data is not None}
