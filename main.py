import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import json
from dotenv import load_dotenv
from file_parser import parse_input_file
from rule_engine import load_guidelines, match_guidelines_to_code
from remarks import write_remarks_to_json
from llm_validator import LLMGuidelineValidator
from reviewer_chain import CodeReviewer
from langchain_litellm import ChatLiteLLM
 

# Step 1: Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-5-sonnet-20240620")
BASE_URL = os.getenv("LITELLM_PROXY_BASE_URL")
API_KEY = os.getenv("LITELLM_API_KEY", "ignore")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4096))

# Step 2: File input path
INPUT_FILE_PATH = "input/test_bad.c"
OUTPUT_JSON_PATH = "output/review_output.json"
GUIDELINES_PATH = "guidelines/embedded_guidelines.json"

def main():
    print("🔧 Starting Embedded Review Agent...")

    # Step 3: Parse the input .c file
    parsed_code_lines = parse_input_file(INPUT_FILE_PATH)
    print(f"📄 Parsed {len(parsed_code_lines)} code lines from input.")

    # Step 4: Load all known embedded guidelines
    guideline_rules = load_guidelines(GUIDELINES_PATH)

    # Step 5: Match potential applicable rules per code line
    flagged_lines = match_guidelines_to_code(parsed_code_lines, guideline_rules)

    if not flagged_lines:
        print("✅ No immediate red flags found. Code looks clean.")
        write_remarks_to_json([], OUTPUT_JSON_PATH)
        return

    # Step 6: Set up real Claude LLM
    print("🤖 Sending flagged lines for Claude LLM review...")
    llm = ChatLiteLLM(
        model=MODEL_NAME,
        api_base=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    llm_validator = LLMGuidelineValidator(
        model_name=MODEL_NAME,
        api_base=BASE_URL,
        api_key=API_KEY,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        llm=llm  # ✅ pass real model instance
    )

    reviewer = CodeReviewer(llm_validator)

    # Step 7: Run the review
    final_remarks = reviewer.run_review(flagged_lines, guideline_rules)

    # Step 8: Save remarks to JSON
    write_remarks_to_json(final_remarks, OUTPUT_JSON_PATH)
    print(f"📁 Review complete. Remarks saved to: {OUTPUT_JSON_PATH}")

if __name__ == "__main__":
    main()
