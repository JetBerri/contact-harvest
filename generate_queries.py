"""
Generates queries combining business terms and locations,
and writes them to queries/queries.txt.
"""

LOCATIONS = [
    "Valencia",
]

# --- Reservation & appointment-based small businesses ---
BUSINESS_TERMS = [

    # Health & wellness (appointment-driven)
    "clínica dental",
    "fisioterapia",
    "psicólogo",
    "clínica estética",
    "centro de masajes",
    "osteopatía",
    "nutricionista",
    "podólogo",
    "logopeda",
    "acupuntura",

    # Beauty & personal care
    "peluquería",
    "barbería",
    "centro de uñas",
    "salón de belleza",
    "depilación láser",
    "microblading",

    # Fitness & sports
    "entrenador personal",
    "academia de baile",
    "pilates",
    "yoga",
    "crossfit",
    "artes marciales",

    # Hospitality & food (reservation-based)
    "restaurante",
    "restaurante de cocina mediterránea",
    "asador",
    "marisquería",
    "restaurante arrocería",

    # Education & tutoring
    "academia de idiomas",
    "clases particulares",
    "academia de música",
    "autoescuela",

    # Repair & home services (appointment-based)
    "taller mecánico",
    "servicio técnico electrodomésticos",
    "empresa de reformas",

]

# --- Original general business terms (kept for reference) ---
# BUSINESS_TERMS = [
#
#     # Marketing & digital
#     "marketing digital",
#     "agencia de publicidad",
#     "diseño web",
#     "SEO consultoría",
#     "community manager",
#     "agencia de comunicación",
#
#     # Business & consulting
#     "consultoría empresarial",
#     "asesoría fiscal",
#     "asesoría laboral",
#     "gestoría",
#     "despacho de abogados",
#     "arquitecto",
#
#     # Health
#     "clínica dental",
#     "clínica médica",
#     "fisioterapia",
#     "psicólogo",
#     "clínica estética",
#     "veterinario",
#     "óptica",
#
#     # Education & training
#     "academia de idiomas",
#     "autoescuela",
#     "centro de formación",
#
#     # Retail & services
#     "inmobiliaria",
#     "empresa de reformas",
#     "fontanero",
#     "electricista",
#     "empresa de limpieza",
#     "catering",
#     "floristería",
#     "fotografía profesional",
#
#     # Hospitality
#     "restaurante",
#     "hotel boutique",
#     "cafetería",
# ]

def generate_queries(business_terms, locations):

    queries = []

    for term in business_terms:

        for location in locations:

            queries.append(f"{term} {location}")

    return queries


if __name__ == "__main__":

    queries = generate_queries(BUSINESS_TERMS, LOCATIONS)

    output_path = "queries/queries.txt"

    with open(output_path, "w", encoding="UTF-8") as f:

        f.write("\n".join(queries))

    print(f"Generated {len(queries)} queries → {output_path}")
