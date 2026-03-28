# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Always activate the venv before running anything:
```bash
source business-scraper-venv/bin/activate
```

## Common commands

```bash
# Generate queries (overwrites queries/queries.txt)
python generate_queries.py

# Run the full scraper pipeline
python main.py
```

## Architecture

The pipeline runs in three sequential stages from `main.py`:

1. **`scraper/getURLs.py`** — Uses async Playwright (headless Chromium) to search Google and return a list of URLs. Filters out social media, aggregators, and platforms where business contact info won't be found.

2. **`scraper/scrapeSources.py`** — Async HTTP scraper using `aiohttp`. Fetches all URLs concurrently via `asyncio.gather`. Extracts structured data (emails, phones, LinkedIn, Twitter, titles, CIF/NIF, addresses, WhatsApp) with regex. Recurses into internal links up to `MAX_DEPTH = 1`.

3. **`scraper/util/summarize.py`** — Flattens the nested output from stage 2: merges each top-level URL's fields with all its internal pages, deduplicates, and removes the `internal` key. Returns `{ url: { field: [...] } }`.

Output is written to two files:
- `scraper/otp/result.json` — raw nested scrape output
- `scraper/otp/summarize.json` — flattened, deduplicated summary

## Query generation

`generate_queries.py` combines `BUSINESS_TERMS` × `LOCATIONS` into queries like `"clínica dental Valencia"`. Edit `LOCATIONS` to target other cities. Output goes to `queries/queries.txt`, which `main.py` samples from at runtime via `get_random_query()` (controlled by `MAX_QUERIES`).

## Key dependencies

- `playwright` — must also run `playwright install chromium` after install
- `aiohttp` — async HTTP (not in pyproject.toml yet, install manually)
- `rich` — used by `scraper/util/statusMessage.py` for colored log output

## Logging

All output uses `print_log_msg(MsgType, message)` from `scraper/util/statusMessage.py`. Use `MsgType.INFO`, `SUCCESS`, `WARNING`, or `ERROR`.
