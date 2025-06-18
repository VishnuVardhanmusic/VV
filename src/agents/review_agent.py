from pydantic_ai.chat import ChatMessage, chat_completion
from src.agents.prompt_manager import buildPrompt

def runReviewAgent(codeLines, guidelineRules, model_name, proxy_url, api_key):
    """
    Runs the AI code review agent using Pydantic-AI and LiteLLM proxy.

    Args:
        codeLines (List[Dict]): Parsed C code with line numbers.
        guidelineRules (List[Dict]): Coding guideline entries.
        model_name (str): The Claude model name.
        proxy_url (str): The LiteLLM proxy URL.
        api_key (str): API key to authenticate with the proxy.

    Returns:
        List[Dict]: LLM response containing review remarks or empty list.
    """
    try:
        prompt = buildPrompt(codeLines, guidelineRules)

        messages = [
            ChatMessage(role="user", content=prompt)
        ]

        result = chat_completion(
            model=model_name,
            messages=messages,
            base_url=proxy_url,
            api_key=api_key,
            max_tokens=2048,
            temperature=0.0
        )

        return result.content

    except Exception as e:
        print(f"🚨 Error during AI review: {e}")
        return "[]"
