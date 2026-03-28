import random
import asyncio
import json

from scraper.getURLs import get_urls
from scraper.scrapeSources import scrape_url
from scraper.util.statusMessage import print_log_msg, MsgType
from scraper.util.summarize import summarize

MAX_QUERIES = 34

def get_random_query(filepath, max = 10):

    with open(filepath) as file:

        lines = file.readlines()

    queries = set()

    while len(queries) < min(max, len(lines)):

        queries.add(random.choice(lines))

    return list(queries)

async def main():

    filepath = "queries/queries.txt"

    queries = get_random_query(filepath, MAX_QUERIES)

    print_log_msg(MsgType.INFO, f"Running {len(queries)} queries...")

    combined_dict = {}

    for query in queries:

        print_log_msg(MsgType.INFO, f"Query: {query.strip()}")

        url_list = await get_urls(query)

        result = await scrape_url(url_list, depth=0)

        combined_dict.update(result)

    print_log_msg(MsgType.SUCCESS, f"Done. Scraped {len(combined_dict)} source(s) across {len(queries)} queries.")

    summary = summarize(combined_dict)

    try:

        with open("scraper/otp/result.json", "w", encoding = "UTF-8") as file:

            json.dump(combined_dict, file, ensure_ascii = False, indent = 4)

            print_log_msg(MsgType.SUCCESS, "Data succesfully written to JSON.")

    except Exception as error:

        print_log_msg(MsgType.ERROR, f"There has been an error while processing the file: {error}")

    try:

        with open("scraper/otp/summarize.json", "w", encoding = "UTF-8") as file_2:

            json.dump(summary, file_2, ensure_ascii = False, indent = 4)

            print_log_msg(MsgType.SUCCESS, "Data succesfully written to example JSON.")

    except Exception as error:

        print_log_msg(MsgType.ERROR, f"There has been an error while processing the file: {error}")

if __name__ == "__main__":

    asyncio.run(main())
