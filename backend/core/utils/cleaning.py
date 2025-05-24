import re

def extract_resume_commentary(text):
    # This grabs the last line if it looks like commentary
    lines = text.strip().split("\n")
    possible_tip = lines[-1]
    if any(phrase in possible_tip.lower() for phrase in ["i tried to highlight", "please let me know", "customization", "tip"]):
        return possible_tip
    return ""
def clean_resume_output(text):
    # Basic cleanup: strip whitespace and markdown noise
    cleaned = text.strip()

    patterns_to_remove = [
        r"(?i)please let me know.*",  # Matches "Please let me know..." in any casing
        r"(?i)if you need.*",         # Matches other common AI-style phrases
        r"(?i)thank you.*",           # Optional catch-all
    ]

    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, "", cleaned).strip()

    return cleaned
