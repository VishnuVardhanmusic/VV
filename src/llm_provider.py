from langchain.llms.base import LLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import requests

class ClaudeViaProxy(LLM):
    def __init__(self, proxy_url: str, api_key: str, model_name: str):
        self.proxy_url = proxy_url
        self.api_key = api_key
        self.model_name = model_name

    @property
    def _llm_type(self) -> str:
        return "custom_claude_proxy"

    def _call(self, prompt: str, stop=None, run_manager=None) -> str:
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 2048
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.proxy_url, json=payload, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"❌ Error from proxy: {response.status_code} - {response.text}")

        return response.json()['choices'][0]['message']['content']


# Example usage
def getClaudeChain():
    proxy_url = "http://localhost:8000/v1/chat/completions"  # 🔁 Replace with your actual proxy endpoint
    api_key = "your-dummy-key"  # 🔐 Replace with actual token
    model_name = "anthropic.claude-3-5-sonnet-20241022-v2:0"

    llm = ClaudeViaProxy(proxy_url=proxy_url, api_key=api_key, model_name=model_name)

    # Define generic prompt template
    prompt_template = PromptTemplate(
        input_variables=["code_review_prompt"],
        template="{code_review_prompt}"
    )

    # Return the review chain
    return LLMChain(llm=llm, prompt=prompt_template)
