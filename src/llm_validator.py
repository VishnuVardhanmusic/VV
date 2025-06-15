from typing import List, Dict
from langchain_core.language_models.chat_models import BaseChatModel

class LLMGuidelineValidator:
    def __init__(self, model_name, api_base, api_key, temperature=0.2, max_tokens=4096, llm: BaseChatModel = None):
        self.model = model_name
        self.base_url = api_base
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm = llm  # should be a real model instance, not a class

    def validate_code(self, code_chunk: str, rules: List[Dict]) -> List[Dict]:
        prompt = self._generate_prompt(code_chunk, rules)

        if not self.llm:
            raise ValueError("LLM instance not set. Pass a valid model instance during initialization.")

        response = self.llm.invoke(prompt)

        try:
            remarks = response.content
            return eval(remarks) if isinstance(remarks, str) else remarks
        except Exception as e:
            return [{
                "line": 0,
                "rule_id": "ERROR",
                "remark": f"Failed to parse LLM response: {e}",
                "severity": "high",
                "tags": ["parsing"]
            }]

    def _generate_prompt(self, code_chunk: str, rules: List[Dict]) -> str:
        return f"""
You are an embedded C code reviewer bot. You are given a chunk of code and a set of coding guidelines.
Check if the code violates any of the rules. If so, provide remarks as JSON list.

Each remark should contain:
- line: Line number (if unknown or spans multiple lines, set to 0)
- rule_id: Unique rule identifier (e.g., A1, C2)
- remark: Explanation of what’s wrong
- severity: "low", "medium", or "high"
- tags: List of related tags like ["safety", "naming", "formatting"]

Respond ONLY with the JSON list.

== CODE START ==
{code_chunk}
== CODE END ==

== RULES ==
{rules}
== END ==
"""
