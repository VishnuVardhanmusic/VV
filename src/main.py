import argparse
from rule_loader import loadGuidelines
from code_loader import readCodeFile
from prompt_manager import buildPrompt
from review_engine import runReview, saveReviewToFile

def main():
    parser = argparse.ArgumentParser(description="Embedded C Code Reviewer")
    parser.add_argument("filepath", help="Path to input .c or .h file")
    parser.add_argument("--guidelines", default="guidelines/c_guidelines.json", help="Path to guideline JSON file")
    parser.add_argument("--output", default="code_review.json", help="Path to save JSON review result")
    args = parser.parse_args()

    try:
        print("📥 Loading guidelines...")
        rules = loadGuidelines(args.guidelines)

        print("📄 Reading source code...")
        code = readCodeFile(args.filepath)

        print("✍️  Building review prompt...")
        prompt = buildPrompt(code, rules)

        print("🤖 Reviewing code via Claude 3.5 (LangChain)...")
        reviewResult = runReview(prompt)

        print("💾 Saving review remarks...")
        saveReviewToFile(reviewResult, args.output)

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
