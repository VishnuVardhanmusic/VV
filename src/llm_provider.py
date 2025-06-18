from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage


def getClaudeChain():
    """
    Returns an LLMChain configured to send prompts to Claude 3.5 via LiteLLM proxy.
    """
    # Replace with your LiteLLM proxy URL and configured model
    base_url = "http://localhost:4000"
    model_name = "anthropic.claude-3-5-sonnet-20241022-v2:0"

    # Instantiate LangChain-compatible Claude model via LiteLLM proxy
    llm = ChatOpenAI(
        base_url=base_url,
        api_key="dummy-key",  # LiteLLM ignores this field
        model=model_name,
        temperature=0.0
    )

    # Define pass-through prompt template
    prompt_template = PromptTemplate(
        input_variables=["code_review_prompt"],
        template="{code_review_prompt}"
    )

    return LLMChain(llm=llm, prompt=prompt_template)


def callClaudeLLM(prompt: str, max_tokens: int = 2048) -> str:
    """
    Sends prompt to Claude 3.5 via the LangChain chain abstraction.
    """
    chain = getClaudeChain()
    result = chain.run({"code_review_prompt": prompt})
    return result
