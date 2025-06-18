import json
import re
from llm_provider import getClaudeResponse

def runReview(prompt):
    """
    Sends the prompt to Claude 3.5 Sonnet via LangChain-LiteLLM and returns JSON feedback.

    Args:
        prompt (str): The complete prompt to review code.

    Returns:
        list: Parsed list of review remarks in JSON format.
    """
    try:
        output = getClaudeResponse(prompt)

        # Extract the first valid JSON array from the response using regex
        json_match = re.search(r'\[\s*{.*?}\s*\]', output, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            review_json = json.loads(json_str)
            return review_json
        else:
            print("❌ Could not extract valid JSON array from Claude response.")
            print("📝 Raw Output:\n", output)
            return []

    except json.JSONDecodeError:
        print("❌ Claude response was not valid JSON.")
        print("📝 Response:\n", output)
        return []
    except Exception as e:
        print("❌ Error calling Claude via LangChain:", str(e))
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
