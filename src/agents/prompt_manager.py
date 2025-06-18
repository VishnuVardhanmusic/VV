from collections import defaultdict
from typing import List, Dict

def buildPrompt(codeLines: List[Dict], guidelineRules: List[Dict]) -> str:
    """
    Constructs a structured prompt to send to the LLM for code review.

    Args:
        codeLines (List[Dict]): List of code lines with line numbers.
        guidelineRules (List[Dict]): List of coding guideline rules.

    Returns:
        str: Final prompt string to be fed into the LLM.
    """

    # 1️⃣ Group by category
    groupedRules = defaultdict(list)
    for rule in guidelineRules:
        category = rule.get('category', 'General')
        groupedRules[category].append(rule)

    # 2️⃣ Format guidelines section
    formattedGuidelines = "### 🧾 Embedded C Coding Guidelines:\n"
    for category, rules in groupedRules.items():
        formattedGuidelines += f"\n📌 {category} Guidelines:\n"
        for rule in rules:
            formattedGuidelines += (
                f"- ({rule['id']}) {rule['description']} [Severity: {rule['severity']}]\n"
                f"  ↪ Suggestion: {rule['suggestion']}\n"
            )

    # 3️⃣ Format C code
    formattedCode = "\n### 🧩 Code to Review:\n"
    for line in codeLines:
        formattedCode += f"{line['lineNumber']:>3}: {line['codeLine']}\n"

    # 4️⃣ Add review instructions
    instructions = """
### 🎯 Task for AI Agent:
You are an expert reviewer of Embedded C code. Your job is to check the code against the listed guidelines.

Return a JSON list of violations in this structure:
[
  {
    "lineNumber": 12,
    "ruleViolated": "G001",
    "description": "Avoid usage of ## operator",
    "severity": "high",
    "explanation": "Found use of '##' which is discouraged.",
    "suggestedFix": "Use clearer macro definitions without token pasting."
  },
  ...
]

If no issues are found, simply return: []
"""

    return f"{formattedGuidelines}\n\n{formattedCode}\n\n{instructions}"
