def buildPrompt(codeLines, guidelineRules):
    """
    Constructs a prompt string to send to an LLM for code review.

    Args:
        codeLines (List[Dict]): List of code lines with line numbers.
        guidelineRules (List[Dict]): List of coding guideline dictionaries.

    Returns:
        str: Final prompt to feed into the LLM.
    """

    # Group guidelines by 'category'
    from collections import defaultdict
    groupedRules = defaultdict(list)
    for rule in guidelineRules:
        category = rule.get('category', 'General')
        groupedRules[category].append(rule)

    # 1️⃣ Format grouped guideline section
    formattedGuidelines = "### Coding Guidelines:\n"
    for category, rules in groupedRules.items():
        formattedGuidelines += f"\n📌 {category} Guidelines:\n"
        for rule in rules:
            formattedGuidelines += (
                f"- ({rule['id']}) {rule['description']} [Severity: {rule['severity']}]\n"
                f"  ↪ Suggestion: {rule['suggestion']}\n"
            )

    # 2️⃣ Format code section
    formattedCode = "\n### C Code to Review:\n"
    for line in codeLines:
        formattedCode += f"{line['lineNumber']:>3}: {line['codeLine']}\n"

    # 3️⃣ Add review instruction
    reviewInstruction = """
### Task for AI Agent:
You are a code reviewer specialized in embedded C development.

Review the code strictly against the provided coding guidelines grouped by category.

For each line that violates a rule, return a structured JSON object with the following fields:
[
  {
    "lineNumber": <int>,                 // Line in source code with violation
    "ruleViolated": "<rule_id>",         // Guideline ID such as G001, G014 etc.
    "description": "<rule description>", // Short title of what rule is violated
    "severity": "<low|medium|high|critical>", // Rule's severity
    "explanation": "<why it violates the rule>",
    "suggestedFix": "<precise improvement or safer approach>"
  }
]

If no violations exist, return an **empty list: []** only.
"""
    # 4️⃣ Combine all
    finalPrompt = f"{formattedGuidelines}\n\n{formattedCode}\n\n{reviewInstruction}"
    return finalPrompt
