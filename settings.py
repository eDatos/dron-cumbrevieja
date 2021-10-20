from prettyconf import config

# Open Data La Palma
ODLP_BASE_URL = config(
    "ODLP_BASE_URL",
    default=(
        "https://www.opendatalapalma.es/search?collection=Dataset"
        "&q=perimetro%20dron&sort=-modified&type=feature%20layer"
    ),
)
