import json
import re
from llm_provider import getClaudeChain

def runReview(prompt, max_tokens=2048):
    """
    Sends the prompt to the Claude model via LangChain and returns JSON feedback.

    Args:
        prompt (str): The prompt to review code.
        max_tokens (int): Token limit (still passed to LLM config).

    Returns:
        list: List of JSON review remarks returned by the model.
    """
    try:
        chain = getClaudeChain()
        output = chain.run(code_review_prompt=prompt)

        # Extract first valid JSON array using regex
        json_match = re.search(r'\[\s*{.*?}\s*\]', output, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            review_json = json.loads(json_str)
            return review_json
        else:
            print("❌ Could not extract valid JSON array from LLM response.")
            print("📝 Raw Output:\n", output)
            return []

    except json.JSONDecodeError:
        print("❌ LLM response was not valid JSON.")
        return []
    except Exception as e:
        print("❌ Error during review:", str(e))
        return []


def saveReviewToFile(reviewData, outputPath="code_review.json"):
    """
    Saves the final review remarks to a JSON file.

    Args:
        reviewData (list): List of remark dictionaries.
        outputPath (str): Path to the output file.
    """
    with open(outputPath, 'w') as f:
        json.dump(reviewData, f, indent=4)
    print(f"✅ Review saved to: {outputPath}")
