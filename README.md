# contact-harvest

**Automated pipeline that turns Google searches into structured business contact data.**

Given a list of search queries, contact-harvest finds business websites, scrapes them concurrently, and extracts emails, LinkedIn profiles, phone numbers, WhatsApp links, job titles, and Spanish tax IDs (CIF/NIF) — outputting clean, deduplicated JSON ready for outreach.

---

## How it works

The pipeline runs three sequential stages:

```
Google Search (Playwright)
        ↓
  URL list (filtered)
        ↓
Concurrent HTTP scraping (aiohttp)
  + internal link recursion (depth=1)
        ↓
  Raw nested JSON  →  result.json
        ↓
  Flatten + deduplicate
        ↓
  Clean flat JSON  →  summarize.json
```

1. **URL Discovery** (`scraper/getURLs.py`) — Launches a headless Chromium browser, searches Google, and returns a filtered list of actual business URLs. Social media, aggregators, and platforms (LinkedIn, Instagram, TikTok, Yelp, etc.) are excluded automatically.

2. **Scraping** (`scraper/scrapeSources.py`) — Fetches all URLs concurrently using `aiohttp`. Extracts structured data via regex from each page body, then follows internal links one level deep (`MAX_DEPTH = 1`).

3. **Summarization** (`scraper/util/summarize.py`) — Merges each site's top-level fields with its internal pages, deduplicates, and removes the nested structure.

---

## Output

Two JSON files are written after each run:

- `scraper/otp/result.json` — raw nested output (preserves internal link structure)
- `scraper/otp/summarize.json` — flattened, deduplicated summary

### Example output (`summarize.json`)

```json
{
  "https://clinicadental-valencia.com": {
    "emails": ["contacto@clinicadental-valencia.com", "info@clinicadental-valencia.com"],
    "linkedins": ["linkedin.com/in/dr-jose-garcia"],
    "twitters": ["twitter.com/clinicavalencia"],
    "titles": ["Director", "CEO"],
    "cif": ["B12345678"],
    "nif": [],
    "addresses": ["Calle Colón 12, 46004"],
    "whatsapps": ["wa.me/34612345678"]
  }
}
```

---

## Installation

**Requirements:** Python 3.11+

```bash
# Clone the repo
git clone https://github.com/your-username/contact-harvest.git
cd contact-harvest

# Create and activate a virtual environment
python3 -m venv business_scraper
source business_scraper/bin/activate

# Install dependencies
pip install requests rich playwright aiohttp

# Install Chromium for Playwright
playwright install chromium
```

---

## Usage

### 1. Create your query generator

The query generator is not included — write your own to target your industry and location. See [Writing a query generator](#writing-a-query-generator) below.

Your generator must produce a `queries/queries.txt` file with one search query per line:

```
clínica dental Valencia
fisioterapia Madrid
restaurante Barcelona
```

### 2. Run the scraper

```bash
python main.py
```

Results are saved to `scraper/otp/result.json` and `scraper/otp/summarize.json`.

---

## Writing a query generator

Create a `generate_queries.py` file at the root of the project. The only requirement is that it writes one query per line to `queries/queries.txt`.

Here's a minimal example you can adapt:

```python
"""
generate_queries.py — customize BUSINESS_TERMS and LOCATIONS for your use case.
Run with: python generate_queries.py
"""

LOCATIONS = [
    "Madrid",
    "Barcelona",
    "Seville",
]

BUSINESS_TERMS = [
    "dental clinic",
    "physiotherapy",
    "personal trainer",
    "language academy",
    "mechanic workshop",
]

def generate_queries(terms, locations):
    return [f"{term} {location}" for term in terms for location in locations]

if __name__ == "__main__":
    queries = generate_queries(BUSINESS_TERMS, LOCATIONS)
    with open("queries/queries.txt", "w", encoding="UTF-8") as f:
        f.write("\n".join(queries))
    print(f"Generated {len(queries)} queries → queries/queries.txt")
```

This produces queries like `"dental clinic Madrid"`, `"physiotherapy Barcelona"`, etc. Use any language, industry, or set of cities you need.

---

## Configuration

| Variable | File | Default | Description |
|---|---|---|---|
| `MAX_QUERIES` | `main.py` | `34` | How many queries are randomly sampled per run |
| `MAX_DEPTH` | `scraper/scrapeSources.py` | `1` | How many levels of internal links to follow |

---

## Extracted fields

| Field | Description |
|---|---|
| `emails` | Email addresses (file extension false-positives filtered out) |
| `linkedins` | LinkedIn profile URLs |
| `twitters` | Twitter / X handles |
| `titles` | Job titles (CEO, CTO, Director, Founder, etc.) |
| `cif` | Spanish company tax ID |
| `nif` | Spanish personal tax ID |
| `addresses` | Street addresses |
| `whatsapps` | WhatsApp contact links |

---

## Project structure

```
contact-harvest/
├── main.py                  # Pipeline entry point
├── queries/
│   └── queries.txt          # One search query per line (generated)
└── scraper/
    ├── getURLs.py           # Google search via Playwright
    ├── scrapeSources.py     # Async HTTP scraper + data extraction
    ├── otp/
    │   ├── result.json      # Raw nested output
    │   └── summarize.json   # Flattened output
    └── util/
        ├── statusMessage.py # Colored logging (Rich)
        └── summarize.py     # Flatten + dedup logic
```

---

## License

MIT
