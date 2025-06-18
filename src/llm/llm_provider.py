from pydantic_ai.openai import OpenAIChat
from typing import Optional

class PydanticClaudeAgent:
    """
    Wraps a Claude LLM hosted via LiteLLM proxy and exposes a simple `getReview` method.
    """

    def __init__(self, proxy_url: str, model_name: str, api_key: str):
        """
        Initializes the Claude agent with required LiteLLM proxy details.
        """
        self.llm = OpenAIChat(
            base_url=proxy_url,
            api_key=api_key,
            model=model_name,
            temperature=0.0,
            max_tokens=2048,
        )

    def getReview(self, prompt: str) -> Optional[list]:
        """
        Sends the constructed prompt to Claude and returns the parsed JSON result.

        Args:
            prompt (str): The full prompt built from the C code and guidelines.

        Returns:
            list or None: Parsed JSON list of violations, or None on error.
        """
        try:
            response = self.llm(prompt)
            return response.json() if hasattr(response, "json") else eval(response)
        except Exception as e:
            print(f"❌ Error during LLM call: {e}")
            return None
