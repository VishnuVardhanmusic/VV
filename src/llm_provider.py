import requests
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.base import LLM


class LiteLLMProxy(LLM):
    def __init__(self, base_url: str, model: str, api_key: str = "dummy"):
        self.base_url = base_url
        self.model = model
        self.api_key = api_key

    @property
    def _llm_type(self):
        return "lite_llm_proxy"

    def _call(self, prompt: str, stop=None, run_manager=None) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 2048
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(f"{self.base_url}/v1/chat/completions", json=payload, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"❌ LLM Error: {response.status_code} — {response.text}")

        return response.json()["choices"][0]["message"]["content"]


def getClaudeChain():
    llm = LiteLLMProxy(
        base_url="http://localhost:4000",
        model="anthropic.claude-3-5-sonnet-20241022-v2:0"
    )

    prompt_template = PromptTemplate(
        input_variables=["code_review_prompt"],
        template="{code_review_prompt}"
    )

    return LLMChain(llm=llm, prompt=prompt_template)
