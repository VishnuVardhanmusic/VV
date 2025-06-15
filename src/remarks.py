import json
import os
from datetime import datetime

def format_review_remark(issue):
    """
    Create a human-readable review remark from a flagged issue.

    Args:
        issue: dict with keys like line_number, code, matched_rule, description, suggestion

    Returns:
        Formatted remark dict
    """
    return {
        "line_number": issue["line_number"],
        "rule_id": issue.get("matched_rule", "N/A"),
        "description": issue.get("description", "No description"),
        "code": issue.get("code", "").strip(),
        "suggestion": issue.get("suggestion", "Please review this line against the guideline.")
    }


def write_remarks_to_json(issues, output_path="review_output"):
    """
    Write all review remarks to a timestamped JSON file.

    Args:
        issues: list of flagged issues from rule_engine + LLM
        output_path: directory to store the output file
    """
    os.makedirs(output_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"remarks_{timestamp}.json"
    file_path = os.path.join(output_path, filename)

    formatted_remarks = [format_review_remark(issue) for issue in issues]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_remarks, f, indent=4)

    print(f"Review remarks saved at: {file_path}")
    return file_path
