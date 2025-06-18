import json
import os

def loadGuidelines(jsonPath: str):
    """
    Loads embedded C coding guidelines from a JSON file.

    Args:
        jsonPath (str): Path to the JSON file.

    Returns:
        List[Dict]: List of guideline dictionaries.
    """
    if not os.path.exists(jsonPath):
        raise FileNotFoundError(f"❌ Guideline file not found: {jsonPath}")

    with open(jsonPath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Expected JSON array of rules")
            for rule in data:
                if 'id' not in rule or 'pattern' not in rule:
                    raise ValueError("Each rule must contain 'id' and 'pattern'")
            return data
        except json.JSONDecodeError:
            raise ValueError(f"❌ Failed to parse JSON from: {jsonPath}")
