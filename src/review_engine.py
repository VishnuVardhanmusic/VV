import os
import json

from src.loaders.rule_loader import loadGuidelines
from src.loaders.code_loader import parseCodeFile
from src.agents.prompt_manager import buildPrompt
from src.llm.llm_provider import PydanticClaudeAgent

def runReview(
    inputCodePath: str,
    guidelinePath: str,
    outputPath: str,
    proxy_url: str,
    model_name: str,
    api_key: str
) -> None:
    """
    Executes the end-to-end code review pipeline:
    1. Loads guidelines
    2. Loads C source code
    3. Builds the prompt
    4. Queries Claude LLM via proxy
    5. Saves review output to JSON

    Args:
        inputCodePath (str): Path to the C/C++ source file.
        guidelinePath (str): Path to the guideline JSON file.
        outputPath (str): Path to store the output JSON.
        proxy_url (str): LiteLLM proxy endpoint.
        model_name (str): Claude model name.
        api_key (str): Authorization token for LiteLLM.
    """

    print("🚀 Starting Code Review Agent...\n")

    # 1️⃣ Load rules
    rules = loadGuidelines(guidelinePath)
    print(f"✅ Loaded {len(rules)} coding rules.")

    # 2️⃣ Load input C code
    codeLines = parseCodeFile(inputCodePath)
    print(f"📄 Loaded {len(codeLines)} lines from code file.")

    # 3️⃣ Build review prompt
    prompt = buildPrompt(codeLines, rules)

    # 4️⃣ Call Claude via Pydantic-AI
    llm = PydanticClaudeAgent(proxy_url, model_name, api_key)
    review_result = llm.getReview(prompt)

    if review_result is None:
        print("❌ Review failed. No output generated.")
        return

    # 5️⃣ Save output to JSON
    os.makedirs(os.path.dirname(outputPath), exist_ok=True)
    with open(outputPath, 'w') as out_file:
        json.dump(review_result, out_file, indent=4)
        print(f"✅ Review saved to {outputPath}")

