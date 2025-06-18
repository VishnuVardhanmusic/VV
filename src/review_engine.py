import litellm
import json
import os

def runReview(prompt, model="ollama/llama3", max_tokens=2048):
    """
    Sends the prompt to the specified LLM using LiteLLM and returns JSON feedback.

    Args:
        prompt (str): The prompt to review code.
        model (str): The model identifier in LiteLLM config.
        max_tokens (int): Token limit for the response.

    Returns:
        list: List of JSON review remarks returned by the model.
    """
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=max_tokens
        )
        import re
        output = response['choices'][0]['message']['content']

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
        print("📝 Response:\n", output)
        return []
    except Exception as e:
        print("❌ Error calling model:", str(e))
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
