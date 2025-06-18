from langchain_core.language_models import BaseChatModel
from langchain.chat_models import ChatLiteLLM
from langchain_core.messages import HumanMessage

# Initialize Claude model via LiteLLM proxy
llm = ChatLiteLLM(
    model="anthropic.claude-3-5-sonnet-20241022-v2:0",  # Claude model name
    api_key="your_dummy_litellm_api_key",              # Replace with actual key
    proxy_url="http://localhost:8000"                  # Replace with actual LiteLLM proxy URL
)

def getClaudeResponse(prompt: str) -> str:
    """
    Sends the prompt to Claude 3.5 Sonnet via LangChain + LiteLLM Proxy
    and returns the raw string response.
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        print(f"❌ Error in Claude model invocation: {e}")
        return "ERROR: LLM invocation failed."
