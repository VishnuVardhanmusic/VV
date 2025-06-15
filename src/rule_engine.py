import json
import re

def load_guidelines(guidelines_path: str) -> list:
    """
    Load the embedded guidelines JSON file.

    Returns:
        List of rule dictionaries.
    """
    try:
        with open(guidelines_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get("guidelines", [])
    except Exception as e:
        print(f"Error loading guidelines: {e}")
        return []

def match_guidelines_to_code(parsed_lines: list, rules: list) -> list:
    """
    Match code lines to rules using regex patterns.

    Args:
        parsed_lines: List of dicts from file_parser.py
        rules: List of hybrid-format guideline dicts

    Returns:
        List of flagged lines with matched rule context
    """
    flagged = []

    for line in parsed_lines:
        code = line["code"]
        line_num = line["line_number"]

        for rule in rules:
            pattern = rule.get("pattern", "")
            if not pattern:
                continue
            try:
                if re.search(pattern, code):
                    flagged.append({
                        "line_number": line_num,
                        "code": code,
                        "matched_rule": rule["id"],
                        "guideline": rule["guideline"],
                        "description": rule["description"],
                        "tags": rule.get("tags", []),
                        "applies_to": rule.get("applies_to", []),
                        "phase": rule.get("phase", "Unknown")
                    })
                    break  # Only the first match is needed
            except re.error as err:
                print(f"⚠️ Invalid regex in rule {rule['id']}: {err}")
                continue

    return flagged
