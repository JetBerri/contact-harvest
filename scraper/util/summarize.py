FIELDS = ("emails", "phones", "linkedins", "twitters", "titles", "cif", "nif", "addresses", "whatsapps")

def summarize(dict_output):

    summary = {}

    for url, entry in dict_output.items():

        merged = {field: [] for field in FIELDS}

        # Collect from top-level entry

        for field in FIELDS:
        
            merged[field].extend(entry.get(field, []))

        # Collect from internal pages
        
        for internal_entry in entry.get("internal", {}).values():
        
            for field in FIELDS:
        
                merged[field].extend(internal_entry.get(field, []))

        # Deduplicate preserving order
        
        summary[url] = {field: list(dict.fromkeys(merged[field])) for field in FIELDS}

    return summary
