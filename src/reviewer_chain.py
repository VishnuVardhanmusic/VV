from typing import List, Dict
from llm_validator import LLMGuidelineValidator

class CodeReviewer:
    def __init__(self, llm_validator: LLMGuidelineValidator):
        self.llm_validator = llm_validator

    def run_review(
        self,
        code_chunks: List[Dict[str, str]],
        guidelines: List[Dict]
    ) -> List[Dict]:
        """
        Run LLM-based code review for given code chunks against guidelines.

        Parameters:
        - code_chunks: List of dicts with keys 'code' and 'line_start'
        - guidelines: List of guideline rules from JSON knowledge base

        Returns:
        - List of remark dicts
        """
        all_remarks = []

        for chunk in code_chunks:
            remarks = self.llm_validator.validate_code(chunk["code"], guidelines)

            for remark in remarks:
                # Update line number offset if LLM returned relative positions
                if remark.get("line", 0) > 0:
                    remark["line"] += chunk["line_start"] - 1
                all_remarks.append(remark)
        return all_remarks