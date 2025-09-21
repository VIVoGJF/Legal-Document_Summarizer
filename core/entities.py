import re
import spacy
import yaml
from pathlib import Path

# -------------------------
# Load configuration (risk keywords etc. can live here later too)
# -------------------------
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"

if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
else:
    config = {}

# Load spaCy English model
try:
    nlp = spacy.load(config.get("spacy_model", "en_core_web_sm"))
except OSError:
    raise RuntimeError(
        "SpaCy model not found. Install with: python -m spacy download en_core_web_sm"
    )


# -------------------------
# Date extraction
# -------------------------
def extract_dates(text: str) -> list[str]:
    
    date_patterns = [
        r"\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b",       # 12/05/2021, 12-05-21, 12.05.2021
        r"\b\d{4}[/.-]\d{1,2}[/.-]\d{1,2}\b",         # 2021-05-12
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b", # July 19, 2025
        r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*,?\s+\d{2,4}\b", # 19 July 2025
        r"\b\d+\s+(days?|weeks?|months?|years?)\b",   # 7 months, 10 years
        r"\b[\(\[\{<\-*]?\d+[\)\]\}>\-*]?\s+(days?|weeks?|months?|years?)\b",  # (3) years, -2 years-
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten|twelve)\s+(days?|weeks?|months?|years?)\b",
    ]

    contextual_dates = []
    for pattern in date_patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            date_val = match.group()

            # Capture surrounding context (50 chars before/after)
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context_snippet = text[start:end].replace("\n", " ").strip()

            contextual_dates.append(f"<b>{context_snippet}:</b> {date_val}")

    # Deduplicate while keeping order
    seen = set()
    contextual_dates = [x for x in contextual_dates if not (x in seen or seen.add(x))]

    return contextual_dates if contextual_dates else ["Not specified"]


# -------------------------
# Entity extraction pipeline
# -------------------------
def extract_entities(text: str) -> dict:

    doc = nlp(text)

    parties = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON"]]
    money = [ent.text for ent in doc.ents if ent.label_ == "MONEY"]

    obligations = re.findall(
        r"\b(shall|must|agree to|responsible for)\b.*?\.",
        text,
        flags=re.IGNORECASE,
    )

    entities = {
        "Parties": list(set(parties)) or ["Not specified"],
        "Dates": extract_dates(text),
        "Money/Penalties": list(set(money)) or ["Not specified"],
        "Obligations": obligations or ["Not specified"],
    }

    return entities
