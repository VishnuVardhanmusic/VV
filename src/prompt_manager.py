def buildPrompt(codeLines, guidelineRules):
    """
    Constructs a prompt string to send to an LLM for code review.

    Args:
        codeLines (List[Dict]): List of code lines with line numbers.
        guidelineRules (List[Dict]): List of coding guideline dictionaries.

    Returns:
        str: Final prompt to feed into the LLM.
    """

    # 1️⃣ Format guideline section
    formattedGuidelines = "### Coding Guidelines:\n"
    for rule in guidelineRules:
        formattedGuidelines += f"- ({rule['id']}) {rule['description']} [Severity: {rule['severity']}]\n  ↪ Suggestion: {rule['suggestion']}\n"

    # 2️⃣ Format code section
    formattedCode = "### C Code to Review:\n"
    for line in codeLines:
        formattedCode += f"{line['lineNumber']:>3}: {line['codeLine']}\n"

    # 3️⃣ Add review instruction
    reviewInstruction = """
### Task for AI Agent:
You are a code reviewer specialized in embedded C development.

Review the above code **strictly** against the listed coding guidelines.

For any violation, return a JSON list with the following format:
[
  {
    "lineNumber": 12,
    "ruleViolated": "G001",
    "explanation": "Usage of '##' token pasting found.",
    "suggestedFix": "Avoid macro token pasting. Consider better macro design."
  },
  ...
]

If the code is clean and no violations exist, return an **empty list: []**.
"""

    # 4️⃣ Combine all
    finalPrompt = f"{formattedGuidelines}\n\n{formattedCode}\n\n{reviewInstruction}"
    return finalPrompt
